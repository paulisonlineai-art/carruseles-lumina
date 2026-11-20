#!/usr/bin/env python3
"""Decisiones por defecto del plan diario automático: Plan B, foto alternativa, etc."""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).parent.parent

def parsear_registro():
    """Lee registro.md y retorna dict con historial."""
    reg_path = PROJECT_ROOT / "registro.md"
    if not reg_path.exists():
        return {"fotos_portada_valu": {}, "fotos_portada_sofia": {}, "fotos_apoyo": {}}

    contenido = reg_path.read_text()
    # Extrae fechas y fotos usadas
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    hace_3_dias = hoy - timedelta(days=3)

    fotos_portada_valu = {}
    fotos_portada_sofia = {}
    fotos_apoyo = {}

    # Busca secciones de fecha (formato ## AAAA-MM-DD)
    fecha_pattern = r"## (\d{4}-\d{2}-\d{2})"
    fechas_encontradas = re.findall(fecha_pattern, contenido)

    for fecha_str in fechas_encontradas[:7]:  # Últimos 7 días para Valu, 3 para Sofi
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            if fecha >= hace_7_dias:
                # Busca fotos en esta sección
                seccion_start = contenido.find(f"## {fecha_str}")
                seccion_end = contenido.find("## ", seccion_start + 1)
                if seccion_end == -1:
                    seccion_end = len(contenido)
                seccion = contenido[seccion_start:seccion_end]

                # Extrae fotos de portada Valu
                valu_match = re.search(r"- Portada: (valu-\d+\.jpg)", seccion)
                if valu_match:
                    foto = valu_match.group(1)
                    fotos_portada_valu[foto] = fotos_portada_valu.get(foto, 0) + 1

                # Extrae fotos de portada Sofi
                sofia_match = re.search(r"- Portada: (sofia-\S+\.jpg)", seccion)
                if sofia_match:
                    foto = sofia_match.group(1)
                    fotos_portada_sofia[foto] = fotos_portada_sofia.get(foto, 0) + 1

                # Extrae fotos de apoyo
                apoyo_matches = re.findall(r"- Apoyo: (.+)", seccion)
                for linea in apoyo_matches:
                    for foto in linea.split(", "):
                        foto = foto.strip()
                        if foto:
                            fotos_apoyo[foto] = fotos_apoyo.get(foto, 0) + 1
        except:
            pass

    return {
        "fotos_portada_valu": fotos_portada_valu,
        "fotos_portada_sofia": fotos_portada_sofia,
        "fotos_apoyo": fotos_apoyo,
        "fecha_ultima": fechas_encontradas[0] if fechas_encontradas else None,
    }

def aplicar_plan_b():
    """Retorna dict con ángulos de reserva + referencias antiguas si TikTok falló."""
    # Ángulos de reserva de guia/aprendizajes-referencia.md
    angulos_reserva = [
        "green flags de que estás sanando",
        "cosas que hago cuando me siento ansiosa",
        "lo que nadie te dice cuando empiezas a manifestar",
        "hábitos chiquitos que me devolvieron la calma",
        "mi ritual de domingo de 10 minutos",
        "señales de que el universo te está pidiendo pausa",
        "cosas que ya no le pido al universo",
        "POV: dejaste de forzar las cosas",
        "mi rutina de noche cuando no puedo dormir",
        "lo que cambié en mi cuarto para sentirme en paz",
        "cosas que solo entiende alguien que ve el 11:11",
        "consejos para tu primer diario de gratitud",
        "red flags de que estás manifestando desde la ansiedad",
        "cosas que dejé de decir en voz alta",
        "señales de que estás en tu era de amor propio",
    ]

    # Lee investigaciones anteriores para hashtags
    investigacion_dir = PROJECT_ROOT / "investigacion"
    hashtags_globales = set()

    if investigacion_dir.exists():
        for archivo_md in sorted(investigacion_dir.glob("*.md"))[-3:]:  # Últimos 3 días
            contenido = archivo_md.read_text()
            matches = re.findall(r"#\w+", contenido)
            hashtags_globales.update(matches)

    # Hashtags por defecto si no hay investigaciones anteriores
    if not hashtags_globales:
        hashtags_globales = {
            "#manifestación", "#leydeatracción", "#528hz", "#ritualdiario",
            "#amorpropio", "#gratitud", "#diariodemanifestación", "#1111",
            "#señalesdeluniverso", "#intuición", "#universo", "#abundancia"
        }

    return {
        "plan_b_activo": True,
        "angulos_reserva": angulos_reserva,
        "hashtags_globales": sorted(list(hashtags_globales)),
    }

