# Piloto B2B de PDV — especificação

Rota liberada pelo curador com duas condições: **contra pedido, sem SKU no catálogo** e
**sem molde novo**. A cruzeta fica fora — ela nunca foi injetada e o custo do molde não existe
no ERP. O piloto roda com os 4 conectores que já rodaram.

---

## 1. O canal já existe, e não é o que a proposta imaginava

A busca por expositor em produto acabado de marca própria devolve **um** SKU vivo:

| CODPROD | Produto | Ref | Grupo | Notas | Clientes | Qtd | Faturamento |
|---|---|---|---|---|---|---|---|
| **13998** | Caixa Expositora com 40 kits com 10 cabides — Preto | `010.001.003` | Linha Organização | 11 | **9** | 15 | **R$ 6.239,65** |
| 10123 | Suporte Expositor Teca — Pizza | `900.001.M00` | Teca Organização | 1 | 1 | 6 | R$ 0,06 |
| 10124 | Suporte Expositor Teca — Tábuas | `901.001.M00` | Teca Organização | 2 | 1 | 0 | R$ 0,00 |

De 06/03/2026 a 22/07/2026, preço unitário praticado de **R$ 352,14 a R$ 742,13**,
`CUSGER` R$ 375,03. Compradores externos incluem Eraldo Magazine Central, Himalaia,
Macedo Utilidades e Adriana Pinheiro Moreira, com recompra mensal.

**Em 5 meses esse SKU fez 1,5× tudo que a Nitron Mob fez na vida, com 9× mais clientes.**

E os dois expositores de **teca** estão mortos — R$ 0,06 e R$ 0,00. Mesmo padrão da lição
nº 8: o mesmo conceito em madeira nobre não vende.

### O que o 13998 ensina e o que ele não ensina

O formato que funciona é **display carregado de produto**, não móvel vazio: o cliente compra
400 cabides e o expositor vem com eles.

Mas a BOM do 13998 tem **três linhas**: 400 × Corpo do Cabide (PI 517), 1 etiqueta e a
cartela. **Não existe nenhuma estrutura de expositor na estrutura.** A "caixa expositora"
não tem caixa cadastrada — hoje o display é custo zero na ficha, e a margem é a dos cabides.

Isso corta nos dois sentidos:
- **A favor:** existe canal comprando display a R$ 352–742, e a Nitron não cobra nada pelo
  display hoje. Há espaço de preço.
- **Contra:** trocar caixa de papel por estrutura de pinus + PP **adiciona** custo a um item
  que já vende. O display só se paga se for reutilizável e permanente na loja — ou vendido
  separado.

⚠️ Divergência a registrar: `CUSGER` R$ 375,03 contra R$ 47,56 somados na BOM — gap de 7,9×.
Não construir business case sobre nenhum dos dois antes de reconciliar.

---

## 2. O alvo de preço: o aço que a própria Nitron compra

| CODPROD | Item | Fornecedor | Data | Qtd | Preço unit. |
|---|---|---|---|---|---|
| 13238 | Gôndola Ponta 170 40×30 | Balanças Bonsucesso | 12/08/2025 | 8 | **R$ 414,00** |
| 13239 | Gôndola Centro 40×30 | Balanças Bonsucesso | 12/08/2025 | 8 | **R$ 677,00** |

O "170" é a altura em cm. É esse número que o módulo tem de alcançar para ser comparável.

---

## 3. O módulo do piloto

Não é o empilhamento de dois módulos de 4 prateleiras — esse caminho duplica estrutura e
gera 8 prateleiras com passo de 215 mm, apertado demais para pote e balde. O módulo é
**construído de propósito pela gramática**, com 5 níveis.

| Grandeza | Valor | Origem |
|---|---|---|
| Largura externa | **~680 mm** | `PSC-03` 595 + 85,26 |
| Profundidade externa | **~372 mm** | `BLA-03-AC` 287 + 85,26 |
| Altura | **~1.737 mm** | 5 nós × 73,08 + 4 barras × (424 − 2 × 40,60) |
| Passo entre prateleiras | **~416 mm** | cabe pote, balde e lixeira |
| Prateleiras | 5 | |
| Peso | **8,48 kg** | 7,08 kg pinus + 1,40 kg PP |

Altura contra a gôndola de aço de 1.700 mm: **1.737 mm**. Bate.

### Lista de peças — tudo já cadastrado e já comprado

| Peça | Ref | Qtd | Tipo | O que faz |
|---|---|---|---|---|
| Trizeta | `850-TZ` | **20** | PP injetado | 4 cantos × 5 níveis |
| Porta-haste | `850-H` | **50** | PP injetado | 2 clipes × 5 réguas × 5 níveis |
| Tampa | `850-T` | **4** | PP injetado | fecha o topo dos 4 montantes |
| Barra de comprimento | `PSC-03` 595 | **10** | pinus | 2 × 5 níveis — define a largura |
| Barra de profundidade | `BLA-03-AC` 287 | **10** | pinus | 2 × 5 níveis |
| Travessa / régua | `PST-02` 617 | **25** | pinus | 5 × 5 níveis — o tampo |
| Barra de altura | `PSA-03` 424 | **16** | pinus | 4 colunas × 4 vãos verticais |
| Pé | `BPE-01-AC` 60 | **4** | pinus | |

