#!/usr/bin/env python3
"""Valida hojas de contacto de carruseles: detecta cara cortada, texto ilegible, etc."""

import sys
from pathlib import Path
from PIL import Image, ImageStat

def validar_carrusel(carpeta_slides, hoja_contacto):
    """Valida un carrusel: retorna lista de problemas o lista vacía si OK."""

    carpeta = Path(carpeta_slides)
    hoja_path = Path(hoja_contacto)

    if not carpeta.exists():
        return ["ERROR: Carpeta de slides no existe"]

    if not hoja_path.exists():
        return ["ERROR: Hoja de contacto no existe"]

    # Cuenta slides
    slides = sorted(carpeta.glob("*.jpg"))
    if len(slides) < 5 or len(slides) > 7:
        return [f"ERROR: Número de slides {len(slides)} fuera de rango (5-7)"]

    problemas = []

    # Verifica cada slide
    for i, slide_path in enumerate(slides):
        try:
            img = Image.open(slide_path)

            # Verifica tamaño
            if img.size != (1080, 1080):
                problemas.append(f"⚠ Slide {i+1}: tamaño incorrecto {img.size}")

            # Detecta contraste bajo (texto ilegible)
            # Convierte a escala de grises y calcula desviación estándar
            img_gs = img.convert('L')
            stat = ImageStat.Stat(img_gs)
            contraste = stat.stddev[0] if stat.stddev else 0

            if contraste < 15:  # Umbral bajo para detectar falta de contraste
                problemas.append(f"⚠ Slide {i+1}: contraste muy bajo (posible ilegibilidad)")

            # Detecta píxeles oscuros en región de cara (arriba de la portada)
            if i == 0:  # Solo en portada
                # Recorta región superior donde debería estar la cara
                crop = img.crop((300, 100, 780, 500))
                crop_gs = crop.convert('L')
                stat_crop = ImageStat.Stat(crop_gs)
                brillo_cara = stat_crop.mean[0]

                if brillo_cara < 50:  # Muy oscuro = cara cortada o tapada
                    problemas.append(f"⚠ Slide 1 (portada): región de cara muy oscura (posible cara cortada)")

        except Exception as e:
            problemas.append(f"ERROR: No se pudo procesar slide {i+1}: {str(e)}")

    # Verifica que la hoja de contacto existe y es válida
    try:
        hoja_img = Image.open(hoja_path)
        if hoja_img.size[0] < 300 or hoja_img.size[1] < 300:
            problemas.append("⚠ Hoja de contacto muy pequeña")
    except:
        problemas.append("ERROR: No se pudo abrir la hoja de contacto")

    return problemas if problemas else ["OK"]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 validador-fotos.py /ruta/carpeta_slides /ruta/hoja.jpg")
        sys.exit(1)

    carpeta = sys.argv[1]
    hoja = sys.argv[2]

    resultado = validar_carrusel(carpeta, hoja)

    for linea in resultado:
        print(linea)

    # Retorna 0 si está OK, 1 si hay problemas
    sys.exit(0 if resultado == ["OK"] else 1)
