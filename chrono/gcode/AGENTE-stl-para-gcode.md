# Tarefa · transformar arquivos `.stl` em `.gcode` para a **Anycubic Kobra 3**

Runbook auto-contido. Tudo o que você precisa está aqui dentro: o perfil, os scripts, os
comandos e o critério de aceite. **Não invente perfil de impressora** — o que está aqui foi
extraído do perfil oficial da Kobra 3 no OrcaSlicer e testado ponta a ponta.

---

## 1. O que entregar

Um `.gcode` por peça, mais um com todas na mesma mesa, prontos para o cartão SD /
transferência. Nada de "provavelmente funciona": só declare pronto quando
**`validar.py` sair com código 0**.

## 2. O erro que este runbook existe para evitar

A Kobra 3 **valida o arquivo antes de imprimir**. Se o start-gcode não for o dela, o painel
para com:

> **CODE: 10133 — The file is missing necessary commands, which may cause printing errors**

O comando que ela procura é **`G9111`**, a macro própria da Anycubic que faz home,
nivelamento, aquecimento de mesa e bico e a purga, tudo de uma vez:

```gcode
G9111 bedTemp=60 extruderTemp=210
```

Um perfil Marlin comum abre com `G28` + `M190` + `M109` — e é recusado. Toda a diferença
entre um arquivo que imprime e um que não imprime está nessa linha.

**Fontes** (confira se desconfiar):
- <https://wiki.anycubic.com/en/error-codes/10133-code/k3>
- <https://raw.githubusercontent.com/OrcaSlicer/OrcaSlicer/main/resources/profiles/Anycubic/machine/Anycubic%20Kobra%203%200.4%20nozzle.json>

## 3. Dados da máquina

| | |
|---|---|
| Mesa | **255 × 255 × 260 mm**, origem no canto, centro em X127,5 Y127,5 |
| Firmware | **Klipper** (fork da Anycubic) → `gcode_flavor = klipper` |
| Bico | 0,40 mm de fábrica (existe perfil oficial de 0,2 / 0,6 / 0,8) |
| Start | `G9111 bedTemp=… extruderTemp=…` + `M117` + `M900 K0.051` |
| Fim | `M400`, retração, sobe, park em **X250 Y220**, desliga |
| Pausa | `M601` |
| Miniatura | **230 × 110 PNG** — aparece no painel |

## 4. Ambiente

```bash
apt-get update -qq && apt-get install -y --no-install-recommends prusa-slicer
pip install trimesh numpy pillow
export QT_QPA_PLATFORM=offscreen      # o CLI roda headless com isso
prusa-slicer --help | head -2         # confirme que abriu
```

Se `prusa-slicer` não estiver disponível, **pare e diga isso** em vez de escrever G-code à
mão. G-code manual não tem perímetro, retração, resfriamento nem compensação de fluxo.

## 5. Estrutura de trabalho

```
./stl/            os .stl de entrada
./prep/           gerado — .stl orientados e posicionados na mesa
./saida/          gerado — os .gcode finais
pecas.json  kobra3.ini  preparar.py  miniatura.py  validar.py
```

## 6. `pecas.json` — a única coisa que você edita por trabalho

```json
{
  "mesa": [255, 255],
  "eixo_vertical_do_stl": "Y",
  "saida": "prep",
  "pecas": [
    { "nome": "pino",     "stl": "stl/Chrono_01_Pino_Travinha.stl", "flip": true },
    { "nome": "anel_dia", "stl": "stl/Chrono_02_Anel_Dia.stl",      "flip": false },
    { "nome": "anel_mes", "stl": "stl/Chrono_03_Anel_Mes.stl",      "flip": false }
  ],
  "chapa": {
    "nome": "chapa_3_pecas",
    "itens": [
      { "peca": "pino",     "dx": -26, "dy":  12 },
      { "peca": "anel_dia", "dx":  26, "dy":  12 },
      { "peca": "anel_mes", "dx":   0, "dy": -26 }
    ]
  }
}
```

