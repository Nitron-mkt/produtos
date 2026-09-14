#!/usr/bin/env python3
"""Orienta STL para impressao: poe o eixo da peca em Z, apoia em z=0 e centra na mesa.
Le pecas.json. Escreve os STL preparados em ./prep/ .

    python3 preparar.py [pecas.json]
"""
import json, sys, os
import numpy as np, trimesh

CFG = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'pecas.json'))
BEDX, BEDY = CFG['mesa']
CX, CY = BEDX / 2.0, BEDY / 2.0
UP = CFG.get('eixo_vertical_do_stl', 'Y').upper()
OUT = CFG.get('saida', 'prep')
os.makedirs(OUT, exist_ok=True)

def prep(stl, flip, dx=0.0, dy=0.0):
    m = trimesh.load(stl)
    if UP == 'Y':                                   # Y do STL -> Z da impressora
        ang, eixo = (-np.pi/2 if flip else np.pi/2), [1, 0, 0]
    elif UP == 'X':
        ang, eixo = (np.pi/2 if flip else -np.pi/2), [0, 1, 0]
    else:                                           # ja e Z
        ang, eixo = (np.pi if flip else 0.0), [1, 0, 0]
    if ang:
        m.apply_transform(trimesh.transformations.rotation_matrix(ang, eixo))
    c = (m.bounds[0] + m.bounds[1]) / 2
    m.apply_translation([-c[0] + dx + CX, -c[1] + dy + CY, -m.bounds[0][2]])
    return m

feito, erros = {}, []
for p in CFG['pecas']:
    m = prep(p['stl'], p.get('flip', False))
    b = m.bounds
    feito[p['nome']] = p
    fora = b[0][0] < 0 or b[1][0] > BEDX or b[0][1] < 0 or b[1][1] > BEDY
    if fora: erros.append('%s fora da mesa' % p['nome'])
    if not m.is_watertight: erros.append('%s nao e watertight' % p['nome'])
    m.export(f'{OUT}/{p["nome"]}.stl')
    print('%-14s XY %6.2f x %6.2f  altura %5.2f  fechada=%s  %s'
          % (p['nome'], b[1][0]-b[0][0], b[1][1]-b[0][1], b[1][2], m.is_watertight,
             'FORA DA MESA' if fora else 'ok'))

ch = CFG.get('chapa')
if ch:
    partes = []
    for it in ch['itens']:
        src = feito[it['peca']]
        m = prep(src['stl'], src.get('flip', False), it.get('dx', 0), it.get('dy', 0))
        m.export(f'{OUT}/{ch["nome"]}__{it["peca"]}.stl')
        partes.append(m)
    u = trimesh.util.concatenate(partes); b = u.bounds
    fora = b[0][0] < 0 or b[1][0] > BEDX or b[0][1] < 0 or b[1][1] > BEDY
    if fora: erros.append('chapa fora da mesa')
    # colisao entre pecas da chapa, na projecao XY
    for i in range(len(partes)):
        for j in range(i+1, len(partes)):
            a, c2 = partes[i].bounds, partes[j].bounds
            if a[0][0] < c2[1][0] and c2[0][0] < a[1][0] and a[0][1] < c2[1][1] and c2[0][1] < a[1][1]:
                erros.append('chapa: %s e %s se sobrepoem'
                             % (ch['itens'][i]['peca'], ch['itens'][j]['peca']))
    print('%-14s XY %6.2f x %6.2f  %s' % (ch['nome'], b[1][0]-b[0][0], b[1][1]-b[0][1],
                                          'FORA DA MESA' if fora else 'ok'))
    print('  arquivos da chapa: ' + ' '.join(f'{OUT}/{ch["nome"]}__{it["peca"]}.stl'
                                             for it in ch['itens']))
if erros:
    print('\nPROBLEMAS:'); [print('  -', e) for e in erros]; sys.exit(1)
print('\nok')
