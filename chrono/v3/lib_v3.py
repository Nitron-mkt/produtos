# -*- coding: utf-8 -*-
"""Primitivas B-rep do Chrono v3. OpenCASCADE via CadQuery.

Duas armadilhas do OCC que o trimesh perdoa e ele nao (ja custaram retrabalho):
  1. poligono com anel externo no sentido horario gera face de normal invertida,
     o extrudeLinear devolve solido ao avesso e o corte apaga a peca inteira;
  2. matriz de determinante -1 (espelho) faz o mesmo. Aqui vira giro de verdade.
"""
import sys, os, numpy as np, cadquery as cq
from math import pi, radians, degrees, cos, sin
from OCP.gp import gp_Trsf
from OCP.BRepCheck import BRepCheck_Analyzer
from shapely.geometry import Polygon as SP
from shapely.geometry.polygon import orient
from shapely import affinity
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'medicao_v2'))
from lib3d import polys_to_shapely
import params as P

_FP = FontProperties(family="FreeSans", weight="bold")
SEM_SAIDA = {'reto': 0, 'tol': {}}   # contador: quantos contornos o OCC recusou

# ---------------------------------------------------------------- 2D
MIN_SEG = 0.10   # menor segmento admitido num contorno, em mm

def limpa_contorno(poly, min_seg=None):
    """Garante que nenhum segmento do contorno fique abaixo de min_seg.

    POR QUE ISTO EXISTE: o SolidWorks (e todo importador de STEP) tem um limite
    de aresta curta. Aresta de 0,0015 mm — que era o que o buffer de arredondar
    canto deixava no contorno das letras — ele colapsa na importacao, a costura
    do solido se desfaz e a peca abre como um monte de superficie solta. Foi
    exatamente o que o projetista viu: 'toda fatiada, pontinhada'.

    0,05 mm num traco de 0,28 e numa letra de 1,50 nao muda nada visivel."""
    min_seg = MIN_SEG if min_seg is None else min_seg
    def anel(cs):
        pts = [tuple(map(float, c)) for c in cs]
        if pts[0] == pts[-1]: pts = pts[:-1]
        out = [pts[0]]
        for p in pts[1:]:
            if (p[0]-out[-1][0])**2 + (p[1]-out[-1][1])**2 >= min_seg*min_seg:
                out.append(p)
        # o fechamento tambem nao pode ser curto
        while len(out) > 3 and ((out[0][0]-out[-1][0])**2 + (out[0][1]-out[-1][1])**2) < min_seg*min_seg:
            out.pop()
        return out
    try:
        q = SP(anel(poly.exterior.coords), [anel(r.coords) for r in poly.interiors
                                            if len(anel(r.coords)) >= 3])
        if not q.is_valid: q = q.buffer(0)
        if q.geom_type == 'MultiPolygon': q = max(q.geoms, key=lambda g: g.area)
        if q.is_valid and q.geom_type == 'Polygon' and q.area > 0.6*poly.area:
            return q
    except Exception:
        pass
    return poly

def arredonda(poly, r):
    """tira os cantos vivos do contorno em planta, por fora e por dentro."""
    if r <= 0: return poly
    # quad_segs baixo de proposito: cada canto vira 2 segmentos, nao 8. Canto de
    # 0,06 mm partido em 8 gera aresta de micra, que e o que quebra a importacao.
    k = dict(join_style=1, quad_segs=2)
    q = poly.buffer(-r, **k).buffer(2*r, **k).buffer(-r, **k)
    if q.is_empty or q.geom_type != 'Polygon':
        q = poly.buffer(r, **k).buffer(-r, **k)
    return q if (not q.is_empty and q.geom_type == 'Polygon') else poly

def glifos(txt, cap=None, xs=1.0, rc=None):
    """poligonos do texto, centrados, altura de caixa alta = cap, cantos abaulados."""
    cap = P.LETRA_CAP if cap is None else cap
    rc  = P.LETRA_RC  if rc  is None else rc
    tp = TextPath((0, 0), txt, size=1.0, prop=_FP)
    polys = [np.asarray(p) for p in tp.to_polygons() if len(p) >= 3]
    h = TextPath((0, 0), "8", size=1.0, prop=_FP).get_extents().height
    k = cap / h
    allp = np.vstack(polys); c = (allp.min(0) + allp.max(0)) / 2
    brutos = [(p - c) * k * np.array([xs, 1.0]) for p in polys]
    return [limpa_contorno(arredonda(s, rc)) for s in polys_to_shapely(brutos)]

def largura(txt, **kw):
    ps = glifos(txt, **kw)
    b = [p.bounds for p in ps]
    return max(t[2] for t in b) - min(t[0] for t in b)