Campos:
- **`mesa`** — `[255, 255]` na Kobra 3. As peças são centradas nela.
- **`eixo_vertical_do_stl`** — `"Y"`, `"X"` ou `"Z"`. Qual eixo do STL é o eixo da peça.
  Muito CAD exporta com Y para cima; se você fatiar sem corrigir, a peça sai **deitada**.
  Confira o bounding box antes de decidir.
- **`flip`** — `true` inverte a peça de cabeça para baixo.
- **`chapa`** — opcional; junta as peças numa mesa só, com deslocamento `dx`/`dy` em mm a
  partir do centro. O script recusa se duas se sobrepuserem.

### Como escolher a orientação

1. **Face plana grande na mesa.** Adesão é o que mais quebra impressão de peça pequena.
2. **Nada de teto horizontal fechado.** Uma peça em forma de cuia, impressa com a boca para
   cima, cria um teto no ar que só o suporte resolve — e o suporte fica trancado dentro.
   Inverta: a boca abre para cima e o suporte deixa de ser necessário.
3. **Detalhe que precisa ficar legível vai para cima**, não contra a mesa.
4. Balanço acima de ~50° o suporte automático pega; abaixo disso ele não é acionado.

## 7. `kobra3.ini` — o perfil

Cole exatamente assim. As duas últimas linhas (`start_gcode`, `end_gcode`) precisam ser
**uma linha cada**, com `\n` literal separando os comandos — o formato de INI do
PrusaSlicer não aceita valor quebrado em várias linhas.

```ini
# ============================================================================
# Perfil Anycubic Kobra 3 / bico 0,40 / PLA — datador Chrono, prototipo de encaixe
# Anycubic Kobra 3 · mesa 255x255x260 · firmware Klipper.
# start_gcode = G9111 (macro da Anycubic: home + nivelamento + aquece + purga).
# E o comando que a Kobra 3 procura; sem ele o painel acusa erro 10133.
# ============================================================================
printer_technology = FFF
bed_shape = 0x0,255x0,255x255,0x255
max_print_height = 260
nozzle_diameter = 0.4
gcode_flavor = klipper
use_relative_e_distances = 0
gcode_comments = 1
z_offset = 0
retract_length = 1.5
retract_speed = 35
deretract_speed = 25
retract_lift = 0.4
retract_before_travel = 2
retract_before_wipe = 70%
wipe = 1
travel_speed = 120
travel_speed_z = 10
machine_max_feedrate_x = 500
machine_max_feedrate_y = 500

filament_diameter = 1.75
filament_type = PLA
filament_density = 1.24
filament_cost = 90
extrusion_multiplier = 1
temperature = 205
first_layer_temperature = 210
bed_temperature = 60
first_layer_bed_temperature = 60

cooling = 1
fan_always_on = 1
min_fan_speed = 100
max_fan_speed = 100
bridge_fan_speed = 100
disable_fan_first_layers = 1
full_fan_speed_layer = 3
fan_below_layer_time = 100
slowdown_below_layer_time = 20
min_print_speed = 10

layer_height = 0.1
first_layer_height = 0.2
perimeters = 3
top_solid_layers = 5
bottom_solid_layers = 4
fill_density = 100%
fill_pattern = rectilinear
top_fill_pattern = monotonic
bottom_fill_pattern = monotonic
solid_infill_every_layers = 0
infill_every_layers = 1
thin_walls = 1
gap_fill_enabled = 1
extra_perimeters = 0
avoid_crossing_perimeters = 1
seam_position = aligned
external_perimeters_first = 0
elefant_foot_compensation = 0.1

extrusion_width = 0.4
first_layer_extrusion_width = 0.42
external_perimeter_extrusion_width = 0.4
perimeter_extrusion_width = 0.4
infill_extrusion_width = 0.4
solid_infill_extrusion_width = 0.4
top_infill_extrusion_width = 0.38
support_material_extrusion_width = 0.36

perimeter_speed = 25
external_perimeter_speed = 15
small_perimeter_speed = 12
infill_speed = 35
solid_infill_speed = 30
top_solid_infill_speed = 22
gap_fill_speed = 20
bridge_speed = 20
first_layer_speed = 15
support_material_speed = 40
support_material_interface_speed = 80%

brim_type = outer_only
brim_width = 3
brim_separation = 0.1
skirts = 0

support_material = 1
support_material_auto = 1
support_material_style = snug
support_material_threshold = 50
support_material_buildplate_only = 1
support_material_contact_distance = 0.1
support_material_bottom_contact_distance = 0.1
support_material_spacing = 1.6
support_material_pattern = rectilinear
support_material_interface_layers = 2
support_material_bottom_interface_layers = 2
support_material_xy_spacing = 60%
support_material_angle = 0
dont_support_bridges = 1

complete_objects = 0
gcode_label_objects = octoprint

layer_gcode = ;AFTER_LAYER_CHANGE\n;[layer_z]

machine_max_acceleration_x = 15000,15000
machine_max_acceleration_y = 15000,15000
thumbnails = 230x110
thumbnails_format = PNG
pause_print_gcode = M601
start_gcode = ; ---- Chrono datador · Anycubic Kobra 3 · bico 0,40 · PLA ----\nG9111 bedTemp={first_layer_bed_temperature[0]} extruderTemp={first_layer_temperature[0]}\nM117\nM900 K0.051 ; pressure advance
end_gcode = ; ---- fim ----\nM400\nG92 E0\nG1 E-2 F3600\n{if max_layer_z < max_print_height - 1}G1 Z{max_layer_z + 2} F900{endif}\nG1 X250 Y220 F12000 ; apresenta a peca\nM140 S0\nM104 S0\nM107\nM84
autoemit_temperature_commands = 0
```

