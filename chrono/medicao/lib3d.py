import numpy as np, trimesh
from math import pi, cos, sin
from shapely.geometry import Polygon as SPoly
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

CX, CZ = 61.97, 102.68          # centro do poco, no sistema dos STL originais
TOPV   = 37.23                  # face de topo da valvula
TOPR   = 38.20                  # topo dos aneis / do pino
BOTR   = 37.25                  # base dos aneis

def revolve(prof, n=288):
    """prof: lista fechada de (r,y) -> solido de revolucao em torno de Y."""
    m=len(prof); V=np.empty((n*m,3)); F=[]
    for k in range(n):
        a=2*pi*k/n; c,s=cos(a),sin(a)
        for j,(r,y) in enumerate(prof):
            V[k*m+j]=(r*c, y, r*s)
    for k in range(n):
        k2=(k+1)%n
        for j in range(m):
            j2=(j+1)%m
            a=k*m+j; b=k*m+j2; c_=k2*m+j2; d=k2*m+j
            F.append([a,b,c_]); F.append([a,c_,d])
    ms=trimesh.Trimesh(vertices=V, faces=np.array(F), process=True)
    trimesh.repair.fix_normals(ms)
    return ms

def cyl(r,y0,y1,n=64,cx=0.0,cz=0.0):
    m=trimesh.creation.cylinder(radius=r, height=y1-y0, sections=n)
    m.apply_transform(trimesh.transformations.rotation_matrix(pi/2,[1,0,0]))
    m.apply_translation([cx,(y0+y1)/2,cz]); return m

def ball(r,cx,cy,cz,n=3):
    m=trimesh.creation.icosphere(subdivisions=n, radius=r)
    m.apply_translation([cx,cy,cz]); return m

_FP=FontProperties(family="DejaVu Sans", weight="bold")
def glyph_polys(txt, cap):
    """poligonos 2D do texto, centrados, altura de caixa alta = cap."""
    tp=TextPath((0,0), txt, size=1.0, prop=_FP)
    polys=[np.asarray(p) for p in tp.to_polygons() if len(p)>=3]
    if not polys: return []
    ref=TextPath((0,0),"8",size=1.0,prop=_FP)
    h=ref.get_extents().height
    k=cap/h
    allp=np.vstack(polys); mn=allp.min(0); mx=allp.max(0); c=(mn+mx)/2
    return [ (p-c)*k for p in polys ]

def polys_to_shapely(polys):
    """monta poligonos com furos por continencia."""
    sp=[SPoly(p) for p in polys]
    sp=[p.buffer(0) if not p.is_valid else p for p in sp]
    order=sorted(range(len(sp)), key=lambda i:-sp[i].area)
    used=set(); out=[]
    for i in order:
        if i in used: continue
        holes=[]
        for j in order:
            if j==i or j in used: continue
            if sp[i].contains(sp[j]):
                holes.append(list(sp[j].exterior.coords)); used.add(j)
        used.add(i)
        out.append(SPoly(list(sp[i].exterior.coords), holes))
    return out

def place(mesh, phi, R, top, depth):
    """leva um prisma local (x=tangencial, y=radial, z=0..depth) para o anel."""
    c,s=cos(phi),sin(phi)
    et=np.array([-s,0,c]); er=np.array([c,0,s]); ey=np.array([0,1,0])
    M=np.eye(4)
    M[:3,0]=et; M[:3,1]=er; M[:3,2]=ey
    M[:3,3]=np.array([0,0,0])+R*er+(top-depth)*ey
    m=mesh.copy(); m.apply_transform(M); return m

def text_cutters(items, R, cap, depth, top=TOPR):
    """items: [(phi_rad, texto)] -> uma malha unica de prismas de gravacao."""
    cs=[]
    for phi,txt in items:
        for sp in polys_to_shapely(glyph_polys(txt,cap)):
            pr=trimesh.creation.extrude_polygon(sp, height=depth)
            cs.append(place(pr,phi,R,top,depth))
    return trimesh.util.concatenate(cs)

def boolean(op, meshes):
    return trimesh.boolean.boolean_manifold(meshes, operation=op)
