"""Ilustracao da ponteira proposta — desenhada por cima do mostrador REAL
(mapa de altura de M01+M02), na mesma escala. Nada de mockup a mao livre."""
import sys; sys.path.insert(0,'.')
import numpy as np, trimesh
from math import radians, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon as SP
from lib3d import CX, CZ
import mapa as MP

# ---------------- cotas propostas ----------------
BULBO_R, BULBO_OFF = 8.20, 1.00     # cabeca: raio e quanto passa atras do eixo
NARIZ_R, NARIZ_Y   = 0.60, 14.95    # ponta em r 15,55 — agulha de novo
PONTA              = NARIZ_Y+NARIZ_R
JR0, JR1, JMEIA    = 8.70, 11.30, 1.80   # janela: SO o mes
MES_R              = 10.00
DIA_R0, DIA_R1     = 15.80, 17.50   # onde ficam os numerais do dia
MARCA_M, MARCA_D   = 7.40, 13.60

def gota(n=400):
    t=np.linspace(0,2*pi,n,endpoint=False)
    a=[(BULBO_R*cos(x), -BULBO_OFF+BULBO_R*sin(x)) for x in t]
    b=[(NARIZ_R*cos(x),  NARIZ_Y+NARIZ_R*sin(x)) for x in t]
    return SP(a).union(SP(b)).convex_hull

# ---------------- fundo: o mostrador de verdade ----------------
D='/home/user/produtos/chrono/stl_v2/'
M1=trimesh.load(D+'Chrono_M01_Valvula_Dias.stl'); M2=trimesh.load(D+'Chrono_M02_Aro_Meses.stl')
def gira(m,g):
    n=m.copy(); n.apply_translation([-CX,0,-CZ])
    n.apply_transform(trimesh.transformations.rotation_matrix(radians(g),[0,1,0]))
    n.apply_translation([CX,0,CZ]); return n
SD=360/31; DIA,MES=9,3
MP.mapa([M1,gira(M2,(MES-1)*30-(DIA-1)*SD)], 36.5, 38.6, 'fundo.png', W=1400, span=46.0)

W=1400; SPAN=46.0; K=W/SPAN; CXp=CYp=W/2
im=Image.open('fundo.png').convert('RGB')
big=Image.new('RGB',(W,W+230),(250,250,251)); big.paste(im,(0,0))
d=ImageDraw.Draw(big,'RGBA')
def P(x,y):   # (tangencial, radial) -> pixel, com a ponteira apontando para o dia
    a=radians(90+(DIA-1)*SD)
    ex,ey=-sin(a),cos(a); rx,ry=cos(a),sin(a)
    X=x*ex+y*rx; Z=x*ey+y*ry
    return (CXp-X*K, CYp-Z*K)
try:
    F  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 25)
    Fp = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 21)
except: F=Fp=ImageFont.load_default()

TEAL=(11,169,177)
d.polygon([P(x,y) for x,y in gota().exterior.coords], fill=TEAL+(200,), outline=(8,120,126,255))
# a janela tem de DEIXAR VER o numeral: repoe o fundo original dentro dela
jan=[P(-JMEIA,JR0),P(JMEIA,JR0),P(JMEIA,JR1),P(-JMEIA,JR1)]
masc=Image.new('L',(W,W),0); ImageDraw.Draw(masc).polygon(jan,fill=255)
big.paste(im,(0,0),masc)
d=ImageDraw.Draw(big,'RGBA')
d.polygon(jan, outline=(8,120,126,255), width=4)
for txt,r in (('M',MARCA_M),('D',MARCA_D)):
    b=d.textbbox((0,0),txt,font=F); d.text((P(0,r)[0]-b[2]/2,P(0,r)[1]-b[3]/2),txt,font=F,fill=(255,255,255,235))
# calls
def seta(p0,p1,txt,anc='ls'):
    d.line([p0,p1],fill=(25,32,40,255),width=3)
    d.ellipse([p0[0]-6,p0[1]-6,p0[0]+6,p0[1]+6],fill=(25,32,40,255))
    b=d.textbbox((0,0),txt,font=Fp); x=p1[0] if anc=='ls' else p1[0]-b[2]
    d.rectangle([x-8,p1[1]-b[3]-9,x+b[2]+8,p1[1]+6],fill=(255,255,255,235))
    d.text((x,p1[1]-b[3]-4),txt,font=Fp,fill=(20,26,32,255))
seta(P(0,10.0),(700,330),'1 · janela enquadra só o MÊS')
seta(P(0,PONTA),(690,1160),'2 · a ponta indica o DIA, sem cobrir')
seta(P(0,-7.4),(300,470),'3 · cabeça com o ícone','rs')
d.rectangle([0,W,W,W+230],fill=(244,246,247,255))
d.text((40,W+24),'PONTEIRA PROPOSTA — seleção só no mês, a seta aponta o dia',font=F,fill=(20,26,32,255))
for i,ln in enumerate([
 'A janela encurta e passa a enquadrar SÓ o numeral do mês (r 8,70 a 11,30, 3,60 de largura).',
 'O dia volta a ser indicado pela PONTA, que para em r 15,55 — 0,25 mm antes do numeral, sem cobri-lo.',
 'Como não há mais rasgo na frente, a ponta pode voltar a ser AGULHA (nariz Ø1,20) como no seu desenho.',
 'Espessura 1,60 e cabeça Ø16,40 com o ícone, sem mudança. M e D gravados marcam cada leitura.']):
    d.text((40,W+62+i*34),'· '+ln,font=Fp,fill=(60,70,78,255))
big.save('/home/user/produtos/chrono/stl_v2/proposta_ponteira.png')
print('proposta_ponteira.png')
g=gota()
for r in (JR0,JR1,13.0,14.5,PONTA):
    xs=[p[0] for p in g.exterior.coords if abs(p[1]-r)<0.06]
    if xs: print('  r=%5.2f  meia-largura da lamina %5.2f'%(r,max(xs)))
