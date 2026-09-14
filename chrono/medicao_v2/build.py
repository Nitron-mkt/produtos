import sys, os, glob, numpy as np, trimesh
sys.path.insert(0,'.')
from lib3d import CX, CZ, revolve, cyl, ball, boolean, place, polys_to_shapely
from math import pi, radians, cos, sin
from shapely.geometry import Polygon as SP
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

OUT='/home/user/produtos/chrono/stl_v2'; os.makedirs(OUT, exist_ok=True)
VALV='/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/5882c071-Mont_pote_com_valvula__prova_valvula1.STL'

FACE = 37.23                       # face de topo da valvula = datum
# ---- M01 valvula ----
DIA_RI, DIA_RE   = 14.60, 18.70    # banda dos dias (fixa, nao gira)
DIA_R            = 16.85
DIA_CAP, DIA_REL = 1.70, 0.25   # traco de 0,32: o relevo desce junto p/ o molde encher
# mesa dos dias: anel plano que ponte a concha de acionamento das 12h, para que
# os 31 numeros nasçam todos na mesma altura e a banda vire superficie de aperto
MESA_RI, MESA_RE, MESA_H = 14.20, 18.75, 0.18
CONCHA_A0, CONCHA_A1, CONCHA_Y0 = 55.0, 125.0, 36.15   # setor e fundo da concha
POST_R, POST_TOP = 5.40, 38.05     # poste reto, rente ao topo do aro: o cubo da
                                   # travinha passa por cima dele, nao em volta
CHAPA_Y0 = 35.40                   # face de BAIXO da valvula no eixo — medida no seu STL
FURO_R   = 2.50                    # furo passante: sai por baixo da valvula
FURO_CH  = 0.35                    # chanfro de entrada no topo do poste
# O indice fixo do mes saiu: quem le o mes agora e a marca M da propria ponteira,
# que passa por cima dos numerais do aro. Dois giros, duas leituras, um so lugar.
DET_R            = 7.50            # raio das molas de detente
# ---- M02 aro dos meses (gira) ----
ARO_RI, ARO_RE, ARO_ESP = 5.60, 13.40, 0.80
ARO_Y0 = FACE+0.02; ARO_Y1 = ARO_Y0+ARO_ESP
MES_R, MES_CAP, MES_REL, MES_XS = 9.60, 2.00, 0.30, 1.00
# ---- M03 travinha com seta (gira livre no poste) ----
CUBO_RI, CUBO_RE = 2.20, 6.90      # cubo: cobre o poste e segura o aro
COL_Y0, COL_Y1   = 38.15, 38.95    # 0,10 acima do poste e do aro (o detente tem 0,16)
PINO_RE          = 2.40            # 0,10 de folga radial no furo de 2,50 — gira solto
PINO_Y1, PINO_Y0 = 34.00, CHAPA_Y0 # ponta do pino e ombro de retencao
FARPA_R          = 2.90            # 0,40 de encaixe radial sobre o furo de 2,50
FENDA_W, FENDAS  = 0.60, 4         # 4 pernas
BRACO_Y0         = 38.45           # face de baixo do braco interno -> 0,50 de espessura
EXT_Y0, EXT_Y1   = 37.95, 38.45    # braco externo, 0,50, rente aos numeros do dia
RAMPA_R0, RAMPA_R1 = 13.90, 14.55
MEIA_BR, MEIA_PT = 1.05, 0.70      # meia-largura do braco e da ponta (era 1,60)
ESP_H, ESP_W     = 0.50, 0.80      # espigao: para no mesmo 38,95 do cubo, topo raso

_FP=FontProperties(family="FreeSans", weight="bold")
def glyphs(txt, cap, xs=1.0):
    tp=TextPath((0,0), txt, size=1.0, prop=_FP)
    polys=[np.asarray(p) for p in tp.to_polygons() if len(p)>=3]
    h=TextPath((0,0),"8",size=1.0,prop=_FP).get_extents().height
    k=cap/h
    allp=np.vstack(polys); c=(allp.min(0)+allp.max(0))/2
    return [ (p-c)*k*np.array([xs,1.0]) for p in polys ]

