# Harmonise les photos d'origine : même cadrage d'assiette, même teinte de fond, veines atténuées.
# Usage : python3 outils/harmoniser-photos.py <dossier des originaux 1200 px> <sortie> outils/assiettes.txt ECE3D6
import sys, os, numpy as np
from PIL import Image, ImageFilter, ImageDraw
src, out = sys.argv[1], sys.argv[2]
N = 1200
CIRCLES = {}  # centre/rayon de l'assiette mesurés précédemment (en px sur 1200)
for line in open(sys.argv[3]):
    k, cx, cy, r = line.split(); CIRCLES[k] = (float(cx), float(cy), float(r))
R_REF, CX_REF, CY_REF = 428, 601, 571
PLAIN = ['hoummous', 'labne', 'caviar-aubergine', 'falafels', 'kebbe']

def load(slug):
    im = Image.open(os.path.join(src, slug + '-1200.webp')).convert('RGB')
    cx, cy, r = CIRCLES[slug]
    s = R_REF / r
    if abs(s - 1) > .01 or abs(cx - CX_REF) > 3:  # remet l'assiette à la taille et à la place de référence
        pad = int(N / s - N) // 2 + 40   # prolonge le fond en miroir pour ne pas créer de bord
        big = Image.fromarray(np.pad(np.asarray(im), ((pad, pad), (pad, pad), (0, 0)), mode='reflect'))
        big = big.resize((round(big.width * s), round(big.height * s)), Image.LANCZOS)
        ox, oy = round((cx + pad) * s - CX_REF), round((cy + pad) * s - CY_REF)
        im = big.crop((ox, oy, ox + N, oy + N))
    return im

def bg_mask(feather=18, grow=1.04):
    m = Image.new('L', (N, N), 255)
    r = R_REF * grow
    ImageDraw.Draw(m).ellipse((CX_REF - r, CY_REF - r, CX_REF + r, CY_REF + r), fill=0)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(feather)), dtype=float) / 255

M = bg_mask()[..., None]
# teinte cible : moyenne des fonds unis, mesurée loin de l'assiette
corner = np.zeros((N, N), bool); corner[:150, :] = True; corner[-120:, :] = True
target = np.mean([np.asarray(load(k), dtype=float)[corner].mean(0) for k in PLAIN], 0)
if len(sys.argv) > 4:  # teinte imposée, ex. ECE3D6 : la même que le fond des sections du site
    h = sys.argv[4]; target = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)
# fondu vers la teinte pure sur les bords, pour que la photo se fonde dans la section
yy, xx = np.mgrid[0:N, 0:N]
edge = np.minimum.reduce([xx, yy, N - 1 - xx, N - 1 - yy]).astype(float)
t = np.clip(edge / 260, 0, 1); EDGE = t * t * (3 - 2 * t)  # fondu progressif
print('cible', target.round(1))

for f in sorted(os.listdir(src)):
    slug = f[:-10]
    im = load(slug); a = np.asarray(im, dtype=float)
    hard = bg_mask(feather=1, grow=1.03)
    w = Image.fromarray((hard * 255).astype('uint8'))
    num = np.asarray(Image.fromarray(np.clip(a * hard[..., None], 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(30)), dtype=float)
    den = np.asarray(w.filter(ImageFilter.GaussianBlur(30)), dtype=float)[..., None] / 255
    low = num / np.maximum(den, 1e-3)
    lum = lambda x: x @ np.array([.299, .587, .114])
    detail = lum(a) - lum(low)                         # veines et grain
    ref = np.percentile(lum(low)[hard > .5], 75)          # luminosité typique du fond, hors assiette
    shade = np.minimum(lum(low) / max(ref, 1), 1.0)         # ne garde que les ombres, jamais d'éclaircissement
    new_bg = target[None, None, :] * shade[..., None] + (detail * .25)[..., None]
    new_bg = target[None, None, :] * (1 - EDGE[..., None]) + new_bg * EDGE[..., None]
    res = a * (1 - M) + new_bg * M
    Image.fromarray(np.clip(res, 0, 255).astype('uint8')).save(os.path.join(out, slug + '.png'))
    print(slug)
