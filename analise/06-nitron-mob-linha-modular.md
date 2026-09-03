# Nitron Mob — a gramática modular e a entrada da CRUZETA

Levantado em 02/09/2026 a partir de 5 STLs (Trizeta 01/02, Cruzeta, Peça L, Porta-haste)
cruzados com a estrutura real no Sankhya. A tampinha ainda não foi enviada.

---

## 1. A linha existe, mas praticamente não vendeu

Grupo `1001901` "Nitron Mob" (pai: "Linha Mob"), **14 PAs**, `CODPROD` 14170–14183.

| Recorte | Valor |
|---|---|
| Faturamento total da linha | **R$ 2.290,60** |
| PAs que faturaram | 11 de 14 |
| Clientes | **1** |
| Notas | 20/08/2026 e 24/08/2026 |
| Nunca faturaram | 850 Arara · 853 Kit Suporte (M) · 854 Kit Suporte (G) |

Recorte padrão do `CLAUDE.md` (`CODEMP IN (1,2,14)`, `STATUSNOTA='L'`, `TIPMOV IN ('V','D')`,
`TOP.ATUALFIN<>0`, exclusão dos `CODTIPOPER` de transferência).

**Preço praticado = 0,670 × `CUSGER` em todas as 11 PAs**, com a constante idêntica até a
terceira casa. A tabela padrão (`CODTAB=0`) tem piso **exatamente em 2,00 × `CUSGER`**.
Logo o custo é confiável e as notas de agosto foram **venda piloto a 33% abaixo do custo** —
não é problema de tabela, é amostra faturada.

> Consequência para o projeto: não existe curva para extrapolar. Qualquer projeção da linha
> modular é aposta, não leitura de demanda.

---

## 2. Nitron Mob não é um produto de plástico

O NCM das PAs é **9403.60.00 (móveis de madeira)**. A estrutura é **pinus comprado da
BRASPINE MADEIRAS LTDA** — 19 PIs de barra de seção **15,3 × 26,6 mm** em 19 comprimentos,
mais painéis de 15 mm. Densidade medida idêntica em barras e painéis: **0,556 g/cm³**.

O plástico injetado são **só 5 conectores**, e eles são de **5,6% a 21,7% do custo da PA**:

| PA | `CUSGER` | conectores PP | % do custo |
|---|---|---|---|
| 850 Arara | R$ 90,10 | R$ 7,46 | 8,3% |
| 851 Sapateira Peq. | R$ 32,01 | R$ 6,94 | **21,7%** |
| 852 Sapateira Gde. | R$ 74,84 | R$ 4,18 | **5,6%** |
| 855 Prateleira G 2P | R$ 57,18 | R$ 4,88 | 8,5% |
| 856 Prateleira G 3P | R$ 84,16 | R$ 7,30 | 8,7% |
| 857 Prateleira G 4P | R$ 109,12 | R$ 9,73 | 8,9% |

O resto é madeira de terceiro + corte + montagem. **A Nitron entra aqui como montadora, não
como injetora.** Isso precisa ser decidido explicitamente, não por inércia.

---

## 3. As 5 peças, casadas ao PI por custo

O cadastro chama todos os PIs de "MOLDE DA …", mas o `CODPROD` é a **peça**, não a ferramenta.
Casamento feito pelo volume da malha (todas as 5 fechadas, **0 arestas não-manifold**) contra
o custo cadastrado — o R$/kg implícito fecha entre R$ 8,53 e R$ 9,38, coerente com blend
PP moído + virgem clarificado.

| Peça | PI | Vias | bbox (mm) | Volume | Massa PP | Custo | R$/kg | Máquina |
|---|---|---|---|---|---|---|---|---|
| Trizeta (esq/dir) | `850-TZ` 14811 | **3 ortogonais** | 61,61 × 83,23 × 73,08 | 48,96 cm³ | 44,3 g | R$ 0,3875 | 8,74 | INJ 8 |
| **Cruzeta** | `850-CZ` 14814 | **4 (T + vertical)** | 101,30 × 83,23 × 73,08 | 62,57 cm³ | 56,6 g | ~R$ 0,495 est. | — | **nenhuma** |
| Peça L | `850-L` 14812 | 2 coplanares | 21,92 × 83,23 × 73,08 | 35,36 cm³ | 32,0 g | R$ 0,3003 | 9,38 | INJ 9 |
| Porta-haste | `850-H` 14815 | clipe em C | 42,22 × 34,51 × 21,92 | 11,29 cm³ | 10,2 g | R$ 0,0872 | 8,53 | INJ 11 |
| Tampa | `850-T` 14813 | tampão | *STL pendente* | ~1,2 cm³ | ~1,1 g | R$ 0,0097 | — | INJ 45 |

