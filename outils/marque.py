# Génère les fichiers du logo Atelier Najjar dans marque/svg (SVG vectorisés : le texte
# est converti en tracés, aucun besoin d'installer les polices pour les ouvrir).
# Logo : نجّار en Amiri Bold, « ATELIER NAJJAR » en Tenor Sans, capitales légèrement espacées.
# Usage : python3 outils/marque.py [dossier de sortie]
import os, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ICI = os.path.dirname(os.path.abspath(__file__))
POLICES = os.path.join(ICI, 'polices')

BORDEAUX, IVOIRE, BRUN, OR, GRIS = '#5A1424', '#FBF8F3', '#2A1E1A', '#D9C29C', '#6F625A'
NOM, BASELINE, ARABE = 'ATELIER NAJJAR', 'CUISINE LIBANAISE  ·  PARIS', 'نجّار'
ESPACEMENT = .1  # espacement des lettres du nom, en fraction de la taille


class Police:
    def __init__(self, fichier):
        chemin = os.path.join(POLICES, fichier)
        self.tt = TTFont(chemin)
        self.glyphes = self.tt.getGlyphSet()
        self.noms = self.tt.getGlyphOrder()
        self.upm = self.tt['head'].unitsPerEm
        self.hb = hb.Font(hb.Face(open(chemin, 'rb').read()))

    def texte(self, s, taille, x=0, y=0, esp=0):
        """Tracé SVG de s posé sur la ligne de base y. Renvoie (d, largeur, bornes)."""
        buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
        hb.shape(self.hb, buf, {})
        k = taille / self.upm
        pen, bornes, cx = SVGPathPen(self.glyphes), BoundsPen(self.glyphes), 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            g = self.glyphes[self.noms[info.codepoint]]
            t = (k, 0, 0, -k, x + (cx + pos.x_offset) * k, y - pos.y_offset * k)
            g.draw(TransformPen(pen, t)); g.draw(TransformPen(bornes, t))
            cx += pos.x_advance + esp / k
        return pen.getCommands(), cx * k - esp, bornes.bounds

    def centre(self, s, taille, cx, y, esp=0):
        _, w, _ = self.texte(s, taille, 0, 0, esp)
        return self.texte(s, taille, cx - w / 2, y, esp)


tenor, amiri = Police('TenorSans-Regular.ttf'), Police('Amiri-Bold.ttf')


def svg(w, h, corps):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}">{corps}</svg>\n')


def chemin(d, couleur):
    return f'<path d="{d}" fill="{couleur}"/>'


def vertical(c_arabe, c_nom, c_baseline=None):
    """نجّار centré au-dessus du nom, baseline facultative."""
    M, T = 80, 150
    _, largeur, _ = tenor.texte(NOM, T, esp=ESPACEMENT * T)
    W = largeur + 2 * M
    _, _, b = amiri.centre(ARABE, 210, W / 2, 0)
    da, _, ba = amiri.centre(ARABE, 210, W / 2, M - b[1])
    _, _, b = tenor.centre(NOM, T, W / 2, 0, ESPACEMENT * T)
    dn, _, bn = tenor.centre(NOM, T, W / 2, ba[3] + 50 - b[1], ESPACEMENT * T)
    corps, bas = chemin(da, c_arabe) + chemin(dn, c_nom), bn[3]
    if c_baseline:
        db, _, bb = tenor.centre(BASELINE, 42, W / 2, bn[3] + 82, 11)
        corps += chemin(db, c_baseline); bas = bb[3]
    return svg(W, bas + M, corps)


def horizontal(c_nom, c_arabe):
    """Le nom suivi de نجّار, pour le menu et le pied de page."""
    M, T = 60, 150
    _, _, b = tenor.texte(NOM, T, esp=ESPACEMENT * T)
    base = M - b[1]
    dn, wn, bn = tenor.texte(NOM, T, M, base, ESPACEMENT * T)
    da, wa, ba = amiri.texte(ARABE, T * 1.15, M + wn + T * .4, base)
    haut, bas = min(bn[1], ba[1]), max(bn[3], ba[3])
    corps = f'<g transform="translate(0 {M - haut:.1f})">{chemin(dn, c_nom)}{chemin(da, c_arabe)}</g>'
    return svg(M + wn + T * .4 + wa + M, bas - haut + 2 * M, corps)


def monogramme(arabe=False, fond=BORDEAUX, encre=IVOIRE, S=512):
    """N seul (favicon) ou N + ن (réseaux sociaux), sur un disque."""
    corps = f'<circle cx="{S / 2}" cy="{S / 2}" r="{S / 2}" fill="{fond}"/>'
    if not arabe:
        _, _, b = tenor.centre('N', S * .56, S / 2, 0)
        d, _, _ = tenor.centre('N', S * .56, S / 2, S / 2 - (b[1] + b[3]) / 2)
        return svg(S, S, corps + chemin(d, encre))
    _, _, bN = tenor.texte('N', S * .4)
    dN, _, _ = tenor.texte('N', S * .4, S * .17 - bN[0], S / 2 - (bN[1] + bN[3]) / 2)
    _, _, ba = amiri.texte('ن', S * .46)
    da, _, _ = amiri.texte('ن', S * .46, S * .6 - ba[0], S / 2 - (ba[1] + ba[3]) / 2)
    filet = (f'<line x1="{S * .52:.1f}" y1="{S * .34:.1f}" x2="{S * .52:.1f}" y2="{S * .66:.1f}" '
             f'stroke="{encre}" stroke-opacity=".55" stroke-width="{S * .006:.1f}"/>')
    return svg(S, S, corps + chemin(dN, encre) + filet + chemin(da, encre))


FICHIERS = {
    'logo-vertical-bordeaux.svg': lambda: vertical(BORDEAUX, BORDEAUX),
    'logo-vertical-bordeaux-baseline.svg': lambda: vertical(BORDEAUX, BORDEAUX, GRIS),
    'logo-vertical-brun.svg': lambda: vertical(BRUN, BRUN),
    'logo-vertical-ivoire.svg': lambda: vertical(IVOIRE, IVOIRE),
    'logo-vertical-ivoire-or.svg': lambda: vertical(OR, IVOIRE),
    'logo-horizontal-bordeaux.svg': lambda: horizontal(BORDEAUX, BORDEAUX),
    'logo-horizontal-brun.svg': lambda: horizontal(BRUN, BRUN),
    'logo-horizontal-ivoire.svg': lambda: horizontal(IVOIRE, IVOIRE),
    'logo-horizontal-ivoire-or.svg': lambda: horizontal(IVOIRE, OR),
    'monogramme-N.svg': lambda: monogramme(),
    'monogramme-N-noun.svg': lambda: monogramme(arabe=True),
}

if __name__ == '__main__':
    sortie = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, '..', 'marque', 'svg')
    os.makedirs(sortie, exist_ok=True)
    for nom, fabrique in FICHIERS.items():
        open(os.path.join(sortie, nom), 'w').write(fabrique())
        print(nom)
