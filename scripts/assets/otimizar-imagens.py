"""Gera variantes responsivas (AVIF/WebP/JPG) das fotos oficiais e da cena.

Uso: python scripts/assets/otimizar-imagens.py  (depois de renderizar a cena)
Originais permanecem em public/images/ e blender/renders/.
"""
import os
from PIL import Image

OUT = 'public/images/opt'
os.makedirs(OUT, exist_ok=True)


def variants(src, name, widths, crop=None, quality=(58, 80, 82), out=OUT):
    im = Image.open(src).convert('RGB')
    if crop:
        im = im.crop(crop)
    for w in widths:
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(f'{out}/{name}-{w}.avif', quality=quality[0])
        r.save(f'{out}/{name}-{w}.webp', quality=quality[1], method=6)
        r.save(f'{out}/{name}-{w}.jpg', quality=quality[2], optimize=True, progressive=True)
        print(name, w, h)


# Fachada (1080x1920): recorte vertical com a placa e a vitrine de serviços
variants('public/images/fachada-oficial.jpg', 'fachada', [480, 800], crop=(60, 0, 1080, 1360))
variants('public/images/projeto-residencial.jpg', 'projeto-residencial', [360, 540])
variants('public/images/servico-condensadora.jpg', 'servico-condensadora', [360, 540])

# Pôsteres da cena (mesmo enquadramento do vídeo): primeiro e último quadro
os.makedirs('public/scene', exist_ok=True)
start = 'blender/renders/still-001.png'
poster = 'blender/renders/still-150.png'
if os.path.exists(start):
    variants(start, 'cena-inicio', [800, 1280, 1600], out='public/scene')
if os.path.exists(poster):
    variants(poster, 'cena-instalada', [800, 1280, 1600], out='public/scene')
    # Compartilhamento social 1200x630 (recorte central do mesmo quadro)
    im = Image.open(poster).convert('RGB')
    w = im.width
    h = round(w * 630 / 1200)
    top = round(im.height * 0.12)
    im.crop((0, top, w, top + h)).resize((1200, 630), Image.LANCZOS).save('public/og-richardson.jpg', quality=84, optimize=True, progressive=True)

# Favicon: marca R + floco do JPG oficial sobre o mesmo azul
logo = Image.open('public/images/logo-oficial.jpg').convert('RGB')
mark = logo.crop((36, 16, 106, 68))  # 70x52, sem o topo do texto
side = 72
sq = Image.new('RGB', (side, side), (15, 48, 102))
sq.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2))
sq.resize((32, 32), Image.LANCZOS).save('public/favicon-32.png', optimize=True)
sq.resize((180, 180), Image.LANCZOS).save('public/apple-touch-icon.png', optimize=True)
