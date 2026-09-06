#!/usr/bin/env python3
"""Layout de corredor para o showroom — Rev. 2 do piloto.

O miolo deixa de ser uma coisa so: a metade do fundo vira corredor (duas
gondolas dupla face), a metade da frente fica aberta (clareira de ilhas a
878 mm e um corredor de checkout baixo desembocando no caixa).
Cotas de corredor, altura e end cap conferidas contra o padrao de mercado.

Gera dados/30-showroom-corredor-layout.csv, dados/31-showroom-vs-mercado.csv
e dados/32-showroom-arranjos-miolo.csv.
"""
import csv, json, importlib.util, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('cad', RAIZ/'analise'/'pdv-caderno.py')
cad = importlib.util.module_from_spec(spec); spec.loader.exec_module(cad)

RIPA = {'PSC-01':315,'PSC-02':415,'PSC-03':595,'PSC-04':717}
PAN  = {315:360,415:450,595:634,717:754}
LARG = {200:('BLA-01-AC',200),300:('BLA-03-AC',287),460:('PSC-02',415)}

def bom(lpan,cref,N,pilha,coroa=None,ganch=False,fundo=False,deck=False,casinha=False):
    lref,lb = LARG[lpan]
    f = dict(nome='',slug='',bc=cref,bcv=RIPA[cref],bl=lref,blv=lb,
             pan=(lpan,PAN[RIPA[cref]]),vaos=(N,N,N),pilha=pilha,coroa=coroa,ganch=ganch,
             fundo=fundo,deck=deck,casinha=casinha,faces=1,lede='',cap='')
    b = cad.bom(f,N); b.update(lpan=lpan,cpan=PAN[RIPA[cref]],cref=cref,N=N,
                               pilha=pilha,coroa=coroa or 0)
    return b

# ---- o predio (mm, x = da frente para o fundo, y = da norte para a sul) ----
SALA = dict(C=13350, L=7520, H=3400,
            porta=(0,2000), caixa=(2400,5800), caixa_prof=600,
            pilar=(6500,6745), pilar_prof=670)

# ---- os modulos, com posicao ----
# zoneamento no eixo do comprimento (soma exata de 13.350 mm):
#   0-2400 descompressao · 2400-5000 clareira das ilhas + corredor de checkout
#   5000-6150 travessa · 6150-6522 ponta · 6522-10850 corridas dupla face
#   10850-11222 ponta · 11222-12850 travessa do fundo · 12850-13350 paredao do fundo
# eixo: 'x' = corrida ao longo do comprimento, 'y' = corrida ao longo da largura
M = []
def add(nid,nome,zona,x,y,eixo,b,faces=1,nota=''):
    L,P = b['L'], b['P']
    w,d = (L,P) if eixo=='x' else (P,L)
    M.append(dict(id=nid,nome=nome,zona=zona,x=x,y=y,w=w,d=d,h=b['A'],eixo=eixo,faces=faces,
                  painel=f"{b['lpan']}x{b['cpan']}",ripa=b['cref'],vaos=b['N'],
                  prat=b['n'],pilha=b['pilha'],coroa=b['coroa'],
                  kg=round(b['kg'],1),custo=round(b['custo'],2),
                  tz=b['tz'],lp=b['lp'],cz=b['cz'],tp=b['tp'],ph=b['ph'],np=b['np'],
                  fundo=bool(b['fundos']),nota=nota))
    return b

b_sul  = bom(300,'PSC-04',18,[270]*7,fundo=True)
b_nor  = bom(200,'PSC-01',18,[270]*7,fundo=True)
b_fun  = bom(460,'PSC-03',11,[513,270,270,270,513],fundo=True)
b_ent  = bom(200,'PSC-02',15,[270]*3,coroa=513)
b_face = bom(460,'PSC-03', 7,[270]*5)               # uma face da gondola dupla
b_facf = bom(460,'PSC-03', 7,[270]*5,fundo=True)    # so p/ contar o fundo compartilhado
b_pta  = bom(300,'PSC-02', 2,[270]*5,coroa=513,fundo=True,casinha=True)
b_ilha = bom(460,'PSC-03', 3,[270]*3,deck=True)
b_lane = bom(300,'PSC-02', 4,[270]*3,coroa=270,ganch=True)
b_gap  = bom(300,'PSC-02', 1,[270]*3,coroa=270,ganch=True)
b_tor  = bom(200,'PSC-01', 1,[270]*4)

