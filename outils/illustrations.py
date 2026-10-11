# Génère les illustrations de plats (sprite SVG) insérées dans index.html entre les commentaires illustrations:start et illustrations:end.
# Usage : python3 outils/illustrations.py sprite.svg
import random, math
R = random.Random(7)
def f(x): return f"{x:.1f}"

PLATE = ('<circle cx="100" cy="100" r="98" fill="#FFFFFF"/>'
         '<circle cx="100" cy="100" r="98" fill="none" stroke="#E2D8C6" stroke-width="1.5"/>'
         '<circle cx="100" cy="100" r="82" fill="none" stroke="#EFE8DA" stroke-width="2"/>')

def dots(n, color, rmin, rmax, area=62, cx=100, cy=100, band=None, opacity=1):
    out = []
    for _ in range(n):
        if band:  # (angle_deg, halfwidth)
            ang, hw = band
            t = R.uniform(-area, area); o = R.uniform(-hw, hw)
            a = math.radians(ang)
            x = cx + t*math.cos(a) - o*math.sin(a); y = cy + t*math.sin(a) + o*math.cos(a)
        else:
            rr = area*math.sqrt(R.random()); th = R.uniform(0, 2*math.pi)
            x, y = cx + rr*math.cos(th), cy + rr*math.sin(th)
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(R.uniform(rmin, rmax))}" fill="{color}"' + (f' opacity="{opacity}"' if opacity < 1 else '') + '/>')
    return ''.join(out)

def leaf(x, y, ang, l=10, w=4.5, color="#4E7A2E"):
    return f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{l}" ry="{w}" fill="{color}" transform="rotate({ang} {f(x)} {f(y)})"/>'

def swirl(color, base_r=68, width=5, op=.55):
    # concentric grooves made with a spoon
    s = ''
    for r in (58, 44, 30):
        s += f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{op}" stroke-dasharray="{r*1.6} {r*0.5}" transform="rotate({R.randint(0,360)} 100 100)"/>'
    return s

S = {}

S['hommos'] = (PLATE + '<circle cx="100" cy="100" r="72" fill="#E8D2A6"/>' + swirl('#D2B17A')
  + '<path d="M70 92 C85 80 118 84 132 100 C120 116 86 118 70 108 Z" fill="#E2B83E" opacity=".45"/>'
  + dots(70, '#B4232A', 2.6, 3.6, band=(-28, 6), area=58) + dots(18, '#7E1219', 2.2, 3, band=(-28, 5), area=52)
  + leaf(128, 74, 30) + leaf(136, 82, -20, 8, 4) + leaf(124, 84, 70, 7, 3.5, '#6A9A3C'))

S['labne'] = (PLATE + '<circle cx="100" cy="100" r="72" fill="#F6F1E6"/>' + swirl('#E3DAC8', op=.8)
  + '<path d="M64 100 C80 88 120 88 136 100 C120 112 80 112 64 100 Z" fill="#E6C24B" opacity=".4"/>'
  + dots(70, '#8FA046', 1.6, 2.8, band=(18, 9), area=52) + dots(18, '#C9A46A', 1.2, 2, band=(18, 9), area=50)
  + leaf(98, 92, -30, 11, 5, '#3F7A34') + leaf(108, 94, 40, 11, 5, '#4E8B3C') + leaf(102, 101, 95, 9, 4, '#5E9A45'))

S['mtabal'] = (PLATE + '<circle cx="100" cy="100" r="72" fill="#D3C1A2"/>' + swirl('#B9A27E', op=.7)
  + dots(40, '#6E5A3E', .8, 1.6, area=64, opacity=.6)
  + '<path d="M66 104 C82 92 118 92 134 100 C118 112 84 114 66 104 Z" fill="#DDB443" opacity=".45"/>'
  + ''.join(dots(5, '#7B55A8', 2, 2.6, cx=x, cy=y, area=4.5) + f'<circle cx="{x}" cy="{y}" r="1.6" fill="#F2D35C"/>'
            for x, y in [(78, 104), (92, 98), (106, 100), (120, 96), (99, 108)])
  + dots(16, '#3E6B2C', 1, 1.8, band=(-8, 7), area=40))