**Zero peça nova. Zero molde novo. Zero comprimento de barra novo.**
A peça L não entra — ela é cotovelo de 2 vias, e num módulo de gôndola todos os nós são
cantos de 3 vias.

### Custo e preço

| | Valor |
|---|---|
| Conectores de PP | **R$ 12,15** |
| Custo total estimado | **R$ 146,86** |
| A 2,00 × custo (piso da tabela padrão) | **R$ 293,73** |
| Gôndola Ponta 170 de aço | R$ 414,00 |
| **Vantagem a 2× custo** | **−29,1% contra o aço** |
| Vantagem a custo (uso interno) | −64,5% |

O custo de R$ 146,86 é **estimado por escala de massa** sobre a Prateleira G 4P
(`857.004.N03`, `CUSGER` R$ 109,12, fator 1,35) — não é custo apurado. O `CUSGER` real
depende de reconciliar o custo da madeira, que hoje está em ordem de milhões por peça.

Mesmo com essa ressalva, a conclusão aguenta a folga: **a 2× custo o módulo fica 29% abaixo
do aço que a Nitron já compra**, e os conectores são só R$ 12,15 dos R$ 147.

---

## 4. Correção aos pesos publicados

Os pesos que publiquei primeiro saíram da camada de PI apenas, antes de eu encontrar a
segunda camada da BOM (`USOPRODMP='M'`). Com as duas camadas, os pesos reais são maiores e
**o erro de cadastro é pior** do que o registrado:

| PA | Peso publicado | **Peso correto** | Cadastro | Erro real |
|---|---|---|---|---|
| 850 Arara | 5,140 kg | 5,140 kg | 0,525 kg | 9,8× |
| 851 Sapateira Peq | 2,056 kg | 2,056 kg | 0,525 kg | 3,9× |
| 852 Sapateira Gde | 2,739 kg | **3,465 kg** | 0,525 kg | **6,6×** |
| 853 Kit Suporte M | — | **2,849 kg** | 0,525 kg | **5,4×** |
| 855 Prateleira G 2P | 0,877 kg | **3,196 kg** | 0,525 kg | **6,1×** |
| 856 Prateleira G 3P | 1,287 kg | **4,815 kg** | 0,525 kg | **9,2×** |
| 857 Prateleira G 4P | 2,429 kg | **6,298 kg** | 0,525 kg | **12,0×** |
| 858 Prateleira M 2P | — | **2,626 kg** | 0,525 kg | **5,0×** |
| 861 Prateleira P 2P | — | **2,309 kg** | 0,525 kg | **4,4×** |

A linha inteira está subdeclarada entre **3,9× e 12,0×**. Nenhuma das catorze PAs tem peso
utilizável para frete.

---

## 5. O que o piloto testa, em ordem

1. **Carga admissível por vão** — parecer do `engenheiro-molde`. Se o nó de PP com parede de
   2,95 mm e encaixe de 40,60 mm não aguenta 20–40 kg por prateleira sob carga permanente,
   o piloto morre aqui e nada depois importa.
2. **Uma amostra montada**, usando o estoque de pinus da Braspine que já está pago.
3. **A Nitron como primeiro cliente** — substituir uma das gôndolas de aço de R$ 414 no
   próprio showroom ou num cliente que ela já mobilia. Isso testa o produto sem SKU no
   catálogo e sem risco de canibalizar a `053`/`079`.
4. **Preço**: oferecer a ≥ 2,00 × custo para ≥ 3 clientes distintos, sem `CODTIPOPER` 3211
   (amostra) nem 3220 (bonificação). É o item nº 1 da lista do curador e o pré-requisito de
   tudo.
5. Só então discutir molde de cruzeta — com volume/ano e nome de cliente na mão.

## 6. O que este piloto deliberadamente não faz

- **Não cria SKU no catálogo.** Projeto contra pedido.
- **Não usa a cruzeta.** Sem molde novo.
- **Não vai para o B2C.** É onde a canibalização da `053`/`079` acontece.
- **Não é configurador.** O site continua vetado até o item 4 acima passar.
- **Não promete carga** antes do parecer estrutural.

---

## 7. Conferência independente de carga (minha, para checar o parecer do engenheiro)

Cálculo de primeira ordem antes do parecer estrutural, para eu ter base de comparação.
**Premissas explicitadas:** MOE do pinus taeda a ~12% de umidade = 9.000 MPa (faixa de
literatura 8.000–12.000); tensão admissível de flexão em longa duração = 12 MPa
(conservadora); régua simplesmente apoiada com carga uniforme; carga da prateleira dividida
igualmente por 5 réguas. Vão e seção vêm das minhas medições, não de literatura.

