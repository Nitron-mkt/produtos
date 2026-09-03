import struct, sys, os, zlib
import numpy as np

def read(p):
    d=open(p,'rb').read(); n=struct.unpack('<I',d[80:84])[0]
    a=np.frombuffer(d[84:84+50*n],dtype=np.dtype([('n','<3f4'),('v','<3,3f4'),('a','<u2')]),count=n)
    return a['v'].astype(np.float64)

def crossings_z(T, step=0.6):
    """para cada (x,y) da grade, devolve os z de interseccao ordenados"""
    V=T.reshape(-1,3); mn=V.min(0); mx=V.max(0)
    gx=np.arange(mn[0]+0.13, mx[0], step); gy=np.arange(mn[1]+0.17, mx[1], step)
    GX,GY=np.meshgrid(gx,gy,indexing='ij'); P=np.stack([GX.ravel(),GY.ravel()],1)
    A=T[:,0,:]; e1=T[:,1,:]-A; e2=T[:,2,:]-A
    det=e1[:,0]*e2[:,1]-e1[:,1]*e2[:,0]; ok=np.abs(det)>1e-12
    a0,a1,az=A[ok][:,0],A[ok][:,1],A[ok][:,2]
    u1,v1,w1=e1[ok][:,0],e1[ok][:,1],e1[ok][:,2]
    u2,v2,w2=e2[ok][:,0],e2[ok][:,1],e2[ok][:,2]; det=det[ok]
    out=[]
    for s in range(0,len(P),900):
        pp=P[s:s+900]
        r0=pp[:,0:1]-a0[None,:]; r1=pp[:,1:2]-a1[None,:]
        uu=( r0*v2[None,:]-r1*u2[None,:])/det[None,:]
        vv=(-r0*v1[None,:]+r1*u1[None,:])/det[None,:]
        ins=(uu>=0)&(vv>=0)&(uu+vv<=1)
        t=az[None,:]+uu*w1[None,:]+vv*w2[None,:]
        for r in range(pp.shape[0]):
            out.append(np.sort(t[r][ins[r]]))
    return P, out, mn, mx, step

def inside_at(hits, z):
    return (np.searchsorted(hits, z) % 2)==1

NAME={'576b9a53-Pe_a_01_Trizeta.STL':'TRIZETA 850-TZ','d346a5c8-Pe_a_Cruzeta.STL':'CRUZETA 850-CZ'}
for path in sys.argv[1:]:
    T=read(path); P,H,mn,mx,step=crossings_z(T)
    nm=NAME.get(os.path.basename(path),path)
    cell=step*step
    print(f"===== {nm}   Z de {mn[2]:.2f} a {mx[2]:.2f}  (altura {mx[2]-mn[2]:.2f} mm)")
    print(f"   {'z (mm)':>9} {'z rel':>7} {'area macica':>13} {'% do bbox XY':>13}")
    bbox_xy=(mx[0]-mn[0])*(mx[1]-mn[1])
    perfil=[]
    for frac in np.arange(0.02,1.0,0.04):
        z=mn[2]+frac*(mx[2]-mn[2])
        area=sum(cell for h in H if inside_at(h,z))
        perfil.append((z, z-mn[2], area, area/bbox_xy*100))
    for z,zr,a,pc in perfil:
        bar='#'*int(pc/2)
        print(f"   {z:9.2f} {zr:7.2f} {a:11.0f} mm2 {pc:11.1f}%  {bar}")
    amin=min(perfil,key=lambda r:r[2]); amax=max(perfil,key=lambda r:r[2])
    print(f"   MIN de area macica: {amin[2]:.0f} mm2 em z={amin[0]:.2f} (z rel {amin[1]:.2f})")
    print(f"   MAX de area macica: {amax[2]:.0f} mm2 em z={amax[0]:.2f} (z rel {amax[1]:.2f})")
    print()