S['taboule'] = (PLATE + '<circle cx="100" cy="100" r="74" fill="#4D7A2A"/>'
  + dots(260, '#6E9B3A', 1.6, 3.2, area=70) + dots(120, '#3A6420', 1.4, 2.8, area=70)
  + dots(60, '#F1E6C8', .9, 1.5, area=68)
  + ''.join(f'<rect x="{f(x)}" y="{f(y)}" width="5.5" height="5.5" rx="1" fill="#D9472F" transform="rotate({R.randint(0,90)} {f(x+2.7)} {f(y+2.7)})"/>'
            for x, y in [(100+60*math.sqrt(R.random())*math.cos(t), 100+60*math.sqrt(R.random())*math.sin(t)) for t in [R.uniform(0, 6.3) for _ in range(16)]])
  + dots(14, '#B01E2C', 2.2, 3, area=62))

def orange(x, y, ang):
    return (f'<g transform="rotate({ang} {x} {y})"><path d="M{x-11} {y} A11 11 0 0 1 {x+11} {y} Z" fill="#F2A33A"/>'
            f'<path d="M{x-8} {y} A8 8 0 0 1 {x+8} {y} Z" fill="#F7C063"/></g>')
def cucumber(x, y):
    return f'<circle cx="{x}" cy="{y}" r="7" fill="#C9DB9A" stroke="#3E6B2C" stroke-width="2"/><circle cx="{x}" cy="{y}" r="2.5" fill="#E7F0CF"/>'
S['salade'] = (PLATE + '<circle cx="100" cy="100" r="74" fill="#3F6B2A"/>'
  + ''.join(leaf(100+62*math.sqrt(R.random())*math.cos(t), 100+62*math.sqrt(R.random())*math.sin(t), R.randint(0, 180), R.uniform(7, 12), R.uniform(3, 5), R.choice(['#5E8F36', '#7FAE45', '#4A7A2A', '#93BB55'])) for t in [R.uniform(0, 6.3) for _ in range(70)])
  + orange(78, 82, -20) + orange(124, 92, 30) + orange(96, 128, 160) + orange(132, 128, 200)
  + cucumber(104, 76) + cucumber(70, 118) + cucumber(118, 116)
  + dots(18, '#B01E2C', 2.2, 3.1, area=60) + dots(10, '#E0533A', 2.4, 3.2, area=58))

def ball(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#8C5A28"/>' + f'<circle cx="{x-r*.25}" cy="{y-r*.25}" r="{r*.7}" fill="#A06A31"/>'
            + dots(14, '#5E8A30', .6, 1.1, cx=x, cy=y, area=r*.85) + dots(10, '#5E3A18', .6, 1.2, cx=x, cy=y, area=r*.9))
S['falafel'] = (PLATE + f'<circle cx="68" cy="72" r="22" fill="#E9E2D3" stroke="#D7CCB6" stroke-width="2"/><circle cx="68" cy="72" r="17" fill="#EDE0BF"/><circle cx="68" cy="72" r="3" fill="#B4532A" opacity=".7"/>'
  + ''.join(ball(x, y, 15) for x, y in [(112, 66), (140, 92), (106, 98), (74, 118), (108, 132), (140, 124), (80, 150)]))

def roll(x, y, ang, l=96, w=19):
    g = f'<g transform="rotate({ang} {x} {y})"><rect x="{x-l/2}" y="{y-w/2}" width="{l}" height="{w}" rx="{w/2}" fill="#4F5F2B"/>'
    for i in range(1, 6):
        xx = x - l/2 + i*l/6
        g += f'<path d="M{xx} {y-w/2+1.5} q3 {w/2-1.5} 0 {w-3}" fill="none" stroke="#3A4720" stroke-width="1.4"/>'
    g += f'<rect x="{x-l/2+3}" y="{y-w/2+2}" width="{l-6}" height="3" rx="1.5" fill="#6C7D3C" opacity=".8"/></g>'
    return g