### A régua `PST-02` — vão 617 mm, seção 15,3 × 26,6 mm

| Carga/prateleira | Por régua | σ eixo forte | FS | Flecha | σ eixo fraco | FS | Flecha |
|---|---|---|---|---|---|---|---|
| 20 kg | 39,2 N | 1,68 MPa | 7,2× | 0,56 mm (L/1110) | 2,92 MPa | 4,1× | 1,68 mm (L/367) |
| 30 kg | 58,9 N | 2,52 MPa | 4,8× | 0,83 mm (L/740) | 4,37 MPa | 2,7× | 2,52 mm (L/245) |
| **40 kg** | 78,5 N | **3,35 MPa** | **3,6×** | **1,11 mm (L/555)** | **5,83 MPa** | **2,1×** | **3,36 mm (L/184)** |

**A madeira não é o limite.** Mesmo a 40 kg e na orientação fraca sobra 2,1× de folga.
Fica a pergunta de qual orientação a régua realmente assenta — em pé (26,6 mm de altura) ou
deitada (15,3 mm) — porque isso muda a flecha de 1,1 para 3,4 mm.

### O nó trizeta em compressão

Área de parede do encaixe = 2 × (15,7 + 27,0) × 2,95 = **252 mm²**.

| Carga/prateleira | Módulo | Por coluna | σ | FS vs 10 MPa adm. do PP |
|---|---|---|---|---|
| 20 kg | 100 kg | 245 N | 0,97 MPa | 10,3× |
| 30 kg | 150 kg | 368 N | 1,46 MPa | 6,8× |
| **40 kg** | **200 kg** | **490 N** | **1,95 MPa** | **5,1×** |

Também com folga.

### O porta-haste — e aqui está o ponto

Cada régua apoia em 2 clipes, então cada clipe pega **2 a 4 kgf**. Tensão nominal de
**0,30 a 0,61 MPa** sobre ~65 mm² de parede. É baixíssimo.

**Conclusão da conferência:** nenhuma das três frentes falha por ruptura de material.
O que sobra como modo crítico não é resistência, é **rigidez e tempo**:

1. **O "C" do clipe abrir sob carga** — geometria e pré-carga do snap, não tensão.
2. **Creep do PP** relaxando a pré-carga do clipe e assentando a coluna ao longo de meses.
   A 1,95 MPa o PP não rompe, mas escoa: 1–3% de deformação em um ano a temperatura ambiente
   sobre 5 nós de 73 mm dá da ordem de **4 a 11 mm de assentamento** na coluna. Visível,
   não catastrófico — mas é exatamente a família de problema já registrada nas refs
   `176.024.001` e `210.024.001`.

**Nenhum dos dois se resolve por cálculo de tensão.** O ensaio que fecha é físico:
carga permanente de 40 kg/prateleira por 60 a 90 dias, medindo flecha e assentamento da
coluna, mais tentativa de arrancamento do clipe carregado.

⚠️ Isto é conferência de primeira ordem, não substitui o parecer do `engenheiro-molde`.
Serve para eu saber se o parecer dele fecha com a física — e para não aceitar de saída um
número de carga que não tenha ensaio atrás.

---

## 8. O estoque de pinus: onde está, quanto é, e por que não baixou

O `CLAUDE.md` registra que `TGFEST` "não é legível sem mapa de local". Para esta linha o mapa é
simples: **um único local**.

| | |
|---|---|
| Empresa | **1** (Matriz) |
| Local | **1010000 — "Terreo"** |
| Itens com saldo | 19 PIs de barra + 13 itens menores |
| Valor parado | **R$ 84.211,67** |
| Percentual parado | **100% do comprado** |
| Parado desde | **04/06/2026** — três meses |

### Correção de um número que eu publiquei errado

Eu havia reportado a compra da Braspine como **R$ 168.423,34 em 2 notas**. Está errado: são
duas notas do mesmo dia com valor idêntico, e uma delas é o pedido, não a compra.

| NUNOTA | TIPMOV | CODTIPOPER | Operação | Qtd | Valor |
|---|---|---|---|---|---|
| 1625037 | `O` | 2001 | **Pedido Compra Consumo** | 0,000572448 | R$ 13.269,22 |
| 1625091 | `C` | 2101 | **Compra Consumo** | 0,000572448 | R$ 13.269,22 |

*(exemplo do `PST-01`; o padrão se repete nos 19 itens)*

Meu filtro `TIPMOV IN ('C','O','E')` somou o **pedido junto com a nota**. A compra real é
**R$ 84.211,67** — que é exatamente o número que o curador havia apurado. O valor dele estava
certo e o meu não.

### E o pinus não baixou nada

O saldo em `TGFEST` é **exatamente igual à quantidade comprada** nos 19 itens — 50,0% da minha
soma inflada, ou seja, 100% da compra real. **Nenhuma baixa de estoque de pinus foi lançada**,
apesar de a linha ter faturado 44 unidades.

