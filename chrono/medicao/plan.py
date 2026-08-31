import numpy as np, json
exec(open('chain.py').read().split('out={}')[0])
out={}
levels=[('rim',39.20),('band',38.50),('panel',38.24),('csk',37.60),('bore',36.00),('floor',31.70)]
for name,y in levels:
    segs=slice_plane(T,1,y)
    polys=[simplify(p,0.05) for p in chain(segs)]
    polys=[p for p in polys if len(p)>3]
    out['tampa_'+name]=[[[round(a,2),round(b,2)] for a,b in p] for p in polys]
    print('tampa',name,y,'polis',len(polys),'pts',sum(len(p) for p in polys))
segs=slice_plane(C,1,37.5); polys=[simplify(p,0.05) for p in chain(segs)]
out['corpo_aro']=[[[round(a,2),round(b,2)] for a,b in p] for p in polys if len(p)>3]
print('corpo aro polis',len(out['corpo_aro']))
json.dump(out,open('plantas.json','w'))
