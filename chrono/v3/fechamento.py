# -*- coding: utf-8 -*-
"""Conferencia de FECHAMENTO do STEP — o que decide se o SolidWorks abre a peca
como solido ou como um monte de superficie solta.

O porteiro `qualidade.py` olha o tamanho das arestas e das faces. Este aqui olha
se a peca FECHA. Sao coisas diferentes: o arquivo da v3 que abriu "fatiado" ja
tinha MANIFOLD_SOLID_BREP no cabecalho e mesmo assim nao costurava.

O que e conferido, arquivo por arquivo:

 1. o texto do STEP declara MANIFOLD_SOLID_BREP e CLOSED_SHELL, e nao
    SHELL_BASED_SURFACE_MODEL (que e o cabecalho de "conjunto de superficies")
 2. exatamente UM solido, UMA casca
 3. a casca e fechada (ShapeAnalysis_Shell: nenhuma aresta livre)
 4. nenhuma aresta usada por numero impar de faces (costura incompleta)
 5. BRepCheck_Analyzer valido, com a lista de defeitos se houver
 6. orientacao: volume positivo pela divergencia (peca do avesso da negativo)
 7. BRepAlgoAPI_Check: sem auto-interseccao
 8. a malha fecha: tesselada em 0,01 mm, watertight e volume igual ao do B-rep
 9. ida e volta: reimportar o arquivo devolve o mesmo volume e a mesma caixa
10. o LEITOR de STEP (o mesmo motor que o SolidWorks usa na importacao) devolve
    1 raiz, 1 forma transferida, e a forma e TopAbs_SOLID — nao composto, nao
    casca, nao modelo de superficie
11. NAO E SOPA DE TRIANGULO: conta as faces planas de 3 arestas. Malha virada
    em STEP abre como solido e passa em tudo acima, mas aparece FACETADA na
    tela — foi o que o projetista viu no aro e nas orelhas da valvula. Acima de
    100 triangulos o arquivo reprova.

  python3 fechamento.py [pasta]
"""
import sys, os, glob, numpy as np, cadquery as cq, trimesh
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.ShapeAnalysis import ShapeAnalysis_Shell
from OCP.TopExp import TopExp
from OCP.TopAbs import TopAbs_ShapeEnum
from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_SurfaceType
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_ReturnStatus
from OCP.TopAbs import TopAbs_ShapeEnum as TS
from tess import _malha

AQUI = os.path.dirname(os.path.abspath(__file__))
SUB  = sys.argv[1] if len(sys.argv) > 1 else 'step_completo'
D    = os.path.join(AQUI, SUB)

def volume(shape):
    p = GProp_GProps(); BRepGProp.VolumeProperties_s(shape, p); return p.Mass()

