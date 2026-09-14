import sys, trimesh, numpy as np
sys.path.insert(0,'.')
from lib3d import boolean, CX, CZ
from math import radians
D='/home/user/produtos/chrono/stl_v2/'
M1=trimesh.load(D+'Chrono_M01_Valvula_Dias.stl')
M2=trimesh.load(D+'Chrono_M02_Aro_Meses.stl')
M3=trimesh.load(D+'Chrono_M03_Travinha_Seta.stl')
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
