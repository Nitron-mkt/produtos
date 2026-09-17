# Runbook — STL → .gcode para Anycubic Kobra 3 Max em PETG

> **Testado.** Os blocos de código deste arquivo foram extraídos para um diretório
> vazio e rodados de ponta a ponta — `preparar` → `fatiar` → `miniatura` → `validar` →
> `camada` — sem nada copiado de fora. Se você copiar como está, funciona.

Este arquivo é auto-contido. Quem receber ele **não precisa de nenhum contexto anterior**:
tudo que é necessário — perfil, scripts, comandos, critério de aceite e as armadilhas já
pagas — está aqui dentro. Copie os blocos como estão.

## O que você vai fazer

Receber arquivos `.stl` de peças pequenas de utilidade doméstica e devolver `.gcode` que
a **Anycubic Kobra 3 Max** aceite e imprima em **PETG**, com um objeto por arquivo (ou
uma mesa com vários, quando pedido).

| | |
|---|---|
| Impressora | Anycubic Kobra 3 Max — mesa **420 × 420 × 500**, centro **210 / 210** |
| Firmware | Klipper (macro própria da Anycubic) |
| Bico | 0,40 mm |
| Material | PETG (rótulo CR-PETG: 1,75 mm, 230–250 °C) |
| Fatiador | PrusaSlicer 2.7.2 por linha de comando, sem interface |

> ⚠️ **Confirme a mesa ANTES de fatiar, e confirme também onde o `end_gcode`
> estaciona o bico.** O firmware da Anycubic valida o arquivo antes de imprimir: uma
> coordenada fora do curso da máquina — inclusive a do estacionamento final — faz ele
> **recusar o arquivo sem mensagem nenhuma**, e o sintoma é "coloco e não acontece
> nada". Isso já aconteceu neste projeto: o `end_gcode` mandava o bico para `X400 Y400`
> e nenhum dos cinco arquivos rodou. Na dúvida, fatie para **255 × 255 com o
> estacionamento em X250 Y220**, que cabe nas duas máquinas.

> **Se a impressora for a Kobra 3 comum e não a Max**, troque no `.ini`:
> `bed_shape = 0x0,255x0,255x255,0x255`, `max_print_height = 260`, e centre as peças em
> **127,5 / 127,5** em vez de 210 / 210. Todo o resto vale igual.

---

## 1. Ambiente

```bash
prusa-slicer --version        # precisa existir; testado na 2.7.2
python3 -c "import trimesh, numpy, PIL; print('ok')"
```

Se faltar: `pip install trimesh numpy pillow manifold3d`.

O PrusaSlicer roda sem tela, mas exige a variável abaixo em **toda** invocação:

```bash
export QT_QPA_PLATFORM=offscreen
```

Sem ela o binário tenta abrir janela e morre.

---

## 2. O perfil

Grave como `kobra3max_petg.ini`. **Não reescreva do zero** — os valores não são
preferência, são o que faz a máquina aceitar e o PETG grudar. O porquê de cada grupo
está na seção 6.

```ini
# ============================================================================
# Perfil Anycubic Kobra 3 / bico 0,40 / PLA — datador Chrono, prototipo de encaixe
# Anycubic Kobra 3 · mesa 255x255x260 · firmware Klipper.
# start_gcode = G9111 (macro da Anycubic: home + nivelamento + aquece + purga).
# E o comando que a Kobra 3 procura; sem ele o painel acusa erro 10133.
# ============================================================================
printer_technology = FFF
bed_shape = 0x0,420x0,420x420,0x420
max_print_height = 500
nozzle_diameter = 0.4
gcode_flavor = klipper
use_relative_e_distances = 0
gcode_comments = 1
z_offset = 0
retract_length = 1.2
retract_speed = 30
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
filament_type = PETG
filament_density = 1.27
filament_cost = 90
extrusion_multiplier = 0.95
temperature = 240
first_layer_temperature = 245
bed_temperature = 80
first_layer_bed_temperature = 80

cooling = 1
fan_always_on = 1
min_fan_speed = 40
max_fan_speed = 40
bridge_fan_speed = 60
disable_fan_first_layers = 4
full_fan_speed_layer = 8
fan_below_layer_time = 100
slowdown_below_layer_time = 25
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
elefant_foot_compensation = 0

extrusion_width = 0.4
first_layer_extrusion_width = 0.50
external_perimeter_extrusion_width = 0.4
perimeter_extrusion_width = 0.4
infill_extrusion_width = 0.4
solid_infill_extrusion_width = 0.4
top_infill_extrusion_width = 0.38
support_material_extrusion_width = 0.36

perimeter_speed = 25
external_perimeter_speed = 15
small_perimeter_speed = 12
infill_speed = 30
solid_infill_speed = 30
top_solid_infill_speed = 22
gap_fill_speed = 20
bridge_speed = 20
first_layer_speed = 15
support_material_speed = 40
support_material_interface_speed = 80%

brim_type = outer_only
brim_width = 8
brim_separation = 0
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
start_gcode = ; ---- Chrono datador · Anycubic Kobra 3 MAX · bico 0,40 · PETG ----\nG9111 bedTemp={first_layer_bed_temperature[0]} extruderTemp={first_layer_temperature[0]}\nM117\nM900 K0.051 ; pressure advance
end_gcode = ; ---- fim ----\nM400\nG92 E0\nG1 E-2 F3600\n{if max_layer_z < max_print_height - 1}G1 Z{max_layer_z + 2} F900{endif}\nG1 X250 Y220 F12000 ; apresenta a peca\nM140 S0\nM104 S0\nM107\nM84
autoemit_temperature_commands = 0
```

