#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""As quatro paredes do showroom, modulo a modulo, com o kit flexivel (N = 1, zero cruzeta).
Generaliza analise/parede-sul.py: cada parede tem corrida, ambiente, modulo e ordem de percurso.
Gera dados/50-paredes-modulos.csv, 51-paredes-alocacao.csv, 52-paredes-bom.csv, 53-paredes-miolo.csv."""
import csv, collections, importlib.util, pathlib, json
RAIZ=pathlib.Path(__file__).resolve().parent.parent
def load(n,f):
    s=importlib.util.spec_from_file_location(n,RAIZ/'analise'/f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
pc=load('pc','planograma-catalogo.py'); cad=load('cad','pdv-caderno.py')
L754=round(cad.ext_comp(717,1),1); L450=round(cad.ext_comp(415,1),1)
TESTEIRA_BASE=1900          # a testeira sobe em hastes; produto na ultima prateleira nao pode passar disso
PILHAS={'alto':[270]*6,'alto-fundo':[513,513,270,270],'arara':[513,513],'baixo':[270]*3}

PAREDES=[
 dict(id='sul',nome='Paredão sul',corrida=13350,ambiente='COZINHA',painel=300,pilha='alto',ajuste=True,
      fluxo=['DECOR','POP','GELADEIRA','MICRO-ONDAS','JARRAS','COZINHA','POTES','TECA'],ultima2=True,vitrine=0,
      lede='da entrada para o fundo: gadget e kit na frente, jarras e cozinha no meio, potes como destino, teca fechando'),
 dict(id='fundo',nome='Paredão do fundo',corrida=6873,ambiente='BANHO E LAVANDERIA',painel=460,pilha='alto-fundo',ajuste=False,
      fluxo=['LIMPEZA','LIXEIRAS','BANHEIRO'],ultima2=False,vitrine=0,
      lede='do canto da cozinha ao canto da organização: limpeza, lixeiras no centro como destino, banheiro'),
 dict(id='norte',nome='Paredão norte',corrida=6100,ambiente='ORGANIZACAO',painel=300,pilha='alto',ajuste=True,
      fluxo=['ORGANIZACAO'],ultima2=False,vitrine=0,
      lede='uma categoria só; o faturamento decide a altura e os blocos de cor ficam juntos'),
 dict(id='entrada',nome='Parede de entrada',corrida=6548,ambiente='FRASQUEIRAS E INFANTIL',painel=300,pilha='alto-fundo',ajuste=False,
      fluxo=['FRASQUEIRAS','INFANTIL+REALCE'],ultima2=False,vitrine=3,merge={'INFANTIL':'INFANTIL+REALCE','REALCE':'INFANTIL+REALCE'},
      lede='parede de descompressão: três módulos de frasqueiras no canto da cozinha; o resto é vitrine do Nitron-Mob montado, com duas araras'),
]

skus=pc.ler()
for s in skus:
    s['classe'],s['frente'],s['prof']=pc.classificar(s); s['baia']=pc.baia(s['alt'])
gond=[s for s in skus if s['classe']=='gondola']

def compor(p):
    """quantos modulos, de que largura, e onde ficam"""
    livre=p['corrida']
    if p['ajuste']:
        cands=[(livre-(a*L754+b*L450),a,b) for a in range(0,25) for b in range(0,8) if a*L754+b*L450<=livre]
        fmin=min(c[0] for c in cands)
        # entre as que fecham a menos de 100 mm da melhor folga, a de menos modulos de 450
        folga,nA,nB=min((c for c in cands if c[0]<=fmin+100),key=lambda c:(c[2],c[0]))
    else:
        nA=int(livre//L754); nB=0; folga=livre-nA*L754
    seq=['450']*(nB//2)+['754']*nA+['450']*(nB-nB//2)
    mods=[]; x=folga/2
    if p['vitrine']:        # a entrada: so os ultimos 'vitrine' modulos sao prateleira; o resto e chao livre + araras
        seq=seq[-p['vitrine']:]; x=livre-len(seq)*L754
    for i,t in enumerate(seq):
        w=L754 if t=='754' else L450; pan=754 if t=='754' else 450
        mods.append(dict(parede=p['id'],n=i+1,tipo=f"{p['painel']}×{pan}-1-{p['pilha']}",painel=pan,x0=round(x),x1=round(x+w),util=pan,pilha=p['pilha'])); x+=w
    return mods,folga,nA,nB

def alocar(p,mods):
    pil=PILHAS[p['pilha']]; faces=pc.prateleiras(pil); prof=round(cad.ext_prof(287 if p['painel']==300 else 415))
    # vao livre acima de cada prateleira: a baia acima, ou ate a base da testeira na ultima
    vao=[ (pil[k]-pc.CONSOME+pc.NOZ-pc.PANT) if k<len(pil) else (TESTEIRA_BASE-faces[k]-pc.PANT/2) for k in range(len(faces))]
    amb=[s for s in gond if s['ambiente']==p['ambiente']]
    for s in amb: s['categoria']=p.get('merge',{}).get(s['categoria'],s['categoria'])
    cabe=[s for s in amb if s['prof']<=prof and s['alt']<=max(vao)]
    fora=[s for s in amb if s not in cabe]
    prat={}
    for m in mods:
        for k,h in enumerate(faces):
            prat[(m['n'],k+1)]=dict(mod=m['n'],nivel=k+1,h=h,zona=pc.zona(h),vao=vao[k],cap=m['util'],livre=m['util'],itens=[])
    dem=collections.Counter()
    for s in cabe: dem[s['categoria']]+=s['frente']
    fluxo=[c for c in p['fluxo'] if dem[c]>0]
    tot=sum(dem.values()) or 1
    alvo={c: dem[c]/tot*len(mods) for c in fluxo}
    nmod={c: max(1,int(alvo[c])) for c in fluxo}
    while sum(nmod.values())<len(mods): c=max(fluxo,key=lambda k: alvo[k]-nmod[k]); nmod[c]+=1
    while sum(nmod.values())>len(mods):
        c=max((k for k in fluxo if nmod[k]>1),key=lambda k: nmod[k]-alvo[k]); nmod[c]-=1
    if p['ultima2'] and nmod.get(fluxo[-1],0)<2 and len(mods)>len(fluxo): nmod[fluxo[-1]]=2; nmod[max(fluxo,key=lambda k:nmod[k])]-=1
    faixa={}; i=0
    for c in fluxo:
        faixa[c]=list(range(i,i+nmod[c])); i+=nmod[c]
        for k in faixa[c]: mods[k]['categoria']=c
    blocos=collections.defaultdict(list)
    for s in cabe: blocos[(s['categoria'],s['ref'].split('.')[0])].append(s)
    MAXW=max(m['util'] for m in mods)
    for k in list(blocos):
        it=sorted(blocos[k],key=lambda x:-x['fat'])
        if sum(x['frente'] for x in it)>MAXW:
            del blocos[k]; parte=[]; larg=0; j=0
            for x in it:
                if parte and larg+x['frente']>MAXW: blocos[(k[0],f'{k[1]}/{j}')]=parte; j+=1; parte=[]; larg=0
                parte.append(x); larg+=x['frente']
            if parte: blocos[(k[0],f'{k[1]}/{j}')]=parte
    def ordem_prat(idx):
        out=[]
        for z in ('olhos','maos','chao'):
            for k,h in sorted(enumerate(faces),key=lambda kh:-kh[1]):
                if pc.zona(h)!=z: continue
                for mi in idx: out.append(prat[(mods[mi]['n'],k+1)])
        return out
    def coloca(bl,ps):
        larg=sum(x['frente'] for x in bl); alt=max(x['alt'] for x in bl)
        a=next((q for q in ps if q['livre']>=larg and q['vao']>=alt),None)
        if a is None: return False
        a['livre']-=larg
        for x in bl: x.update(mod=a['mod'],nivel=a['nivel'],h=a['h'],zona=a['zona']); a['itens'].append(x)
        return True
    spill=[]
    for c in fluxo:
        bl=sorted([(k,v) for k,v in blocos.items() if k[0]==c],key=lambda kv:-sum(x['fat'] for x in kv[1]))
        ps=ordem_prat(faixa[c])
        for k,it in bl:
            if not coloca(it,ps): spill.append(it)
    ps=ordem_prat(range(len(mods)))
    spill=[it for it in spill if not coloca(it,ps)]
    for it in spill:
        for x in it: fora.append(x)
    cabe=[s for s in cabe if s.get('mod')]
    return dict(faces=faces,prof=prof,vao=vao,cabe=cabe,fora=fora,prat=prat,nmod=nmod,dem=dem,fluxo=fluxo,amb=amb)

def bom_mod(painel,pilha):
    cref='PSC-04' if painel==754 else 'PSC-02'
    lpan=300 if painel in (450,754) and pilha!='x' else 460
    return None
def bom(p,painel):
    lpan=p['painel']; cref='PSC-04' if painel==754 else 'PSC-02'
    f=dict(nome='',slug='',bc=cref,bcv=717 if painel==754 else 415,bl='BLA-03-AC' if lpan==300 else 'PSC-02',blv=287 if lpan==300 else 415,
           pan=(lpan,painel),vaos=(1,1,1),pilha=PILHAS[p['pilha']],coroa=None,ganch=False,fundo=False,deck=False,casinha=False,faces=1,lede='',cap='')
    return cad.bom(f,1)

D=RAIZ/'dados'; RES={}
fm=open(D/'50-paredes-modulos.csv','w',newline='',encoding='utf-8'); wm=csv.writer(fm)
wm.writerow(['parede','modulo','tipo','painel_mm','x_inicio_mm','x_fim_mm','categoria','prateleiras','skus','frente_ocupada_mm','frente_util_mm','ocupacao','faturamento_12m'])
fa=open(D/'51-paredes-alocacao.csv','w',newline='',encoding='utf-8'); wa=csv.writer(fa)
wa.writerow(['parede','modulo','prateleira','altura_face_mm','zona','vao_livre_mm','ordem','referencia','nome','categoria','frente_mm','profundidade_min_mm','altura_mm','faturamento_12m','clientes'])
fb=open(D/'52-paredes-bom.csv','w',newline='',encoding='utf-8'); wb_=csv.writer(fb)
wb_.writerow(['parede','item','quantidade','custo_rs'])
fo=open(D/'53-paredes-miolo.csv','w',newline='',encoding='utf-8'); wo=csv.writer(fo)
wo.writerow(['parede_de_origem','ambiente','referencia','nome','categoria','motivo','frente_mm','profundidade_min_mm','altura_mm','faturamento_12m'])
for p in PAREDES:
    mods,folga,nA,nB=compor(p); A=alocar(p,mods)
    for m in mods:
        it=[s for s in A['cabe'] if s['mod']==m['n']]; oc=sum(s['frente'] for s in it); cap=m['util']*len(A['faces'])
        wm.writerow([p['id'],m['n'],m['tipo'],m['painel'],m['x0'],m['x1'],m.get('categoria',''),len(A['faces']),len(it),round(oc),cap,round(oc/cap,3),round(sum(s['fat'] for s in it),2)])
    for (mn,k),q in sorted(A['prat'].items()):
        for j,s in enumerate(sorted(q['itens'],key=lambda s:(s['ref'].split('.')[0],-s['fat']))):
            wa.writerow([p['id'],mn,k,q['h'],q['zona'],round(q['vao']),j+1,s['ref'],s['nome'],s['categoria'],round(s['frente']),s['prof'],round(s['alt']),round(s['fat'],2),s['clientes']])
    for s in sorted(A['fora'],key=lambda s:-s['fat']):
        mot='profundidade %d > %d'%(s['prof'],A['prof']) if s['prof']>A['prof'] else ('altura %d > %d'%(round(s['alt']),round(max(A['vao']))) if s['alt']>max(A['vao']) else 'sem prateleira com vão')
        wo.writerow([p['id'],p['ambiente'],s['ref'],s['nome'],s['categoria'],mot,round(s['frente']),s['prof'],round(s['alt']),round(s['fat'],2)])
    bA=bom(p,754); bB=bom(p,450) if nB else None
    nmods=len(mods); nA_=sum(1 for m in mods if m['painel']==754); nB_=nmods-nA_
    itens=[('Módulo %s'%mods[0]['tipo'].replace('450','754'),nA_,bA['custo']*nA_),]
    if nB_: itens.append(('Módulo %s'%mods[-1]['tipo'],nB_,bB['custo']*nB_))
    tz=nA_*bA['tz']+(nB_*bB['tz'] if bB else 0); np_=nA_*bA['np']+(nB_*bB['np'] if bB else 0)
    itens+=[('Trizeta',tz,None),('Tampa',nA_*bA['tp']+(nB_*bB['tp'] if bB else 0),None),('Painel %d×754'%p['painel'],nA_*bA['np'],None)]
    if nB_: itens.append(('Painel 300×450',nB_*bB['np'],None))
    itens+=[('Ripa PSC-04 (717)',nA_*bA['qbc'],None)]
    if nB_: itens.append(('Ripa PSC-02 (415) como comprimento',nB_*bB['qbc'],None))
    itens+=[('Ripa de largura %s'%('BLA-03-AC (287)' if p['painel']==300 else 'PSC-02 (415)'),nA_*bA['qbl']+(nB_*bB['qbl'] if bB else 0),None)]
    for r_,q_ in sorted(collections.Counter({k:v*nA_ for k,v in bA['vert'].items()}).items()):
        q_+= (bB['vert'].get(r_,0)*nB_) if bB else 0
        itens.append(('Ripa vertical %d'%r_,q_,None))
    itens+=[('Pé',nA_*bA['pes']+(nB_*bB['pes'] if bB else 0),None),('Cruzeta',0,None),
            ('Ancoragem (bucha S8 + parafuso 5×50 + arruela)',nmods,nmods*1.20),('União poste a poste, 2 níveis',2*(nmods-1),2*(nmods-1)*0.35),
            ('Testeira %d × 200'%754,nA_,None)]
    if nB_: itens.append(('Testeira 450 × 200',nB_,None))
    itens.append(('Faixa de prateleira',nmods*len(A['faces']),None))
    if p['vitrine']:
        fa_=dict(nome='',slug='',bc='PSC-04',bcv=717,bl='BLA-03-AC',blv=287,pan=(300,754),vaos=(1,1,1),pilha=[513,513],coroa=513,ganch=False,fundo=False,deck=False,casinha=False,faces=1,lede='',cap='')
        ARARA=cad.bom(fa_,1)
        itens+=[('Módulo 300×754-1-arara (vitrine Nitron-Mob)',2,2*ARARA['custo']),('Ancoragem das araras',2,2*1.20)]
    for it,q,c in itens: wb_.writerow([p['id'],it,q,round(c,2) if c else ''])
    custo=bA['custo']*nA_+(bB['custo']*nB_ if bB else 0)+(2*ARARA['custo'] if p['vitrine'] else 0)
    kg=bA['kg']*nA_+(bB['kg']*nB_ if bB else 0)
    z={zz:dict(skus=sum(1 for s in A['cabe'] if s['zona']==zz),fat=sum(s['fat'] for s in A['cabe'] if s['zona']==zz)) for zz in ('olhos','maos','chao')}
    RES[p['id']]=dict(p=p,mods=mods,folga=folga,nA=nA_,nB=nB_,faces=A['faces'],prof=A['prof'],vao=[round(v) for v in A['vao']],
        amb=len(A['amb']),cabe=len(A['cabe']),fora=len(A['fora']),fat_amb=sum(s['fat'] for s in A['amb']),fat_cabe=sum(s['fat'] for s in A['cabe']),fat_fora=sum(s['fat'] for s in A['fora']),
        m_dem=sum(s['frente'] for s in A['cabe'])/1000,m_fora=sum(s['frente'] for s in A['fora'])/1000,oferta=sum(m['util'] for m in mods)*len(A['faces'])/1000,
        nmod=A['nmod'],dem={c:round(A['dem'][c]/1000,1) for c in A['fluxo']},fluxo=A['fluxo'],zonas=z,
        prat_vazias=sum(1 for q in A['prat'].values() if not q['itens']),prat_total=len(A['prat']),custo=custo,kg=kg,triz=tz,paineis=np_,
        fora_prof=sum(1 for s in A['fora'] if s['prof']>A['prof']),fora_alt=sum(1 for s in A['fora'] if s['prof']<=A['prof']),
        fora_lista=[(s['ref'],s['nome'],s['categoria'],'prof %d'%s['prof'] if s['prof']>A['prof'] else 'alt %d'%round(s['alt']),s['fat']) for s in sorted(A['fora'],key=lambda s:-s['fat'])],
        cel={f"{m['n']}-{k}":[len(q['itens']),sum(x['frente'] for x in q['itens']),sum(x['fat'] for x in q['itens'])] for (mn,k),q in A['prat'].items() for m in mods if m['n']==mn})
    print('%-18s %2d mód (%d×754%s) · %5d mm · folga %3.0f · %3d de %3d SKUs · dem %5.1f m / oferta %5.1f m · vazias %2d/%3d · olhos %2.0f%% · fora %2d (%d prof, %d alt) · R$ %8.2f · %d triz'%(
        p['nome'],len(mods),nA_,' + %d×450'%nB_ if nB_ else '',sum(m['x1']-m['x0'] for m in mods),folga if not p['vitrine'] else p['corrida']-sum(m['x1']-m['x0'] for m in mods),
        len(A['cabe']),len(A['amb']),RES[p['id']]['m_dem'],RES[p['id']]['oferta'],RES[p['id']]['prat_vazias'],len(A['prat']),100*z['olhos']['fat']/max(RES[p['id']]['fat_cabe'],1),len(A['fora']),RES[p['id']]['fora_prof'],RES[p['id']]['fora_alt'],custo,tz))
for f in (fm,fa,fb,fo): f.close()
json.dump(RES,open('/tmp/claude-0/-home-user-produtos/a90e79dc-9d6b-5cf3-8b87-00e7e5301ee0/scratchpad/paredes.json','w'),ensure_ascii=False,default=float)
tot=sum(r['custo'] for r in RES.values()); print('TOTAL paredes: R$ %.2f · %d módulos · fora para o miolo: %d SKUs'%(tot,sum(len(r['mods']) for r in RES.values())+2,sum(r['fora'] for r in RES.values())))
