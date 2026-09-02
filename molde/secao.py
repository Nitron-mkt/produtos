# -*- coding: utf-8 -*-
"""Dois cortes cotados, gerados das MESMAS cotas do modelo.

A-A  corte longitudinal a 18 mm do eixo: aro, junta do aro, batente, boca,
     junta da boca e o cursor.
B-B  corte transversal em y = 15: aba do corpo, trava de correr, trilho da
     porta e o patim do cursor pousado no piso.
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pecas import P, K, do, dw, di
from geo import zval

HY, HX = P['HY'], P['HX']
TKF = P['TK_CY'] + P['TK_HY']          # 90  — parede frontal da pista
BCF = P['BC_CY'] + P['BC_HY']          # 82  — borda frontal da boca
CUF = P['CU_CY'] + P['CU_HY']          # 88  — borda frontal do cursor
ABA = zval(P['ABA_D'], 15.0, P['ABA_YC'], P['ABA_W'], 1.6)

F = lambda v: ('%.2f' % v).rstrip('0').rstrip('.').replace('.', ',')


# ----------------------------------------------------------------- A-A ----
def aa_corpo():
    W = P['WALL'] + P['RECUO']
    p = [(dw(111.0), 111.0), (dw(P['Z_FLARE0']), P['Z_FLARE0']),
         (do(P['Z_FLARE1']), P['Z_FLARE1']), (do(119.70), 119.70),
         (-0.20, P['H']), (-W + 0.20, P['H']), (-W, 119.70), (di(111.0), 111.0)]
    return [(HY + d, z) for (d, z) in p]


def aa_tampa():
    ZT, ZB, ZBD, ZK = P['Z_PLATE_T'], P['Z_PLATE_B'], P['Z_BORDA'], P['Z_TRACK']
    o = lambda d: HY + d
    pts = [(BCF, ZK), (BCF, P['Z_SLAB']), (TKF, P['Z_SLAB']), (TKF, ZB), (o(P['SEAM']), ZB)]
    pts += [(o(d), z) for (d, z) in [
        (P['LIP_IN'], ZB), (P['LIP_IN'], P['LIP_TIP'] + 0.40),
        (P['LIP_IN'] + 0.40, P['LIP_TIP']), (P['LIP_ROOT'] - 0.20, P['LIP_TIP'] + 0.40),
        (P['LIP_ROOT'], P['LIP_TIP'] + 1.40), (P['LIP_ROOT'], ZB),
        (P['GR_D0'], ZB), (P['GR_D0'], P['GR_Z']), (P['GR_D1'], P['GR_Z']),
        (P['GR_D1'], ZB), (P['LEG_IN'], ZB), (P['LEG_IN'], P['Z_SKIRT']),
        (P['LEG_OUT'], P['Z_SKIRT']), (P['LEG_OUT'], ZBD - 0.60),
        (P['LEG_OUT'] - 0.40, ZBD), (-P['BORDA_W'], ZBD), (-P['BORDA_W'], ZT),
        (P['SEAM'], ZT)]]
    pts += [(TKF, ZT), (TKF, ZK), (BCF + P['GB_D1'], ZK),
            (BCF + P['GB_D1'], P['GB_Z']), (BCF + P['GB_D0'], P['GB_Z']),
            (BCF + P['GB_D0'], ZK)]
    return pts


def aa_cursor():
    z0 = P['Z_TRACK']
    z1 = z0 + P['CU_T']
    return [(CUF - 26.0, z0), (CUF, z0), (CUF, z1 - 0.30),
            (CUF - 0.30, z1), (CUF - 26.0, z1)]


def aa_junta_aro():
    d0 = P['GR_D0'] + 0.05
    zt = P['Z_PLATE_B'] + P['TPE_SEAT']
    return _anel(HY + d0, HY + d0 + P['TPE_W'], zt - P['TPE_H'], zt)


def aa_junta_boca():
    d0 = BCF + P['GB_D0'] + 0.05
    zt = P['Z_TRACK'] + P['TPE_OUT']
    return _anel(d0, d0 + P['TPE_W'], zt - P['TPE_H'], zt)


def _anel(a0, a1, zb, zt, r=0.35):
    return [(a0 + r, zb), (a1 - r, zb), (a1, zb + r), (a1, zt - r),
            (a1 - r, zt), (a0 + r, zt), (a0, zt - r), (a0, zb + r)]


# ----------------------------------------------------------------- B-B ----
def bb_corpo():
    W = P['WALL'] + P['RECUO']
    a0, a1, a2 = P['ABA_Z0'], P['ABA_Z1'], P['ABA_Z2']
    p = [(dw(106.0), 106.0), (dw(a0 - 0.10), a0 - 0.10),
         (dw(a0) + ABA, a0), (dw(a1) + ABA, a1), (dw(a2), a2),
         (dw(P['Z_FLARE0']), P['Z_FLARE0']), (do(P['Z_FLARE1']), P['Z_FLARE1']),
         (do(119.70), 119.70), (-0.20, P['H']), (-W + 0.20, P['H']),
         (-W, 119.70), (di(106.0), 106.0)]
    return [(HX + d, z) for (d, z) in p]


def bb_tampa():
    ZT, ZB, ZBD, ZK = P['Z_PLATE_T'], P['Z_PLATE_B'], P['Z_BORDA'], P['Z_TRACK']
    o = lambda d: HX + d
    pts = [(P['TK_HX'], ZK), (P['TK_HX'], ZB), (o(P['SEAM']), ZB)]
    pts += [(o(d), z) for (d, z) in [
        (P['LIP_IN'], ZB), (P['LIP_IN'], P['LIP_TIP'] + 0.40),
        (P['LIP_IN'] + 0.40, P['LIP_TIP']), (P['LIP_ROOT'] - 0.20, P['LIP_TIP'] + 0.40),
        (P['LIP_ROOT'], P['LIP_TIP'] + 1.40), (P['LIP_ROOT'], ZB),
        (P['GR_D0'], ZB), (P['GR_D0'], P['GR_Z']), (P['GR_D1'], P['GR_Z']),
        (P['GR_D1'], ZB), (P['LEG_IN'], ZB), (P['LEG_IN'], P['Z_SKIRT']),
        (P['LEG_OUT'], P['Z_SKIRT']), (P['LEG_OUT'], ZBD - 0.60),
        (P['LEG_OUT'] - 0.40, ZBD), (-P['BORDA_W'], ZBD), (-P['BORDA_W'], ZT),
        (P['SEAM'], ZT)]]
    pts += [(P['TK_HX'], ZT)]
    return pts


def bb_trilho_porta():
    x0, x1 = P['TK_HX'], P['TK_HX'] + P['RAIL_W']
    lp = P['TK_HX'] - P['RAIL_LIP']
    return [(x0, P['Z_TRACK']), (x1, P['Z_TRACK']), (x1, P['RAIL_Z']),
            (lp, P['RAIL_Z']), (lp, P['RAIL_LIP_Z']), (x0, P['RAIL_LIP_Z'])]


def bb_trilho_trava():
    x = lambda d: HX + d
    return [[(x(P['RAIL_D0']), P['TRV_Z1']), (x(P['RAIL_D1']), P['TRV_Z1']),
             (x(P['RAIL_D1']), P['TRV_Z2']), (x(P['RAIL_D0']), P['TRV_Z2'])],
            [(x(P['RAIL_D1']), P['TRV_Z0']), (x(P['RAIL_D2']), P['TRV_Z0']),
             (x(P['RAIL_D2']), P['TRV_Z3']), (x(P['RAIL_D1']), P['TRV_Z3'])]]


def bb_trava():
    x = lambda d: HX + d
    d2, d3 = P['RAIL_D2'], P['TR_D3']
    return [[(x(d2), P['TR_Z_BOT']), (x(d3), P['TR_Z_BOT']),
             (x(d3), P['TR_Z_TOP']), (x(d2), P['TR_Z_TOP'])],
            [(x(P['RAIL_D1'] - 0.20), P['TR_ZB']), (x(d2), P['TR_ZB']),
             (x(d2), P['TRV_Z0']), (x(P['RAIL_D1'] - 0.20), P['TRV_Z0'])],
            [(x(P['RAIL_D1'] - 0.20), P['TRV_Z3']), (x(d2), P['TRV_Z3']),
             (x(d2), P['TR_Z_TOP']), (x(P['RAIL_D1'] - 0.20), P['TR_Z_TOP'])],
            [(x(P['TG_D']), P['TG_BOT']), (x(d2), P['TG_BOT']),
             (x(d2), P['TG_LAND']), (x(P['TG_D']), P['TG_LAND'])],
            [(x(d3), 116.2), (x(d3 + 0.60), 116.2), (x(d3 + 0.60), 119.0), (x(d3), 119.0)]]


def bb_cursor():
    z0, z1 = P['Z_TRACK'], P['Z_TRACK'] + P['CU_T']
    return [[(P['CU_HX'] - 22.0, z0), (P['CU_HX'], z0),
             (P['CU_HX'], z1 - 0.30), (P['CU_HX'] - 0.30, z1), (P['CU_HX'] - 22.0, z1)],
            [(P['SK_X0'], z0 - P['PAD_H']), (P['SK_X1'], z0 - P['PAD_H']),
             (P['SK_X1'], z0), (P['SK_X0'], z0)]]


def bb_junta_boca():
    d0 = P['BC_HX'] + P['GB_D0'] + 0.05
    zt = P['Z_TRACK'] + P['TPE_OUT']
    return _anel(d0, d0 + P['TPE_W'], zt - P['TPE_H'], zt)


def bb_junta_aro():
    d0 = P['GR_D0'] + 0.05
    zt = P['Z_PLATE_B'] + P['TPE_SEAT']
    return _anel(HX + d0, HX + d0 + P['TPE_W'], zt - P['TPE_H'], zt)


# --------------------------------------------------------------- desenho ---
STYLE = '''<style>
.corpo{fill:var(--sw-pp,#C3D0D4);fill-opacity:.5;stroke:var(--ink,#15191A);stroke-width:1}
.tampa{fill:var(--sw-teal,#17959F);fill-opacity:.4;stroke:var(--ink,#15191A);stroke-width:1}
.curs{fill:var(--sw-op,#B9C2C4);fill-opacity:.65;stroke:var(--ink,#15191A);stroke-width:1}
.trava{fill:var(--clay,#A8703C);fill-opacity:.5;stroke:var(--ink,#15191A);stroke-width:1}
.tpe{fill:var(--seal,#B23A22);fill-opacity:.85;stroke:var(--ink,#15191A);stroke-width:.9}
.ld{stroke:var(--faint,#8A9291);stroke-width:.8;fill:none}
.dot{fill:var(--teal,#0E7C86)}
.tx{font-family:"Martian Mono",ui-monospace,monospace;font-size:10px;fill:var(--ink,#15191A)}
.sb{font-family:"Karla",sans-serif;font-size:9.5px;fill:var(--faint,#8A9291)}
.cap{font-family:"Martian Mono",ui-monospace,monospace;font-size:9px;fill:var(--faint,#8A9291);
     letter-spacing:.08em;text-transform:uppercase}
</style>'''


class Draw:
    def __init__(self, a0, a1, z0, z1, s=14.0):
        self.a0, self.z1, self.s = a0, z1, s
        self.W, self.H = (a1 - a0) * s, (z1 - z0) * s
        self.o = []

    def X(self, a):
        return (a - self.a0) * self.s

    def Y(self, z):
        return (self.z1 - z) * self.s

    def path(self, pts, cls):
        d = 'M' + ' L'.join('%.2f %.2f' % (self.X(a), self.Y(b)) for (a, b) in pts) + ' Z'
        self.o.append('<path class="%s" d="%s"/>' % (cls, d))

    def leader(self, a, z, ta, tz, txt, anchor='start', sub=''):
        dx = 4 if anchor == 'start' else -4
        self.o.append('<path class="ld" d="M%.1f %.1f L%.1f %.1f"/>'
                      % (self.X(a), self.Y(z), self.X(ta), self.Y(tz)))
        self.o.append('<circle class="dot" cx="%.1f" cy="%.1f" r="1.6"/>'
                      % (self.X(a), self.Y(z)))
        self.o.append('<text class="tx" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                      % (self.X(ta) + dx, self.Y(tz) + 3, anchor, txt))
        if sub:
            self.o.append('<text class="sb" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
                          % (self.X(ta) + dx, self.Y(tz) + 13, anchor, sub))

    def cap(self, txt):
        self.o.append('<text class="cap" x="4" y="%.1f">%s</text>' % (self.H - 4, txt))

    def svg(self, label):
        return ('<svg class="draw" viewBox="0 0 %.0f %.0f" xmlns="http://www.w3.org/2000/svg" '
                'role="img" aria-label="%s">%s%s</svg>'
                % (self.W, self.H, label, STYLE, ''.join(self.o)))


def svg_aa():
    d = Draw(78.0, 112.0, 112.0, 126.5, 20.0)
    d.path(aa_corpo(), 'corpo')
    d.path(aa_tampa(), 'tampa')
    d.path(aa_cursor(), 'curs')
    d.path(aa_junta_aro(), 'tpe')
    d.path(aa_junta_boca(), 'tpe')
    d.leader(HY - 1.2, P['Z_PLATE_B'] + 0.5, 90.0, 125.6,
             'junta do aro %s mm' % F(P['TPE_W']), 'end',
             sub='aperto %s mm (%d%%) em %s mm' % (F(P['TPE_OUT']), 29, F(590.4)))
    d.leader(HY - P['WALL'] - P['RECUO'] + 0.4, P['Z_PLATE_B'], 82.0, 122.0,
             'batente', sub='topo do aro na mesa — o aperto e geometria')
    d.leader(BCF + P['GB_D0'] + 0.7, P['Z_TRACK'] + 0.2, 79.0, 116.0,
             'junta da boca', sub='o cursor desce 0,55 e comprime')
    d.leader(CUF - 3.0, P['Z_TRACK'] + P['CU_T'], 96.0, 118.5,
             'cursor %s mm' % F(P['CU_T']), sub='corre %s mm' % F(P['CU_CURSO']))
    d.cap('A-A · corte longitudinal a 18 mm do eixo')
    return d.svg('Corte longitudinal da vedacao')


def svg_bb():
    d = Draw(30.0, 61.0, 106.0, 126.5, 20.0)
    d.path(bb_corpo(), 'corpo')
    d.path(bb_tampa(), 'tampa')
    d.path(bb_trilho_porta(), 'tampa')
    for p in bb_trilho_trava():
        d.path(p, 'tampa')
    for p in bb_trava():
        d.path(p, 'trava')
    for p in bb_cursor():
        d.path(p, 'curs')
    d.path(bb_junta_aro(), 'tpe')
    d.path(bb_junta_boca(), 'tpe')
    crest = dw(P['ABA_Z0']) + ABA
    d.leader(HX + (P['TG_D'] + crest) / 2, P['ABA_Z0'], 31.0, 110.0,
             'engate %s mm' % F(crest - P['TG_D']),
             sub='aba de %s mm · face a 0 grau' % F(P['ABA_D']))
    d.leader(HX + P['RAIL_D1'], (P['TRV_Z1'] + P['TRV_Z2']) / 2, 58.5, 124.0,
             'trilho em T', 'end', sub='secao constante — gaveta reta em Y')
    d.leader(P['SK_X0'] + 2.0, P['Z_TRACK'] - P['PAD_H'] / 2, 33.0, 121.0,
             'patim %s mm' % F(P['PAD_H']), sub='4 patins descem juntos')
    d.leader(P['TK_HX'] - 0.2, P['RAIL_LIP_Z'], 44.0, 125.6,
             'labio %s mm' % F(P['RAIL_LIP']), 'end', sub='extracao forcada')
    d.cap('B-B · corte transversal em y = 15 mm, trava fechada')
    return d.svg('Corte transversal da trava')


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    open(os.path.join(here, 'web/secao-aa.svg'), 'w').write(svg_aa())
    open(os.path.join(here, 'web/secao-bb.svg'), 'w').write(svg_bb())
    print('secao-aa.svg + secao-bb.svg')