add(1,'Paredão sul','Lateral sul · parede de impacto', 30, 7148,'x',b_sul)
add(2,'Paredão norte','Do pilar ao módulo do fundo', 6745, 0,'x',b_nor)
add(3,'Paredão do fundo','Destino do percurso · pilha mista', 12850, 285,'y',b_fun)
add(4,'Parede de entrada','Face da frente · baixa, com coroa', 0, 800,'y',b_ent,1,
    'altura de 1.383 mm para não fechar a visão do salão')
for k,y0 in enumerate([1906,4527]):
    add(10+k,'Gôndola dupla face '+'AB'[k],'Miolo · corrida central', 6522, y0,'x',b_face,2,
        'duas faces costa a costa, painel de fundo compartilhado')
for k,(x0,y0) in enumerate([(6150,1960),(10850,1960),(6150,4581),(10850,4581)]):
    add(20+k,'Ponta de gôndola '+str(k+1),'Cabeceira de corrida', x0, y0,'y',b_pta)
for k,y0 in enumerate([3700,5500]):
    add(40+k,'Ilha '+str(k+1),'Miolo · clareira, altura de balcão', 2700, y0,'x',b_ilha,2,
        'quatro faces, top deck, 878 mm — vê-se o salão por cima')
for k,x0 in enumerate([3150,4622]):
    add(50+k,'Corredor de checkout · lado '+'AB'[k],'Fila do caixa', x0, 700,'y',b_lane,2,
        'fila de 1.100 mm entre os dois; coroa com gancheira em porta-hastes')
add(30,'Módulo caixa–pilar','Folga caixa–pilar', 5900, 0,'x',b_gap)
add(31,'Torre de serviço','Folga porta–caixa', 2015, 0,'x',b_tor)

# gondola dupla face = 2 faces + 1 jogo de fundo
N_FUNDO = sum(b_facf['fundos'].values())
KG_FUNDO = N_FUNDO*634*247*15*0.556/1e6/1000
CUSTO_FUNDO = N_FUNDO*634*247*15*(0.556/1000)/1000*19.03

tot = dict(custo=0,kg=0,frente=0,facings=0)
agg = {}
for mm in M:
    q = 2 if mm['nome'].startswith('Gôndola') else 1   # cada gondola = 2 faces montadas
    tot['custo'] += mm['custo']*q; tot['kg'] += mm['kg']*q
    L = mm['w'] if mm['eixo']=='x' else mm['d']
    tot['frente'] += L*mm['prat']/1000*mm['faces']
    tot['facings'] += (L//120)*mm['prat']*mm['faces']
    for k in ('tz','lp','cz','tp','ph','np'): agg[k] = agg.get(k,0)+mm[k]*q
tot['custo'] += 2*CUSTO_FUNDO; tot['kg'] += 2*KG_FUNDO
agg['np'] += 2*N_FUNDO

print(f"ESTRUTURAS: {len(M)} posicoes ({len(M)+2} montagens)   "
      f"TOTAL R$ {tot['custo']:,.2f} · {tot['kg']:,.1f} kg · "
      f"{tot['frente']:.1f} m de frente · {tot['facings']:.0f} facings · "
      f"{tot['frente']/(tot['custo']/1000):.2f} m/mil")
print('pecas:', ' · '.join(f'{k} {v}' for k,v in sorted(agg.items())))
print(f"(gondola dupla face: {N_FUNDO} paineis de fundo compartilhados por par)")

with open(RAIZ/'dados'/'30-showroom-corredor-layout.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['id','modulo','zona','x_mm','y_mm','largura_mm','profundidade_mm','altura_mm',
                'eixo','faces_de_venda','painel','ripa','vaos','prateleiras','coroa_mm','peso_kg',
                'custo','trizetas','pecas_l','cruzetas','tampas','porta_hastes','paineis','nota'])
    for mm in M:
        w.writerow([mm['id'],mm['nome'],mm['zona'],mm['x'],mm['y'],mm['w'],mm['d'],mm['h'],
                    mm['eixo'],mm['faces'],mm['painel'],mm['ripa'],mm['vaos'],mm['prat'],
                    mm['coroa'],mm['kg'],mm['custo'],mm['tz'],mm['lp'],mm['cz'],mm['tp'],
                    mm['ph'],mm['np'],mm['nota']])
