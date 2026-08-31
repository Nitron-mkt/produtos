import json, numpy as np
exec(open('chain.py').read().split('out={}')[0])
cx,cz=61.97,102.68
def get(tris,axis,val,eps):
    segs=slice_plane(tris,axis,val)
    return [simplify(p,eps) for p in chain(segs) if len(p)>3]
def swapZY(polys):   # axis=0 slice gives (Y,Z) -> return (Z-cz, Y)
    return [[[b-cz,a] for a,b in p] for p in polys]
def clipbox(polys, xr, yr):
    out=[]
    for p in polys:
        cur=[]
        for a,b in p:
            if xr[0]<=a<=xr[1] and yr[0]<=b<=yr[1]: cur.append([round(a,3),round(b,3)])
            else:
                if len(cur)>2: out.append(cur)
                cur=[]
        if len(cur)>2: out.append(cur)
    return out
def rnd(polys,nd=2): return [[[round(a,nd),round(b,nd)] for a,b in p] for p in polys]
def fmtplan(polys,nd=2): return [[[round(a-cx,nd),round(b-cz,nd)] for a,b in p] for p in polys]

data={'plan':{},'sec':{},'wide':{}}
data['plan']['aro']=fmtplan(get(T,1,39.20,0.35))
data['plan']['painel']=fmtplan(get(T,1,38.24,0.35))
data['plan']['furo']=fmtplan(get(T,1,36.00,0.25))
for k,v in data['plan'].items(): print('plan',k,len(v),sum(len(p) for p in v))

secT=swapZY(get(T,0,cx,0.02)); secV=swapZY(get(V,0,cx,0.02)); secC=swapZY(get(C,0,cx,0.05))
data['sec']['tampa']=clipbox(secT,(-27,27),(29,41))
data['sec']['valv'] =clipbox(secV,(-27,27),(29,41))
data['sec']['corpo']=clipbox(secC,(-27,27),(29,41))
for k,v in data['sec'].items(): print('sec',k,len(v),sum(len(p) for p in v))

data['wide']['tampa']=rnd(swapZY(get(T,0,cx,0.06)))
data['wide']['corpo']=rnd(swapZY(get(C,0,cx,0.06)))
data['wide']['valv'] =rnd(swapZY(get(V,0,cx,0.04)))
for k,v in data['wide'].items(): print('wide',k,len(v),sum(len(p) for p in v))
s=json.dumps(data,separators=(',',':'))
open('geo.json','w').write(s); print('bytes',len(s))
