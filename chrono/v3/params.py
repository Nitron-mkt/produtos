# -*- coding: utf-8 -*-
"""Cotas do Chrono v3 — revisao de moldabilidade pedida pela ferramentaria.

Tudo em mm, no sistema dos STL da tampa: Y e a vertical, eixo do poco em
X 61,97 / Z 102,68.  Extracao em +Y para as tres pecas.
"""
from math import tan, radians

# ---- regras globais desta revisao --------------------------------------
SAIDA      = 1.5     # graus de saida em TODA parede vertical (pedido: 1 a 3)
RAIO       = 0.30    # raio de abaulamento das arestas estruturais
RAIO_FINO  = 0.15    # onde a parede nao comporta 0,30
LETRA_CAP  = 1.50    # altura de caixa alta padrao (MES)
DIA_CAP    = 2.40    # dias: o maior que cabe com os numeros juntos (vao de 0,69 mm)
MES_CAP    = 2.20    # meses: 47% maior, e a janela foi aberta junto
LETRA_REL  = 0.10    # relevo de TODA letra e numero (auto relevo, nunca gravado)
LETRA_RC   = 0.04    # raio de canto no contorno do caractere (plano)
# Saida do caractere: ZERO, e por medida, nao por preguica.
#
# A extrusao conica do OpenCASCADE (LocOpe_DPrism) degenera nos cantos de um
# contorno de letra: com 15 graus saem 700 arestas abaixo de 0,05 mm (a menor
# com 0,00065) e 205 faces de area praticamente nula. Com 7 graus, 529. Com 3
# graus, 367. Com ZERO: aresta minima de 0,10 mm e NENHUMA micro-face. Foi
# exatamente esse lixo que fez a peca abrir "fatiada e pontinhada" no SolidWorks.
#
# E nao faz falta: o que solta uma letra de 0,10 mm de relevo do aco nao e a
# saida da parede lateral, e a propria altura de 0,10. Se a ferramentaria quiser
# saida nos caracteres, o caminho limpo e aplicar no CAD dela, com a operacao de
# draft nativa — o kernel do SolidWorks resolve isso sem gerar lasca.
LETRA_SAIDA = 0.0

def rec(h):
    """quanto o raio recua em h mm de altura, com a saida padrao"""
    return tan(radians(SAIDA)) * h

# ---- datums da valvula (nao mudam: vem da peca ja injetada) -------------
CX, CZ    = 61.97, 102.68
FACE      = 37.23    # face de topo da valvula
CHAPA_Y0  = 35.40    # face de baixo da chapa, no eixo

# ---- M01 ---------------------------------------------------------------
MESA_RI, MESA_RE, MESA_H = 14.20, 18.75, 0.18       # mesa dos dias -> topo 37,41
CUNHA_A0, CUNHA_A1, CUNHA_RE = 55.0, 125.0, 18.80   # a concha das 12 h
REB_H, REB_RE   = 0.60, 13.60                        # rebaixo onde a rodinha afunda
POST_R, POST_TOP = 6.60, 38.25
FURO_R, FURO_CH  = 3.00, 0.35
CHANFRO          = 0.30    # chanfro de topo do poste, a 45,000 graus
DIA_R            = 16.85                             # raio da escala dos dias

# detente: agora centrado na faixa do rebaixo e com 2,00 de base
DET_R    = (POST_R + REB_RE) / 2                     # 10,10 — meio da faixa
DET_BASE = 2.00                                      # diametro da base da calota
DET_ALT  = 0.25                                      # quanto sobe do piso
DET_ESF  = ((DET_BASE/2)**2 + DET_ALT**2) / (2*DET_ALT)   # raio da esfera: 2,125

# ---- M02 rodinha dos meses ---------------------------------------------
# corpo 1,50 + 0,10 de numeral = 1,60 de envelope, o mesmo de antes
ARO_RI, ARO_RE = 6.80, 13.40
ARO_Y0 = FACE - REB_H + 0.02        # 36,65
ARO_ESP = 1.50
ARO_Y1 = ARO_Y0 + ARO_ESP           # 38,15 ; numerais chegam a 38,25
MES_R  = 9.80
ENT_R, ENT_RC = 13.75, 1.10         # entalhes de unha

# ---- M03 ponteira -------------------------------------------------------
# corpo 1,50 + 0,10 de relevo = 1,60 de envelope, o mesmo de antes
CUBO_R   = 3.30
CUBO_Y0  = 38.35
PONT_ESP = 1.50
TOPO     = CUBO_Y0 + PONT_ESP       # 39,85 ; relevo chega a 39,95
# Ponta do pino em 34,30 e nao 34,00: com a rampa de 30 graus saindo de O6,80,
# a 34,00 a parede da ponta ficava em 0,242 mm — gume, que rebarba e quebra. Em
# 34,30 sao 0,448 e o pino ainda desce 1,10 abaixo da chapa para a farpa pegar.
PINO_RE, PINO_Y1, FARPA_R = 2.90, 34.30, 3.40
FENDA_W, FENDAS = 0.70, 4
ICONE_H  = 8.00
BULBO_R, BULBO_OFF = 8.20, 1.00
NARIZ_R, NARIZ_Y   = 1.20, 14.35
# Janela do mes, dimensionada a partir do numeral: 0,45 mm de folga em volta do
# maior deles ("10", 2,96 de largura a cap 2,20). A borda ate o contorno da gota
# fica em 1,09 mm — medida, nao estimada.
JAN_R0, JAN_R1, JAN_M, JAN_RC = 8.25, 11.35, 1.93, 0.70
JAN_RAIO = 0.30                     # raio das arestas da janela, em cima e embaixo
# MES recuou 1,50 mm: a 7,40 o acento do E chegava a r 8,33 e era cortado pela
# janela, que comeca em 8,25. A 5,90 ele para em 6,83 — 1,42 mm de folga.
MES_TXT_R = 5.90
