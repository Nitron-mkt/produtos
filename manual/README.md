# Manual de montagem — Arara Nitron-MOB (REF. 850.004.N03)

Reprodução editável do manual de uma folha só: PEÇAS INCLUSAS à esquerda, o desenho do
conjunto e PEÇAS PLÁSTICAS à direita, MONTAGEM em 8 caixas 4×2, ATENÇÃO e QR no rodapé.
O conteúdo inteiro vive num bloco JSON dentro do próprio arquivo, e a página se desenha
a partir dele.

## Arquivos

| Arquivo | O que é |
|---|---|
| `manual-850-004-N03.html` | **O manual.** Arquivo único, abre em qualquer navegador. Não edite à mão — é gerado. |
| `template.html` | A fonte: CSS, o JSON do conteúdo e o código que desenha a folha. |
| `build.py` | Junta `template.html` + tudo que estiver em `pecas/` e gera o manual. |
| `linework.py` | Malha 3D → arte de linha vetorial, com remoção de linha oculta. |
| `stl2svg.py` | Desenha uma peça a partir de um STL. |
| `montagem2svg.py` | Modela a arara pelas medidas das ripas, desenha o conjunto e as 7 etapas ilustradas, e posiciona os balões de identificação. |
| `pecas/*.svg` | Todas as artes. Importam em Illustrator, Inkscape e Canva. |

## Três formas de editar

1. **Na página** — abra o manual, clique em *Editar textos*, reescreva, clique em
   *Concluir edição*. *Salvar versão* grava uma nova versão publicada; *Imprimir / PDF*
   gera o PDF (A4, escala 100%, sem margens).
2. **No JSON** — abra `template.html`, edite o bloco `<script id="dados">` e rode
   `python3 manual/build.py`. É o caminho para mudar quantidades e etapas em lote.
3. **No layout** — o CSS está em `<style id="css">` no mesmo arquivo. As medidas estão
   em milímetros para casar com a folha A4.

## Regerar as artes

```bash
# uma peça plástica, a partir do STL
python3 manual/stl2svg.py caminho/Peca.STL manual/pecas/850TZ1.svg --eye=1,-1,0.62

# o conjunto, as ripas soltas e as ilustrações das etapas 2 a 8
python3 manual/montagem2svg.py

python3 manual/build.py
```

`--eye` é a direção da câmera (x,y,z); `--crease` (padrão 22°) decide quais arestas
internas viram linha. Nas ilustrações de etapa, o que **entra naquela etapa** sai com
traço cheio e o que já estava montado sai mais fino — é assim que a caixa mostra o que
muda sem precisar de seta.

Cada peça que entra na etapa leva um **balão numerado**, na mesma ordem da lista
REF. usadas da caixa. As âncoras dos balões ficam em `ETAPAS`, em `montagem2svg.py`;
o tamanho do balão sai de `CAIXA_MM` (a área, em mm, onde o desenho é impresso), para
sair igual em todas as ilustrações qualquer que seja a escala do desenho.

As medidas do modelo 3D saem da própria lista de peças (`montagem2svg.py`):
PSC-04 717 mm, PST-01 437 mm, PSA-05 513 mm, PSC-02 415 mm, BPE-01-AC 60 mm.
Mexeu numa medida, rode os dois scripts e o desenho acompanha.

## A conferência automática

O painel abaixo da folha compara, referência por referência, a quantidade declarada em
PEÇAS INCLUSAS com a soma do que as 8 etapas pedem. Aparece só na tela — não sai na
impressão. Se você mexer numa quantidade e a conta deixar de fechar, ele acusa na hora.

## A sequência de montagem

Pedido da qualidade: **cada andar é montado inteiro, deitado, e só depois as alturas são
conectadas** — nunca montar um quadro no ar.

| Etapa | O que faz |
|---|---|
| 1 | Separe e confira todas as peças |
| 2–5 | Monta os 4 andares inteiros, um por caixa (o 2º já com porta-hastes e ripas do calceiro) |
| 6–7 | Levanta: conecta 1º→2º, depois 2º→3º→4º com as 12 colunas PSA-05 |
| 8 | Tampas |

A medida de cada peça vem da própria lista de peças (campo `med`), não de um segundo
cadastro — mudou na lista, muda no passo a passo.

## O que mudou em relação ao manual anterior

- **A conta não fechava.** O passo 7 monta dois quadros (4× PSC-04 + 4× PST-01 = 8 ripas,
  logo 8 cantos) mas listava só 4 conectores: 2× 850L, 1× 850TZ1 e 1× 850TZ2. Sobravam
  2× 850TZ1 e 2× 850TZ2 na lista, sem etapa que os usasse. Corrigido para **2× 850L,
  3× 850TZ1 e 3× 850TZ2** — aí 4 quadros × 4 cantos = 16 = os 16 conectores da lista, e
  as 10 referências fecham.
- **Ilustrações vetoriais** — as 5 peças plásticas saem da geometria real dos STLs; o
  conjunto e as etapas saem de um modelo construído com as medidas das ripas.
- **850TZ1 × 850TZ2**: medidas na geometria dos STLs confirmam mesma inércia (0,1% de
  diferença) e quiralidade oposta. São espelhadas e não se substituem.
- **Sequência refeita** para montar andar inteiro antes de conectar as alturas, e
  **peças identificadas** por balão, referência e medida em cada etapa.

## Pendência aberta

Em quais 2 cantos do 4º andar entram os conectores **850L**. A quantidade fecha
(2 unidades na etapa 5), mas a posição não foi conferida contra o desenho de conjunto —
um canto de 2 vias não fecha sozinho um retângulo de 4 cantos. Enquanto isso não se
resolve, o balão 1 da etapa 5 está num canto provisório.