- **Trizeta 01 e 02 são o par espelhado em Z** — 3.204 dos 3.238 vértices coincidem sob
  espelhamento em Z. Confirma o "ESQ/DIR" da descrição.
- **A cruzeta nunca foi produzida**: zero registro em `AD_APONTACICLO`. As outras 4 rodaram
  1 ciclo cada, em injetoras de 120–160 t (`AD_TONELAGEMMIN/MAX` = 120 nas cinco).
- Faixa ≤260 t é a mais ociosa do parque (56,9%, 7 de 15 máquinas paradas). Capacidade de
  injeção **não é o gargalo** — mas ver lição nº 4 do `CLAUDE.md`.

---

## 4. A interface de junta (medida, não estimada)

| Grandeza | Valor | Como foi obtido |
|---|---|---|
| Seção da barra | **15,3 × 26,6 mm** | descrição dos 19 PIs, confirmada pela cavidade (~15,7 × 27,0) |
| Folga do encaixe | **~0,4 mm** | cavidade medida − seção da barra |
| Profundidade do encaixe | **40,60 mm** | face +Y da Peça L, mediana sobre 1.666 raios |
| Parede do conector | **2,95 mm** | faces planas paralelas em X |
| Passo vertical do nó | **73,08 mm** | Trizeta 02 assenta exatamente sobre a 01 (Z 230,37) |

⚠️ **O nó não é cúbico** (61,61 × 83,23 × 73,08). O incremento que ele soma à dimensão
externa depende do eixo. Para o configurador, a grade tem de ser definida em
**centro-a-centro de nó**, não em dimensão externa — senão a matemática não fecha nos três eixos.

---

## 5. A gramática de montagem — fecha em todas as 9 prateleiras

Decodificada da estrutura e verificada peça por peça:

**Por nível de prateleira**
- 4 × trizeta (os cantos)
- 2 × barra de comprimento `PSC` → **define a LARGURA**
- 2 × barra de largura `BLA-03-AC` (287 mm) → **define a PROFUNDIDADE**
- 5 × travessa `PST`/`BPS` → as réguas do tampo
- 10 × porta-haste → **2 clipes por régua**

**Por coluna, entre níveis:** 1 × barra de altura (`PSA` ou `BAL-02-AC`)
**Uma vez por móvel:** 4 × pé (`BPE-01-AC` 60 mm) + 4 × tampa

Conferência na 855 (Prateleira G 2P): trizeta 8 = 4×2 níveis ✓ · `BLA-03-AC` 4 = 2×2 ✓ ·
`PSC-03` 4 = 2×2 ✓ · `PST-02` 10 = 5×2 ✓ · porta-haste 20 = 10×2 ✓ · pé 4 ✓ · tampa 4 ✓.

**Regra observada, exata em 3 de 3 pares:** `travessa = comprimento + 22 mm`
(315→337 · 415→437 · 595→617).

---

## 6. As 3 larguras já existem — e não são as três que você citou

Você pediu para fixar 3 larguras a partir de 850 (arara), 851 (sapateira) e 852.
Duas correções do dado:

1. **`852.004.N03` é `SAPATEIRA GRANDE`, não prateleira.** As prateleiras são
   `855` a `863` (Multiuso P/M/G × 2P/3P/4P). Provável origem da confusão: a 852 é a
   **única PA da linha com painel** (`PAN-01-AC` 435 × 200 × 15).
2. **850, 851 e 852 têm todas a MESMA largura.** As três usam `PSC-02` = 415 mm e
   `PST-01` = 437 mm. Tirar 3 larguras delas devolveria **uma**, não três.

