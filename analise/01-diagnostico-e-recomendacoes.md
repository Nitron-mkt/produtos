# Projeto de Desenvolvimento de Produtos Nitron
## Fase 1 — Diagnóstico das curvas e recomendação de lançamentos

**Fonte:** Sankhya (produção) — TGFCAB/TGFITE/TGFPRO/TGFGRU/TGFCUS/TGFTAB/TGFNTA
**Escopo:** Nitronplast (empresas 1 Matriz, 2 Filial, 14 Extrema) — grupo "Produto Acabado (PA)/Revenda"
**Período:** 36 meses em janelas móveis de 12 meses (ago/23–jul/24, ago/24–jul/25, ago/25–jul/26)

> **Revisão 3** — auditoria do vetor cor e levantamento de capacidade das injetoras.
> **Dois certeiros da revisão 2 estavam errados** (produtos que eu propus lançar já existem).
> Correções marcadas com **[CORRIGIDO]**.

---

## 0. Sobre o filtro de tabela: o que encontrei

A "003 – tabela padrão" é **`CODTAB = 0`**, cadastrada como `PV0003 - TABELA PADRÃO`. Atenção:
`CODTAB = 3` é a `TABELA EXPORTAÇÃO NITRON`. A tabela usada na venda fica em `TGFITE.NUTAB`,
que se resolve via `TGFTAB.NUTAB → CODTAB`.

Você estava certo sobre a distorção. A tabela **`PV0134 - AVON` (CODTAB 84) fez R$ 8,97 M em apenas
580 itens** nos últimos 12 meses — é o cliente Natura/Avon, e é ele que quebrava a curva. Todos os
SKUs "Candy" e com referência de 6-8 dígitos que apareciam no topo da revisão 1 saem com esse filtro.

**Mas o corte só na tabela padrão tem um problema que preciso registrar:** a padrão caiu de
R$ 48,3 M → R$ 30,6 M → R$ 13,2 M (−73%), e isso é **migração de tabela, não queda de demanda**.
As tabelas que nasceram ou cresceram no período somam cerca de R$ 37 M — praticamente os R$ 35 M
que a padrão perdeu:

| Tabela | 23/24 | 24/25 | 25/26 |
|---|---|---|---|
| PV0003 – TABELA PADRÃO | 48,3 M | 30,6 M | **13,2 M** |
| FAT EXTREMA SIMPLES NACIONAL | — | 8,9 M | 10,2 M |
| FOB ESPECIAL NORDESTE | 0,9 M | 5,8 M | 7,5 M |
| AMIGÃO | 0,4 M | 2,9 M | 3,5 M |
| ESPECIAL DISTRIBUIDORA | 0,25 M | 0,8 M | 3,0 M |
| RED-141 EXTREMA SIMPLES NACIONAL | — | 0,2 M | 2,6 M |
| CLUBE NITRON (4 tabelas) | — | — | 5,6 M |
| TUBARÃO / LOJAS G / SHOPPING UD | — | — | 3,0 M |
| CLIENTES FORA DA PROMOÇÃO | 8,2 M | 4,4 M | 0,29 M |

Extrema (empresa 14) abriu em 2025 e o programa **Clube Nitron** nasceu no último ciclo. Os clientes
saíram da tabela padrão sem sair do mercado. Então trabalho com **dois cortes**, cada um para o que
ele mede bem:

| Corte | Definição | Serve para | Não serve para |
|---|---|---|---|
| **A — Tabela padrão** | `CODTAB = 0` | Teto de preço e de margem: quanto o produto rende quando vendido sem desconto negociado | Tendência — contaminado por migração de tabela |
| **B — Mercado limpo** | tudo menos Avon/Natura (84) e exportação (3) | Curva, tendência, vetores, histórico de lançamento | Precificação de tabela cheia |

O **corte B é a curva principal** deste relatório: tira a distorção que você apontou e mantém
todo o canal real (Modenuti, Kalunga, Centerlar, Lojas Mel, Tambasa, Clube Nitron, Amigão, Leroy).

---

## 1. A curva limpa

| Janela 12M | Corte B — mercado limpo | Global (revisão 1) |
|---|---|---|
| ago/23–jul/24 | R$ 101,4 M | R$ 122,7 M |
| ago/24–jul/25 | R$ 96,1 M | R$ 117,6 M |
| ago/25–jul/26 | **R$ 83,1 M** | R$ 94,9 M |
| Variação 2 anos | **−18,0%** | −23% |

**[CORRIGIDO]** A queda real é de 18%, não 23%. Cinco pontos dos 23 eram o desmonte do contrato
Avon/Natura, que é uma conversa de conta-chave, não de desenvolvimento de produto.

