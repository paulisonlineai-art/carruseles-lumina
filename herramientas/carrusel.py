"""Renderer oficial de carruseles Lumina / @valu.manifiesta (modelo aprobado 19/11/2026).
Portada = foto de Valu CENTRADA con la cara libre (usa valu/caras.json; texto debajo del mentón, y≈830–910). Resto = fotos de apoyo tipo Pinterest (texto centrado, y=540).
Uso: python3 carrusel.py spec.json carpeta_salida
Estilos: normal (por defecto) o "estilo": "dump" en slides de apoyo (photo dump: texto chico abajo, foto casi sin oscurecer).
spec.json = [{"foto": "/ruta/valu-03.jpg", "portada": true, "texto": "5 cosas que...", "sub": "(guárdalo)"},
             {"foto": "/ruta/vaso-de-agua.jpg", "texto": "1. sirvo un vaso de agua", "sub": "apenas me levanto"}, ...]
"""
import sys, os, json, random
from PIL import Image, ImageDraw, ImageFont, ImageStat
S = 1080

def font(names, size):
    for n in names:
        for d in (os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fuentes') + '/', '/usr/share/fonts/opentype/inter/', '/usr/share/fonts/truetype/inter/', '/usr/share/fonts/truetype/dejavu/'):
            if os.path.exists(d + n): return ImageFont.truetype(d + n, size)
    raise SystemExit('Falta la fuente Inter (pip/apt fonts-inter) o DejaVu')
F_MAIN = font(['Inter-ExtraBold.otf', 'Inter-ExtraBold.ttf', 'DejaVuSans-Bold.ttf'], 44)
F_SUB = font(['Inter-Bold.otf', 'Inter-Bold.ttf', 'DejaVuSans-Bold.ttf'], 28)
F_DUMP = font(['Inter-Bold.otf', 'Inter-Bold.ttf', 'DejaVuSans-Bold.ttf'], 36)

def cover(img, fy=0.5):
    img = img.convert('RGB'); s = S / min(img.size)
    img = img.resize((round(img.width*s), round(img.height*s)), Image.LANCZOS)
    x = (img.width-S)//2; y = int((img.height-S)*fy)
    return img.crop((x, y, x+S, y+S))

def cara(img, ruta):
    """(cx, cy, h) de la cara en píxeles. Primero caras.json junto a la foto (banco-carr-valu lo trae), luego opencv 4 si existe."""
    W, H = img.size
    j = os.path.join(os.path.dirname(ruta), 'caras.json')
    if os.path.exists(j):
        d = json.load(open(j)).get(os.path.basename(ruta))
        if d: return d[0]*W, d[1]*H, d[2]*H
    try:
        import cv2, numpy as np
        det = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        g = cv2.cvtColor(np.array(img.convert('RGB')), cv2.COLOR_RGB2GRAY)
        f = det.detectMultiScale(g, 1.1, 6, minSize=(W//10, W//10))
        if len(f):
            x, y, w, h = max(f, key=lambda r: r[2]*r[3]); return x + w/2, y + h/2, h
    except Exception:
        pass
    return None

def cover_valu(img, ruta=''):
    """Portada: Valu centrada, cara arriba del centro y libre; el texto va debajo del mentón."""
    img = img.convert('RGB'); c = cara(img, ruta)
    if not c: return cover(img, 0.12), 860
    cx, cy, fh = c
    s = S / min(img.size)
    im = img.resize((round(img.width*s), round(img.height*s)), Image.LANCZOS)
    cx, cy, fh = cx*s, cy*s, fh*s
    ox = round(min(0, max(S - im.width, S/2 - cx)))
    oy = round(min(0, max(S - im.height, 400 - cy)))
    out = im.crop((-ox, -oy, -ox + S, -oy + S))
    menton = oy + cy + fh*0.6
    return out, int(max(830, min(910, menton + 170)))

def treat(img, minimo=0.18):
    lum = ImageStat.Stat(img.convert('L')).mean[0]
    a = int(255*min(0.35, max(minimo, 0.18 + (lum-90)/400)))
    img = Image.alpha_composite(img.convert('RGBA'), Image.new('RGBA', (S, S), (10, 6, 20, a))).convert('RGB')
    random.seed(1); n = Image.effect_noise((S, S), 18).convert('RGB')
    return Image.blend(img, n, 0.03)

def wrap(t, f, maxw=900):
    out, cur = [], ''
    for w in t.split():
        x = (cur+' '+w).strip()
        if f.getlength(x) <= maxw: cur = x
        else: out.append(cur); cur = w
    out.append(cur); return out

def bwrap(t, f, maxw=900):  # cortes balanceados: sin palabras huérfanas
    n = len(wrap(t, f, maxw)); w = maxw
    while w > 300 and len(wrap(t, f, w-10)) == n: w -= 10
    return wrap(t, f, w)

def draw(img, main, sub, cy, fm=None):
    d = ImageDraw.Draw(img); fm = fm or F_MAIN
    L = bwrap(main, fm, 820 if fm is F_DUMP else 900); lh = 68 if fm is F_MAIN else 56
    sl = bwrap(sub, F_SUB) if sub else []; slh = 48
    tot = len(L)*lh + (len(sl)*slh + 18 if sl else 0)
    y = cy - tot//2
    for ln in L:
        d.text((S/2+3, y+lh/2+4), ln, font=fm, fill=(0, 0, 0), anchor='mm')
        d.text((S/2, y+lh/2), ln, font=fm, fill='white', anchor='mm', stroke_width=5 if fm is F_MAIN else 4, stroke_fill='black'); y += lh
    y += 18
    for ln in sl:
        d.text((S/2, y+slh/2), ln, font=F_SUB, fill='white', anchor='mm', stroke_width=4, stroke_fill='black'); y += slh

spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for i, s in enumerate(spec, 1):
    im = Image.open(s['foto'])
    if s.get('portada'):
        img, cy = cover_valu(im, s['foto']); img = treat(img)
    elif s.get('estilo') == 'dump':  # "photo dump": foto casi sin capa, texto más chico centrado, como de usuaria
        img = cover(im); random.seed(i); n = Image.effect_noise((S, S), 18).convert('RGB')
        img = Image.alpha_composite(img.convert('RGBA'), Image.new('RGBA', (S, S), (0, 0, 0, 40))).convert('RGB')
        img = Image.blend(img, n, 0.03); cy = 540  # CENTRADO: mismo que slides normales
    else:
        img = treat(cover(im)); cy = 540
    draw(img, s['texto'], s.get('sub'), cy, F_DUMP if s.get('estilo') == 'dump' and not s.get('portada') else None)
    img.save(f'{out}/{i:02d}.jpg', quality=95)
print('ok', len(spec), 'slides en', out)
