# Chrono v2 · arquivos .gcode para **Anycubic Kobra 3**

Fatiados com **PrusaSlicer 2.7.2** a partir de `../stl_v2/`, com o mesmo perfil que
resolveu o erro **10133** na primeira rodada (`G9111` no lugar de `G28`/`M109`/`M190`,
firmware `klipper`, mesa 255×255, miniatura 230×110).

## Os cinco arquivos

| Arquivo | O que é | Tempo | PLA |
|---|---|---|---|
| `Chrono_v2_01_Valvula_Dias.gcode` | M01 sozinha, números para cima, com suporte | 54 min | 3,95 g |
| `Chrono_v2_02_Aro_Meses.gcode` | M02, plano | 10 min | 0,49 g |
| `Chrono_v2_03a_Ponteira_MD.gcode` | M03a, **invertida** (pino para cima) | 5 min | 0,23 g |
| `Chrono_v2_03b_Ponteira_Janela.gcode` | M03b, **invertida** | 6 min | 0,25 g |
| **`Chrono_v2_04_Todas_As_Pecas_1x.gcode`** | **as quatro peças numa mesa só, 1:1** | **1 h 15** | **4,95 g** |
| `Chrono_v2_05_Mecanismo_3x.gcode` | disco de prova + aro + ponteira do rasgo, **3×** | 7 h 48 | 35,26 g |

## O arquivo único

`Chrono_v2_04_Todas_As_Pecas_1x.gcode` traz **as quatro peças já fatiadas na mesma
mesa**: válvula, aro dos meses e as duas ponteiras. É um arquivo só, manda para a
impressora e sai o datador inteiro com as duas opções de ponteira para comparar na mão.

Conferido no percurso da primeira camada (`../stl_v2/chapa_primeira_camada.png`): as
quatro peças aparecem, separadas, dentro da mesa, com o ícone da Nitron já visível nos
dois cubos e o rasgo retangular visível na `M03b` — as ponteiras vão invertidas, então
a primeira camada é justamente a face de topo delas.

> Cuidado ao medir sobreposição pelo `; printing object` do gcode: com `--merge` o
> rótulo não particiona os deslocamentos, e as caixas saem maiores que as peças. Quem
> decide é o desenho da camada, ou a checagem de colisão em `preparar.py` antes de fatiar.

## Por que dois testes e não um

**1:1 (arquivos 01 a 04)** prova **assentamento** — se o datador cai no poço da tampa
real, se a altura passa sob o aro de empilhamento, se o colar prende no poste.
Não prova leitura: o traço dos dias tem 0,32 mm e o bico tem 0,40. O fatiador resolve
isso como *parede fina* — cada número sai como **um único traço de extrusão**, então
ele aparece, mas com 0,40 de largura em vez de 0,32, mais gordo que o projeto e com
os olhos do 6, 8, 9 e 0 apertados.

**3× (arquivo 05)** prova **mecanismo e leitura** — a 3× o traço vira 0,96 mm (2,4
extrusões), a folga entre peças vira 0,30 e o detente 0,48. Aí gira e lê de verdade.
Não assenta em tampa nenhuma, e não deve mesmo.

O 3× usa o `Chrono_M01_Disco_Prova.stl`: só o mostrador de M01 (o que está acima da
face, Y 37,23) sobre uma base chapada de 1,20 mm. A válvula inteira a 3× seria um
casco de 19 mm de altura com 922 mm² de teto em balanço — horas de suporte para
provar exatamente nada, porque o que interessa no teste de escala é o mostrador.

## M03 vai invertida

Com o pino passante, M03 na posição de projeto apoiaria **na ponta do pino**: 0,3 mm²
de contato com a mesa e tudo o mais em balanço. Invertida (pino para cima) ela apoia
pelo topo do cubo e do braço — **150,6 mm²**. Para isso o espigão do dorso foi
nivelado com o cubo, os dois em Y 38,95: o topo da travinha virou um plano só.

