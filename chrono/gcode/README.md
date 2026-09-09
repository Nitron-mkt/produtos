# Chrono · datador — arquivos .gcode

Fatiados em 09/09/2026 com **PrusaSlicer 2.7.2**, a partir dos STL de `../stl/`.

> ⚠️ **Confira antes de imprimir.** G-code não é portátil: ele carrega mesa, firmware,
> temperatura e o start-gcode da máquina. Estes quatro arquivos foram gerados num
> **perfil genérico Marlin, mesa 220×220, bico 0,40, PLA** — serve numa Ender 3 e
> compatíveis. Se a sua impressora for outra, ou se ela depende de malha de mesa
> salva (`M420 S1`) ou de sonda (`G29`) depois do `G28`, **o start-gcode aqui não tem
> isso** e precisa ser regerado. Regerar leva um comando: veja o fim deste arquivo.

## Os quatro arquivos

| Arquivo | O que é | Tempo | PLA |
|---|---|---|---|
| `Chrono_01_Pino_Travinha.gcode` | o pino sozinho, **invertido** (face de topo na mesa) | 49 min | 3,53 g |
| `Chrono_02_Anel_Dia.gcode` | anel de dia, plano, números para cima | 18 min | 0,90 g |
| `Chrono_03_Anel_Mes.gcode` | anel de mês, plano, números para cima | 11 min | 0,46 g |
| `Chrono_04_Chapa_3_Pecas.gcode` | **as três de uma vez**, na mesma mesa | 1 h 18 min | 4,89 g |

O quarto arquivo substitui o `Chrono_04_Datador_Montado.stl`: o conjunto montado não se
imprime montado — as folgas são de 0,10 a 0,30 mm, fora do alcance de qualquer FDM, e as
peças sairiam fundidas umas nas outras. A chapa com as três é o equivalente útil.

## Verificação feita em cada arquivo

- Percurso todo **dentro da mesa 220×220**, peças centradas em X110 Y110 (cabe também
  em MK3S 250×210 e em qualquer mesa maior).
- Z começa em 0,16 (primeira camada) e nunca fica negativo.
- Camadas: 9 nos anéis (0,95 mm de espessura), 56 no pino e na chapa (5,63 mm).
- Bico 210 °C na primeira camada / 205 nas demais · mesa 60 °C.
- Chapa confirmada com os **três** objetos (o primeiro fatiamento saiu com um só — o CLI
  precisa de `--merge --dont-arrange` para respeitar a posição de cada peça).
- Rótulo de objeto emitido como comentário (`; printing object …`), não como `M486`, que
  firmware antigo não entende.

## Orientação — por que o pino vai invertido

A casca do pino é uma cuia rasa. Na posição de projeto, o interior fica com um teto
horizontal de Ø33 no ar — precisaria de suporte trancado dentro da peça. Invertido, a face
de topo plana (Ø38) apoia na mesa: adesão ótima, o interior abre para cima e o único
balanço é a parede a ~42° mais as duas orelhas, que o suporte automático pega.

Os anéis vão planos, com os números para cima. Suporte fica **automático com limiar de
50°** em todos os arquivos: os anéis não recebem nada, o pino recebe só embaixo das orelhas.

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

**Para girar e ler**, duas saídas: **bico de 0,25 mm** (aí o traço vira 2,1 extrusões) ou
**imprimir em escala ≥ 2×** (a 3× tudo folga: traço de 1,56 mm, folga de 0,30 mm, mola de
0,45 mm). A peça em 3× não encaixa em nada, mas é a que demonstra o mecanismo.
As duas coisas são testes diferentes e ambas valem.

## Como regerar

```bash
cd fatiamento
python3 orienta.py                       # orienta, inverte o pino, apoia em z=0, centra em 110,110
prusa-slicer --export-gcode --dont-arrange --load chrono_generico.ini -o pino.gcode pino.stl
prusa-slicer --export-gcode --merge --dont-arrange --load chrono_generico.ini \
             -o chapa.gcode chapa_pino.stl chapa_dia.stl chapa_mes.stl
python3 valida.py                        # mesa, Z, camadas, temperatura, filamento, objetos
```

Para outra impressora, mexa em `chrono_generico.ini`: `bed_shape`, `max_print_height`,
`nozzle_diameter`, `gcode_flavor` e o `start_gcode`. Para escala, `--scale 3`.
`camada.py arquivo.gcode <Z> saida.png` desenha o percurso de uma camada — foi assim que
se conferiu que os 31 números realmente aparecem no topo do anel.