Duas explicações possíveis, e as duas importam:
1. As 44 unidades foram montadas à mão como amostra, sem apontamento de consumo — coerente com
   as notas de amostra e bonificação do §7 do dossiê.
2. O material foi comprado como **"Compra Consumo"** (`CODTIPOPER` 2101), não como
   matéria-prima de estoque. Item de consumo costuma ser apropriado na entrada e não consumido
   via BOM — o que fecha com os 19 PIs estarem no grupo `8000100` "Diversos" sob *Exportação*.

**Consequência prática para o piloto:** os R$ 84.211,67 de pinus estão fisicamente lá e pagos,
então a amostra do piloto sai de estoque existente. Mas **não é possível dizer quantos módulos
saem dele** enquanto a unidade de `QTDNEG` não for corrigida — a quantidade em estoque está na
mesma unidade quebrada da compra, e ela não é a peça. Contar peça de pinus hoje exige contagem
física, não consulta.

Isso torna a correção da unidade um bloqueio do planejamento, não só da contabilidade.

---

## 9. Parecer estrutural do engenheiro-molde, e o corte de seção que ele pediu

O parecer **confirmou minhas quatro contas número por número** (régua 3,35 MPa / FS 3,6× /
flecha 1,11 mm no eixo forte; 5,83 MPa / 2,1× / 3,36 mm no fraco; nó 1,95 MPa / FS 5,1×;
clipe 0,60 MPa). Acrescentou um check que eu não fiz — **flambagem local da parede de
2,95 mm como placa**: σcr ≈ 68 MPa, muito acima de 1,95 MPa, então a parede não flamba antes
de esmagar. Ruptura por compressão está descartada.

E apontou um buraco real no meu cálculo: **eu assumi que a carga desce pela parede em
compressão**, mas o encaixe tem 40,60 mm num nó de 73,08 mm — logo existe estrutura interna
entre o topo e a base que eu não havia medido. Se a carga passasse por uma nervura em flexão,
a tensão real seria muito maior que 1,95 MPa.

Ele pediu corte de seção. **Fiz o corte na malha**, varrendo a área maciça em Z de 0,25 em
0,25 mm.

### O que o corte mostrou

| Elemento | z relativo | Espessura | Área |
|---|---|---|---|
| Parede da base | 0 → 40,0 mm | — | **288 mm²** (mínimo da peça) |
| **Chapa 1** | 40,0 → 42,9 mm | **~2,9 mm** | 1.857 mm² |
| Parede intermediária | 43 → 51 mm | — | ~600 mm² |
| **Chapa 2** | 51,3 → 54,4 mm | **~3,1 mm** | 1.828 mm² |
| Parede superior | 54,5 → 69 mm | — | 728 mm² |
| **Chapa 3 — face de topo** | 70,0 → 72,9 mm | **~2,9 mm** | **3.114 mm²** |

**Parede uniforme de 2,9 a 3,1 mm em toda a peça**, igual à parede externa de 2,95 mm.
Projeto de injeção correto — nenhum ponto maciço, nenhuma nervura grossa.

**Primeiro resultado: minha premissa estava conservadora, não otimista.** A seção vertical
contínua mínima é **288 mm²**, e não os 252 mm² que eu havia estimado pelo perímetro da
parede — 14% a mais. A tensão corrigida a 40 kg/prateleira cai de 1,95 para **1,70 MPa**,
FS de 5,1× para **5,9×**.

**Segundo resultado, e é o que importa: a chapa 1 está em z rel 40,0 mm — exatamente onde o
encaixe de 40,60 mm termina.** Ou seja, **a barra vertical fundo-de-curso apoia numa chapa de
2,9 mm**. A dúvida do engenheiro estava certa, só não no lugar em que ele supôs: não é a
parede, é o fundo do encaixe.

### Três caminhos de carga possíveis, e eles diferem em 100×

| Hipótese | Caminho | σ a 40 kg/prateleira | Veredito |
|---|---|---|---|
| **A** | Parede em compressão, 288 mm² | **1,70 MPa** · FS 5,9× | tranquilo |
| **B** | Barra apoia na chapa 1 em flexão, t = 2,9 mm | **8,5 a 18,4 MPa** | **no limite ou acima dos 10 MPa admissíveis** |
| **C** | Trizeta apoia em trizeta pela chapa 3, 3.114 mm² | **0,16 MPa** | irrelevante |

A faixa da hipótese B vem da condição de borda: **8,5 MPa com bordas engastadas, 18,4 MPa com
bordas apoiadas** (placa 15,7 × 27,0 sob pressão uniforme de 1,16 MPa).

Por carga:

| Carga/prateleira | Hipótese B, bordas apoiadas | Hipótese B, engastadas |
|---|---|---|
| **20 kg** | 9,2 MPa · FS 1,1× | 4,2 MPa · FS 2,4× |
| 30 kg | 13,8 MPa · **acima** | 6,4 MPa · FS 1,6× |
| 40 kg | 18,4 MPa · **acima** | 8,5 MPa · FS 1,2× |