## 8. Scripts

### `preparar.py`

```python
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
```

### `miniatura.py`

```python
#!/usr/bin/env python3
"""Renderiza o STL de cima e injeta a miniatura 230x110 PNG no .gcode, no formato
que PrusaSlicer/Orca escrevem e a Kobra 3 le. O CLI do PrusaSlicer nao gera
miniatura sem interface grafica, por isso este passo existe.

    python3 miniatura.py saida.gcode peca.stl [mais.stl ...]
"""
import base64, io, sys, pathlib
import numpy as np, trimesh
from PIL import Image

W, H = 230, 110
FUNDO = (243, 245, 245)
COR = (206, 214, 220)
LUZ = np.array([0.12, 0.24, 0.96]); LUZ /= np.linalg.norm(LUZ)

def render(stls, W2=920, H2=440):
    tris = np.vstack([trimesh.load(s).triangles for s in stls])
    # vista de cima do STL ja preparado (Z para cima): tela X = X, tela Y = Y,
    # profundidade = Z. Nao troca eixo nenhum — trocar espelha a peca.
    V = tris.copy()
    p = V.reshape(-1, 3); mn, mx = p.min(0), p.max(0)
    c = (mn + mx) / 2; sp = (mx - mn) * 1.08
    # cabe a peca inteira no quadro deitado 230x110, sem cortar
    sc = min(W2 / max(sp[0], 1e-6), H2 / max(sp[1], 1e-6))
    img = np.full((H2, W2, 3), float(FUNDO[0])); img[:] = FUNDO
    zb = np.full((H2, W2), -1e18)
    n = np.cross(V[:, 1] - V[:, 0], V[:, 2] - V[:, 0])
    ln = np.linalg.norm(n, axis=1); ok = ln > 1e-12
    V, n = V[ok], n[ok] / ln[ok][:, None]
    sh = np.clip(np.abs(n @ LUZ), 0, 1) * 0.74 + 0.26
    sx = (V[:, :, 0] - c[0]) * sc + W2 / 2
    sy = H2 / 2 - (V[:, :, 1] - c[1]) * sc
    sz = V[:, :, 2]
    for i in range(len(V)):
        ax, ay = sx[i, 0], sy[i, 0]; bx, by = sx[i, 1], sy[i, 1]; cx, cy = sx[i, 2], sy[i, 2]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9: continue
        X0 = max(int(min(ax, bx, cx)), 0); X1 = min(int(max(ax, bx, cx)) + 1, W2 - 1)
        Y0 = max(int(min(ay, by, cy)), 0); Y1 = min(int(max(ay, by, cy)) + 1, H2 - 1)
        if X1 < X0 or Y1 < Y0: continue
        gx, gy = np.meshgrid(np.arange(X0, X1 + 1) + .5, np.arange(Y0, Y1 + 1) + .5)
        l1 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / den
        l2 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / den
        m = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
        if not m.any(): continue
        z = l1 * sz[i, 0] + l2 * sz[i, 1] + (1 - l1 - l2) * sz[i, 2]
        sub = zb[Y0:Y1+1, X0:X1+1]; up = m & (z > sub); sub[up] = z[up]
        img[Y0:Y1+1, X0:X1+1][up] = np.array(COR) * sh[i]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

def bloco(im):
    im = im.copy(); im.thumbnail((W, H), Image.LANCZOS)
    cv = Image.new('RGB', (W, H), FUNDO)
    cv.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    buf = io.BytesIO(); cv.save(buf, 'PNG', optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    ls = ['; thumbnail begin %dx%d %d' % (W, H, len(b64))]
    ls += ['; ' + b64[i:i+76] for i in range(0, len(b64), 76)]
    ls += ['; thumbnail end', ';']
    return '\n'.join(ls) + '\n'

g = pathlib.Path(sys.argv[1]); stls = sys.argv[2:]
L = g.read_text(errors='ignore').splitlines(keepends=True)
if any('thumbnail begin' in l for l in L[:80]):
    print('%s ja tem miniatura' % g.name)
else:
    b = bloco(render(stls))
    L.insert(1, b); g.write_text(''.join(L))
    print('%-26s miniatura 230x110 injetada (%d bytes)' % (g.name, len(b)))
```