def foto_alternativa(banco, cuenta, fotos_hoy_usadas=None):
    """Retorna foto menos usada del banco, evitando repetir en el mismo día.

    Args:
        banco: 'valu', 'sofia', 'apoyo', 'apoyo-sofia'
        cuenta: 'valu' o 'sofia' (para portadas)
        fotos_hoy_usadas: lista de fotos ya usadas hoy (para evitar repetición)
    """
    if fotos_hoy_usadas is None:
        fotos_hoy_usadas = []

    registro = parsear_registro()

    fotos_dir = PROJECT_ROOT / "fotos" / banco
    if not fotos_dir.exists():
        return None

    fotos_disponibles = sorted([f.name for f in fotos_dir.glob("*.jpg") if f.name != "caras.json"])
    if not fotos_disponibles:
        return None

    # Filtra fotos ya usadas hoy (evita repetición el mismo día)
    fotos_disponibles = [f for f in fotos_disponibles if f not in fotos_hoy_usadas]

    if not fotos_disponibles:
        # Si se agotan las nuevas, usa la menos usada globalmente
        fotos_disponibles = sorted([f.name for f in fotos_dir.glob("*.jpg") if f.name != "caras.json"])

    # Determina qué dict usar según el banco
    if banco == "valu":
        uso_dict = registro["fotos_portada_valu"]
    elif banco == "sofia":
        uso_dict = registro["fotos_portada_sofia"]
    else:
        uso_dict = registro["fotos_apoyo"]

    # Retorna la menos usada (prioriza sin uso = 0, luego 1, etc.)
    foto_menos_usada = min(fotos_disponibles, key=lambda f: uso_dict.get(f, 0))
    return foto_menos_usada

def cambiar_foto_en_spec(spec_path, foto_nueva, slide_index=0):
    """Reemplaza foto en spec.json en un slide específico."""
    if not Path(spec_path).exists():
        return False

    spec = json.loads(Path(spec_path).read_text())
    if slide_index < len(spec):
        spec[slide_index]["foto"] = str(foto_nueva)
        Path(spec_path).write_text(json.dumps(spec, indent=2, ensure_ascii=False))
        return True
    return False

def anguos_ya_usados():
    """Retorna lista de ángulos de reserva ya usados (en registro.md)."""
    reg_path = PROJECT_ROOT / "registro.md"
    if not reg_path.exists():
        return []

    contenido = reg_path.read_text()
    seccion_match = re.search(r"## Ángulos de reserva ya usados\n(.*?)(?=##|$)", contenido, re.DOTALL)
    if not seccion_match:
        return []

    seccion = seccion_match.group(1)
    # Extrae items de lista (- item)
    items = re.findall(r"- (.+)", seccion)
    return items

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "plan_b":
        result = aplicar_plan_b()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif len(sys.argv) > 2 and sys.argv[1] == "foto_alternativa":
        banco = sys.argv[2]
        cuenta = sys.argv[3] if len(sys.argv) > 3 else "valu"
        foto = foto_alternativa(banco, cuenta)
        if foto:
            print(foto)
    else:
        print("Uso: python3 decisiones.py plan_b | python3 decisiones.py foto_alternativa <banco> [<cuenta>]")
