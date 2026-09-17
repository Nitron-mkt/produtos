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
# --- orcamento de altura: da face da valvula (37,23) ao aro de empilhamento da
# tampa (39,72) sao 2,49 mm. Rodinha e ponteiro no dobro pedem 3,3. A saida foi
# AFUNDAR a rodinha 0,60 num rebaixo, e gravar o numeral do mes em vez de releva-lo.
REB_H            = 0.60            # quanto a rodinha afunda na valvula
REB_RE           = 13.60           # parede externa do rebaixo
POST_R           = 6.60            # circunferencia central: O10,80 -> O13,20
POST_TOP         = 38.25           # rente ao topo da rodinha
CHAPA_Y0 = 35.40                   # face de BAIXO da valvula no eixo — medida no seu STL
FURO_R   = 3.00                    # furo passante O6,00 (era O5,00)
FURO_CH  = 0.35                    # chanfro de entrada no topo do poste
# O indice fixo do mes saiu: quem le o mes agora e a marca M da propria ponteira,
# que passa por cima dos numerais do aro. Dois giros, duas leituras, um so lugar.
DET_R            = 7.80            # raio das molas de detente
# ---- M02 aro dos meses (gira) ----
ARO_RI, ARO_RE, ARO_ESP = 6.80, 13.40, 1.60   # o DOBRO da espessura · bore no poste novo
ARO_Y0 = FACE-REB_H+0.02; ARO_Y1 = ARO_Y0+ARO_ESP   # 36,65 -> 38,25
MES_R, MES_CAP, MES_REL, MES_XS = 9.80, 2.00, 0.30, 1.00   # MES_REL agora e GRAVADO
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
poste=revolve([(POST_R,CHAPA_Y0),(POST_R,POST_TOP-0.30),(POST_R-0.30,POST_TOP),
               (FURO_R,POST_TOP),(FURO_R,CHAPA_Y0)])
# rebaixo onde a rodinha afunda 0,60: anel entre o poste e REB_RE
reb=revolve([(POST_R,FACE-REB_H),(REB_RE,FACE-REB_H),(REB_RE,FACE+0.5),(POST_R,FACE+0.5)])
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
# molas do detente: nascem no FUNDO do rebaixo, nao na face
mol=[ball(0.42, DET_R*cos(radians(a)), FACE-REB_H+0.18-0.42, DET_R*sin(radians(a))) for a in (0,180)]
m01=boolean('difference',[boolean('union',[base,mesa,ench]+dias), reb])
m01=boolean('union',[m01,poste]+mol)
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
# numeral GRAVADO: com 1,60 de espessura o topo tem de ficar raso, senao o
# relevo rouba os 0,30 que faltam para o conjunto passar sob o aro da tampa
txt=relevo([(radians(90+i*30), MES[i]) for i in range(12)], MES_R, MES_CAP, ARO_Y1-MES_REL, MES_REL+0.20, MES_XS)
# 12 entalhes de unha no bordo externo (material RETIRADO: nada invade o anel do indice)
ent=[]
for i in range(12):
    a=radians(90+(i+0.5)*30)
    c=trimesh.creation.cylinder(radius=1.10, height=4.0, sections=48)
    c.apply_transform(trimesh.transformations.rotation_matrix(pi/2,[1,0,0]))
    c.apply_translation([13.75*cos(a), (ARO_Y0+ARO_Y1)/2, 13.75*sin(a)])  # entalhe 0,75 fundo
    ent.append(c)
# 12 covinhas de detente na face de baixo
dim=[ball(0.55, DET_R*cos(radians(90+i*30)), ARO_Y0+0.55-0.25, DET_R*sin(radians(90+i*30))) for i in range(12)]
m02=boolean('difference',[aro, trimesh.util.concatenate(txt+ent+dim)])
print('M02 aro dos meses: faces=%6d  vol=%7.1f  massa=%.2f g'%(len(m02.faces),m02.volume,m02.volume*0.905/1000))

# =================================================== MOLDE 03 — PONTEIRA
# Lamina em CUNHA: sai larga do meio do icone e afina ate a ponta, como ponteiro
# de relogio. Era isso que faltava — lamina de lados paralelos deixa a borda da
# janela fina demais perto do cubo, que foi o que voce viu na peca impressa.
CUBO_RI, CUBO_RE = 2.20, 7.60      # cubo maior: cobre o poste de O13,20
CUBO_Y0, TOPO    = 38.35, 39.95    # 1,60 de espessura — o DOBRO
PINO_RE          = 2.90            # 0,10 de folga radial no furo de 3,00
PINO_Y1, PINO_Y0 = 34.00, CHAPA_Y0
FARPA_R          = 3.40            # 0,40 de encaixe radial sobre o furo
FENDA_W, FENDAS  = 0.70, 4
MARCA_REL, ICONE_H = 0.25, 8.00
import icone

