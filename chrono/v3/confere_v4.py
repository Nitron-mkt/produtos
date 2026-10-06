# -*- coding: utf-8 -*-
"""Confere a revisao sem depender do STL da valvula (que saiu da sessao): a M01
e montada sobre a chapa lisa. Tudo o que importa aqui — interferencia, folga,
orcamento de altura e a janela contra o numeral — vive acima da face da valvula.
"""
import sys, os, itertools, numpy as np, trimesh, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P, lib_v3 as L
from tess import _malha
from OCP.BRepCheck import BRepCheck_Analyzer
STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step')
SAI  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stl'); os.makedirs(SAI, exist_ok=True)
G = lambda n: cq.importers.importStep('%s/%s.step' % (STEP, n)).val()

chapa = L.cone(19.0, 19.0 - P.rec(P.FACE - P.CHAPA_Y0), P.CHAPA_Y0, P.FACE
               ).moved(cq.Location(cq.Vector(P.CX, 0, P.CZ)))
m01b = chapa.fuse(G('Chrono_v3_M01_1_SOMAR_enchimento_mesa_dias')) \
            .cut(G('Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes')) \
            .fuse(G('Chrono_v3_M01_3_SOMAR_poste')) \
            .cut(G('Chrono_v3_M01_4_SUBTRAIR_furo_passante'))
assert BRepCheck_Analyzer(m01b.wrapped).IsValid(), 'M01 sobre chapa saiu invalida'
pec = {'M01': _malha(m01b.Solids()[0].wrapped, 0.012, 0.20),
       'M02': _malha(G('Chrono_v3_M02_Rodinha_Meses').Solids()[0].wrapped, 0.012, 0.20),
       'M03': _malha(G('Chrono_v3_M03_Ponteira').Solids()[0].wrapped, 0.012, 0.20)}
print('== 1. pecas')
for k, m in pec.items():
    m.export('%s/Chrono_v4_%s.stl' % (SAI, k))
    print('   %-4s %7d faces  fechado=%s  vol %8.2f  massa %.3f g'
          % (k, len(m.faces), m.is_volume, m.volume, m.volume*0.905/1000))

print('\n== 2. interferencia (mm3)')
B = lambda op, m: trimesh.boolean.boolean_manifold(m, operation=op)
for a, b in itertools.combinations(pec, 2):
    r = B('intersection', [pec[a], pec[b]])
    print('   %s x %s : %.4f' % (a, b, r.volume if len(r.faces) else 0.0))

print('\n== 3. folga minima em servico')
import trimesh.proximity as px
for a, b in [('M01','M02'), ('M01','M03'), ('M02','M03')]:
    p = pec[b].sample(14000); d = px.closest_point(pec[a], p)[1]; q = p[d.argmin()]
    print('   %s -> %s : %.4f mm  em r %.2f  Y %.2f'
          % (b, a, d.min(), ((q[0]-P.CX)**2 + (q[2]-P.CZ)**2) ** 0.5, q[1]))

print('\n== 4. altura')
conj = trimesh.util.concatenate(list(pec.values()))
print('   topo do conjunto Y %.3f   (ponto mais alto da tampa: 39,762 -> %+.3f mm)'
      % (conj.bounds[1][1], conj.bounds[1][1] - 39.762))

print('\n== 5. a janela contra o numeral do mes')
from shapely.geometry import Polygon as SP
import math
t = np.linspace(0, 2*math.pi, 1440, endpoint=False)
gota = SP([(P.BULBO_R*math.cos(a), -P.BULBO_OFF+P.BULBO_R*math.sin(a)) for a in t]).union(
       SP([(P.NARIZ_R*math.cos(a),  P.NARIZ_Y+P.NARIZ_R*math.sin(a)) for a in t])).convex_hull
jan = SP([(-P.JAN_M+P.JAN_RC, P.JAN_R0+P.JAN_RC), (P.JAN_M-P.JAN_RC, P.JAN_R0+P.JAN_RC),
          (P.JAN_M-P.JAN_RC, P.JAN_R1-P.JAN_RC), (-P.JAN_M+P.JAN_RC, P.JAN_R1-P.JAN_RC)]
         ).buffer(P.JAN_RC, join_style=1)
print('   janela r %.2f..%.2f  meia-largura %.2f  canto R%.2f' % (P.JAN_R0, P.JAN_R1, P.JAN_M, P.JAN_RC))
print('   borda ate o contorno da gota: %.2f mm' % gota.exterior.distance(jan))
pior = 99; qual = None
for m in range(1, 13):
    for sp in L.glifos(str(m), cap=P.MES_CAP):
        b = sp.bounds
        folga = min(b[0]-(-P.JAN_M), P.JAN_M-b[2], (b[1]+P.MES_R)-P.JAN_R0, P.JAN_R1-(b[3]+P.MES_R))
        if folga < pior: pior, qual = folga, m
print('   folga do numeral dentro da janela: %.2f mm (pior: mes %d, cap %.2f)' % (pior, qual, P.MES_CAP))
mes = L.glifos('MÊS'); bm = [p.bounds for p in mes]
print('   MES ocupa r %.2f..%.2f -> %.2f mm da janela e %.2f do icone'
      % (P.MES_TXT_R+min(x[1] for x in bm), P.MES_TXT_R+max(x[3] for x in bm),
         P.JAN_R0-(P.MES_TXT_R+max(x[3] for x in bm)),
         (P.MES_TXT_R+min(x[1] for x in bm)) - 3.90))
