# -*- coding: utf-8 -*-
"""Confere a v3 e gera os STL: monta a valvula pela receita, mede saida face a
face, interferencia entre pecas, ajustes e orcamento de altura."""
import sys, os, math, numpy as np, trimesh, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'medicao_v2'))
import params as P
from tess import tessela, _malha as tessela_bruto
def tessela_solido(s): return tessela_bruto(s.wrapped)
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus

AQUI = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(AQUI, 'step'); STL = os.path.join(AQUI, 'stl'); os.makedirs(STL, exist_ok=True)
VALV = '/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/5882c071-Mont_pote_com_valvula__prova_valvula1.STL'
TAMPA = '/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/1c50a47b-Mont_pote_com_valvula__Tampa_Pote_025_Pequeno_Cav1.STL'
B = lambda op, m: trimesh.boolean.boolean_manifold(m, operation=op)
TIPO = {GeomAbs_Plane:'plano', GeomAbs_Cylinder:'cilindro', GeomAbs_Cone:'cone',
        GeomAbs_Sphere:'esfera', GeomAbs_Torus:'toro'}

print('== 1. monta a valvula pela receita dos 4 arquivos')
valv = trimesh.load(VALV)
corte = trimesh.creation.box(extents=[60, 8, 60]); corte.apply_translation([P.CX, P.FACE+4, P.CZ])
base = B('difference', [valv, corte])
a = tessela(f'{STEP}/Chrono_v3_M01_1_SOMAR_enchimento_mesa_dias.step')
b = tessela(f'{STEP}/Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes.step')
c = tessela(f'{STEP}/Chrono_v3_M01_3_SOMAR_poste.step')
d = tessela(f'{STEP}/Chrono_v3_M01_4_SUBTRAIR_furo_passante.step')
m01 = B('difference', [B('union', [B('difference', [B('union', [base, a]), b]), c]), d])
m02 = tessela(f'{STEP}/Chrono_v3_M02_Rodinha_Meses.step')
m03 = tessela(f'{STEP}/Chrono_v3_M03_Ponteira.step')
for n, m in [('Chrono_v3_M01_Valvula_Dias', m01), ('Chrono_v3_M02_Rodinha_Meses', m02),
             ('Chrono_v3_M03_Ponteira', m03)]:
    m.export(f'{STL}/{n}.stl')
    print('   %-30s %6d faces  vol %8.2f  massa %.3f g  solido %s'
          % (n, len(m.faces), m.volume, m.volume*0.905/1000, m.is_volume))
print('   massa do conjunto: %.3f g   (v2: 2,908 g · valvula original 2,044 g)'
      % ((m01.volume+m02.volume+m03.volume)*0.905/1000))

print('\n== 2. interferencia entre as pecas (mm3)')
import itertools
pec = {'M01': m01, 'M02': m02, 'M03': m03}
for x, y in itertools.combinations(pec, 2):
    r = B('intersection', [pec[x], pec[y]])
    print('   %s x %s : %.4f' % (x, y, r.volume if len(r.faces) else 0.0))

print('\n== 3. orcamento de altura')
tampa = trimesh.load(TAMPA)
conj = trimesh.util.concatenate([m01, m02, m03])
print('   topo do conjunto      Y %.3f' % conj.bounds[1][1])
print('   ponto mais alto da tampa Y %.3f' % tampa.bounds[1][1])
print('   diferenca             %+.3f mm' % (conj.bounds[1][1]-tampa.bounds[1][1]))

print('\n== 4. folga minima entre as pecas em servico')
import trimesh.proximity as _px
for x, y in [('M01','M02'), ('M01','M03'), ('M02','M03')]:
    p = pec[y].sample(12000)
    d = _px.closest_point(pec[x], p)[1]
    q = p[d.argmin()]
    print('   %s -> %s : folga minima %.4f mm  em r %.2f  Y %.2f'
          % (y, x, d.min(), ((q[0]-P.CX)**2 + (q[2]-P.CZ)**2) ** 0.5, q[1]))

print('\n== 5. saida: rode saida_v3.py — a conta honesta e na peca montada,\n   nao em cada arquivo de operacao (o furo do poste aparece como parede\n   vertical no M01c e some quando o M01d e cortado)')

print('\n== 6. ajustes')
print('   poste no topo O%.3f  x  furo da rodinha embaixo O%.3f  -> folga radial %.3f'
      % (2*(P.POST_R-P.rec(P.POST_TOP-(P.FACE-P.REB_H))), 2*P.ARO_RI, P.ARO_RI-(P.POST_R-P.rec(1.62))))
print('   pino O%.2f x furo no ponto mais estreito O%.2f -> folga radial %.3f'
      % (2*P.PINO_RE, 2*P.FURO_R, P.FURO_R-P.PINO_RE))
print('   farpa O%.2f sobre furo embaixo O%.2f -> encaixe %.2f mm' % (2*P.FARPA_R, 2*P.FURO_R, P.FARPA_R-P.FURO_R))
print('   detente: base O%.2f  altura %.2f  raio da esfera %.4f  em r %.2f' % (P.DET_BASE, P.DET_ALT, P.DET_ESF, P.DET_R))
