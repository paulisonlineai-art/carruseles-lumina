#!/usr/bin/env python3
"""Alerta cuando se agotan las fotos de portada (Valu/Sofi) para rotarlas sin repetir."""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).parent.parent

def analizar_disponibilidad_portadas():
    """Analiza disponibilidad de fotos de portada y alerta si quedan pocas."""

    reg_path = PROJECT_ROOT / "registro.md"
    if not reg_path.exists():
        return []

    registro = reg_path.read_text()
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    hace_3_dias = hoy - timedelta(days=3)

    # Cuenta fotos de Valu usadas en últimos 7 días
    fotos_valu_usadas = set()
    fotos_sofia_usadas = set()

    # Busca secciones de fecha
    fecha_pattern = r"## (\d{4}-\d{2}-\d{2})"
    fechas_encontradas = re.findall(fecha_pattern, registro)

    for fecha_str in fechas_encontradas:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            if fecha >= hace_7_dias:
                # Busca portadas en esta sección
                seccion_start = registro.find(f"## {fecha_str}")
                seccion_end = registro.find("## ", seccion_start + 1)
                if seccion_end == -1:
                    seccion_end = len(registro)
                seccion = registro[seccion_start:seccion_end]

                # Extrae fotos de portada
                valu_match = re.search(r"- Portada: (valu-\d+\.jpg)", seccion)
                if valu_match:
                    fotos_valu_usadas.add(valu_match.group(1))

                sofia_match = re.search(r"- Portada: (sofia-\S+\.jpg)", seccion)
                if sofia_match:
                    fotos_sofia_usadas.add(sofia_match.group(1))
        except:
            pass

    # Cuenta fotos disponibles
    fotos_valu_total = len(list((PROJECT_ROOT / "fotos" / "valu").glob("valu-*.jpg")))
    fotos_sofia_total = len(list((PROJECT_ROOT / "fotos" / "sofia").glob("sofia-*.jpg")))

    alertas = []

    # Valu: alerta si quedan pocas (menos de 5 sin usar en 7 días)
    fotos_valu_disponibles = fotos_valu_total - len(fotos_valu_usadas)
    if fotos_valu_disponibles < 5:
        alertas.append({
            "cuenta": "@valu.manifiesta",
            "total": fotos_valu_total,
            "usadas_7dias": len(fotos_valu_usadas),
            "disponibles": fotos_valu_disponibles,
            "urgencia": "CRÍTICA" if fotos_valu_disponibles < 3 else "ALTA",
            "mensaje": f"⚠ Valu: {fotos_valu_disponibles} fotos disponibles. Necesita rotación de portadas."
        })

    # Sofi: alerta si quedan pocas (menos de 3 sin usar en 3 días)
    fotos_sofia_disponibles = fotos_sofia_total - len(fotos_sofia_usadas)
    if fotos_sofia_disponibles < 3:
        alertas.append({
            "cuenta": "@manifiesta.con.sofia",
            "total": fotos_sofia_total,
            "usadas_3dias": len(fotos_sofia_usadas),
            "disponibles": fotos_sofia_disponibles,
            "urgencia": "CRÍTICA" if fotos_sofia_disponibles < 2 else "ALTA",
            "mensaje": f"⚠ Sofi: {fotos_sofia_disponibles} fotos disponibles. Necesita rotación de portadas."
        })

    return alertas

def mostrar_alertas():
    """Muestra alertas en consola."""
    alertas = analizar_disponibilidad_portadas()

    if not alertas:
        print("✓ Fotos de portada OK (suficientes sin repetir)")
        return

    print("\n" + "="*60)
    print("⚠ ALERTAS DE ROTACIÓN DE FOTOS DE PORTADA")
    print("="*60)

    for alerta in alertas:
        print(f"\n{alerta['mensaje']}")
        print(f"  Total disponibles: {alerta['total']}")
        if 'usadas_7dias' in alerta:
            print(f"  Usadas (últimos 7 días): {alerta['usadas_7dias']}")
        if 'usadas_3dias' in alerta:
            print(f"  Usadas (últimos 3 días): {alerta['usadas_3dias']}")
        print(f"  Urgencia: {alerta['urgencia']}")

    print("\n💡 RECOMENDACIÓN: Cambiar/rotación de fotos para evitar bloqueos de TikTok")
    print("="*60 + "\n")

if __name__ == "__main__":
    mostrar_alertas()
