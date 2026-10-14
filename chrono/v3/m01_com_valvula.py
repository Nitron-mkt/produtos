# -*- coding: utf-8 -*-
"""A M01 INTEIRA em STEP, com a valvula injetada de verdade.

A valvula nunca existiu como superficie exata — chegou como malha. Aqui ela
entra como solido de faces planas (ver solido_facetado.py), e o Chrono entra por
cima com SUPERFICIE EXATA, pela mesma receita de 4 passos. Resultado: um solido
so, onde o que esta em revisao e cilindro, cone e spline de verdade, e o corpo
da valvula e corpo de referencia facetado.
"""
import sys, os, time, numpy as np, trimesh, trimesh.proximity as px, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P
import solido_facetado as SF
from completas import rotula
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCP.TopTools import TopTools_ListOfShape

FUZZY = 1e-5

def bool_fuzzy(a, b, cut):
    """Booleano com TOLERANCIA DIFUSA. Sem ela o OCC descarta a valvula em
    silencio: o fuse do solido facetado com a receita exata devolvia 535,83 mm3
    (so a receita) e 1 solido valido — resultado errado que passa em toda
    checagem. Com fuzzy de 1e-5 devolve 2.020,93 mm3, que e o esperado. A causa
    e a diferenca de tolerancia entre a casca costurada em 1e-7 e as faces
    exatas do STEP."""
    L1 = TopTools_ListOfShape(); L1.Append(a.wrapped)
    L2 = TopTools_ListOfShape(); L2.Append(b.wrapped)
    op = (BRepAlgoAPI_Cut if cut else BRepAlgoAPI_Fuse)()
    op.SetArguments(L1); op.SetTools(L2)
    op.SetFuzzyValue(FUZZY); op.SetRunParallel(True); op.Build()
    assert op.IsDone(), 'booleano nao concluiu'
    return cq.Shape(op.Shape())

AQUI = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(AQUI, 'step')
SAI  = os.path.join(AQUI, 'step_completo')
G = lambda n: cq.importers.importStep('%s/%s.step' % (STEP, n)).val()

if __name__ == '__main__':
    t0 = time.time()
    fac, exata = SF.valvula_facetada()
    e = px.closest_point(fac, exata.sample(40000))[1]
    print('valvula facetada: %s' % SF.medidas(fac))
    print('   erro contra a malha exata: max %.4f  medio %.4f mm' % (e.max(), e.mean()))
    val = SF.solido(fac)
    print('   solido: %d faces  valido=%s  vol %.2f  (%.0fs)'
          % (len(val.Faces()), BRepCheck_Analyzer(val.wrapped).IsValid(), val.Volume(), time.time()-t0))
    r = val
    for op, n in [('fuse', 'Chrono_v3_M01_1_SOMAR_enchimento_e_dias'),
                  ('cut',  'Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes'),
                  ('fuse', 'Chrono_v3_M01_3_SOMAR_poste'),
                  ('cut',  'Chrono_v3_M01_4_SUBTRAIR_furo_passante')]:
        t = time.time(); r = bool_fuzzy(r, G(n), op == 'cut')
        print('   %-5s %-46s %6d faces  %5.0fs' % (op, n[:46], len(r.Faces()), time.time()-t))
    ss = r.Solids()
    assert len(ss) == 1, '%d solidos' % len(ss)
    s = ss[0]
    assert BRepCheck_Analyzer(s.wrapped).IsValid(), 'M01 com valvula saiu invalida'
    arq = '%s/Chrono_M01_Valvula_Dias_COM_VALVULA.step' % SAI
    cq.exporters.export(cq.Workplane(obj=s), arq, exportType='STEP')
    rotula(arq, 'Chrono M01 - valvula com os dias',
           'valvula injetada como corpo facetado (erro max 0,043 mm) + Chrono com superficie exata')
    print('%s  %.1f MB  %d faces  vol %.2f  (%.0fs no total)'
          % (os.path.basename(arq), os.path.getsize(arq)/1e6, len(s.Faces()), s.Volume(), time.time()-t0))
