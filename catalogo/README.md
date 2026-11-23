# Catálogo Nitron — dados do Sankhya direto para o InDesign

Ninguém digita EAN, referência, caixa ou preço. Esses campos saem do Sankhya, são
conferidos por script e entram no InDesign automaticamente.

```
Sankhya (tabela padrão)  ─┐
traducoes.csv  (PT/EN/ES) ├─→ gera_catalogo.py ─→ saida/catalogo_indesign.csv ─→ indesign/monta_catalogo.jsx ─→ PDF COM preço
lancamentos.csv          ─┘                      saida/catalogo_mestre.xlsx (pendências)                    └→ PDF SEM preço
```

## Arquivos

| Arquivo | Quem mexe | O que é |
|---|---|---|
| `sql/extrai_tabela_padrao.sql` | — | Consulta do Sankhya: tabela padrão (**CODTAB 0**; o 3 é exportação), ativos e não suspensos |
| `dados/sankhya_raw.txt` | gerado | Resultado da consulta (620 itens em 23/11/2026, conferido por soma de controle) |
| `traducoes.csv` | **marketing** | Nome-base → nome PT limpo, EN e ES. Coluna `REVISAR=S` = nome ambíguo no cadastro |
| `cores.csv` / `linhas.csv` | marketing | Tradução da cor escrita no nome e seção do catálogo, com a ordem das seções |
| `cores_codigo.csv` | marketing | Código de cor (3ª parte de REF.EMB.COR) → cor. Usado quando o nome não diz a cor |
| `lancamentos.csv` | **marketing** | Produtos que ainda não existem no Sankhya. Saem com selo "LANÇAMENTO" |
| `excluir.csv` | marketing | CODPROD ou referência que não entram (o item Avon/OEM já está fora) |
| `gera_catalogo.py` | — | Junta tudo, valida e gera o CSV para o InDesign e a planilha de pendências |
| `indesign/monta_catalogo.jsx` | — | Monta o documento inteiro no InDesign e exporta os 2 PDFs |
| `indesign/codigo_barras_avulso.jsx` | — | Você digita o número e ele desenha o código na página aberta (embalagem, etiqueta, qualquer peça) |

## A referência: REF.EMB.COR

`233.012.001` = **233** (referência macro do SKU) · **012** (peças por embalagem master) · **001** (código da cor).
O script usa cada parte:

- **REF** agrupa o mesmo produto: as cores do mesmo SKU saem lado a lado na página.
- **EMB** é conferida contra a `QTD_CAIXA` do cadastro. Se divergir, vai para Pendências.
- **COR** preenche a cor quando o nome não diz (pendência "confirmar") e acusa quando o nome diz uma cor e o código diz outra.

## Código de barras

O script desenha o EAN-13 em vetor a partir dos números. Aceita **12 dígitos** (calcula o
verificador sozinho) ou 13 (confere o verificador e recusa se estiver errado). Espaços,
pontos e traços são ignorados. Isso vale para o catálogo (coluna `EAN13` de `lancamentos.csv`)
e para o script avulso.

## Como gerar o catálogo

1. **Atualizar os dados do Sankhya.** Rode a consulta de `sql/` e salve o resultado em
   `dados/sankhya_raw.txt`, uma linha por produto. Pelo Claude, basta pedir:
   *"atualiza a extração do catálogo"*.
2. **Rodar `python3 gera_catalogo.py`.** Depois abra `saida/catalogo_mestre.xlsx` na aba
   **Pendências** e corrija o que estiver apontado **no Sankhya** (não no InDesign).
3. **Fotos.** Uma pasta com os arquivos nomeados pela **referência completa**:
   `233.012.001.png`. Nunca `233.png`, porque são produtos diferentes. Aceita psd, tif, png, jpg, ai, eps e pdf.
4. **InDesign.** Copie `indesign/monta_catalogo.jsx` para a pasta de scripts
   (painel *Scripts* > *Usuário* > clique direito > *Mostrar no Finder/Explorer*) e dê dois cliques.
   O script pede o CSV e a pasta de fotos, monta tudo, salva `catalogo_nitron.indd`,
   escreve `relatorio_montagem.txt` (sem foto, texto apertado, sem EAN) e exporta os dois PDFs.

## Como funciona "com e sem preço"

O preço fica numa camada própria (**Preço**). O script exporta um PDF com a camada ligada e
outro com ela desligada. Se você ajustar a diagramação à mão, ajusta uma vez só. Para
reexportar, ligue ou desligue a camada no painel *Camadas* e exporte.

## Diagramação: o que vem pronto e o que ajustar

- Grade de 9 produtos por página (3×3) em A4. Cada seção começa numa página nova, com faixa de título em PT/EN/ES.
- Fonte: **Gotham Book e Gotham Bold** em tudo, sem itálico. O inglês e o espanhol vão em Book
  cinza. O script acha a Gotham tanto instalada como família "Gotham" (estilos Book/Bold) quanto como
  "Gotham Book" / "Gotham Bold". Se não achar, avisa antes de montar.
- Tudo usa **estilos de parágrafo** (`NomePT`, `NomeEN`, `NomeES`, `Specs`, `Preco`...). Para trocar
  fonte ou cor do catálogo inteiro, edite o estilo e não o texto.
- Cores da marca ficam no bloco `CFG` no topo do `.jsx` (`corMarca`, `fonte`, grade, margens).
- O código de barras é desenhado em **vetor** a partir do EAN (EAN-13 a 80%, com dígito
  verificador conferido). Não depende de plugin nem de fonte de código de barras.
- Nome que não cabe tem o corpo reduzido automaticamente e é listado no relatório.

## Limitações conhecidas

- **Tamanho (dimensões):** a view do Sankhya disponível não traz altura, largura e profundidade.
  Só os painéis Teca têm a medida no nome. Pedir ao TI para incluir essas colunas
  (`TGFPRO.ALTURA/LARGURA/ESPESSURA`) na `AD_VW_COM_CADPRODUTOS`. Até lá, o campo fica vazio.
- **Volume** é lido do nome do produto (ex.: "2,9L" → "2,9 L").
- **Espanhol** usa vocabulário do Cone Sul ("heladera", "porotos"). Ajuste `traducoes.csv` se o mercado for outro.
- As traduções são um rascunho bem feito, mas precisam de revisão de quem vende fora.
- O script do InDesign foi escrito para InDesign CC e ainda **não foi rodado num InDesign real**.
  O primeiro teste deve ser com uma seção pequena.
