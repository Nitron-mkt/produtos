# -*- coding: utf-8 -*-
"""Mapa de altura v2 x v3, visto de cima. Mostra o que mudou sem depender de
sombreamento: cada patamar vira uma cor."""
import sys, os, numpy as np, trimesh, matplotlib
matplotlib.use('Agg'); from matplotlib import cm
from PIL import Image, ImageDraw
CX, CZ = 61.97, 102.68
def mapa(arq, R, N=900, lo=None, hi=None):
    m = trimesh.load(arq); V = m.triangles
    X = (V[:,:,0]-(CX-R))/(2*R)*N; Y = ((CZ+R)-V[:,:,2])/(2*R)*N; Z = V[:,:,1]
    zb = np.full((N,N), -1e18)
    for i in range(len(V)):
        ax,ay=X[i,0],Y[i,0]; bx,by=X[i,1],Y[i,1]; cx,cy=X[i,2],Y[i,2]
        den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(den)<1e-12: continue
        X0=max(int(min(ax,bx,cx)),0); X1=min(int(max(ax,bx,cx))+1,N-1)
        Y0=max(int(min(ay,by,cy)),0); Y1=min(int(max(ay,by,cy))+1,N-1)
        if X1<X0 or Y1<Y0: continue
        gx,gy=np.meshgrid(np.arange(X0,X1+1)+.5,np.arange(Y0,Y1+1)+.5)
        l1=((by-cy)*(gx-cx)+(cx-bx)*(gy-cy))/den
        l2=((cy-ay)*(gx-cx)+(ax-cx)*(gy-cy))/den
        msk=(l1>=-1e-9)&(l2>=-1e-9)&(l1+l2<=1+1e-9)
        if not msk.any(): continue
        z=l1*Z[i,0]+l2*Z[i,1]+(1-l1-l2)*Z[i,2]
        sub=zb[Y0:Y1+1,X0:X1+1]; up=msk&(z>sub); sub[up]=z[up]
    ok=zb>-1e17
    lo = np.percentile(zb[ok],1) if lo is None else lo
    hi = zb[ok].max() if hi is None else hi
    img=(cm.turbo(np.clip((zb-lo)/(hi-lo),0,1))[:,:,:3]*255).astype(np.uint8)
    img[~ok]=(246,244,240)
    return Image.fromarray(img)

def painel(pares, saida, R, lo, hi, N=900):
    ims=[mapa(a,R,N,lo,hi) for _,a in pares]
    W=N*len(ims); cv=Image.new('RGB',(W,N+34),(246,244,240)); d=ImageDraw.Draw(cv)
    for k,(t,_) in enumerate(pares):
        cv.paste(ims[k],(k*N,34)); d.text((k*N+12,12), t, fill=(30,26,22))
    cv.save(saida); print(saida, cv.size)

painel([('v2  —  passo constante, o vao do zero sobrou em 1..9',
         '../stl_v2/Chrono_M01_Valvula_Dias.stl'),
        ('v3  —  vao igual entre as bordas dos 31, concha enchida, detente O2,00 centrado',
         'stl/Chrono_v3_M01_Valvula_Dias.stl')],
       'comparacao_M01.png', R=20.0, lo=35.4, hi=38.30)
painel([('v2  —  M e D gravados, icone rebaixado',  '../stl_v2/Chrono_M03_Ponteira.stl'),
        ('v3  —  MES em auto relevo, D removido, icone em auto relevo',
         'stl/Chrono_v3_M03_Ponteira.stl')],
       'comparacao_M03.png', R=14.0, lo=38.3, hi=39.96)
painel([('v2  —  numerais gravados 0,30',  '../stl_v2/Chrono_M02_Rodinha_Meses.stl'),
        ('v3  —  numerais em auto relevo 0,10, covinhas O2,00 em r 10,10',
         'stl/Chrono_v3_M02_Rodinha_Meses.stl')],
       'comparacao_M02.png', R=14.5, lo=36.6, hi=38.26)
