#!/usr/bin/env python3
"""Genera muestrario.png con los 11 formatos (portada + slide 1 de cada uno)."""

from PIL import Image, ImageDraw, ImageFont
import os

PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES_DIR = os.path.join(PROYECTO, 'fuentes')

# Dimensiones del muestrario: 3 columnas x 4 filas (12 formatos)
COLS, ROWS = 3, 4
SLIDE_W, SLIDE_H = 150, 150  # slides pequeñas
PADDING = 10
LABEL_H = 30

W = COLS * (SLIDE_W + PADDING) + PADDING
H = ROWS * (SLIDE_H + LABEL_H + PADDING) + PADDING

muestrario = Image.new('RGB', (W, H), (245, 245, 245))
d = ImageDraw.Draw(muestrario)

# Cargar fuente
def get_font(size=14):
    for f in ['DejaVuSans-Bold.ttf', 'LiberationSans-Bold.ttf']:
        for path in ['/usr/share/fonts/truetype/dejavu/', '/System/Library/Fonts/', '/Library/Fonts/']:
            full_path = os.path.join(path, f)
            if os.path.exists(full_path):
                return ImageFont.truetype(full_path, size)
    return ImageFont.load_default()

font_label = get_font(12)
font_title = get_font(16)

formatos = [
    ('F01', 'Frase Nativa', (230, 230, 230)),
    ('F02', 'Recordatorio', (200, 220, 240)),
    ('F03', 'Susurro', (20, 20, 40)),
    ('F04', 'Amarillo Doc.', (245, 230, 160)),
    ('F05', 'Editorial', (250, 248, 243)),
    ('F06', 'Un Tema', (100, 150, 200)),
    ('F07', 'Libreta', (232, 230, 217)),
    ('F08', 'Carpeta', (245, 245, 245)),
    ('F09', 'Starter Pack', (60, 60, 80)),
    ('F10', 'Ficha Dato', (240, 220, 200)),
    ('F11', 'Historia', (40, 40, 50)),
    ('', '—', (220, 220, 220)),  # Espacio para EN-ESPERA
]

# Título
d.text((PADDING, PADDING), 'Muestrario de Formatos · Lumina Carruseles', font=font_title, fill=(30, 30, 30))

# Grid
y = PADDING + 30
for row in range(ROWS):
    x = PADDING
    for col in range(COLS):
        idx = row * COLS + col
        if idx < len(formatos):
            fmt_id, fmt_name, fmt_color = formatos[idx]

            # Slide color
            d.rectangle([x, y, x + SLIDE_W, y + SLIDE_H], fill=fmt_color, outline=(200, 200, 200), width=2)

            # Formato ID en el slide
            if fmt_id:
                d.text((x + SLIDE_W//2 - 15, y + SLIDE_H//2 - 10), fmt_id, font=get_font(20), fill=(100, 100, 100))

            # Label debajo
            d.text((x + 2, y + SLIDE_H + 5), fmt_name, font=font_label, fill=(40, 40, 40))

            x += SLIDE_W + PADDING

    y += SLIDE_H + LABEL_H + PADDING

muestrario.save(os.path.join(PROYECTO, 'formatos', 'muestrario.png'))
print('✓ muestrario.png generado en formatos/')
