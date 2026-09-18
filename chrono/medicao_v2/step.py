# -*- coding: utf-8 -*-
"""Reconstroi as pecas do Chrono como SOLIDO B-rep (OpenCASCADE via CadQuery) e
exporta STEP AP214 — cilindro e cilindro de verdade, nao triangulo.

Mesma geometria, mesmas cotas e MESMO sistema de coordenadas do build.py.
Conferencia contra o STL validado esta em confere_step.py.

  python3 step.py m02|m03|m01add|tudo
"""
import sys, os, numpy as np, cadquery as cq
from OCP.gp import gp_Trsf
from OCP.BRepCheck import BRepCheck_Analyzer
from math import pi, radians, cos, sin
from shapely.geometry import Polygon as SP
from shapely.geometry.polygon import orient
from shapely import affinity
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib3d import CX, CZ, polys_to_shapely
import icone

OUT = '/home/user/produtos/chrono/step_v2'; os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- cotas (= build.py)
FACE = 37.23
DIA_R, DIA_CAP, DIA_REL = 16.85, 1.70, 0.25
MESA_RI, MESA_RE, MESA_H = 14.20, 18.75, 0.18
CONCHA_A0, CONCHA_A1, CONCHA_Y0 = 55.0, 125.0, 36.15
REB_H, REB_RE = 0.60, 13.60
POST_R, POST_TOP = 6.60, 38.25
CHAPA_Y0, FURO_R, FURO_CH = 35.40, 3.00, 0.35
DET_R = 7.80
ARO_RI, ARO_RE, ARO_ESP = 6.80, 13.40, 1.60
ARO_Y0 = FACE - REB_H + 0.02; ARO_Y1 = ARO_Y0 + ARO_ESP
MES_R, MES_CAP, MES_REL, MES_XS = 9.80, 2.00, 0.30, 1.00
CUBO_Y0, TOPO = 38.35, 39.95
PINO_RE, PINO_Y1, PINO_Y0, FARPA_R = 2.90, 34.00, CHAPA_Y0, 3.40
FENDA_W, FENDAS = 0.70, 4
MARCA_REL, ICONE_H = 0.25, 8.00
BULBO_R, BULBO_OFF, NARIZ_R, NARIZ_Y = 8.20, 1.00, 1.20, 14.35
JAN_R0, JAN_R1, JAN_M, JAN_RC = 8.70, 11.30, 1.80, 0.70

_FP = FontProperties(family="FreeSans", weight="bold")
def glyphs(txt, cap, xs=1.0):
    tp = TextPath((0, 0), txt, size=1.0, prop=_FP)
    polys = [np.asarray(p) for p in tp.to_polygons() if len(p) >= 3]
    h = TextPath((0, 0), "8", size=1.0, prop=_FP).get_extents().height
    k = cap / h
    allp = np.vstack(polys); c = (allp.min(0) + allp.max(0)) / 2
    return [(p - c) * k * np.array([xs, 1.0]) for p in polys]

# ---------------------------------------------------------------- primitivas B-rep
def rev(prof):
    """perfil fechado [(r,y)] revolvido em torno de Y — superficie analitica."""
    lim = []
    for p in prof:
        if not lim or abs(p[0]-lim[-1][0]) > 1e-9 or abs(p[1]-lim[-1][1]) > 1e-9: lim.append(p)
    return (cq.Workplane("XY").polyline([(float(r), float(y)) for r, y in lim])
              .close().revolve(360, (0, 0, 0), (0, 1, 0)).val())

def cil(r, y0, y1, cx=0.0, cz=0.0):
    return cq.Solid.makeCylinder(r, y1-y0, cq.Vector(cx, y0, cz), cq.Vector(0, 1, 0))

def esfera(r, cx, cy, cz):
    return cq.Solid.makeSphere(r, cq.Vector(cx, cy, cz), angleDegrees1=-90, angleDegrees2=90)

def face_sp(poly):
    # ORIENTACAO IMPORTA: anel externo horario gera face com normal invertida e o
    # extrudeLinear devolve solido ao avesso — o corte apaga a peca inteira em vez
    # do sulco. Foi o que aconteceu com o icone depois do xflip.
    poly = orient(poly, 1.0)
    def wire(cs):
        pts = [(float(x), float(y)) for x, y in cs]
        if pts[0] == pts[-1]: pts = pts[:-1]
        return cq.Wire.makePolygon([cq.Vector(x, y, 0) for x, y in pts], close=True)
    return cq.Face.makeFromWires(wire(poly.exterior.coords), [wire(r.coords) for r in poly.interiors])

def prisma(poly, depth):
    return cq.Solid.extrudeLinear(face_sp(poly), cq.Vector(0, 0, depth))