As 3 larguras reais da linha estão nas prateleiras, no nível de matéria-prima
(`USOPRODMP='M'`, por isso não aparecem na view PA→PI):

| Tamanho | Barra de comprimento | Travessa | Profundidade |
|---|---|---|---|
| **P** | `PSC-01` **315 mm** | `BPS-01` 337 | `BLA-03-AC` 287 |
| **M** | `PSC-02` **415 mm** | `PST-01` 437 | `BLA-03-AC` 287 |
| **G** | `PSC-03` **595 mm** | `PST-02` 617 | `BLA-03-AC` 287 |

**A profundidade já é única (287 mm) nas 9 prateleiras.** E P/M/G é largura, não altura —
a altura é modulada pela barra vertical: 2P = 1 × `PSA-03` 424 por coluna ·
3P = 2 × `PSA-02` 346 · 4P = 3 × `BAL-02-AC` 270.

### Recomendação: fixar 315 / 415 / 595 e não criar barra nova

Os três comprimentos **já estão cadastrados, já foram comprados da Braspine e já estão em
BOM ativa**. Fixá-los custa zero SKU novo. Criar uma escala nova de larguras significaria
2 a 3 SKUs de barra a mais e 2 a 3 linhas de corte a mais.

E vale aqui a mesma aritmética da lição de 2022 do `CLAUDE.md`: estoque de segurança é
proporcional ao desvio, não à demanda. Partir a demanda em N comprimentos de barra derruba a
demanda por SKU para 1/N mas o desvio só para 1/√N — **3 comprimentos = +73% de estoque de
segurança para vender o mesmo tanto**, e ruptura subindo junto.

**Para larguras maiores, o caminho é a cruzeta, não uma barra mais longa.**

---

## 7. O que a cruzeta muda, exatamente

- **Peça L** = 2 vias coplanares → cotovelo. Termina o vão.
- **Trizeta** = 3 vias ortogonais → canto de caixa. Também **termina** o vão.
- **Cruzeta** = 4 vias (T no plano + vertical) → **atravessa** o vão.

Hoje, com trizeta e L, todo móvel da linha é **uma caixa fechada**: a corrida de barra sempre
morre no canto. A cruzeta é o nó de **meio de vão** — é ela que permite dois módulos
compartilharem um montante.

Num nível de 2 vãos: em vez de 4 + 4 = 8 trizetas e 8 montantes, usa-se
**4 trizetas + 2 cruzetas**, com 2 montantes a menos. É daí que sai o "alongar, prolongar e
modular" — e é por isso que a largura comercial deve vir de **N vãos**, não de barra maior:

| Configuração | Nós por nível | Largura |
|---|---|---|
| 1 vão | 4 trizetas | 1 × barra |
| 2 vãos | 4 trizetas + 2 cruzetas | 2 × barra + 1 nó |
| 3 vãos | 4 trizetas + 4 cruzetas | 3 × barra + 2 nós |

Com `PSC-03` (595) em 2 vãos chega-se à ordem de **1,2 m** — a faixa de módulo de gôndola de
PDV. Sem barra nova.

---

## 8. Divergências de cadastro encontradas (todas verificáveis)

Detalhe em `dados/14-nitron-mob-divergencias-cadastro.csv`.

**Peso das barras — 3 itens com erro de exatamente 10×.** Das 12 barras conferidas, 10 fecham
com fator 1,00 contra a seção 15,3 × 26,6 a 0,556 g/cm³ (0,22628 g/mm, r²=1,0). Três não:

| Item | `PESOLIQ` | Correto | Onde entra |
|---|---|---|---|
| `BLA-03-AC` 15862 | 0,64941 kg | **0,06494 kg** | **todas as 9 prateleiras** |
| `BAL-02-AC` 15847 | 0,61093 kg | **0,06110 kg** | as três 4P |
| `BCO-01` 15850 | 0,81915 kg | **0,08191 kg** | Kit Suporte (M) |

**Peso e dimensão das 14 PAs são o mesmo valor copiado**: `PESOLIQ` 0,525 kg e
1,2 × 21 × 39,5 nas quatorze. O peso real recalculado da BOM vai de **0,877 kg a 5,140 kg** —
a Arara está **9,8× subdeclarada**. Isso é frete e cubagem.

