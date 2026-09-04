# Nitron Mob — a cota externa real e a grade de painéis

Rev. 2 · 04/09/2026 · a Rev. 1 fechou as três contas de cota. Esta corta a grade
de 12 para 7 painéis, entra com a **peça L** como nó de topo e libera altura
mista dentro do mesmo módulo.

---

## 1. As grandezas — medidas nas malhas, não estimadas

`dados/22-mob-cota-modelo.csv`

| grandeza | mm | de onde vem |
|---|---|---|
| encaixe (a ripa entra) | **40,60** | face +Y da peça L, mediana de 1.666 raios |
| trizeta no eixo do **comprimento** | **61,61** | malha da trizeta |
| **cruzeta** no eixo do comprimento | **101,30** | malha da cruzeta |
| **peça L** no eixo em que trabalha | **83,23** | malha da peça L, bbox 21,92 × 83,23 × 73,08 |
| nó no eixo da **profundidade** | **83,23** | malha da trizeta |
| nó no eixo **vertical** | **73,08** | malha da trizeta **e da peça L** |
| pé exposto (BPE-01-AC 60 − 40,60) | **19,40** | soma uma vez na altura |

```
sobra por extremidade = extensão do nó − 40,60

eixo COMPRIMENTO  : 61,61 − 40,60 = 21,01 mm  →  externo = ripa + 42,02
eixo PROFUNDIDADE : 83,23 − 40,60 = 42,63 mm  →  externo = ripa + 85,26
os dois nós comem 81,20 mm de cada ripa
```

## 2. As fórmulas

```
COMPRIMENTO   = 2×61,61 + (N−1)×101,30 + N×(ripa_comprimento − 81,20)
PROFUNDIDADE  = ripa_largura + 2×42,63
ALTURA        = 19,40 + n_nós×73,08 + Σᵢ(ripa_i − 81,20)

N = vãos na corrida
uma ripa vertical por baia; n_nós = prateleiras + 1 quando há coroa
```

A altura deixou de ser `n × uma ripa só`: **cada baia tem a sua ripa**, e a soma
é o que fecha a cota. Isso é o que permite prateleira baixa embaixo e vão alto no
topo dentro do mesmo módulo.

## 3. A peça L é um nó de topo — e é por isso que ela dá altura

O achado é numérico: a peça L tem **73,08 mm no eixo vertical, exatamente como a
trizeta**. Ela empilha no poste igual a um nó de prateleira, mas só tem **2 vias
coplanares** — segura uma ripa atravessada e nada mais. É assim que a arara ganha
altura sem ganhar prateleira, e é o que a imagem de referência mostra: o poste
sobe além da última prateleira, o L fecha, e a ripa de cima recebe a cabeceira e
os ganchos.

```
a coroa acrescenta  (ripa − 81,20) + 73,08  =  ripa − 8,12 mm de altura
com a ripa 270 → +261,88 mm      com a ripa 513 → +504,88 mm
```

**A coroa é mais larga que a estrutura**, e a conta diz quanto: o L tem 83,23 mm
nesse eixo contra 61,61 da trizeta, então passa **21,62 mm por lado** —
`comprimento da coroa = comprimento + 43,24`. A cabeceira acompanha essa cota, o
que explica o painel de topo aparecer mais largo que o corpo na referência.

⚠️ Isso pressupõe o L montado **no plano da frente** (via vertical + via ao longo
do comprimento). O bounding box não diz a orientação de uso — é a segunda medida
a tirar no showroom.

## 4. A grade caiu de 12 para 7 painéis — e existe uma regra por trás

`dados/23-mob-paineis-grade.csv`

Os cortes propostos foram: 200×634, 200×754 (tira estreita), 300×360, 460×360 e
460×450 (quadrados). Os cinco cortes **são um único critério**:

```
1,3 ≤ comprimento ÷ largura ≤ 2,6
```

| largura | 360 | 450 | 634 | 754 |
|---|---|---|---|---|
| **200** | 1,80 ✅ | 2,25 ✅ | 3,17 ❌ | 3,77 ❌ |
| **300** | 1,20 ❌ | 1,50 ✅ | 2,11 ✅ | 2,51 ✅ |
| **460** | 0,78 ❌ | 0,98 ❌ | 1,38 ✅ | 1,64 ✅ |

Sete mantidos, cinco cortados, exatamente os cinco propostos. A banda que sobra
é 1,38–2,51, e os vizinhos excluídos estão em 1,20 e 3,17 — folga confortável dos
dois lados, então a regra não é ajuste de curva, é o critério real.

