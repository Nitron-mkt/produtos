import sys, numpy as np, trimesh
sys.path.insert(0,'/tmp/claude-0/-home-user-produtos/25a64868-b28d-5a69-b1c3-502a4891561f/scratchpad/chrono')
from lib3d import *
from math import pi, radians, cos, sin

OUT='/home/user/produtos/chrono/stl'
import os; os.makedirs(OUT, exist_ok=True)
VALV='/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/5882c071-Mont_pote_com_valvula__prova_valvula1.STL'

def toC(m):            # leva do eixo (0,0) para o centro do poco
    n=m.copy(); n.apply_translation([CX,0,CZ]); return n

# ---------------------------------------------------------------- detentes
def bump(r,phi):       # mola no pino: calota h=0.15, base 0.30
    R=(0.30**2+0.15**2)/(2*0.15)
    return ball(R, r*cos(phi), TOPV+0.15-R, r*sin(phi))
def dimple(r,phi):     # encaixe no anel: calota h=0.25, base 0.35
    R=(0.35**2+0.25**2)/(2*0.25)
    return ball(R, r*cos(phi), BOTR+R-0.25, r*sin(phi))

# ================================================================ 1 · PINO
valv=trimesh.load(VALV)
valv.apply_translation([-CX,0,-CZ])

cubo=revolve([(5.80,37.13),(5.80,37.38),(5.30,37.58),(5.30,37.82),(5.80,38.02),
              (5.80,38.14),(5.60,38.20),(4.60,38.20),(4.60,37.13)])
colar=revolve([(14.20,37.13),(14.20,37.38),(13.70,37.58),(13.70,37.82),(14.20,38.02),
               (14.20,38.14),(14.00,38.20),(12.20,38.20),(12.20,37.13)])
# molas: o par tem de estar afastado de um multiplo do passo do anel.
# dia  -> 15 passos de 11,613 graus; mes -> 6 passos de 30 graus.
SD_=360.0/31
molas=[bump(15.2,radians(90-7*SD_)), bump(15.2,radians(90-22*SD_)),
       bump(7.0,radians(90)),        bump(7.0,radians(90-6*30))]

# a aba de dedo da valvula, a 6 h, sobe ate Y 38,24 e ocupa o espaco dos aneis.
# o pino trunca a casca em Y 37,23 (a interface do assento fica toda abaixo disso).
corte=trimesh.creation.box(extents=[60,6,60]);
corte.apply_translation([0,TOPV+3,0])
casca=boolean('difference',[valv,corte])
pino=boolean('union',[casca,cubo,colar]+molas)

# marcas de leitura gravadas no colar, a 12 h (+Z)
from shapely.geometry import Polygon as SP
tri_out=SP([(-0.50,0.05),(0.50,0.05),(0.0,0.85)])
tri_in =SP([(-0.50,-0.05),(0.50,-0.05),(0.0,-0.85)])
marcas=[place(trimesh.creation.extrude_polygon(t,height=0.30), radians(90), 13.20, TOPR, 0.30)
        for t in (tri_out,tri_in)]
pino=boolean('difference',[pino, trimesh.util.concatenate(marcas)])
print('pino  faces=%d watertight=%s vol=%.1f mm3 massa=%.2f g'%(
      len(pino.faces),pino.is_watertight,pino.volume,pino.volume*0.905/1000))

# ================================================================ 2 · ANEL DIA
ND=31; SD=360.0/ND
anel_d=revolve([(14.30,BOTR),(20.50,BOTR),(20.50,38.05),(20.30,TOPR),(14.30,TOPR),
                (14.30,37.95),(13.90,37.80),(13.90,37.60),(14.30,37.45)])
serr=[cyl(0.50,37.15,38.30,24,20.50*cos(radians(k*15)),20.50*sin(radians(k*15))) for k in range(24)]
nums=text_cutters([(radians(90-(d-1)*SD), "%02d"%d) for d in range(1,ND+1)], 17.40, 2.20, 0.30)
dims=[dimple(15.2, radians(90-(d-1)*SD)) for d in range(1,ND+1)]
anel_d=boolean('difference',[anel_d, trimesh.util.concatenate(serr+[nums]+dims)])
print('dia   faces=%d watertight=%s vol=%.1f mm3 massa=%.2f g'%(
      len(anel_d.faces),anel_d.is_watertight,anel_d.volume,anel_d.volume*0.905/1000))

# ================================================================ 3 · ANEL MES
NM=12; SM=30.0
anel_m=revolve([(6.00,BOTR),(12.10,BOTR),(12.10,38.05),(11.90,TOPR),(6.00,TOPR),
                (6.00,37.95),(5.60,37.80),(5.60,37.60),(6.00,37.45)])
numsm=text_cutters([(radians(90-(m-1)*SM), "%02d"%m) for m in range(1,NM+1)], 9.30, 2.40, 0.30)
divs=[]
for m in range(NM):
    a=radians(90-(m+0.5)*SM)
    sp=SP([(-0.20,-2.75),(0.20,-2.75),(0.20,2.75),(-0.20,2.75)])
    divs.append(place(trimesh.creation.extrude_polygon(sp,height=0.30), a, 9.05, TOPR, 0.30))
dimsm=[dimple(7.0, radians(90-(m-1)*SM)) for m in range(1,NM+1)]
anel_m=boolean('difference',[anel_m, trimesh.util.concatenate([numsm]+divs+dimsm)])
print('mes   faces=%d watertight=%s vol=%.1f mm3 massa=%.2f g'%(
      len(anel_m.faces),anel_m.is_watertight,anel_m.volume,anel_m.volume*0.905/1000))

# ================================================================ export
for nome,m in [('Chrono_01_Pino_Travinha',pino),
               ('Chrono_02_Anel_Dia',anel_d),
               ('Chrono_03_Anel_Mes',anel_m)]:
    toC(m).export(f'{OUT}/{nome}.stl')
conj=trimesh.util.concatenate([toC(pino),toC(anel_d),toC(anel_m)])
conj.export(f'{OUT}/Chrono_04_Datador_Montado.stl')

# --- verificacao de interferencia entre as pecas montadas
for a,b,n in [(pino,anel_d,'pino x anel de dia'),(pino,anel_m,'pino x anel de mes'),
              (anel_d,anel_m,'anel dia x anel mes')]:
    try:
        i=boolean('intersection',[a,b]); v=i.volume if i is not None and len(i.faces) else 0.0
    except Exception: v=float('nan')
    print('interferencia %-22s %8.4f mm3'%(n,v))
print('\nmassa do datador: %.2f g  ·  valvula original: %.2f g  ·  delta %+.2f g'%(
   (pino.volume+anel_d.volume+anel_m.volume)*0.905/1000, 2258.5*0.905/1000,
   (pino.volume+anel_d.volume+anel_m.volume-2258.5)*0.905/1000))
