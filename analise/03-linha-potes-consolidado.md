# Linha Potes — consolidado

Base: Sankhya, marca própria, 12 meses corridos até **24/08/2026**, empresas 1/2/14,
`STATUSNOTA='L'`, `TIPMOV IN ('V','D')` (devolução com sinal −1), `ATUALFIN<>0`,
sem transferências intercompany, **fora Avon/Natura (`CODTAB=84`) e exportação (`CODTAB=3`)**,
`CODGRUPOPROD BETWEEN 1000000 AND 1009999`. Custo: `TGFCUS`, último registro do ano, emp 1,
local 0.

Contexto: a marca própria caiu 18% no ciclo (R$ 101,4 M → R$ 83,1 M) e a taxa de acerto de
lançamento foi de 28,0% (2021) para 0,7% (2025 — 2 SKUs de 278). Tudo aqui é lido contra
esse pano de fundo: **o viés padrão é não lançar.**

---

## 1. Família trava — o pareamento de tampas

Informação de fábrica: **4 tampas cobrem 8 corpos.** Isso muda o payback, porque o
investimento de uma tampa se divide por dois corpos.

| Tampa | Corpos | Litragens | FAT 12M | vs ant. | Clientes | MB |
|---|---|---|---|---|---|---|
| A | 231 + 154 | 270 ml / 460 ml | R$ 181.152 | **−14,6%** | 759 / 822 | 64,6% / 61,4% |
| B | 232 + 155 | 500 ml / 850 ml | R$ 410.623 | +1,4% | 920 / 952 | 45,8% / 58,4% |
| **C** | **233 + 156** | **1,1 L / 2,2 L** | **R$ 608.996** | **+32,9%** | **1.124** / 946 | 52,6% / 46,2% |
| D | 234 + 151 | 2,3 L / 4,3 L | R$ 448.566 | +7,7% | 686 / 550 | 34,5% / 44,9% |
| | | | **R$ 1.649.337** | **+10,5%** | | |

**A família cresce 10,5% enquanto a marca própria cai 18%** — é o melhor lugar do
portfólio para investir.

**O motor é a litragem média, não a pequena.** A leitura anterior ("Alto cresce, Raso cai")
estava errada; com o pareamento correto o eixo é o tamanho. A tampa A é a única caindo.
A tampa C cresceu R$ 151 k no ano e o 233 tem **1.124 clientes** — o SKU mais penetrado
da família.

Margem cai com o tamanho (A ~63% → D ~40%): resina escala com o volume, preço não.

---

## 2. Chrono (tampa datadora) — veredito: passa **só** pela rota do inserto

### O problema de engenharia
Especificado como "válvula que indica mês e data", o datador **é** a válvula: peça rotativa
sobre o assento de vedação. Folga de rotação é caminho de vazamento.

**Separar as funções.** Disco datador cedado no topo da tampa, **sem furar**:
1. zero caminho de vazamento, zero risco de claim
2. o disco vira **peça comum** — reusável em trava, modular e rosca
3. peça pequena roda nas injetoras **≤ 260 t**, onde há 7 de 15 paradas

### O payback decide, e quem decide o payback é a ferramentaria

Tampa C move **121.194 peças/ano**. Capturando 15% com spread líquido de R$ 0,55
(prêmio − custo do disco e da montagem) → **~R$ 10 k/ano**.

| Rota | Custo típico | Payback | Veredito |
|---|---|---|---|
| Molde novo de tampa | R$ 80–150 k | 8–15 anos | **não passa** |
| Inserto trocável + 1 molde do disco | R$ 25–35 k | ~3 anos | passa raspando |

**Pergunta aberta, e é a que decide:** os moldes de tampa atuais aceitam inserto?
É questão para o ferramenteiro, não para o ERP.

### Alternativa recomendada
Colocar o datador **nas referências que já existem**, em vez de criar 8 novas. Captura o
diferencial sem somar 8 SKUs numa carteira que acertou 2 de 278. Se o datador é bom, ele
vende o 233 que já tem 1.124 clientes.

**Se for criar SKU novo: comece pela tampa C, depois a D. Nunca pela A.**

---

## 3. Modulares — freio

