#!/usr/bin/env python3
"""Modela a arara a partir das medidas reais das ripas e desenha o conjunto
mais uma ilustracao por etapa de montagem.

Sequencia pedida pela qualidade: cada andar e montado inteiro, deitado, e so
depois as alturas sao conectadas. Cada peca que entra na etapa leva um balao
numerado, na mesma ordem da lista REF. usadas da caixa.

    python3 manual/montagem2svg.py
"""
import sys, pathlib, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from linework import caixa, desenha

BASE = pathlib.Path(__file__).parent
SAI = BASE / 'pecas'

# --- medidas em mm, da lista de pecas -------------------------------------
LX, LY, LZ, CAL, PE = 717, 437, 513, 415, 60   # PSC-04, PST-01, PSA-05, PSC-02, BPE-01-AC
SEC, J = 22, 74                                # secao da ripa; altura do conector
NIVEL = [k * (LZ + J) for k in range(4)]       # 4 andares, 3 conjuntos de colunas
CANTOS = [(0, 0), (LX, 0), (LX, LY), (0, LY)]
m = SEC / 2
h = 15                                         # meia altura do bloco do conector


def quadro(k):
    """Um andar: 4 conectores de canto + 2 PSC-04 + 2 PST-01."""
    z, p = NIVEL[k], []
    for cx, cy in CANTOS:
        p.append(caixa((cx-h, cy-h, z-h), (cx+h, cy+h, z+h)))
    for cy in (0, LY):                                   # PSC-04, no comprimento
        p.append(caixa((h, cy-m, z-m), (LX-h, cy+m, z+m)))
    for cx in (0, LX):                                   # PST-01, na travessa
        p.append(caixa((cx-m, h, z-m), (cx+m, LY-h, z+m)))
    return p


def colunas(k):
    """PSA-05 ligando o andar k ao andar k+1."""
    return [caixa((cx-m, cy-m, NIVEL[k]+h), (cx+m, cy+m, NIVEL[k+1]-h)) for cx, cy in CANTOS]


def pes():
    return [caixa((cx-m, cy-m, NIVEL[0]-h-PE), (cx+m, cy+m, NIVEL[0]-h)) for cx, cy in CANTOS]


SLAT_X = [55 + i * (LX - 110) / 7 for i in range(8)]
SLAT_Y0, SLAT_Y1 = (LY - CAL) / 2, (LY + CAL) / 2
SLAT_Z = NIVEL[1] + m


def calceiro():
    """8 ripas PSC-02 na travessa, com um porta-haste em cada ponta."""
    p = []
    for x in SLAT_X:
        p.append(caixa((x-m, SLAT_Y0, SLAT_Z), (x+m, SLAT_Y1, SLAT_Z+SEC)))
        for yy, s in ((SLAT_Y0, 1), (SLAT_Y1, -1)):      # 850H
            p.append(caixa((x-m-4, yy, SLAT_Z-4), (x+m+4, yy + s*26, SLAT_Z+SEC+4)))
    return p


def tampas():
    z = NIVEL[3] + h
    return [caixa((cx-h, cy-h, z), (cx+h, cy+h, z+9)) for cx, cy in CANTOS]


def move(blocos, dz):
    """Desce um andar para z=0, para desenha-lo sozinho."""
    return [b + np.array([0, 0, dz]) for b in blocos]


# --- ancoras dos baloes, na ordem da lista REF. usadas ---------------------
def ancoras_andar(z=0, com_pes=False, topo=False):
    """Os 4 pontos de um andar: 2 cantos, a ripa de comprimento e a travessa."""
    a = [((0, 0, z), 1), ((LX, 0, z), 2), ((LX*0.66, 0, z), 3), ((LX, LY*0.62, z), 4)]
    if topo:                                  # no cabideiro o canto da frente e o 850L
        a = [((0, 0, z), 1), ((LX, 0, z), 2), ((LX, LY, z), 3),
             ((LX*0.66, 0, z), 4), ((LX, LY*0.62, z), 5)]
    if com_pes:
        a.append(((0, 0, z - h - PE/2), 5))
    return a