**Peso dos 5 conectores é 0,022 kg nos cinco**, contra 1,1 g a 56,6 g reais. A tampa está
20× superdeclarada e a cruzeta 2,6× subdeclarada.

**`CUSGER` dos 19 PIs de barra sai entre R$ 14 e R$ 33 MILHÕES por unidade.** A compra da
Braspine (**R$ 84.211,67**, nota 1625091 de 04/06/2026) entrou com `QTDNEG` numa unidade que
não é a peça. Efeito: `VW_COMPOSICAO_NIT` devolve **R$ 236 milhões** de custo para a Arara.
O `CUSGER` das PAs (R$ 32 a R$ 109) não veio por esse caminho e está sadio.

**`854.004.N03` Kit Suporte Decorativo (G) não tem nenhuma linha de estrutura** — ativa,
NCM 44192000 (diferente das outras 13), sem BOM, sem faturamento. Não pode ser produzida
nem custeada.

**`AD_QTDCAVIDADE` da trizeta = 1**, mas o molde é ESQ/DIR e as duas mãos são geometricamente
espelhadas. Além disso a BOM consome um único `CODPROD` para as duas mãos — não há como
planejar tiro por mão.

**Os 19 PIs de barra estão no grupo `8000100` "Diversos" sob "Exportação"** — madeira
classificada em grupo de exportação distorce qualquer relatório por grupo.

---

## 9. Correções ao CLAUDE.md que este levantamento produziu

1. **A estrutura PA→PI existe em view direta.** `VW_PA_PIS_QTD_NIT` e `VW_PA_PIS_ATIVOS_NIT`
   (`CODPRODPA`, `CODPRODPI`, `QTDMISTURA`), e `VW_COMPOSICAO_NIT` / `VW_BOM_EXPLODIDA`
   (`CODPRODPA`, `CODPRODMP`) para descer até a MP. O `CLAUDE.md` registra isso como
   não encontrado.
2. **`VW_COMPOSICAO_NIT` não serve para custo** enquanto o `CUSGER` dos PIs de madeira estiver
   corrompido. Serve para quantidade.
3. **A BOM tem duas camadas e a segunda é fácil de perder.** `VW_PA_PIS_QTD_NIT` mostra só
   `USOPRODMP='2'`; as barras compradas entram com `USOPRODMP='M'` e só aparecem em
   `VW_COMPOSICAO_NIT`. Foi exatamente aí que estavam as 3 larguras P/M/G — ler só a primeira
   camada faz P, M e G parecerem idênticas.
4. **`QTDCAPACIDADEPAD` de `VW_MAQUINA_CAPACIDADE` não é confiável como tonelagem.** As
   injetoras 8, 9 e 11 aparecem com 1600 enquanto `CAPDESCR`/`CODCAP` dizem 160.
   Usar `CAPDESCR`.

---

## 10. O que falta para especificar o configurador

Resolvível com o dado que já temos:
- catálogo de barras: 19 comprimentos já compráveis (`dados/13-…csv`)
- gramática de montagem por nível (seção 5)
- interface de junta (seção 4)

Falta:
- **a tampinha** (`850-T`) — STL não recebido
- **uma medida física** do nó em cada eixo, para fechar dimensão externa a partir de
  centro-a-centro (o nó é anisotrópico)
- **qual é a carga admissível por vão** — sem isso não se pode oferecer PDV nem hack de TV
- **o desenho da cruzeta em uso**: ela nunca foi injetada, então não há peça para tryout

---

## 11. Parecer do curador de portfólio — VETO

Rodado em 02/09/2026 com poder de veto, conforme o processo do `CLAUDE.md`.
Nada foi gravado em `pdp_lancamento`.

| Frente | Veredito |
|---|---|
| Molde da cruzeta `850-CZ` | **veta** |
| B2C móveis modulares (hack TV, armário, mesa, escrivaninha) | **veta** |
| Site configurador | **veta** |
| B2B móvel de PDV | **investiga antes** — piloto contra pedido, sem SKU, sem molde |
| Estoque Braspine parado | decisão de liquidação, separada da de lançar |

### O achado que derruba a frente B2C

