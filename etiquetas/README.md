# Etiqueta frontal padronizada — adaptação da planilha de produtos

Adapta `ProdutosNitron2026.xlsx` (635 SKUs, 22 colunas de catálogo e SEO) para o
modelo `Nitron_Matriz_Etiquetas.xlsx` (6 separadores, conteúdo por SKU).

O resultado é **`Nitron_Matriz_Etiquetas_PREENCHIDA.xlsx`**, com os separadores
do modelo original mais três de apoio, e os mesmos CSV em `csv/` prontos para
importar.

## O que a planilha nova resolve

O modelo separa o que é **fixo** do que é **variável**:

| | Onde é impresso | Quantas artes |
|---|---|---|
| Cabeçalho turquesa, rodapé de redes, dados da empresa | Gráfica, bobina pré-impressa | **4** (uma por layout) |
| Nome, capacidade, ícones, código de barras, QR | Impressoras internas, na janela branca | 635 registos de dados |

Daí as 200+ etiquetas caírem para 4 bobinas. O que multiplicava era o conteúdo
variável estar fixo na chapa; passando-o para a impressão interna, sobra apenas
o formato.

A distribuição dos 635 SKUs pelos 4 layouts ficou 47 / 170 / 215 / 203 — nenhum
layout com menos de 7% do portfólio, nenhum acima de 34%. **Quatro chegam**; não
foi preciso ir aos 8.

## Como foi preenchido

Três origens distintas, e a diferença importa na revisão:

1. **Cópia exata** da folha de produtos — `REFERENCIA` (REF) e
   `DESCRICAO SANKHYA` (PORTUGUÊS). Nada foi tocado.
2. **Derivação mecânica** — sem juízo de valor, verificável linha a linha:
   - `NOME PT/EN/ES`: nome comercial sem o código interno entre parênteses, sem
     a capacidade e sem a cor. "Pote Monterey com 3 Divisórias - Transparente
     1,1L (0307.012.001)" → "Pote Monterey com 3 Div." A cor sai porque está no
     produto; a capacidade sai porque tem coluna própria. 635 nomes de origem
     reduzem-se a **297 nomes distintos**.
   - `CAP VALOR` / `CAP UNID`: a coluna VOL convertida em número + unidade
     métrica (`1,1L` → `1.1` + `L`). 424 SKUs têm capacidade; os outros 211 não
     têm no ficheiro de origem e estão sinalizados.
   - `LARG/ALT/PROF CM`: COM → LARG, ALT → ALT, LAR → PROF. Os 59 casos com Ø
     (medida de diâmetro) entram com o valor numérico e ficam sinalizados.
   - `QTD PECAS`: lida do nome ("Kit POP com 6 Potes" → 6). 55 SKUs são kits.
   - `URL QR`: `nitron.com.br/p/` + REFERENCIA.
3. **Proposta com regra** — `LAYOUT`, `SELOS`, `APLICACOES`. É aqui que a
   revisão do Marketing tem de incidir. As regras estão todas em
   `scripts/etiquetas/regras.py` e reproduzidas no separador `Regras_Auto`.

### Layout

Precedência, de cima para baixo:

1. Categoria que é organizador ou maleta (Organização, Teca, Frasqueiras,
   Nitron-Mob) → layout 4, independente da capacidade: a face onde a etiqueta
   assenta é grande.
2. Lixeiras → layout 3.
3. Capacidade: até 400 ml → 1 · 400 ml a 1 L → 2 · acima de 1 L → 3.
4. Sem capacidade: área da face (LARG × ALT) até 100 cm² → 1 · até 250 cm² → 2 ·
   acima → 3.

A coluna `PORQUE ESTE LAYOUT` na Auditoria diz qual das quatro regras decidiu
cada SKU.

### Selos e aplicações

Só entram códigos que existem no `Cat_Selos` e no `Cat_Aplicacoes` — o gerador
aborta se algum código ficar órfão. Duas fontes:

