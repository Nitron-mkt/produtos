import sys, trimesh, numpy as np
sys.path.insert(0,'.')
from lib3d import boolean, CX, CZ
from math import radians
D='/home/user/produtos/chrono/stl_v2/'
M1=trimesh.load(D+'Chrono_M01_Valvula_Dias.stl')
M2=trimesh.load(D+'Chrono_M02_Aro_Meses.stl')
M3a=trimesh.load(D+'Chrono_M03a_Ponteira_MD.stl')
M3b=trimesh.load(D+'Chrono_M03b_Ponteira_Janela.stl')
M3=M3a
T =trimesh.load('/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/1c50a47b-Mont_pote_com_valvula__Tampa_Pote_025_Pequeno_Cav1.STL')
V0=trimesh.load('/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/5882c071-Mont_pote_com_valvula__prova_valvula1.STL')
def vol(a,b):
    i=boolean('intersection',[a,b]); return i.volume if i is not None and len(i.faces) else 0.0
def p(n,v,tol=0.01):
    print('  %-36s %9.4f mm3  %s'%(n,v,'ok' if v<tol else '*** COLIDE ***')); return v
def gira(m,deg):
    n=m.copy(); n.apply_translation([-CX,0,-CZ])
    n.apply_transform(trimesh.transformations.rotation_matrix(radians(deg),[0,1,0]))
    n.apply_translation([CX,0,CZ]); return n

print('ENTRE AS TRES PECAS (posicao de projeto)')
p('valvula x aro',vol(M1,M2)); p('valvula x travinha',vol(M1,M3)); p('aro x travinha',vol(M2,M3))
print('\nCONTRA A TAMPA — a tampa NAO foi tocada')
p('aro x tampa',vol(M2,T)); p('travinha x tampa',vol(M3,T))
vn=p('valvula nova x tampa',vol(M1,T),tol=99)
vo=boolean('intersection',[V0,T]).volume
print('  %-36s %9.4f mm3  <- a valvula que voce ja injeta'%('valvula ORIGINAL x tampa',vo))
print('  diferenca %+.4f mm3  %s'%(vn-vo,'nenhum aperto novo' if abs(vn-vo)<0.01 else '*** ATENCAO ***'))

print('\nVARREDURA — a travinha tem de dar a volta livre sobre o aro')
pior=0.0
for d in range(0,360,15):
    M3r=gira(M3,d); v=max(vol(M3r,M1),vol(M3r,M2)); pior=max(pior,v)
    if v>=0.01: print('  *** trava em %d deg: %.4f mm3'%(d,v))
p('pior caso da travinha em 24 posicoes',pior)
print('\nVARREDURA — o aro dos meses gira sob a travinha')
enc=[];meio=[]
for d in range(0,360,15):
    M2r=gira(M2,d); v=max(vol(M2r,M1),vol(M2r,M3))
    (enc if d%30==0 else meio).append(v)
p('nas 12 posicoes de encaixe (tem de ser 0)',max(enc))
print('  %-36s %9.4f mm3  <- interferencia do DETENTE, e de projeto'
      %('entre encaixes (a mola passa por cima)',max(meio)))

print('\nALTURAS (aro de empilhamento da tampa em Y 39,72)')
for n,m in (('M01 valvula+dias',M1),('M02 aro dos meses',M2),('M03 travinha/seta',M3)):
    b=m.bounds; print('  %-20s Y %6.2f .. %6.2f   O%5.2f   folga ate o aro da tampa: %5.2f mm'
        %(n,b[0][1],b[1][1],max(b[1][0]-b[0][0],b[1][2]-b[0][2]),39.72-b[1][1]))

# ---------------------------------------------------------------- pino passante
print('\nPINO PASSANTE')
import numpy as np
from math import radians
v3=M3.vertices-np.array([CX,0,CZ]); r3=np.hypot(v3[:,0],v3[:,2])
v1=M1.vertices-np.array([CX,0,CZ]); r1=np.hypot(v1[:,0],v1[:,2])
print('  ponta do pino chega a Y %.2f  (face de baixo da valvula: 35,40)'%M3.bounds[0][1])
print('  atravessa a chapa? %s  — passa %.2f mm alem dela'
      %('SIM' if M3.bounds[0][1]<35.40 else 'NAO', 35.40-M3.bounds[0][1]))
