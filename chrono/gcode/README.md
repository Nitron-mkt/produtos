# Chrono · datador — arquivos .gcode para **Anycubic Kobra 3**

Fatiados em 09/09/2026 com **PrusaSlicer 2.7.2**, a partir dos STL de `../stl/`.

## O erro 10133 e o que estava faltando

A primeira versão destes arquivos foi fatiada num perfil **genérico Marlin, mesa 220×220**,
e a Kobra 3 recusou com **CODE: 10133 — "The file is missing necessary commands"**.

A Kobra 3 **valida o arquivo antes de imprimir** e procura o start-gcode dela. O perfil
genérico abria com `G28` + `M190` + `M109` (o jeito Marlin de referenciar e aquecer). A
Kobra 3 não quer isso: ela quer **`G9111`**, a macro própria da Anycubic que faz home,
nivelamento, aquecimento de mesa e bico e a purga, tudo num comando:

```gcode
G9111 bedTemp=60 extruderTemp=210
M117
M900 K0.051              ; pressure advance
```

Sem `G9111`, o arquivo é recusado. Foi só isso — a geometria estava certa.

## O que mudou nesta versão

| | Antes (genérico) | Agora (Kobra 3) |
|---|---|---|
| Start-gcode | `G28` / `M190` / `M109` | **`G9111`** + `M117` + `M900 K0.051` |
| Firmware | `marlin` | **`klipper`** |
| Mesa | 220 × 220, centro 110/110 | **255 × 255 × 260, centro 127,5/127,5** |
| Fim | park em X5 Y200 | `M400`, retração, park em **X250 Y220** |
| Primeira camada | 0,16 mm | **0,20 mm** |
| Z-hop | 0,2 mm | **0,4 mm** |
| Miniatura | nenhuma | **230 × 110 PNG** (a peça aparece no painel) |

Os valores vieram do **perfil oficial da Kobra 3 no OrcaSlicer**, que está guardado em
`fatiamento/orca_anycubic_kobra3_0.4.json` para conferência — não foram adivinhados.

## Os quatro arquivos

| Arquivo | O que é | Tempo | PLA |
|---|---|---|---|
| `Chrono_01_Pino_Travinha.gcode` | o pino sozinho, **invertido** (face de topo na mesa) | 49 min | 3,57 g |
| `Chrono_02_Anel_Dia.gcode` | anel de dia, plano, números para cima | 18 min | 0,94 g |
| `Chrono_03_Anel_Mes.gcode` | anel de mês, plano, números para cima | 11 min | 0,49 g |
| `Chrono_04_Chapa_3_Pecas.gcode` | **as três de uma vez**, na mesma mesa | 1 h 19 min | 5,00 g |

O quarto substitui o `Chrono_04_Datador_Montado.stl`: o conjunto montado não se imprime
montado — as folgas são de 0,10 a 0,30 mm e as peças sairiam fundidas numa só.

## Verificação feita em cada arquivo

- **`G9111` presente** com mesa 60 °C e bico 210 °C.
- Percurso **dentro da mesa 255 × 255**, peças centradas em X127,5 Y127,5.
- Z começa em 0,20 e nunca fica negativo. 9 camadas nos anéis (0,95 mm), 55 no pino e na chapa.
- **Miniatura decodificada e conferida**: 230 × 110, PNG, tamanho base64 batendo com o
  cabeçalho declarado.
- Chapa com os **três** objetos (o CLI precisa de `--merge --dont-arrange`; sem isso sai
  uma peça só).
- **Lista completa de comandos usados**, para não sobrar nada que o Klipper não entenda:
  `G1 G21 G90 G9111 G92 M82 M84 M104 M106 M107 M117 M140 M400 M900`. Sem `G28`, sem `M109`,
  sem `M190`, sem `M486`, sem `M73`.

## Se o painel ainda reclamar

O caminho que a Anycubic garante é o dela: abra os **STL de `../stl/`** no
**Anycubic Slicer Next** e fatie lá. A checagem de arquivo do firmware não é documentada —
o que está aqui foi reconstruído a partir do perfil oficial do OrcaSlicer, que é o que a
comunidade usa nessa máquina, mas quem tem a última palavra é o firmware.

## Orientação — por que o pino vai invertido

A casca do pino é uma cuia rasa. Na posição de projeto, o interior fica com um teto
horizontal de Ø33 no ar — precisaria de suporte trancado dentro da peça. Invertido, a face
de topo plana (Ø38) apoia na mesa: adesão ótima, o interior abre para cima e o único balanço
é a parede a ~42° mais as duas orelhas, que o suporte automático pega. Os anéis vão planos,
números para cima. Suporte **automático com limiar de 50°**: os anéis não recebem nada.

## O que a impressão 1:1 consegue provar — e o que não

**Consegue:** diâmetro, proporção, altura, e principalmente **se o datador assenta no poço
da tampa real**. É para isso que vale imprimir.

**Não consegue, e a conta é essa:**

| Detalhe | Cota | Contra extrusão de 0,40 mm |
|---|---|---|
| Traço mais fino dos números | 0,52 mm (dia) · 0,56 mm (mês) | 1,3 extrusão — o número **forma, mas sai esfarrapado** |
| Folga radial anel ↔ colar | 0,10 mm | funde. **Os anéis não vão girar** |
| Saliência de encaixe | 0,40 mm | 1 extrusão — forma torto |
| Mola de detente | 0,15 mm de altura | 1,5 camada — no limite |

**Para girar e ler**, duas saídas: **bico de 0,25 mm** — a Kobra 3 aceita, e o perfil oficial
do OrcaSlicer tem versão 0.2 e 0.4 — ou **imprimir em escala ≥ 2×** (a 3× tudo folga: traço
de 1,56 mm, folga de 0,30 mm, mola de 0,45 mm). A peça em 3× não encaixa em nada, mas é a que
demonstra o mecanismo. São dois testes diferentes e os dois valem.

## Como regerar

```bash
cd fatiamento
python3 orienta.py                       # orienta, inverte o pino, apoia em z=0, centra em 127,5
prusa-slicer --export-gcode --dont-arrange --load chrono_kobra3.ini -o pino.gcode pino.stl
prusa-slicer --export-gcode --merge --dont-arrange --load chrono_kobra3.ini \
             -o chapa.gcode chapa_pino.stl chapa_dia.stl chapa_mes.stl
python3 miniatura.py pino.gcode ../../pdf/assets/fig_pino.png   # injeta a miniatura 230x110
python3 valida_k3.py                     # G9111, mesa, Z, camadas, miniatura, comandos
```

Para escala, `--scale 3`. Para bico de 0,25, mude `nozzle_diameter` e as larguras de
extrusão em `chrono_kobra3.ini`. `camada.py arquivo.gcode <Z> saida.png` desenha o percurso
de uma camada — foi assim que se conferiu que os 31 números aparecem no topo do anel.
