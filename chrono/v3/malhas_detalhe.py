# -*- coding: utf-8 -*-
"""Malhas finas para o visor de inspecao (flecha 0,008 mm contra os 0,020 do
visor de apresentacao: a 0,020 a calota de O2,00 do detente sai facetada).

O visor mostra EXATAMENTE o que vai nos STEP entregues — inclusive a M01, que
agora e lida de step_completo. Antes ele mostrava a valvula recuperada do STL
e o arquivo mostrava outra coisa; essa diferenca foi fonte de confusao.
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

COMPL = os.path.join(AQUI, 'step_completo')
C = lambda n: cq.importers.importStep('%s/%s.step' % (COMPL, n)).val().Solids()[0]
pecas = {k: _malha(C(n).wrapped, LIN, ANG) for k, n in
         [('M01', 'Chrono_M01_Valvula_Dias'),
          ('M02', 'Chrono_M02_Rodinha_Meses'),
          ('M03', 'Chrono_M03_Ponteira')]}
pecas['M01c'] = pecas['M01']   # o modo conjunto usa a mesma peca

for k, m in pecas.items():
    m.export('%s/%s.stl' % (SAI, k))
    print('%-5s %7d faces %6d vert  %s  fechado=%s  vol %8.2f'
          % (k, len(m.faces), len(m.vertices),
             'u16 serve' if len(m.vertices) <= 65536 else '*** precisa u32 ***',
             m.is_volume, m.volume))