### Duas linhas que você não pode quebrar

`start_gcode` e `end_gcode` são **uma linha só cada**, com `\n` literal (barra + n)
separando os comandos. Se você editar esse arquivo com `re.sub` em Python e usar `\n`
na string de substituição, o Python troca por uma quebra de linha DE VERDADE, o `.ini`
passa a ter linhas sem `=`, e o PrusaSlicer morre com
`'=' character not found in line`. Para montar essas linhas, junte com `'\\n'`
(barra escapada), nunca com `'\n'`.

---

## 3. Preparar os STL

Trabalhe tudo num diretório só, com esta estrutura:

```
.
├── kobra3max_petg.ini      seção 2
├── pecas.json              abaixo
├── preparar.py             abaixo
├── inteiros.py             seção 5
├── miniatura.py            seção 6
├── valida.py               seção 7
├── camada.py               seção 6
├── stl/                    os .stl que você recebeu
├── prep/                   criado por preparar.py
└── saida/                  crie você:  mkdir -p saida
```


As peças vêm modeladas no sistema do produto (eixo em **Y**, na altura real da tampa).
Para imprimir é preciso: deitar o eixo em Z, apoiar em z=0 e centrar na mesa.

Grave `pecas.json` descrevendo o que fatiar:

```json
{ "mesa": [420,420], "eixo_vertical_do_stl": "Y", "saida": "prep",
  "pecas": [
    {"nome":"m01_valvula", "stl":"stl/Chrono_M01_Valvula_Dias.stl"},
    {"nome":"m02_rodinha", "stl":"stl/Chrono_M02_Rodinha_Meses.stl"},
    {"nome":"m03_ponteira","stl":"stl/Chrono_M03_Ponteira.stl", "flip":true}
  ],
  "chapa": {"nome":"chapa", "itens":[
    {"peca":"m01_valvula", "dx":-30, "dy": 25},
    {"peca":"m02_rodinha", "dx": 35, "dy": 25},
    {"peca":"m03_ponteira","dx":  0, "dy":-30}
  ]}
}
```

`flip: true` vira a peça de cabeça para baixo. **Use quando a peça tem pino, haste ou
ponta apontando para baixo** — senão ela apoia na ponta. Regra prática: rode
`preparar.py`, olhe a área de contato reportada, e se der menos que ~20 mm² tente com
`flip` e compare.

`chapa` é opcional: só quando quiserem tudo numa mesa. `dx`/`dy` são deslocamentos em
mm a partir do centro.

Grave `preparar.py`:

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

```bash
python3 preparar.py pecas.json
```

Ele já **recusa** peça fora da mesa, peça não-watertight e peças da chapa que se
sobreponham. Se acusar, conserte antes de fatiar.

---

## 4. Fatiar