S['vigne'] = (PLATE + ''.join(roll(100, y, -14) for y in (54, 77, 100, 123, 146))
  + '<path d="M128 150 a14 14 0 0 1 28 0 Z" fill="#F2D35C" transform="rotate(-30 142 150)"/>'
  + leaf(60, 150, 40, 9, 2.5, '#5E8A30') + leaf(66, 146, -20, 8, 2.2, '#5E8A30'))

def kebbe(x, y, ang):
    return (f'<g transform="rotate({ang} {x} {y})"><path d="M{x-28} {y} C{x-14} {y-17} {x+14} {y-17} {x+28} {y} C{x+14} {y+17} {x-14} {y+17} {x-28} {y} Z" fill="#6E3F1E"/>'
            f'<path d="M{x-18} {y-3} Q{x} {y-14} {x+18} {y-3}" fill="none" stroke="#93602F" stroke-width="2" stroke-linecap="round"/></g>')
S['kebbe'] = (PLATE + ''.join(kebbe(x, y, a) for x, y, a in [(72, 66, 30), (118, 60, 30), (58, 104, 30), (102, 100, 30), (146, 96, 30), (84, 142, 30), (130, 138, 30)]))

def tri(x, y, ang, s=36):
    h = s*.87
    return (f'<g transform="rotate({ang} {x} {y})"><path d="M{x} {y-h*.66} L{x+s/2} {y+h*.34} L{x-s/2} {y+h*.34} Z" fill="#D9A257" stroke="#B9813C" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M{x} {y-h*.66} L{x} {y+h*.05} M{x+s/2} {y+h*.34} L{x} {y+h*.05} M{x-s/2} {y+h*.34} L{x} {y+h*.05}" stroke="#C08A42" stroke-width="1.2" opacity=".8"/></g>')
S['fatayer'] = (PLATE + ''.join(tri(x, y, a) for x, y, a in [(66, 70, 10), (102, 58, -15), (138, 74, 20), (60, 112, -25), (100, 100, 5), (140, 114, -10), (80, 146, 25), (120, 146, -20)]))

def moon(x, y, ang, r=25):
    g = f'<g transform="rotate({ang} {x} {y})"><path d="M{x-r} {y} A{r} {r} 0 0 1 {x+r} {y} Z" fill="#E1B169"/>'
    for i in range(9):
        a = math.pi + i*math.pi/8
        g += f'<circle cx="{f(x+(r-1)*math.cos(a))}" cy="{f(y+(r-1)*math.sin(a))}" r="2.1" fill="#C68E45"/>'
    g += f'<path d="M{x-r+5} {y-2} A{r-6} {r-6} 0 0 1 {x+r-5} {y-2}" fill="none" stroke="#F0CC8A" stroke-width="2.5" opacity=".7"/></g>'
    return g
S['samboussek'] = (PLATE + ''.join(moon(x, y, a) for x, y, a in [(72, 76, -10), (126, 72, 15), (64, 118, 5), (114, 112, -20), (88, 156, 10), (140, 150, -5)]))

S['feta'] = (PLATE + '<circle cx="100" cy="100" r="72" fill="#F7F3EA"/>' + swirl('#E6DDCB', op=.9)
  + dots(60, '#C7432E', .9, 1.8, area=56) + dots(30, '#7C8F3A', .8, 1.4, area=56)
  + '<path d="M70 100 C86 90 114 90 130 100 C114 110 86 110 70 100 Z" fill="#E6C24B" opacity=".35"/>')

with open(__import__('sys').argv[1], 'w') as fh:
    fh.write('<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true">')
    for k, v in S.items():
        fh.write(f'<symbol id="p-{k}" viewBox="0 0 200 200">{v}</symbol>')
    fh.write('</svg>')
print(list(S))