def relevo(itens, R, cap, base, alt, xs=1.0):
    cs=[]
    for phi,txt in itens:
        for sp in polys_to_shapely(glyphs(txt,cap,xs)):
            pr=trimesh.creation.extrude_polygon(sp, height=alt)
            cs.append(place(pr, phi, R, base+alt, alt))
    return cs

def barra(r0,r1,y0,y1,meia,phi=radians(90)):
    pr=trimesh.creation.extrude_polygon(SP([(-meia,r0),(meia,r0),(meia,r1),(-meia,r1)]), height=y1-y0)
    return place(pr, phi, 0.0, y1, y1-y0)

def toC(m):
    n=m.copy(); n.apply_translation([CX,0,CZ]); return n

# =================================================== MOLDE 01 — VALVULA + 31 DIAS
valv=trimesh.load(VALV); valv.apply_translation([-CX,0,-CZ])
corte=trimesh.creation.box(extents=[60,8,60]); corte.apply_translation([0,FACE+4,0])
base=boolean('difference',[valv,corte])          # <<< parte de baixo REPLICADA, intacta
print('parte de baixo replicada: %.1f mm3, topo em Y %.2f'%(base.volume, base.bounds[1][1]))

# poste reto e VAZADO. O rebaixo da versao anterior era um undercut no lado de
# fora do macho — pedia gaveta ou arranque forcado. Furo reto e pino de macho.
poste=revolve([(POST_R,FACE),(POST_R,POST_TOP-0.30),(POST_R-0.30,POST_TOP),
               (FURO_R,POST_TOP),(FURO_R,FACE)])
# mesa: anel plano + enchimento da concha, so na cunha das 12h (a face de baixo
# da valvula nessa cunha nao passa de Y 35,40, entao nada e acrescentado por baixo)
mesa=revolve([(MESA_RI,FACE-0.60),(MESA_RE,FACE-0.60),(MESA_RE,FACE+MESA_H-0.10),
              (MESA_RE-0.10,FACE+MESA_H),(MESA_RI+0.10,FACE+MESA_H),(MESA_RI,FACE+MESA_H-0.10)])
NW=64; pol=[(0.0,0.0)]+[ (18.80*cos(radians(a)),18.80*sin(radians(a)))
       for a in np.linspace(CONCHA_A0,CONCHA_A1,NW) ]
cunha=trimesh.creation.extrude_polygon(SP(pol), height=FACE-CONCHA_Y0)
M=np.eye(4); M[:3,0]=[1,0,0]; M[:3,1]=[0,0,1]; M[:3,2]=[0,1,0]; M[:3,3]=[0,CONCHA_Y0,0]
cunha.apply_transform(M)
anel=boolean('difference',[cyl(18.80,CONCHA_Y0,FACE,n=192), cyl(MESA_RI,CONCHA_Y0-1,FACE+1,n=192)])
ench=boolean('intersection',[cunha,anel])
SD=360.0/31
dias=relevo([(radians(90+(d-1)*SD), '%d'%d) for d in range(1,32)], DIA_R, DIA_CAP, FACE+MESA_H, DIA_REL)
# indice FIXO do mes: triangulo em relevo entre o aro e a mesa
# 2 molas de detente (12 posicoes do aro => par a 180 deg fecha em 6 passos)
mol=[ball(0.42, DET_R*cos(radians(a)), FACE+0.18-0.42, DET_R*sin(radians(a))) for a in (0,180)]
m01=boolean('union',[base,mesa,ench,poste]+dias+mol)
# furo passante no eixo, com chanfro de entrada. Nao mexe na vedacao: a valvula
# veda nos 12h contra o ressalto que cerca o respiro, e a cavidade debaixo dela
# ja respira para fora pela folga de 0,22 mm em volta do disco.
furo=boolean('union',[cyl(FURO_R, CHAPA_Y0-2.0, POST_TOP+0.5, n=144),
                      revolve([(FURO_R,POST_TOP-FURO_CH),(FURO_R+FURO_CH,POST_TOP),
                               (FURO_R+FURO_CH,POST_TOP+0.5),(FURO_R,POST_TOP+0.5)])])
