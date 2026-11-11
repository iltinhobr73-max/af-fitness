"""Padroniza as fotos da AF Fitness. Miniaturas quadradas (320x320) + foto de destaque 3:2 + fundo do hero.
Saída na raiz do site, em WebP + JPG."""
import sys, glob
from PIL import Image, ImageFilter, ImageEnhance
SRC, OUT = sys.argv[1], sys.argv[2]
def src(n): return glob.glob(f"{SRC}/{n}.*")[0]
def crop(im, ratio, cx=0.5, cy=0.5):
    w, h = im.size
    nw, nh = (h * ratio, h) if w / h > ratio else (w, w / ratio)
    x, y = (w - nw) * cx, (h - nh) * cy
    return im.crop(tuple(round(v) for v in (x, y, x + nw, y + nh)))
SQ = {  # nome: (foto, centro x, centro y)
 "af-salao":      (18, 0.5, 0.5),
 "af-lutas":      (19, 0.5, 0.45),
 "af-fachada":    (20, 0.5, 0.5),
 "af-funcional":  (21, 0.6, 0.5),
 "af-equipe":     (22, 0.5, 0.3),
 "af-kimono":     (23, 0.5, 0.45),
 "af-suplementos":(24, 0.5, 0.5),
 "af-turma":      (25, 0.5, 0.5),
 "af-pesos":      (28, 0.5, 0.45),
 "af-aparelhos":  (29, 0.4, 0.5),
 "af-aerobico":   (30, 0.5, 0.5),
 "af-musculacao": (17, 0.55, 0.5),
}
for name, (n, cx, cy) in SQ.items():
    im = crop(Image.open(src(n)).convert("RGB"), 1, cx, cy).resize((320, 320), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=35, threshold=2))
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=84, method=6); im.save(f"{OUT}/{name}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
big = Image.open(src(17)).convert("RGB")
d = crop(big, 3 / 2).resize((900, 600), Image.LANCZOS)
d.save(f"{OUT}/af-academia.webp", "WEBP", quality=82, method=6); d.save(f"{OUT}/af-academia.jpg", "JPEG", quality=84, optimize=True, progressive=True)
bg = crop(big, 16 / 9, 0.5, 0.45).resize((1600, 900), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
ImageEnhance.Color(bg).enhance(0.75).save(f"{OUT}/af-fundo.webp", "WEBP", quality=62, method=6)
og = crop(big, 1200 / 630).resize((1200, 630), Image.LANCZOS); og.save(f"{OUT}/af-capa.jpg", "JPEG", quality=84, optimize=True)
print("ok", len(SQ) + 3)
