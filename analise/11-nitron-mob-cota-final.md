# Nitron Mob — a cota externa real do módulo

Rev. 1 · 04/09/2026 · fecha o pedido "calcule a medida final do módulo, considerando
que as ripas entram na cruzeta, no L e na trizeta".

A pergunta tem resposta fechada e ela **não é a soma das ripas**. A ripa entra
40,60 mm dentro de cada nó, e o nó sobra para fora. Em cada eixo a sobra é
diferente, porque a peça tem extensão diferente em cada direção.

---

## 1. As grandezas — medidas nas malhas, não estimadas

Todas saem das malhas STL das cinco peças de linha (malhas fechadas, zero arestas
não-manifold). Estão em `dados/22-mob-cota-modelo.csv`.

| grandeza | mm | de onde vem |
|---|---|---|
| encaixe (a ripa entra) | **40,60** | face +Y da peça L, mediana de 1.666 raios |
| nó no eixo do **comprimento** (trizeta) | **61,61** | malha da trizeta |
| **cruzeta** no eixo do comprimento | **101,30** | malha da cruzeta |
| nó no eixo da **profundidade** | **83,23** | malha da trizeta |
| nó no eixo **vertical** | **73,08** | malha da trizeta |
| pé exposto (BPE-01-AC 60 − 40,60) | **19,40** | soma uma vez na altura |

Disso saem as três sobras:

```
sobra por extremidade = extensão do nó − 40,60

eixo COMPRIMENTO  : 61,61 − 40,60 = 21,01 mm  →  externo = ripa + 42,02
eixo PROFUNDIDADE : 83,23 − 40,60 = 42,63 mm  →  externo = ripa + 85,26
eixo VERTICAL     : 73,08 − 40,60 = 32,48 mm

os dois nós comem 81,20 mm de cada ripa
vão livre entre as faces internas dos nós = ripa − 81,20
```

## 2. As três fórmulas

```
COMPRIMENTO   = 2×61,61 + (N−1)×101,30 + N×(ripa_comprimento − 81,20)
PROFUNDIDADE  = ripa_largura + 2×42,63
ALTURA        = n×73,08 + (n−1)×(ripa_vertical − 81,20) + 19,40

N = vãos na corrida   n = prateleiras
```

A cruzeta é o que faz a corrida: ela **consome os mesmos 81,20 mm** que uma
trizeta, mas ocupa 101,30 mm no eixo, então cada vão a mais soma
`ripa + 20,10` mm — não `ripa`.

## 3. A conferência que fecha o modelo

Esta é a parte que importa: **a sua própria lista de painéis valida a conta do
eixo do comprimento**, sem que eu tenha ajustado nada para isso.

| ripa de comprimento | mm | externo = ripa + 42,02 | painel que você fixou | diferença |
|---|---|---|---|---|
| PSC-01 | 315 | 357,02 | **360** | +2,98 |
| PSC-02 | 415 | 457,02 | **450** | −7,02 |
| PSC-03 | 595 | 637,02 | **634** | −3,02 |
| PSC-04 | 717 | 759,02 | **754** | −5,02 |

Quatro ripas, quatro painéis, todos dentro de ±7 mm da cota externa calculada.
O painel foi cortado na medida externa do vão — ele **deita sobre os nós** e cobre
o vão de ponta a ponta. Se o painel fosse cortado no vão livre, daria 233,8 / 333,8 /
513,8 / 635,8 mm, e não é isso que está na sua lista.

No eixo da profundidade a lógica é outra e também fecha: o nó sobra 42,63 mm por
lado, a tábua **não** alcança essa cota, ela apoia nas duas ripas de largura e
sobressai um pouco:

| tábua | ripa de largura | mm | profundidade externa | sobressai por lado |
|---|---|---|---|---|
| 200 | BLA-01-AC | 200 | **285,26** | 0,00 |
| 300 | BLA-03-AC | 287 | **372,26** | +6,50 |
| 460 | PSC-02 | 415 | **500,26** | +22,50 |

As 12 combinações estão em `dados/23-mob-cota-12-paineis.csv`.

## 4. Comprimento externo por corrida

`dados/24-mob-cota-corridas.csv`

| ripa | passo/vão | 1 vão | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| PSC-01 315 | 335,1 | 357 | 692 | 1.027 | 1.362 | 1.697 | 2.033 |
| PSC-02 415 | 435,1 | 457 | 892 | 1.327 | 1.762 | 2.197 | 2.633 |
| PSC-03 595 | 615,1 | 637 | 1.252 | 1.867 | 2.482 | 3.097 | 3.713 |
| PSC-04 717 | 737,1 | 759 | 1.496 | 2.233 | 2.970 | 3.707 | 4.445 |

## 5. Altura — aqui falta uma medida física