m01=boolean('difference',[m01,furo])
print('M01 valvula+dias : faces=%6d  vol=%7.1f  massa=%.2f g'%(len(m01.faces),m01.volume,m01.volume*0.905/1000))

# =================================================== MOLDE 02 — ARO DOS MESES
aro=revolve([(ARO_RI,ARO_Y0),(ARO_RE,ARO_Y0),(ARO_RE,ARO_Y1-0.15),(ARO_RE-0.15,ARO_Y1),
             (ARO_RI+0.15,ARO_Y1),(ARO_RI,ARO_Y1-0.15)])
MES=[str(i) for i in range(1,13)]   # numeral, nao abreviacao: vende fora do Brasil
txt=relevo([(radians(90+i*30), MES[i]) for i in range(12)], MES_R, MES_CAP, ARO_Y1, MES_REL, MES_XS)
# 12 entalhes de unha no bordo externo (material RETIRADO: nada invade o anel do indice)
ent=[]
for i in range(12):
    a=radians(90+(i+0.5)*30)
    c=trimesh.creation.cylinder(radius=1.00, height=4.0, sections=48)
    c.apply_transform(trimesh.transformations.rotation_matrix(pi/2,[1,0,0]))
    c.apply_translation([13.85*cos(a), (ARO_Y0+ARO_Y1)/2, 13.85*sin(a)])
    ent.append(c)
# 12 covinhas de detente na face de baixo
dim=[ball(0.55, DET_R*cos(radians(90+i*30)), ARO_Y0+0.55-0.25, DET_R*sin(radians(90+i*30))) for i in range(12)]
m02=boolean('difference',[boolean('union',[aro]+txt), trimesh.util.concatenate(ent+dim)])
print('M02 aro dos meses: faces=%6d  vol=%7.1f  massa=%.2f g'%(len(m02.faces),m02.volume,m02.volume*0.905/1000))

# =================================================== MOLDE 03 — PONTEIRA
# Duas versoes, para comparar:
#   'md'     lamina cheia com as letras M e D gravadas. Estreitada na cintura
#            sobre a faixa do mes, senao a propria lamina tapa o numeral.
#   'janela' lamina mais larga com UM rasgo retangular que enquadra mes e dia.
CUBO_RE, CUBO_Y0, TOPO = 6.30, 38.15, 38.95   # cubo macico: fecha o pino e leva o icone
PINO_RE          = 2.40            # 0,10 de folga radial no furo de 2,50
PINO_Y1, PINO_Y0 = 34.00, CHAPA_Y0
FARPA_R          = 2.90            # 0,40 de encaixe radial, ombro a 90 graus
FENDA_W, FENDAS  = 0.60, 4
BR_Y0, EXT_Y0    = 38.45, 38.15    # face de baixo: interna (livre do relevo do mes) e externa
R_RAMPA0, R_RAMPA1 = 11.90, 12.50
MARCA_REL, ICONE_H = 0.25, 7.00    # marcas GRAVADAS: o topo continua raso em 38,95
import icone

def lam(r0,r1,meia,y0,y1):
    pr=trimesh.creation.extrude_polygon(SP([(-meia,r0),(meia,r0),(meia,r1),(-meia,r1)]), height=y1-y0)
    return place(pr, radians(90), 0.0, y1, y1-y0)

