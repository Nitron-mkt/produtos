# Chrono · datador — 3 moldes sobre a válvula que a Nitron já injeta

Gerado de `Mont_pote_com_valvula__prova_valvula1.STL`. **A tampa não foi tocada.**
A parte de baixo da válvula é a original, bit a bit: tudo abaixo de Y 37,23 saiu do
seu arquivo, e a prova disso é a interferência contra a tampa (abaixo).

| Arquivo | Peça | Gira? | Massa PP |
|---|---|---|---|
| `Chrono_M01_Valvula_Dias.stl` | válvula + 31 dias em relevo | **não** — é a válvula | 2,25 g |
| `Chrono_M02_Aro_Meses.stl` | aro dos 12 meses | **sim** | 0,30 g |
| `Chrono_M03_Travinha_Seta.stl` | travinha com a seta | **sim, solta no poste** | 0,06 g |
| `Chrono_M04_Conjunto.stl` | os três montados, só para ver | — | 2,61 g |

Válvula original: 2,04 g. O datador inteiro custa **+0,57 g de PP** por tampa.

## Como se lê — e por que a seta gira

Duas peças giram porque **um único giro só marca um número**. Com o dia fixo na
válvula e só o aro dos meses girando, dia e mês ficariam amarrados: escolher o mês
escolheria o dia. Então:

- **dia** → a seta da travinha gira e aponta um dos 31 números da válvula;
- **mês** → o aro gira e o mês para embaixo do **índice fixo ▼ às 12 h**, que é
  moldado na própria válvula.

Dois giros independentes, três moldes, o dia fixo na válvula como você pediu.
Dia e mês ficam **em pé quando lidos às 12 h** — a mesma convenção para os dois.

## O acionamento — a concha das 12 h

Medindo a sua válvula, ela tem **uma concha de 1,02 mm de fundo às 12 h**
(setor ~55°–125°, r 8 a 18) e tinha **um ressalto de aperto às 6 h** (r 7,5–17,
subindo até Y 38,24). São as duas pontas do gangorra: *"aperta em uma das pontas,
ela fecha, e se você aperta na outra ponta ela abre."*

O ressalto das 6 h ficava acima de Y 37,23 e saiu junto com o topo antigo. No lugar
dele entrou a **mesa dos dias** — um anel plano de 0,18 mm, de r 14,20 a 18,75, que
também faz ponte sobre a concha para que os 31 números nasçam todos na mesma altura.

O aperto passa a ser **na banda dos dias, às 6 h e às 12 h**. Isso não é perda:

| | ressalto original (6 h) | mesa dos dias |
|---|---|---|
| raio onde o dedo cai | ~12,2 mm | **16,6 mm** |
| braço de alavanca sobre o eixo das orelhas | 12,2 mm | **16,6 mm — 36% maior** |

O eixo do gangorra passa pelas orelhas (3 h/9 h), então o braço é a distância até
elas: a mesa aperta **com mais vantagem** que o ressalto que substituiu. A concha
funda (r < 14,20) continua aberta como poço de polegar; o aro dos meses passa por
cima dela sem encostar (1,04 mm de ar).

## Conferência numérica

```
ENTRE AS TRES PECAS
  valvula x aro                           0.0000 mm3  ok
  valvula x travinha                      0.0000 mm3  ok
  aro x travinha                          0.0000 mm3  ok

CONTRA A TAMPA — a tampa NAO foi tocada
  aro x tampa                             0.0000 mm3  ok
  travinha x tampa                        0.0000 mm3  ok
  valvula nova x tampa                    1.6357 mm3
  valvula ORIGINAL x tampa                1.6357 mm3  <- a que voce ja injeta
  diferenca +0.0000 mm3  nenhum aperto novo

VARREDURA (24 posicoes de giro)
  travinha, pior caso                     0.0000 mm3  ok
  aro nas 12 posicoes de encaixe          0.0000 mm3  ok
  aro entre encaixes                      0.0580 mm3  <- o detente, e de projeto

ALTURAS (aro de empilhamento da tampa em Y 39,72)
  M01 valvula+dias     Y 32.57 .. 38.90   folga 0.82 mm
  M02 aro dos meses    Y 37.25 .. 38.35   folga 1.37 mm
  M03 travinha/seta    Y 37.95 .. 39.05   folga 0.67 mm
```

**+0,0000 mm³** é o número que importa: a válvula nova aperta a tampa exatamente
como a que já está em linha. Nada mudou embaixo.

## Cotas

| | |
|---|---|
| face de topo da válvula (datum) | Y 37,23 |
| mesa dos dias | r 14,20–18,75 · Y 37,23→37,41 |
| 31 dias | r 16,65 · caixa alta 2,00 · relevo 0,30 · passo **3,37 mm** de arco |
| grafia dos dias | **1 a 9 sem zero**, 10 a 31 com dois dígitos |
| índice fixo do mês | 12 h · r 14,25–15,30 · relevo 0,30 |
| poste central | r 5,40 · topo Y 38,90 · canaleta r 4,70 de 38,15 a 38,55 |
| aro dos meses | r 5,60–12,90 · espessura 0,80 · Y 37,25→38,05 |
| 12 meses | r 10,80 · caixa alta 1,90 condensada 0,78 · relevo 0,30 |
| folga entre dois meses | **1,39 mm** (palavra 4,26 em passo 5,65) |
| entalhes de unha | 12 · r 1,00 centrados em r 13,30 |
| detente | 2 molas r 0,42 na válvula × 12 covinhas r 0,55 no aro, em r 7,50 |
| curso do detente | **0,16 mm** de interferência entre encaixes |
| travinha | colar r 5,55–**6,90** · braço **2,10** de largura, 0,50 de espessura |
| ponta da seta | afina de 2,10 para **1,40** e fecha em ponta em r **19,90** |
| espigão do dorso | 0,80 × 0,60, de r 14,45 a 19,50 · topo Y 39,05 |

## O que ainda não está resolvido

- **Traço de 0,36–0,38 mm.** Em molde, é relevo fino mas viável em PP; o contraste
  tem de vir de **acabamento de molde** (caractere polido sobre campo VDI 27-30),
  não de tampografia. Em impressão 3D com bico de 0,40 é **1 extrusão** — o número
  forma mas sai esfarrapado. Para provar a leitura, bico de 0,25 ou escala ≥ 2×.
- **Fecho do colar da travinha.** A barbela interna de 0,45 mm tem de estalar na
  canaleta do poste e ainda girar solta. Isso é ensaio de peça, não de CAD.
- **Rigidez do braço da seta.** O braço tem 0,50 mm de espessura num vão de 5,5 mm,
  e só 0,24 mm de folga sobre os números. Por isso o **espigão de 0,60 mm no dorso**,
  que triplica a inércia sem engrossar o desenho visto de cima. Se ainda raspar, a
  correção é subir o braço externo (37,95 → 38,05), não engrossá-lo.
- **Onde o detente trava.** 0,16 mm de interferência num aro de 0,80 mm de PP é
  firme; se ficar duro demais, a correção é a mola (0,42 → 0,35), não a covinha.

## Como regerar

```bash
cd ../medicao_v2
python3 build.py     # gera os 4 STL em ../stl_v2
python3 check.py     # interferencia entre as pecas, contra a tampa, e varredura de giro
python3 mapa.py      # mapas de altura para conferir que os numeros formaram
```