# ---------------------------------------------------------------- 3D
def face_sp(poly):
    poly = orient(poly, 1.0)
    def wire(cs):
        pts = [(float(x), float(y)) for x, y in cs]
        if pts[0] == pts[-1]: pts = pts[:-1]
        return cq.Wire.makePolygon([cq.Vector(x, y, 0) for x, y in pts], close=True)
    return cq.Face.makeFromWires(wire(poly.exterior.coords), [wire(r.coords) for r in poly.interiors])

def _wire(cs):
    pts = [(float(x), float(y)) for x, y in cs]
    if pts[0] == pts[-1]: pts = pts[:-1]
    return cq.Wire.makePolygon([cq.Vector(x, y, 0) for x, y in pts], close=True)

def simplifica(poly, tol=0.002):
    """o buffer de arredondar densifica o contorno; acima de ~200 pontos o
    prisma com saida do OCC comeca a recusar. 0,002 mm esta muito abaixo da
    tolerancia de qualquer molde."""
    q = poly.simplify(tol, preserve_topology=True)
    return q if (not q.is_empty and q.geom_type == 'Polygon') else poly

def prisma(poly, h, saida=0.0):
    """extrusao em +Z. saida>0 estreita para cima (a cavidade sai para +Z).

    ARMADILHA: Solid.extrudeLinear(outer, inner, vec, taper) com taper != 0
    IGNORA SILENCIOSAMENTE os aneis internos — o 8 sai sem os dois furos e o
    volume aumenta em vez de diminuir. Por isso, com saida, cada furo e
    extrudado a parte, com a saida invertida (furo alarga para cima), e
    subtraido."""
    if abs(saida) < 1e-9:
        f = face_sp(orient(simplifica(poly), 1.0))
        return cq.Solid.extrudeLinear(f.outerWire(), f.innerWires(), cq.Vector(0, 0, h))
    # o LocOpe_DPrism do OCC recusa contorno com segmento curto demais. Vai
    # afrouxando a simplificacao ate ele aceitar; so no fim desiste da saida,
    # e ai avisa em vez de entregar canto reto calado.
    for tol in (0.002, 0.006, 0.012, 0.020):
        q = orient(simplifica(poly, tol), 1.0)
        try:
            s = cq.Solid.extrudeLinear(_wire(q.exterior.coords), [], cq.Vector(0, 0, h), saida)
            for anel in q.interiors:
                w = _wire(anel.coords)
                furo = cq.Solid.extrudeLinear(w, [], cq.Vector(0, 0, h + 0.05), -saida).fuse(
                       cq.Solid.extrudeLinear(w, [], cq.Vector(0, 0, 0.1)).moved(cq.Location(cq.Vector(0, 0, -0.1))))
                s = s.cut(furo)
            SEM_SAIDA['tol'][tol] = SEM_SAIDA['tol'].get(tol, 0) + 1
            return s.clean()
        except Exception:
            continue
    SEM_SAIDA['reto'] += 1
    f = face_sp(orient(simplifica(poly), 1.0))
    return cq.Solid.extrudeLinear(f.outerWire(), f.innerWires(), cq.Vector(0, 0, h))

def mergulha(poly, rel, saida, ov):
    """Prisma de relevo que MERGULHA ov mm dentro do corpo.

    Encostar o solido do caractere na face por uma face coplanar faz o fuse do
    OCC devolver volume MENOR — e, num dos contornos do "MES", devolveu VAZIO.
    Com mergulho vira sobreposicao de volume e o booleano se comporta. A base e
    alargada em tan(saida)*ov para que a secao na altura da face continue sendo
    exatamente o contorno de projeto."""
    from math import tan, radians
    base = poly.buffer(tan(radians(saida)) * ov, join_style=1)
    if base.is_empty or base.geom_type != 'Polygon': base = poly
    return prisma(base, rel + ov, saida)

def prisma_wire(w, h, saida=0.0):
    """extrusao de um contorno ANALITICO (retas e arcos), sem furo."""
    return cq.Solid.extrudeLinear(w, [], cq.Vector(0, 0, h), saida)

def gota_wire(rb, off, rn, yn):
    """Contorno da gota como B-rep de verdade: dois arcos e as duas tangentes
    externas. Em poligono de 180 lados o OCC recusava abaular a aresta — e o
    STEP saia com 180 faces planas onde deveria ter dois cilindros."""
    A = (0.0, -off); B = (0.0, yn)
    d = B[1] - A[1]
    b = -(rb - rn) / d
    c = rb - b * A[1]
    a = (1.0 - b*b) ** 0.5
    P  = (A[0] - rb*a,  A[1] - rb*b)          # tangencia no bulbo, lado -x
    Q  = (B[0] - rn*a,  B[1] - rn*b)          # tangencia no nariz, lado -x
    Pl = (-P[0], P[1]); Ql = (-Q[0], Q[1])    # espelho, lado +x
    return (cq.Workplane("XY").moveTo(*P)
            .threePointArc((A[0], A[1] - rb), Pl)     # volta do bulbo
            .lineTo(*Ql)                              # tangente do lado +x
            .threePointArc((B[0], B[1] + rn), Q)      # ponta do nariz
            .close().val())