print('30-showroom-corredor-layout.csv escrito')

# ------------------------------------------------ 31 · contra o mercado
REF = [
 ('Corredor mais comum','42–48 in',1067,1219,'corredor central do showroom',1621,'acima da faixa: sobra folga'),
 ('Corredor de supermercado, 2 carrinhos','240–300 cm',2400,3000,'corredor central',1621,'abaixo: showroom não usa carrinho'),
 ('Gôndola, seção métrica','600–1000 mm',600,1000,'vão PSC-03 / PSC-02 2 vãos',637,'dentro'),
 ('Gôndola, prateleira superior','200–400 mm',200,400,'profundidade 285 e 372',285,'dentro'),
 ('Gôndola, prateleira base','300–500 mm',300,500,'profundidade 372 e 500',500,'no topo da faixa'),
 ('Gôndola dupla face, profundidade total','32–48 in',813,1219,'2 × 500 costa a costa',1000,'no meio da faixa'),
 ('Altura de gôndola central','54 in',1372,1372,'6 prateleiras',1402,'+2,2%'),
 ('Altura de gôndola de parede','72 in',1829,1829,'8 prateleiras',1926,'+5,3%'),
 ('End cap, largura','36 in',914,914,'ponta 2 vãos PSC-02',892,'−2,4%'),
 ('End cap, altura','54–72 in',1372,1829,'ponta 6 prat + coroa 513',1907,'+4,3% sobre 72 in'),
 ('Corredor de checkout, largura da fila','36 in (mínimo acessível)',914,914,'entre os dois módulos baixos',1100,'+20% sobre o mínimo'),
 ('Móvel de checkout, altura','48–54 in',1219,1372,'4 prateleiras + coroa 270',1140,'abaixo: o operador vê a fila'),
 ('Zona de descompressão','5–15 ft',1524,4572,'da porta ao primeiro módulo',2400,'dentro'),
]
with open(RAIZ/'dados'/'31-showroom-vs-mercado.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['medida_de_mercado','referencia','min_mm','max_mm','equivalente_nitron','valor_mm','veredito'])
    for nome,rot,a,b,eq,v,ver in REF: w.writerow([nome,rot,a,b,eq,v,ver])
print('31-showroom-vs-mercado.csv escrito')

# ------------------------------------------------ 32 · os tres arranjos de miolo
ARRANJOS = [
 ('A · tres ilhas soltas',        249.7, 2043, 23465.71,  726),
 ('B · corredor puro, 2 x 8,13 m',442.3, 3633, 45350.66, 1340),
 ('C · misto (adotado)',          408.6, 3350, 38234.50, 1240),
]
with open(RAIZ/'dados'/'32-showroom-arranjos-miolo.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['arranjo','frente_linear_m','facings','material_brl','cruzetas','frente_por_mil_brl'])
    for nome,fr,fa,cu,cz in ARRANJOS:
        w.writerow([nome,fr,fa,cu,cz,round(fr/(cu/1000),2)])
print('32-showroom-arranjos-miolo.csv escrito')
