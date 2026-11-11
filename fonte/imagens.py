"""Padroniza as fotos da AF Fitness. Fotos quadradas (640x640) + foto de destaque 3:2 + fundo do hero.
Saída na raiz do site, em WebP + JPG."""
import sys, glob
import cv2
import numpy as np
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
def restaurar(im, lado):
    """Amplia uma foto pequena sem deixar quadriculado: remove os blocos da compressão,
    amplia em duas etapas com suavização que preserva as bordas, realça e aplica um grão fino."""
    a = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
    a = cv2.fastNlMeansDenoisingColored(a, None, 5, 6, 5, 15)                     # tira blocos e ruído de cor
    h, w = a.shape[:2]
    a = cv2.resize(a, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)
    a = cv2.bilateralFilter(a, 7, 28, 7)                                          # alisa áreas planas, mantém contornos
    a = cv2.resize(a, (lado, lado), interpolation=cv2.INTER_LANCZOS4)
    a = cv2.bilateralFilter(a, 5, 18, 5)
    blur = cv2.GaussianBlur(a, (0, 0), 2.2)
    a = cv2.addWeighted(a, 1.55, blur, -0.55, 0)                                  # realce de contorno
    rng = np.random.default_rng(7)
    grao = rng.normal(0, 5.5, (lado, lado, 1)).astype(np.float32)                 # grão de filme, igual nos 3 canais
    a = np.clip(a.astype(np.float32) + grao, 0, 255).astype(np.uint8)
    return Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB))


for name, (n, cx, cy) in SQ.items():
    orig = Image.open(src(n)).convert("RGB")
    im = crop(orig, 1, cx, cy)
    im = restaurar(im, 640) if orig.width < 400 else im.resize((640, 640), Image.LANCZOS)
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=80, method=6); im.save(f"{OUT}/{name}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
big = Image.open(src(17)).convert("RGB")
d = crop(big, 3 / 2).resize((900, 600), Image.LANCZOS)
d.save(f"{OUT}/af-academia.webp", "WEBP", quality=82, method=6); d.save(f"{OUT}/af-academia.jpg", "JPEG", quality=84, optimize=True, progressive=True)
bg = crop(big, 16 / 9, 0.5, 0.45).resize((1600, 900), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
ImageEnhance.Color(bg).enhance(0.75).save(f"{OUT}/af-fundo.webp", "WEBP", quality=62, method=6)
og = crop(big, 1200 / 630).resize((1200, 630), Image.LANCZOS); og.save(f"{OUT}/af-capa.jpg", "JPEG", quality=84, optimize=True)
print("ok", len(SQ) + 3)
