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
import sys, os, io, re, unicodedata, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P
from math import cos, sin, radians
from lib_v3 import cone, esfera, rev_perfil
from OCP.BRepCheck import BRepCheck_Analyzer

AQUI = os.path.dirname(os.path.abspath(__file__))
STEP = os.path.join(AQUI, 'step')
SAI  = os.path.join(AQUI, 'step_completo'); os.makedirs(SAI, exist_ok=True)
L = lambda n: cq.importers.importStep('%s/%s.step' % (STEP, n)).val()

# ---------------------------------------------------------------- o corpo
# Nao e mais um disco liso. E o corpo da valvula MEDIDO e refeito com
# superficie exata — plano, cilindro, toro e esfera —, para o arquivo abrir sem
# uma faceta sequer. Todas as cotas vieram de cortes do STL da valvula:
#
#   face de baixo      Y 35,400                      (medido)
#   face de topo       Y 37,230                      (medido)
#   diametro externo   O38,09  (r 19,042)            (medido em 9 angulos)
#   raio do aro        R0,50 em cima e embaixo       (ajuste: erro max 0,037)
#   orelhas            2 esferas R1,878              (ajuste exato: a largura
#                      em r 20,22, Y 34,69,           tangencial bate com 2R em
#                      a 0 e 180 graus                todas as 9 alturas)
#
# O QUE NAO ESTA AQUI: a saia e os pinos da valvula, tudo abaixo de Y 35,400.
# Essa parte nao e de revolucao — a secao varia continuamente com o angulo — e
# so existe como malha. Refaze-la com superficie exata seria inventar a peca do
# cliente. Para ela, o caminho e a receita de 4 passos sobre o CAD da valvula.
ARO_RE_V  = 19.042      # raio externo da valvula
# Quebra de 0,10 a 45 graus na aresta de cima, e nao o raio de 0,50 que o ajuste
# sugeria. Motivo medido: o enchimento da concha vai ate r 18,80 e o portador
# ate 18,60; com raio de 0,50 a face de topo acabaria em 18,54 e os dois
# passariam dela, deixando aresta de 0,0034 mm em 55 e 125 graus — o mesmo
# defeito do arquivo fatiado. Com 0,10 a face plana chega a 18,94 e sobra folga
# para os dois. Custo: 0,25 mm de desvio numa faixa de 0,5 mm do aro.
ARO_RAIO  = 0.10
ORELHA_R, ORELHA_RC, ORELHA_Y = 1.878, 20.22, 34.69

def corpo_medido():
    """O corpo da valvula como solido de revolucao exato, mais as 2 orelhas."""
    r0, rr = ARO_RE_V, ARO_RAIO
    perfil = (cq.Workplane("XY")
        # sem raio na aresta de baixo: a esfera da orelha cruzava o toro E o
        # plano de baixo, e cada cruzamento desses deixa aresta de microns. Com
        # a aresta viva, a esfera corta so o cilindro.
        .moveTo(3.00, P.CHAPA_Y0)
        .lineTo(r0, P.CHAPA_Y0)
        .lineTo(r0, P.FACE - rr)
        .lineTo(r0 - rr, P.FACE)            # quebra de 45,000 graus
        .lineTo(3.00, P.FACE))
    corpo = rev_perfil(perfil)
    for a in (0.0, 180.0):
        corpo = corpo.fuse(esfera(ORELHA_R, ORELHA_RC*cos(radians(a)), ORELHA_Y,
                                  ORELHA_RC*sin(radians(a))))
    return corpo.Solids()[0].moved(cq.Location(cq.Vector(P.CX, 0, P.CZ)))

def m01_completa():
    chapa = corpo_medido()
    r = chapa.fuse(L('Chrono_v3_M01_1_SOMAR_enchimento_e_dias'))
    r = r.cut(L('Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes'))
    r = r.fuse(L('Chrono_v3_M01_3_SOMAR_poste'))
    r = r.cut(L('Chrono_v3_M01_4_SUBTRAIR_furo_passante'))
    return r

def rotula(arq, nome, descricao):
    """Escreve o nome da peca DENTRO do STEP (FILE_NAME, FILE_DESCRIPTION e
    PRODUCT). O SolidWorks mostra o PRODUCT como nome do corpo na arvore — e e
    ali, e nao no nome do arquivo, que a informacao sobrevive a um 'salvar como'.
    So ASCII: string STEP com acento precisa de escape \\X2\\ e nem todo
    importador aceita."""
    t = io.open(arq, encoding='utf-8').read()
    nome = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode()
    desc = unicodedata.normalize('NFKD', descricao).encode('ascii', 'ignore').decode()
    t = re.sub(r"FILE_DESCRIPTION\(\('[^']*'\)", "FILE_DESCRIPTION(('%s')" % desc, t, count=1)
    t = re.sub(r"FILE_NAME\('[^']*'", "FILE_NAME('%s'" % nome, t, count=1)
    t = re.sub(r"PRODUCT\('[^']*',\s*'[^']*',\s*''",
               "PRODUCT('%s','%s',''" % (nome, desc), t, count=1, flags=re.S)
    io.open(arq, 'w', encoding='utf-8').write(t)

def grava(s, nome, rotulo=None, descricao=''):
    ss = s.Solids()
    assert len(ss) == 1, '%s saiu com %d solidos' % (nome, len(ss))
    s = ss[0]
    ok = BRepCheck_Analyzer(s.wrapped).IsValid()
    arq = '%s/%s.step' % (SAI, nome)
    cq.exporters.export(cq.Workplane(obj=s), arq, exportType='STEP')
    rotula(arq, rotulo or nome, descricao)
    b = s.BoundingBox()
    print('   %-44s 1 solido  %4d faces  vol %8.2f mm3  Y %6.2f..%6.2f  B-rep %s'
          % (nome + '.step', len(s.Faces()), s.Volume(), b.ymin, b.ymax,
             'VALIDO' if ok else '*** INVALIDO ***'))
    return s

if __name__ == '__main__':
    print('as tres pecas, um solido cada:')
    grava(m01_completa(), 'Chrono_M01_Valvula_Dias',
          rotulo='Chrono M01 - valvula com os dias',
          descricao='corpo da valvula medido e refeito com superficie exata - '
                    'sem a saia e os pinos, que ficam abaixo de Y 35,40')
    grava(L('Chrono_v3_M02_Rodinha_Meses'), 'Chrono_M02_Rodinha_Meses',
          rotulo='Chrono M02 - rodinha do mes',
          descricao='peca nova inteira - PP - 0,542 g')
    grava(L('Chrono_v3_M03_Ponteira'), 'Chrono_M03_Ponteira',
          rotulo='Chrono M03 - ponteira',
          descricao='peca nova inteira - PP - 0,381 g')