| Linha | 23/24 | 24/25 | 25/26 | Var 2a | MB % | Lucro bruto |
|---|---|---|---|---|---|---|
| Organização | 29,2 M | 26,2 M | 22,1 M | −24% | 54,2% | **11,8 M** |
| Potes | 18,9 M | 17,2 M | 16,0 M | **−15%** | 45,1% | 7,2 M |
| Cozinha | 15,1 M | 13,8 M | 12,4 M | −18% | 49,9% | 6,2 M |
| Lixeiras | 9,0 M | 10,7 M | 9,1 M | **+0,2%** | 43,0% | 3,9 M |
| **Frasqueiras** | 6,3 M | 7,0 M | **6,9 M** | **+8,6%** | 53,7% | 3,7 M |
| Banheiro | 4,2 M | 4,7 M | 4,1 M | **−3,5%** | 55,0% | 2,3 M |
| Limpeza | 4,3 M | 4,4 M | 3,6 M | −15% | 54,8% | 2,0 M |
| Jarras | 3,6 M | 2,6 M | 2,6 M | −29% | 43,1% | 1,1 M |
| **Micro-ondas** | 1,8 M | 1,7 M | 1,7 M | **−8,7%** | **53,6%** | 0,9 M |
| **Decor Util** | 1,2 M | 1,7 M | 1,4 M | **+21%** | **59,6%** | 0,8 M |
| Teca | 1,1 M | 1,7 M | 1,3 M | +10% | **36,8%** | 0,5 M |
| ECO | 2,1 M | 2,1 M | 0,8 M | −64% | 57,0% | 0,4 M |
| Infantil | 2,6 M | 1,2 M | 0,5 M | **−81%** | 61,4% | 0,3 M |
| Geladeira | 0,8 M | 0,5 M | 0,4 M | −42% | 58,4% | 0,3 M |
| Coloratto | 0,7 M | 0,5 M | 0,3 M | −51% | 55,8% | 0,2 M |
| Realce | 0,5 M | 0,2 M | 0,06 M | −87% | 41,5% | 0,02 M |
| POP | — | — | 0,04 M | nova | 19,7% | 0,01 M |

### Quatro conclusões da revisão 1 que estavam erradas

1. **[CORRIGIDO] Potes caiu 15%, não 38%.** Os R$ 12,5 M de queda da revisão 1 eram quase todos
   rotação de private label (Kit Potes Candy). A linha de marca própria está bem menos machucada.
2. **[CORRIGIDO] Micro-ondas tem margem de 53,6%, não 29,8%,** e cai 8,7%, não 32%. A margem ruim
   *era o contrato OEM*, não a linha. Micro-ondas sai da lista de "não lançar" e volta a ser
   candidata — a Caçarola 2,6L cresce 50% com 664 clientes.
3. **[CORRIGIDO] Decor Util cresce 21%, não 96%,** e tem MB de 59,6%, não 65,4%. Continua sendo a
   melhor margem da casa entre as linhas que crescem, mas o +96% estava inflado pelo Cortador
   Dupla Face (OEM). O caso ainda se sustenta — apenas menor do que parecia.
4. **[CORRIGIDO] Teca tem MB de 36,8%, não 18,8%.** Abaixo da média da casa, mas não catastrófico.
   Parte do problema de margem também era OEM.

Confirmados como colapso real de marca própria: **Infantil (−81%), Realce (−87%), ECO (−64%),
Geladeira (−42%), Coloratto (−51%)**. E **Banheiro está praticamente estável (−3,5%)**, não caindo
23% — outra correção relevante.

---

## 2. O achado principal piora no corte limpo

Taxa de acerto de lançamento por safra, **só marca própria**:

| Safra | SKUs | Acertos (R$500k+) | Taxa | Abaixo de R$100k |
|---|---|---|---|---|
| 2021 | 186 | 52 | **28,0%** | 82 (44%) |
| 2022 | 452 | 55 | 12,2% | 285 (63%) |
| 2023 | 500 | 39 | 7,8% | 318 (64%) |
| 2024 | 357 | 12 | 3,4% | 304 (85%) |
| 2025 | 278 | **2** | **0,7%** | 247 (89%) |
| 2026 (parcial) | 96 | 0 | 0% | 95 |

**Dos 278 SKUs de marca própria lançados em 2025, dois passaram de R$ 500 mil.** Os 12 "acertos"
que eu reportei na revisão 1 para essa safra incluíam SKUs OEM — tirando o private label, sobram 2.

A ressalva de maturidade continua valendo: safras recentes tiveram menos tempo. Mas 304 dos 357 SKUs
de 2024 não passaram de R$ 100 mil em mais de dois anos. Isso é proliferação de cadastro.

**A recomendação nº 1 do projeto, antes de qualquer produto: lançar menos e melhor.**

---

## 3. Os 7 vetores — todos sobrevivem, alguns ficam mais fortes

Este foi o teste mais importante da revisão: se os vetores só existiam por causa do private label,
a carteira toda cairia. Não é o caso.

