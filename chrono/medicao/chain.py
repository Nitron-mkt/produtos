import numpy as np, json
exec(open('slice.py').read().split("T=load(F['tampa'])")[0])
T=load(F['tampa']); C=load(F['corpo']); V=load(F['valv'])
cx,cz=61.97,102.68

def chain(segs, tol=0.02):
    from collections import defaultdict
    key=lambda p:(round(p[0]/tol),round(p[1]/tol))
    adj=defaultdict(list); pts={}
    for a,b in segs:
        ka,kb=key(a),key(b)
        if ka==kb: continue
        pts[ka]=a; pts[kb]=b
        adj[ka].append(kb); adj[kb].append(ka)
    used=set(); polys=[]
    for start in list(adj):
        if start in used: continue
        # walk
        poly=[start]; used.add(start); cur=start; prev=None
        while True:
            nxt=[k for k in adj[cur] if k!=prev and k not in used]
            if not nxt: break
            prev=cur; cur=nxt[0]; used.add(cur); poly.append(cur)
        if len(poly)>3: polys.append([pts[k] for k in poly])
    return polys

def simplify(pl, eps=0.03):
    # Douglas-Peucker
    P=np.array(pl)
    def dp(i,j):
        if j<=i+1: return [i]
        a,b=P[i],P[j]; d=b-a; L=np.hypot(*d)
        if L<1e-9:
            dist=np.hypot(*(P[i+1:j]-a).T)
        else:
            dist=np.abs(np.cross(d, P[i+1:j]-a))/L
        k=int(np.argmax(dist))+i+1
        if dist.max()<eps: return [i]
        return dp(i,k)+dp(k,j)
    import sys; sys.setrecursionlimit(10000)
    idx=dp(0,len(P)-1)+[len(P)-1]
    return P[idx].tolist()

out={}
for name,tris,axis,val in [('tampa_ZY',T,0,cx),('corpo_ZY',C,0,cx),('valv_ZY',V,0,cx),
                           ('tampa_XY',T,2,cz),('corpo_XY',C,2,cz),('valv_XY',V,2,cz)]:
    segs=slice_plane(tris,axis,val)
    polys=[simplify(p,0.025) for p in chain(segs)]
    polys=[p for p in polys if len(p)>3]
    out[name]=[[[round(a,3),round(b,3)] for a,b in p] for p in polys]
    print(name,'polilinhas',len(polys),'pontos',sum(len(p) for p in polys))
json.dump(out,open('secoes.json','w'))
