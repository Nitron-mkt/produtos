#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O kit enxuto do Nitron Mob PDV: 1 painel, 3 ripas, 2 conectores, 2 modulos.
Gera dados/45-nitron-mob-kit.xlsx. Custos unitarios vem do caderno (pdv-caderno.py)."""
import importlib.util, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
RAIZ = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('cad', RAIZ/'analise'/'pdv-caderno.py')
cad = importlib.util.module_from_spec(spec); spec.loader.exec_module(cad)
OUT = RAIZ/'dados'/'45-nitron-mob-kit.xlsx'

F='Arial'; fb=Font(name=F,size=10); fB=Font(name=F,size=10,bold=True); fin=Font(name=F,size=10,color='0000FF')
fh=Font(name=F,size=10,bold=True,color='FFFFFF'); ft=Font(name=F,size=14,bold=True); fn=Font(name=F,size=9,italic=True,color='555555')
flink=Font(name=F,size=10,color='008000')
HEAD=PatternFill('solid',fgColor='1EA7AC'); YEL=PatternFill('solid',fgColor='FFFF00')
thin=Side(style='thin',color='BFBFBF'); box=Border(left=thin,right=thin,top=thin,bottom=thin)
C=Alignment(horizontal='center',vertical='center'); WR=Alignment(wrap_text=True,vertical='top')
BRL='"R$" #,##0.00'; KG='0.0" kg"'; MM='#,##0'
def header(ws,row,cols):
    for i,c in enumerate(cols):
        x=ws.cell(row,1+i,c); x.font=fh; x.fill=HEAD; x.alignment=C; x.border=box
def widths(ws,w):
    for i,x in enumerate(w,1): ws.column_dimensions[L(i)].width=x

# geometria e massa por peca, do caderno
GMM=cad.GMM; DENS=cad.DENS; PANT=cad.PANT; RSKG=cad.RSKG
ripa_kg = lambda mm: mm*GMM/1000                       # g/mm -> kg
pan_kg  = lambda l,c: l*c*PANT*DENS/1000                # mm^3 * g/mm^3 -> kg

wb=Workbook()
# ============================================================ Kit
K=wb.active; K.title='Kit'
K['A1']='Nitron Mob PDV — o kit enxuto'; K['A1'].font=ft
K['A2']='Seis peças. Um painel, três ripas, dois conectores. Todo módulo da loja sai daqui — sem cruzeta, sem peça L, sem porta-haste.'; K['A2'].font=fn
header(K,4,['Peça','Código / PI','Medida','Massa unit. (kg)','Custo unit. (R$)','Origem do custo'])
pecas=[
 ('Painel de prateleira','novo · pinus 15 mm','300 × 754 mm',pan_kg(300,754),pan_kg(300,754)*RSKG,'pinus a R$ %.2f/kg (caderno)'%RSKG),
 ('Ripa de largura','BLA-03-AC','287 mm',ripa_kg(287),ripa_kg(287)*RSKG,'PI existente'),
 ('Ripa de comprimento','PSC-04','717 mm',ripa_kg(717),ripa_kg(717)*RSKG,'PI existente'),
 ('Ripa vertical (baia)','BAL-02-AC','270 mm',ripa_kg(270),ripa_kg(270)*RSKG,'PI existente'),
 ('Pé','—','60 mm',ripa_kg(60),ripa_kg(60)*RSKG,'sobra de ripa'),
 ('Trizeta','PP · molde existente','61,61 × 83,23 × 73,08',cad.M_TZ/1000,cad.C_TZ,'caderno: %.1f g de PP'%cad.M_TZ),
 ('Tampa','PP · molde existente','—',cad.M_T/1000,cad.C_T,'caderno: %.1f g de PP'%cad.M_T),
]
for i,(a,b,c,kg,cu,org) in enumerate(pecas):
    r=5+i
    K.cell(r,1,a).font=fB; K.cell(r,2,b).font=fb; K.cell(r,3,c).font=fb
    x=K.cell(r,4,round(kg,4)); x.font=fin; x.number_format='0.0000'
    y=K.cell(r,5,round(cu,4)); y.font=fin; y.number_format='"R$" 0.0000'; y.fill=YEL
    K.cell(r,6,org).font=fn
    for k in range(1,7): K.cell(r,k).border=box
KIT_ROW={a:5+i for i,(a,*_) in enumerate(pecas)}
K.cell(13,1,'O que SAI do sistema e por quê').font=fB
fora=[('Cruzeta','4 injetadas contra centenas necessárias. Módulos de um vão encostados dispensam poste compartilhado — custa 7% a mais em madeira e trizeta e zera a dependência do molde.'),
      ('Painéis de 200 e 460','uma profundidade só. 372 mm cobre 82% dos SKUs do catálogo e 75% do faturamento em prateleira; o resto (lixeira, cesto, caixa grande) vai para o tampo do módulo baixo ou para o piso — onde já fica em qualquer loja.'),
      ('Ripas PSC-01/02/03','um vão só, o maior: menos postes, menos trizetas e menos painéis por metro. As paredes do showroom fecham com folga de 28 a 476 mm.'),
      ('Ripa PSA-05 (513)','uma baia só. Produto acima de 247 mm de altura não vai em prateleira — vai no tampo do módulo baixo (878 mm, sem teto).'),
      ('Peça L e porta-haste','sem coroa e sem gancheira nesta fase. A testeira sobe em haste comum fixada na tampa do poste.')]
for i,(a,b) in enumerate(fora):
    K.cell(14+i,1,a).font=fB; K.cell(14+i,2,b).font=fb; K.cell(14+i,2).alignment=WR
    K.merge_cells(start_row=14+i,start_column=2,end_row=14+i,end_column=6); K.row_dimensions[14+i].height=30
widths(K,[24,24,22,16,16,44])

# ============================================================ Modulos
M=wb.create_sheet('Modulos')
M['A1']='Os dois módulos'; M['A1'].font=ft
M['A2']='Um vão de PSC-04, painel 300 × 754, baias de 270. ALTO para parede, BAIXO para o miolo. Contagem e custo são fórmulas sobre a aba Kit.'; M['A2'].font=fn
header(M,4,['','ALTO · 270 × 6','BAIXO · 270 × 3','fórmula'])
def bom(pilha):
    f=dict(nome='',slug='',bc='PSC-04',bcv=717,bl='BLA-03-AC',blv=287,pan=(300,754),vaos=(1,1,1),pilha=pilha,coroa=None,
           ganch=False,fundo=False,deck=False,casinha=False,faces=1,lede='',cap='')
    return cad.bom(f,1)
A_,B_=bom([270]*6),bom([270]*3)
M['B5']=6; M['C5']=3; M['A5']='baias'; 
for c in ('B5','C5'): M[c].font=fin; M[c].fill=YEL
rows=[('prateleiras','=B5+1','baias + 1'),
      ('comprimento externo (mm)',f'=2*Parametros!$C$6+717-Parametros!$C$13','2×NOX + ripa − CONSOME'),
      ('profundidade externa (mm)',f'=287+2*(Parametros!$C$8-Parametros!$C$5)','ripa + 2×(NOY − ENC)'),
      ('altura externa (mm)',f'=Parametros!$C$11+(B5+1)*Parametros!$C$9+B5*(270-Parametros!$C$13)','PE + (baias+1)×NOZ + baias×(270 − CONSOME)'),
      ('face da última prateleira (mm)',f'=B9-Parametros!$C$9+Parametros!$C$9+Parametros!$C$12/2-Parametros!$C$9+Parametros!$C$9','topo do nó + painel/2'),
      ('trizetas','=4*B6','4 por nível'),
      ('tampas','=4','1 por poste'),
      ('painéis','=B6','1 por prateleira'),
      ('ripas de comprimento','=2*B6','frente e fundo por nível'),
      ('ripas de largura','=2*B6','2 por nível'),
      ('ripas verticais 270','=4*B5','4 por baia'),
      ('pés','=4','1 por poste'),
      ('massa (kg)',"=B11*Kit!$D$10+B12*Kit!$D$11+B13*Kit!$D$5+B14*Kit!$D$7+B15*Kit!$D$6+B16*Kit!$D$8+B17*Kit!$D$9",'Σ peças × massa'),
      ('custo material (R$)',"=B11*Kit!$E$10+B12*Kit!$E$11+B13*Kit!$E$5+B14*Kit!$E$7+B15*Kit!$E$6+B16*Kit!$E$8+B17*Kit!$E$9",'Σ peças × custo'),
      ('frente linear por módulo (m)','=B7*B6/1000','comprimento × prateleiras'),
      ('razão altura ÷ profundidade','=B9/B8','acima de 3 pede ancoragem na parede')]
for i,(rot,fA,exp) in enumerate(rows):
    r=6+i
    M.cell(r,1,rot).font=fB
    M.cell(r,2,fA).font=fb
    M.cell(r,3,fA.replace('B5','C5').replace('B6','C6').replace('B7','C7').replace('B8','C8').replace('B9','C9').replace('B10','C10').replace('B11','C11').replace('B12','C12').replace('B13','C13').replace('B14','C14').replace('B15','C15').replace('B16','C16').replace('B17','C17')).font=fb
    M.cell(r,4,exp).font=fn
    for k in range(1,5): M.cell(r,k).border=box
for r in (7,8,9,10): M.cell(r,2).number_format=MM; M.cell(r,3).number_format=MM
M.cell(18,2).number_format=KG; M.cell(18,3).number_format=KG
M.cell(19,2).number_format=BRL; M.cell(19,3).number_format=BRL
M.cell(20,2).number_format='0.00'; M.cell(20,3).number_format='0.00'
M.cell(21,2).number_format='0.00'; M.cell(21,3).number_format='0.00'
# corrigir a linha "face da ultima prateleira": simplificar
M['B10']='=B9-Parametros!$C$9+Parametros!$C$9-Parametros!$C$9+Parametros!$C$12/2+Parametros!$C$9'
M['B10']='=Parametros!$C$11+(B5+1)*Parametros!$C$9+B5*(270-Parametros!$C$13)+Parametros!$C$12/2'
M['C10']='=Parametros!$C$11+(C5+1)*Parametros!$C$9+C5*(270-Parametros!$C$13)+Parametros!$C$12/2'
M.cell(23,1,'Custo é só material (madeira a R$/kg do caderno + PP dos conectores). Não inclui corte, montagem, embalagem nem frete. Módulo contra parede não leva painel de fundo — a parede do prédio é o fundo.').font=fn
M.cell(23,1).alignment=WR; M.merge_cells('A23:D24')
widths(M,[30,16,16,40])

# ============================================================ Parametros (copia das cotas, para as formulas)
P=wb.create_sheet('Parametros')
P['A1']='Cotas do sistema (mesmas da planilha 44 — em amarelo as que faltam conferir com trena)'; P['A1'].font=fB
header(P,4,['Parâmetro','Símbolo','Valor (mm)'])
par=[('Encaixe','ENC',40.60,True),('Trizeta · comprimento','NOX',61.61,True),('Cruzeta · comprimento','NOXC',101.30,True),
     ('Trizeta · profundidade','NOY',83.23,True),('Trizeta · vertical','NOZ',73.08,True),('Peça L · sobra','NOL',21.92,True),
     ('Pé exposto','PE',19.40,True),('Espessura do painel','PANT',15,False),('Ripa consome','CONSOME','=2*C5',False)]
for i,(a,b,v,chk) in enumerate(par):
    r=5+i; P.cell(r,1,a).font=fb; P.cell(r,2,b).font=fB
    c=P.cell(r,3,v); c.font=fb if isinstance(v,str) else fin
    if chk: c.fill=YEL
    for k in range(1,4): P.cell(r,k).border=box
widths(P,[28,10,12])

# ============================================================ Showroom
S=wb.create_sheet('Showroom')
S['A1']='O showroom só com os dois módulos'; S['A1'].font=ft
S['A2']='Módulos encostados, poste ao lado de poste. Folga vai para o canto. Contagem e custo são fórmulas.'; S['A2'].font=fn
header(S,4,['Onde','Corrida livre (mm)','Módulo','Quantidade','Comprimento montado (mm)','Folga (mm)','Custo (R$)','Frente (m)'])
lin=[('Paredão sul',13350,'ALTO'),('Paredão norte',6100,'ALTO'),('Paredão do fundo',6873,'ALTO'),('Parede de entrada',6548,'ALTO'),
     ('Ilha 1 (2 × 2, costa a costa)',None,'BAIXO'),('Ilha 2 (2 × 2, costa a costa)',None,'BAIXO'),
     ('Corredor de checkout (2 lados × 3)',None,'BAIXO')]
qtd_fix={'Ilha 1 (2 × 2, costa a costa)':4,'Ilha 2 (2 × 2, costa a costa)':4,'Corredor de checkout (2 lados × 3)':6}
for i,(onde,livre,mod) in enumerate(lin):
    r=5+i; col='B' if mod=='ALTO' else 'C'
    S.cell(r,1,onde).font=fB; S.cell(r,3,mod).font=fb; S.cell(r,3).alignment=C
    if livre:
        S.cell(r,2,livre).font=fin
        S.cell(r,4,f'=INT(B{r}/Modulos!${col}$7)')
        S.cell(r,6,f'=B{r}-E{r}').number_format=MM
        S.cell(r,5,f'=D{r}*Modulos!${col}$7').number_format=MM
    else:
        S.cell(r,4,qtd_fix[onde]).font=fin
    S.cell(r,7,f'=D{r}*Modulos!${col}$19').number_format=BRL
    S.cell(r,8,f'=D{r}*Modulos!${col}$20').number_format='0.0'
    for k in range(1,9): S.cell(r,k).border=box
r=5+len(lin)
S.cell(r,1,'TOTAL').font=fB
S.cell(r,4,f'=SUM(D5:D{r-1})').font=fB
S.cell(r,7,f'=SUM(G5:G{r-1})').font=fB; S.cell(r,7).number_format=BRL
S.cell(r,8,f'=SUM(H5:H{r-1})').font=fB; S.cell(r,8).number_format='0.0'
for k in range(1,9): S.cell(r,k).border=box
S.cell(r+2,1,'Peças para comprar / injetar').font=fB
header(S,r+3,['Peça','Quantidade','Massa total (kg)','Custo total (R$)'])
alto_q=f'SUMIF($C$5:$C${r-1},"ALTO",$D$5:$D${r-1})'; baixo_q=f'SUMIF($C$5:$C${r-1},"BAIXO",$D$5:$D${r-1})'
comp=[('Trizeta',11,'Kit!$D$10','Kit!$E$10'),('Tampa',12,'Kit!$D$11','Kit!$E$11'),('Painel 300 × 754',13,'Kit!$D$5','Kit!$E$5'),
      ('Ripa PSC-04 (717)',14,'Kit!$D$7','Kit!$E$7'),('Ripa BLA-03-AC (287)',15,'Kit!$D$6','Kit!$E$6'),('Ripa BAL-02-AC (270)',16,'Kit!$D$8','Kit!$E$8'),('Pé',17,'Kit!$D$9','Kit!$E$9')]
for i,(nome,mrow,kg,cu) in enumerate(comp):
    rr=r+4+i
    S.cell(rr,1,nome).font=fB
    S.cell(rr,2,f'={alto_q}*Modulos!$B${mrow}+{baixo_q}*Modulos!$C${mrow}').number_format=MM
    S.cell(rr,3,f'=B{rr}*{kg}').number_format=KG
    S.cell(rr,4,f'=B{rr}*{cu}').number_format=BRL
    for k in range(1,5): S.cell(rr,k).border=box
rr=r+4+len(comp)
S.cell(rr,1,'Cruzetas').font=fB; S.cell(rr,2,0).font=fB; S.cell(rr,3,'← era 716 na spec anterior').font=fn
S.cell(rr+2,1,'Spec anterior (painel 460, postes compartilhados, com fundo): R$ 26.914 e 716 cruzetas só nas quatro paredes. Esta: veja o TOTAL acima, zero cruzetas, e cada módulo sai da caixa igual ao outro.').font=fn
S.cell(rr+2,1).alignment=WR; S.merge_cells(start_row=rr+2,start_column=1,end_row=rr+3,end_column=8)
widths(S,[34,16,10,12,22,11,16,11])

wb.move_sheet('Parametros',offset=2)
wb.save(OUT); print('gravado',OUT)