| # | Vetor | Evidência no corte limpo (24/25 → 25/26) |
|---|---|---|
| **V1** | **Válvula** | Pote Alto 2,9L **+1.297%** · Alto 4,6L **+1.032%** · Quadrado 3L **+495%** · Raso 3,2L +73% · Raso 1,9L +56% |
| **V2** | **Cor chumbo** | Lixeira Rattan Pedal 6L **+208%** (R$ 554 k, 711 clientes) · Juta Pedal 12L **+196%** |
| **V3** | **Acoplado + rosca** | Acoplado 2L **+566%** · **Feijão 2L +198%** · Açúcar 2L +51% · Café 2L +44% |
| **V4** | **Flat / slim** | Porta Detergente Flat 2 pçs **+420%** — 364 → **811 clientes** |
| **V5** | **Nitronfort** | Caixa 2,2L **+111%** · Caixa 16L **+74%** |
| **V6** | **Gadget "Fácil"** | Churros Fácil **+117%** (342 → **842 clientes**) · Escorredor Multiuso **+110%** · Saleiro Premier **+101%** |
| **V7** | **Kit / multipack** | Kit Acoplados 5 pçs preto **+99%** · Kit Potes Altos 3 pçs **+71%** · Kit Acoplados branco +36% |

Ficaram **mais** fortes no corte limpo: **Cesto Europa Juta +372%** (era +230%) e **Pote Alto
Válvula 2,9L +1.297%**, que não aparecia antes. E surgiu um oitavo vetor que a curva global escondia:

**V8 — Frasqueira, variante de cor e formato.** Mega Luxo **vermelha** 12L **+183%** · Oval com
bandeja **branca** **+177%** · a 2,8L branca +33%. Três variantes da mesma família crescendo forte
ao mesmo tempo, na única linha em alta. É a evidência mais direta da carteira.

---

## 4. Teto de preço e margem — o que o corte A entrega

Aqui a tabela padrão ganha valor: mostra quanto o produto rende **sem desconto negociado**. É a
régua para precificar lançamento.

| Produto | Preço padrão | Preço médio geral | MB padrão | Clientes na padrão |
|---|---|---|---|---|
| Kit Churros Fácil | R$ 14,49 | R$ 8,51 | **81,5%** | 405 |
| Organizador Multiuso Rattan 3 div. | R$ 6,47 | R$ 4,02 | **78,8%** | 448 |
| Porta Vassouras 4 encaixes preto | R$ 10,11 | R$ 6,16 | **75,9%** | 197 |
| Porta Sabão em Pó Dosador 2 kg preto | R$ 20,11 | R$ 10,46 | **74,1%** | 106 |
| Porta Escovas c/ Tampa branco | R$ 7,57 | R$ 4,80 | 72,3% | 343 |
| Frasqueira Medicamentos 6,2L | R$ 28,49 | R$ 19,07 | 71,8% | 270 |
| Porta Talher 6 div. branco | R$ 18,46 | R$ 12,19 | 68,4% | 269 |
| Frasqueira Medicamentos 2,8L | R$ 15,05 | R$ 11,61 | 62,8% | 313 |
| Frasqueira Medicamentos **vermelha** 2,8L | R$ 15,24 | — | 63,3% | 95 |

Dois usos práticos:

1. **A margem-teto é de 60% a 80%**, não os 45–55% da média. O desconto de canal come 15 a 25 pontos.
   Um lançamento precificado na padrão e vendido majoritariamente na padrão vale muito mais.
2. **O Churros Fácil a 81,5% de MB é o produto mais rentável da casa.** Isso reforça o certeiro de
   Decor Util mais do que qualquer outro dado do projeto.

E a **Frasqueira vermelha 2,8L já aparece na padrão** com 95 clientes e MB de 63,3% — a tese de
variante de cor está validada na tabela cheia, não só na média.

---

## 5. A carteira — 3 candidatos + 1 certeiro por linha

Oito linhas, **R$ 37,7 M dos R$ 41,4 M de lucro bruto (91%)**. Cada certeiro cruza **molde existente
com vetor comprovado** — o investimento é pigmento, embalagem e cadastro, não ferramentaria.
As recomendações da revisão 1 se mantêm: os vetores sobreviveram ao corte. O que mudou foram os
números de suporte e a entrada de Micro-ondas como linha elegível.

### 5.1 Organização — R$ 22,1 M · MB 54,2% · LB R$ 11,8 M · −24%
Top: Kit Nitronbox R$ 2,68 M (49 clientes, B2B) · Suporte Botijão areia R$ 1,25 M · Organizador
Multiuso Rattan R$ 862 k (1.732 clientes) · Gaveteiro 4 gavetas preta R$ 753 k · Suporte Botijão
preto R$ 650 k (+44%).

1. **Cesto Europa Juta — 10,8L e 18,7L em preto.** O 5,3L fez **+372%**; moldes maiores já existem na Teca.
2. **Gaveteiro Modular Rattan chumbo + torre de 3 módulos.** Modular transparente +29%, 4 gavetas rosa +110%.
3. **Organizador Multiuso Rattan com tampa / empilhável.** 1.732 clientes e **MB de 78,8% na padrão**.
4. ⭐ **CERTEIRO — Caixa Organizadora Rattan c/ Tampa em CHUMBO (4L e 16L).**
   A dupla preta + branca do 16L faz **R$ 1,13 M**. Chumbo entregou +208% na lixeira do mesmo período.
   Molde existe; entrada = pigmento e etiqueta.