def estadio_wire(y0, y1, meia):
    """Estadio ANALITICO: duas retas e dois arcos exatos. Feito com buffer de
    LineString, cada meia-cana virava 8+ segmentos de 0,14 mm; a extrusao com
    saida recua 0,115 mm ao longo da fenda e engole esses segmentos, deixando
    aresta de micra. Com arco de verdade isso nao acontece."""
    return (cq.Workplane("XY").moveTo(-meia, y0)
            .lineTo(-meia, y1).threePointArc((0.0, y1 + meia), (meia, y1))
            .lineTo(meia, y0).threePointArc((0.0, y0 - meia), (-meia, y0))
            .close().val())

def ret_wire(r0, r1, meia, rc):
    """Retangulo de cantos arredondados, analitico: 4 retas e 4 arcos."""
    x, y0, y1 = meia - rc, r0 + rc, r1 - rc
    w = (cq.Workplane("XY").moveTo(-meia, y0)
         .lineTo(-meia, y1).threePointArc((-x + rc*0.29289 - rc*1.0 + rc, y1 + rc), (-x, r1))
         )
    # mais simples e seguro: monta por segmentos explicitos
    import math
    P = []
    def arco(cx, cy, a0, a1):
        am = (a0 + a1) / 2
        return ((cx + rc*math.cos(math.radians(am)), cy + rc*math.sin(math.radians(am))),
                (cx + rc*math.cos(math.radians(a1)), cy + rc*math.sin(math.radians(a1))))
    wp = cq.Workplane("XY").moveTo(-meia, y0)
    wp = wp.lineTo(-meia, y1)
    m, e = arco(-x, y1, 180, 90); wp = wp.threePointArc(m, e)
    wp = wp.lineTo(x, r1)
    m, e = arco(x, y1, 90, 0);    wp = wp.threePointArc(m, e)
    wp = wp.lineTo(meia, y0)
    m, e = arco(x, y0, 0, -90);   wp = wp.threePointArc(m, e)
    wp = wp.lineTo(-x, r0)
    m, e = arco(-x, y0, -90, -180); wp = wp.threePointArc(m, e)
    return wp.close().val()

def place(shape, phi, R, top, depth):
    """local x=tangencial, y=radial, z=altura. Determinante +1."""
    c, s = cos(phi), sin(phi)
    et = (-s, 0.0, c); er = (c, 0.0, s); ey = (0.0, 1.0, 0.0)
    t = gp_Trsf(); t.SetValues(et[0], er[0], ey[0], R*er[0],
                               et[1], er[1], ey[1], top - depth,
                               et[2], er[2], ey[2], R*er[2])
    return shape.moved(cq.Location(t))

def deitado(poly, h, y0, saida=0.0, ov=0.0):
    """poligono no plano XZ, crescendo em +Y a partir de y0. ov mergulha o
    solido ov mm abaixo de y0 (ver mergulha)."""
    p = affinity.scale(poly, xfact=1.0, yfact=-1.0, origin=(0, 0))
    t = gp_Trsf(); t.SetValues(1, 0, 0, 0,  0, 0, 1, y0 - ov,  0, -1, 0, 0)
    corpo = mergulha(p, h, saida, ov) if ov > 0 else prisma(p, h, saida)
    return corpo.moved(cq.Location(t))

def rev(prof):
    """perfil fechado [(r,y)] revolvido em Y. A saida ja vem embutida no perfil."""
    lim = []
    for p in prof:
        if not lim or abs(p[0]-lim[-1][0]) > 1e-9 or abs(p[1]-lim[-1][1]) > 1e-9: lim.append(p)
    return (cq.Workplane("XY").polyline([(float(r), float(y)) for r, y in lim])
              .close().revolve(360, (0, 0, 0), (0, 1, 0)).val())

def cil(r, y0, y1, cx=0.0, cz=0.0):
    return cq.Solid.makeCylinder(r, y1-y0, cq.Vector(cx, y0, cz), cq.Vector(0, 1, 0))

def cone(r0, r1, y0, y1, cx=0.0, cz=0.0):
    return cq.Solid.makeCone(r0, r1, y1-y0, cq.Vector(cx, y0, cz), cq.Vector(0, 1, 0))

def esfera(r, cx, cy, cz):
    return cq.Solid.makeSphere(r, cq.Vector(cx, cy, cz), angleDegrees1=-90, angleDegrees2=90)

