#!/usr/bin/env python3
"""Parser de archivos de investigación TikTok para extraer hashtags y referencias."""

import re
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def parsear_investigacion(archivo_md):
    """Extrae hashtags, referencias y ángulos de un archivo investigacion/*.md."""
    if not Path(archivo_md).exists():
        return {"hashtags": [], "referencias": [], "angulos": []}

    contenido = Path(archivo_md).read_text()

    # Extrae todos los hashtags
    hashtags = set(re.findall(r"#\w+", contenido))

    # Extrae referencias (líneas con "Post", "Carrusel", "Video", etc.)
    referencias = re.findall(
        r"(?:Post|Carrusel|Video|Hallazgo|Referencia)(?:\s+#)?:?\s*([^\n]+)",
        contenido,
        re.IGNORECASE
    )

    # Extrae ángulos (palabras clave de fórmulas virales)
    formulas = [
        "cosas que", "señales de", "mi ritual", "lo que", "consejos",
        "green flags", "red flags", "POV", "si eres", "rutina de"
    ]
    angulos = []
    for linea in contenido.split("\n"):
        for formula in formulas:
            if formula.lower() in linea.lower():
                angulos.append(linea.strip())
                break

    return {
        "hashtags": sorted(list(hashtags)),
        "referencias": referencias[:5],  # Top 5
        "angulos": angulos[:10],  # Top 10
        "fecha": Path(archivo_md).stem,
    }

def consolidar_investigaciones(dias=3):
    """Lee las últimas N investigaciones y consolida hashtags/ángulos."""
    investigacion_dir = PROJECT_ROOT / "investigacion"
    if not investigacion_dir.exists():
        return {"hashtags_top": [], "angulos_top": []}

    archivos = sorted(investigacion_dir.glob("*.md"))[-dias:]
    todos_hashtags = []
    todos_angulos = []

    for archivo in archivos:
        data = parsear_investigacion(str(archivo))
        todos_hashtags.extend(data["hashtags"])
        todos_angulos.extend(data["angulos"])

    # Cuenta frecuencias
    hashtag_freq = {}
    for h in todos_hashtags:
        hashtag_freq[h] = hashtag_freq.get(h, 0) + 1

    angulo_freq = {}
    for a in todos_angulos:
        angulo_freq[a] = angulo_freq.get(a, 0) + 1

    return {
        "hashtags_top": sorted(hashtag_freq.items(), key=lambda x: -x[1])[:8],
        "angulos_top": sorted(angulo_freq.items(), key=lambda x: -x[1])[:5],
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Si se pasa una ruta, parsea ese archivo
        resultado = parsear_investigacion(sys.argv[1])
    else:
        # Si no, consolida las últimas investigaciones
        resultado = consolidar_investigaciones(3)

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