Invertida, o ombro da farpa vira um ressalto de 0,50 mm virado para baixo — um balanço
de uma extrusão por camada. Forma com leve queda, e é o lado que não se vê.

## Orientação — e o problema de M01

M01 impressa com os números para cima encosta na mesa em **23,7 mm² de 1.161** (2%):
o corpo é um disco com saia, e a saia toca só pelas nervuras. Além disso **922 mm²
da peça nasce em balanço a 2,7 mm** de altura.

Inverter não resolve: de cabeça para baixo o relevo dos dias vira o ponto mais baixo,
e a peça passaria a apoiar em 23 ilhotas de 0,25 mm com a face inteira fazendo ponte
por cima na segunda camada.

Então é **números para cima, com suporte e aba (brim) de 3 mm**, que é o que o perfil
já faz (`support_material_auto`, limiar 50°, `support_material_buildplate_only`).
As marcas de suporte ficam na face de baixo — que numa cópia em FDM não é funcional
de qualquer jeito.

## Conferência feita em cada arquivo

- **`G9111 bedTemp=60 extruderTemp=210`** presente.
- Percurso dentro da mesa 255 × 255.
- Z começa em 0,20 e nunca fica negativo. (O Z máximo dá 0,40 acima da peça: é o
  *z-hop* de retração, não material.)
- **Miniatura 230×110 PNG** decodificada e conferida. O CLI do PrusaSlicer não emite
  miniatura sem interface gráfica — ela é injetada por `fatiamento/miniatura.py`.
- Camada dos números desenhada e conferida: os **31 algarismos aparecem**, cada um
  como um traço fechado, mais o triângulo do índice às 12 h.
- Só comandos que o Klipper da Kobra 3 entende:
  `G1 G21 G90 G9111 G92 M82 M84 M104 M106 M107 M117 M140 M400 M900`.
  Sem `G28`, `M109`, `M190`, `M486`, `M73`.

## O que o 1:1 **não** vai provar do pino

O furo é Ø5,00 e o pino Ø4,80. Em FDM o furo sai sub-dimensionado e o pino
sobre-dimensionado — tipicamente 0,1 a 0,3 mm cada. A folga de projeto é 0,10 mm no
raio. **Se o pino não entrar na peça impressa, isso é tolerância de impressora, não
de projeto.** Quem prova o encaixe é o 3×, onde a folga vira 0,30 e a farpa 1,20.

## Se quiser o traço certo no 1:1

Bico de **0,25 mm**. A Kobra 3 aceita, e o perfil oficial do OrcaSlicer tem versão
0.2 e 0.4 de fábrica. Com 0,25 o traço de 0,32 vira 1,3 extrusão e o número forma
com a largura de projeto. É trocar `nozzle_diameter` e as larguras de extrusão em
`fatiamento/chrono_kobra3.ini`.

## Como regerar

```bash
cd fatiamento
python3 disco_prova.py                  # gera o disco de prova a partir de M01
python3 preparar.py pecas_1x.json       # orienta, apoia em z=0, centra na mesa
python3 prep3x.py                       # chapa 3x, escalada e posicionada a mao
QT_QPA_PLATFORM=offscreen prusa-slicer --export-gcode --dont-arrange \
    --load chrono_kobra3.ini -o ../Chrono_v2_01_Valvula_Dias.gcode prep1x/m01_valvula.stl
python3 miniatura.py ../Chrono_v2_01_Valvula_Dias.gcode prep1x/m01_valvula.stl
python3 valida_k3.py                    # G9111, mesa, Z, camadas, miniatura, comandos
python3 camada.py ../arquivo.gcode 5.0 saida.png   # desenha o percurso de uma camada
```

Para a chapa, `--merge --dont-arrange` com os três STL. **Sem `--merge` sai uma peça só** —
o CLI sobrescreve a saída a cada arquivo.
