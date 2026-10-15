# -*- coding: utf-8 -*-
"""A M01 INTEIRA: a valvula injetada completa, com a parte que se ve em
SUPERFICIE EXATA e nenhuma faceta.

O problema: a valvula so existe aqui como malha, e malha em STEP vira triangulo.
A versao anterior tinha 8.730 faces triangulares e o projetista viu a peca
"fatiada" no aro e nas orelhas.

A saida nao foi converter a malha — foi ENGOLI-LA onde a geometria e conhecida.
Uniao de solidos: onde A contem B, a fronteira do resultado e a de A. Entao:

  * a CHAPA exata (disco r 19,042 de Y 35,40 a 37,23, com quebra de 0,10 a 45
    graus em cima) contem a chapa real da valvula, medida em 9 angulos;
  * cada ORELHA e uma esfera R1,878 em r 20,22, Y 34,69 — e o ajuste e exato: a
    largura tangencial medida bate com 2R nas nove alturas conferidas, e o
    intervalo em Y (32,811..36,568) da 2x1,878.

Faceta de esfera e inscrita na esfera, e a chapa real cabe dentro do disco.
Logo as duas regioes perdem as facetas sozinhas, sem corte e sem costura nova.

O que SOBRA facetado: a saia e os pinos, tudo abaixo de Y 35,400 — ~5.000
triangulos na face de baixo. Nao da para fazer melhor daqui: a saia NAO e de
revolucao. Cortando a valvula em 144 angulos, a area da secao varia
continuamente de 21,08 a 48,17 mm2. Refazer aquilo com superficie exata seria
inventar a peca do cliente (a melhor tentativa desviou 0,9 mm).

O disco tapa tambem o rebaixo e o furo da v3 que ficaram gravados na malha
(348 + 52 mm3) — e a propria receita torna a corta-los, agora na cota v4.
"""
import sys, os, time, numpy as np, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import cos, sin, radians
import params as P
import solido_facetado as SF
from lib_v3 import esfera, rev_perfil
from completas import rotula
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCP.TopTools import TopTools_ListOfShape
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_SurfaceType as GA

AQUI = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(AQUI, 'step')
SAI  = os.path.join(AQUI, 'step_completo')
G = lambda n: cq.importers.importStep('%s/%s.step' % (STEP, n)).val()

ARO_RE_V, ARO_CH = 19.042, 0.10
ORELHA_R, ORELHA_RC, ORELHA_Y = 1.878, 20.22, 34.69
FUZZY = 1e-5     # sem isto o OCC descarta a valvula em silencio (ver MUDANCAS)

def bool_fuzzy(a, b, cut):
    L1 = TopTools_ListOfShape(); L1.Append(a.wrapped)
    L2 = TopTools_ListOfShape(); L2.Append(b.wrapped)
    op = (BRepAlgoAPI_Cut if cut else BRepAlgoAPI_Fuse)()
    op.SetArguments(L1); op.SetTools(L2)
    op.SetFuzzyValue(FUZZY); op.SetRunParallel(True); op.Build()
    assert op.IsDone(), 'booleano nao concluiu'
    return cq.Shape(op.Shape())

def triangulos(s):
    return sum(1 for f in s.Faces()
               if len(f.Edges()) == 3
               and BRepAdaptor_Surface(f.wrapped).GetType() == GA.GeomAbs_Plane)

def valvula_solida():
    """A valvula completa: malha engolida pela chapa exata e pelas 2 esferas."""
    fac, exata = SF.valvula_facetada()
    val = SF.solido(fac).moved(cq.Location(cq.Vector(-P.CX, 0, -P.CZ)))
    r0, ch = ARO_RE_V, ARO_CH
    chapa = rev_perfil(cq.Workplane("XY")
        .moveTo(0.0, P.CHAPA_Y0).lineTo(r0, P.CHAPA_Y0)
        .lineTo(r0, P.FACE - ch).lineTo(r0 - ch, P.FACE)   # quebra de 45,000
        .lineTo(0.0, P.FACE))
    v = bool_fuzzy(val, chapa, False)
    for a in (0.0, 180.0):
        v = bool_fuzzy(v, esfera(ORELHA_R, ORELHA_RC*cos(radians(a)), ORELHA_Y,
                                 ORELHA_RC*sin(radians(a))), False)
    return v.moved(cq.Location(cq.Vector(P.CX, 0, P.CZ))), fac, exata

if __name__ == '__main__':
    t0 = time.time()
    val, fac, exata = valvula_solida()
    import trimesh.proximity as px
    e = px.closest_point(fac, exata.sample(40000))[1]
    print('valvula: %d faces  %d triangulos  vol %.2f  (erro do corpo facetado: max %.4f medio %.4f mm)'
          % (len(val.Faces()), triangulos(val), val.Volume(), e.max(), e.mean()))
    r = val
    for op, n in [('fuse', 'Chrono_v3_M01_1_SOMAR_enchimento_e_dias'),
                  ('cut',  'Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes'),
                  ('fuse', 'Chrono_v3_M01_3_SOMAR_poste'),
                  ('cut',  'Chrono_v3_M01_4_SUBTRAIR_furo_passante')]:
        t = time.time(); r = bool_fuzzy(r, G(n), op == 'cut')
        print('   %-5s %-46s %6d faces  %5d tri  %4.0fs'
              % (op, n[:46], len(r.Faces()), triangulos(r), time.time()-t))
    ss = r.Solids(); assert len(ss) == 1, '%d solidos' % len(ss)
    s = ss[0]
    assert BRepCheck_Analyzer(s.wrapped).IsValid(), 'M01 saiu invalida'
    arq = '%s/Chrono_M01_Valvula_Dias.step' % SAI
    cq.exporters.export(cq.Workplane(obj=s), arq, exportType='STEP')
    rotula(arq, 'Chrono M01 - valvula com os dias',
           'valvula injetada completa - chapa e orelhas com superficie exata, '
           'saia abaixo de Y 35,40 vinda da malha')
    print('%s  %.1f MB  %d faces  %d triangulos  vol %.2f  (%.0fs)'
          % (os.path.basename(arq), os.path.getsize(arq)/1e6, len(s.Faces()),
             triangulos(s), s.Volume(), time.time()-t0))