- **Evidência no texto**: o nome ou a descrição dizem "micro-ondas", "com
  travas", "válvula", "pedal", "basculante". Estas ganham prioridade e estão
  listadas na coluna `SELOS COM EVIDENCIA NO TEXTO` da Auditoria.
- **Proposta por categoria**: a tabela em `Regras_Auto`, secção 3 e 4. É
  inferência, não evidência.

Quando o layout não tem lugar para todos, corta-se pelo fim da lista de
prioridade, e o que foi cortado fica registado na Auditoria.

⚠️ **Livre de BPA, apto para micro-ondas e apto para congelador são declarações
técnicas.** Estão propostas em 370 SKUs (BPA em 370, MIC em 33, FRZ em 28) e
precisam de assinatura da Engenharia/Qualidade antes de ir para chapa. As restantes (empilhável,
higiénico, fácil de limpar) são descritivas e o Marketing pode fechar sozinho.

### Aplicações novas

Faltavam três no catálogo do modelo para cobrir o portfólio. Foram
acrescentadas ao `Cat_Aplicacoes` com `NOVO = S`, e cada uma obriga a um ícone:

| Código | PT | Para que SKUs |
|---|---|---|
| `BEBI` | Bebidas | Jarras, copos, canecas, espremedores (35 SKUs) |
| `CONF` | Confeitaria e bolos | linha Decor-Confeitaria (8 SKUs) |
| `DECO` | Decoração | Nitron-Mob, prateleiras, suportes, cestos Teca (34 SKUs) |

Selos novos: **nenhum**. Os 16 do modelo cobrem tudo.

Biblioteca de ícones a desenhar: **53** (16 selos + 37 aplicações), dos quais 3
são os novos acima.

### MAX CARAC NOME

O modelo deixou os limites do separador `Layouts` em branco. Ficaram
28 / 34 / 40 / 44, calculados no `Regras_Auto` como o **menor** entre:

- o que cabe na janela branca: largura útil ÷ (corpo × 0,3528 mm/pt × 0,52), a
  multiplicar pelo número de linhas;
- um teto editorial, decisão de Marketing: acima dele o nome deixa de ler na
  gôndola mesmo cabendo.

Quando o nome excede, o gerador aplica abreviaturas por ordem (`com` → `c/`,
`Divisórias` → `Div.`, `Peças` → `Pçs`…) e registra quais usou. 32 SKUs foram
abreviados; **16 continuam acima do limite** e precisam de decisão editorial —
estão filtráveis na Auditoria.

## Separadores do ficheiro entregue

| Separador | O que é | Importar no Sankhya |
|---|---|---|
| `Instrucoes` | as do modelo + nota do que foi automático | não |
| `Matriz_SKU` | 635 SKUs × 16 colunas, estrutura intacta do modelo | **sim** |
| `Cat_Selos` | 16 selos, sem alterações | sim |
| `Cat_Aplicacoes` | 34 do modelo + 3 novos marcados `NOVO = S` | sim |
| `Layouts` | 4 layouts com dimensões e limites preenchidos | sim |
| `Unidades` | sem alterações | sim |
| `Auditoria` | 1 linha por SKU: razão de cada decisão + `ALERTAS` | não |
| `Impressao_Interna` | os mesmos dados + EAN, para a impressora de código de barras | não |
| `Regras_Auto` | as regras usadas e o cálculo do MAX CARAC | não |

As cores do modelo foram mantidas: **cinzento** = vem do Sankhya, não mexer;
**amarelo** = preenchimento do Marketing.

O EAN ficou fora da `Matriz_SKU` de propósito — não é conteúdo gráfico da
bobina, é dado da impressão interna. Vive no `Impressao_Interna`.

## Por onde começar a revisão

Abrir a `Auditoria`, filtrar `ALERTAS` não vazio: são **330 SKUs**. Os outros 305
não têm nada a assinalar.

