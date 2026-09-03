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
