#!/usr/bin/env python3
"""Planograma do showroom — aloca 100% do catalogo nos modulos do PDV Nitron Mob.

Entradas (extraidas do Sankhya em 06/09/2026, ver docstring de cada bloco):
  - o catalogo ativo classificado por aptidao de gondola
  - metros lineares por linha e por profundidade minima exigida
  - faturamento de 12 M por linha, recorte de marca propria

Saidas:
  dados/33-catalogo-classificacao.csv
  dados/34-planograma-ambientes.csv
  dados/35-planograma-modulos.csv
"""
import csv, pathlib
RAIZ = pathlib.Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- geometria
NOZ, PEX, PANT, CONSOME = 73.08, 19.4, 15, 81.2
def prateleiras(pilha):
    """Altura da face de cada prateleira, do chao para cima (mm)."""
    z, out = PEX, []
    for i in range(len(pilha)+1):
        out.append(round(z + NOZ + PANT/2))
        if i < len(pilha): z = z + NOZ + (pilha[i]-CONSOME)
    return out
def zona(h):
    if h <= 800:  return 'chao'
    if h <= 1400: return 'maos'
    if h <= 1700: return 'olhos'
    return 'topo'

# ------------------------------------------------- 33 · catalogo classificado
CLASSES = [
 ('1 · sem cota no cadastro', 338, None, 'nao da para planogramar sem medir'),
 ('2 · cota suja (data no campo)', 15, None, 'LARGURA/ALTURA/ESPESSURA com serial de data'),
 ('3 · material de construcao (>1,20 m)', 111, 70.4, 'countertop, forro, meia-cana em teca'),
 ('4 · nao cabe nem na prateleira de 460', 26, 19.5, 'exige piso, cavalete ou expositor proprio'),
 ('5 · vai para gondola', 2589, 415.6, 'o catalogo planogramavel'),
]
with open(RAIZ/'dados'/'33-catalogo-classificacao.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['classe','skus','metros_de_lado','observacao']); w.writerows(CLASSES)

# ------------------------------------------------------ linhas -> ambientes
# metros = frente linear com o produto virado de lado (menor dimensao de planta)
# m285/m372/m500 = metros que exigem no minimo aquela profundidade
LINHAS = [
 # linha,                 skus, m285, m372, m500, skus_altos, m_altos, fat_mil, ambiente
 ('Linha Potes',           689, 62.9, 36.1,  0.3,  38, 10.5, 16540, 'COZINHA'),
 ('Linha Cozinha',         314, 17.3, 19.1,  6.3,   4,  1.3, 12761, 'COZINHA'),
 ('Linha Jarras',           71,  8.6,  0.0,  0.0,   6,  0.7,  2659, 'COZINHA'),
 ('Linha Micro-ondas',      44,  4.2,  3.7,  0.0,   0,  0.0,  1712, 'COZINHA'),
 ('Decor-Chef',             70,  1.7,  9.2,  0.6,   2,  0.6,   635, 'COZINHA'),
 ('Linha Geladeira',        27,  2.1,  2.0,  0.0,   0,  0.0,   461, 'COZINHA'),
 ('Teca Tabuas',            39,  1.0,  5.2,  2.5,   0,  0.0,   374, 'COZINHA'),
 ('Teca Cozinha',           15,  0.4,  2.9,  0.0,   0,  0.0,   208, 'COZINHA'),
 ('Decor-Confeitaria',       8,  0.7,  0.0,  0.0,   0,  0.0,   771, 'COZINHA'),
 ('POP',                     9,  0.9,  0.0,  0.0,   0,  0.0,    42, 'COZINHA'),
 ('Teca Petisqueira',        9,  0.8,  0.7,  0.0,   0,  0.0,    37, 'COZINHA'),
 ('Linha Organizacao',     560, 33.9, 55.8,  9.1,  51, 14.8, 22880, 'ORGANIZACAO'),
 ('Teca Organizacao',      211,  7.2, 16.2, 23.4,   3,  1.1,   779, 'ORGANIZACAO'),
 ('Linha Decor Util',       43,  0.5,  6.7,  0.0,   0,  0.0,    21, 'ORGANIZACAO'),
 ('Linha Lixeiras',        137, 10.3, 13.9,  2.1, 106, 20.5,  9577, 'BANHO E LAVANDERIA'),
 ('Linha Banheiro',         59,  5.8,  0.0,  0.0,  14,  1.4,  4222, 'BANHO E LAVANDERIA'),
 ('Linha Limpeza',          44,  3.0,  2.2,  1.9,  11,  3.0,  3797, 'BANHO E LAVANDERIA'),
 ('Linha ECO',              17,  0.6,  2.7,  0.0,   1,  0.2,   631, 'BANHO E LAVANDERIA'),
 ('Linha Frasqueiras',      70,  7.1,  4.6,  0.0,   0,  0.0,  6977, 'IMPULSO'),
 ('Linha Infantil',         62,  4.0,  3.9,  0.0,   5,  0.9,   492, 'IMPULSO'),
 ('Linha Coloratto',        32,  3.4,  0.0,  0.0,   0,  0.0,   311, 'IMPULSO'),
 ('Linha Realce',           46,  4.6,  0.6,  0.0,   0,  0.0,    58, 'IMPULSO'),
 ('Nitron Mob',             14,  0.0,  2.9,  0.0,   0,  0.0,     5, 'IMPULSO'),
]
AMB = {}
for nome,sk,a,b,c,ska,ma,fat,amb in LINHAS:
    d = AMB.setdefault(amb, dict(skus=0,m285=0.0,m372=0.0,m500=0.0,skus_alt=0,m_alt=0.0,fat=0,linhas=[]))
    d['skus']+=sk; d['m285']+=a; d['m372']+=b; d['m500']+=c
    d['skus_alt']+=ska; d['m_alt']+=ma; d['fat']+=fat; d['linhas'].append(nome)

with open(RAIZ/'dados'/'34-planograma-ambientes.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['ambiente','linhas','skus','metros_total','m_prof_285','m_prof_372','m_prof_500',
                'skus_altura_acima_247','metros_altura_acima_247','faturamento_12m_mil','fat_por_metro_mil'])
    for amb,d in sorted(AMB.items(), key=lambda kv:-kv[1]['fat']):
        mt = round(d['m285']+d['m372']+d['m500'],1)
        w.writerow([amb,' · '.join(d['linhas']),d['skus'],mt,round(d['m285'],1),round(d['m372'],1),
                    round(d['m500'],1),d['skus_alt'],round(d['m_alt'],1),d['fat'],
                    round(d['fat']/mt,1)])