Ler a tabela na diagonal dá a frase que vale para o catálogo:
**quanto mais funda a prateleira, mais longo o vão.** Nenhuma ripa sai da lista —
os 4 comprimentos e as 3 larguras continuam todos em uso. **Só o estoque de
painel cai 42%.**

### Sobre o empenamento: o mecanismo é outro

Corte 200×634 e 200×754 pela razão certa, não pela que parecia.

O painel **não é apoiado só nas pontas** — ele deita sobre as duas ripas de
comprimento (frente e fundo) e sobre as duas de largura. Fica apoiado nos quatro
lados, e flexiona na direção **curta**. Sob carga, portanto, o painel de 200 é o
mais rígido dos três, não o mais fraco. Sag não é o problema.

O que existe de real numa tábua de 15 mm com proporção 3,8:1 é **arqueamento e
torção** ao longo do comprimento — instabilidade dimensional, não flexão de
carga. E as duas ripas de comprimento restringem isso só se o painel estiver
fixado nelas; solto, ele levanta.

## 5. O argumento mais forte para o corte veio do ERP

`dados/26-mob-cobertura-curva.csv`

`TGFPRO.LARGURA`, `ALTURA` e `ESPESSURA` (em **centímetros**) estão preenchidas
em **2.742 dos 3.079 PAs ativos** — 89%. Cruzando com o faturamento de marca
própria dos últimos 12 meses (1.273 SKUs, **R$ 83,8 M**, tabelas 84 e 3 fora),
dá para medir quanto do catálogo cabe em cada prateleira:

| profundidade | externa | produto **de lado** | produto **de frente** |
|---|---|---|---|
| 200 (BLA-01-AC) | 285 mm | **56,8%** | 18,1% |
| 300 (BLA-03-AC) | 372 mm | **90,5%** | 67,0% |
| 460 (PSC-02) | 500 mm | 99,9% | 96,1% |

**A prateleira de 200 acomoda 56,8% do faturamento, e só virando o produto de
lado. De frente, com o rótulo à mostra, cai para 18,1%.** Esse é o motivo mais
duro para não fazer o vão mais longo na profundidade mais rasa: seria a maior
área de exposição do sistema servindo a menor parte do catálogo.

E resolve por que o corte vale mesmo com a alternativa da cruzeta: **o comprimento
vem da corrida, não do painel.** Um paredão de 200 de profundidade continua
possível com 200×450 e mais vãos — só paga mais cruzeta.

### Altura livre da baia — e por que a altura mista não é luxo

| ripa vertical | passo | livre (menos o painel) | % do faturamento em pé |
|---|---|---|---|
| BAL-02-AC 270 | 261,88 | **247 mm** | **79,1%** |
| PSA-05 513 | 504,88 | **490 mm** | **98,2%** |

Um módulo só de ripa 270 deixa **21% do faturamento fora** — o que não fica de pé
em 247 mm. Um módulo só de 513 desperdiça altura em 79% dos casos. **Misturar as
duas na mesma pilha é o que cobre o catálogo inteiro**, e é exatamente o que a
imagem de referência faz.

## 6. O que isso muda nas quatro famílias

O paredão era **200 × 754** — o painel de razão 3,77, o primeiro a cair. Ele passa
a **300 × 754** (razão 2,51):

| família | painel | pilha de baias (baixo → topo) | coroa | medida final |
|---|---|---|---|---|
| Checkout | 300 × 450 | 270 · 270 · 270 · 270 | **270 + gancheira** | 892 × 372 × **1.402** |
| Ilha | 460 × 634 | 270 · 270 · 270 | — | 1.252 × 500 × **878** |
| Ponta de gôndola | 300 × 634 | 270 × 5 | **513** | 1.252 × 372 × **1.907** |
| Paredão | 300 × 754 | 270 × 7 | — | 2.970 × 285→**372** × 1.926 |

A corrida do paredão não muda (2.970 mm em 4 vãos) e a profundidade sobe de 285
para 372 mm — o que a tabela do §5 diz que era o ajuste certo de todo modo:
**de 56,8% para 90,5% da curva.** Uma gôndola de parede a 372 mm de profundidade
é medida normal de mercado; a 285 era rasa demais.

### A alternativa da cruzeta, medida contra a do painel mais fundo