### `validar.py`

```python
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
```

## 9. Pipeline

```bash
export QT_QPA_PLATFORM=offscreen
set -e

python3 preparar.py pecas.json          # orienta, apoia em z=0, centra, checa colisão

for p in pino anel_dia anel_mes; do     # troque pelos nomes do seu pecas.json
  prusa-slicer --export-gcode --dont-arrange --load kobra3.ini \
               -o saida/$p.gcode prep/$p.stl
  python3 miniatura.py saida/$p.gcode prep/$p.stl
done

# a chapa: --merge junta os objetos, --dont-arrange preserva a posição de cada um
prusa-slicer --export-gcode --merge --dont-arrange --load kobra3.ini \
             -o saida/chapa_3_pecas.gcode prep/chapa_3_pecas__*.stl
python3 miniatura.py saida/chapa_3_pecas.gcode prep/chapa_3_pecas__*.stl

python3 validar.py 255 255 saida/*.gcode
```

## 10. Critério de aceite

`validar.py` tem de sair com **código 0**. Ele reprova o arquivo se:

- [ ] não tiver **`G9111`** → a Kobra 3 acusaria 10133
- [ ] o percurso sair da mesa 255 × 255
- [ ] aparecer **Z negativo**
- [ ] não tiver marca de camada `;Z:`
- [ ] faltar miniatura, ou o base64 não bater com o tamanho declarado no cabeçalho
- [ ] aparecer comando indesejado: `M486`, `M73`, `G29`, `M420`

Confira também, com o olho, no relatório que ele imprime:

