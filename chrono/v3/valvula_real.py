# -*- coding: utf-8 -*-
"""Recupera a VALVULA REAL do STL antigo e monta a M01 v4 inteira sobre ela.

O STL `Mont_pote_com_valvula__prova_valvula1.STL` sumiu com o container. Mas o
`stl/Chrono_v3_M01_Valvula_Dias.stl` tem a valvula injetada DENTRO dele, somada
ao Chrono v3 — e tudo o que o Chrono v3 acrescentou vive ACIMA da face de topo
(Y 37,23), ou coincide com material que a valvula ja tem:

  mesa      36,63..37,41 em r 14,20..18,75 — abaixo de 37,23 ela e a propria
            valvula (a face foi medida plana em 37,230 nessa faixa)
  numerais  assentavam em 37,41 — acima do corte
  poste     sobe ate 38,25; abaixo de 36,63 e cilindro dentro da chapa
  rebaixo   v3 cortava r<=13,60 a partir de 36,63; o v4 corta a partir de 36,53,
            pelo MESMO cone — o corte novo contem o velho
  furo      identico nas duas versoes
  molas     a calota v3 fica dentro do corte do rebaixo v4, que a refaz

Conferido que o STL antigo NAO tem o bug das duas bolhas penduradas: abaixo de
Y 35,35, em r 7,5..12,5, so existe material entre 60 e 120 graus (a concha das
12 h), e nada em 0 e 180 graus, que e onde as bolhas estariam.

Logo:  valvula = STL antigo cortado em Y <= 37,23
e a M01 inteira = (((valvula + SOMAR_1) - SUBTRAIR_2) + SOMAR_3) - SUBTRAIR_4,
a mesma receita dos quatro arquivos, so que aplicada em malha.
"""
import sys, os, numpy as np, trimesh, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P
from tess import _malha

AQUI = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(AQUI, 'step')
VELHO = os.path.join(AQUI, 'stl', 'Chrono_v3_M01_Valvula_Dias.stl')
LIN, ANG = 0.010, 0.20
B = lambda op, ms: trimesh.boolean.boolean_manifold(ms, operation=op)

def _g(n):
    sh = cq.importers.importStep('%s/%s.step' % (STEP, n)).val()
    return _malha(sh.Solids()[0].wrapped, LIN, ANG)

def valvula():
    """A valvula injetada sozinha: o STL antigo cortado na face de topo."""
    m = trimesh.load(VELHO)
    v = m.slice_plane([0, P.FACE, 0], [0, -1, 0], cap=True)
    v.remove_unreferenced_vertices(); v.merge_vertices()
    return v

def m01_inteira(val=None):
    val = valvula() if val is None else val
    r = B('union',       [val, _g('Chrono_v3_M01_1_SOMAR_enchimento_e_dias')])
    r = B('difference',  [r,   _g('Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes')])
    r = B('union',       [r,   _g('Chrono_v3_M01_3_SOMAR_poste')])
    r = B('difference',  [r,   _g('Chrono_v3_M01_4_SUBTRAIR_furo_passante')])
    return r

if __name__ == '__main__':
    SAI = os.path.join(AQUI, 'stl'); os.makedirs(SAI, exist_ok=True)
    val = valvula()
    print('valvula recuperada : %6d faces  fechada=%-5s vol %8.2f  Y %6.3f..%6.3f  r max %.2f'
          % (len(val.faces), val.is_volume, val.volume, val.bounds[0][1], val.bounds[1][1],
             np.hypot(val.vertices[:,0]-P.CX, val.vertices[:,2]-P.CZ).max()))
    val.export('%s/Chrono_v4_M00_Valvula_recuperada.stl' % SAI)
    m = m01_inteira(val)
    print('M01 inteira        : %6d faces  fechada=%-5s vol %8.2f  Y %6.3f..%6.3f'
          % (len(m.faces), m.is_volume, m.volume, m.bounds[0][1], m.bounds[1][1]))
    m.export('%s/Chrono_v4_M01_COM_VALVULA.stl' % SAI)
    # o conjunto montado, as tres pecas na posicao de servico
    pecas = [m] + [_g(n) for n in ('Chrono_v3_M02_Rodinha_Meses', 'Chrono_v3_M03_Ponteira')]
    conj = trimesh.util.concatenate(pecas)
    conj.export('%s/Chrono_v4_CONJUNTO_COM_VALVULA.stl' % SAI)
    print('conjunto montado   : %6d faces  Y %6.3f..%6.3f'
          % (len(conj.faces), conj.bounds[0][1], conj.bounds[1][1]))
