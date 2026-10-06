# -*- coding: utf-8 -*-
"""As tres pecas em UM solido cada, que e o que o projetista abre e mede.

M01: a receita de 4 passos (somar/subtrair) e o que vai para a ferramenta, porque
o corpo da valvula ja esta injetado e nao pode ser remodelado — mas receita nao se
abre, e foi por isso que "nao veio a valvula". Aqui a receita ja vem aplicada.

ATENCAO: o STL da valvula injetada saiu da sessao quando o container foi recriado,
entao o corpo abaixo da face de topo e uma CHAPA DE PROVA: disco de O38,00 com a
mesma saida, da face de baixo (Y 35,40) a face de topo (Y 37,23). Os datums estao
certos e tudo o que o Chrono acrescenta esta exato. A saia e os pes da valvula nao
estao. Com o STL de volta, o mesmo script gera a peca completa de verdade.
"""
import sys, os, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P
from lib_v3 import cone
from OCP.BRepCheck import BRepCheck_Analyzer

AQUI = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(AQUI, 'step')
SAI  = os.path.join(AQUI, 'step_completo'); os.makedirs(SAI, exist_ok=True)
L = lambda n: cq.importers.importStep('%s/%s.step' % (STEP, n)).val()

CHAPA_RE = 19.00   # raio da chapa de prova, na face de baixo

def m01_completa():
    chapa = cone(CHAPA_RE, CHAPA_RE - P.rec(P.FACE - P.CHAPA_Y0),
                 P.CHAPA_Y0, P.FACE).moved(cq.Location(cq.Vector(P.CX, 0, P.CZ)))
    r = chapa.fuse(L('Chrono_v3_M01_1_SOMAR_enchimento_mesa_dias'))
    r = r.cut(L('Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes'))
    r = r.fuse(L('Chrono_v3_M01_3_SOMAR_poste'))
    r = r.cut(L('Chrono_v3_M01_4_SUBTRAIR_furo_passante'))
    return r

def grava(s, nome):
    ss = s.Solids()
    assert len(ss) == 1, '%s saiu com %d solidos' % (nome, len(ss))
    s = ss[0]
    ok = BRepCheck_Analyzer(s.wrapped).IsValid()
    arq = '%s/%s.step' % (SAI, nome)
    cq.exporters.export(cq.Workplane(obj=s), arq, exportType='STEP')
    b = s.BoundingBox()
    print('   %-44s 1 solido  %4d faces  vol %8.2f mm3  Y %6.2f..%6.2f  B-rep %s'
          % (nome + '.step', len(s.Faces()), s.Volume(), b.ymin, b.ymax,
             'VALIDO' if ok else '*** INVALIDO ***'))
    return s

if __name__ == '__main__':
    print('as tres pecas, um solido cada:')
    grava(m01_completa(),                       'Chrono_M01_Valvula_Dias__CHAPA_DE_PROVA')
    grava(L('Chrono_v3_M02_Rodinha_Meses'),     'Chrono_M02_Rodinha_Meses')
    grava(L('Chrono_v3_M03_Ponteira'),          'Chrono_M03_Ponteira')
