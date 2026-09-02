# -*- coding: utf-8 -*-
"""Corte longitudinal A-A (a 12 mm do eixo) — gerado das MESMAS cotas do modelo."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pecas import P, K, KC, do, di, DI_SEAL
from geo import zval

XS = 12.0                       # plano do corte: passa pela trava e pelo ressalto
CATCH = zval(P['CATCH_D'], XS, 0.0, P['CATCH_W'], 2.0)
BEAD = zval(P['BEAD'], XS, 16.0, 8.0, 1.5) + zval(P['BEAD'], XS, -16.0, 8.0, 1.5)
CHAM = zval(-0.60, XS, 16.0, 9.0, 1.5) + zval(-0.60, XS, -16.0, 9.0, 1.5)
HY, PKF, THF = P['HY'], P['PK_CY'] + P['PK_HY'], P['PK_CY'] + P['TH_HY']
ZC = 98.0                       # altura do corte inferior do desenho


def corpo_pts():
    zc0, zc1, zc2 = P['CATCH_Z0'], P['CATCH_Z1'], P['CATCH_Z2']
    p = [(do(ZC), ZC), (do(zc0 - 0.05), zc0 - 0.05),
         (do(zc0) + CATCH, zc0), (do(zc1) + CATCH, zc1), (do(zc2), zc2),
         (do(119.70), 119.70), (-0.20, P['H']), (-P['WALL'] + 0.20, P['H']),
         (-P['WALL'], 119.70), (DI_SEAL, P['Z_SEAL1']), (DI_SEAL, P['Z_SEAL0']),
         (di(P['Z_SEAL0'] - 0.40), P['Z_SEAL0'] - 0.40), (di(ZC), ZC)]
    return [(HY + d, z) for (d, z) in p]


def tampa_pts():
    dcb = -KC * (P['Z_PK'] - P['COLLAR_Z'])
    cw, ZT, ZB, ZP = P['COLLAR_W'], P['Z_PLATE_T'], P['Z_PLATE_B'], P['Z_PK']
    per = [(P['LEG_OUT'], P['Z_SKIRT']), (P['LEG_OUT'], ZT - 1.00),
           (P['LEG_OUT'] - 0.45, ZT)]
    fim = [(P['LIP_IN'], ZB), (P['LIP_IN'], P['LIP_TIP'] + 0.40),
           (P['LIP_IN'] + 0.55, P['LIP_TIP']), (-2.30, P['LIP_TIP'] + 0.60),
           (P['LIP_CREST'], P['Z_CREST']), (P['LIP_ROOT'], P['Z_CREST'] + 1.80),
           (P['LIP_ROOT'], ZB), (P['LEG_IN'], ZB), (P['LEG_IN'], P['Z_SKIRT'])]
    pts = [(HY + d, z) for (d, z) in per]
    pts += [(PKF, ZT), (PKF + BEAD, P['BEAD_Z']), (PKF, ZP), (THF, ZP),
            (THF + dcb, P['COLLAR_Z']), (THF + cw, P['COLLAR_Z']),
            (THF + cw, P['Z_SLAB_B']), (PKF, P['Z_SLAB_B']), (PKF, ZB)]
    pts += [(HY + d, z) for (d, z) in fim]
    return pts


def porta_pts():
    g, ZT, ZB = -P['GAP'], P['Z_PLATE_T'], P['Z_PK']
    yc = P['PK_CY'] - 8.0
    return [(PKF + g, ZB), (PKF + g, ZT - 0.30), (PKF + g - 0.30 + CHAM, ZT),
            (yc, ZT), (yc, ZB), (THF + P['LIP2_IN'], ZB),
            (THF + P['LIP2_IN'], P['LIP2_TIP']), (THF - 0.90, P['LIP2_TIP']),
            (THF - 0.55, P['LIP2_TIP'] + 0.80),
            (THF + P['LIP2_CREST'], P['Z_CREST2']), (THF - 0.30, ZB)]


def alavanca_pts():
    yo = HY + P['LEG_OUT']
    return [[(yo, 112.60), (yo + 0.85, 112.60), (yo + 0.85, 113.05), (yo, 113.05)],
            [(yo + 0.25, 101.80), (yo + 1.45, 101.80), (yo + 1.45, 113.05), (yo + 0.25, 113.05)],
            [(yo + 0.25, 104.40), (yo + 0.25, 105.35), (103.00, 105.35), (103.75, 104.40)],
            [(yo + 0.25, 99.60), (yo + 2.30, 100.20), (yo + 2.30, 101.90), (yo + 0.25, 101.90)]]


# ---------------------------------------------------------------- desenho ---
S = 13.0
Y0, Y1, Z0, Z1 = 74.0, 110.5, ZC - 1.0, 128.0
Wd, Hd = (Y1 - Y0) * S, (Z1 - Z0) * S
X = lambda y: (y - Y0) * S
Y = lambda z: (Z1 - z) * S
f = lambda v: ('%.1f' % v).rstrip('0').rstrip('.')


def path(pts, cls):
    d = 'M' + ' L'.join('%.2f %.2f' % (X(a), Y(b)) for (a, b) in pts) + ' Z'
    return '<path class="%s" d="%s"/>' % (cls, d)


def leader(y, z, ty, tz, txt, anchor='start', sub=''):
    o = ['<path class="ld" d="M%.1f %.1f L%.1f %.1f"/>' % (X(y), Y(z), X(ty), Y(tz)),
         '<circle class="dot" cx="%.1f" cy="%.1f" r="1.7"/>' % (X(y), Y(z))]
    dx = 4 if anchor == 'start' else -4
    o.append('<text class="tx" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
             % (X(ty) + dx, Y(tz) + 3, anchor, txt))
    if sub:
        o.append('<text class="sb" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                 % (X(ty) + dx, Y(tz) + 14, anchor, sub))
    return ''.join(o)


def svg():
    o = ['<svg class="draw" viewBox="0 0 %.0f %.0f" xmlns="http://www.w3.org/2000/svg" '
         'role="img" aria-label="Corte longitudinal da vedacao">' % (Wd, Hd)]
    o.append('''<style>
    .corpo{fill:var(--sw-pp,#C3D0D4);fill-opacity:.55;stroke:var(--ink,#15191A);stroke-width:1.1}
    .tampa{fill:var(--sw-teal,#17959F);fill-opacity:.42;stroke:var(--ink,#15191A);stroke-width:1.1}
    .porta{fill:var(--sw-op,#B9C2C4);fill-opacity:.7;stroke:var(--ink,#15191A);stroke-width:1.1}
    .trava{fill:var(--sw-teal,#17959F);fill-opacity:.42;stroke:var(--ink,#15191A);stroke-width:1.1}
    .ld{stroke:var(--faint,#8A9291);stroke-width:.8;fill:none}
    .dot{fill:var(--teal,#0E7C86)}
    .tx{font-family:"Martian Mono",ui-monospace,monospace;font-size:10.5px;fill:var(--ink,#15191A)}
    .sb{font-family:"Karla",sans-serif;font-size:10px;fill:var(--faint,#8A9291)}
    .ax{stroke:var(--rule,#DAD6CD);stroke-width:.8;stroke-dasharray:6 4;fill:none}
    </style>''')
    o.append('<path class="ax" d="M0 %.1f L%.1f %.1f"/>' % (Y(P['Z_PLATE_B']), Wd, Y(P['Z_PLATE_B'])))
    o.append(path(corpo_pts(), 'corpo'))
    o.append(path(tampa_pts(), 'tampa'))
    o.append(path(porta_pts(), 'porta'))
    for p in alavanca_pts():
        o.append(path(p, 'trava'))
    L = P['LIP_CREST']
    o.append(leader(HY + (L + DI_SEAL) / 2, P['Z_CREST'], 77.0, 126.5,
                    'interferencia %s mm' % f(P['LIP_CREST'] - DI_SEAL).replace('.', ','),
                    sub='labio flexivel contra a banda de 0 grau'))
    o.append(leader(HY + P['LEG_IN'] + 0.9, P['Z_PLATE_B'] + 0.15, 93.0, 122.5,
                    'batente', sub='a mesa apoia no topo do aro'))
    o.append(leader(HY - P['WALL'] / 2, 116.0, 104.0, 110.5,
                    'canal %s mm' % f(P['LEG_IN'] - P['LIP_ROOT']).replace('.', ','),
                    'end', sub='folga externa 0,35 — o aro nao abre'))
    o.append(leader(HY + do(P['CATCH_Z0']) + CATCH / 2, P['CATCH_Z0'], 88.0, 103.0,
                    'engate 0,82 mm', 'end', sub='ressalto 1,20 · rampa 25 graus'))
    o.append(leader(THF + P['LIP2_CREST'] / 2, P['Z_CREST2'], 76.0, 112.0,
                    'interferencia 0,30 mm', sub='selo radial da portinhola'))
    o.append(leader(PKF + BEAD / 2, P['BEAD_Z'], 92.0, 127.2,
                    'retencao 0,90 mm', 'end', sub='trava a aba no rebaixo'))
    o.append(leader(THF + P['COLLAR_W'] / 2, 117.0, 76.0, 104.0,
                    'gargalo %s mm · 3 graus' % f(P['Z_PK'] - P['COLLAR_Z']).replace('.', ','),
                    sub='assento conico, entra centrando'))
    o.append('</svg>')
    return ''.join(o)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    open(os.path.join(here, 'web/secao.svg'), 'w').write(svg())
    print('secao.svg  %.0f x %.0f px' % (Wd, Hd))