### 5.2 Potes — R$ 16,0 M · MB 45,1% · LB R$ 7,2 M · −15% **[CORRIGIDO]**
Top: Kit Potes Modulares 6 pçs R$ 593 k · Kit Potes Acoplados 5 pçs R$ 591 k (+36%) · Porta Pão
2,7L R$ 498 k (1.097 clientes) · Pote Raso Travas 1,1L R$ 331 k · Kit Mantimentos 5 pçs R$ 307 k (+37%).
Com o OEM fora, **o topo de Potes é kit e pote funcional** — exatamente onde estão os vetores.

1. **Família válvula completa + kit válvula 3 peças.** Vetor mais forte do banco: **+1.297%** no 2,9L.
2. **Linha Ultraforte ampliada (tamanhos e chumbo).** O 2,1L preto +117%, 795 clientes; o 6,9L rende **66,3% na padrão**.
3. **Mantimentos acoplados com rosca — arroz e farinha 3–5L.** Hoje só açúcar, café, feijão e genérico, todos crescendo 44–566%.
4. ⭐ **CERTEIRO — Kit Mantimentos acoplado com rosca, 4–5 peças.**
   Combina V1 + V3 + V7. Os quatro avulsos acoplados somam **R$ 771 k crescendo 44% a 566%**; os dois
   kits acoplados somam R$ 792 k crescendo 36% e 99%. Ticket de ~R$ 5 para ~R$ 25 **com moldes existentes**.

### 5.3 Cozinha — R$ 12,4 M · MB 49,9% · LB R$ 6,2 M · −18%
Top: Forma de Gelo Firenze R$ 584 k · Porta Detergente Rattan R$ 516 k · Porta Frios c/ Pinça
R$ 500 k · Porta Talher 6 div. preto R$ 440 k · **Porta Óleo Italia R$ 439 k com 1.735 clientes**.
7.825 clientes — maior capilaridade da casa.

1. **Linha Flat de pia completa — 3 peças, branco, chumbo.** O 2 peças fez **+420%** e 364 → 811 clientes.
2. **Porta Óleo Italia — família e conjunto azeite + vinagre.** 1.735 clientes a R$ 2,50: a melhor porta de entrada para subir ticket.
3. **Escorredor de Pratos chumbo + versão com bandeja.** Preto R$ 387 k; Escorredor Multiuso +110%.
4. ⭐ **CERTEIRO — Conjunto Porta Detergente FLAT 3 peças (+ branco e chumbo).**
   Adoção mais rápida da linha: **+420% e 447 clientes novos em um ano**. 2→3 peças eleva ticket sem molde novo.

### 5.4 Frasqueiras — R$ 6,9 M · MB 53,7% · LB R$ 3,7 M · **+8,6% — única linha em alta**
Top: 2,8L branca **R$ 1,70 M (+33%, 1.181 clientes)** · 6,2L branca R$ 1,41 M · 1,4L R$ 701 k ·
Mega Luxo 12L R$ 461 k · Nitronfort 2,2L R$ 274 k (+111%) · Frasqueira Cristal rosa R$ 232 k (+27%).
**R$ 132 k por SKU** contra R$ 33 k em Potes. Se o projeto escolher uma linha só, é esta.

1. **Frasqueira Medicamentos com divisórias removíveis / organizador semanal de comprimidos.**
2. **Nitronfort expandido — 6L intermediário, maleta com bandeja, versão grafite.** 2,2L +111%, 16L +74%.
3. **Frasqueira Oval com bandeja — ampliar tamanhos e cores.** A branca fez **+177%** partindo de base pequena.
4. ⭐ **CERTEIRO — Frasqueira Medicamentos 2,8L e 6,2L em CHUMBO/GRAFITE.**
   O 2,8L branca é o maior SKU de marca própria da casa. **Três variantes da família já provaram
   a tese no mesmo período: vermelha 12L +183%, oval branca +177%, e a vermelha 2,8L já vende na
   tabela padrão com 63,3% de MB.** Menor risco do portfólio inteiro.

### 5.5 Lixeiras — R$ 9,1 M · MB 43,0% · LB R$ 3,9 M · **+0,2% (estável)**
Top: Rattan Pedal preta 6L R$ 1,01 M · branca 6L R$ 921 k (+30%) · Vime preta 12L R$ 720 k ·
**Rattan Pedal CHUMBO 6L R$ 554 k, de zero em dois anos** · Basculante Rattan 4,5L R$ 550 k (+21%).

1. **Lixeira Flat c/ Pedal — família de tamanhos e cores.** Hoje só a preta 7L, a R$ 24,59 de ticket.
2. **Lixeira seletiva / duo com 2 compartimentos.** Ausente do portfólio; ticket alto.
3. **Lixeira Vime em chumbo.** Preta 12L R$ 720 k, branca R$ 54 k na padrão a R$ 26,48.
4. ⭐ **CERTEIRO — Lixeira Basculante Rattan CHUMBO 4,5L + Rattan c/ Pedal CHUMBO 12L.**
   Chumbo é o vetor com maior crescimento comprovado: **+208%** e **+196%**. A basculante 4,5L
   preta faz R$ 550 k (+21%, 926 clientes) e o pedal 12L é o buraco óbvio. Moldes existem.