def deitado(poly, depth, y0):
    """Prisma horizontal: o poligono fica no plano XZ e cresce em +Y a partir de y0.
    O build.py faz isso com uma matriz de determinante -1 (espelho). No trimesh nao
    da problema; no OpenCASCADE um solido espelhado sai com a orientacao invertida e
    o corte apaga a peca inteira. Aqui o espelho vira giro de verdade (det +1) e o
    poligono e que e invertido em y — mesmo resultado, solido valido."""
    p = affinity.scale(poly, xfact=1.0, yfact=-1.0, origin=(0, 0))
    t = gp_Trsf(); t.SetValues(1, 0, 0, 0,  0, 0, 1, y0,  0, -1, 0, 0)
    return prisma(p, depth).moved(cq.Location(t))

def place(shape, phi, R, top, depth):
    """mesma matriz do lib3d.place: local x=tangencial, y=radial, z=altura."""
    c, s = cos(phi), sin(phi)
    et = (-s, 0.0, c); er = (c, 0.0, s); ey = (0.0, 1.0, 0.0)
    tx, ty, tz = (R*er[0], (top-depth)*ey[1] + R*er[1], R*er[2])
    t = gp_Trsf(); t.SetValues(et[0], er[0], ey[0], tx,
                               et[1], er[1], ey[1], ty,
                               et[2], er[2], ey[2], tz)
    return shape.moved(cq.Location(t))

def relevo(itens, R, cap, base, alt, xs=1.0):
    out = []
    for phi, txt in itens:
        for sp in polys_to_shapely(glyphs(txt, cap, xs)):
            out.append(place(prisma(sp, alt), phi, R, base+alt, alt))
    return out

def fundir(ss):
    o = ss[0]
    for s in ss[1:]: o = o.fuse(s)
    return o.clean()

def tirar(a, ss):
    for s in ss: a = a.cut(s)
    return a.clean()

def grava_step(shape, nome):
    t = gp_Trsf(); t.SetValues(1, 0, 0, CX,  0, 1, 0, 0,  0, 0, 1, CZ)
    s = shape.moved(cq.Location(t))
    cq.exporters.export(cq.Workplane(obj=s), f'{OUT}/{nome}.step', exportType='STEP')
    ok = BRepCheck_Analyzer(s.wrapped).IsValid()
    print('  %-46s solidos=%d  faces=%4d  vol=%8.2f mm3  B-rep %s' %
          (nome+'.step', len(s.Solids()), len(s.Faces()), s.Volume(),
           'VALIDO' if ok else '*** INVALIDO ***'))
    return s

# ---------------------------------------------------------------- M02 rodinha
def m02():
    aro = rev([(ARO_RI, ARO_Y0), (ARO_RE, ARO_Y0), (ARO_RE, ARO_Y1-0.15), (ARO_RE-0.15, ARO_Y1),
               (ARO_RI+0.15, ARO_Y1), (ARO_RI, ARO_Y1-0.15)])
    txt = relevo([(radians(90+i*30), str(i+1)) for i in range(12)],
                 MES_R, MES_CAP, ARO_Y1-MES_REL, MES_REL+0.20, MES_XS)
    ent = [cil(1.10, (ARO_Y0+ARO_Y1)/2-2.0, (ARO_Y0+ARO_Y1)/2+2.0,
               13.75*cos(radians(90+(i+0.5)*30)), 13.75*sin(radians(90+(i+0.5)*30)))
           for i in range(12)]
    dim = [esfera(0.55, DET_R*cos(radians(90+i*30)), ARO_Y0+0.55-0.25, DET_R*sin(radians(90+i*30)))
           for i in range(12)]
    return tirar(aro, txt+ent+dim)

# ---------------------------------------------------------------- M03 ponteira
def gota(rb=BULBO_R, off=BULBO_OFF, rn=NARIZ_R, yn=NARIZ_Y, n=180):
    t = np.linspace(0, 2*pi, n, endpoint=False)
    pa = [(rb*cos(a), -off+rb*sin(a)) for a in t]
    pb = [(rn*cos(a),  yn+rn*sin(a)) for a in t]
    return SP(pa).union(SP(pb)).convex_hull

def ret_arred(r0, r1, meia, rc):
    return SP([(-meia+rc, r0+rc), (meia-rc, r0+rc), (meia-rc, r1-rc), (-meia+rc, r1-rc)]).buffer(rc, join_style=1)

