#!/usr/bin/env python3
"""Confere cada .gcode antes de mandar para a impressora. Sai com codigo 1 se algo falhar.

    python3 validar.py 255 255 saida/*.gcode
"""
import re, sys, os, base64, io
from collections import Counter
from PIL import Image

BEDX, BEDY = float(sys.argv[1]), float(sys.argv[2])
ARQS = sys.argv[3:]
# comandos que o Klipper da Anycubic nao entende ou que nao devem estar aqui
PROIBIDOS = {'M486', 'M73', 'G29', 'M420', 'M900 K0'}
falhas = []

for fn in ARQS:
    txt = open(fn, errors='ignore').read()
    corpo = re.split(r'; ---- fim ----|^M400\s*$', txt, flags=re.M)[0]
    X, Y, zmin, zmax = [], [], 1e9, -1e9
    for ln in corpo.splitlines():
        if ln[:3] not in ('G1 ', 'G0 '): continue
        for t in ln.split()[1:]:
            if t[:1] in 'XYZ':
                try: v = float(t[1:])
                except ValueError: continue
                if t[0] == 'X': X.append(v)
                elif t[0] == 'Y': Y.append(v)
                else: zmin, zmax = min(zmin, v), max(zmax, v)
    camadas = {float(m) for m in re.findall(r'^;Z:([\d.]+)', corpo, re.M)}
    cmds = Counter(re.findall(r'^([GM]\d+)', txt, re.M))
    pega = lambda p: (re.search(p, txt).group(1) if re.search(p, txt) else '?')
    nome = os.path.basename(fn); prob = []

    if 'G9111' not in txt: prob.append('sem G9111 -> a Kobra 3 vai acusar erro 10133')
    if not X or not Y: prob.append('nenhum movimento XY')
    else:
        if min(X) < 0 or max(X) > BEDX or min(Y) < 0 or max(Y) > BEDY:
            prob.append('percurso fora da mesa %gx%g' % (BEDX, BEDY))
    if zmin < 0: prob.append('Z negativo (%.2f)' % zmin)
    if not camadas: prob.append('sem marcas de camada ;Z:')
    for c in sorted(PROIBIDOS & set(cmds)): prob.append('comando indesejado: ' + c)

    mb = re.search(r'; thumbnail begin (\d+)x(\d+) (\d+)\n((?:; .*\n)+?); thumbnail end', txt)
    mini = 'ausente'
    if not mb:
        prob.append('sem miniatura')
    else:
        b64 = ''.join(l[2:] for l in mb.group(4).splitlines())
        if len(b64) != int(mb.group(3)): prob.append('miniatura: base64 nao bate com o cabecalho')
        try:
            im = Image.open(io.BytesIO(base64.b64decode(b64)))
            mini = '%sx%s %s' % (mb.group(1), mb.group(2), im.format)
            if im.format != 'PNG': prob.append('miniatura nao e PNG')
        except Exception as e:
            prob.append('miniatura ilegivel: %s' % e)

    print('=== %-28s %5.2f MB' % (nome, os.path.getsize(fn) / 1e6))
    print('    G9111:      %s' % (pega(r'(G9111 [^\n]+)')))
    if X: print('    mesa:       X %.1f..%.1f   Y %.1f..%.1f   (limite %gx%g)'
                % (min(X), max(X), min(Y), max(Y), BEDX, BEDY))
    print('    Z:          %.2f .. %.2f   camadas %d   1a %.2f'
          % (zmin, zmax, len(camadas), min(camadas) if camadas else 0))
    print('    miniatura:  %s' % mini)
    print('    material:   %s mm = %s g   |  %s'
          % (pega(r'; filament used \[mm\] = ([\d.]+)'),
             pega(r'; total filament used \[g\] = ([\d.]+)'),
             pega(r'; estimated printing time \(normal mode\) = (.+)')))
    print('    objetos:    %s' % ', '.join(sorted(set(re.findall(r'; printing object (\S+)', txt)))))
    print('    comandos:   %s' % '  '.join('%s×%d' % kv for kv in sorted(cmds.items())))
    print('    -> %s\n' % ('OK' if not prob else 'FALHOU: ' + '; '.join(prob)))
    if prob: falhas.append(nome)

if falhas:
    print('REPROVADOS: %s' % ', '.join(falhas)); sys.exit(1)
print('todos os %d arquivos passaram' % len(ARQS))
