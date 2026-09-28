# -*- coding: utf-8 -*-
"""Tesselacao do STEP para malha. Cada SOLIDO e malhado e soldado sozinho:
juntar 56 solidos soltos numa malha so antes de soldar deixa costura aberta e o
booleano recusa ('Not all meshes are volumes')."""
import numpy as np, trimesh, cadquery as cq
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS

def _malha(sh, lin=0.020, ang=0.25):
    BRepMesh_IncrementalMesh(sh, lin, False, ang, True)
    V, F = [], []
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
                x, y, z = tri.Triangle(i).Get()
                F.append((off+x-1, off+z-1, off+y-1) if rev else (off+x-1, off+y-1, off+z-1))
        ex.Next()
    m = trimesh.Trimesh(vertices=np.array(V), faces=np.array(F), process=True)
    for dg in (8, 6, 5, 4):
        if m.is_volume: break
        m.merge_vertices(digits_vertex=dg)
        m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
        trimesh.repair.fill_holes(m); trimesh.repair.fix_normals(m)
    return m

def tessela(arq, aviso=True):
    sh = cq.importers.importStep(arq).val()
    ms = [_malha(s.wrapped) for s in sh.Solids()]
    ruins = [i for i, m in enumerate(ms) if not m.is_volume]
    if ruins and aviso:
        print('      *** %d de %d solidos nao fecharam em %s ***'
              % (len(ruins), len(ms), arq.split('/')[-1]))
    return trimesh.util.concatenate(ms) if len(ms) > 1 else ms[0]