```bash
export QT_QPA_PLATFORM=offscreen

# uma peça por arquivo
prusa-slicer --export-gcode --dont-arrange --load kobra3max_petg.ini \
             --brim-width 10 -o saida/1_valvula.gcode prep/m01_valvula.stl

prusa-slicer --export-gcode --dont-arrange --load kobra3max_petg.ini \
             --brim-width 8  -o saida/2_rodinha.gcode prep/m02_rodinha.stl

prusa-slicer --export-gcode --dont-arrange --load kobra3max_petg.ini \
             --brim-width 8  -o saida/3_ponteira.gcode prep/m03_ponteira.stl

# tudo numa mesa só
prusa-slicer --export-gcode --merge --dont-arrange --load kobra3max_petg.ini \
             --brim-width 8 -o saida/tudo.gcode \
             prep/chapa__m01_valvula.stl prep/chapa__m02_rodinha.stl prep/chapa__m03_ponteira.stl
```

**`--merge` é obrigatório para a mesa com várias peças.** Sem ele o CLI sobrescreve a
saída a cada arquivo e você termina com **uma peça só** no gcode, sem nenhum erro.

**`--dont-arrange` é obrigatório sempre.** Sem ele o PrusaSlicer reposiciona as peças e
joga fora o centramento que o `preparar.py` fez.

---

## 5. Pós-processar: arredondar `M106 S`

`M106` é a velocidade do cooler, numa escala de 0 a 255. Quando `min_fan_speed`
difere de `max_fan_speed`, **ou** quando `full_fan_speed_layer > 0`, o PrusaSlicer
interpola e escreve valores com casa decimal — `M106 S28.05`, `M106 S76.5`.

O Klipper aceita float sem reclamar. Mas os .gcode que a Kobra 3 deste cliente
imprimiu de fato **só tinham inteiros** (51/102/153/204/255). A impressora valida o
arquivo antes de imprimir, e não vale a pena introduzir um formato que os arquivos
bons nunca tiveram. Arredonde.

Grave `inteiros.py`:

```python
#!/usr/bin/env python3
"""Arredonda para inteiro a velocidade do cooler (M106 S...).

CUIDADO: mexe SO em M106 S. Nao generalize para "todo parametro M com decimal" —
M900 K0.051 (pressure advance) tambem casa nesse padrao e arredonda para K0, o que
desliga o pressure advance sem nenhum aviso. Ja aconteceu.

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
```

Rode em **todos** os arquivos, sempre antes da miniatura:

```bash
python3 inteiros.py saida/*.gcode
```

Aceite só se a saída mostrar `M900 K0.051` intacto em cada arquivo.

## 6. Injetar a miniatura

O CLI do PrusaSlicer **não gera miniatura sem interface gráfica**, mesmo com
`thumbnails` configurado. Sem miniatura o painel da impressora mostra um quadrado
cinza. Este passo existe só por causa disso.

Grave `miniatura.py`:

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

```bash
python3 miniatura.py saida/1_valvula.gcode prep/m01_valvula.stl
python3 miniatura.py saida/tudo.gcode prep/chapa__m01_valvula.stl prep/chapa__m02_rodinha.stl prep/chapa__m03_ponteira.stl
```

Passe **os mesmos STL** que foram fatiados, na mesma ordem.

---

## 7. Validar — e este passo não é opcional

Grave `valida.py`:

```python
import re, glob, os, sys, base64, io
from collections import Counter
from PIL import Image
BEDX=BEDY=420.0
DIR = sys.argv[1] if len(sys.argv) > 1 else 'saida'   # python3 valida.py [diretorio]
for fn in sorted(glob.glob(os.path.join(DIR,'*.gcode'))):
    txt=open(fn,errors='ignore').read()
    body=txt.split('; ---- fim ----')[0]
    X=[];Y=[];zmax=-1e9;zmin=1e9
    for ln in body.splitlines():
        if ln[:3] not in ('G1 ','G0 '): continue
        for t in ln.split()[1:]:
            if t[:1] in 'XYZ':
                try: v=float(t[1:])
                except: continue
                if t[0]=='X': X.append(v)
                elif t[0]=='Y': Y.append(v)
                else: zmax=max(zmax,v); zmin=min(zmin,v)
    Zl={float(m) for m in re.findall(r'^;Z:([\d.]+)',body,re.M)}
    cmds=Counter(m for m in re.findall(r'^([GM]\d+)',txt,re.M))
    g=lambda p:(re.search(p,txt).group(1) if re.search(p,txt) else '?')
    # miniatura
    mb=re.search(r'; thumbnail begin (\d+)x(\d+) (\d+)\n((?:; .*\n)+?); thumbnail end', txt)
    mini='ausente'
    if mb:
        b64=''.join(l[2:] for l in mb.group(4).splitlines())
        ok = len(b64)==int(mb.group(3))
        try:
            im=Image.open(io.BytesIO(base64.b64decode(b64))); mini='%s %s (base64 %s)'%(mb.group(1)+'x'+mb.group(2), im.format, 'confere' if ok else 'TAMANHO ERRADO')
        except Exception as e: mini='ILEGIVEL: %s'%e
    objs=sorted(set(re.findall(r'; printing object (\S+)',txt)))
    print('=== %-22s %5.2f MB'%(os.path.basename(fn), os.path.getsize(fn)/1e6))
    print('    G9111 presente:      %s'%('SIM  ->  '+g(r'(G9111 [^\n]+)') if 'G9111' in txt else '*** NAO ***'))
    print('    mesa %.0fx%.0f:        X %.1f..%.1f  Y %.1f..%.1f  -> %s'%(BEDX,BEDY,min(X),max(X),min(Y),max(Y),
          'DENTRO' if (min(X)>=0 and max(X)<=BEDX and min(Y)>=0 and max(Y)<=BEDY) else '*** FORA ***'))
    print('    Z %.2f..%.2f   camadas %d   1a camada %.2f'%(zmin,zmax,len(Zl),min(Zl)))
    print('    miniatura:           %s'%mini)
    print('    %s mm de filamento = %s g   |  %s'%(g(r'; filament used \[mm\] = ([\d.]+)'),
          g(r'; total filament used \[g\] = ([\d.]+)'), g(r'; estimated printing time \(normal mode\) = (.+)')))
    print('    objetos:             %s'%', '.join(objs))
    print('    comandos usados:     %s'%'  '.join('%s×%d'%(k,v) for k,v in sorted(cmds.items())))
    print()
```

```bash
python3 valida.py saida
```

### Critério de aceite — todos têm de passar

| Item | Esperado | Por que importa |
|---|---|---|
| **`G9111` presente** | `G9111 bedTemp=80 extruderTemp=245` | A Kobra 3 **valida o arquivo antes de imprimir** e procura a macro própria da Anycubic. Sem ela: **erro 10133 — "The file is missing necessary commands"**, o arquivo é recusado e não é problema de geometria. |
| **Percurso dentro da mesa** | 0 a 420 em X e Y | Fora disso a máquina bate no fim de curso. |
| **Z começa em 0,20** | e nunca negativo | Z máximo dá ~0,40 acima da peça: é o *z-hop* de retração, não material. |
| **Miniatura** | 230 × 110 PNG, base64 batendo | Painel. |
| **Lista de comandos** | só `G1 G21 G90 G9111 G92 M82 M84 M104 M106 M107 M117 M140 M400 M900` | Nada de `G28`, `M109`, `M190`, `M486`, `M73` — o `G9111` já faz home, nivelamento, aquecimento e purga. |

### Olhe uma camada antes de entregar

Número de 0,32 mm de traço e janela de 3,60 mm **não aparecem** num relatório de texto.
Grave `camada.py`:

```python
import re, sys, numpy as np
from PIL import Image, ImageDraw
def paths(fn, zalvo, tol=0.01):
    segs=[]; x=y=z=None; ext=False; cur=[]
    for ln in open(fn,errors='ignore'):
        if ln.startswith(';Z:'):
            try: z=float(ln[3:]) 
            except: pass
            continue
        if not (ln.startswith('G1 ') or ln.startswith('G0 ')): continue
        d={}
        for t in ln.split()[1:]:
            if t[:1] in 'XYZEF':
                try: d[t[0]]=float(t[1:])
                except: pass
        nx=d.get('X',x); ny=d.get('Y',y)
        e=d.get('E')
        if z is not None and abs(z-zalvo)<tol and x is not None and nx is not None:
            if e is not None and e>0 and ('X' in d or 'Y' in d):
                cur.append((x,y)); cur.append((nx,ny))
        x,y=nx,ny
        if 'Z' in d: pass
    return cur
def plot(fn, zalvo, out, W=1500, lw=3):
    pts=paths(fn,zalvo)
    if not pts: print('nada em Z=%.2f'%zalvo); return
    P=np.array(pts); mn=P.min(0)-1; mx=P.max(0)+1
    sc=W/(mx[0]-mn[0]); H=int((mx[1]-mn[1])*sc)
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    for i in range(0,len(pts)-1,2):
        a,b=pts[i],pts[i+1]
        d.line([((a[0]-mn[0])*sc,H-(a[1]-mn[1])*sc),((b[0]-mn[0])*sc,H-(b[1]-mn[1])*sc)],
               fill=(30,80,170),width=lw)
    im.save(out); print(out, im.size, 'segmentos', len(pts)//2)
if __name__=='__main__':
    plot(sys.argv[1], float(sys.argv[2]), sys.argv[3])
```