A função que a linha quer atacar **já é vendida pela Nitron, em plástico, para milhares de
clientes**:

| CODPROD | Produto | Ref | Clientes | Faturamento vida |
|---|---|---|---|---|
| 3307 | Porta Shampoo e Prateleira Madri Preto | `079.012.003` | **3.866** | R$ 1.666.356 |
| 3306 | Porta Shampoo e Prateleira Madri Branco | `079.012.002` | **3.881** | R$ 1.626.178 |
| 434 | Prateleira Multi Uso 4 Andares Preta | `053.004.003` | **1.556** | R$ 1.105.280 |
| 3108 | Prateleira Multi Uso 4 Andares Branca | `053.004.002` | **1.513** | R$ 972.851 |
| 236 | Prateleira Multi Uso 4 Andares | `053` | 688 | R$ 596.361 |

Família `053` ≈ **R$ 2,70 M** · família `079` ≈ **R$ 3,3 M**, tudo injetado.
Contra isso, a Nitron Mob tem **9 SKUs literalmente chamados "PRATELEIRA MULTIUSO"** que
somam R$ 1.904 com 1 cliente. Mesma função, mesmo nome, material comprado de terceiro,
margem negativa.

E "mesa" já está no catálogo: `11369` Tampo de Mesa em Teca 2500×800×18 (`631.010.M00`) e
`11370` 1000×1500×18 (`633.020.M00`), cadastrados desde 2025, **faturamento zero, nenhuma nota**.

### A história comercial completa é menor do que o recorte padrão mostra

O recorte padrão pega R$ 2.290,60. Fora dele há mais:

| Parceiro | CODTIPOPER | Tabela | Valor |
|---|---|---|---|
| Visual Comercio de Embalagens (53828) | 3218 Venda Clientes Especiais | 165 | R$ 2.290,60 |
| Visual Comercio de Embalagens (53828) | **3211 Amostra** | 165 | R$ 516,26 |
| Viccomex Trade Solutions (971) | **3220 Bonificação Especial** | 0 | R$ 1.340,04 |

**Vida inteira da linha: R$ 4.146,90, 2 parceiros, zero venda de canal.** Um é "cliente
especial", os outros dois lançamentos são amostra e bonificação.

### A margem realizada

| | |
|---|---|
| Receita (44 un) | R$ 2.290,60 |
| CPV (Σ qtd × `CUSGER`) | R$ 3.418,84 |
| **Prejuízo bruto** | **−R$ 1.128,24** |
| **MB realizada** | **−49,3%** |

Pior SKU: `14182` Prateleira G 4P, **−R$ 36,01 por unidade**.

### Por que o payback da cruzeta não fecha

O molde de plástico não gera a margem do móvel — gera a margem da **injeção de R$ 0,39/peça**.
Com 8 a 16 cruzetas por móvel, a contribuição de injeção é da ordem de **R$ 2 a 6 por móvel**.
Um molde de 2 cavidades precisaria de **milhares de móveis/ano**. A linha vendeu 44 unidades
na vida. E o custo do molde **não existe no ERP**: `14814` tem zero linhas em `TGFITE` e em
`TGFCUS` — numerador desconhecido, denominador negativo.

Creditar ao molde a margem cheia do móvel (2,00 × `CUSGER`) é creditar ao plástico a margem da
**madeira de terceiro**. É o tipo de conta que produziu 3,4% de acerto em 2024.

### Madeira não escala nesta casa

Linha Teca, 12 M contra os 12 M anteriores:

| Grupo | 12 M | 12 M ant. | Δ | Clientes |
|---|---|---|---|---|
| 1001802 Teca Organização | R$ 775.194 | R$ 766.275 | +1,2% | 309 |
| 1001801 Teca Tábuas | R$ 372.504 | R$ 400.906 | **−7,1%** | 213 |
| 1001803 Teca Cozinha | R$ 204.418 | R$ 229.972 | **−11,1%** | 194 |
| 1001804 Teca Petisqueira | R$ 35.980 | R$ 109.520 | **−67,1%** | 112 |
| 1001901 Nitron Mob | R$ 2.291 | R$ 0 | — | **1** |