| Alerta | SKUs | O que fazer |
|---|---|---|
| SEM CAPACIDADE | 211 | ver se o produto tem capacidade e a origem não a tem, ou se não se aplica (tábua, cabide) |
| SEM DESCRICAO NA ORIGEM | 93 | os selos e aplicações desses saíram só da categoria, sem evidência de texto — conferir com mais atenção |
| DIMENSAO E DIAMETRO | 59 | a origem traz Ø; confirmar se LARG/PROF fazem sentido para produto redondo |
| SEM NOME EN / ES | 28 | traduzir |
| NOME PT EXCEDE LIMITE | 16 | encurtar à mão |
| CAPACIDADE MULTIPLA NA ORIGEM | 8 | a origem tem "1,5L / 2,9L / 4,6L" numa célula; ficou o primeiro valor |
| CATEGORIA NORMALIZADA | 3 | "teca" → "Teca", "Microondas" → "Micro-ondas"; corrigir na origem |
| EAN INVALIDO | 1 | 4 dígitos em vez de 13 |
| EAN DUPLICADO | 1 | dois SKUs com o mesmo EAN |

Os dois últimos travam a impressão do código de barras: resolver antes de mandar
bobina para a gráfica.

## O que ainda falta e não dá para automatizar

- **`CODPROD` está vazio.** O código interno do Sankhya não consta da folha de
  produtos — só a REFERENCIA. Preencher com um PROCV sobre a REFERENCIA antes de
  importar.
- **Dimensões da bobina.** 60×40, 80×50, 100×70 e 120×80 mm são proposta,
  encostada a formatos correntes de bobina. Confirmar com a gráfica e com a
  impressora interna (largura máxima de material) e, se mudarem, editar
  `LAYOUTS` em `regras.py` — o MAX CARAC recalcula sozinho.
- **`BRA` (Produzido no Brasil) é igual nos 635 SKUs.** Sai mais barato
  imprimi-lo na arte pré-impressa e libertar um lugar de ícone na janela
  variável. Enquanto isso não for decidido, fica na matriz.

## Como exportar

**Para revisão interna** — mandar o `.xlsx` como está. Tem filtro no cabeçalho
das três folhas grandes e painéis fixos na linha 3.

**Para importar no Sankhya** — os CSV já estão em `csv/`, separador `;`,
codificação UTF-8 com BOM (o Excel abre sem estragar acentos):

```
csv/matriz_sku.csv          635 linhas   ← a importação principal
csv/cat_selos.csv            16
csv/cat_aplicacoes.csv       37          ← 3 com NOVO = S
csv/layouts.csv               4
csv/unidades.csv              7
csv/impressao_interna.csv   635          ← não vai para o Sankhya
csv/auditoria.csv           635          ← não vai para o Sankhya
```

Se preferires gerar do Excel: abrir o separador, *Ficheiro → Guardar Como →
CSV UTF-8*, uma folha de cada vez. Apagar as linhas 1 e 2 (título e legenda)
antes de importar — o cabeçalho de dados está na **linha 3**.

**Para as impressoras de código de barras** — `csv/impressao_interna.csv`. Uma
linha por SKU com REFERENCIA, EAN, LAYOUT, NOME PT, capacidade, selos,
aplicações e URL do QR. É o formato que BarTender, NiceLabel e o utilitário da
Zebra/Argox consomem como fonte de dados: aponta-se o campo EAN ao objeto de
código de barras EAN-13 e os restantes a campos de texto.

**Para a gráfica** — não é este ficheiro. São as 4 artes de bobina com a janela
branca nas medidas do separador `Layouts`, mais a biblioteca de 53 ícones em
vetor, como diz o próprio `Instrucoes` do modelo.

## Voltar a correr

```bash
python3 scripts/etiquetas/gerar_matriz.py
```

Reescreve o `.xlsx` e os CSV a partir de `fonte/`. Mudar critério é editar
`scripts/etiquetas/regras.py` e correr outra vez — nunca corrigir 635 linhas à
mão. Os ficheiros de entrada nunca são alterados.

```bash
# com outra folha de produtos
python3 scripts/etiquetas/gerar_matriz.py --produtos caminho/para/produtos.xlsx
```

`fonte/produtos-nitron-2026.csv` é o extrato da folha original (a folha `.xlsx`
tem 10 MB por causa das imagens embutidas e fica fora do repositório).
