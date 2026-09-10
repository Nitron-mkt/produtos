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
SALA=dict(C=13350,L=7520,H=3400,porta=(0,2000),caixa=(2400,5800,600),pilar=(6500,6745,670))
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

# ------------------------------------------------------------------ os modulos na planta (mm; x = comprimento, y = largura; porta em x=0, norte em y=0)
M=[]
def add(area,tipo,x,y,eixo,amb,nota=''):
    g=G[tipo]; w,d=(g['L'],g['P']) if eixo=='x' else (g['P'],g['L'])
    M.append(dict(n=len(M)+1,area=area,tipo=tipo,x=round(x),y=round(y),w=round(w),d=round(d),eixo=eixo,ambiente=amb,nota=nota))
    return x+(w if eixo=='x' else 0), y+(d if eixo=='y' else 0)
# sul: 2x659 + 14x759 + 2x659, folga 88 nos cantos
x=44
for t in ['parede-620']*2+['parede-725']*14+['parede-620']*2: x,_=add('Paredão sul',t,x,SALA['L']-372,'x','COZINHA')
# norte: do pilar ao modulo do fundo — baixo (1.030), a janela comeca em 1.100
x=6745
for _ in range(8): x,_=add('Paredão norte','parede-baixa',x,0,'x','ORGANIZACAO','sob a janela')
# fundo: entre norte e sul; o 659 no canto do norte
y=372
for t in ['fundo-620']+['parede-fundo']*8: _,y=add('Paredão do fundo',t,SALA['C']-372,y,'y','BANHO E LAVANDERIA')
# entrada: 3 modulos encostados no canto do sul, araras na vitrine
y=SALA['L']-372-3*L759
for _ in range(3): _,y=add('Parede de entrada','parede-725',0,y,'y','FRASQUEIRAS E INFANTIL')
add('Vitrine da entrada','arara',0,2300,'y','NITRON-MOB','arara Nitron-Mob montada'); add('Vitrine da entrada','arara',0,3600,'y','NITRON-MOB','arara Nitron-Mob montada')
# ilhas: 2 x 2 de 450x725 costa a costa, ponta em cada cabeceira (759 ao longo de y, 372 em x)
for k,(ix,iy) in enumerate(((5400,1900),(5400,4300))):
    add(f'Ilha {k+1}','ponta',ix,iy+(1000-L759)/2,'y','MIOLO','cabeceira oeste')
    for j in range(2):
        add(f'Ilha {k+1}','ilha',ix+372+j*L759,iy,'x','MIOLO','face norte'); add(f'Ilha {k+1}','ilha',ix+372+j*L759,iy+500,'x','MIOLO','face sul')
    add(f'Ilha {k+1}','ponta',ix+372+2*L759,iy+(1000-L759)/2,'y','MIOLO','cabeceira leste')
# corredor de PDV: duas gondolas dupla-face (3 pares costa a costa, 744 de fundo) com ponta em cada cabeceira, ao longo de y
for k,rx in enumerate((8700,10844)):
    nome='Gôndola '+'AB'[k]; y0=2250
    add(nome,'ponta',rx+372-L759/2,y0,'x','CORREDOR','cabeceira norte'); y=y0+372
    for j in range(3):
        add(nome,'gondola',rx,y,'y','CORREDOR','face oeste'); _,y=add(nome,'gondola',rx+372,y,'y','CORREDOR','face leste')
    add(nome,'ponta',rx+372-L759/2,y,'x','CORREDOR','cabeceira sul')
# checkout: duas fileiras ao longo de y desembocando no caixa (caixa em y 0-600, x 2400-5800)
for cx,lado in ((2600,'lado oeste'),(4000,'lado leste')):
    y=800
    for _ in range(3): _,y=add('Corredor de checkout','checkout',cx,y,'y','CHECKOUT',lado)
assert len(M)==74, len(M)

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
ZONAS=[('Paredão sul',['Paredão sul'],'COZINHA',['DECOR','POP','GELADEIRA','MICRO-ONDAS','JARRAS','COZINHA','POTES','TECA']),
       ('Corredor de PDV + norte',['Gôndola A','Gôndola B','Paredão norte'],'ORGANIZACAO',['ORGANIZACAO']),
       ('Paredão do fundo',['Paredão do fundo'],'BANHO E LAVANDERIA',['LIMPEZA','LIXEIRAS','BANHEIRO']),
       ('Parede de entrada',['Parede de entrada'],'FRASQUEIRAS E INFANTIL',['FRASQUEIRAS','INFANTIL','REALCE'])]