**R$ 1,388 M = 1,7% dos R$ 83,1 M**, caindo em 3 dos 4 grupos. Somado à lição nº 8 já
documentada (tampa plástica R$ 492.548 contra tampa teca R$ 16.192 no mesmo corpo, 30× de
diferença), a evidência interna sobre madeira aponta contra a proposta.

### O espaço de PDV não está vazio — está ocupado por aço

A própria Nitron **compra** gôndola: `13238` Gôndola Ponta 170 40×30 a **R$ 414/un** e `13239`
Gôndola Centro 40×30 a **R$ 677/un**, 8 unidades de cada, Balanças Bonsucesso, 12/08/2025.
Um módulo em pinus 15,3 × 26,6 unido por conector de R$ 0,39 tem de ser mais barato que isso
**e** aguentar carga de loja.

Isso também é o argumento a favor do único caminho que o curador deixa aberto: **o primeiro
cliente de PDV pode ser a própria Nitron**, e o teste custa uma amostra e uma medição de carga.

### O risco que nenhum business case conta

A Nitron entrega **8,3% a 8,7% do valor** do produto; ~91% são do fornecedor de madeira e da
mão de obra de montagem. Isso é desverticalização, não verticalização. E o risco de
contaminação não é químico, é **de fluxo**: pó de madeira no ambiente do moinho e dos silos
ameaça o ciclo de moído de **R$ 2,63 M/ano**. Não foi medido — e é o teste que precisa vir
antes do molde: o setor de montagem compartilha ar, piso ou fluxo de refugo com o moinho?

### O que mudaria o veredito, do mais barato ao mais caro

1. **Preço.** Uma venda a **≥ 2,00 × `CUSGER` para ≥ 3 clientes distintos**, sem `CODTIPOPER`
   3211 (amostra) nem 3220 (bonificação). Enquanto o único preço da história for 0,670 ×
   `CUSGER`, nada mais importa.
2. **Diagnosticar a `053`.** Por que a prateleira de plástico, com 3.069 clientes somados e
   R$ 2,7 M, não é a resposta para a demanda que a Nitron Mob quer atender? Custa zero molde.
3. **Corrigir o cadastro** de `14811`–`14815` e o NCM de `14183`.
4. **Custo do molde da cruzeta**: nota ou orçamento formal, com valor, prazo e cavidades.
5. **Volume/ano com nome de cliente** para o móvel que consome cruzeta.
6. **Carga estrutural** do conector em prateleira de gôndola carregada (`engenheiro-molde`).
7. **Receita por m³** do móvel contra a do pote.
8. **Contaminação de fluxo** entre montagem de madeira e moinho.
9. **Saldo Braspine hoje**: R$ 84.211,67 comprados em 04/06/2026 contra ~R$ 3,1 k consumidos.
   Decidir isso **separado** da decisão de lançar — senão o estoque parado vira o argumento
   para lançar, exatamente como a capacidade ociosa (lição nº 4).

### Correção adicional ao CLAUDE.md, vinda do curador

**`QTDCAPACIDADEPAD` é kN, não tonelada.** WCP 8/9/11 = 1600 com `CAPDESCR` "160";
1600 kN ≈ 163 tf. O campo de tonelagem é **`CAPDESCR`**.
⚠️ Isso levanta a suspeita de que **as faixas de ocupação documentadas no `CLAUDE.md`
(≤260 t, 261–1.100 t, 1.101–2.000 t, >2.000 t) estejam lendo kN como tonelada** — o parque da
Nitron não tem injetora de 2.000 t. As faixas precisam ser refeitas antes de serem usadas de
novo. (O WCP 45, 258 com `CAPDESCR` 120, não fecha na mesma conversão — então a hipótese vale
como suspeita a verificar, não como conclusão.)

### Divergência de cadastro nº 14

Os cinco PIs `14811`–`14815` estão com **`NCM` 39241000** (artigo plástico de uso doméstico) e
`CODGRUPOPROD` 2000000 e descrição "MOLDE DA…", enquanto são consumidos como peça
(`QTDMISTURA` de 2 a 40 por PA, `CONTROLEPI='CINZA'`). O NCM confirma que são peça; a descrição
e o grupo dizem ferramenta. Quatro campos em desacordo numa linha com duas semanas de vida.