def fundir(ss):
    """Uniao. Encadear fuse dois a dois estoura quando os solidos sao disjuntos
    (31 numerais soltos devolveram TopoDS nulo); um booleano so com todos os
    argumentos o OCC aguenta. Se ainda assim recusar, devolve composto — que e
    o certo para peca que so vai se fundir ao corpo no CAD da ferramentaria."""
    if len(ss) == 1: return ss[0]
    try:
        o = ss[0].fuse(*ss[1:])
        if BRepCheck_Analyzer(o.wrapped).IsValid(): return o.clean()
    except Exception:
        pass
    # achatar em solidos: composto montado com os objetos crus sai reprovado
    # no BRepCheck mesmo com todos os solidos validos
    return cq.Compound.makeCompound([x for s in ss for x in s.Solids()])

def tirar(a, ss):
    for s in ss: a = a.cut(s)
    return a.clean()

# ---------------------------------------------------------------- letras
def letras(itens, R, base, cap=None, xs=1.0, rel=None, saida=None, ov=0.10):
    """texto em AUTO RELEVO sobre uma face horizontal, com saida e canto abaulado.
    itens: [(phi_rad, texto)] · base: Y da face · rel: altura do relevo"""
    rel   = P.LETRA_REL   if rel   is None else rel
    saida = P.LETRA_SAIDA if saida is None else saida
    out = []
    for phi, txt in itens:
        for sp in glifos(txt, cap, xs):
            out.append(place(mergulha(sp, rel, saida, ov), phi, R, base + rel, rel + ov))
    return out

# (ov, saida) tentados em ordem quando o booleano do relevo recusa. O OCC
# reprova certos pares contorno/angulo sem motivo geometrico visivel — o "3" do
# mes recusava com 0,10/15 graus e passava com 0,08/15 ou 0,10/12. A diferenca
# fica em micra e nao muda nada de funcional; ficar com canto vivo, sim.
VARIANTES = [(0.10, None), (0.08, None), (0.12, None), (0.10, 12.0), (0.08, 12.0),
             (0.10, 18.0), (0.06, 10.0), (0.12, 12.0)]

def aplica_letras(corpo, itens, R, base, cap=None, xs=1.0, rel=None, nome=''):
    """Funde o texto em auto relevo NO corpo, tentando variantes ate o OCC aceitar."""
    rel = P.LETRA_REL if rel is None else rel
    usados, falhas = {}, []
    for phi, txt in itens:
        for k, sp in enumerate(glifos(txt, cap, xs)):
            for ov, sa in VARIANTES:
                sa = P.LETRA_SAIDA if sa is None else sa
                try:
                    o = corpo.fuse(place(mergulha(sp, rel, sa, ov), phi, R, base + rel, rel + ov))
                    if not BRepCheck_Analyzer(o.wrapped).IsValid(): continue
                    corpo = o; usados[(ov, sa)] = usados.get((ov, sa), 0) + 1
                    break
                except Exception:
                    continue
            else:
                falhas.append('%s[%d]' % (txt, k))
    print('      %-26s %s%s' % (nome,
          '  '.join('%d× ov %.2f/%.0f°' % (n, ov, sa) for (ov, sa), n in sorted(usados.items())),
          '   *** NAO ENTRARAM: %s ***' % ', '.join(falhas) if falhas else ''))
    return corpo

def angulos_dias(R=None, cap=None):
    """Espacamento por BORDA, nao por centro: o vao entre numeros vizinhos fica
    igual nos 31. Com passo constante, 1..9 (um digito) abrem um vao quase o
    dobro do de 10..31 — era o 'espaco do zero' que sobrou."""
    R = P.DIA_R if R is None else R
    arco = [degrees(largura(str(d), cap=cap) / R) for d in range(1, 32)]
    folga = (360.0 - sum(arco)) / 31
    ang, acc = [], 0.0
    for a in arco:
        ang.append(acc + a/2); acc += a + folga
    off = 90.0 - ang[0]
    return [a + off for a in ang], arco, folga

# ---------------------------------------------------------------- arestas
def arred(s, r, filtro=None, nome=''):
    """Abaula arestas. Se o OCC recusar o conjunto, tenta raios menores e, por
    fim, desiste avisando — melhor canto vivo declarado do que peca errada."""
    es = [e for e in s.Edges() if (filtro is None or filtro(e))]
    if not es:
        print('      %-26s nenhuma aresta no filtro' % nome); return s
    for raio in (r, r*0.6, r*0.35):
        try:
            o = s.fillet(raio, es)
            if BRepCheck_Analyzer(o.wrapped).IsValid():
                print('      %-26s %3d arestas  R %.2f' % (nome, len(es), raio)); return o
        except Exception:
            pass
    print('      %-26s %3d arestas  *** OCC RECUSOU, ficaram vivas ***' % (nome, len(es)))
    return s

def valido(s):
    return BRepCheck_Analyzer(s.wrapped).IsValid()
