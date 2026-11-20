#!/usr/bin/env python3
"""Genera publicar_hoy.md con títulos, descripciones y hashtags listos para TikTok."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def generar_publicar(carpeta_salida, plan_archivo):
    """Lee plan-dia.json y genera publicar_hoy.md."""

    carpeta = Path(carpeta_salida)
    plan_path = Path(plan_archivo)

    if not plan_path.exists():
        print(f"Error: {plan_archivo} no existe", file=sys.stderr)
        return False

    plan = json.loads(plan_path.read_text())

    # Horarios sugeridos por cuenta
    horarios = {
        "VALU-1": "7–9 a.m.",
        "VALU-2": "12–2 p.m.",
        "VALU-3": "7–9 p.m.",
        "SOFI-1": "7–9 a.m.",
        "SOFI-2": "12–2 p.m.",
        "SOFI-3": "7–9 p.m.",
    }

    lineas = ["# Publicar Hoy\n"]

    # Agrupa por cuenta
    for cuenta in ["VALU", "SOFI"]:
        cuenta_amiga = "@valu.manifiesta" if cuenta == "VALU" else "@manifiesta.con.sofia"
        lineas.append(f"\n## {cuenta_amiga}\n")

        carruseles_cuenta = [c for c in plan if cuenta in c.get("id", "")]

        for i, carrusel in enumerate(carruseles_cuenta, 1):
            carrusel_id = carrusel.get("id", f"{cuenta}-{i}")
            horario = horarios.get(carrusel_id, "7–9 a.m.")
            tipo = carrusel.get("tipo", "").title()
            tema = carrusel.get("tema", "")

            lineas.append(f"### Carrusel {i} ({tipo}) — Horario: {horario}")
            lineas.append(f"**Tema:** {tema}\n")

            # Título
            titulo = carrusel.get("titulo", "")
            if titulo:
                lineas.append("**Título (copiar y pegar):**")
                lineas.append(f"```")
                lineas.append(titulo)
                lineas.append("```\n")

            # Descripción
            descripcion = carrusel.get("descripcion", "")
            if descripcion:
                lineas.append("**Descripción (copiar y pegar):**")
                lineas.append("```")
                lineas.append(descripcion)
                lineas.append("```\n")

            # Hashtags
            hashtags = carrusel.get("hashtags", [])
            if hashtags:
                lineas.append("**Hashtags:**")
                lineas.append("```")
                lineas.append(" ".join(hashtags))
                lineas.append("```\n")

            # Ángulo y referencias
            angulo = carrusel.get("referencia", "")
            if angulo:
                lineas.append(f"**Ángulo:** {angulo}\n")

            lineas.append("---\n")

    lineas.append("\n⚠ **Recordatorio:** Marcar \"Contenido generado por IA\" al publicar.\n")

    # Escribe publicar_hoy.md
    output_path = carpeta / "publicar_hoy.md"
    output_path.write_text("\n".join(lineas), encoding="utf-8")
    print(f"✓ {output_path.name}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 generador-publicar.py salida/AAAA-MM-DD salida/AAAA-MM-DD/plan-dia.json")
        sys.exit(1)

    if generar_publicar(sys.argv[1], sys.argv[2]):
        print("publicar_hoy.md generado.")
        sys.exit(0)
    else:
        print("Error al generar publicar_hoy.md.")
        sys.exit(1)