### 5.6 Banheiro — R$ 4,1 M · MB 55,0% · LB R$ 2,3 M · **−3,5% [CORRIGIDO]**
Top: Porta Escovas preto R$ 536 k (1.227 clientes) · branco R$ 493 k · fumê R$ 304 k — **o trio faz
R$ 1,33 M**. Porta Shampoo Madri preto R$ 421 k. Cantoneiras caindo. 6.002 clientes.

1. **Porta Escovas c/ Tampa em CHUMBO.** O trio prova três vezes que cor vende neste SKU; MB de 72,3% na padrão.
2. **Dispenser de sabonete líquido de bancada.** Hoje só saboneteira de parede a R$ 2,05–2,54. Gap total de ticket médio.
3. **Organizador / bandeja de bancada.** Inexistente; aproveita as texturas rattan.
4. ⭐ **CERTEIRO — Kit Banheiro coordenado 3 peças (porta escovas + saboneteira + porta algodão), nas 3 cores.**
   Ticket de ~R$ 5 para ~R$ 15 **sem um molde novo**, sobre a 2ª maior base de clientes da casa.

### 5.7 Limpeza — R$ 3,6 M · MB 54,8% · LB R$ 2,0 M · −15%
Top: Pá de Lixo c/ Cabo R$ 889 k (+9%, 1.049 clientes) · Porta Vassouras preto R$ 628 k ·
branco R$ 405 k (**−52%**) · Porta Sabão em Pó preto R$ 246 k (+23%).

1. **Porta Sabão em Pó c/ Dosador 5 kg.** O 2 kg rende **74,1% de MB a R$ 20,11 na padrão** — a maior margem da linha. Exige molde novo: é aposta.
2. **Kit Limpeza (pá + porta-vassouras + cestinho).** Aplica V7 sobre os dois campeões.
3. **Balde espremedor / conjunto mop.** Categoria adjacente ausente, ticket alto.
4. ⭐ **CERTEIRO — Porta Vassouras 4 encaixes em CHUMBO.**
   O preto faz R$ 628 k com 1.116 clientes e **75,9% de MB na padrão**; o branco despencou **52%** —
   saturação da cor, não do produto. Molde existe.

### 5.8 Decor Util — R$ 1,4 M · **MB 59,6% (maior entre as linhas que crescem)** · +21% **[CORRIGIDO]**
Top: **Kit Churros Fácil R$ 602 k (+117%, 842 clientes)** · Hamburgueira R$ 243 k (755 clientes) ·
Cortador e Ralador de Legumes R$ 62 k · Kit Biscoito Fácil R$ 36 k.
Com o OEM fora, **os dois maiores produtos da linha são exatamente o conceito "Fácil"**.

1. **Kit Confeitaria (bicos + saco + espátula + alisador).** O subgrupo Decor-Confeitaria existe no cadastro sem produto relevante; Biscoito Fácil rende **73,2% na padrão**.
2. **Utensílios de hambúrguer e churrasco — prensa dupla, formador de kibe.** Hamburgueira: 755 clientes, 68,7% de MB na padrão.
3. **Espremedores e cortadores em cores.** Hoje quase todo o subgrupo é branco.
4. ⭐ **CERTEIRO — Família "Fácil": Coxinha & Croquete Fácil e Pastel Fácil.**
   **O Churros Fácil rende 81,5% de MB a R$ 14,49 na tabela padrão — o produto mais rentável da
   casa** — e saltou de 342 para 842 clientes em doze meses. Molde pequeno, tonelagem baixa, CAPEX
   baixo, giro alto, compra por impulso. Coxinha é o salgado mais consumido do país e não tem
   utensílio dominante no varejo UD.

---

## 6. Onde não lançar

| Linha | Situação no corte limpo | Encaminhamento |
|---|---|---|
| **Infantil** | MB 61,4%, receita **−81%** | Reativação, não lançamento. Copo Infantil c/ Alça ainda faz R$ 320 k com 628 clientes. Diagnóstico próprio. |
| **Realce** | R$ 60 k com **47 SKUs** e 174 clientes | Descontinuação. Libera cadastro, estoque e atenção comercial. |
| **ECO** | −64%, MB 57,0% | Margem boa, execução perdida. Investigar ruptura ou perda de cliente. |
| **Geladeira** | −42%, MB 58,4% | Mesmo padrão do ECO. Margem preservada, volume evaporando. |
| **Coloratto** | −51%, MB 55,8% | Idem. |
| **Teca** | +10% mas MB **36,8%** — a 2ª pior | Revisar preço e custo antes de ampliar. Melhor do que os 18,8% da revisão 1, ainda 17 pontos abaixo da casa. |
| **POP** | Nova, 9 SKUs, R$ 36 k, MB **19,7%** | Corrigir precificação antes de ampliar. Nasceu com margem de sobrevivência. |
| **Micro-ondas** | **[CORRIGIDO]** −8,7%, MB **53,6%** | **Sai desta lista.** A margem ruim era o OEM. Caçarola 2,6L +50% com 664 clientes. Elegível para a próxima rodada. |

---

## 7. Sobre o período

