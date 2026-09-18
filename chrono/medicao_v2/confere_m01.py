# -*- coding: utf-8 -*-
"""Prova que a receita dos 3 STEP reproduz exatamente o M01 validado:
  valvula_final = ((valvula_original - rebaixo) + acrescimo) - furo"""
import numpy as np, trimesh
from confere_step import tessela, dist
S='/home/user/produtos/chrono/step_v2'
VALV='/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/5882c071-Mont_pote_com_valvula__prova_valvula1.STL'
FACE=37.23
B=lambda op,m: trimesh.boolean.boolean_manifold(m, operation=op)

valv=trimesh.load(VALV)
corte=trimesh.creation.box(extents=[60,8,60]); corte.apply_translation([61.97,FACE+4,102.68])
base=B('difference',[valv,corte])
reb =tessela(f'{S}/Chrono_M01a_SUBTRAIR_1_rebaixo.step')
add =tessela(f'{S}/Chrono_M01b_SOMAR_2_poste_mesa_dias_detentes.step')
furo=tessela(f'{S}/Chrono_M01c_SUBTRAIR_3_furo_passante.step')
r=B('difference',[B('union',[B('difference',[base,reb]),add]),furo])
alvo=trimesh.load('/home/user/produtos/chrono/stl_v2/Chrono_M01_Valvula_Dias.stl')
d1=dist(alvo,r); d2=dist(r,alvo)
print('receita dos 3 STEP  x  Chrono_M01_Valvula_Dias.stl')
print('   volume  receita %8.2f   alvo %8.2f   dif %+.3f%%'%(r.volume,alvo.volume,100*(r.volume-alvo.volume)/alvo.volume))
print('   caixa   receita %s'%np.round(r.bounds[1]-r.bounds[0],3))
print('           alvo    %s'%np.round(alvo.bounds[1]-alvo.bounds[0],3))
print('   desvio  alvo->receita  med %.4f  max %.4f mm'%(d1.mean(),d1.max()))
print('           receita->alvo  med %.4f  max %.4f mm'%(d2.mean(),d2.max()))