`dados/25-mob-cota-alturas.csv`

O encaixe vertical da trizeta **abre para baixo** e a face de topo é fechada
(chapa medida em z relativo 70,0–72,9 mm na malha). É por isso que a peça sai em
**par espelhado ESQ/DIR**. Isso deixa duas leituras do passo, e a diferença não é
pequena:

| ripa vertical | modelo | passo | 4 prat. | 6 prat. | 8 prat. |
|---|---|---|---|---|---|
| BAL-02-AC 270 | **A** — um nó por nível | 261,88 | 878 | 1.402 | 1.926 |
| BAL-02-AC 270 | **B** — par espelhado | 334,96 | 1.170 | 1.840 | 2.510 |
| PSA-05 513 | **A** | 504,88 | 1.607 | 2.617 | 3.627 |
| PSA-05 513 | **B** | 577,96 | 1.899 | 3.055 | 4.211 |

**A lista de painéis não resolve isso** — ela só restringe os eixos horizontais.
O front-end usa o **modelo A** por padrão e traz um seletor interno para trocar.

### As duas medidas para tirar no showroom

Quando você for montar, essas duas fitas fecham o modelo inteiro:

1. **Passo vertical.** Monte duas prateleiras com a ripa **BAL-02-AC (270 mm)** e
   meça a distância de uma face de apoio à outra.
   **261,9 mm → modelo A. 335,0 mm → modelo B.** Não tem meio.
2. **Profundidade externa de um vão.** Um nó com a ripa de largura
   **BLA-01-AC (200 mm)** montada, medindo face externa a face externa.
   Deve dar **285,3 mm**. Se der outro número, a extensão de 83,23 mm do nó
   nesse eixo precisa ser remedida.

Se puder, uma terceira confirma o resto de graça: **um vão com PSC-01 (315 mm)
deve fechar 357,0 mm externos.**

---

## 6. O que mudou no portal do lojista

`frontend/monte-seu-pdv.html` foi reescrito na estrutura nova.

- **Nada fora da lista.** 4 ripas de comprimento, 3 de largura, 2 verticais,
  12 painéis. Não há mais campo livre de dimensão.
- **A cota aparece com a conta à vista.** O painel lateral mostra as três
  equações preenchidas com os números escolhidos, não só o resultado.
- **Ficha de encaixe do painel.** Diferença do painel contra a cota externa do
  vão, quanto a tábua sobressai por lado, e o vão livre entre nós.
- **Duas rotas comerciais, só.** Venda direta (2× o custo de material, com nota)
  e bonificação por volume (20× o custo, arredondado para a faixa). Saíram a
  coparticipação e o comodato.
- **As quatro famílias saem diferentes de fábrica** — cada uma nasce numa
  combinação distinta de painel, corrida e altura:

| família | painel | corrida | altura | medida final |
|---|---|---|---|---|
| Checkout | 300 × 450 | 2 vãos PSC-02 | 5 prat. BAL-02-AC | **892 × 372 × 1.140** |
| Ilha | 460 × 634 | 2 vãos PSC-03 | 4 prat. BAL-02-AC | **1.252 × 500 × 878** |
| Ponta de gôndola | 300 × 634 | 2 vãos PSC-03 | 7 prat. BAL-02-AC | **1.252 × 372 × 1.664** |
| Paredão | 200 × 754 | 4 vãos PSC-04 | 8 prat. BAL-02-AC | **2.970 × 285 × 1.926** |

- O seletor de prateleiras só oferece o que fica **abaixo de 2.450 mm** de altura
  para a ripa vertical escolhida — com a PSA-05 sobram 4 opções, não 7.

## 7. O que continua aberto

1. **O modelo do nó vertical** — as duas medidas da seção 5.
2. **A chapa crua.** A `PAN-01` tem 200 mm de largura. As tábuas de **300 e 460 mm
   precisam de emenda ou de chapa mais larga** — o portal já avisa isso na ficha
   de encaixe, mas a decisão de fornecimento não está tomada.
3. **A carga de 20 kg por prateleira é provisória.** A chapa 1 da trizeta está em
   z relativo 40,0 mm, exatamente onde o encaixe de 40,60 mm termina: a ripa
   apoia numa chapa de 2,9 mm, dando 8,5–18,4 MPa. Falta ensaio de carga
   permanente.
4. **A ferramentaria da cruzeta** — primeira de cinco cadastrada em 17/07/2026,
   quatro já injetadas; ainda não sabemos se as 2 cavidades são o par esq/dir.
5. **A tampinha** — o STL nunca chegou; ela entra na conta de custo pelo peso
   cadastrado (1,10 g), não por malha medida.
6. **Preço médio de caixa real** para calibrar a escada de bonificação. O portal
   usa R$ 250 como padrão editável.
