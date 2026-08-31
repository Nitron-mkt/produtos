import struct, glob, os, math
import numpy as np

D='/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/'
def load(fn):
    with open(fn,'rb') as f:
        f.read(80); n=struct.unpack('<I',f.read(4))[0]
        data=np.frombuffer(f.read(n*50), dtype=np.uint8)
    data=data.reshape(n,50)
    verts=data[:,12:48].copy().view('<f4').reshape(n,3,3)
    norms=data[:,0:12].copy().view('<f4').reshape(n,3)
    return verts, norms

for fn in sorted(glob.glob(D+'*.STL')):
    v,nm=load(fn)
    p=v.reshape(-1,3)
    mn=p.min(0); mx=p.max(0)
    print('===', os.path.basename(fn))
    print('  tris', len(v))
    print('  min', np.round(mn,3), 'max', np.round(mx,3))
    print('  dims', np.round(mx-mn,3))
    # volume via divergence theorem
    a,b,c = v[:,0], v[:,1], v[:,2]
    vol = np.abs(np.einsum('ij,ij->i', a, np.cross(b,c)).sum()/6.0)
    print('  volume mm3', round(float(vol),1), ' -> g PP(0.905):', round(float(vol)*0.905/1000,2))
