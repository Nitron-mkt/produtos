#!/usr/bin/env python3
"""Arredonda para inteiro a velocidade do cooler (M106 S...).

Motivo: com min_fan_speed != max_fan_speed, ou com full_fan_speed_layer > 0, o
PrusaSlicer interpola e escreve "M106 S28.05". O Klipper aceita float, mas os
.gcode que a Kobra 3 do cliente imprimiu de fato so tinham inteiros — nao vale a
pena introduzir um formato novo num arquivo que a impressora valida antes de
imprimir.

CUIDADO: mexe SO em M106 S. Nao toque em M900 K (pressure advance) — o valor
util (0.051) arredonda para 0 e voce desliga o pressure advance sem perceber.

Uso:  python3 inteiros.py arquivo.gcode [...]   (reescreve no lugar)
"""
import re, sys

RE = re.compile(r'^(M106\s+S)(\d+\.\d+)', re.M)

for fn in sys.argv[1:]:
    txt = open(fn, errors='ignore').read()
    n = len(RE.findall(txt))
    if n:
        open(fn, 'w').write(RE.sub(lambda m: '%s%d' % (m.group(1), round(float(m.group(2)))), txt))
        txt = open(fn, errors='ignore').read()
    fan = sorted({float(v) for v in re.findall(r'^M106 S([\d.]+)', txt, re.M)})
    pa  = re.findall(r'^M900 [^\n]*', txt, re.M)
    print('%-44s %3d arredondados | M106 S: %s | %s'
          % (fn.split('/')[-1], n, [int(v) for v in fan], pa[0] if pa else 'sem M900'))