| Ref | Litragem | FAT 12M | Δ | Clientes | MB |
|---|---|---|---|---|---|
| 319 | 250 ml | R$ 42.015 | −27,7% | 272 | 65,1% |
| 320 | 450 ml | R$ 31.523 | −21,6% | 248 | 61,4% |
| 321 | 800 ml | R$ 35.431 | −40,9% | 267 | 59,6% |
| 322 | 1,2 L | R$ 64.068 | −28,9% | 369 | 58,8% |
| 323 | 2,4 L | R$ 99.230 | **+9,0%** | 375 | 48,0% |
| | | **R$ 272.267** | **−19,8%** | | |

6× menor que a trava, com 3-4× menos penetração (248-375 clientes contra 550-1.124).

### O sinal que trava a decisão
**KIT POTES MODULARES 6 PEÇAS (353.006.001): R$ 2,59 M → R$ 436 k, −83%.**

Não foi cliente que saiu:

| | Clientes | FAT | Ticket/cliente | Top 1 | Top 5 |
|---|---|---|---|---|---|
| Ciclo anterior | 127 | R$ 2.593.200 | R$ 20.419 | 6,8% | 24,1% |
| Ciclo atual | **179** | R$ 435.975 | **R$ 2.436** | 13,6% | 40,8% |

Os clientes **aumentaram** e o ticket caiu 88%. Queda difusa no canal inteiro — pior que
contrato encerrado, porque não há um telefone para ligar.

**Veredito: não investir molde aqui até a queda do 353 ter explicação.** Custa zero
investigar e pode devolver mais que um lançamento.

### O claim "não vaza" está certo — na linha errada
**Zero dos 267 anúncios coletados no ML dizem "não vaza".** A linguagem está livre e é
claim melhor que "hermético": concreto, testável, sem o problema do art. 36 do CDC.

Mas **rosca veda melhor que tampa PE de encaixe** — volta de aperto dá força de fechamento
crescente; encaixe em PE mole relaxa por fluência. O "não vaza" pertence à **rosca 2 L**,
que cresce 66%, não ao modular em PE.

Teste antes de escrever: água corada, fechado, invertido 30 min e 24 h, com foto e data.
Palavra final passa pelo jurídico.

---

## 4. Kits

### O que o mercado faz (267 anúncios ML)
**181 de 267 (68%) são kit/conjunto/jogo.** O mercado não vende pote avulso.

| Peças | Anúncios | Ticket médio | Preço/peça |
|---|---|---|---|
| 2–3 | 25 | R$ 49,88 | R$ 20,63 |
| **4–6** | **58** | **R$ 58,37** | **R$ 12,38** |
| 7–12 | 42 | R$ 101,77 | R$ 9,91 |
| 13+ | 30 | R$ 101,62 | R$ 4,78 |

**4 a 6 peças é a faixa que captura valor.** Acima de 12, o preço por peça cai 60% — kit
grande é desconto disfarçado.

⚠️ `vendidos` veio **nulo nos 267**. Isso é evidência de **preço e presença**, não de demanda.

### A linha rosca 2 L

| Ref | Produto | FAT 12M | Δ | Peças | Clientes | MB |
|---|---|---|---|---|---|---|
| 362 | Açúcar | R$ 248.403 | +56,2% | 50.726 | **1.002** | 48,0% |
| 363 | Café | R$ 247.063 | +42,9% | 49.629 | 712 | **25,9%** ⚠ |
| 360 | Feijão | R$ 142.423 | +210,3% | 27.731 | 543 | 50,4% |
| 359 | Arroz | R$ 128.600 | +163,3% | 25.124 | 391 | 50,3% |
| 361 | Farinha | R$ 23.620 | **−51,5%** | 4.089 | 232 | 37,7% |
| | | **R$ 790.109** | **+66,2%** | 157.299 | | |

Genéricos da mesma plataforma: **238 transparente 2 L +522%** (R$ 181.397, MB 52,0%),
**239 transparente 3 L +242%** (R$ 75.341, MB 46,0%).

Recorte limpo: **rosca 2 L e 3 L em transparente cresce; 500 ml e branco, não.**
(238 branco −25%, 236 branco −49%, 239 branco −16%; tomatinho 500 ml −36%,
feijão 500 ml −40%, alho 500 ml −33%.)

