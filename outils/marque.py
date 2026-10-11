# Génère les fichiers du logo Atelier Najjar (SVG vectorisés + PNG) dans marque/.
# Usage : python3 outils/marque.py
import os, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ICI, '..', 'marque')
CASLON = os.path.join(ICI, 'polices', 'LibreCaslonDisplay-Regular.ttf')
AMIRI = os.path.join(ICI, 'polices', 'Amiri-Bold.ttf')

BORDEAUX, IVOIRE, BRUN, OR = '#5A1424', '#FBF8F3', '#2A1E1A', '#D9C29C'

class Police:
    def __init__(self, chemin):
        self.tt = TTFont(chemin); self.gs = self.tt.getGlyphSet()
        self.upm = self.tt['head'].unitsPerEm
        data = open(chemin, 'rb').read()
        self.hbfont = hb.Font(hb.Face(data))

    def texte(self, s, taille, x=0, y=0, espacement=0):
        """Renvoie (path_d, largeur, (xmin, ymin, xmax, ymax)) pour s posé à la ligne de base y."""
        buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {})
        k = taille / self.upm; names = self.tt.getGlyphOrder()
        pen = SVGPathPen(self.gs); bp = BoundsPen(self.gs)
        cx = 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            g = names[info.codepoint]
            t = (k, 0, 0, -k, x + (cx + pos.x_offset) * k, y - pos.y_offset * k)
            self.gs[g].draw(TransformPen(pen, t)); self.gs[g].draw(TransformPen(bp, t))
            cx += pos.x_advance + espacement / k
        return pen.getCommands(), cx * k - espacement, bp.bounds

caslon, amiri = Police(CASLON), Police(AMIRI)
NOM, ESP, T_LAT = 'Atelier Najjar', 0, 200   # remplacé par la version capitales plus bas

def svg(w, h, corps, fond=None):
    f = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{fond}"/>' if fond else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{f}{corps}</svg>\n'

def centre(police, s, taille, cx, base, esp=0):
    _, w, _ = police.texte(s, taille, 0, base, esp)
    return police.texte(s, taille, cx - w / 2, base, esp)

def vertical(c_ar, c_lat, c_tag=None, fond=None):
    M = 80
    _, wl, _ = caslon.texte(NOM, T_LAT, 0, 0, ESP)
    W = max(wl, 900) + 2 * M
    d1, _, b1 = centre(amiri, 'نجّار', 170, W / 2, 0)
    d2, _, b2 = centre(caslon, NOM, T_LAT, W / 2, 0, ESP)
    h1 = b1[3] - b1[1]; h2 = b2[3] - b2[1]
    y1 = M - b1[1]; y2 = y1 + b1[3] + 40 - b2[1]
    d1, _, _ = centre(amiri, 'نجّار', 170, W / 2, y1)
    d2, _, b2b = centre(caslon, NOM, T_LAT, W / 2, y2, ESP)
    corps = f'<path d="{d1}" fill="{c_ar}"/><path d="{d2}" fill="{c_lat}"/>'
    H = b2b[3] + M
    if c_tag:
        d3, _, b3 = centre(caslon, 'CUISINE LIBANAISE  ·  PARIS', 44, W / 2, b2b[3] + 90, esp=14)
        corps += f'<path d="{d3}" fill="{c_tag}"/>'; H = b3[3] + M
    return svg(W, H, corps, fond)

def horizontal(c_lat, c_ar, fond=None):
    M, T = 60, 200
    d2, w2, b2 = caslon.texte(NOM, T * T_LAT / 200, M, 0, ESP)
    base = M - b2[1]
    d2, w2, b2 = caslon.texte(NOM, T * T_LAT / 200, M, base, ESP)
    _, w1, _ = amiri.texte('نجّار', T * .82, 0, 0)
    x1 = M + w2 + T * (.28 if ESP == 0 else .42)
    d1, w1, b1 = amiri.texte('نجّار', T * .82, x1, base)
    top = min(b1[1], b2[1]); bot = max(b1[3], b2[3])
    corps = f'<g transform="translate(0 {M - top:.1f})"><path d="{d2}" fill="{c_lat}"/><path d="{d1}" fill="{c_ar}"/></g>'
    return svg(x1 + w1 + M, bot - top + 2 * M, corps, fond)

def monogramme(mode, fond=BORDEAUX, encre=IVOIRE, S=512):
    corps = f'<circle cx="{S/2}" cy="{S/2}" r="{S/2}" fill="{fond}"/>'
    if mode == 'N':
        d, _, b = centre(caslon, 'N', S * .62, S / 2, 0)
        h = b[3] - b[1]; d, _, _ = centre(caslon, 'N', S * .62, S / 2, S / 2 + h / 2)
        corps += f'<path d="{d}" fill="{encre}"/>'
    else:  # N + ن
        dN, _, bN = caslon.texte('N', S * .44, 0, 0); hN = bN[3] - bN[1]
        dN, wN, _ = caslon.texte('N', S * .44, S * .16, S / 2 + hN / 2)
        da, wa, ba = amiri.texte('ن', S * .46, 0, 0)
        ha = ba[3] - ba[1]
        da, _, _ = amiri.texte('ن', S * .46, S * .58 - ba[0], S / 2 + ha / 2 - ba[3] + ha * 0 + (ha / 2 - ha / 2))
        corps += (f'<path d="{dN}" fill="{encre}"/>'
                  f'<line x1="{S*.52:.1f}" y1="{S*.33:.1f}" x2="{S*.52:.1f}" y2="{S*.67:.1f}" stroke="{encre}" stroke-opacity=".55" stroke-width="{S*.006:.1f}"/>'
                  f'<path d="{da}" fill="{encre}"/>')
    return svg(S, S, corps)

FICHIERS = {
    'logo-vertical-bordeaux.svg': lambda: vertical(BORDEAUX, BORDEAUX),
    'logo-vertical-bordeaux-baseline.svg': lambda: vertical(BORDEAUX, BORDEAUX, '#6F625A'),
    'logo-vertical-brun.svg': lambda: vertical(BRUN, BRUN),
    'logo-vertical-ivoire.svg': lambda: vertical(IVOIRE, IVOIRE),
    'logo-vertical-ivoire-or.svg': lambda: vertical(OR, IVOIRE),
    'logo-horizontal-bordeaux.svg': lambda: horizontal(BORDEAUX, BORDEAUX),
    'logo-horizontal-brun.svg': lambda: horizontal(BRUN, BRUN),
    'logo-horizontal-ivoire.svg': lambda: horizontal(IVOIRE, IVOIRE),
    'logo-horizontal-ivoire-or.svg': lambda: horizontal(IVOIRE, OR),
    'monogramme-N.svg': lambda: monogramme('N'),
    'monogramme-N-noun.svg': lambda: monogramme('NN'),
}
def generer(dossier):
    os.makedirs(dossier, exist_ok=True)
    for nom, f in FICHIERS.items():
        open(os.path.join(dossier, nom), 'w').write(f())

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'capitales':
        NOM, ESP, T_LAT = 'ATELIER NAJJAR', 30, 150
    generer(sys.argv[2] if len(sys.argv) > 2 else OUT)
