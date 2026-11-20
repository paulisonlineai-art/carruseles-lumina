"""Hoja de contacto de un carrusel: python3 herramientas/hoja.py carpeta_slides salida.jpg"""
import sys, glob
from PIL import Image
fs = sorted(glob.glob(sys.argv[1].rstrip('/') + '/*.jpg')); W = 360
cols = 3; rows = (len(fs) + cols - 1) // cols
s = Image.new('RGB', (cols * W, rows * W), 'white')
for i, f in enumerate(fs):
    im = Image.open(f); im.thumbnail((W, W)); s.paste(im, ((i % cols) * W, (i // cols) * W))
s.save(sys.argv[2], quality=88); print('hoja:', sys.argv[2])