# --- GOTA: fecho convexo de dois circulos no eixo radial. Cabeca redonda que
# passa atras do eixo, afinando ate o nariz. Desenho do cliente.
BULBO_R, BULBO_OFF = 8.20, 1.00    # cabeca: centro 1,00 atras do eixo
NARIZ_R, NARIZ_Y   = 1.20, 14.35   # ponta ARREDONDADA O2,40 em r 15,55
# A janela agora enquadra SO o mes e para em r 11,30, entao nao ha mais rasgo
# la na frente obrigando nariz grosso. O nariz de O2,40 e por LAVAGEM: ponta
# viva engancha na bucha. Somado ao canto R0,70 da janela, a borda no canto
# externo dela vai de 0,76 para 1,23 mm.
def gota(rb=BULBO_R, off=BULBO_OFF, rn=NARIZ_R, yn=NARIZ_Y, n=180):
    import numpy as _np
    t=_np.linspace(0,2*pi,n,endpoint=False)
    pa=[(rb*cos(a), -off+rb*sin(a)) for a in t]
    pb=[(rn*cos(a),  yn+rn*sin(a)) for a in t]
    return SP(pa).union(SP(pb)).convex_hull

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

JAN_R0, JAN_R1, JAN_M, JAN_RC = 8.70, 11.30, 1.80, 0.70   # janela SO do mes
def retangulo_arredondado(r0,r1,meia,rc):
    return SP([(-meia+rc,r0+rc),(meia-rc,r0+rc),(meia-rc,r1-rc),(-meia+rc,r1-rc)]).buffer(rc, join_style=1)

def ponteira():
    cubo=cyl(3.30, CUBO_Y0, TOPO, n=96)
    pino=revolve([(2.05,CUBO_Y0),(PINO_RE,CUBO_Y0),(PINO_RE,PINO_Y0),(FARPA_R,PINO_Y0),
                  (2.55,PINO_Y1),(2.35,PINO_Y1),(2.35,PINO_Y0),(2.05,CUBO_Y0)])
    fendas=[]; drenos=[]
    for i in range(FENDAS):
        a=radians(45+i*360.0/FENDAS)
        pr=trimesh.creation.extrude_polygon(
            SP([(-FENDA_W/2,0.0),(FENDA_W/2,0.0),(FENDA_W/2,4.20),(-FENDA_W/2,4.20)]),
            height=CUBO_Y0-PINO_Y1+0.2)
        fendas.append(place(pr, a, 0.0, CUBO_Y0, CUBO_Y0-PINO_Y1+0.2))
        dr=trimesh.creation.extrude_polygon(
            SP([(-0.35,2.60),(0.35,2.60),(0.35,8.20),(-0.35,8.20)]), height=0.30)
        drenos.append(place(dr, a, 0.0, CUBO_Y0+0.30, 0.30))

    lamina=place(trimesh.creation.extrude_polygon(gota(), height=TOPO-CUBO_Y0),
                 radians(90), 0.0, TOPO, TOPO-CUBO_Y0)
    jp=retangulo_arredondado(JAN_R0,JAN_R1,JAN_M,JAN_RC)
    jan=place(trimesh.creation.extrude_polygon(jp, height=TOPO-CUBO_Y0+0.6),
              radians(90), 0.0, TOPO+0.3, TOPO-CUBO_Y0+0.6)
    # chanfro no bordo de cima: abre o cone de visao do numeral no fundo de 1,60
    ch=place(trimesh.creation.extrude_polygon(jp.buffer(0.45, join_style=1), height=0.75),
             radians(90), 0.0, TOPO+0.35, 0.75)
    marcas=grava([(radians(90),'M')], 7.40, 1.10)+grava([(radians(90),'D')], 13.60, 1.10)

    ico=[]
    for sp in icone.poligonos(ICONE_H, xflip=True):
        pr=trimesh.creation.extrude_polygon(sp, height=MARCA_REL+0.2)
        Mi=np.eye(4); Mi[:3,0]=[1,0,0]; Mi[:3,1]=[0,0,1]; Mi[:3,2]=[0,1,0]
        Mi[:3,3]=[0.0, TOPO-MARCA_REL, 0.0]
        pr.apply_transform(Mi); ico.append(pr)

    corpo=boolean('union',[cubo,pino,lamina])
    corte=boolean('union', fendas+drenos+marcas+ico+[jan,ch])
    return boolean('difference',[corpo, corte])

m03=ponteira()
print('M03 ponteira     : faces=%6d  vol=%7.1f  massa=%.2f g  Ymax %.2f  Omax %.2f'
      %(len(m03.faces),m03.volume,m03.volume*0.905/1000,m03.bounds[1][1],
        max(m03.bounds[1][0]-m03.bounds[0][0], m03.bounds[1][2]-m03.bounds[0][2])))

for nome,m in [('Chrono_M01_Valvula_Dias',m01),('Chrono_M02_Rodinha_Meses',m02),
               ('Chrono_M03_Ponteira',m03)]:
    toC(m).export(f'{OUT}/{nome}.stl')
trimesh.util.concatenate([toC(m01),toC(m02),toC(m03)]).export(f'{OUT}/Chrono_M04_Conjunto.stl')
print('\nmassa do datador: %.2f g   (valvula original 2,04 g)'
      %((m01.volume+m02.volume+m03.volume)*0.905/1000))

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