**3 anos bastam para a curva** — três janelas móveis de 12 meses, sazonalidade neutralizada.
**Para o histórico de lançamentos precisei de 2021 em diante**, e foi isso que revelou a queda de
28% para 0,7% na taxa de acerto. Com 3 anos eu concluiria que 3% é o normal da casa. Sugiro manter
2021 como marco nessa métrica.

---

## 8. Fase 2 — o que preciso de você

**Bloqueantes:**

1. **Qual corte vale como oficial?** Entreguei os dois. Minha recomendação: **corte B (mercado limpo)
   para tendência e seleção de produto; corte A (tabela padrão) para precificação e margem-teto.**
   Se você quiser a padrão como número oficial de curva, eu uso — mas registro que ela mede migração
   de tabela junto com demanda, e o Clube Nitron e Extrema distorcem o último ciclo.
2. **Escopo inclui private label?** A carteira acima é marca Nitron para atacado e varejo UD. Se OEM
   entra, a lógica é outra: valida-se com o cliente, não com raspagem.
3. **Teto de CAPEX e tonelagem disponível.** Separa "cor nova em molde existente" (os 8 certeiros)
   de "molde novo". Vi `AD_TONELAGEMMIN/MAX` no cadastro e a view `VW_MAQUINA_CAPACIDADE` —
   **consigo levantar a capacidade ociosa por faixa de tonelagem se você autorizar.**
4. **Meta do projeto:** faturamento incremental, margem, ou redução de SKU count?

**Para calibrar a raspagem:**

5. **Concorrentes:** Sanremo, Plasútil, Coza/OU, Martiplast, Arthi, Paramount, Vintage, Casambiente,
   Tramontina utilidades. Confirma, corta, adiciona? Inclui importado?
6. **Canais:** Mercado Livre, Amazon BR, Shopee, Magalu + Havan e Casas Bahia. Prioriza algum?
7. **Calendário de lançamento** e **se o pigmento chumbo/grafite está homologado** — se estiver,
   5 dos 8 certeiros são executáveis quase imediatamente.

**A escolha que quero deixar explícita:** os 8 certeiros são todos extensão de molde existente, de
propósito. Com 0,7% de acerto na safra 2025, reconstruir a pontaria vem antes de gastar em
ferramentaria. Se você esperava produtos genuinamente novos, eu reordeno para uma carteira mais
agressiva — mas quero que essa troca de risco seja decisão sua.

---

## 9. Auditoria do vetor cor — "só o chumbo performou bem mesmo?"

Pergunta justa: eu apoiei o vetor chumbo em **2 SKUs**. Testei todas as cores do portfólio.
A resposta é **sim e não**.

### Sim: chumbo e laranja foram as únicas duas cores que cresceram

| Cor | SKUs | 23/24 | 24/25 | 25/26 | Ganho abs. | Var | R$/SKU |
|---|---|---|---|---|---|---|---|
| **CHUMBO** | 44 | — | 1,33 M | **2,57 M** | **+1,24 M** | **+93,1%** | 58 k |
| **LARANJA** | 3 | 0,48 M | 0,38 M | **0,70 M** | **+0,31 M** | **+81,7%** | **233 k** |
| Transparente | 118 | 9,65 M | 11,02 M | 10,31 M | −0,71 M | −6,4% | 87 k |
| Areia/bege | 6 | 1,69 M | 1,38 M | 1,25 M | −0,14 M | −9,9% | 208 k |
| Branco | 284 | 24,18 M | 25,01 M | 21,83 M | −3,19 M | −12,7% | 77 k |
| Preto | 254 | 28,65 M | 30,61 M | 26,09 M | −4,52 M | −14,8% | 103 k |
| Sortido | 19 | 0,82 M | 0,62 M | 0,51 M | −0,11 M | −17,0% | 27 k |
| Fumê | 8 | 0,84 M | 0,76 M | 0,59 M | −0,17 M | −22,8% | 74 k |
| Vermelho | 77 | 4,34 M | 2,84 M | 2,14 M | −0,70 M | −24,5% | 28 k |
| Rosa | 98 | 2,80 M | 2,18 M | 1,36 M | −0,83 M | −37,8% | 14 k |
| Azul | 21 | 1,23 M | 0,58 M | 0,29 M | −0,30 M | −50,7% | 14 k |
| Amarelo | 4 | 0,09 M | 0,02 M | 0,01 M | −0,01 M | −64,4% | 1,6 k |
| Verde | 102 | 3,65 M | 0,88 M | 0,16 M | −0,72 M | **−81,7%** | 1,6 k |
| Marrom/terracota | 34 | 2,45 M | 0,78 M | 0,08 M | −0,70 M | **−89,9%** | 2,3 k |
| Cinza/grafite | 19 | 0,90 M | 0,41 M | 0,03 M | −0,38 M | **−92,7%** | 1,6 k |

### Não: eu exagerei o chumbo de três maneiras

**1. Não são 2 SKUs — são 44. O rollout já aconteceu.**
Chumbo está em 12 SKUs de Lixeiras, 13 de Organização, 12 de Cozinha, 3 de Banheiro e 1 de Limpeza.
Foram cadastrados em bloco (CODPROD 11806–12072), na safra 2024/2025.