A saída proposta para manter os 200 mm era "coloca uma cruzeta e aumenta para o
lado" — construir o comprimento com mais vãos de painel curto. As quatro rotas,
todas com 8 prateleiras e ~3.000 mm de corrida:

| rota | corrida | prof. | peso | custo | cruzetas | painéis | curva |
|---|---|---|---|---|---|---|---|
| **300×754 · 4 vãos** | 2.970 | 372 | 125,4 kg | **R$ 2.344** | 48 | 32 | **90,5%** |
| 200×754 · 4 vãos (a Rev. 1) | 2.970 | 285 | 104,5 kg | R$ 1.946 | 48 | 32 | 56,8% |
| 200×450 · 7 vãos (a alternativa) | 3.068 | 285 | 114,8 kg | R$ 2.114 | **96** | 56 | 56,8% |
| 300×634 · 5 vãos | 3.097 | 372 | 133,4 kg | R$ 2.487 | 64 | 40 | 90,5% |

**A alternativa da cruzeta custa R$ 2.114 e continua em 56,8%.** Ir para 300 de
profundidade custa **R$ 230 a mais (11%)** e compra **+34 pontos de cobertura**.
Ela dobra a contagem de cruzeta (96) e sobe o painel de 32 para 56 peças — mais
estoque, justamente o que o corte da grade queria evitar. **Não compensa.**

O que ela resolve bem é outra coisa: quando o ponto de venda for de blister,
cartela e limpeza — categorias que a prateleira rasa atende —, `200×450` com mais
vãos é a rota certa e continua na grade.

⚠️ **125 kg por módulo é decisão de logística.** O paredão M nessa configuração
passa a exigir embarque e montagem em duas partes, ou a versão P (2.233 mm,
94,5 kg) como unidade padrão.

## 7. Ainda falta medir — duas fitas, no showroom

1. **Passo vertical.** Duas prateleiras com a ripa **BAL-02-AC (270)**, de apoio a
   apoio. **261,9 mm → modelo A. 335,0 mm → modelo B.** Não tem meio. O encaixe
   vertical da trizeta abre para baixo e o topo é fechado (chapa em z 70,0–72,9),
   e é por isso que ela sai em par espelhado — a dúvida é se o par empilha um nó
   ou dois por nível.
2. **Profundidade externa.** Um nó com a ripa **BLA-01-AC (200)** montada, face
   externa a face externa: deve dar **285,3 mm**.
3. **De brinde, se der:** um vão com PSC-01 (315) deve fechar **357,0 mm**, e a
   coroa montada deve passar **21,6 mm por lado** do corpo.

## 8. O que continua aberto

1. **A chapa crua.** A `PAN-01` tem 200 mm de largura. Dos 7 painéis, **5 são de
   300 ou 460** e precisam de emenda ou chapa mais larga. O corte de 12 para 7
   reduz o estoque, mas não resolve isso.
2. **O painel de fundo não sai da lista dos 7.** Fechar o fundo de uma baia exige
   um corte de `comprimento × altura livre da baia` — 634 × 247, 754 × 247 etc.
   Nenhum deles está na grade. O portal já lista isso como corte dedicado.
3. **A orientação de uso da peça L** (§3), que define a sobra de 21,62 mm da coroa.
4. **A carga de 20 kg por prateleira é provisória.** A chapa 1 da trizeta está em
   z relativo 40,0 mm, exatamente onde o encaixe de 40,60 termina: a ripa apoia
   numa chapa de 2,9 mm, dando 8,5–18,4 MPa.
5. **Ferramentaria da cruzeta** — primeira de cinco cadastrada em 17/07/2026,
   quatro já injetadas; não sabemos se as 2 cavidades são o par esq/dir.
6. **A tampinha** — STL nunca recebido; entra pelo peso cadastrado (1,10 g).
7. **Um registro sujo achado no caminho:** `CODPROD` 3579 (Kit Potes Acoplados
   c/ 5 peças) tem `ALTURA` = 45437 — uma data digitada no campo de altura.

## 9. Nota de método

O cadastro de dimensão do produto (`TGFPRO.LARGURA/ALTURA/ESPESSURA`, em cm)
está 89% preenchido e é **utilizável** — ao contrário dos campos `AD_TONELAGEMMIN`,
`AD_QTDCAVIDADE` e `AD_CODCORPROD`, que o `CLAUDE.md` registra como vazios. Vale
acrescentar à lista de fontes confiáveis: é o que transformou "acho que 200 é
raso" em "200 atende 56,8% do faturamento de lado e 18,1% de frente".