sobra=[]
for nome,areas_,amb,fluxo in ZONAS:
    mods=sorted([m for m in M if m['area'] in areas_ and m['tipo']!='ponta'],key=lambda m:(areas_.index(m['area']),m['n']))
    ps_all=[p for p in prat.values() if p['mod'] in {m['n'] for m in mods}]
    prof=min(p['prof'] for p in ps_all); vmax=max(p['vao'] for p in ps_all)
    A=[s for s in gond if s['ambiente']==amb]
    cabe=[s for s in A if s['fundo']<=prof and s['alt']<=vmax]; sobra+= [s for s in A if s not in cabe]
    if nome=='Parede de entrada':
        for s in cabe: s['cat2']='FRASQUEIRAS' if s['categoria']=='FRASQUEIRAS' else 'INFANTIL+REALCE'
        fluxo=['FRASQUEIRAS','INFANTIL+REALCE']
    else:
        for s in cabe: s['cat2']=s['categoria']
    dem=collections.Counter()
    for s in cabe: dem[s['cat2']]+=s['frente']
    fluxo=[c for c in fluxo if dem[c]>0]; tot=sum(dem.values()) or 1
    alvo={c:dem[c]/tot*len(mods) for c in fluxo}; nmod={c:max(1,int(alvo[c])) for c in fluxo}
    while sum(nmod.values())<len(mods): c=max(fluxo,key=lambda k:alvo[k]-nmod[k]); nmod[c]+=1
    while sum(nmod.values())>len(mods): c=max((k for k in fluxo if nmod[k]>1),key=lambda k:nmod[k]-alvo[k]); nmod[c]-=1
    if nome=='Paredão sul' and nmod.get('TECA',0)<2: nmod['TECA']=2; nmod['POTES']-=1
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
    w=csv.writer(f); w.writerow(['modulo','area','tipo','painel','pilha','x_mm','y_mm','largura_mm','profundidade_mm','eixo','altura_mm','prateleiras','ambiente','categoria','skus_1_facing','skus_2_facing','frente_ocupada_mm','frente_util_mm','faturamento_12m','nota'])
    for m in M:
        g=G[m['tipo']]; ps=[p for p in prat.values() if p['mod']==m['n']]
        it1=[x for p in ps for x,fc in p['itens'] if fc==1]; it2=[x for p in ps for x,fc in p['itens'] if fc==2]
        w.writerow([m['n'],m['area'],m['tipo'],g['painel'],'·'.join(map(str,g['pilha']))+(f'+L{g["coroa"]}' if g['coroa'] else ''),m['x'],m['y'],m['w'],m['d'],m['eixo'],round(g['A']),len(g['faces']),m['ambiente'],m.get('categoria',''),len(it1),len(it2),round(sum(x['frente']*(1+p['extra'][x['ref']]) for p in ps for x,fc in p['itens'])),g['util']*len(g['faces']),round(sum(x['fat'] for x in it1),2),m['nota']])