```bash
python3 camada.py saida/tudo.gcode 0.20 primeira_camada.png
```

Abra o PNG e confira que **todas as peças estão lá e separadas**, e que os detalhes
finos (números, janelas, ícones) aparecem no percurso.

---

## 8. As armadilhas — todas já custaram retrabalho

**Não meça sobreposição pelo `; printing object` do gcode.** Com `--merge` esse rótulo
não particiona os deslocamentos entre peças, e as caixas por peça saem **maiores que as
peças**, acusando toque que não existe. Quem decide é o desenho da camada (seção 6) ou
a checagem de colisão do `preparar.py`, feita antes de fatiar.

**Peça com pino vai invertida.** Na posição de projeto ela apoia na ponta do pino:
0,3 mm² de contato. Invertida, apoia pelo topo: ~150 mm². O `preparar.py` reporta a
altura e se está fechada, mas a decisão de `flip` é sua.

**Peça em forma de disco com saia apoia em quase nada.** A válvula deste projeto toca a
mesa em **11 mm² de 1.161**. Não adianta inverter (o relevo dos números vira o ponto
mais baixo e ela passaria a apoiar em 23 ilhotas de 0,25 mm). A saída é **suporte +
aba larga**, que o perfil já faz. Se ainda assim descolar, fatie com raft:
`--brim-width 0 --raft-layers 3 --raft-contact-distance 0.15 --raft-expansion 3`.

**`brim_separation` em 0,1 é aba que não segura.** Ela acompanha a peça sem puxar. No
perfil está **0**. Se alguém "consertar" isso, a adesão volta a falhar.

**Booleano com cortadores concatenados deixa material.** Se você for gerar geometria:
cortadores que se cruzam, concatenados numa malha só, ficam auto-intersectantes e o
booleano preserva justamente a região dupla. Una os cortadores (`boolean('union', ...)`)
antes de subtrair.

**Faces degeneradas depois de booleano.** O STL reabre sem ser sólido. Recarregue,
`merge_vertices(digits_vertex=8)`, `update_faces(nondegenerate_faces())`,
`remove_unreferenced_vertices()`, `repair.fix_normals()`, e grave de novo.

---

## 9. PETG — o que muda em relação a PLA

Se alguém pedir para "usar o perfil de PLA", **não use**. Três valores, sozinhos,
descolam a peça:

| | PLA | **PETG** | O que acontece se errar |
|---|---|---|---|
| Mesa | 60 °C | **80 °C** | Abaixo de ~70 o PETG encosta e solta. É o maior fator isolado. |
| Bico | 205/210 °C | **240/245 °C** | A 210 o PETG mal escoa: sai pouco material e não solda na chapa nem na camada de baixo. |
| Ventoinha | 100% | **30–45%**, desligada nas 4 primeiras | 100% é o que descola **no meio da impressão**: o PETG contrai e levanta as bordas. |

E mais: multiplicador de extrusão **0,95** (PETG infla mais), retração **1,2 mm a
30 mm/s** (retração rápida entope e faz fio), preenchimento **30 mm/s**.

Avisos para quem vai imprimir, que não são de fatiamento mas derrubam a peça do mesmo
jeito:

- **Não tirar a peça com a mesa quente.** A 80 °C o PETG está colado de verdade; espere
  baixar de 50 °C. Forçar quente arranca o PEI da chapa.
- **Não usar cola** na chapa texturizada. Em PETG cola é **desmoldante**, não adesivo.
- **Rolo aberto puxa umidade.** PETG úmido imprime estalando, com fio e bolha.

---

## 10. Antes de entregar

Antes de dizer que terminou, confirme que você realmente:

1. rodou `preparar.py` e ele não acusou nada;
2. fatiou com `--dont-arrange` (e `--merge`, se for mesa com várias);
3. injetou a miniatura em **cada** arquivo;
4. rodou `inteiros.py` (e conferiu que `M900 K0.051` sobreviveu) e `valida.py`, e **todos** os itens da tabela passaram;
5. desenhou pelo menos uma camada e **olhou** o PNG.

Se algum falhou, diga qual e por quê, em vez de entregar assim mesmo.
