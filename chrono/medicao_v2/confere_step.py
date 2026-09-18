# -*- coding: utf-8 -*-
"""Prova objetiva de que o STEP e a mesma peca do STL validado:
tessela o STEP, compara volume, caixa e a maior distancia entre as duas
superficies nos dois sentidos.  python3 confere_step.py"""
import sys, numpy as np, trimesh, cadquery as cq
from cadquery.occ_impl.shapes import Shape
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

STEP='/home/user/produtos/chrono/step_v2'; STL='/home/user/produtos/chrono/stl_v2'

def tessela(arq, lin=0.01, ang=0.1):
    sh = cq.importers.importStep(arq).val().wrapped
    BRepMesh_IncrementalMesh(sh, lin, False, ang, True)
    V=[]; F=[]
    ex = TopExp_Explorer(sh, TopAbs_FACE)
    while ex.More():
        f = TopoDS.Face_s(ex.Current()); loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(f, loc)
        if tri is not None:
            tr = loc.Transformation(); off = len(V)
            for i in range(1, tri.NbNodes()+1):
                p = tri.Node(i).Transformed(tr); V.append((p.X(), p.Y(), p.Z()))
            rev = f.Orientation() == 1
            for i in range(1, tri.NbTriangles()+1):
                a, b, c = tri.Triangle(i).Get()
                F.append((off+a-1, off+c-1, off+b-1) if rev else (off+a-1, off+b-1, off+c-1))
        ex.Next()
    m = trimesh.Trimesh(vertices=np.array(V), faces=np.array(F), process=True)
    # a tesselacao do OCC repete vertice na costura entre faces: sem soldar,
    # a malha nao fecha e o booleano recusa
    for d in (8, 6, 5, 4):
        if m.is_volume: break
        m.merge_vertices(digits_vertex=d)
        m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
        trimesh.repair.fill_holes(m); trimesh.repair.fix_normals(m)
    return m

def dist(a, b, n=60000):
    p = a.sample(n)
    return trimesh.proximity.closest_point(b, p)[1]

def main(nomes):
  for nome in nomes:
      m = tessela(f'{STEP}/{nome}.step'); s = trimesh.load(f'{STL}/{nome}.stl')
      d1 = dist(s, m); d2 = dist(m, s)
      print('%s' % nome)
      print('   volume   STEP %8.2f   STL %8.2f   dif %+.3f%%' %
            (m.volume, s.volume, 100*(m.volume-s.volume)/s.volume))
      print('   caixa    STEP %s' % np.round(m.bounds[1]-m.bounds[0], 3))
      print('            STL  %s' % np.round(s.bounds[1]-s.bounds[0], 3))
      print('   centro   dif  %s mm' % np.round(m.bounds.mean(0)-s.bounds.mean(0), 4))
      print('   desvio   STL->STEP  med %.4f  max %.4f mm' % (d1.mean(), d1.max()))
      print('            STEP->STL  med %.4f  max %.4f mm' % (d2.mean(), d2.max()))
      print('   solido:  STEP %s   STL %s' % (m.is_volume, s.is_volume))

if __name__ == '__main__':
    main(sys.argv[1:] or ['Chrono_M02_Rodinha_Meses', 'Chrono_M03_Ponteira'])