with open(D/'56-projeto-alocacao.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['modulo','area','prateleira','altura_face_mm','zona','vao_livre_mm','facing','facings_na_prateleira','ordem','referencia','nome','ambiente','categoria','frente_mm','profundidade_min_mm','altura_mm','faturamento_12m','clientes'])
    for (mn,k),p in sorted(prat.items()):
        for j,(s,fc) in enumerate(p['itens']):
            w.writerow([mn,p['area'],k,p['h'],p['zona'],round(p['vao']),fc,1+p['extra'][s['ref']],j+1,s['ref'],s['nome'],s['ambiente'],s['categoria'],round(s['frente']),s['prof'],round(s['alt']),round(s['fat'],2),s['clientes']])
tot=collections.Counter(); custo=kg=0
for m in M:
    b=B[m['tipo']]; custo+=b['custo']; kg+=b['kg']
    tot['Painel '+G[m['tipo']]['painel']]+=b['np']; tot['Ripa largura %d'%PAINEIS[G[m['tipo']]['painel']][2]]+=b['qbl']; tot['Ripa comprimento %d'%PAINEIS[G[m['tipo']]['painel']][3]]+=b['qbc']
    for a,n in b['vert'].items(): tot['Ripa vertical %d'%a]+=n
    tot['Trizeta']+=b['tz']; tot['Tampa']+=b['tp']; tot['Peça L']+=b['lp']; tot['Pé']+=b['pes']
nparede=sum(1 for m in M if m['area'].startswith('Pared'))
tot['Ancoragem (bucha S8 + parafuso 5×50 + arruela)']=nparede+2
tot['União poste a poste, 2 níveis (parafuso)']=2*(nparede-4)
tot['União costa a costa das gôndolas, 2 níveis (parafuso)']=2*sum(1 for m in M if m['tipo']=='gondola')
with open(D/'57-projeto-compras.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['item','quantidade'])
    for k in ['Painel 200×620','Painel 305×620','Painel 305×725','Painel 450×725','Ripa largura 183','Ripa largura 287','Ripa largura 415','Ripa comprimento 617','Ripa comprimento 717','Ripa vertical 270','Ripa vertical 346','Ripa vertical 513','Pé','Trizeta','Peça L','Tampa','Ancoragem (bucha S8 + parafuso 5×50 + arruela)','União poste a poste, 2 níveis (parafuso)','União costa a costa das gôndolas, 2 níveis (parafuso)']:
        w.writerow([k,tot[k]])
    w.writerow(['Cruzeta',0])
# resumo
fat_tot=sum(s['fat'] for s in gond); fat_al=sum(s['fat'] for s in aloc)
z=collections.Counter(); zf=collections.Counter()
for s in aloc: z[s['zona']]+=1; zf[s['zona']]+=s['fat']
areas=collections.OrderedDict()
for m in M:
    a=areas.setdefault(m['area'],dict(mods=0,custo=0,kg=0,skus=0,fat=0,frente=0,prat=0,vazias=0))
    a['mods']+=1; a['custo']+=B[m['tipo']]['custo']; a['kg']+=B[m['tipo']]['kg']
    ps=[p for p in prat.values() if p['mod']==m['n']]; a['prat']+=len(ps); a['vazias']+=sum(1 for p in ps if not p['itens'])
    a['skus']+=sum(1 for p in ps for x,fc in p['itens'] if fc==1); a['fat']+=sum(x['fat'] for p in ps for x,fc in p['itens'] if fc==1); a['frente']+=G[m['tipo']]['util']*len(ps)/1000
R=dict(sala=SALA,M=M,G={t:dict(painel=g['painel'],pilha=g['pilha'],coroa=g['coroa'],L=round(g['L']),P=round(g['P']),A=round(g['A']),faces=g['faces'],vao=[round(v) for v in g['vao']],util=g['util']) for t,g in G.items()},
       B={t:dict(custo=b['custo'],kg=b['kg'],tz=b['tz'],np=b['np']) for t,b in B.items()},
       areas=areas,custo=custo,kg=kg,tot=dict(tot),gond=len(gond),aloc=len(aloc),resto=[(s['ref'],s['nome'],s['categoria'],round(s['alt']),s['fundo'],s['fat']) for s in sorted(resto,key=lambda s:-s['fat'])],
       fat_tot=fat_tot,fat_al=fat_al,nfac=nfac,npos=npos,n2n=n2n,nrep=nrep,janela=JANELA,zonas={k:dict(n=z[k],fat=zf[k]) for k in z},n2p=n2p,n2c=n2c,
       cel={f"{p['mod']}-{p['nivel']}":[sum(1 for x,fc in p['itens'] if fc==1),sum(x['frente']*(1+p['extra'][x['ref']]) for x,fc in p['itens']),sum(x['fat'] for x,fc in p['itens'] if fc==1),sum(1 for x,fc in p['itens'] if fc==2),sum(1 for x,fc in p['itens'] if fc==3)] for p in prat.values()},
       cat={m['n']:m.get('categoria','') for m in M})
json.dump(R,open('/tmp/claude-0/-home-user-produtos/a90e79dc-9d6b-5cf3-8b87-00e7e5301ee0/scratchpad/projeto.json','w'),ensure_ascii=False,default=float)
print('%d módulos · R$ %.2f · %.0f kg'%(len(M),custo,kg))
print('catálogo em prateleira: %d de %d SKUs · R$ %.2f M de %.2f (%.1f%%) · sem lugar: %d'%(len(aloc),len(gond),fat_al/1e6,fat_tot/1e6,100*fat_al/fat_tot,len(resto)))
for k in ('olhos','maos','chao','topo'):
    if z[k]: print('  %-6s %3d SKUs · %.0f%% do faturamento alocado'%(k,z[k],100*zf[k]/fat_al))
print('segundo facing: %d nas pontas · %d no checkout · %d no norte · %d prateleiras repetidas · facings totais %d em %d posições (%.1f por posição)'%(n2p,n2c,n2n,nrep,nfac,npos,nfac/npos))
for a,v in areas.items(): print('  %-24s %2d mód · R$ %8.2f · %3d SKUs · R$ %5.2f M · %5.1f m · vazias %2d/%2d'%(a,v['mods'],v['custo'],v['skus'],v['fat']/1e6,v['frente'],v['vazias'],v['prat']))
if resto: print('sem lugar:',[(r['ref'],r['nome'][:30],round(r['alt']),r['fundo']) for r in resto[:6]])