**2. Parte do "+93%" é renomeação, não demanda nova.**
Os SKUs "CINZA" antigos foram substituídos por SKUs "CHUMBO" novos, par a par — e "LISO" virou "FLAT":

| Antigo (cinza) | 23/24 → 25/26 | Novo (chumbo) | 24/25 → 25/26 |
|---|---|---|---|
| Organizador Multiuso Rattan CINZA | 91 k → 3,5 k | Organizador Multiuso 3 div CHUMBO | 68 k → 93 k |
| Organizador Rattan 6 div CINZA | 86 k → 3,3 k | Organizador Multiuso 6 div CHUMBO | 58 k → 77 k |
| Cesto Organizador Rattan G CINZA | 149 k → 3,0 k | Caixa Organizadora Rattan CHUMBO 16L | 50 k → 81 k |
| Porta Escova LISO CINZA | 12 k → 0,8 k | Porta Escova FLAT CHUMBO | 23 k → 32 k |
| Porta Sabão Líquido LISO CINZA | 20 k → 0 | Porta Sabão Líquido FLAT CHUMBO | 31 k → 29 k |

Cinza perdeu R$ 868 k enquanto chumbo ganhou R$ 2,57 M. **O ganho líquido da família cinza+chumbo é
de +R$ 1,70 M (+189%)** — ainda excelente, mas não os +R$ 2,57 M que o número do chumbo sozinho sugere.

**3. Um SKU é 45% do crescimento.** A Lixeira Rattan c/ Pedal chumbo 6L faz R$ 554 k dos R$ 2,57 M.
A média dos 44 SKUs chumbo é **R$ 58 k** — 36 deles estão abaixo de R$ 100 k. É o mesmo padrão de
cauda longa que eu critiquei na seção 2. O rollout de chumbo produziu **um acerto e 43 produtos pequenos.**

### O que eu não tinha visto e é mais importante

**O portfólio está consolidando numa paleta neutra, e o lado colorido está morrendo.**

Preto + branco + transparente + chumbo = **R$ 60,8 M dos R$ 83,1 M (73%)**. E as quedas mais fundas
são todas do lado colorido: marrom −90%, verde −82%, amarelo −64%, azul −51%, rosa −38%, vermelho −25%.

Isso muda a diretriz: **não é "lançar chumbo", é "parar de lançar cor".** Chumbo é o único entrante
novo no conjunto neutro. E laranja sobrevive porque **não é cor decorativa, é sinalização funcional**
(Nitronfort = ferramenta) — com **R$ 233 k por SKU, é a cor mais produtiva do portfólio, 4× o chumbo.**

### Onde o chumbo ainda não chegou

| Linha | SKUs chumbo | Status |
|---|---|---|
| Lixeiras | 12 | coberta |
| Organização | 13 | coberta — **falta gaveteiro** |
| Cozinha | 12 | coberta |
| Banheiro | 3 (só os Flat) | **falta o Porta Escovas c/ Tampa** (o SKU de R$ 536 k) |
| Limpeza | 1 | **falta Porta Vassouras e Porta Sabão em Pó** |
| **Frasqueiras** | **0** | **vazia — e é a única linha em crescimento** |
| Potes, Jarras, Micro-ondas, Decor Util, Geladeira | 0 | vazias |

---

## 10. Capacidade das injetoras

### O parque

**56 injetoras na Nitron-Fábrica** e 10 na Tanamu:

| Faixa | Máquinas | Detalhe |
|---|---|---|
| ≤ 260 t (pequenas) | 15 | 80t(2) 130t(2) 160t(2) 200t(3) 250t(3) 258t(2) 260t(1) |
| 261–1.100 t (médias) | 6 | 398t(1) 600t(1) 650t(2) 800t(1) 1.100t(1) |
| 1.101–2.000 t (grandes) | 23 | 1.200t(5) 1.600t(6) 2.000t(12) |
| > 2.000 t (XL) | 12 | 2.500t(6) 2.800t(1) 3.000t(1) 3.800t(3) 6.000t(1) |

### A ocupação — e é aqui que a carteira se ranqueia

| Faixa | Cadastradas | Com apontamento | **Paradas** | Ocupação 24/7 |
|---|---|---|---|---|
| ≤ 260 t | 15 | 8 | **7** | **56,9%** |
| 261–1.100 t | 6 | 1 | **5** | 76,4% |
| 1.101–2.000 t | 23 | 23 | 0 | 73,5% |
| > 2.000 t | 12 | 12 | 0 | 72,7% |

**A folga está toda nas máquinas pequenas e médias: 12 injetoras sem um único apontamento no ano,**
e as pequenas em uso rodam a 57% contra 73% das grandes. As grandes e XL estão com o parque inteiro
em uso.

Ressalvas de método: as horas vêm de `DHTERMINOPRODUCAO − DHPRODUCAO` no apontamento, o que pode
incluir tempo morto dentro da ordem — então a ocupação real é provavelmente **menor** que a tabela.
E a base é 24/7 (8.760 h/ano); se a fábrica não roda três turnos em todas as faixas, os percentuais
sobem proporcionalmente. A comparação **entre** faixas e o fato de 12 máquinas não terem apontamento
nenhum são robustos independentemente disso.

