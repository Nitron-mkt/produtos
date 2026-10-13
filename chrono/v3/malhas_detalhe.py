# -*- coding: utf-8 -*-
"""Malhas finas para o visor de inspecao (flecha 0,008 mm contra os 0,020 do
visor de apresentacao: a 0,020 a calota de O2,00 do detente sai facetada).

A M01 e montada sobre a VALVULA REAL, recuperada do STL antigo — ver
valvula_real.py para como e por que isso e exato.
"""
import sys, os, numpy as np, trimesh, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P
from tess import _malha
from lib_v3 import cone
from valvula_real import valvula, m01_inteira
from OCP.BRepCheck import BRepCheck_Analyzer

LIN, ANG = 0.008, 0.18
AQUI = os.path.dirname(os.path.abspath(__file__))
STEP, SAI = os.path.join(AQUI, 'step'), os.path.join(AQUI, 'stl_detalhe')
os.makedirs(SAI, exist_ok=True)
L = lambda n: cq.importers.importStep('%s/%s.step' % (STEP, n)).val()

# A M01 agora e montada sobre a VALVULA REAL, recuperada do STL antigo (ver
# valvula_real.py). O indice do visor e u16, entao a peca inteira nao pode
# passar de 65.536 vertices — a valvula sozinha ja traz 46.848 triangulos.
r = m01_inteira()

pecas = {'M01': r}
for k, n in [('M02', 'Chrono_v3_M02_Rodinha_Meses'), ('M03', 'Chrono_v3_M03_Ponteira')]:
    pecas[k] = _malha(L(n).Solids()[0].wrapped, LIN, ANG)
pecas['M01c'] = pecas['M01']   # o modo conjunto usa a mesma peca

for k, m in pecas.items():
    m.export('%s/%s.stl' % (SAI, k))
    print('%-5s %7d faces %6d vert  %s  fechado=%s  vol %8.2f'
          % (k, len(m.faces), len(m.vertices),
             'u16 serve' if len(m.vertices) <= 65536 else '*** precisa u32 ***',
             m.is_volume, m.volume))
