# -*- coding: utf-8 -*-
"""Lâminas do ícone da Nitron, em cache no repositório.

A versão original saía do `icone_nitron.pdf` por `medicao_v2/icone.py`, que lia o
PDF na pasta de uploads da sessão. Essa pasta é efêmera: quando o container foi
recriado, o PDF sumiu e o build parou. Estes contornos foram extraídos de uma
seção do próprio `Chrono_v3_M03_Ponteira.step` em Y 39,90 — já com o canto
arredondado de 0,10 que o build aplicava — e agora vivem no repositório.

Convenção: (x, y) do polígono = (x, z) do mundo, relativo ao eixo do poço, que é
o que `deitado()` espera.
"""
import json, os
from shapely.geometry import Polygon as SP
_J = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icone_nitron.json')

def laminas():
    d = json.load(open(_J))
    out = []
    for pts in d['laminas']:
        p = SP(pts)
        if not p.is_valid: p = p.buffer(0)
        out.append(p)
    return out
