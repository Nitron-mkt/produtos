#!/usr/bin/env python3
"""Cruza a planta do showroom com a grade do Nitron Mob.

Responde duas coisas: quantos vaos de cada ripa cabem em cada parede (e com que
folga), e qual o BOM/custo do layout proposto em analise/12-showroom-piloto-pdv.html.

Gera dados/28-showroom-encaixe-paredes.csv e dados/29-showroom-layout-bom.csv.
"""
import csv, importlib.util, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('cad', RAIZ/'analise'/'pdv-caderno.py')
cad = importlib.util.module_from_spec(spec); spec.loader.exec_module(cad)

RIPA = {'PSC-01':315, 'PSC-02':415, 'PSC-03':595, 'PSC-04':717}
PAN  = {315:360, 415:450, 595:634, 717:754}
LARG = {200:('BLA-01-AC',200), 300:('BLA-03-AC',287), 460:('PSC-02',415)}

def bom(lpan, cref, N, pilha, coroa=None, ganch=False,
        fundo=False, deck=False, casinha=False):
    lref, lb = LARG[lpan]
    f = dict(nome='', slug='', bc=cref, bcv=RIPA[cref], bl=lref, blv=lb,
             pan=(lpan, PAN[RIPA[cref]]), vaos=(N,N,N), pilha=pilha, coroa=coroa,
             ganch=ganch, fundo=fundo, deck=deck, casinha=casinha, faces=1, lede='', cap='')
    b = cad.bom(f, N); b.update(lpan=lpan, cpan=PAN[RIPA[cref]], cref=cref, N=N)
    return b

# ------------------------------------------------- 28 · encaixe nas paredes
# Livre ja descontado porta, caixa, pilar e o avanco dos modulos vizinhos.
PAREDES = [
  ('Lateral sul',                13350, 'parede de impacto, pano corrido'),
  ('Norte, do pilar ao fundo',    6100, '6.600 brutos menos os 500 do modulo do fundo'),
  ('Fundo, entre os dois laterais',6873, '7.500 brutos menos 372 da sul e 285 da norte'),
  ('Folga caixa-pilar',            700, 'vaga de servico na planta'),
  ('Folga porta-caixa',            400, 'vaga de servico na planta'),
  ('Frente, se virar parede',     7530, 'face sem definicao'),
]
linhas = []
for nome, W, obs in PAREDES:
    for cref, cb in RIPA.items():
        melhor = None
        for N in range(1, 60):
            e = cad.ext_comp(cb, N)
            if e <= W: melhor = (N, e)
            else: break
        if not melhor:
            linhas.append([nome, W, cref, PAN[cb], cb, 0, '', '', '', obs]); continue
        N, e = melhor
        ec = e + 2*cad.SOL
        linhas.append([nome, W, cref, PAN[cb], cb, N, round(e,1), round(W-e,1),
                       round(100*(W-e)/W,2), 'sim' if ec <= W else 'nao'])
with open(RAIZ/'dados'/'28-showroom-encaixe-paredes.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['parede','livre_mm','ripa_comprimento','painel_mm','ripa_mm','vaos',
                'corrida_mm','folga_mm','folga_pct','aceita_coroa'])
    w.writerows(linhas)
print(f'28-showroom-encaixe-paredes.csv: {len(linhas)} linhas')

# ------------------------------------------------------- 29 · BOM do layout
LAYOUT = [
  (1,'Paredão sul','Lateral sul · parede de impacto',
   dict(lpan=300,cref='PSC-04',N=18,pilha=[270]*7,fundo=True),1),
  (2,'Paredão norte','Do pilar ao fundo',
   dict(lpan=200,cref='PSC-01',N=18,pilha=[270]*7,fundo=True),1),
  (3,'Paredão do fundo','Destino do percurso · pilha mista',
   dict(lpan=460,cref='PSC-03',N=11,pilha=[513,270,270,270,513],fundo=True),1),
  (4,'Torre de serviço','Folga porta-caixa',
   dict(lpan=200,cref='PSC-01',N=1,pilha=[270]*4),1),
  (5,'Checkout do caixa','Folga caixa-pilar · coroa + gancheira',
   dict(lpan=300,cref='PSC-02',N=1,pilha=[270]*4,coroa=270,ganch=True),1),
  (6,'Ponta de gôndola','Miolo, de frente para a porta · coroa 513',
   dict(lpan=300,cref='PSC-03',N=2,pilha=[270]*5,coroa=513,fundo=True,casinha=True),1),
  (7,'Ilha central','Miolo, fileira central · quatro faces',
   dict(lpan=460,cref='PSC-03',N=3,pilha=[270]*3,deck=True),3),
]
rows = []; tot = dict(custo=0, kg=0, frente=0, facings=0, area=0)
agg = {}
for idx, nome, onde, kw, q in LAYOUT:
    b = bom(**kw); npr = b['n']
    frente = b['L']*npr/1000*q; fac = (b['L']//120)*npr*q
    area = b['np']*b['lpan']*b['cpan']/1e6*q
    rows.append([idx, nome, onde, f"{b['lpan']}x{b['cpan']}", b['cref'], b['N'],
                 '·'.join(str(x) for x in kw['pilha']),
                 kw.get('coroa') or 0, 'sim' if kw.get('ganch') else 'nao',
                 b['L'], b['P'], b['A'], npr, round(b['kg'],1),
                 round(b['custo'],2), round(2*b['custo'],2), q,
                 b['tz'], b['lp'], b['cz'], b['tp'], b['ph'], b['np'],
                 round(frente,1), int(fac)])
    tot['custo'] += b['custo']*q; tot['kg'] += b['kg']*q
    tot['frente'] += frente; tot['facings'] += fac; tot['area'] += area
    for k in ('tz','lp','cz','tp','ph','np','qbc','qbl','pes'):
        agg[k] = agg.get(k,0) + b[k]*q
    for r,n in b['vert'].items():  agg[f'vertical_{r}'] = agg.get(f'vertical_{r}',0) + n*q
    for h,n in b['fundos'].items(): agg[f'fundo_{h}']  = agg.get(f'fundo_{h}',0) + n*q
with open(RAIZ/'dados'/'29-showroom-layout-bom.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['n','modulo','onde','painel','ripa_comprimento','vaos','pilha','coroa_mm',
                'gancheira','comprimento_mm','profundidade_mm','altura_mm','prateleiras',
                'peso_kg','custo_estimado','venda_direta_2x','qtd','trizetas','pecas_l',
                'cruzetas','tampas','porta_hastes','paineis','frente_linear_m','facings'])
    w.writerows(rows)
print(f'29-showroom-layout-bom.csv: {len(rows)} linhas')
print(f"  TOTAL  R$ {tot['custo']:,.2f} · {tot['kg']:,.1f} kg · {tot['frente']:.1f} m de frente · "
      f"{tot['facings']:.0f} facings · {tot['area']:.1f} m² de prateleira")
print('  peças:', ' · '.join(f'{k} {v}' for k,v in sorted(agg.items())))