- [ ] **contagem de camadas** compatível com a altura da peça
  (altura ÷ `layer_height`, + 1 da primeira camada)
- [ ] **objetos** — na chapa têm de aparecer **todos**. Se aparecer um só, você esqueceu
  o `--merge`
- [ ] **lista de comandos** sem nada estranho. O esperado é só:
  `G1 G21 G90 G9111 G92 M82 M84 M104 M106 M107 M117 M140 M400 M900`

## 11. Armadilhas já pagas — não repita

| Sintoma | Causa | Correção |
|---|---|---|
| Painel acusa 10133 | start-gcode Marlin (`G28`/`M190`/`M109`) | `G9111` |
| A chapa sai com **uma peça só** | `--merge` ausente. Sem ele o CLI trata cada STL como um trabalho separado e sobrescreve a saída | `--merge --dont-arrange` |
| Peça sai **deitada** | STL com Y para cima fatiado sem rotação | `eixo_vertical_do_stl` |
| `M109` redundante depois do `G9111` | o PrusaSlicer injeta comando de temperatura por conta própria | `autoemit_temperature_commands = 0` |
| Sem miniatura | o CLI não renderiza miniatura sem interface gráfica, mesmo com `thumbnails` no perfil | `miniatura.py` |
| Miniatura de lado ou espelhada | troca de eixo na hora de renderizar | vista de cima do STL **já preparado**: tela X = X, tela Y = Y, profundidade = Z. Não troque eixo nenhum |
| `'=' character not found in line` ao carregar o INI | `start_gcode` quebrado em várias linhas | uma linha só, com `\n` literal |
| Peça pequena solta da mesa no meio | sem brim | `brim_width = 3`, `brim_type = outer_only` |

## 12. Se o painel ainda reclamar

O caminho que a Anycubic garante é o dela: abrir os **STL** no **Anycubic Slicer Next** e
fatiar lá. A checagem de arquivo do firmware não é documentada. O que está neste runbook foi
reconstruído do perfil oficial do OrcaSlicer, que é o que a comunidade usa nessa máquina, e
passa na validação — mas quem tem a última palavra é o firmware.

## 13. Variações

| Quero | Faça |
|---|---|
| Escala | `--scale 3` no comando do PrusaSlicer |
| Bico 0,25 | `nozzle_diameter = 0.25` e as larguras de extrusão para 0,25 / 0,27 / 0,24 |
| Camada mais grossa (mais rápido) | `layer_height = 0.2`, `first_layer_height = 0.25` |
| ABS / PETG | mude `filament_type`, `temperature`, `bed_temperature` e desligue `fan_always_on` |
| Outra impressora | `bed_shape`, `max_print_height`, `gcode_flavor` e principalmente o
`start_gcode`/`end_gcode` **da máquina certa** — puxe do perfil oficial dela no OrcaSlicer |

## 14. Limite de peça pequena em FDM — não prometa o que não sai

Antes de dizer que a impressão "valida o projeto", faça esta conta: divida a menor
dimensão de cada detalhe pela largura de extrusão (0,40 mm com bico 0,40).

| Detalhe | Cota | Contra 0,40 mm |
|---|---|---|
| Traço de número gravado | 0,52 mm | 1,3 extrusão — **forma, mas sai esfarrapado** |
| Folga entre peças que giram | 0,10 mm | funde. **Não gira** |
| Saliência de encaixe | 0,40 mm | 1 extrusão — forma torto |
| Mola de detente | 0,15 mm de altura | 1,5 camada — no limite |

Regra prática: **detalhe abaixo de 2 extrusões (0,80 mm) não sai limpo**, e **folga móvel
abaixo de 0,30 mm cola**. Para essas duas coisas: bico de 0,25 mm, ou escala ≥ 2×. A peça
1:1 continua valendo — ela prova diâmetro, proporção e **encaixe na peça real**, que é
normalmente o que se quer saber primeiro. Diga qual dos dois testes o arquivo entrega.
