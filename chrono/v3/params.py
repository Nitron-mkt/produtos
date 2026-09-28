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
LETRA_CAP  = 1.50    # altura de caixa alta de TODA letra e numero
LETRA_REL  = 0.10    # relevo de TODA letra e numero (auto relevo, nunca gravado)
LETRA_RC   = 0.06    # raio de canto no contorno do caractere (plano)
# Saida do caractere. Com 0,10 de relevo, 1,5 grau da 2,6 MICRA de recuo — o aco
# nao guarda isso. Letra rasa se tira do molde com saida generosa: 15 graus
# custam 0,027 mm por lado num traco de 0,28 e a letra continua legivel.
LETRA_SAIDA = 15.0

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
PINO_RE, PINO_Y1, FARPA_R = 2.90, 34.00, 3.40
FENDA_W, FENDAS = 0.70, 4
ICONE_H  = 8.00
BULBO_R, BULBO_OFF = 8.20, 1.00
NARIZ_R, NARIZ_Y   = 1.20, 14.35
JAN_R0, JAN_R1, JAN_M, JAN_RC = 8.70, 11.30, 1.80, 0.70
MES_TXT_R = 7.40                    # onde ficava o "M", agora "MES"