### O que isso faz com a carteira

- **Família "Fácil" (Coxinha, Pastel) → melhor viabilidade real do projeto.** Decor Util aponta
  **100% das suas horas em máquina ≤260 t**, exatamente a faixa com 7 máquinas paradas e 57% de
  ocupação. É a linha de 81,5% de margem rodando na faixa mais ociosa da fábrica.
- **Frasqueiras** → tamanhos de 1,4L a 12L devem cair entre pequenas e médias, onde estão as 12
  máquinas paradas. Segunda melhor viabilidade.
- **Caixas organizadoras 16L, lixeiras grandes, Nitronbox** → 1.101 t+, onde **não há máquina livre**.
  Um lançamento aqui desloca produção existente, não adiciona.

### A lacuna de dado que preciso reportar

Prometi ranquear todos os candidatos por tonelagem. **Não consigo com os dados atuais**, porque o
cadastro está vazio:

| Campo | Preenchido |
|---|---|
| `TGFPRO.AD_TONELAGEMMIN/MAX` | **10 de 4.252** produtos |
| `TGFPRO.AD_QTDCAVIDADE` | 52 de 4.252 |
| `TGFPRO.AD_CODCORPROD` | **0** |
| `AD_FICHATECNICA` (ciclo, cavidades, molde, injetora) | **4 linhas** |
| `AD_INJETORAFICHA` | 1 linha |
| `TPRCPR` (roteiro) | 0 linhas |

O apontamento real (`AD_APONTACICLO`, 37 mil registros) tem produto, máquina, ciclo e até cor — mas
**99,7% dos apontamentos são em Produto Intermediário (PI)**, e não achei a estrutura PA→PI numa
view direta. É por isso que consegui ocupação por faixa mas não tonelagem por produto acabado.

Duas saídas, e é decisão sua qual seguir:
1. **Me indicar onde está a estrutura PA→PI** (nome da tabela ou view) — daí eu fecho o ranking completo.
2. **Preencher a ficha técnica** dos ~35 candidatos da carteira (molde, cavidades, ciclo, injetora).
   São 35 fichas, não 4.252 — dá para fazer manualmente e resolve o planejamento de capacidade do projeto.

---

## 11. [CORRIGIDO] Dois certeiros da revisão 2 estavam errados

A auditoria de cor mostrou que **eu propus lançar produtos que já existem**. As correções:

### Organização — o certeiro anterior já existe
❌ *"Caixa Organizadora Rattan c/ Tampa em CHUMBO (4L e 16L)"* — **já existe em 2L, 4L, 8L e 16L**
(R$ 35 k, 64 k, 89 k e 81 k, crescendo 44% a 96%).

⭐ **NOVO CERTEIRO — Gaveteiro em CHUMBO (4 gavetas e Modular Rattan 8,2L)**
É o **único buraco de chumbo na linha**: 13 SKUs chumbo em Organização e nenhum gaveteiro. E gaveteiro
é justamente o subgrupo que cresce — 4 gavetas preta R$ 753 k (+22%), branca R$ 471 k (+22%), rosa
+110%, Modular transparente R$ 390 k (+29%). Molde existe, cor comprovada, gap claro.

### Lixeiras — o certeiro anterior já existe
❌ *"Lixeira Basculante Rattan CHUMBO 4,5L"* — **já existe** (R$ 141 k, +67%, 329 clientes).

⭐ **NOVO CERTEIRO — Lixeira Rattan c/ Pedal CHUMBO nos volumes que faltam (12L e acima)**
O Rattan c/ Pedal chumbo **6L é o maior sucesso de chumbo da casa**: R$ 554 k e 711 clientes partindo
de zero. Mas a família só tem chumbo no 6L — o 12L chumbo existe em Juta e em Vime, não em Rattan.
Mesma família, mesmo padrão de sucesso, gap explícito. **Ressalva:** lixeira grande roda em máquina
1.101 t+, onde não há folga — então este certeiro compete por capacidade ocupada.

### Os outros seis se mantêm — e três ficam mais fortes
- **Frasqueiras** (chumbo 2,8L e 6,2L): a linha tem **zero SKUs chumbo**, é a única em crescimento,
  e roda em faixa com máquina parada. **Passa a ser o certeiro nº 1 do projeto.**
- **Decor Util** (Coxinha & Pastel Fácil): 81,5% de margem e 100% das horas na faixa mais ociosa.
  **Certeiro nº 2.**
- **Limpeza** (Porta Vassouras chumbo): confirmado que não existe. Mantido.
- **Banheiro** (Kit 3 peças): o Porta Escovas c/ Tampa chumbo também não existe — vale somar ao kit.
- **Cozinha** (Flat 3 peças): o chumbo do 2 peças já existe (R$ 107 k, 434 clientes); o **3 peças** não.
  Mantido no 3 peças.
- **Potes** (Kit Mantimentos acoplado c/ rosca): nunca dependeu de cor. Mantido.
