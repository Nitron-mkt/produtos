# -*- coding: utf-8 -*-
"""Malhas finas para o visor de inspecao (flecha 0,008 mm contra os 0,020 do
visor de apresentacao: a 0,020 a calota de O2,00 do detente sai facetada).

M01 e montada sobre uma CHAPA LISA que faz as vezes da valvula. O STL da valvula
original nao esta no repositorio (so derivados) e o container foi recriado. Nao
faz falta para inspecao: o que esta em revisao sao os acrescimos do Chrono, e a
chapa mostra todos eles — mesa, 31 numerais, rebaixo, as 2 molas, poste e furo.
"""
import sys, os, numpy as np, trimesh, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P
from tess import _malha
from lib_v3 import cone
from OCP.BRepCheck import BRepCheck_Analyzer

LIN, ANG = 0.008, 0.18
AQUI = os.path.dirname(os.path.abspath(__file__))
STEP, SAI = os.path.join(AQUI, 'step'), os.path.join(AQUI, 'stl_detalhe')
os.makedirs(SAI, exist_ok=True)
L = lambda n: cq.importers.importStep('%s/%s.step' % (STEP, n)).val()

chapa = cone(19.0, 19.0 - P.rec(P.FACE - P.CHAPA_Y0), P.CHAPA_Y0, P.FACE
             ).moved(cq.Location(cq.Vector(P.CX, 0, P.CZ)))
r = chapa.fuse(L('Chrono_v3_M01_1_SOMAR_enchimento_mesa_dias'))
r = r.cut(L('Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes'))
r = r.fuse(L('Chrono_v3_M01_3_SOMAR_poste'))
r = r.cut(L('Chrono_v3_M01_4_SUBTRAIR_furo_passante'))
assert BRepCheck_Analyzer(r.wrapped).IsValid(), 'M01 montada saiu invalida'

pecas = {'M01': _malha(r.Solids()[0].wrapped, LIN, ANG)}
for k, n in [('M02', 'Chrono_v3_M02_Rodinha_Meses'), ('M03', 'Chrono_v3_M03_Ponteira')]:
    pecas[k] = _malha(L(n).Solids()[0].wrapped, LIN, ANG)
# O modo "conjunto" usa a MESMA M01 sobre chapa. O STL da valvula completa que
# estava aqui e de antes desta revisao — mostra-lo junto com a rodinha e a
# ponteira novas seria misturar duas versoes.
pecas['M01c'] = pecas['M01']

for k, m in pecas.items():
    m.export('%s/%s.stl' % (SAI, k))
    print('%-5s %7d faces %6d vert  %s  fechado=%s  vol %8.2f'
          % (k, len(m.faces), len(m.vertices),
             'u16 serve' if len(m.vertices) <= 65536 else '*** precisa u32 ***',
             m.is_volume, m.volume))
