#!/usr/bin/env python3
"""Modela a arara a partir das medidas reais das ripas e desenha o conjunto
mais uma ilustracao por etapa de montagem.

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
NIVEL = [k * (LZ + J) for k in range(4)]       # 4 quadros, 3 conjuntos de colunas
CANTOS = [(0, 0), (LX, 0), (LX, LY), (0, LY)]
m = SEC / 2
h = 15                                          # meia altura do bloco do conector


def quadro(k):
    """Um quadro horizontal: 4 conectores de canto + 2 PSC-04 + 2 PST-01."""
    z, p = NIVEL[k], []
    for cx, cy in CANTOS:
        p.append(caixa((cx-h, cy-h, z-h), (cx+h, cy+h, z+h)))
    for cy in (0, LY):                                   # PSC-04, no comprimento
        p.append(caixa((h, cy-m, z-m), (LX-h, cy+m, z+m)))
    for cx in (0, LX):                                   # PST-01, na travessa
        p.append(caixa((cx-m, h, z-m), (cx+m, LY-h, z+m)))
    return p


def colunas(k):
    """PSA-05 entre o quadro k e o quadro k+1."""
    return [caixa((cx-m, cy-m, NIVEL[k]+h), (cx+m, cy+m, NIVEL[k+1]-h)) for cx, cy in CANTOS]


def pes():
    return [caixa((cx-m, cy-m, NIVEL[0]-h-PE), (cx+m, cy+m, NIVEL[0]-h)) for cx, cy in CANTOS]


def calceiro():
    """8 ripas PSC-02 na travessa, com um porta-haste em cada ponta."""
    z, p = NIVEL[1] + m, []
    y0, y1 = (LY-CAL)/2, (LY+CAL)/2
    for i in range(8):
        x = 55 + i * (LX - 110) / 7
        p.append(caixa((x-m, y0, z), (x+m, y1, z+SEC)))
        for yy in (y0, y1):                              # 850H
            s = -1 if yy == y1 else 1
            p.append(caixa((x-m-4, yy, z-4), (x+m+4, yy + s*26, z+SEC+4)))
    return p


def tampas():
    z = NIVEL[3] + h
    return [caixa((cx-h, cy-h, z), (cx+h, cy+h, z+9)) for cx, cy in CANTOS]


# --- etapas: (o que ja estava, o que entra agora) --------------------------
Q0, PES, C0, Q1, CALC, C1, Q2, C2, Q3, TP = (
    quadro(0), pes(), colunas(0), quadro(1), calceiro(),
    colunas(1), quadro(2), colunas(2), quadro(3), tampas())

# o ultimo campo diz se a etapa usa a moldura alta comum; as duas primeiras
# ainda sao quadros deitados e ficariam minusculas dentro dela
ETAPAS = [
    ('passo-2', [],                            Q0,          False),
    ('passo-3', Q0,                            PES,         False),
    ('passo-4', Q0+PES,                        C0+Q1,       True),
    ('passo-5', Q0+PES+C0+Q1,                  CALC,        True),
    ('passo-6', Q0+PES+C0+Q1+CALC,             C1,          True),
    ('passo-7', Q0+PES+C0+Q1+CALC+C1,          Q2+C2+Q3,    True),
    ('passo-8', Q0+PES+C0+Q1+CALC+C1+Q2+C2+Q3, TP,          True),
]
TUDO = Q0+PES+C0+Q1+CALC+C1+Q2+C2+Q3+TP
OLHO = (1.0, -1.05, 0.50)


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
    maior = np.concatenate(solta(max(SOLTAS.values())))
    for ref, mm in SOLTAS.items():
        desenha(np.concatenate(solta(mm)), SAI / f'{ref}.svg', eye=(.55, -1, .30),
                lado=560, pad=10, vinco=18, res=900, traco=(2.0, 1.2), ref=maior)
        print(f'  {ref}.svg      ripa de {mm} mm')
    desenha(np.concatenate([caixa((0, -m, -m), (PE, m, m))]), SAI / 'BPE-01-AC.svg',
            eye=(.8, -1, .45), lado=200, pad=10, vinco=18, res=700, traco=(2.0, 1.2))
    print('  BPE-01-AC.svg  pe de 60 mm')
    t, g = junta([], TUDO)
    w, hh, n = desenha(t, SAI / 'conjunto.svg', g, eye=OLHO, lado=900, vinco=18, res=1500)
    print(f'  conjunto.svg   {w:.0f}x{hh:.0f}  {n} segmentos')
    moldura = np.concatenate(TUDO)          # etapas altas no mesmo enquadramento
    for nome, feito, novo, comum in ETAPAS:
        t, g = junta(feito, novo)
        w, hh, n = desenha(t, SAI / f'{nome}.svg', g, eye=OLHO, lado=680, vinco=18,
                           res=1150, ref=None)
        print(f'  {nome}.svg     {w:.0f}x{hh:.0f}  {n} segmentos')