def m03():
    cubo = cil(3.30, CUBO_Y0, TOPO)
    pino = rev([(2.05, CUBO_Y0), (PINO_RE, CUBO_Y0), (PINO_RE, PINO_Y0), (FARPA_R, PINO_Y0),
                (2.55, PINO_Y1), (2.35, PINO_Y1), (2.35, PINO_Y0), (2.05, CUBO_Y0)])
    lamina = place(prisma(gota(), TOPO-CUBO_Y0), radians(90), 0.0, TOPO, TOPO-CUBO_Y0)
    fendas, drenos = [], []
    for i in range(FENDAS):
        a = radians(45+i*360.0/FENDAS)
        fendas.append(place(prisma(SP([(-FENDA_W/2, 0.0), (FENDA_W/2, 0.0),
                                       (FENDA_W/2, 4.20), (-FENDA_W/2, 4.20)]),
                                   CUBO_Y0-PINO_Y1+0.2), a, 0.0, CUBO_Y0, CUBO_Y0-PINO_Y1+0.2))
        drenos.append(place(prisma(SP([(-0.35, 2.60), (0.35, 2.60), (0.35, 8.20), (-0.35, 8.20)]), 0.30),
                            a, 0.0, CUBO_Y0+0.30, 0.30))
    jp = ret_arred(JAN_R0, JAN_R1, JAN_M, JAN_RC)
    jan = place(prisma(jp, TOPO-CUBO_Y0+0.6), radians(90), 0.0, TOPO+0.3, TOPO-CUBO_Y0+0.6)
    ch  = place(prisma(jp.buffer(0.45, join_style=1), 0.75), radians(90), 0.0, TOPO+0.35, 0.75)
    marcas = ([place(prisma(sp, MARCA_REL+0.2), radians(90), 7.40, TOPO+0.2, MARCA_REL+0.2)
               for sp in polys_to_shapely(glyphs('M', 1.10))] +
              [place(prisma(sp, MARCA_REL+0.2), radians(90), 13.60, TOPO+0.2, MARCA_REL+0.2)
               for sp in polys_to_shapely(glyphs('D', 1.10))])
    ico = [deitado(sp, MARCA_REL+0.2, TOPO-MARCA_REL)
           for sp in icone.poligonos(ICONE_H, xflip=True)]
    return tirar(fundir([cubo, pino, lamina]), fendas+drenos+marcas+ico+[jan, ch])

# ---------------------------------------------------------------- M01: so os acrescimos
def m01add():
    """O que o Chrono ACRESCENTA a valvula existente. A metade de baixo da
    valvula vem do STL injetado do cliente (malha, sem CAD), entao nao pode
    virar B-rep aqui — a ferramentaria funde isto no CAD original da valvula."""
    poste = rev([(POST_R, CHAPA_Y0), (POST_R, POST_TOP-0.30), (POST_R-0.30, POST_TOP),
                 (FURO_R, POST_TOP), (FURO_R, CHAPA_Y0)])
    mesa = rev([(MESA_RI, FACE-0.60), (MESA_RE, FACE-0.60), (MESA_RE, FACE+MESA_H-0.10),
                (MESA_RE-0.10, FACE+MESA_H), (MESA_RI+0.10, FACE+MESA_H), (MESA_RI, FACE+MESA_H-0.10)])
    pol = [(0.0, 0.0)] + [(18.80*cos(radians(a)), 18.80*sin(radians(a)))
                          for a in np.linspace(CONCHA_A0, CONCHA_A1, 64)]
    cunha = deitado(SP(pol), FACE-CONCHA_Y0, CONCHA_Y0)
    anel = cil(18.80, CONCHA_Y0, FACE).cut(cil(MESA_RI, CONCHA_Y0-1, FACE+1))
    ench = cunha.intersect(anel)
    SD = 360.0/31
    dias = relevo([(radians(90+(d-1)*SD), '%d' % d) for d in range(1, 32)],
                  DIA_R, DIA_CAP, FACE+MESA_H, DIA_REL)
    mol = [esfera(0.42, DET_R*cos(radians(a)), FACE-REB_H+0.18-0.42, DET_R*sin(radians(a)))
           for a in (0, 180)]
    reb = rev([(POST_R, FACE-REB_H), (REB_RE, FACE-REB_H), (REB_RE, FACE+0.5), (POST_R, FACE+0.5)])
    furo = fundir([cil(FURO_R, CHAPA_Y0-2.0, POST_TOP+0.5),
                   rev([(FURO_R, POST_TOP-FURO_CH), (FURO_R+FURO_CH, POST_TOP),
                        (FURO_R+FURO_CH, POST_TOP+0.5), (FURO_R, POST_TOP+0.5)])])
    add = fundir([tirar(fundir([mesa, ench]+dias), [reb]), poste]+mol)
    # Receita exata, na ordem (a mesma do build.py):
    #   valvula_final = ((valvula_original - REBAIXO) + ACRESCIMO) - FURO
    # O rebaixo sai ANTES do acrescimo porque as duas molas de detente nascem no
    # FUNDO dele: subtrair o rebaixo depois raspa as molas.
    return add, reb, furo

if __name__ == '__main__':
    alvo = sys.argv[1] if len(sys.argv) > 1 else 'tudo'
    print('gerando STEP em', OUT)
    if alvo in ('m02', 'tudo'): grava_step(m02(), 'Chrono_M02_Rodinha_Meses')
    if alvo in ('m03', 'tudo'): grava_step(m03(), 'Chrono_M03_Ponteira')
    if alvo in ('m01add', 'tudo'):
        add, reb, furo = m01add()
        grava_step(reb,  'Chrono_M01a_SUBTRAIR_1_rebaixo')
        grava_step(add,  'Chrono_M01b_SOMAR_2_poste_mesa_dias_detentes')
        grava_step(furo, 'Chrono_M01c_SUBTRAIR_3_furo_passante')