### A evidência aponta para a hipótese C — mas não fecha

As coordenadas de montagem dos STLs favorecem C: **a Trizeta 02 assenta exatamente sobre a
Trizeta 01** (a fronteira é Z = 230,37 nas duas), e a chapa 3 é justamente a face de topo.
Se o par espelhado se apoia chapa-contra-chapa, a coluna descarrega em 3.114 mm² e o
problema desaparece.

Mas isso é leitura de coordenada de exportação, não de peça montada. **Só a montagem física
decide** — e a decisão vale 100× em tensão.

### O número que eu sustentaria hoje

**20 kg por prateleira.** É a única carga que sobrevive à hipótese mais pessimista
(9,2 MPa contra 10 MPa admissíveis, FS 1,1×). Declarar 40 kg exige antes provar que o
caminho de carga é A ou C.

E a FS de 1,1× é fina demais para carga permanente de loja, então mesmo os 20 kg são
**provisórios até o ensaio**, não um número de etiqueta.

### O que o parecer corrigiu na minha leitura de capacidade

Eu havia escrito que capacidade de injeção não é o gargalo, citando a faixa ≤260 t com
56,9% de ocupação. **Está incompleto:**

| WCP | Apontamentos (12 M) | Horas brutas | Ocupação bruta |
|---|---|---|---|
| 8 (trizeta) | 113 | 6.008 h | ~69% |
| 9 (peça L) | 127 | 6.194 h | ~71% |
| 11 (porta-haste) | 125 | 6.055 h | ~69% |
| 45 (tampa) | 68 | 4.777 h | ~55% |

**Estas quatro não são as 7 injetoras paradas da faixa** — são máquinas ativas rodando outra
coisa. A folga da faixa está em *outras* 160 t e 120 t do parque. Em minutos absolutos o
módulo é trivial (15 a 25 min de máquina, ou 2,5 a 4 h/mês a 10 módulos), então o risco não é
"não cabe em horas" — é **inserção na fila de máquina ocupada**, com custo de troca e
prioridade contra a produção regular. É decisão de PCP, não de engenharia.

E `AD_APONTACICLO` **não serve para cycle time**: há um único registro por peça, cobrindo dias
(trizeta com `DHTERMINOPRODUCAO` nulo, tampa 4,1 dias, porta-haste 29 dias). É o intervalo de
abertura e fechamento de ordem que ficou na fila, não o tempo de um tiro. Cronometrar no chão
de fábrica é o único caminho.

### O elo fraco entre os conectores

**O porta-haste** — não pela tensão, que é baixíssima, mas porque é **o único dos três que
depende de trava elástica ativa**. Trizeta e tampa são geometria passiva. Ele também é o de
maior contagem (50 por módulo) e o que mais sofre ciclos de montagem e reposição em PDV.

Relaxamento de tensão do PP, por literatura genérica (não do composto da Nitron): perda de
20 a 30% da força de fixação nas primeiras 24 a 100 h, 40 a 50% em semanas a poucos meses.
O modo de falha é **de serviço, não estrutural**: régua frouxa, chocalho, aparência degradada
num móvel que fica meses no chão de loja do cliente. E temperatura de loja perto de vitrine
pode passar de 35–40 °C, o que acelera creep de PP fortemente — minha estimativa de 4 a 11 mm
de assentamento em um ano pode estar otimista.

**Alterações baratas que resolveriam, sem molde novo:** nervura no pé do cantilever da trava;
fechar a folga de ~0,4 mm por solda e reusinagem local da cavidade; ou — a alavanca mais
barata, zero ferramentaria — **trocar a resina só do porta-haste** para PP copolímero com
modificador de impacto, ou PP com fibra de vidro curta de 10 a 20%.

⚠️ Se for PP com fibra, **o moído dessa peça não pode entrar no ciclo mono-resina de
R$ 2,63 M/ano**. Precisa segregação — mas 50 peças por módulo é volume pequeno o bastante
para isolar sem drama.

### Sobre o claim de carga

Não há confirmação de norma ABNT dedicada a estante ou expositor de PDV — a NBR 15878 é de
móveis de escritório, escopo errado. **Não afirmar que existe ou que não existe sem checar o
catálogo da ABNT com o jurídico.** A referência internacional de método é a **EN 16121**
(mobiliário de armazenamento para uso não doméstico): não é obrigatória no Brasil, mas é o
protocolo — carga de prova, carga permanente por tempo definido, medição de deformação
residual — que sustentaria um número.

Vale o mesmo raciocínio já documentado para "hermético": **carga não é atributo do material,
é o que o ensaio documentado mostrar**, e o art. 36 do CDC obriga a guardar o ensaio que
sustenta o número da etiqueta. A diferença é que aqui é claim de **segurança estrutural** —
prateleira que cede em loja de cliente é dano material e responsabilidade do fabricante, não
claim fraco. Texto de etiqueta passa pelo jurídico.

