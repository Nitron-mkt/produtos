import re, sys, numpy as np
from PIL import Image, ImageDraw
def paths(fn, zalvo, tol=0.01):
    segs=[]; x=y=z=None; ext=False; cur=[]
    for ln in open(fn,errors='ignore'):
        if ln.startswith(';Z:'):
            try: z=float(ln[3:]) 
            except: pass
            continue
        if not (ln.startswith('G1 ') or ln.startswith('G0 ')): continue
        d={}
        for t in ln.split()[1:]:
            if t[:1] in 'XYZEF':
                try: d[t[0]]=float(t[1:])
                except: pass
        nx=d.get('X',x); ny=d.get('Y',y)
        e=d.get('E')
        if z is not None and abs(z-zalvo)<tol and x is not None and nx is not None:
            if e is not None and e>0 and ('X' in d or 'Y' in d):
                cur.append((x,y)); cur.append((nx,ny))
        x,y=nx,ny
        if 'Z' in d: pass
    return cur
def plot(fn, zalvo, out, W=1500, lw=3):
    pts=paths(fn,zalvo)
    if not pts: print('nada em Z=%.2f'%zalvo); return
    P=np.array(pts); mn=P.min(0)-1; mx=P.max(0)+1
    sc=W/(mx[0]-mn[0]); H=int((mx[1]-mn[1])*sc)
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    for i in range(0,len(pts)-1,2):
        a,b=pts[i],pts[i+1]
        d.line([((a[0]-mn[0])*sc,H-(a[1]-mn[1])*sc),((b[0]-mn[0])*sc,H-(b[1]-mn[1])*sc)],
               fill=(30,80,170),width=lw)
    im.save(out); print(out, im.size, 'segmentos', len(pts)//2)
if __name__=='__main__':
    plot(sys.argv[1], float(sys.argv[2]), sys.argv[3])
