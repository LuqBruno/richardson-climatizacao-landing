"""Gera a logo com fundo transparente a partir do JPG oficial (150 px).

Desmistura de cor: cada pixel é tratado como mistura entre o azul do fundo
(#0f3066, amostrado nos cantos) e a cor original da arte. O alfa é a menor
opacidade capaz de explicar a cor observada; a cor é recuperada sem inventar
detalhes. O slogan (6 px de altura, ilegível no cabeçalho) fica fora do recorte.
Uso: python scripts/assets/logo-transparente.py
"""
from PIL import Image

SRC = 'public/images/logo-oficial.jpg'
BG = (15, 48, 102)
CROP = (0, 19, 150, 105)  # marca R + floco, "Richardson" e "CLIMATIZAÇÃO"
NOISE = 14  # ruído de compressão JPG ao redor do fundo

im = Image.open(SRC).convert('RGB').crop(CROP)
out = Image.new('RGBA', im.size)
src, dst = im.load(), out.load()
for y in range(im.height):
    for x in range(im.width):
        p = src[x, y]
        a = 0.0
        for c in range(3):
            diff = p[c] - BG[c]
            span = (255 - BG[c]) if diff > 0 else BG[c]
            a = max(a, (abs(diff) - NOISE) / (span - NOISE) if abs(diff) > NOISE else 0)
        a = min(1.0, a)
        if a <= 0.02:
            dst[x, y] = (0, 0, 0, 0)
            continue
        col = tuple(max(0, min(255, round(BG[c] + (p[c] - BG[c]) / a))) for c in range(3))
        dst[x, y] = (*col, round(a * 255))
out.save('public/images/logo-richardson.png', optimize=True)
out.resize((out.width * 2, out.height * 2), Image.LANCZOS).save('public/images/logo-richardson@2x.png', optimize=True)
print(out.size)
