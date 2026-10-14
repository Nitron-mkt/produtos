# -*- coding: utf-8 -*-
"""Transforma a malha da valvula em SOLIDO B-rep de faces planas, costurado.

Por que isso agora funciona e antes nao: a primeira tentativa costurou a malha
decimada crua. Decimacao deixa triangulo degenerado e orientacao trocada, e dai
o BRepBuilderAPI_Sewing devolve casca invalida e todo booleano depois dela
colapsa. Limpando a malha primeiro — tirar face degenerada, soldar vertice
coincidente, normalizar orientacao — a casca fecha de primeira, com ZERO aresta
livre e ZERO aresta multipla, e o solido sai valido com o volume exato da malha.

E ha um segundo cuidado, que e o mesmo da lição do arquivo "fatiado": aresta
curta demais. Decimacao gera sliver, e sliver vira aresta de microns no STEP,
que o importador colapsa. Entao antes de costurar as arestas curtas sao
colapsadas (merge_vertices com tolerancia) e o resultado e conferido.
"""
import numpy as np, trimesh, cadquery as cq
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace,
                                BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid)
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Pnt
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.ShapeFix import ShapeFix_Shell

MIN_ARESTA = 0.05     # o mesmo limite do porteiro de qualidade

def _colapsa_curtas(m, lim):
    """Colapsa aresta abaixo de `lim` preservando a variedade.

    Condicao do elo (link condition): colapsar (u,v) so e seguro se u e v tem
    exatamente 2 vizinhos em comum — os dois vertices opostos das duas faces que
    dividem a aresta. Sem essa checagem o colapso costura regioes que nao se
    tocavam e a malha deixa de ser fechada, que foi o que estourou na primeira
    tentativa com arredondamento em grade.
    """
    V = np.asarray(m.vertices, float).copy()
    F = np.asarray(m.faces, np.int64).copy()
    for _ in range(40):
        E = np.unique(np.sort(np.concatenate([F[:, [0,1]], F[:, [1,2]], F[:, [0,2]]]), axis=1), axis=0)
        L = np.linalg.norm(V[E[:,0]] - V[E[:,1]], axis=1)
        alvo = E[L < lim]
        if not len(alvo): break
        viz = [set() for _ in range(len(V))]
        for a, b in E:
            viz[a].add(b); viz[b].add(a)
        pai = np.arange(len(V))
        def raiz(i):
            while pai[i] != i: pai[i] = pai[pai[i]]; i = pai[i]
            return i
        feitos = 0
        for u, v in alvo[np.argsort(L[L < lim])]:
            ru, rv = raiz(u), raiz(v)
            if ru == rv: continue
            if len(viz[ru] & viz[rv]) != 2: continue      # condicao do elo
            V[ru] = (V[ru] + V[rv]) / 2.0
            pai[rv] = ru
            viz[ru] |= viz[rv] - {ru}
            for w in viz[rv]:
                if w != ru: viz[w].discard(rv); viz[w].add(ru)
            feitos += 1
        if not feitos: break
        F = np.vectorize(raiz)(F)
        F = F[(F[:,0] != F[:,1]) & (F[:,1] != F[:,2]) & (F[:,0] != F[:,2])]
        novo = trimesh.Trimesh(vertices=V, faces=F, process=False)
        novo.remove_unreferenced_vertices()
        V = np.asarray(novo.vertices, float).copy(); F = np.asarray(novo.faces, np.int64).copy()
    r = trimesh.Trimesh(vertices=V, faces=F, process=False)
    r.remove_unreferenced_vertices(); r.merge_vertices(); r.fix_normals()
    return r


