#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Plano de pecas do showroom com a lista de 10/09/2026:
paineis 200x620 (checkout) · 305x620 e 305x725 (parede/ponta) · 450x725 (ilha)
altura BAL02AC 270 · PSA02 346 · PSA05 513 · largura BAL01AC 183 · BLA03AC 287 · PSC02 415
comprimento PST02 617 · PSC04 717. Gera dados/54-plano-pecas.xlsx (formulas) e imprime o resumo."""
import importlib.util, pathlib, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
RAIZ=pathlib.Path(__file__).resolve().parent.parent
def load(n,f):
    s=importlib.util.spec_from_file_location(n,RAIZ/'analise'/f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
cad=load('cad','pdv-caderno.py'); pc=load('pc','planograma-catalogo.py')
OUT=RAIZ/'dados'/'54-plano-pecas.xlsx'

# ------------------------------------------------------------ as pecas
PAINEIS={'200×620':(200,620,183,617),'305×620':(305,620,287,617),'305×725':(305,725,287,717),'450×725':(450,725,415,717)}
LARG={183:'BAL01AC',287:'BLA03AC',415:'PSC02'}; COMP={617:'PST02',717:'PSC04'}; ALT={270:'BAL02AC',346:'PSA02',513:'PSA05'}
GMM,DENS,PANT,RSKG=cad.GMM,cad.DENS,cad.PANT,cad.RSKG
ripa_kg=lambda mm: mm*GMM/1000; pan_kg=lambda l,c: l*c*PANT*DENS/1000
def bom(painel,pilha,coroa=None):
    lp,cp,rl,rc=PAINEIS[painel]
    f=dict(nome='',slug='',bc=COMP[rc],bcv=rc,bl=LARG[rl],blv=rl,pan=(lp,cp),vaos=(1,1,1),pilha=pilha,coroa=coroa,ganch=False,fundo=False,deck=False,casinha=False,faces=1,lede='',cap='')
    b=cad.bom(f,1); b['painel']=painel; b['rl']=rl; b['rc']=rc; b['pilha']=pilha; b['coroa']=coroa; return b

# ------------------------------------------------------------ os modulos do plano
MOD=[
 ('parede-725',  '305×725',[270]*6,None,'Parede · sul, norte, entrada · 7 prateleiras, duas na zona dos olhos'),
 ('parede-620',  '305×620',[270]*6,None,'Parede · ajuste de canto do sul'),
 ('parede-fundo','305×725',[513,346,346,270],None,'Parede do fundo · lixeira na baia de 490 e nas duas de 323; olhos a 1.542'),
 ('fundo-620',   '305×620',[513,346,346,270],None,'Parede do fundo · ajuste de canto, mesma pilha'),
 ('ponta',       '305×725',[346,346,270],None,'Ponta de gôndola · cabeceira das ilhas, 4 prateleiras, baias de 323'),
 ('ilha',        '450×725',[513,346],None,'Ilha · 500 de profundidade, topo aberto para produto alto; 2 × 2 costa a costa'),
 ('checkout',    '200×620',[270]*3,None,'Checkout · 268 de profundidade, 4 prateleiras, segundo facing dos campeões'),
 ('arara',       '305×725',[513,513],513,'Arara Nitron-Mob · vitrine da entrada; peça L como coroa'),
]
B={k:bom(p,pil,cor) for k,p,pil,cor,_ in MOD}
L759=cad.ext_comp(717,1); L659=cad.ext_comp(617,1)
def compor(livre):
    c=[(livre-(a*L759+b*L659),a,b) for a in range(0,25) for b in range(0,6) if a*L759+b*L659<=livre]
    fmin=min(x[0] for x in c); return min((x for x in c if x[0]<=fmin+100),key=lambda x:(x[2],x[0]))
# corridas livres com as paredes laterais a 372: sul inteira; norte do pilar (6.745) ao modulo do fundo (12.978); fundo entre sul e norte; entrada da porta (2.000) ao modulo do sul (7.148)
fs,aS,bS=compor(13350); fn,aN,bN=compor(12978-6745); ff,aF,bF=compor(7520-372-372); fe,aE,bE=compor(7148-2000)
PLANO=[
 ('Paredão sul · cozinha','parede-725',aS,13350),('Paredão sul · ajuste de canto','parede-620',bS,None),
 ('Paredão norte · organização','parede-725',aN,6233),
 ('Paredão do fundo · banho e lavanderia','parede-fundo',aF,6776),('Paredão do fundo · ajuste de canto','fundo-620',bF,None),
 ('Parede de entrada · frasqueiras e infantil','parede-725',3,5148),
 ('Vitrine da entrada · araras Nitron-Mob','arara',2,None),
 ('Ilhas · 2 ilhas de 2 × 2','ilha',8,None),
 ('Pontas de gôndola · 2 por ilha','ponta',4,None),
 ('Corredor de checkout · 2 lados × 3','checkout',6,None),
]

# ------------------------------------------------------------ planilha
F='Arial'; fb=Font(name=F,size=10); fB=Font(name=F,size=10,bold=True); fin=Font(name=F,size=10,color='0000FF'); flink=Font(name=F,size=10,color='008000')
fh=Font(name=F,size=10,bold=True,color='FFFFFF'); ft=Font(name=F,size=14,bold=True); fn_=Font(name=F,size=9,italic=True,color='555555')
HEAD=PatternFill('solid',fgColor='1EA7AC'); YEL=PatternFill('solid',fgColor='FFFF00')
thin=Side(style='thin',color='BFBFBF'); box=Border(left=thin,right=thin,top=thin,bottom=thin)
C=Alignment(horizontal='center',vertical='center'); WR=Alignment(wrap_text=True,vertical='top')
BRL='"R$" #,##0.00'; MM='#,##0'
def header(ws,row,cols):
    for i,c in enumerate(cols):
        x=ws.cell(row,1+i,c); x.font=fh; x.fill=HEAD; x.alignment=C; x.border=box
def widths(ws,w):
    for i,x in enumerate(w,1): ws.column_dimensions[L(i)].width=x
wb=Workbook()

# Pecas
K=wb.active; K.title='Pecas'
K['A1']='Nitron Mob PDV — as peças (lista de 10/09/2026)'; K['A1'].font=ft
K['A2']='4 painéis com papel definido, 8 ripas (PIs existentes), 4 conectores. Custo unitário em amarelo é entrada; madeira a R$ %.2f/kg.'%RSKG; K['A2'].font=fn_
header(K,4,['Peça','Código','Medida (mm)','Massa unit. (kg)','Custo unit. (R$)','Papel'])
pecas=[('Painel 200×620','novo · pinus 15','200 × 620',pan_kg(200,620),pan_kg(200,620)*RSKG,'checkout'),
       ('Painel 305×620','novo · pinus 15','305 × 620',pan_kg(305,620),pan_kg(305,620)*RSKG,'parede / ponta — ajuste'),
       ('Painel 305×725','novo · pinus 15','305 × 725',pan_kg(305,725),pan_kg(305,725)*RSKG,'parede / ponta — padrão'),
       ('Painel 450×725','novo · pinus 15','450 × 725',pan_kg(450,725),pan_kg(450,725)*RSKG,'ilha'),
       ('Ripa largura 183','BAL01AC','183',ripa_kg(183),ripa_kg(183)*RSKG,'profundidade 268 (checkout)'),
       ('Ripa largura 287','BLA03AC','287',ripa_kg(287),ripa_kg(287)*RSKG,'profundidade 372 (parede, ponta)'),
       ('Ripa largura 415','PSC02','415',ripa_kg(415),ripa_kg(415)*RSKG,'profundidade 500 (ilha)'),
       ('Ripa comprimento 617','PST02','617',ripa_kg(617),ripa_kg(617)*RSKG,'vão de 620'),
       ('Ripa comprimento 717','PSC04','717',ripa_kg(717),ripa_kg(717)*RSKG,'vão de 725'),
       ('Ripa vertical 270','BAL02AC','270',ripa_kg(270),ripa_kg(270)*RSKG,'baia de 247 livres'),
       ('Ripa vertical 346','PSA02','346',ripa_kg(346),ripa_kg(346)*RSKG,'baia de 323 livres — lixeira e cesto médios'),
       ('Ripa vertical 513','PSA05','513',ripa_kg(513),ripa_kg(513)*RSKG,'baia de 490 livres — e a coroa da arara'),
       ('Pé','sobra de ripa','60',ripa_kg(60),ripa_kg(60)*RSKG,''),
       ('Trizeta','PP · molde existe','—',cad.M_TZ/1000,cad.C_TZ,'canto de cada nível'),
       ('Cruzeta','PP · 4 injetadas','—',cad.M_CZ/1000,cad.C_CZ,'zero neste plano: módulos de um vão'),
       ('Peça L','PP · molde existe','—',cad.M_L/1000,cad.C_L,'coroa da arara'),
       ('Tampa','PP · molde existe','—',cad.M_T/1000,cad.C_T,'uma por poste')]
KR={}
for i,(a,b,c,kg,cu,pap) in enumerate(pecas):
    r=5+i; KR[a]=r
    K.cell(r,1,a).font=fB; K.cell(r,2,b).font=fb; K.cell(r,3,c).font=fb
    x=K.cell(r,4,round(kg,4)); x.font=fin; x.number_format='0.0000'
    y=K.cell(r,5,round(cu,4)); y.font=fin; y.number_format='"R$" 0.0000'; y.fill=YEL
    K.cell(r,6,pap).font=fn_
    for k in range(1,7): K.cell(r,k).border=box
widths(K,[22,18,12,15,15,52])
kd=lambda n: f'Pecas!$D${KR[n]}'; kc=lambda n: f'Pecas!$E${KR[n]}'

# Modulos
M=wb.create_sheet('Modulos')
M['A1']='Os sete módulos do plano — todos de um vão, quatro postes próprios, zero cruzeta'; M['A1'].font=ft
M['A2']='Contagem por módulo: trizeta 4 por nível de prateleira · tampa e pé 4 · painel 1 por prateleira · ripa de comprimento e de largura 2 por nível · ripa vertical 4 por baia. Coroa: 4 peças L no lugar das trizetas, +2 ripas de comprimento, sem ripa de largura e sem prateleira.'; M['A2'].font=fn_
cols=['Módulo','Painel','Ripa larg.','Ripa compr.','Pilha (de baixo p/ cima)','Baias','Coroa','Prateleiras','Comprimento (mm)','Profundidade (mm)','Altura (mm)',
      'Trizetas','Peças L','Tampas','Painéis','Ripas compr.','Ripas larg.','Ripas 270','Ripas 346','Ripas 513','Pés','Massa (kg)','Custo material (R$)','Uso']
header(M,4,cols); MR={}
for i,(k,p,pil,cor,uso) in enumerate(MOD):
    r=5+i; MR[k]=r; b=B[k]; lp,cp,rl,rc=PAINEIS[p]
    M.cell(r,1,k).font=fB; M.cell(r,2,p).font=fb; M.cell(r,3,rl).font=fin; M.cell(r,4,rc).font=fin
    M.cell(r,5,'·'.join(map(str,pil))+(f' + coroa {cor}' if cor else '')).font=fb
    M.cell(r,6,len(pil)).font=fin; M.cell(r,7,cor or 0).font=fin
    M.cell(r,8,f'=F{r}+1'); M.cell(r,9,round(cad.ext_comp(rc,1),1)).number_format=MM; M.cell(r,10,round(cad.ext_prof(rl),1)).number_format=MM
    M.cell(r,11,round(cad.altura(pil,cor),1)).number_format=MM
    # coroa: a peca L faz o no de topo (sem trizeta) e so leva ripa de comprimento (sem largura) -- igual ao caderno
    M.cell(r,12,f'=4*H{r}'); M.cell(r,13,f'=IF(G{r}>0,4,0)'); M.cell(r,14,4); M.cell(r,15,f'=H{r}')
    M.cell(r,16,f'=2*(H{r}+IF(G{r}>0,1,0))'); M.cell(r,17,f'=2*H{r}')
    for j,alt in enumerate((270,346,513)):
        n=pil.count(alt)+(1 if cor==alt else 0); M.cell(r,18+j,f'=4*{n}')
    M.cell(r,21,4)
    pn='Painel %s'%p; rln='Ripa largura %d'%rl; rcn='Ripa comprimento %d'%rc
    massa=f'=L{r}*{kd("Trizeta")}+M{r}*{kd("Peça L")}+N{r}*{kd("Tampa")}+O{r}*{kd(pn)}+P{r}*{kd(rcn)}+Q{r}*{kd(rln)}+R{r}*{kd("Ripa vertical 270")}+S{r}*{kd("Ripa vertical 346")}+T{r}*{kd("Ripa vertical 513")}+U{r}*{kd("Pé")}'
    M.cell(r,22,massa).number_format='0.0'; M.cell(r,23,massa.replace('$D$','$E$')).number_format=BRL
    M.cell(r,24,uso).font=fn_
    for c_ in range(1,25): M.cell(r,c_).border=box
widths(M,[13,9,8,9,22,6,6,9,12,12,10,8,7,7,8,9,9,8,8,8,5,9,14,60])
M.freeze_panes='B5'

# Showroom
S=wb.create_sheet('Showroom')
S['A1']='O showroom com as peças novas — onde vai cada módulo e quanto'; S['A1'].font=ft
S['A2']='Quantidades em azul são a proposta; troque e o resto recalcula. Paredes: sul %d × 759 + %d × 659 (folga %.0f) · norte %d × 759 (%.0f) · fundo %d × 759 + %d × 659 (%.0f) · entrada 3 módulos + vitrine de %.0f mm.'%(aS,bS,fs,aN,fn,aF,bF,ff,5148-3*L759); S['A2'].font=fn_
header(S,4,['Onde','Módulo','Qtd','Comprimento montado (mm)','Custo (R$)','Massa (kg)','Frente (m)'])
LK=lambda col,r: f'INDEX(Modulos!${col}$5:${col}${4+len(MOD)},MATCH($B{r},Modulos!$A$5:$A${4+len(MOD)},0))'
for i,(onde,mod,q,livre) in enumerate(PLANO):
    r=5+i; S.cell(r,1,onde).font=fB; S.cell(r,2,mod).font=fin; S.cell(r,3,q).font=fin; S.cell(r,3).fill=YEL
    S.cell(r,4,f'=C{r}*{LK("I",r)}').number_format=MM
    S.cell(r,5,f'=C{r}*{LK("W",r)}').number_format=BRL; S.cell(r,6,f'=C{r}*{LK("V",r)}').number_format='0.0'
    S.cell(r,7,f'=C{r}*{LK("I",r)}*{LK("H",r)}/1000').number_format='0.0'
    for c_ in range(1,8): S.cell(r,c_).border=box
rt=5+len(PLANO); S.cell(rt,1,'TOTAL').font=fB; S.cell(rt,3,f'=SUM(C5:C{rt-1})').font=fB
for c_,fm in ((5,BRL),(6,'0.0'),(7,'0.0')):
    x=S.cell(rt,c_,f'=SUM({L(c_)}5:{L(c_)}{rt-1})'); x.font=fB; x.number_format=fm
for c_ in range(1,8): S.cell(rt,c_).border=box
widths(S,[42,14,6,22,14,10,10])

# Compras
P_=wb.create_sheet('Compras')
P_['A1']='Lista de compras — painéis, ripas e conectores para o showroom inteiro'; P_['A1'].font=ft
P_['A2']='Cada linha soma quantidade × módulos da aba Showroom. É a resposta do plano: quantos painéis de cada, quantas ripas de largura, comprimento e altura.'; P_['A2'].font=fn_
header(P_,4,['Peça','Quantidade','Massa (kg)','Custo (R$)','Onde entra'])
def soma(colM,filtro=None):
    # SUMPRODUCT(qtd, [filtro por painel], INDEX(col) por MATCH)
    rng=f'$C$5:$C${rt-1}'; idx=f'IFERROR(INDEX(Modulos!${colM}$5:${colM}${4+len(MOD)},MATCH(Showroom!$B$5:$B${rt-1},Modulos!$A$5:$A${4+len(MOD)},0)),0)'
    f=f'=SUMPRODUCT(Showroom!{rng},{idx}'
    if filtro: f+=f',--(IFERROR(INDEX(Modulos!$B$5:$B${4+len(MOD)},MATCH(Showroom!$B$5:$B${rt-1},Modulos!$A$5:$A${4+len(MOD)},0)),"")="{filtro}")'
    return f+')'
def soma_ripa(colM,valor,colV):
    idxv=f'IFERROR(INDEX(Modulos!${colV}$5:${colV}${4+len(MOD)},MATCH(Showroom!$B$5:$B${rt-1},Modulos!$A$5:$A${4+len(MOD)},0)),0)'
    idx=f'IFERROR(INDEX(Modulos!${colM}$5:${colM}${4+len(MOD)},MATCH(Showroom!$B$5:$B${rt-1},Modulos!$A$5:$A${4+len(MOD)},0)),0)'
    return f'=SUMPRODUCT(Showroom!$C$5:$C${rt-1},{idx},--({idxv}={valor}))'
linhas=[('Painel 200×620',soma('O','200×620'),'checkout'),('Painel 305×620',soma('O','305×620'),'ajuste de canto do sul'),
        ('Painel 305×725',soma('O','305×725'),'paredes, pontas, araras'),('Painel 450×725',soma('O','450×725'),'ilhas'),
        ('Ripa largura 183',soma_ripa('Q',183,'C'),'checkout'),('Ripa largura 287',soma_ripa('Q',287,'C'),'paredes, pontas, araras'),('Ripa largura 415',soma_ripa('Q',415,'C'),'ilhas'),
        ('Ripa comprimento 617',soma_ripa('P',617,'D'),'checkout e ajuste'),('Ripa comprimento 717',soma_ripa('P',717,'D'),'todo o resto'),
        ('Ripa vertical 270',soma('R'),'baias de 247'),('Ripa vertical 346',soma('S'),'fundo, pontas, ilhas'),('Ripa vertical 513',soma('T'),'fundo, ilhas, araras'),
        ('Pé',soma('U'),''),('Trizeta',soma('L'),'4 por nível'),('Peça L',soma('M'),'araras'),('Tampa',soma('N'),''),('Cruzeta','=0','nenhuma')]
for i,(nome,f,onde) in enumerate(linhas):
    r=5+i; P_.cell(r,1,nome).font=fB; P_.cell(r,2,f).number_format=MM
    P_.cell(r,3,f'=B{r}*{kd(nome)}').number_format='0.0'; P_.cell(r,4,f'=B{r}*{kc(nome)}').number_format=BRL; P_.cell(r,5,onde).font=fn_
    for c_ in range(1,6): P_.cell(r,c_).border=box
r=5+len(linhas); P_.cell(r,1,'TOTAL material').font=fB
P_.cell(r,3,f'=SUM(C5:C{r-1})').number_format='0.0'; P_.cell(r,4,f'=SUM(D5:D{r-1})').number_format=BRL; P_.cell(r,4).font=fB
for c_ in range(1,6): P_.cell(r,c_).border=box
P_.cell(r+2,1,'Ancoragem: 1 ponto por módulo de parede (bucha S8 + parafuso 5×50 + arruela) e união poste a poste em 2 níveis entre vizinhos. Custo só de material; sem corte, montagem, embalagem e frete. Painel de fundo não contado (a parede do prédio é o fundo).').font=fn_
P_.cell(r+2,1).alignment=WR; P_.merge_cells(start_row=r+2,start_column=1,end_row=r+3,end_column=5)
widths(P_,[24,12,12,14,34])
wb.save(OUT)

# resumo em texto
tot=collections.Counter(); custo=0; kg=0; frente=0
for onde,mod,q,_ in PLANO:
    b=B[mod]; custo+=q*b['custo']; kg+=q*b['kg']; frente+=q*b['L']*b['n']/1000
    tot['Painel '+b['painel']]+=q*b['np']; tot['Ripa largura %d'%b['rl']]+=q*b['qbl']; tot['Ripa comprimento %d'%b['rc']]+=q*b['qbc']
    for a,n in b['vert'].items(): tot['Ripa vertical %d'%a]+=q*n
    tot['Trizeta']+=q*b['tz']; tot['Tampa']+=q*b['tp']; tot['Peça L']+=q*b['lp']; tot['Pé']+=q*b['pes']; tot['modulos']+=q
print('MODULOS'); 
for k,p,pil,cor,_ in MOD:
    b=B[k]; print('  %-13s %-8s %-22s %4.0f x %3.0f x %4.0f · %d prat · %5.1f kg · R$ %7.2f'%(k,p,'·'.join(map(str,pil))+(f'+L{cor}' if cor else ''),b['L'],b['P'],b['A'],b['n'],b['kg'],b['custo']))
print('\nPLANO'); 
for onde,mod,q,_ in PLANO: print('  %-44s %-13s x%2d  R$ %8.2f'%(onde,mod,q,q*B[mod]['custo']))
print('\nCOMPRAS')
for k in ['Painel 200×620','Painel 305×620','Painel 305×725','Painel 450×725','Ripa largura 183','Ripa largura 287','Ripa largura 415','Ripa comprimento 617','Ripa comprimento 717','Ripa vertical 270','Ripa vertical 346','Ripa vertical 513','Pé','Trizeta','Peça L','Tampa']:
    print('  %-22s %5d'%(k,tot[k]))
print('\nTOTAL: %d módulos · R$ %.2f · %.0f kg · %.1f m de frente · 0 cruzetas'%(tot['modulos'],custo,kg,frente))
