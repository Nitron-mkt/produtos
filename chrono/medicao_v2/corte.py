"""Corte no plano do eixo (z=0): desenha os segmentos de cada malha. Sem scipy."""
import sys; sys.path.insert(0,'.')
import numpy as np, trimesh
from PIL import Image, ImageDraw
from lib3d import CX, CZ
D='/home/user/produtos/chrono/stl_v2/'
U='/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/'
def segs(m):
    T=m.triangles-np.array([CX,0,CZ]); out=[]
    for t in T:
        z=t[:,2]; s=np.sign(z)
        if abs(s.sum())==3: continue
        p=[]
        for i in range(3):
            a,b=t[i],t[(i+1)%3]
            if (a[2]>0)!=(b[2]>0):
                f=a[2]/(a[2]-b[2]); p.append((a[0]+f*(b[0]-a[0]), a[1]+f*(b[1]-a[1])))
        if len(p)>=2: out.append((p[0],p[1]))
    return out
PECAS=[('tampa',U+'1c50a47b-Mont_pote_com_valvula__Tampa_Pote_025_Pequeno_Cav1.STL',(150,158,166),1),
       ('M01',D+'Chrono_M01_Valvula_Dias.stl',(90,102,112),2),
       ('M02',D+'Chrono_M02_Aro_Meses.stl',(23,85,143),2),
       ('M03',D+'Chrono_M03_Travinha_Seta.stl',(168,74,22),2)]
X0,X1,Y0,Y1 = -26.0,26.0,30.0,40.5
W=1500; K=W/(X1-X0); H=int((Y1-Y0)*K)
img=Image.new('RGB',(W,H),(248,249,250)); d=ImageDraw.Draw(img)
def px(p): return ((p[0]-X0)*K, (Y1-p[1])*K)
for nome,f,cor,lw in PECAS:
    m=trimesh.load(f)
    for a,b in segs(m): d.line([px(a),px(b)], fill=cor, width=lw)
for y,txt in ((37.23,'37,23 face de topo'),(35.40,'35,40 face de baixo da valvula'),
              (34.00,'34,00 ponta do pino'),(32.15,'32,15 fundo do poco da tampa')):
    yy=(Y1-y)*K; d.line([(0,yy),(W,yy)], fill=(210,215,220), width=1)
    d.text((8,yy-14), txt, fill=(120,128,136))
img.save('corte.png'); print('corte.png', img.size)