fur=v1[(r1<3.2)&(v1[:,1]>35.3)&(v1[:,1]<35.5)]
rfuro=np.hypot(fur[:,0],fur[:,2]).max() if len(fur) else 0.0
print('  raio do furo na saida: %.2f'%rfuro)
far=v3[(v3[:,1]>35.35)&(v3[:,1]<35.45)]
print('  raio da farpa no ombro: %.2f  ->  encaixe radial %.2f mm'
      %(np.hypot(far[:,0],far[:,2]).max(), np.hypot(far[:,0],far[:,2]).max()-rfuro))
print('  folga ate o fundo do poco da tampa (Y 32,15): %.2f mm'%(M3.bounds[0][1]-32.15))

print('\nCURSO DO GANGORRA — a pergunta nao e "bate?", e "bate ANTES da original?"')
print('  (eixo das orelhas em 3h-9h, pivo em Y 34,69 — meia altura medida no STL)')
PIVO=34.69
def bascula(ms,g):
    out=[]
    for m in ms:
        n=m.copy(); n.apply_translation([-CX,-PIVO,-CZ])
        n.apply_transform(trimesh.transformations.rotation_matrix(radians(g),[1,0,0]))
        n.apply_translation([CX,PIVO,CZ]); out.append(n)
    return out
print('  %6s  %14s  %14s'%('graus','conjunto novo','valvula original'))
lim_n=lim_o=None
for g in [x*0.15 for x in range(-24,25)]:
    a,b,c2=bascula([M1,M2,M3],g); (o,)=bascula([V0],g)
    vn=max(vol(a,T),vol(b,T),vol(c2,T)); vo_=vol(o,T)
    if lim_n is None and abs(g)>0.01 and vn>vo+0.05: lim_n=g if g>0 else lim_n
    if abs(g) in (0.0,) or round(abs(g)/0.6,3)%1==0:
        print('  %+6.2f  %12.3f    %12.3f'%(g,vn,vo_))
print()
for sinal,nome in ((+1,'fechando (12h para baixo)'),(-1,'abrindo  (12h para cima) ')):
    gn=go=None
    for k in range(1,60):
        g=sinal*k*0.05
        if gn is None:
            a,b,c2=bascula([M1,M2,M3],g)
            if max(vol(a,T),vol(b,T),vol(c2,T))>vo+0.05: gn=abs(g)
        if go is None:
            (o,)=bascula([V0],g)
            if vol(o,T)>vo+0.05: go=abs(g)
        if gn is not None and go is not None: break
    print('  %s  novo trava em %s  |  original trava em %s  ->  %s'
          %(nome, ('%.2f graus'%gn) if gn else '>2,95', ('%.2f graus'%go) if go else '>2,95',
            'IGUAL' if (gn is None)==(go is None) and (gn is None or abs(gn-go)<1e-9) else 'DIFERENTE'))

# --------------------------------------------- as duas versoes da ponteira
print('\nAS DUAS VERSOES DA PONTEIRA')
for nome,m in (('M03a  M / D ',M3a),('M03b  janela',M3b)):
    b=m.bounds
    print('  %s  Y %6.2f..%6.2f  O%5.2f  massa %.2f g  folga ate o aro da tampa %.2f'
          %(nome,b[0][1],b[1][1],max(b[1][0]-b[0][0],b[1][2]-b[0][2]),m.volume*0.905/1000,39.72-b[1][1]))
    print('     x valvula %7.4f  x aro %7.4f  x tampa %7.4f mm3'%(vol(m,M1),vol(m,M2),vol(m,T)))
    pior=0.0
    for d in range(0,360,15):
        r=gira(m,d); pior=max(pior,vol(r,M1),vol(r,M2),vol(r,T))
    print('     varredura de 24 posicoes: pior caso %7.4f mm3  %s'%(pior,'ok' if pior<0.01 else '*** COLIDE ***'))
