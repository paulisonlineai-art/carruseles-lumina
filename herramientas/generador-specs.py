#!/usr/bin/env python3
"""Genera 6 JSON specs desde plan-dia.json (usando fotos y textos del plan)."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def generar_specs(plan_archivo):
    """Lee plan-dia.json y genera 6 archivos JSON specs."""

    if not Path(plan_archivo).exists():
        print(f"Error: {plan_archivo} no existe", file=sys.stderr)
        return False

    plan = json.loads(Path(plan_archivo).read_text())
    salida_dir = Path(plan_archivo).parent

    for carrusel in plan:
        carrusel_id = carrusel.get("id")
        if not carrusel_id:
            continue

        # Extrae los slides del carrusel (vienen en plan-dia.json)
        slides = carrusel.get("slides", [])

        # Si no hay slides, crea desde cero
        if not slides:
            # Por defecto: portada + 4 slides de apoyo
            portada_foto = carrusel.get("portada_foto", "")
            slides = [
                {
                    "foto": portada_foto,
                    "portada": True,
                    "texto": carrusel.get("portada_texto", carrusel.get("tema", "")),
                    "sub": carrusel.get("portada_sub", ""),
                }
            ]

            # Agrega slides de apoyo del carrusel
            apoyo_slides = carrusel.get("apoyo_slides", [])
            for i, slide in enumerate(apoyo_slides):
                spec_slide = {
                    "foto": slide.get("foto", ""),
                    "portada": False,
                    "texto": slide.get("texto", ""),
                    "sub": slide.get("sub", ""),
                }
                # Si es photo dump, marca el estilo
                if carrusel.get("tipo") == "dump":
                    spec_slide["estilo"] = "dump"
                slides.append(spec_slide)

        # Escribe el spec.json para este carrusel
        spec_path = salida_dir / f"{carrusel_id}.json"
        spec_path.write_text(json.dumps(slides, indent=2, ensure_ascii=False))
        print(f"✓ {spec_path.name}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 generador-specs.py salida/AAAA-MM-DD/plan-dia.json")
        sys.exit(1)

    if generar_specs(sys.argv[1]):
        print("\nTodos los specs generados.")
        sys.exit(0)
    else:
        print("Error al generar specs.")
        sys.exit(1)