Q0, PES, C0, Q1, CALC, C1, Q2, C2, Q3, TP = (
    quadro(0), pes(), colunas(0), quadro(1), calceiro(),
    colunas(1), quadro(2), colunas(2), quadro(3), tampas())

DZ1, DZ2, DZ3 = -NIVEL[1], -NIVEL[2], -NIVEL[3]
ERGUIDO = Q0 + PES + C0 + Q1 + CALC

# (arquivo, ja montado, entra agora, baloes, usa a moldura do conjunto inteiro).
# Cada etapa preenche a propria caixa: na folha a caixa tem 41x22 mm e uma
# estrutura de 1,9 m presa ao enquadramento do conjunto sairia ilegivel.
ETAPAS = [
    ('passo-2', [], Q0 + PES,
     ancoras_andar(0, com_pes=True), False),

    ('passo-3', [], move(Q1 + CALC, DZ1),
     ancoras_andar(0) + [((SLAT_X[2], SLAT_Y0 + 8, SEC + m), 5),
                         ((SLAT_X[5], LY/2, SEC + m), 6)], False),

    ('passo-4', [], move(Q2, DZ2), ancoras_andar(0), False),

    ('passo-5', [], move(Q3, DZ3), ancoras_andar(0, topo=True), False),

    ('passo-6', Q0 + PES + Q1 + CALC, C0,
     [((LX, 0, (NIVEL[0] + NIVEL[1]) / 2), 1)], False),

    ('passo-7', ERGUIDO + Q2 + Q3, C1 + C2,
     [((LX, 0, (NIVEL[1] + NIVEL[2]) / 2), 1)], False),

    ('passo-8', ERGUIDO + C1 + Q2 + C2 + Q3, TP,
     [((LX, 0, NIVEL[3] + h + 20), 1)], False),
]
TUDO = ERGUIDO + C1 + Q2 + C2 + Q3 + TP
OLHO = (1.0, -1.05, 0.50)
CAIXA_MM = (41, 22)          # a area util da caixa de etapa, na folha


def junta(feito, novo):
    tris = np.concatenate(feito + novo) if (feito or novo) else np.zeros((0, 3, 3))
    g = np.concatenate([np.zeros(sum(len(b) for b in feito), int),
                        np.ones(sum(len(b) for b in novo), int)])
    return tris, g


# --- as pecas de madeira soltas, como aparecem na lista -------------------
SOLTAS = {'PSC-04': 717, 'PSA-05': 513, 'PST-01': 437, 'PSC-02': 415}


def solta(mm):
    return [caixa((0, -m, -m), (mm, m, m))]


if __name__ == '__main__':
    SAI.mkdir(exist_ok=True)

    t, g = junta([], TUDO)
    w, hh, n = desenha(t, SAI / 'conjunto.svg', g, eye=OLHO, lado=900, vinco=18, res=1500)
    print(f'  conjunto.svg   {w:.0f}x{hh:.0f}  {n} segmentos')

    moldura = np.concatenate(TUDO)
    for nome, feito, novo, baloes, comum in ETAPAS:
        t, g = junta(feito, novo)
        w, hh, n = desenha(t, SAI / f'{nome}.svg', g, eye=OLHO, lado=680, vinco=18,
                           res=1150, ref=(moldura if comum else None),
                           baloes=baloes, caixa_mm=CAIXA_MM)
        print(f'  {nome}.svg     {w:.0f}x{hh:.0f}  {n} segmentos  {len(baloes)} balões')

    maior = np.concatenate(solta(max(SOLTAS.values())))
    for ref, mm in SOLTAS.items():
        desenha(np.concatenate(solta(mm)), SAI / f'{ref}.svg', eye=(.55, -1, .30),
                lado=560, pad=10, vinco=18, res=900, traco=(2.0, 1.2), ref=maior)
    desenha(np.concatenate([caixa((0, -m, -m), (PE, m, m))]), SAI / 'BPE-01-AC.svg',
            eye=(.8, -1, .45), lado=200, pad=10, vinco=18, res=700, traco=(2.0, 1.2))
    print('  ripas soltas e pé: ok')