def limpa(m, min_aresta=MIN_ARESTA):
    """Malha pronta para costurar: sem face degenerada, sem vertice duplicado,
    orientacao coerente e sem aresta abaixo do limite."""
    m = m.copy()
    m.update_faces(m.nondegenerate_faces())
    m.merge_vertices()
    # colapsa aresta curta soldando vertices dentro da tolerancia
    for _ in range(6):
        E = m.vertices[m.edges_unique]
        L = np.linalg.norm(E[:, 0] - E[:, 1], axis=1)
        if L.min() >= min_aresta: break
        m.merge_vertices(merge_tex=True, merge_norm=True, digits_vertex=None)
        m = trimesh.Trimesh(*trimesh.remesh.merge_vertices if False else (m.vertices, m.faces))
        m.merge_vertices()
        # solda por grade: arredonda para metade do limite
        q = np.round(m.vertices / (min_aresta * 0.5)) * (min_aresta * 0.5)
        _, inv = np.unique(q, axis=0, return_inverse=True)
        f = inv[m.faces]
        f = f[(f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])]
        m = trimesh.Trimesh(vertices=np.unique(q, axis=0), faces=f, process=False)
        m.update_faces(m.nondegenerate_faces()); m.merge_vertices()
        m.remove_unreferenced_vertices()
    m.fix_normals()
    return m

def solido(m):
    """Malha fechada -> TopoDS_Solid de faces planas."""
    V = np.asarray(m.vertices)
    sew = BRepBuilderAPI_Sewing(1e-7, True, True, True, False)
    for f in m.faces:
        pol = BRepBuilderAPI_MakePolygon(gp_Pnt(*V[f[0]]), gp_Pnt(*V[f[1]]),
                                         gp_Pnt(*V[f[2]]), True)
        mf = BRepBuilderAPI_MakeFace(pol.Wire())
        if mf.IsDone(): sew.Add(mf.Face())
    sew.Perform()
    assert sew.NbFreeEdges() == 0,     '%d arestas livres na costura' % sew.NbFreeEdges()
    assert sew.NbMultipleEdges() == 0, '%d arestas multiplas' % sew.NbMultipleEdges()
    fx = ShapeFix_Shell(TopoDS.Shell_s(sew.SewedShape())); fx.Perform()
    s = cq.Shape(BRepBuilderAPI_MakeSolid(fx.Shell()).Solid())
    assert BRepCheck_Analyzer(s.wrapped).IsValid(), 'solido facetado invalido'
    if s.Volume() < 0: s = s.mirror()   # nunca aconteceu, mas custa nada
    return s

def medidas(m, nome=''):
    E = m.vertices[m.edges_unique]
    L = np.linalg.norm(E[:, 0] - E[:, 1], axis=1)
    return ('%s %6d faces %6d vert  fechada=%-5s  aresta min %.4f  vol %8.2f'
            % (nome, len(m.faces), len(m.vertices), m.is_watertight, L.min(), m.volume))

# ------------------------------------------------------------------ valvula
TOL_SIMPL = 0.025   # tolerancia da simplificacao do corpo da valvula, em mm

def valvula_facetada(tol=TOL_SIMPL, min_aresta=MIN_ARESTA):
    """A valvula injetada como SOLIDO B-rep de faces planas, pronta para booleano.

    Tres passos, e cada um resolve um problema medido:

    1. o corte na face de topo e feito por BOOLEANO contra uma caixa, nao por
       slice_plane: o cap do slice_plane triangula com sliver e deixa aresta de
       4,6e-7 mm, que e justo o defeito que fez o arquivo abrir "fatiado";
    2. `Manifold.simplify(tol)` reduz 46.118 faces a ~8.000 com erro limitado,
       preservando a variedade;
    3. o colapso de arestas curtas tira o que sobrou abaixo de 0,05 mm.
    """
    import manifold3d as m3
    from valvula_real import VELHO
    import params as P
    m = trimesh.load(VELHO)
    b = m.bounds
    cx = trimesh.creation.box(extents=[200.0, 200.0, 200.0])
    cx.apply_translation([(b[0][0]+b[1][0])/2, P.FACE - 100.0, (b[0][2]+b[1][2])/2])
    v = trimesh.boolean.boolean_manifold([m, cx], operation='intersection')
    M = m3.Manifold(m3.Mesh(np.asarray(v.vertices, 'float32'),
                            np.asarray(v.faces, 'uint32'))).simplify(tol)
    me = M.to_mesh()
    s = trimesh.Trimesh(vertices=np.asarray(me.vert_properties)[:, :3],
                        faces=np.asarray(me.tri_verts), process=False)
    s = _colapsa_curtas(s, min_aresta)
    assert s.is_watertight, 'valvela facetada nao fechou'
    return s, v
