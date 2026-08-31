import numpy as np
exec(open('slice.py').read().split("T=load(F['tampa'])")[0])
T=load(F['tampa']); V=load(F['valv'])
cx,cz=61.97,102.68
def circles(tris,y,box,name):
    s=slice_plane(tris,1,y)
    P=np.array([p for seg in s for p in seg])
    m=(P[:,0]>box[0])&(P[:,0]<box[1])&(P[:,1]>box[2])&(P[:,1]<box[3])
    Q=P[m]
    if len(Q)<6: print(name,'y=%.2f'%y,'poucos pontos',len(Q)); return
    c=Q.mean(0); r=np.sqrt(((Q-c)**2).sum(1))
    print('%s y=%.2f  n=%d centro=(%.2f,%.2f) dZ=%+.2f dX=%+.2f  r=%.2f..%.2f  Ø~%.2f'%(name,y,len(Q),c[0],c[1],c[1]-cz,c[0]-cx,r.min(),r.max(),2*r.mean()))
# vent hole on well floor
for y in [31.4,31.7,32.0]:
    circles(T,y,(cx-8,cx+8,cz+6,cz+19),'furo respiro')
# vent boss outer
for y in [33.0,34.0,35.0]:
    circles(T,y,(cx-14,cx+14,cz+2,cz+22),'ressalto respiro')
# lateral slots at 3 and 9 o'clock
for y in [33.5,35.0,36.5,37.0]:
    circles(T,y,(cx+20,cx+30,cz-6,cz+6),'rasgo 3h')
    circles(T,y,(cx-30,cx-20,cz-6,cz+6),'rasgo 9h')
# well bore: measure at several Y the min radius of the wall in the free quadrant (6h side)
for y in [33.0,34.0,35.0,36.0,37.0,37.6,38.0]:
    s=slice_plane(T,1,y)
    P=np.array([p for seg in s for p in seg])
    d=np.sqrt((P[:,0]-cx)**2+(P[:,1]-cz)**2)
    ang=np.degrees(np.arctan2(P[:,1]-cz,P[:,0]-cx))
    sel=(d<32)&(ang<-40)&(ang>-140)   # 6 o'clock quadrant, free of features
    if sel.sum(): print('  bore y=%.2f  r_min=%.2f (Ø%.2f)  r_max=%.2f'%(y,d[sel].min(),2*d[sel].min(),d[sel].max()))
# valve ears
for y in [33.5,34.5]:
    circles(V,y,(cx+18,cx+26,cz-5,cz+5),'orelha valv 3h')