### Os seis ensaios que fecham as lacunas

1. **Montagem física de um nó carregado** — decide entre as hipóteses A, B e C. É o ensaio de
   maior alavancagem de todos: vale 100× em tensão e define a carga declarável.
2. **Inserção e retenção do porta-haste** — força de montagem nova contra a força após carga
   sustentada acelerada (estufa 40–50 °C, semanas), para ter curva real de relaxamento em vez
   de literatura.
3. **Módulo montado sob carga declarada por semanas**, com leitura de flecha em t=0, 24 h,
   1 semana e 4 semanas — mede creep de madeira e assentamento nos nós juntos.
4. **Cronometragem no chão de fábrica** das 3 ferramentas na próxima rodada — ciclo real e
   número de cavidades, para substituir o `AD_APONTACICLO`.
5. **Flexão destrutiva em amostra das réguas** do lote real de pinus — confirma se os 12 MPa
   são valor médio ou característico. Pinus tem COV de 20 a 30%; se 12 MPa for média, a FS de
   2,1× no eixo fraco pode não se sustentar no pior lote.
6. **Carga de prova mais carga permanente do módulo completo**, documentada, antes de qualquer
   número ir para etiqueta — é o que o art. 36 exige ter em mãos.

E uma pergunta de geometria que muda a flecha em 3×: **a régua assenta em pé (h = 26,6 mm) ou
deitada (h = 15,3 mm)?** Em pé a flecha é 1,11 mm, deitada 3,36 mm, e com creep de madeira
(kdef ~0,8) a deitada vai a ~6 mm em um ano.

---

## 10. A CRUZETA REENTRA — decisão do usuário, e ele está certo no mérito

O curador vetou o molde e eu especifiquei o piloto sem a cruzeta. **O piloto de um vão que
saiu dali é uma estante, não uma ilha nem uma parede modular** — com só trizeta e peça L,
toda corrida de barra morre no canto. As quatro aplicações do projeto (ilha, ponta de gôndola,
checkout, parede modular) são todas de **mais de um vão**, e nenhuma delas existe sem nó de
meio de vão.

A decisão de incluir é do usuário e está registrada. O que segue é o projeto com a cruzeta.

### A álgebra dos nós — é isso que o configurador precisa

Para uma corrida encadeada de **N vãos**, por nível de prateleira:

| | |
|---|---|
| **trizetas** | **4** — fixo, só as quatro quinas das duas pontas |
| **cruzetas** | **2 × (N − 1)** |
| linhas de montante | N + 1 |
| montantes | 2 × (N + 1) |
| barras de largura `PSC` | 2N |
| barras de profundidade `BLA-03-AC` | N + 1 |
| réguas `PST` | 5N |
| porta-hastes | 10N |

**A contagem de trizeta nunca cresce.** Só a de cruzeta. Essa é a assinatura de um sistema
modular de verdade, e é o argumento estrutural a favor da peça.

### As larguras que saem disso

| N vãos | Largura externa | Trizetas | Cruzetas | Montantes | Peso | Custo est. | 2× custo |
|---|---|---|---|---|---|---|---|
| 1 | 680 mm | 20 | **0** | 4 | 8,5 kg | R$ 146,79 | R$ 293,59 |
| **2** | **1.361 mm** | 20 | **10** | 6 | 15,5 kg | R$ 269,47 | R$ 538,94 |
| 3 | 2.041 mm | 20 | 20 | 8 | 22,6 kg | R$ 392,14 | R$ 784,29 |
| 4 | 2.721 mm | 20 | 30 | 10 | 29,6 kg | R$ 514,82 | R$ 1.029,64 |
| 5 | 3.402 mm | 20 | 40 | 12 | 36,6 kg | R$ 637,49 | R$ 1.274,99 |
| 6 | 4.082 mm | 20 | 50 | 14 | 43,7 kg | R$ 760,17 | R$ 1.520,34 |

**2 vãos = 1.361 mm** é a faixa de módulo de gôndola. E o catálogo já tem um item chamado
`CONJ. CRUZETAS E MOLAS 1330` (CODPROD 6004) — a coincidência de 1.330 com 1.361 vale
conferir com quem desenhou.

### Encadear é 11% MAIS BARATO que módulos separados

A cruzeta não só viabiliza — ela **reduz custo**. Três vãos:

| | Custo | Nós | Montantes |
|---|---|---|---|
| 3 módulos de 1 vão, lado a lado | R$ 440,38 | 60 trizetas | 12 |
| **1 parede de 3 vãos** | **R$ 392,14** | 20 trizetas + 20 cruzetas | **8** |
| **Economia** | **R$ 48,24 · 11,0%** | **−20 nós** | **−4** |

Poupa também 10 barras de profundidade, 4 pés e 4 tampas. E entrega **um** móvel em vez de
três encostados, sem emenda visível.

