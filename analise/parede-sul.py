#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Paredao sul, modulo a modulo, com o kit flexivel (N = 1, zero cruzeta).
Composicao, alocacao da cozinha por modulo e prateleira, BOM e ancoragem.
Gera dados/47-parede-sul-modulos.csv, dados/48-parede-sul-alocacao.csv, dados/49-parede-sul-bom.csv."""
import csv, collections, importlib.util, pathlib, json, math
RAIZ=pathlib.Path(__file__).resolve().parent.parent
def load(n,f):
    s=importlib.util.spec_from_file_location(n,RAIZ/'analise'/f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
pc=load('pc','planograma-catalogo.py'); cad=load('cad','pdv-caderno.py')

LIVRE=13350; PROF=372; PILHA=[270]*6
L754=round(cad.ext_comp(717,1),1); L450=round(cad.ext_comp(415,1),1)
FACES=pc.prateleiras(PILHA)                      # 100 362 624 886 1148 1409 1671
ORDEM_Z=['olhos','maos','chao']
# ---------------------------------------------------------------- composicao
best=None
for a in range(0,20):
    for b in range(0,8):
        t=a*L754+b*L450
        if t<=LIVRE and (best is None or LIVRE-t<best[0]): best=(LIVRE-t,a,b)
folga,nA,nB=best
seq=['450']*(nB//2)+['754']*nA+['450']*(nB-nB//2)
mods=[]; x=folga/2
for i,t in enumerate(seq):
    w=L754 if t=='754' else L450; pan=754 if t=='754' else 450
    mods.append(dict(n=i+1,tipo=f'300×{pan}-1-alto',painel=pan,x0=round(x),x1=round(x+w),largura=round(w),util=pan)); x+=w
# ---------------------------------------------------------------- os SKUs
skus=pc.ler()
for s in skus:
    s['classe'],s['frente'],s['prof']=pc.classificar(s); s['baia']=pc.baia(s['alt'])
coz=[s for s in skus if s['classe']=='gondola' and s['ambiente']=='COZINHA']
cabe=[s for s in coz if s['prof']<=PROF and s['baia']==270]
fora=[s for s in coz if s not in cabe]
# ordem de percurso: da entrada (x=0) para o fundo. Gadget e kit na frente, potes como destino, teca no final.
FLUXO=['DECOR','POP','GELADEIRA','MICRO-ONDAS','JARRAS','COZINHA','POTES','TECA']
dem=collections.Counter()
for s in cabe: dem[s['categoria']]+=s['frente']
tot=sum(dem.values())
# modulos por categoria, proporcional a demanda (minimo 1), fechando em len(mods)
alvo={c: dem[c]/tot*len(mods) for c in FLUXO}
nmod={c: max(1,int(alvo[c])) for c in FLUXO}
while sum(nmod.values())<len(mods):
    c=max(FLUXO,key=lambda k: alvo[k]-nmod[k]); nmod[c]+=1
while sum(nmod.values())>len(mods):
    c=max((k for k in FLUXO if nmod[k]>1),key=lambda k: nmod[k]-alvo[k]); nmod[c]-=1
# a ultima categoria fica com as duas pontas de 450 do fim: 2 x 3,1 m para 3,3 m de demanda
if nmod['TECA']<2: nmod['TECA']=2; nmod['POTES']-=1
faixa={}; i=0
for c in FLUXO:
    faixa[c]=list(range(i,i+nmod[c])); i+=nmod[c]
    for k in faixa[c]: mods[k]['categoria']=c
# ---------------------------------------------------------------- alocacao
# prateleiras: (modulo, nivel) com largura util = painel. Blocos = cores da mesma referencia-base.
prat={}
for m in mods:
    for k,h in enumerate(FACES):
        prat[(m['n'],k+1)]=dict(mod=m['n'],nivel=k+1,h=h,zona=pc.zona(h),cap=m['util'],livre=m['util'],itens=[])
blocos=collections.defaultdict(list)
for s in cabe: blocos[(s['categoria'],s['ref'].split('.')[0])].append(s)
# bloco mais largo que a prateleira mais larga (ex.: 9 cores) e partido em pedacos que cabem
MAXW=max(m['util'] for m in mods)
for k in list(blocos):
    it=sorted(blocos[k],key=lambda x:-x['fat'])
    if sum(x['frente'] for x in it)>MAXW:
        del blocos[k]; parte=[]; larg=0; j=0
        for x in it:
            if parte and larg+x['frente']>MAXW:
                blocos[(k[0],f'{k[1]}/{j}')]=parte; j+=1; parte=[]; larg=0
            parte.append(x); larg+=x['frente']
        if parte: blocos[(k[0],f'{k[1]}/{j}')]=parte
spill=[]
def ordem_prat(mod_idx):
    out=[]
    for z in ORDEM_Z:
        for k,h in sorted(enumerate(FACES),key=lambda kh:-kh[1]):
            if pc.zona(h)!=z: continue
            for mi in mod_idx: out.append(prat[(mods[mi]['n'],k+1)])
    return out
for c in FLUXO:
    bl=sorted([(k,v) for k,v in blocos.items() if k[0]==c],key=lambda kv:-sum(x['fat'] for x in kv[1]))
    ps=ordem_prat(faixa[c])
    for (cat,base),itens in bl:
        larg=sum(x['frente'] for x in itens)
        alvo_p=next((p for p in ps if p['livre']>=larg),None)
        if alvo_p is None: spill.append((cat,base,itens)); continue
        alvo_p['livre']-=larg
        for x in itens:
            x['mod']=alvo_p['mod']; x['nivel']=alvo_p['nivel']; x['h']=alvo_p['h']; x['zona']=alvo_p['zona']; alvo_p['itens'].append(x)
# spill: qualquer prateleira da parede
for cat,base,itens in list(spill):
    larg=sum(x['frente'] for x in itens)
    ps=ordem_prat(range(len(mods)))
    alvo_p=next((p for p in ps if p['livre']>=larg),None)
    if alvo_p:
        alvo_p['livre']-=larg
        for x in itens:
            x['mod']=alvo_p['mod']; x['nivel']=alvo_p['nivel']; x['h']=alvo_p['h']; x['zona']=alvo_p['zona']; alvo_p['itens'].append(x)
        spill.remove((cat,base,itens))
aloc=[s for s in cabe if s.get('mod')]
# ---------------------------------------------------------------- BOM e ancoragem
def bom(pan):
    cref='PSC-04' if pan==754 else 'PSC-02'
    f=dict(nome='',slug='',bc=cref,bcv=717 if pan==754 else 415,bl='BLA-03-AC',blv=287,pan=(300,pan),vaos=(1,1,1),pilha=PILHA,coroa=None,
           ganch=False,fundo=False,deck=False,casinha=False,faces=1,lede='',cap='')
    return cad.bom(f,1)
bA,bB=bom(754),bom(450)
BOM=[('Módulo 300×754-1-alto','un',nA,bA['kg'],bA['custo']),('Módulo 300×450-1-alto','un',nB,bB['kg'],bB['custo']),
     ('Trizeta','un',nA*bA['tz']+nB*bB['tz'],None,None),('Tampa','un',nA*bA['tp']+nB*bB['tp'],None,None),
     ('Painel 300×754','un',nA*bA['np'],None,None),('Painel 300×450','un',nB*bB['np'],None,None),
     ('Ripa PSC-04 (717)','un',nA*bA['qbc'],None,None),('Ripa PSC-02 (415)','un',nB*bB['qbc'],None,None),
     ('Ripa BLA-03-AC (287)','un',nA*bA['qbl']+nB*bB['qbl'],None,None),('Ripa BAL-02-AC (270)','un',nA*bA['vert'][270]+nB*bB['vert'][270],None,None),
     ('Pé','un',nA*bA['pes']+nB*bB['pes'],None,None),('Cruzeta','un',0,None,None),
     ('Bucha S8 + parafuso 5×50 + arruela (ancoragem)','un',len(mods),None,len(mods)*1.20),
     ('Parafuso de união entre postes vizinhos (2 níveis)','un',2*(len(mods)-1),None,2*(len(mods)-1)*0.35),
     ('Testeira 754 × 200','un',nA,None,None),('Testeira 450 × 200','un',nB,None,None),('Faixa de prateleira','un',len(mods)*len(FACES),None,None)]
# ---------------------------------------------------------------- saida
D=RAIZ/'dados'
with open(D/'47-parede-sul-modulos.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['modulo','tipo','painel_mm','x_inicio_mm','x_fim_mm','largura_ext_mm','categoria','prateleiras','skus','frente_ocupada_mm','frente_util_mm','ocupacao','faturamento_12m'])
    for m in mods:
        it=[s for s in aloc if s['mod']==m['n']]
        oc=sum(s['frente'] for s in it); cap=m['util']*len(FACES)
        w.writerow([m['n'],m['tipo'],m['painel'],m['x0'],m['x1'],m['largura'],m['categoria'],len(FACES),len(it),round(oc),cap,round(oc/cap,3),round(sum(s['fat'] for s in it),2)])
with open(D/'48-parede-sul-alocacao.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['modulo','prateleira','altura_face_mm','zona','ordem_na_prateleira','referencia','nome','categoria','frente_mm','profundidade_min_mm','faturamento_12m','clientes'])
    for (mn,k),p in sorted(prat.items()):
        for j,s in enumerate(sorted(p['itens'],key=lambda s:(s['ref'].split('.')[0],-s['fat']))):
            w.writerow([mn,k,p['h'],p['zona'],j+1,s['ref'],s['nome'],s['categoria'],round(s['frente']),s['prof'],round(s['fat'],2),s['clientes']])
with open(D/'49-parede-sul-bom.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['item','unidade','quantidade','massa_kg','custo_total_rs'])
    for it,u,q,kg,cu in BOM: w.writerow([it,u,q,round(kg*q,1) if kg else '',round(cu*q,2) if (cu and it.startswith('Módulo')) else (round(cu,2) if cu else '')])
resumo=dict(folga=folga,nA=nA,nB=nB,mods=mods,faces=FACES,
            cozinha=len(coz),cabe=len(cabe),fora=len(fora),fora_prof=sum(1 for s in fora if s['prof']>PROF),fora_alt=sum(1 for s in fora if s['baia']!=270),
            fat_cabe=sum(s['fat'] for s in cabe),fat_fora=sum(s['fat'] for s in fora),m_cabe=sum(s['frente'] for s in cabe)/1000,m_fora=sum(s['frente'] for s in fora)/1000,
            oferta=sum(m['util'] for m in mods)*len(FACES)/1000,alocados=len(aloc),spill=len(spill),
            nmod=nmod,dem={c:round(dem[c]/1000,1) for c in FLUXO},
            zonas={z:dict(skus=sum(1 for s in aloc if s['zona']==z),fat=sum(s['fat'] for s in aloc if s['zona']==z)) for z in ORDEM_Z},
            custo=nA*bA['custo']+nB*bB['custo'],kg=nA*bA['kg']+nB*bB['kg'],triz=nA*bA['tz']+nB*bB['tz'],paineis=nA*bA['np']+nB*bB['np'],
            prat_vazias=sum(1 for p in prat.values() if not p['itens']),prat_total=len(prat),
            fora_lista=[(s['ref'],s['nome'],s['categoria'],'prof %d'%s['prof'] if s['prof']>PROF else 'alt %d'%round(s['alt']),s['fat']) for s in sorted(fora,key=lambda s:-s['fat'])])
json.dump(resumo,open('/tmp/claude-0/-home-user-produtos/a90e79dc-9d6b-5cf3-8b87-00e7e5301ee0/scratchpad/sul-resumo.json','w'),ensure_ascii=False,default=float)
print('composicao: %d x 754 + %d x 450 · folga %.0f mm · oferta %.1f m em %d prateleiras'%(nA,nB,folga,resumo['oferta'],len(prat)))
print('cozinha %d · cabem %d (%.1f m · R$ %.2f M) · fora %d (%d por profundidade, %d por altura)'%(len(coz),len(cabe),resumo['m_cabe'],resumo['fat_cabe']/1e6,len(fora),resumo['fora_prof'],resumo['fora_alt']))
print('modulos por categoria:',{c:nmod[c] for c in FLUXO})
print('alocados %d de %d · sem lugar %d · prateleiras vazias %d de %d'%(len(aloc),len(cabe),len(spill),resumo['prat_vazias'],len(prat)))
for z in ORDEM_Z: print('  %-6s %3d SKUs · R$ %5.2f M (%.0f%%)'%(z,resumo['zonas'][z]['skus'],resumo['zonas'][z]['fat']/1e6,100*resumo['zonas'][z]['fat']/resumo['fat_cabe']))
print('BOM: R$ %.2f · %.0f kg · %d trizetas · %d paineis · 0 cruzetas · %d ancoragens'%(resumo['custo'],resumo['kg'],resumo['triz'],resumo['paineis'],len(mods)))