def grava(itens, R, cap):
    out=[]
    for phi,txt in itens:
        for sp in polys_to_shapely(glyphs(txt,cap)):
            pr=trimesh.creation.extrude_polygon(sp, height=MARCA_REL+0.2)
            out.append(place(pr, phi, R, TOPO+0.2, MARCA_REL+0.2))
    return out

def ponteira(variante):
    cubo=boolean('union',[
        revolve([(3.00,CUBO_Y0),(CUBO_RE,CUBO_Y0),(CUBO_RE,TOPO-0.20),(CUBO_RE-0.20,TOPO),(3.00,TOPO)]),
        cyl(3.10, CUBO_Y0, TOPO, n=96)])
    pino=revolve([(1.55,CUBO_Y0),(PINO_RE,CUBO_Y0),(PINO_RE,PINO_Y0),(FARPA_R,PINO_Y0),
                  (2.05,PINO_Y1),(1.85,PINO_Y1),(1.85,PINO_Y0),(1.55,CUBO_Y0)])
    fendas=[]; drenos=[]
    for i in range(FENDAS):
        a=radians(45+i*360.0/FENDAS)
        pr=trimesh.creation.extrude_polygon(
            SP([(-FENDA_W/2,0.0),(FENDA_W/2,0.0),(FENDA_W/2,3.60),(-FENDA_W/2,3.60)]),
            height=CUBO_Y0-PINO_Y1+0.2)
        fendas.append(place(pr, a, 0.0, CUBO_Y0, CUBO_Y0-PINO_Y1+0.2))
        # dreno radial sob o cubo: a agua do canal sai pelas fendas, corre por estes
        # quatro sulcos e cai fora. Cavidade cega que junta agua e o que nao pode.
        dr=trimesh.creation.extrude_polygon(
            SP([(-0.30,2.00),(0.30,2.00),(0.30,CUBO_RE+0.20),(-0.30,CUBO_RE+0.20)]), height=0.25)
        drenos.append(place(dr, a, 0.0, CUBO_Y0+0.25, 0.25))

    if variante=='md':
        MEIA, CINT = 1.60, 0.45        # lamina grossa, cintura fina sobre o numeral do mes
        R_PONTA, R_BICO = 14.40, 15.65
        partes=[lam(5.20, 8.40, MEIA, BR_Y0, TOPO),
                lam(8.40, 10.90, CINT, BR_Y0, TOPO),       # cintura: o numeral do mes
                lam(10.90, R_RAMPA0, MEIA, BR_Y0, TOPO),   # aparece 0,95 de cada lado
                lam(R_RAMPA0, R_RAMPA1, MEIA, BR_Y0, TOPO),
                lam(R_RAMPA1-0.10, R_PONTA, MEIA, EXT_Y0, TOPO),
                place(trimesh.creation.extrude_polygon(
                        SP([(-MEIA,R_PONTA-0.01),(MEIA,R_PONTA-0.01),(0.0,R_BICO)]), height=TOPO-EXT_Y0),
                      radians(90), 0.0, TOPO, TOPO-EXT_Y0)]
        vazio=[]
        marcas=grava([(radians(90),'M')], 7.00, 1.30)+grava([(radians(90),'D')], 13.10, 1.30)
    else:
        MEIA, JAN = 2.70, 1.70         # lamina larga, um rasgo so cobrindo as duas faixas
        R_JAN0, R_JAN1, R_BICO = 8.30, 17.70, 19.10
        partes=[lam(5.20, R_RAMPA0, MEIA, BR_Y0, TOPO),
                lam(R_RAMPA0, R_RAMPA1, MEIA, BR_Y0, TOPO),
                lam(R_RAMPA1-0.10, R_BICO-0.90, MEIA, EXT_Y0, TOPO),
                place(trimesh.creation.extrude_polygon(
                        SP([(-MEIA,R_BICO-0.91),(MEIA,R_BICO-0.91),(MEIA-0.9,R_BICO),(-MEIA+0.9,R_BICO)]),
                        height=TOPO-EXT_Y0), radians(90), 0.0, TOPO, TOPO-EXT_Y0)]
        vazio=[lam(R_JAN0, R_JAN1, JAN, EXT_Y0-0.30, TOPO+0.30)]
        marcas=grava([(radians(90),'M')], 7.10, 1.30)+grava([(radians(90),'D')], 18.45, 1.30)

    # rampa: desce de BR_Y0 para EXT_Y0 entre R_RAMPA0 e R_RAMPA1
    tri=trimesh.creation.extrude_polygon(
        SP([(R_RAMPA0-0.3,EXT_Y0-1.0),(R_RAMPA1+0.3,EXT_Y0-1.0),
            (R_RAMPA1+0.3,EXT_Y0),(R_RAMPA0,BR_Y0),(R_RAMPA0-0.3,BR_Y0)]), height=6.0)
    Mt=np.eye(4); Mt[:3,0]=[0,0,1]; Mt[:3,1]=[0,1,0]; Mt[:3,2]=[-1,0,0]; Mt[:3,3]=[3.0,0,0]
    tri.apply_transform(Mt)

    ico=[]
    for sp in icone.poligonos(ICONE_H, xflip=True):
        pr=trimesh.creation.extrude_polygon(sp, height=MARCA_REL+0.2)
        Mi=np.eye(4); Mi[:3,0]=[1,0,0]; Mi[:3,1]=[0,0,1]; Mi[:3,2]=[0,1,0]
        Mi[:3,3]=[0.0, TOPO-MARCA_REL, 0.0]
        pr.apply_transform(Mi); ico.append(pr)

    corpo=boolean('union',[cubo,pino]+partes)
    return boolean('difference',[corpo, trimesh.util.concatenate(fendas+drenos+marcas+ico+vazio+[tri])])