def confere(arq):
    nome, falhas, notas = os.path.basename(arq), [], []
    txt = open(arq, 'r', errors='ignore').read()

    # 1. cabecalho
    if 'MANIFOLD_SOLID_BREP' not in txt: falhas.append('sem MANIFOLD_SOLID_BREP')
    if 'CLOSED_SHELL' not in txt:        falhas.append('sem CLOSED_SHELL')
    if 'SHELL_BASED_SURFACE_MODEL' in txt or 'OPEN_SHELL' in txt:
        falhas.append('tem casca ABERTA no arquivo')
    notas.append('%d× MANIFOLD_SOLID_BREP' % txt.count('MANIFOLD_SOLID_BREP'))

    # 10. o que o leitor de STEP devolve
    rd = STEPControl_Reader()
    if rd.ReadFile(arq) != IFSelect_ReturnStatus.IFSelect_RetDone:
        falhas.append('o leitor de STEP recusou o arquivo')
    nt = rd.TransferRoots(); forma = rd.OneShape()
    if rd.NbRootsForTransfer() != 1: falhas.append('%d raizes' % rd.NbRootsForTransfer())
    if nt != 1: falhas.append('%d formas transferidas' % nt)
    if forma.ShapeType() != TS.TopAbs_SOLID:
        falhas.append('o leitor devolve %s, nao SOLID' % str(forma.ShapeType()).split('_')[-1])
    notas.append('leitor devolve SOLID' if forma.ShapeType() == TS.TopAbs_SOLID else 'leitor NAO devolve SOLID')

    sh = cq.importers.importStep(arq).val()
    sols, shells = sh.Solids(), sh.Shells()
    if len(sols)   != 1: falhas.append('%d solidos' % len(sols))
    if len(shells) != 1: falhas.append('%d cascas' % len(shells))
    if not sols: return nome, falhas, notas, None

    s = sols[0]
    # 3. casca fechada
    for shl in shells:
        if not ShapeAnalysis_Shell().CheckOrientedShells(shl.wrapped) is not None:
            pass
    sa = ShapeAnalysis_Shell(); sa.LoadShells(sh.wrapped)
    sa.CheckOrientedShells(sh.wrapped, True, True)
    if sa.HasFreeEdges(): falhas.append('a casca tem ARESTA LIVRE')

    # 4. toda aresta usada por numero PAR de faces
    mp = TopTools_IndexedDataMapOfShapeListOfShape()
    TopExp.MapShapesAndAncestors_s(s.wrapped, TopAbs_ShapeEnum.TopAbs_EDGE,
                                   TopAbs_ShapeEnum.TopAbs_FACE, mp)
    # ARESTA DEGENERADA nao conta: o polo de uma esfera e uma aresta de
    # comprimento zero com uma face so, e e geometria legitima, nao costura solta.
    from OCP.BRep import BRep_Tool
    from OCP.TopoDS import TopoDS
    impar = 0
    for i in range(1, mp.Extent()+1):
        if mp.FindFromIndex(i).Extent() == 2: continue
        if BRep_Tool.Degenerated_s(TopoDS.Edge_s(mp.FindKey(i))): continue
        impar += 1
    if impar: falhas.append('%d arestas com != 2 faces' % impar)

    # 5. validade
    an = BRepCheck_Analyzer(s.wrapped)
    if not an.IsValid(): falhas.append('B-rep INVALIDO')

    # 6. orientacao / volume
    v = volume(s.wrapped)
    if v <= 0: falhas.append('volume %.3f — peca do avesso' % v)

    # 7. auto-interseccao
    ck = BRepAlgoAPI_Check(s.wrapped); ck.Perform()
    if not ck.IsValid(): falhas.append('auto-interseccao')

    # 9. ida e volta — ANTES de tesselar. Tesselar pendura uma triangulacao no
    # TopoDS e dai em diante o BoundingBox sai dela, nao da superficie exata:
    # comparar com o arquivo reimportado acusaria uma diferenca que nao existe.
    cx = s.BoundingBox()
    tmp = arq + '.volta'
    cq.exporters.export(cq.Workplane(obj=s), tmp, exportType='STEP')
    s2 = cq.importers.importStep(tmp).val(); os.remove(tmp)
    if abs(volume(s2.wrapped) - v) > 1e-6 * max(1.0, abs(v)):
        falhas.append('ida e volta muda o volume')
    c2 = s2.BoundingBox()
    d = max(abs(getattr(cx, k) - getattr(c2, k))
            for k in ('xmin','xmax','ymin','ymax','zmin','zmax'))
    if d > 1e-6: falhas.append('ida e volta muda a caixa em %.2e mm' % d)
    notas.append('ida e volta: %.1e mm' % d)

    # 8. a malha fecha
    m = _malha(s.wrapped, 0.010, 0.20)
    if not m.is_volume: falhas.append('malha nao fecha (nao e watertight)')
    if m.is_volume and abs(m.volume - v) / v > 0.01:
        falhas.append('volume malha %.2f x B-rep %.2f' % (m.volume, v))
    notas.append('malha %s' % ('fecha' if m.is_volume else 'ABERTA'))

    # 11. sopa de triangulo
    tri = sum(1 for f in s.Faces()
              if len(f.Edges()) == 3
              and BRepAdaptor_Surface(f.wrapped).GetType() == GeomAbs_SurfaceType.GeomAbs_Plane)
    if tri > 100: falhas.append('%d faces triangulares — a peca vai aparecer FACETADA' % tri)
    notas.append('%d triangulos' % tri)

    notas.append('%d faces · %d arestas · vol %.2f mm3' % (len(s.Faces()), mp.Extent(), v))
    return nome, falhas, notas, s

if __name__ == '__main__':
    arqs = sorted(glob.glob(os.path.join(D, '*.step')))
    print('conferencia de fechamento — %s (%d arquivos)\n' % (SUB, len(arqs)))
    ruim = 0
    for a in arqs:
        nome, falhas, notas, s = confere(a)
        ruim += 1 if falhas else 0
        print('%s' % nome)
        print('   %s' % ' · '.join(notas))
        if falhas:
            for f in falhas: print('   *** %s' % f)
        else:
            print('   FECHA: leitor devolve 1 SOLID · 1 casca · sem aresta livre · toda aresta com')
            print('          2 faces · B-rep valido · sem auto-interseccao · malha watertight · sem facetas')
        print()
    print('REPROVADOS: %d' % ruim if ruim else 'os %d arquivos fecham' % len(arqs))
    sys.exit(1 if ruim else 0)
