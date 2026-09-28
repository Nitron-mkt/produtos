# -*- coding: utf-8 -*-
"""Saida medida na PECA PRONTA, triangulo a triangulo, ponderada por area.

Auditar cada arquivo de operacao em separado engana: o furo do poste aparece
como parede vertical no M01c e desaparece quando o M01d e cortado; a parede do
enchimento aparece no M01a e some dentro da valvula. So a peca montada conta.
"""
import sys, os, numpy as np, trimesh
A = os.path.dirname(os.path.abspath(__file__))
LIM = np.sin(np.radians(0.5))

def mede(arq):
    m = trimesh.load(arq)
    n = m.face_normals; ar = m.area_faces
    vert = np.abs(n[:, 1]) < LIM
    # angulo de saida de cada triangulo (0 = parede vertical)
    ang = np.degrees(np.arcsin(np.clip(np.abs(n[:, 1]), 0, 1)))
    lat = ang < 60                       # so as paredes, fora topo e fundo
    return (100*ar[vert].sum()/ar.sum(), ar[vert].sum(),
            np.average(ang[lat], weights=ar[lat]) if lat.any() else float('nan'))

print('%-34s %10s %10s  %s' % ('', 'vertical', 'mm2', 'saida media das paredes'))
for nome, v2, v3 in [
    ('M01 valvula + dias', '../stl_v2/Chrono_M01_Valvula_Dias.stl', 'stl/Chrono_v3_M01_Valvula_Dias.stl'),
    ('M02 rodinha dos meses', '../stl_v2/Chrono_M02_Rodinha_Meses.stl', 'stl/Chrono_v3_M02_Rodinha_Meses.stl'),
    ('M03 ponteira', '../stl_v2/Chrono_M03_Ponteira.stl', 'stl/Chrono_v3_M03_Ponteira.stl')]:
    a = mede(os.path.join(A, v2)); b = mede(os.path.join(A, v3))
    print('%-34s' % nome)
    print('   v2  %26.1f%% %9.1f   %.2f graus' % a)
    print('   v3  %26.1f%% %9.1f   %.2f graus' % b)
