"""Extrai o icone da Nitron do PDF e devolve poligonos 2D ja centrados,
com Y para cima e altura normalizada em 1,0. Fonte: icone_nitron.pdf (vetor)."""
import numpy as np, pymupdf
from shapely.geometry import Polygon as SP
PDF='/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/7f6ce8c6-icone_nitron.pdf'

def _bez(p0,p1,p2,p3,n=24):
    t=np.linspace(0,1,n)[1:,None]
    return ((1-t)**3*p0 + 3*(1-t)**2*t*p1 + 3*(1-t)*t**2*p2 + t**3*p3)

def contornos():
    p=pymupdf.open(PDF)[0]
    saida=[]
    for g in p.get_drawings():
        pts=[]
        for it in g['items']:
            if it[0]=='l':
                a,b=it[1],it[2]
                if not pts: pts.append([a.x,a.y])
                pts.append([b.x,b.y])
            elif it[0]=='c':
                a,b,c,dd=it[1],it[2],it[3],it[4]
                if not pts: pts.append([a.x,a.y])
                pts.extend(_bez(*[np.array([q.x,q.y]) for q in (a,b,c,dd)]).tolist())
        if len(pts)>=3: saida.append(np.array(pts))
    todos=np.vstack(saida)
    mn,mx=todos.min(0),todos.max(0); c=(mn+mx)/2; h=mx[1]-mn[1]
    # PDF tem Y para baixo: espelha
    return [ (np.c_[(q[:,0]-c[0])/h, -(q[:,1]-c[1])/h]) for q in saida ]

def shapely(altura):
    out=[]
    for q in contornos():
        s=SP(q*altura)
        if not s.is_valid: s=s.buffer(0)
        if s.geom_type=='Polygon' and s.area>1e-9: out.append(s)
        elif s.geom_type=='MultiPolygon': out+= [g for g in s.geoms if g.area>1e-9]
    return out

if __name__=='__main__':
    for a in (6.0,8.0,10.0):
        ps=shapely(a)
        b=[p.bounds for p in ps]
        x0=min(t[0] for t in b); x1=max(t[2] for t in b)
        y0=min(t[1] for t in b); y1=max(t[3] for t in b)
        # traco mais fino de cada lamina
        fin=[]
        for p in ps:
            lo,hi=0.0,3.0
            for _ in range(40):
                md=(lo+hi)/2
                if p.buffer(-md).is_empty: hi=md
                else: lo=md
            fin.append(2*lo)
        print('altura %.1f mm -> %d laminas, caixa %.2f x %.2f, area %.2f mm2, traco min %.2f'
              %(a,len(ps),x1-x0,y1-y0,sum(p.area for p in ps),min(fin)))

def poligonos(altura, xflip=False):
    """Poligonos shapely do icone, centrados, com a altura pedida em mm.
    xflip espelha em X — necessario quando o icone e GRAVADO na face de topo:
    a matriz de place/grava inverte a mao, e sem o espelho o N sai ao contrario."""
    out=shapely(altura)
    if xflip:
        from shapely import affinity
        out=[affinity.scale(p, xfact=-1.0, yfact=1.0, origin=(0,0)) for p in out]
    return out