---

## 11. A cruzeta é a peça crítica do sistema — e isso é novo

Cortei a malha da cruzeta do mesmo jeito que a da trizeta, varrendo área maciça de 0,25 em
0,25 mm. **A arquitetura interna é idêntica** — chapas nas mesmas cotas — o que confirma um
projeto de família bem feito: mesma gramática vertical, ramificação diferente no plano.

| Elemento | Trizeta | **Cruzeta** |
|---|---|---|
| Chapa 1 — fundo do encaixe | z rel 40,0 → 42,9 · **2,90 mm** · 1.857 mm² | z rel 40,0 → 42,8 · **2,75 mm** · 1.888 mm² |
| Chapa 2 | z rel 51,3 → 54,4 · 3,10 mm · 1.828 mm² | z rel 51,3 → 54,3 · 3,00 mm · 3.137 mm² |
| Chapa 3 — topo | z rel 70,0 → 72,9 · 2,90 mm · 3.114 mm² | z rel 70,0 → 72,8 · 2,75 mm · **4.370 mm²** |
| **Seção contínua mínima** | **288 mm²** | **258 mm² — 10% MENOR** |

E o ponto: **como nó de meio de vão, a cruzeta carrega o dobro da carga de um canto.**
Por vão de carga L, cada linha de montante de ponta pega L/2 (logo L/4 por montante), e cada
linha intermediária pega 2 × L/2 = L (logo **L/2 por montante**).

**Seção 10% menor, chapa 5% mais fina, carga 2× maior.**

| Carga/prateleira | Hipótese | Trizeta | **Cruzeta** |
|---|---|---|---|
| **20 kg** | A · parede em compressão | 0,85 MPa · FS 11,7× | **1,90 MPa · FS 5,3×** |
| | B · chapa 1, borda apoiada | 9,2 MPa · FS 1,1× | **20,5 MPa · ACIMA** |
| | B · chapa 1, borda engastada | 4,2 MPa · FS 2,4× | **9,4 MPa · FS 1,1×** |
| | C · chapa de topo | 0,08 MPa | 0,11 MPa |
| **40 kg** | A · parede em compressão | 1,70 MPa · FS 5,9× | **3,80 MPa · FS 2,6×** |
| | B · chapa 1, borda apoiada | 18,4 MPa · ACIMA | **41,0 MPa · ACIMA** |
| | B · chapa 1, borda engastada | 8,5 MPa · FS 1,2× | **18,9 MPa · ACIMA** |
| | C · chapa de topo | 0,16 MPa | 0,22 MPa |

**Consequência direta:** a carga declarável do sistema passa a ser governada pela cruzeta, não
pela trizeta. E o ensaio nº 1 — montar um nó e carregá-lo — fica ainda mais decisivo, porque
agora ele decide entre *"40 kg tranquilo"* (hipóteses A ou C) e *"nem 20 kg"* (hipótese B com
borda apoiada).

Se der hipótese B, a correção é conhecida e barata: **engrossar a chapa 1 da cruzeta** —
alteração de aço na cavidade existente, não molde novo. Passar de 2,75 para 4,0 mm derruba a
tensão pelo quadrado da espessura, de 20,5 para 9,7 MPa.

---

## 12. O molde: três bases de payback, e qual delas é honesta

A cruzeta custa **~R$ 0,495/peça** (volume de malha 62,57 cm³ × 0,905 g/cm³ × o R$/kg
implícito dos irmãos). Uma parede de 3 vãos leva **20 cruzetas**.

| Base de atribuição | Por parede de 3 vãos |
|---|---|
| (a) Contribuição da **injeção só** — 2× o custo da peça | R$ 9,90 |
| (b) **Economia** de encadear contra módulos separados | R$ 48,24 |
| (c) Margem do **produto que a cruzeta viabiliza** — 2× custo | **R$ 392,14** |

Payback, em meses:

| Molde | (a) a 3/mês | (b) a 3/mês | **(c) a 3/mês** | **(c) a 10/mês** |
|---|---|---|---|---|
| R$ 20.000 | 673 | 138 | **17,0** | **5,1** |
| R$ 30.000 | 1.010 | 207 | **25,5** | **7,7** |
| R$ 50.000 | 1.683 | 345 | **42,5** | **12,8** |
| R$ 80.000 | 2.693 | 553 | **68,0** | **20,4** |

A base (c) é a que o curador rejeitou, por creditar ao plástico a margem da madeira. **A
objeção é legítima e o enquadramento correto é outro: o molde não é centro de lucro, é
portão.** Investimento de portão se julga pela contribuição do portfólio que ele destrava —
decisão de capital normal — desde que fique dito, e fica: **a contribuição vem majoritariamente
de madeira comprada e montagem, não de injeção.**

