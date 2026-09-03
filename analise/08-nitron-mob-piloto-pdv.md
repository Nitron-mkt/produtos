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