### ✅ Recomendação nº 1 — KIT MANTIMENTO ROSCA 2 L, 4 peças
Arroz + Feijão + Açúcar + Café. **Zero molde.**

- Base: **R$ 766.489/ano, +79,6%** (era R$ 426.730)
- 4 peças = a faixa de melhor preço por peça no ML
- Custo somado R$ 11,34; avulso somado R$ 20,14 → kit a R$ 21–23 atacado, MB ~45%
- **Nenhum kit existe nessa plataforma** — verificado no `TGFPRO`; os "KIT MANTIMENTOS"
  atuais são das refs 152 e 038/4, outra família
- Precedente próprio: KIT MANTIMENTOS 5 PÇS preto (152.006.003) R$ 299.993, +31%
- **Farinha fica de fora**: −51,5%, 232 clientes, 4.089 peças — 12× menos volume que o açúcar

Custo total: cadastro, EAN, arte, caixa, foto. Nada de ferramentaria.

### ✅ Recomendação nº 2 — estender o conjunto flat de 2 peças
O kit mais forte da casa não é de pote:

| Ref | Cor | FAT 12M | Δ | Clientes |
|---|---|---|---|---|
| 920.004.003 | Preto | R$ 320.249 | +383% | 821 |
| 920.004.002 | Branco | R$ 115.283 | +396% | 509 |
| 920.004.086 | Chumbo | R$ 109.007 | +219% | 424 |
| | | **R$ 544.539** | **+254%** | |

MB 60,8%. Flat + kit + cor ao mesmo tempo (vetores V4 e V2).
E **KIT CHURROS FÁCIL** (408.012.002): R$ 606.221, +107%, **839 clientes**. A linha "Fácil"
funciona para churros e biscoito (+60%), não para donuts (−16%) nem decorador (−10%).

### ❌ Recomendação nº 3 — não fazer kit da linha trava
Já existe: **190.012.001 KIT POTES ALTOS COM TRAVAS 3 PEÇAS** — R$ 24.459, **−64%**,
81 clientes, top 1 = 5,5% (sem concentração). O canal já respondeu.

### ⚠️ Cuidado com os benchmarks
- **293.006.002** (KIT ACOPLADOS 5 PÇS, R$ 609.103, +40%): **2 clientes = 50,7%** do
  faturamento. 414 clientes no papel, meia dúzia no caixa.
- **500.002.001** (KIT NITRONBOX, R$ 2,68 M): **50 clientes**, −16%. É private label,
  não canal. Não usar como prova de que kit funciona.

---

## 5. Achado aberto — o custo do Café 2 L

**363 (Café 2 L)** custa **R$ 3,69** contra **R$ 2,55** de açúcar, feijão e arroz — mesmo
corpo de 2 L, preço praticamente igual (R$ 4,98 vs R$ 4,90), e **MB de 25,9% contra 48–50%**.

R$ 1,14 × 49.629 peças = **R$ 56.577/ano de margem**.

Ou o café tem uma peça a mais que ninguém lembra, ou o custo está errado no `TGFCUS`.
Nos dois casos vale mais que a maioria dos lançamentos da safra passada — e a investigação
é uma conversa sobre custo, não um molde.

---

## 6. Ordem recomendada

1. **KIT MANTIMENTO ROSCA 2 L de 4 peças** — zero molde, R$ 766 k de base crescendo 80%
2. **Pergunta ao ferramenteiro:** os moldes de tampa da linha trava aceitam inserto?
3. **Investigar** o custo do Café 2 L e a queda de 83% do kit modular 353
4. **Chrono** — passa se o inserto for viável, começando pela tampa C
5. **Modular em PE** — fora, até o item 3 ter resposta

## Perguntas ainda sem resposta
- Os moldes de tampa atuais aceitam inserto trocável? (decide o Chrono)
- Por que o kit modular 353 caiu 83% de forma difusa?
- Por que o Café 2 L custa R$ 1,14 a mais que os irmãos?
- Por que as refs `176.024.001` e `210.024.001` (trava+válvula, as melhores margens da
  família) caíram 57% e 39%? — pendência aberta desde o ciclo anterior

---

## 7. Pote quadrado — o formato já existe no catálogo