m03a=ponteira('md')
m03b=ponteira('janela')
for n,m in (('M03a M / D  ',m03a),('M03b janela ',m03b)):
    print('%s: faces=%6d  vol=%7.1f  massa=%.2f g  Ymax %.2f  Omax %.2f'
          %(n,len(m.faces),m.volume,m.volume*0.905/1000,m.bounds[1][1],
            max(m.bounds[1][0]-m.bounds[0][0], m.bounds[1][2]-m.bounds[0][2])))

for nome,m in [('Chrono_M01_Valvula_Dias',m01),('Chrono_M02_Aro_Meses',m02),
               ('Chrono_M03a_Ponteira_MD',m03a),('Chrono_M03b_Ponteira_Janela',m03b)]:
    toC(m).export(f'{OUT}/{nome}.stl')
trimesh.util.concatenate([toC(m01),toC(m02),toC(m03a)]).export(f'{OUT}/Chrono_M04a_Conjunto_MD.stl')
trimesh.util.concatenate([toC(m01),toC(m02),toC(m03b)]).export(f'{OUT}/Chrono_M04b_Conjunto_Janela.stl')
print('\nmassa do datador: %.2f g (M/D)  ·  %.2f g (janela)  ·  valvula original 2,04 g'
      %((m01.volume+m02.volume+m03a.volume)*0.905/1000,(m01.volume+m02.volume+m03b.volume)*0.905/1000))

print('\nlimpeza dos arquivos gravados:')
for f in sorted(glob.glob(OUT+'/*.stl')):
    n=trimesh.load(f)
    if not n.is_volume:
        deg=(~n.nondegenerate_faces()).sum()
        n.merge_vertices(digits_vertex=8)
        n.update_faces(n.nondegenerate_faces()); n.remove_unreferenced_vertices()
        trimesh.repair.fix_normals(n); n.export(f)
        print('  %-34s %4d faces degeneradas -> solido=%s'%(os.path.basename(f),deg,n.is_volume))
    else:
        print('  %-34s ja solido'%os.path.basename(f))
