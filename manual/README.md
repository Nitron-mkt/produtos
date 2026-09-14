# Manual de montagem — Arara Nitron-MOB (REF. 850.004.N03)

Manual editável em A4, frente e verso. O conteúdo inteiro vive num bloco JSON
dentro do próprio arquivo, e a página se desenha a partir dele.

## Arquivos

| Arquivo | O que é |
|---|---|
| `manual-850-004-N03.html` | **O manual.** Arquivo único, abre em qualquer navegador. Não edite à mão — é gerado. |
| `template.html` | A fonte: CSS, o JSON do conteúdo e o código que desenha a página. |
| `build.py` | Junta `template.html` + as artes de `pecas/` e gera o manual. |
| `stl2svg.py` | Gera arte de linha vetorial a partir de um STL. |
| `pecas/*.svg` | As 5 peças plásticas desenhadas a partir dos STLs. Importam em Illustrator, Inkscape e Canva. |

## Três formas de editar

1. **Na página** — abra o manual, clique em *Editar textos*, reescreva, clique em
   *Concluir edição*. *Salvar versão* grava uma nova versão publicada; *Imprimir / PDF*
   gera o PDF (marque frente e verso, escala 100%, sem margens).
2. **No JSON** — abra `template.html`, edite o bloco `<script id="dados">` e rode
   `python3 manual/build.py`. É o caminho para mudar quantidades e etapas em lote.
3. **No layout** — o CSS está em `<style id="css">` no mesmo arquivo.

## Regerar a arte de uma peça

```bash
python3 manual/stl2svg.py caminho/Peca.STL manual/pecas/850TZ1.svg --eye=1,-1,0.62
python3 manual/build.py
```

`--eye` é a direção da câmera (x,y,z). As duas trizetas usam a **mesma** câmera de
propósito: é assim que dá para ver que são espelhadas. `--crease` (padrão 22°) controla
quais arestas internas viram linha.

## A conferência automática

O painel ao pé da página compara, referência por referência, a quantidade declarada na
lista de peças com a soma do que as 9 etapas pedem. Ele aparece só na tela — não sai na
impressão. Se você mexer numa quantidade e a conta deixar de fechar, ele acusa na hora.

## O que mudou em relação ao manual anterior

- **A conta não fechava.** O passo 7 antigo montava dois quadros (4× PSC-04 + 4× PST-01 =
  8 ripas, logo 8 cantos) mas listava só 4 conectores. Sobravam 2× 850TZ1 e 2× 850TZ2 na
  lista, sem etapa que os usasse. As 8 etapas viraram 9, separando o quadro intermediário
  do quadro do cabideiro, e as 10 referências passaram a fechar.
- **Arte vetorial** das 5 peças plásticas, tirada da geometria real dos STLs.
- **Um "Confira" por etapa** — o que olhar antes de seguir para a próxima.
- **850TZ1 × 850TZ2**: medidas na geometria confirmam mesma inércia e quiralidade oposta.
  São espelhadas e não se substituem; o manual passou a dizer isso e a mostrar as duas
  lado a lado, na mesma câmera.

## Pendência aberta

Em quais 2 cantos do quadro do cabideiro entram os conectores **850L**. A quantidade está
fechada (2 unidades, etapa 8), mas a posição não foi conferida contra o desenho de
conjunto — um canto de 2 vias não fecha sozinho um retângulo de 4 cantos.