**Verificação obrigatória feita primeiro** (lição nº 1 deste projeto). O quadrado/retangular
não é espaço em branco: são **4 plataformas** e ~**R$ 2,39 M/ano**, maior que a linha trava.

### Quadrado com travas (família 037x)
| Ref | Litragem | FAT 12M | Δ | Clientes | Preço | Custo | MB |
|---|---|---|---|---|---|---|---|
| 3770.012.001 | 1,8 L | R$ 264.653 | **+42,0%** | 730 | 4,89 | 2,77 | 43,4% |
| 3760.012.001 | 3,7 L | R$ 179.791 | +24,8% | 414 | 7,08 | 3,81 | 46,2% |
| 3780.012.001 | 860 ml | R$ 158.253 | +9,5% | **809** | 3,86 | 1,79 | 53,7% |
| 3790.012.001 | 360 ml | R$ 74.695 | −21,8% | 697 | 2,29 | 1,00 | 56,2% |
| | | **R$ 677.392** | **+18,7%** | | | | |

### Alto retangular (família 025x)
| Ref | Litragem | FAT 12M | Δ | Clientes | MB |
|---|---|---|---|---|---|
| 2580.012.001 | 3 L | R$ 307.915 | **+87,9%** | **870** | 41,1% |
| 2590.012.001 | 1,5 L | R$ 187.627 | +27,1% | 674 | 48,8% |
| 2570.012.001 | 4,6 L | R$ 162.007 | +9,1% | 455 | 42,7% |
| 2500.012.001 | 868 ml | R$ 46.733 | **−42,6%** | 503 | 49,9% |

### Raso retangular (família 30x)
302 (1,9 L) R$ 88.930 **+74%** · 301 (950 ml) R$ 53.980 +3,8% · 300 (460 ml) R$ 36.395
+2,5% · 303 (3,2 L) R$ 30.679 **−40%**

### Quadrado com válvula
**240.024.001 (3 L): R$ 32.129 → R$ 190.421 = +492,7%**, 283 clientes, MB 42,8%.

⚠️ Armadilha de referência confirmada de novo: `037/7`, `037/8`, `037/9` têm a **mesma
descrição** dos 3770/3780/3790 mas 4 a 7 clientes — são as refs antigas. Não somar.

### O achado que vale mais que o molde

Comparando volume equivalente, quadrado × redondo:

| | Redondo 850 ml (155) | Quadrado 860 ml (3780) |
|---|---|---|
| Preço | R$ 3,81 | R$ 3,86 |
| Custo | R$ 1,59 | **R$ 1,79 (+12,6%)** |
| MB | 58,4% | **53,7% (−4,7 pts)** |

**A Nitron vende quadrado ao mesmo preço por litro do redondo e paga 12,6% mais para
fabricar.** Coerente com a geometria: um cubo tem ~8% mais área de superfície que um
cilindro de proporção ótima no mesmo volume; cantos e reforços fazem o resto.

No Mercado Livre, os anúncios que **declaram** formato: quadrado/retangular preço médio
**R$ 77,71** (47 anúncios, 25 marcas) contra redondo **R$ 36,97** (14 anúncios, 6 marcas).
Ressalva séria: 206 dos 267 não declaram formato, n=14 no redondo, e o número de peças do
kit confunde a comparação. É indício de direção, não prova.

Universo quadrado/retangular ≈ R$ 2,39 M. **Recuperar os 4,7 pontos de margem vale
~R$ 112 k/ano, sem nenhum molde** — 11× o retorno estimado do Chrono.

### A plataforma válvula dobrou

