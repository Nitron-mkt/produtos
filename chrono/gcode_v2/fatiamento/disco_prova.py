"""Disco de prova para o teste em escala: so o mostrador de M01 (tudo acima da
face, Y 37,23) sobre uma base chapada de 1,20 mm. Imprime deitado, sem suporte,
e serve para provar leitura + giro do aro + a seta. Nao serve para provar
assentamento no poco da tampa — para isso e a M01 inteira, 1:1."""
import sys, trimesh
sys.path.insert(0,'/home/user/produtos/chrono/medicao_v2')
from lib3d import revolve, cyl, boolean
FACE=37.23; BASE_H=1.20; BASE_R=19.04
m=trimesh.load('/home/user/produtos/chrono/stl_v2/Chrono_M01_Valvula_Dias.stl')
c=(m.bounds[0]+m.bounds[1])/2
m.apply_translation([-c[0],0,-c[2]])
corte=trimesh.creation.box(extents=[60,8,60]); corte.apply_translation([0,FACE-4,0])
topo=boolean('difference',[m,corte])                      # so o que esta acima da face
# anel + nucleo: revolve ate o eixo gera faces degeneradas
casca=revolve([(BASE_R,FACE-BASE_H),(BASE_R,FACE-0.30),(BASE_R-0.30,FACE),
               (3.00,FACE),(3.00,FACE-BASE_H)])
base=boolean('union',[casca, cyl(3.10, FACE-BASE_H, FACE, n=96)])
d=boolean('union',[topo,base])
d.apply_translation([c[0],0,c[2]])
b=d.bounds
print('disco de prova: O%.2f  altura %.2f (%.2f..%.2f)  fechada=%s'
      %(b[1][0]-b[0][0], b[1][1]-b[0][1], b[0][1], b[1][1], d.is_watertight))
d.export('/home/user/produtos/chrono/stl_v2/Chrono_M01_Disco_Prova.stl')
