import struct, numpy as np
D='/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/'
F={'tampa':D+'1c50a47b-Mont_pote_com_valvula__Tampa_Pote_025_Pequeno_Cav1.STL',
   'corpo':D+'25c15f02-Mont_pote_com_valvula__Corpo_Pote_025_Pequeno_Cav1.STL',
   'valv': D+'5882c071-Mont_pote_com_valvula__prova_valvula1.STL'}
def load(fn):
    with open(fn,'rb') as f:
        f.read(80); n=struct.unpack('<I',f.read(4))[0]
        d=np.frombuffer(f.read(n*50),dtype=np.uint8).reshape(n,50)
    return d[:,12:48].copy().view('<f4').reshape(n,3,3).astype(np.float64)

def slice_plane(tris, axis, val):
    """return list of 2D segments (other two axes) """
    segs=[]
    other=[i for i in range(3) if i!=axis]
    d=tris[:,:,axis]-val
    sign=d>0
    cnt=sign.sum(1)
    m=(cnt==1)|(cnt==2)
    T=tris[m]; dd=d[m]
    for tri,dv in zip(T,dd):
        pts=[]
        for i in range(3):
            j=(i+1)%3
            if (dv[i]>0)!=(dv[j]>0):
                t=dv[i]/(dv[i]-dv[j])
                p=tri[i]+t*(tri[j]-tri[i])
                pts.append((p[other[0]],p[other[1]]))
        if len(pts)==2: segs.append(pts)
    return segs

T=load(F['tampa']); C=load(F['corpo']); V=load(F['valv'])
# center of valve
pv=V.reshape(-1,3); cx=(pv[:,0].min()+pv[:,0].max())/2; cz=(pv[:,2].min()+pv[:,2].max())/2
print('valve center X,Z =',round(cx,2),round(cz,2))
# valve radial profile: distance from axis vs Y
r=np.sqrt((pv[:,0]-cx)**2+(pv[:,2]-cz)**2)
print('valve r max',round(r.max(),2),'  (X-only extent):',round((pv[:,0].max()-pv[:,0].min())/2,2),' Z-only:',round((pv[:,2].max()-pv[:,2].min())/2,2))
import collections
# histogram of radius at several Y levels
for y0 in [32.8,33.5,34.5,35.5,36.5,37.0,37.5,38.0]:
    s=slice_plane(V,1,y0)
    if not s: print('  valve Y=%.1f: vazio'%y0); continue
    P=np.array([p for seg in s for p in seg])
    rr=np.sqrt((P[:,0]-cx)**2+(P[:,1]-cz)**2)
    print('  valve Y=%.1f: r %.2f..%.2f  (Ø %.2f..%.2f) segs=%d'%(y0,rr.min(),rr.max(),2*rr.min(),2*rr.max(),len(s)))
print()
for y0 in [31.5,32.5,33.5,35.0,36.5,37.0,37.6,38.0,38.5,39.0,39.5]:
    s=slice_plane(T,1,y0)
    if not s: print('  tampa Y=%.1f: vazio'%y0); continue
    P=np.array([p for seg in s for p in seg])
    rr=np.sqrt((P[:,0]-cx)**2+(P[:,1]-cz)**2)
    # look only near center
    near=rr<40
    print('  tampa Y=%.1f: segs=%d ; perto do centro r %.2f..%.2f (Ø int %.2f)'%(y0,len(s), rr[near].min() if near.any() else -1, rr[near].max() if near.any() else -1, 2*rr[near].min() if near.any() else -1))