E o que decide não é o molde, é o volume. A 10 paredes/mês um molde de R$ 50 k paga em
**13 meses**; a 3 paredes/mês, **43 meses**. O análogo mais próximo no catálogo — a Caixa
Expositora `010.001.003` — roda a **3 unidades/mês**. Então o intervalo honesto hoje é
**13 a 43 meses, e a variável é o volume, não o molde.**

### O achado que pode dispensar essa conta inteira

Os cinco moldes foram cadastrados em **17/07/2026 dentro de 79 segundos** um do outro:

| Hora | CODPROD | Peça | Já injetada? |
|---|---|---|---|
| **14:25:00** | **14814** | **CRUZETA** | **não** |
| 14:25:26 | 14815 | Haste / porta-haste | sim, WCP 11 |
| 14:25:43 | 14812 | Peça L | sim, WCP 9 |
| 14:26:00 | 14813 | Tampa | sim, WCP 45 |
| 14:26:19 | 14811 | Trizeta | sim, WCP 8 |

**A cruzeta foi a PRIMEIRA das cinco a ser cadastrada.** Não foi adendo — foi especificada
como parte de um conjunto de cinco, e quatro desses cinco já rodaram na máquina.

**Então a pergunta não é "devemos comprar um molde". É "onde está o quinto molde do
conjunto?"** Isso é pergunta para a ferramentaria, custa um telefonema, e se o molde existir —
pronto ou em tryout — toda a tabela de payback acima vira irrelevante.

É o item nº 1 da lista agora, à frente de qualquer ensaio.

---

## 13. As quatro aplicações, mapeadas na álgebra

| Aplicação | Topologia | Nós por nível | Situação |
|---|---|---|---|
| **Parede modular** | corrida reta de N vãos | 4 trizetas + 2(N−1) cruzetas | ✅ resolvida pela cruzeta |
| **Ponta de gôndola** | 1–2 vãos, com a linha final aberta para emendar na corrida | a linha de junção usa cruzeta em vez de trizeta | ✅ resolvida |
| **Checkout em L** | duas corridas a 90° | canto interno = **trizeta** (2 vias no plano); retas = cruzeta | ✅ resolvida |
| **Ilha costa a costa** | duas corridas partilhando a linha de montantes | exigiria **5 vias**: −X, +X, +Y, −Y, Z | ⚠️ ver abaixo |

### O limite honesto: a ilha costa a costa

A cruzeta tem **4 vias**: −X, +X (a corrida passa através), +Y (a ramificação de profundidade)
e Z. Um nó partilhado entre duas corridas costa a costa precisaria de ramificação em **+Y e
−Y ao mesmo tempo** — cinco vias. **A cruzeta, sozinha, não faz isso.**

Duas saídas, e a primeira é provavelmente a resposta:

1. **A hipótese do par espelhado.** A trizeta vem como par ESQ/DIR e as duas mãos **assentam
   uma sobre a outra** — foi isso que as coordenadas dos STLs mostraram (Trizeta 02 sobre a 01,
   fronteira em Z = 230,37). O cadastro da cruzeta diz **"2 CAVIDADES"** e `AD_QTDCAVIDADE = 2`.
   **Se essas duas cavidades forem o par esq/dir**, então uma cruzeta esquerda empilhada sobre
   uma direita dá ramificação em +Y e −Y no mesmo nó — e a ilha costa a costa está resolvida
   com a peça que já existe. **Isto é hipótese testável e é pergunta de uma frase para quem
   desenhou.**
2. **Duas corridas independentes lado a lado**, cada uma com seus montantes. Funciona hoje,
   sem peça nenhuma nova — só fica mais pesada e mais caras (é exatamente o caso "módulos
   separados" da tabela do §10, 11% mais caro).

Não vou afirmar qual é sem confirmação. Mas se for a hipótese 1, o projeto fecha inteiro com
os cinco moldes do conjunto original — nenhuma peça nova.

---

## 14. A lista atualizada, em ordem

1. **Ferramentaria: onde está o molde da cruzeta?** Cadastrado 17/07/2026, primeiro dos cinco,
   quatro irmãos já rodando. Um telefonema. Se existe, o payback sai da conversa.
2. **As 2 cavidades da cruzeta são o par esq/dir?** Uma pergunta a quem desenhou. Decide se a
   ilha costa a costa existe ou não.
3. **Montar um nó de cruzeta e carregá-lo.** Decide entre as hipóteses A, B e C — e agora com a
   cruzeta no circuito o intervalo é de "40 kg tranquilo" a "nem 20 kg".
4. **A régua assenta em pé ou deitada?** Muda a flecha de 1,11 para 3,36 mm.
5. **A tampinha** — STL ainda pendente.
6. **Preço**: uma venda a ≥ 2,00 × custo para ≥ 3 clientes, sem amostra nem bonificação.
   Continua sendo o item que destrava tudo do lado comercial.
7. **Corrigir a unidade de `QTDNEG`** dos PIs de madeira — sem ela não se planeja consumo do
   estoque de R$ 84.211,67 que está parado no local `1010000`.
