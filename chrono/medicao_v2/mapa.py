import numpy as np, trimesh, sys
from PIL import Image
sys.path.insert(0,'.')
from lib3d import CX, CZ
D='/home/user/produtos/chrono/stl_v2/'
def mapa(meshes, y0, y1, out, W=1000, span=42.0):
    tri=np.vstack([m.triangles for m in meshes])
    tri=tri-np.array([CX,0,CZ])
    # projeta em X (horizontal) e Z (vertical, para BAIXO na imagem = -Z)
    img=np.full((W,W),-1e9)
    sx=(0.5-tri[:,:,0]/span)*W; sy=(0.5-tri[:,:,2]/span)*W; sz=tri[:,:,1]   # de cima: direita do observador = -X, para cima = +Z
    for i in range(len(tri)):
        ax,ay=sx[i,0],sy[i,0]; bx,by=sx[i,1],sy[i,1]; cx,cy=sx[i,2],sy[i,2]
        den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(den)<1e-9: continue
        X0=max(int(min(ax,bx,cx)),0); X1=min(int(max(ax,bx,cx))+1,W-1)
        Y0=max(int(min(ay,by,cy)),0); Y1=min(int(max(ay,by,cy))+1,W-1)
        if X1<X0 or Y1<Y0: continue
        gx,gy=np.meshgrid(np.arange(X0,X1+1)+.5,np.arange(Y0,Y1+1)+.5)
        l1=((by-cy)*(gx-cx)+(cx-bx)*(gy-cy))/den
        l2=((cy-ay)*(gx-cx)+(ax-cx)*(gy-cy))/den
        l3=1-l1-l2; m=(l1>=-1e-9)&(l2>=-1e-9)&(l3>=-1e-9)
        if not m.any(): continue
        z=l1*sz[i,0]+l2*sz[i,1]+l3*sz[i,2]
        sub=img[Y0:Y1+1,X0:X1+1]; upd=m&(z>sub); sub[upd]=z[upd]
    v=np.clip((img-y0)/(y1-y0),0,1); v[img<-1e8]=np.nan
    rgb=np.zeros((W,W,3),np.uint8)
    g=(np.nan_to_num(v)*255).astype(np.uint8)
    rgb[...,0]=g; rgb[...,1]=g; rgb[...,2]=g
    rgb[np.isnan(v)]=255
    Image.fromarray(rgb).save(out); print(out,'gravado')
M1=trimesh.load(D+'Chrono_M01_Valvula_Dias.stl')
M2=trimesh.load(D+'Chrono_M02_Aro_Meses.stl')
M3=trimesh.load(D+'Chrono_M03_Travinha_Seta.stl')
mapa([M1],37.15,37.70,'n_dias.png')
mapa([M2],37.95,38.40,'n_meses.png')
mapa([M1,M2,M3],37.15,39.25,'n_conj.png')