| Ref | Produto | FAT 12M | Δ | Clientes |
|---|---|---|---|---|
| 244.012.001 | Raso válvula 3,2 L | R$ 284.114 | +81,4% | 511 |
| 243.024.001 | Raso válvula 1,9 L | R$ 231.370 | +58,0% | 495 |
| 242.024.001 | Raso válvula 950 ml | R$ 212.819 | +51,4% | 567 |
| **240.024.001** | **Quadrado válvula 3 L** | **R$ 190.421** | **+492,7%** | **283** |
| 818.012.001 | Alto válvula 2,9 L | R$ 163.977 | **+1.272%** | 385 |
| 819.012.001 | Alto válvula 4,6 L | R$ 159.834 | **+1.005%** | 302 |
| 817.012.001 | Alto válvula 1,5 L | R$ 111.688 | +487% | 365 |
| 241.024.001 | Raso válvula 460 ml | R$ 93.779 | +0,7% | 423 |
| 246.024.001 | Alto válvula 868 ml | R$ 79.124 | −8,9% | 374 |
| **176.024.001** | **Válvula + TRAVAS 600 ml** | R$ 31.803 | **−56,1%** | 162 |
| **210.024.001** | **Válvula + TRAVAS 788 ml** | R$ 16.171 | **−49,0%** | 61 |
| | | **R$ 1.575.100** | **+95,6%** | |

**A pendência aberta virou padrão.** 9 das 11 referências de válvula cresceram (de +0,7% a
+1.272%). As **duas únicas que caem são exatamente as duas que combinam válvula + trava**,
ambas ~−50%, numa plataforma que quase dobrou. Isso deixa de ser coincidência.

### Crítica ao "quadrado hermético, parede fina, tampa PE"

São quatro forças puxando em direções opostas:

1. **Quadrado é a geometria mais difícil de vedar.** Quatro cantos onde o lábio muda de
   direção; canto perde compressão primeiro e é onde a tampa levanta. Vedação redonda
   comprime uniforme.
2. **Parede fina piora a vedação.** O aro precisa ficar rígido para distribuir a força de
   fechamento; painel fino e plano embarriga e tira o aro do plano.
3. **Parede fina pode tirar você das máquinas paradas.** Moldagem de parede fina exige
   pressão de injeção maior e enchimento mais rápido → **mais tonelagem de fechamento por
   área projetada, não menos**. A folga da Nitron está em ≤ 260 t (7 de 15 paradas); a
   faixa 1.101–2.000 t está a 73,5% com **zero máquina livre**. Isso inverte o argumento
   do CNC ocioso e precisa ser verificado com processo **antes** do projeto.
4. **Tampa PE** — já estabelecido: PE não cria hermeticidade (vedação é geometria de lábio
   + força de fechamento). E PE tem módulo menor, então embarriga mais nos vãos planos de
   um quadrado.

**Quadrado com rosca é contradição geométrica**: rosca precisa girar, logo o fechamento tem
que ser circular. Corpo quadrado com gargalo redondo existe no mercado, mas os cantos viram
espaço morto no enchimento e o corpo é molde novo do mesmo jeito.

### Recomendação — estender o 240, não criar plataforma

O 240 já é quadrado, já tem válvula, cresce 492,7% e tem **283 clientes** — contra 730 do
quadrado trava 1,8 L e 809 do 860 ml. Está subdistribuído, não saturado.

As três litragens que o canal mais compra em quadrado são **860 ml (809 clientes)**,
**1,8 L (730)** e **3 L / 3,7 L**. O 3 L já existe. A escada de 3 tamanhos é
**~900 ml / ~1,8 L / 3 L** com o topo já provado.

⚠️ **Tensão central, dita explicitamente:** a rota barata seria uma tampa de válvula para os
corpos quadrados com trava que já existem — mas isso cai exatamente na combinação
válvula + trava que está caindo ~50%. Não dá para ter as duas coisas sem resolver primeiro
por que 176 e 210 caem.

⚠️ **Não sabemos o que compartilha ferramental.** `TPRCPR` (roteiro) tem 0 linhas e
`AD_FICHATECNICA` tem 4. Quantos moldes essa extensão custa é pergunta para a ferramentaria,
não para o ERP.

### Ordem para o quadrado
1. **Revisar preço do quadrado** — R$ 2,39 M vendidos ao preço/litro do redondo com 12,6%
   mais custo. ~R$ 112 k/ano, zero molde.
2. **Investigar 176 e 210** — por que válvula + trava cai 50% numa plataforma que dobra.
   Decide o Chrono e decide a rota barata do quadrado+válvula.
3. **Distribuir o 240** antes de estender — 283 clientes num SKU crescendo 493% é problema
   comercial, não de produto.
4. **Só então** avaliar as litragens novas de quadrado com válvula.
5. **Fora:** quadrado hermético de parede fina com tampa PE.
