#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Projeto do showroom com a spec de 10/09/2026: 58 modulos posicionados na sala,
o catalogo alocado modulo a modulo (paredes, ilhas, pontas, checkout) e a lista de compras.
Gera dados/55-projeto-modulos.csv, 56-projeto-alocacao.csv, 57-projeto-compras.csv e o JSON do documento."""
import csv, collections, importlib.util, pathlib, json
RAIZ=pathlib.Path(__file__).resolve().parent.parent
def load(n,f):
    s=importlib.util.spec_from_file_location(n,RAIZ/'analise'/f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
pc=load('pc','planograma-catalogo.py'); cad=load('cad','pdv-caderno.py')

# ------------------------------------------------------------------ a sala
SALA=dict(C=13350,L=7520,H=3400,porta=(0,2400),porta_parede='norte',porta_folhas=2,porta_giro=1200,porta_tipo='duas folhas na parede norte, do canto ao caixa, abrindo para dentro',caixa=(2400,5800,600),pilar=(6500,6745,670))
TESTEIRA=1900
L759=cad.ext_comp(717,1); L659=cad.ext_comp(617,1)
PAINEIS={'200×620':(200,620,183,617),'305×620':(305,620,287,617),'305×725':(305,725,287,717),'450×725':(450,725,415,717)}
JANELA=1100  # peitoril da janela do norte: nada de estrutura acima disso
TIPOS={  # tipo: painel, pilha, coroa, vao do topo (None = teto e a base da testeira; numero = topo aberto com esse vao)
 'parede-725':('305×725',[270]*6,None,None),'parede-620':('305×620',[270]*6,None,None),
 'parede-fundo':('305×725',[513,346,346,270],None,None),'fundo-620':('305×620',[513,346,346,270],None,None),
 'parede-baixa':('305×725',[346,346,270],None,350),   # norte, sob a janela: 1.030 de altura, produto baixo no topo
 'gondola':('305×725',[513,346,346,270],None,700),     # corredor de PDV: dupla-face costa a costa, topo aberto
 'ponta':('305×725',[346,346,270],None,700),'ilha':('450×725',[513,346],None,700),
 'checkout':('200×620',[270]*3,None,700),'arara':('305×725',[513,513],513,None)}
def geo(tipo):
    pan,pil,cor,topo=TIPOS[tipo]; lp,cp,rl,rc=PAINEIS[pan]
    faces=pc.prateleiras(pil) if not cor else []
    vao=[(pil[k]-pc.CONSOME+pc.NOZ-pc.PANT) if k<len(pil) else ((topo if topo is not None else TESTEIRA-faces[k]-pc.PANT/2)) for k in range(len(faces))]
    return dict(painel=pan,pilha=pil,coroa=cor,L=cad.ext_comp(rc,1),P=cad.ext_prof(rl),A=cad.altura(pil,cor),faces=faces,vao=vao,util=cp,prof_util=cad.ext_prof(rl))
def bom(tipo):
    pan,pil,cor,_=TIPOS[tipo]; lp,cp,rl,rc=PAINEIS[pan]
    f=dict(nome='',slug='',bc={617:'PST02',717:'PSC04'}[rc],bcv=rc,bl={183:'BAL01AC',287:'BLA03AC',415:'PSC02'}[rl],blv=rl,pan=(lp,cp),vaos=(1,1,1),pilha=pil,coroa=cor,ganch=False,fundo=False,deck=False,casinha=False,faces=1,lede='',cap='')
    return cad.bom(f,1)
G={t:geo(t) for t in TIPOS}; B={t:bom(t) for t in TIPOS}

# ------------------------------------------------------------------ as corridas na planta (mm; x = comprimento, y = largura; porta em x=0, norte em y=0)
# Uma corrida = N vaos com postes compartilhados (cruzeta no meio, trizeta nas pontas). Cada vao continua sendo um "modulo" para a alocacao.
# A ripa entra ENC = 40,60 em cada no (o "4 cm" da fabrica); consome 81,20 por ripa. No de ponta 61,61; no compartilhado (cruzeta) 101,30.
ENC,NOX,NOXC=cad.ENC,cad.NOX,cad.NOXC
NMAX=3  # corrida padrao: ate 3 vaos (logistica e montagem)
M=[]; RUNS=[]
def run(area,tipos,x,y,eixo,amb,nota=''):
    tipos=list(tipos); N=len(tipos); rid=len(RUNS)+1
    ripas=[PAINEIS[TIPOS[t][0]][3] for t in tipos]
    L=2*NOX+(N-1)*NOXC+sum(r-cad.CONSOME for r in ripas); P=G[tipos[0]]['P']
    RUNS.append(dict(id=rid,area=area,tipos=tipos,N=N,x=round(x),y=round(y),eixo=eixo,L=round(L),P=round(P),A=G[tipos[0]]['A'],ambiente=amb,nota=nota,mods=[]))
    pos=0
    for k,(t,r) in enumerate(zip(tipos,ripas)):
        w=(r-cad.CONSOME)+(NOX if k==0 else NOXC/2)+(NOX if k==N-1 else NOXC/2)
        mx,my=(x+pos,y) if eixo=='x' else (x,y+pos)
        M.append(dict(n=len(M)+1,area=area,tipo=t,x=round(mx),y=round(my),w=round(w if eixo=='x' else P),d=round(P if eixo=='x' else w),eixo=eixo,ambiente=amb,nota=nota,
                      run=rid,pos=('unico' if N==1 else 'ini' if k==0 else 'fim' if k==N-1 else 'meio')))
        RUNS[-1]['mods'].append(len(M)); pos+=w
    return (x+L,y) if eixo=='x' else (x,y+L)
def corridas(tipos,nmax=NMAX):
    """divide uma fila de vaos em corridas de ate nmax, sem deixar corrida de 1 se der para evitar"""
    out=[]; t=list(tipos)
    while t:
        k=min(nmax,len(t))
        if len(t)-k==1 and k>1: k-=1
        out.append(t[:k]); t=t[k:]
    return out
def fila(area,tipos,x,y,eixo,amb,nota=''):
    for c in corridas(tipos): x,y=run(area,c,x,y,eixo,amb,nota)
    return x,y
# comprimento das filas com postes compartilhados
def L_fila(tipos): return sum(2*NOX+(len(c)-1)*NOXC+sum(PAINEIS[TIPOS[t][0]][3]-cad.CONSOME for t in c) for c in corridas(tipos))
# sul: 2x620 + 14x725 + 2x620, folga dividida nos cantos
SUL=['parede-620']*2+['parede-725']*14+['parede-620']*2; fS=SALA['C']-L_fila(SUL)
fila('Paredão sul',SUL,fS/2,SALA['L']-372,'x','COZINHA')
# norte: do pilar ao modulo do fundo — baixo (1.030), a janela comeca em 1.100
fila('Paredão norte',['parede-baixa']*8,6745,0,'x','ORGANIZACAO','sob a janela')
# fundo: entre norte e sul; o 659 no canto do norte
fila('Paredão do fundo',['fundo-620']+['parede-fundo']*8,SALA['C']-372,372,'y','BANHO E LAVANDERIA')
# entrada: a porta (2 folhas, 2.400) esta na parede NORTE, do canto ao caixa, abrindo para dentro. A folha do canto, aberta, deita sobre a
# parede oeste ate y = 1.200; a parede da esquerda vai de prateleira dali ao canto do sul (7.148): 8 vaos em corridas 3 + 3 + 2 = 5.762 em 5.948 livres
ENT=['parede-725']*6+['parede-620']*2
fila('Parede de entrada',ENT,0,SALA['L']-372-L_fila(ENT),'y','FRASQUEIRAS E INFANTIL')
assert SALA['L']-372-L_fila(ENT)>=SALA['porta_giro']
# ilhas: 2 vaos de 450x725 em corrida (cruzeta no meio), duas faces costa a costa, ponta em cada cabeceira
LI=L_fila(['ilha']*2)
# a terceira ilha ocupa a praca entre a parede de entrada e o checkout, alinhada com a ilha 2 (corredores de 1.394 para os dois lados)
for k,(ix,iy) in enumerate(((5400,1900),(5400,4300),(1766,4300))):
    run(f'Ilha {k+1}',['ponta'],ix,iy+(1000-L759)/2,'y','MIOLO','cabeceira oeste')
    run(f'Ilha {k+1}',['ilha']*2,ix+372,iy,'x','MIOLO','face norte'); run(f'Ilha {k+1}',['ilha']*2,ix+372,iy+500,'x','MIOLO','face sul')
    run(f'Ilha {k+1}',['ponta'],ix+372+LI,iy+(1000-L759)/2,'y','MIOLO','cabeceira leste')
# corredor de PDV: duas gondolas dupla-face (corrida de 3 vaos costa a costa, 744 de fundo) com ponta em cada cabeceira, ao longo de y
LG=L_fila(['gondola']*3)
for k,rx in enumerate((8700,10844)):
    nome='Gôndola '+'AB'[k]; y0=2250
    run(nome,['ponta'],rx+372-L759/2,y0,'x','CORREDOR','cabeceira norte'); y=y0+372
    run(nome,['gondola']*3,rx,y,'y','CORREDOR','face oeste'); run(nome,['gondola']*3,rx+372,y,'y','CORREDOR','face leste')
    run(nome,['ponta'],rx+372-L759/2,y+LG,'x','CORREDOR','cabeceira sul')
# checkout: duas fileiras (corrida de 3) ao longo de y desembocando no caixa (caixa em y 0-600, x 2400-5800)
for cx,lado in ((2600,'lado oeste'),(4000,'lado leste')):
    run('Corredor de checkout',['checkout']*3,cx,800,'y','CHECKOUT',lado)
assert len(M)==83, len(M)
# ------------------------------------------------------------------ BOM por corrida (generaliza cad.bom para vaos de ripa mista)
def bom_run(r):
    tipos=r['tipos']; N=len(tipos); pan,pil,cor,_=TIPOS[tipos[0]]
    n=len(pil)+1; cor_=bool(cor)
    tz=4*n; lp=4 if cor_ else 0; cz=2*(N-1)*(n+(1 if cor_ else 0)); tp=2*(N+1); pes=2*(N+1)
    qbc=collections.Counter(); qbl=collections.Counter(); np_=collections.Counter(); mad=0; madp=0
    rl=PAINEIS[pan][2]; qbl[rl]=(N+1)*n; mad+=qbl[rl]*rl
    for t in tipos:
        lp_,cp_,rl_,rc_=PAINEIS[TIPOS[t][0]]
        qbc[rc_]+=2*n+(2 if cor_ else 0); mad+=(2*n+(2 if cor_ else 0))*rc_
        np_[TIPOS[t][0]]+=n; madp+=n*lp_*cp_*cad.PANT*cad.DENS
    vert=collections.Counter()
    for rp in pil: vert[rp]+=2*(N+1); mad+=2*(N+1)*rp
    if cor_: vert[cor]+=2*(N+1); mad+=2*(N+1)*cor
    mad+=pes*60; mad*=cad.GMM
    conn=tz*cad.C_TZ+cz*cad.C_CZ+lp*cad.C_L+tp*cad.C_T; plast=tz*cad.M_TZ+cz*cad.M_CZ+lp*cad.M_L+tp*cad.M_T
    return dict(tz=tz,cz=cz,lp=lp,tp=tp,pes=pes,qbc=qbc,qbl=qbl,vert=vert,np=np_,kg=(mad+madp+plast)/1000,custo=conn+(mad+madp)/1000*cad.RSKG)
for r in RUNS: r['bom']=bom_run(r)
# o que custaria tudo em modulos avulsos (N = 1, encostados), para comparar
AVULSO=sum(B[m['tipo']]['custo'] for m in M); AVULSO_TZ=sum(B[m['tipo']]['tz'] for m in M)

# ------------------------------------------------------------------ o catalogo
skus=pc.ler()
for s in skus:
    s['classe'],s['frente'],s['prof']=pc.classificar(s); s['fundo']=max(s['comp'],s['larg']) if s['comp'] else 9999
gond=[s for s in skus if s['classe']=='gondola' and s['ambiente']!='NITRON-MOB']
prat={}
for m in M:
    g=G[m['tipo']]
    for k,h in enumerate(g['faces']):
        prat[(m['n'],k+1)]=dict(mod=m['n'],nivel=k+1,h=h,zona=pc.zona(h),vao=g['vao'][k],prof=g['prof_util'],cap=g['util'],livre=g['util'],itens=[],area=m['area'])
def prats(filtro): return [p for p in prat.values() if filtro(p)]
def ordem(ps):
    return sorted(ps,key=lambda p:({'olhos':0,'maos':1,'chao':2,'topo':3}[p['zona']],-p['h'],p['mod']))
def blocos(lista,maxw):
    bl=collections.defaultdict(list)
    for s in lista: bl[s['ref'].split('.')[0]].append(s)
    out=[]
    for k,it in bl.items():
        it=sorted(it,key=lambda x:-x['fat']); parte=[]; larg=0
        for x in it:
            if parte and larg+x['frente']>maxw: out.append(parte); parte=[]; larg=0
            parte.append(x); larg+=x['frente']
        if parte: out.append(parte)
    return sorted(out,key=lambda b:-sum(x['fat'] for x in b))
def coloca(bl,ps,facing=1):
    larg=sum(x['frente'] for x in bl); alt=max(x['alt'] for x in bl); fundo=max(x['fundo'] for x in bl)
    a=next((q for q in ps if q['livre']>=larg and q['vao']>=alt and q['prof']>=fundo),None)
    if a is None: return False
    a['livre']-=larg
    for x in bl:
        if facing==1: x.update(mod=a['mod'],nivel=a['nivel'],h=a['h'],zona=a['zona'],area=a['area'])
        a['itens'].append((x,facing))
    return True
# 1) paredes e corredor, por ambiente, categoria em bloco vertical (ordem de percurso)
# Organizacao vive no corredor de PDV (gondolas, 5 niveis com baia de 490) e transborda para o norte baixo (sob a janela)
# a entrada (7 vaos) leva as linhas de design e presente — Decor e Teca — mais Infantil/Realce e Frasqueiras (a linha que cresce), Frasqueiras no canto que emenda com o sul
ZONAS=[('Paredão sul',['Paredão sul'],'COZINHA',['POP','GELADEIRA','MICRO-ONDAS','JARRAS','COZINHA','POTES']),
       ('Corredor de PDV + norte',['Gôndola A','Gôndola B','Paredão norte'],'ORGANIZACAO',['ORGANIZACAO']),
       ('Paredão do fundo',['Paredão do fundo'],'BANHO E LAVANDERIA',['LIMPEZA','LIXEIRAS','BANHEIRO']),
       ('Parede de entrada',['Parede de entrada'],'FRASQUEIRAS E INFANTIL',['DECOR','TECA','INFANTIL','REALCE','FRASQUEIRAS'])]
sobra=[]
for nome,areas_,amb,fluxo in ZONAS:
    mods=sorted([m for m in M if m['area'] in areas_ and m['tipo']!='ponta'],key=lambda m:(areas_.index(m['area']),m['n']))
    ps_all=[p for p in prat.values() if p['mod'] in {m['n'] for m in mods}]
    prof=min(p['prof'] for p in ps_all); vmax=max(p['vao'] for p in ps_all)
    A=[s for s in gond if s['categoria'] in fluxo]
    cabe=[s for s in A if s['fundo']<=prof and s['alt']<=vmax]; sobra+= [s for s in A if s not in cabe]
    if nome=='Parede de entrada':
        for s in cabe: s['cat2']='INFANTIL+REALCE' if s['categoria'] in ('INFANTIL','REALCE') else s['categoria']
        fluxo=['DECOR','TECA','INFANTIL+REALCE','FRASQUEIRAS']
    else:
        for s in cabe: s['cat2']=s['categoria']
    dem=collections.Counter()
    for s in cabe: dem[s['cat2']]+=s['frente']
    fluxo=[c for c in fluxo if dem[c]>0]; tot=sum(dem.values()) or 1
    alvo={c:dem[c]/tot*len(mods) for c in fluxo}; nmod={c:max(1,int(alvo[c])) for c in fluxo}
    while sum(nmod.values())<len(mods): c=max(fluxo,key=lambda k:alvo[k]-nmod[k]); nmod[c]+=1
    while sum(nmod.values())>len(mods): c=max((k for k in fluxo if nmod[k]>1),key=lambda k:nmod[k]-alvo[k]); nmod[c]-=1
    i=0; faixa={}
    for c in fluxo:
        faixa[c]=[mods[j]['n'] for j in range(i,i+nmod[c])]; i+=nmod[c]
        for j in range(i-nmod[c],i): mods[j]['categoria']=c
    maxw=max(G[m['tipo']]['util'] for m in mods)
    spill=[]
    for c in fluxo:
        ps=ordem([p for p in prat.values() if p['mod'] in faixa[c]])
        for bl in blocos([s for s in cabe if s['cat2']==c],maxw):
            if not coloca(bl,ps): spill.append(bl)
    ps=ordem(ps_all)
    for bl in spill:
        if not coloca(bl,ps): sobra+=bl
# 2) corredor de PDV: a sobra das paredes, por categoria, enchendo modulo a modulo (bloco vertical por categoria)
ps_g=sorted([p for p in prat.values() if p['area'].startswith('Gôndola') and M[p['mod']-1]['tipo']=='gondola'],key=lambda p:(p['mod'],{'olhos':0,'maos':1,'chao':2,'topo':3}[p['zona']],-p['h']))
catfat=collections.Counter()
for s_ in sobra: catfat[s_['categoria']]+=s_['fat']
sobra2=[]
for bl in sorted(blocos(sobra,725),key=lambda b:(-catfat[b[0]['categoria']],-sum(x['fat'] for x in b))):
    if not coloca(bl,ps_g): sobra2+=bl
sobra=sobra2
# 3) ilhas: o que ainda sobrou (o que pede 500 de fundo), por faturamento, nas 8 ilhas (topo aberto)
ps_ilha=ordem([p for p in prat.values() if p['area'].startswith('Ilha') and 'ilha'==M[p['mod']-1]['tipo']])
ps_ponta=ordem([p for p in prat.values() if M[p['mod']-1]['tipo']=='ponta'])
resto=[]
for bl in blocos(sobra,725):
    if not coloca(bl,ps_ilha):
        if not coloca(bl,ps_ponta): resto+=bl
# 4) segundo facing: campeoes nas 8 pontas (372) e no checkout (268)
camp=sorted([s for s in gond if s.get('mod')],key=lambda s:-s['fat'])
n2p=0
for s in camp:
    if n2p>=64: break
    if coloca([s],ps_ponta,facing=2): n2p+=1
ps_ck=ordem([p for p in prat.values() if p['area']=='Corredor de checkout'])
n2c=0
for s in camp:
    if n2c>=60: break
    if coloca([s],ps_ck,facing=2): n2c+=1
aloc=[s for s in gond if s.get('mod')]
# 5) facing multiplo: a frente livre de cada prateleira e preenchida repetindo os campeoes da propria prateleira (ate 4 facings por SKU)
for p in prat.values():
    p['extra']=collections.Counter(); its=sorted([x for x,fc in p['itens']],key=lambda x:-x['fat'])
    while its and p['livre']>0:
        add_=False
        for x in its:
            if p['extra'][x['ref']]>=3: continue
            if x['frente']<=p['livre']: p['livre']-=x['frente']; p['extra'][x['ref']]+=1; add_=True
        if not add_: break
# 5b) ilhas: prateleira vazia de ilha recebe segundo facing dos campeoes (a ilha 3 fica na praca da entrada)
ps_il2=ordem([p for p in prat.values() if p['area'].startswith('Ilha') and not p['itens']])
n2i=0
for s_ in camp:
    if not any(p['livre']>=s_['frente'] for p in ps_il2): break
    if coloca([s_],ps_il2,facing=2): n2i+=1
# 6) reforco do norte baixo: prateleiras vazias do norte recebem segundo facing dos campeoes de Organizacao (o corredor esta em frente)
ps_norte=ordem([p for p in prat.values() if p['area']=='Paredão norte'])
n2n=0
for s_ in [s for s in camp if s['categoria']=='ORGANIZACAO']:
    if not any(p['livre']>=s_['frente'] for p in ps_norte): break
    if coloca([s_],ps_norte,facing=2): n2n+=1
# 7) repeticao na propria coluna: prateleira vazia repete a prateleira mais forte do mesmo modulo que caiba (facing = 3)
nrep=0
for m in M:
    ps=[p for p in prat.values() if p['mod']==m['n']]
    fontes=sorted([p for p in ps if p['itens']],key=lambda p:-sum(x['fat'] for x,fc in p['itens']))
    for e in ordem([p for p in ps if not p['itens']]):
        for src in fontes:
            its=[x for x,fc in src['itens']]; larg=sum(x['frente'] for x in its)
            if its and larg<=e['livre'] and max(x['alt'] for x in its)<=e['vao'] and max(x['fundo'] for x in its)<=e['prof']:
                for x in its: e['itens'].append((x,3))
                e['livre']-=larg; nrep+=1; break
    for p in ps:
        its=sorted([x for x,fc in p['itens']],key=lambda x:-x['fat'])
        while its and p['livre']>0:
            add_=False
            for x in its:
                if p['extra'][x['ref']]>=3: continue
                if x['frente']<=p['livre']: p['livre']-=x['frente']; p['extra'][x['ref']]+=1; add_=True
            if not add_: break
nfac=sum(1+p['extra'][x['ref']] for p in prat.values() for x,fc in p['itens'])
npos=sum(len(p['itens']) for p in prat.values())
# categoria dominante dos modulos do miolo (para rotulo)
for m in M:
    if not m.get('categoria'):
        c=collections.Counter()
        for p in prat.values():
            if p['mod']==m['n']:
                for x,fc in p['itens']:
                    if fc==1: c[x['categoria']]+=x['fat']
        m['categoria']=c.most_common(1)[0][0] if c else ''

# ------------------------------------------------------------------ saidas
D=RAIZ/'dados'
with open(D/'55-projeto-modulos.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['modulo','corrida','posicao','area','tipo','painel','pilha','x_mm','y_mm','largura_mm','profundidade_mm','eixo','altura_mm','prateleiras','ambiente','categoria','skus_1_facing','skus_2_facing','frente_ocupada_mm','frente_util_mm','faturamento_12m','nota'])
    for m in M:
        g=G[m['tipo']]; ps=[p for p in prat.values() if p['mod']==m['n']]
        it1=[x for p in ps for x,fc in p['itens'] if fc==1]; it2=[x for p in ps for x,fc in p['itens'] if fc==2]
        w.writerow([m['n'],m['run'],m['pos'],m['area'],m['tipo'],g['painel'],'·'.join(map(str,g['pilha']))+(f'+L{g["coroa"]}' if g['coroa'] else ''),m['x'],m['y'],m['w'],m['d'],m['eixo'],round(g['A']),len(g['faces']),m['ambiente'],m.get('categoria',''),len(it1),len(it2),round(sum(x['frente']*(1+p['extra'][x['ref']]) for p in ps for x,fc in p['itens'])),g['util']*len(g['faces']),round(sum(x['fat'] for x in it1),2),m['nota']])
with open(D/'56-projeto-alocacao.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['modulo','area','prateleira','altura_face_mm','zona','vao_livre_mm','facing','facings_na_prateleira','ordem','referencia','nome','ambiente','categoria','frente_mm','profundidade_min_mm','altura_mm','faturamento_12m','clientes'])
    for (mn,k),p in sorted(prat.items()):
        for j,(s,fc) in enumerate(p['itens']):
            w.writerow([mn,p['area'],k,p['h'],p['zona'],round(p['vao']),fc,1+p['extra'][s['ref']],j+1,s['ref'],s['nome'],s['ambiente'],s['categoria'],round(s['frente']),s['prof'],round(s['alt']),round(s['fat'],2),s['clientes']])
tot=collections.Counter(); custo=kg=0
for r in RUNS:
    b=r['bom']; custo+=b['custo']; kg+=b['kg']
    for k,v in b['np'].items(): tot['Painel '+k]+=v
    for k,v in b['qbl'].items(): tot['Ripa largura %d'%k]+=v
    for k,v in b['qbc'].items(): tot['Ripa comprimento %d'%k]+=v
    for a,n in b['vert'].items(): tot['Ripa vertical %d'%a]+=n
    tot['Trizeta']+=b['tz']; tot['Cruzeta']+=b['cz']; tot['Tampa']+=b['tp']; tot['Peça L']+=b['lp']; tot['Pé']+=b['pes']
nparede=sum(1 for m in M if m['area'].startswith('Pared'))
tot['Ancoragem (bucha S8 + parafuso 5×50 + arruela)']=nparede+2
tot['União poste a poste entre corridas vizinhas, 2 níveis (parafuso)']=2*sum(1 for r in RUNS if r['area'].startswith('Pared'))-2*4
tot['União costa a costa das gôndolas, 2 níveis (parafuso)']=2*sum(1 for m in M if m['tipo']=='gondola')
with open(D/'57-projeto-compras.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['item','quantidade'])
    for k in ['Painel 200×620','Painel 305×620','Painel 305×725','Painel 450×725','Ripa largura 183','Ripa largura 287','Ripa largura 415','Ripa comprimento 617','Ripa comprimento 717','Ripa vertical 270','Ripa vertical 346','Ripa vertical 513','Pé','Trizeta','Peça L','Tampa','Cruzeta','Ancoragem (bucha S8 + parafuso 5×50 + arruela)','União poste a poste entre corridas vizinhas, 2 níveis (parafuso)','União costa a costa das gôndolas, 2 níveis (parafuso)']:
        w.writerow([k,tot[k]])
with open(D/'58-projeto-corridas.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['corrida','area','vaos','N','modulos','x_mm','y_mm','eixo','comprimento_mm','profundidade_mm','altura_mm','trizetas','cruzetas','pecas_L','tampas','paineis','custo_material','kg','nota'])
    for r in RUNS:
        b=r['bom']; w.writerow([r['id'],r['area'],' + '.join(r['tipos']),r['N'],'-'.join(map(str,r['mods'])),r['x'],r['y'],r['eixo'],r['L'],r['P'],r['A'],b['tz'],b['cz'],b['lp'],b['tp'],sum(b['np'].values()),round(b['custo'],2),round(b['kg'],2),r['nota']])
# resumo
fat_tot=sum(s['fat'] for s in gond); fat_al=sum(s['fat'] for s in aloc)
z=collections.Counter(); zf=collections.Counter()
for s in aloc: z[s['zona']]+=1; zf[s['zona']]+=s['fat']
areas=collections.OrderedDict()
for m in M:
    a=areas.setdefault(m['area'],dict(mods=0,custo=0,kg=0,skus=0,fat=0,frente=0,prat=0,vazias=0,runs=0))
    a['mods']+=1
for r in RUNS:
    a=areas[r['area']]; a['custo']+=r['bom']['custo']; a['kg']+=r['bom']['kg']; a['runs']+=1
for m in M:
    a=areas[m['area']]
    ps=[p for p in prat.values() if p['mod']==m['n']]; a['prat']+=len(ps); a['vazias']+=sum(1 for p in ps if not p['itens'])
    a['skus']+=sum(1 for p in ps for x,fc in p['itens'] if fc==1); a['fat']+=sum(x['fat'] for p in ps for x,fc in p['itens'] if fc==1); a['frente']+=G[m['tipo']]['util']*len(ps)/1000
R=dict(sala=SALA,M=M,RUNS=[dict(id=r['id'],area=r['area'],tipos=r['tipos'],N=r['N'],mods=r['mods'],L=r['L'],P=r['P'],A=r['A'],x=r['x'],y=r['y'],eixo=r['eixo'],nota=r['nota'],tz=r['bom']['tz'],cz=r['bom']['cz'],custo=r['bom']['custo'],kg=r['bom']['kg']) for r in RUNS],avulso=AVULSO,avulso_tz=AVULSO_TZ,enc=ENC,G={t:dict(painel=g['painel'],pilha=g['pilha'],coroa=g['coroa'],L=round(g['L']),P=round(g['P']),A=round(g['A']),faces=g['faces'],vao=[round(v) for v in g['vao']],util=g['util']) for t,g in G.items()},
       B={t:dict(custo=b['custo'],kg=b['kg'],tz=b['tz'],np=b['np']) for t,b in B.items()},
       areas=areas,custo=custo,kg=kg,tot=dict(tot),gond=len(gond),aloc=len(aloc),resto=[(s['ref'],s['nome'],s['categoria'],round(s['alt']),s['fundo'],s['fat']) for s in sorted(resto,key=lambda s:-s['fat'])],
       fat_tot=fat_tot,fat_al=fat_al,nfac=nfac,npos=npos,n2n=n2n,n2i=n2i,nrep=nrep,janela=JANELA,zonas={k:dict(n=z[k],fat=zf[k]) for k in z},n2p=n2p,n2c=n2c,
       cel={f"{p['mod']}-{p['nivel']}":[sum(1 for x,fc in p['itens'] if fc==1),sum(x['frente']*(1+p['extra'][x['ref']]) for x,fc in p['itens']),sum(x['fat'] for x,fc in p['itens'] if fc==1),sum(1 for x,fc in p['itens'] if fc==2),sum(1 for x,fc in p['itens'] if fc==3)] for p in prat.values()},
       cat={m['n']:m.get('categoria','') for m in M})
json.dump(R,open('/tmp/claude-0/-home-user-produtos/a90e79dc-9d6b-5cf3-8b87-00e7e5301ee0/scratchpad/projeto.json','w'),ensure_ascii=False,default=float)
print('%d vãos em %d corridas · R$ %.2f · %.0f kg · %d trizetas · %d cruzetas · avulso (N=1) seria R$ %.2f com %d trizetas'%(len(M),len(RUNS),custo,kg,tot['Trizeta'],tot['Cruzeta'],AVULSO,AVULSO_TZ))
print('catálogo em prateleira: %d de %d SKUs · R$ %.2f M de %.2f (%.1f%%) · sem lugar: %d'%(len(aloc),len(gond),fat_al/1e6,fat_tot/1e6,100*fat_al/fat_tot,len(resto)))
for k in ('olhos','maos','chao','topo'):
    if z[k]: print('  %-6s %3d SKUs · %.0f%% do faturamento alocado'%(k,z[k],100*zf[k]/fat_al))
print('segundo facing: %d nas pontas · %d no checkout · %d nas ilhas · %d no norte · %d prateleiras repetidas · facings totais %d em %d posições (%.1f por posição)'%(n2p,n2c,n2i,n2n,nrep,nfac,npos,nfac/npos))
for a,v in areas.items(): print('  %-24s %2d mód · R$ %8.2f · %3d SKUs · R$ %5.2f M · %5.1f m · vazias %2d/%2d'%(a,v['mods'],v['custo'],v['skus'],v['fat']/1e6,v['frente'],v['vazias'],v['prat']))
if resto: print('sem lugar:',[(r['ref'],r['nome'][:30],round(r['alt']),r['fundo']) for r in resto[:6]])