print('AMBIENTES')
tot_m=tot_sk=tot_fat=0
for amb,d in sorted(AMB.items(), key=lambda kv:-kv[1]['fat']):
    mt=d['m285']+d['m372']+d['m500']; tot_m+=mt; tot_sk+=d['skus']; tot_fat+=d['fat']
    print(f"  {amb:20} {d['skus']:5} SKUs · {mt:6.1f} m · R$ {d['fat']:6} mil"
          f" · R$ {d['fat']/mt:6.1f} mil/m · alto {d['m_alt']:5.1f} m")
print(f"  {'TOTAL':20} {tot_sk:5} SKUs · {tot_m:6.1f} m · R$ {tot_fat} mil")

# --------------------------------------------------------- 35 · os modulos
# pilha do paredao do fundo revista: 7 prateleiras, baia alta embaixo,
# para por uma prateleira na zona dos olhos e fechar o deficit de metro linear
MODULOS = [
 # id, nome, corrida_mm, faces, pilha, prof, ambiente
 (1,'Paredao sul',            13290,1,[270]*7,               372,'COZINHA'),
 (2,'Paredao norte',           6054,1,[270]*7,               285,'ORGANIZACAO'),
 (3,'Paredao do fundo',        6788,1,[513,270,270,270,270,270],500,'BANHO E LAVANDERIA'),
 (4,'Parede de entrada',       6548,1,[270,270,270],          285,'ORGANIZACAO'),
 (10,'Gondola A, face corredor 1',4328,1,[270]*5,             500,'COZINHA'),
 (11,'Gondola A, face corredor 2',4328,1,[270]*5,             500,'COZINHA'),
 (12,'Gondola B, face corredor 2',4328,1,[270]*5,             500,'ORGANIZACAO'),
 (13,'Gondola B, face corredor 3',4328,1,[270]*5,             500,'ORGANIZACAO'),
 (20,'Ponta 1',                 892,1,[270]*5,                372,'COZINHA'),
 (21,'Ponta 2',                 892,1,[270]*5,                372,'COZINHA'),
 (22,'Ponta 3',                 892,1,[270]*5,                372,'ORGANIZACAO'),
 (23,'Ponta 4',                 892,1,[270]*5,                372,'ORGANIZACAO'),
 (40,'Ilha 1',                 1867,2,[270,270,270],          500,'COZINHA'),
 (41,'Ilha 2',                 1867,2,[270,270,270],          500,'ORGANIZACAO'),
 (50,'Corredor de checkout A', 1762,2,[270,270,270],          372,'IMPULSO'),
 (51,'Corredor de checkout B', 1762,2,[270,270,270],          372,'IMPULSO'),
 (30,'Modulo caixa-pilar',      457,1,[270,270,270],          372,'IMPULSO'),
 (31,'Torre de servico',        357,1,[270]*4,                285,'IMPULSO'),
]
linhas_csv=[]; oferta={}; zonas={}
for mid,nome,L,faces,pilha,prof,amb in MODULOS:
    for k,h in enumerate(prateleiras(pilha)):
        m = L/1000*faces
        z = zona(h)
        linhas_csv.append([mid,nome,k+1,h,z,prof,faces,round(m,2),amb])
        oferta[amb]=oferta.get(amb,0)+m
        zonas[z]=zonas.get(z,0)+m
with open(RAIZ/'dados'/'35-planograma-modulos.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['modulo_id','modulo','prateleira','altura_face_mm','zona','profundidade_mm',
                'faces','metros_lineares','ambiente'])
    w.writerows(linhas_csv)

print('\nOFERTA POR AMBIENTE (m lineares de prateleira)')
falta=0
for amb,d in sorted(AMB.items(), key=lambda kv:-kv[1]['fat']):
    dem=d['m285']+d['m372']+d['m500']; of=oferta.get(amb,0)
    falta+=max(0,dem-of)
    print(f"  {amb:20} demanda {dem:6.1f} · oferta {of:6.1f} · {'falta' if of<dem else 'sobra'} {abs(of-dem):5.1f} m")
print(f"  TOTAL oferta {sum(oferta.values()):.1f} m · demanda {tot_m:.1f} m · deficit {tot_m-sum(oferta.values()):.1f} m")
print('\nOFERTA POR ZONA DE ALTURA')
for z in ('chao','maos','olhos','topo'):
    print(f"  {z:6} {zonas.get(z,0):6.1f} m  ({100*zonas.get(z,0)/sum(zonas.values()):4.1f}%)")
print(f"\n33/34/35 escritos em dados/")
