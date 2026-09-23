# Visor do Chrono datador

`Chrono_Datador.html` — **um arquivo só, 1,34 MB, abre com dois cliques.** Não
depende de internet nem de CDN: os sólidos estão embutidos no próprio arquivo e o
desenho é WebGL2 escrito à mão. Pode ser mandado por e-mail ou aberto de um pen
drive; o único recurso externo é a fonte do Google, e sem ela a página apenas
troca a tipografia.

Mesmo padrão do visor do Cesto Mini Organizador.

## Os 4 modos

| modo | o que mostra |
|---|---|
| **O conjunto** | as 3 peças montadas, na data de hoje |
| **Como marca a data** | idem, com os botões de dia e mês ativos |
| **Os 3 moldes** | vista explodida, peças alinhadas e separadas em 7 e 15 mm |
| **Na tampa** | recorte de Ø60 mm da tampa Pote 025 Pequeno, na posição real |

Os controles de dia e mês giram as peças de verdade — não é animação gravada. A
ponta da gota aponta o dia na escala externa; a janela recortada nela enquadra o
mês na rodinha de baixo.

## A cinemática

```
ponteira (M03):  −(dia − 1) · 360/31
rodinha  (M02):  (mês − 1) · 30  −  (dia − 1) · 360/31
```

A rodinha acompanha o giro da ponteira **e** soma o deslocamento do mês, porque a
janela do mês vive na ponteira. Um giro ajusta o dia, o outro ajusta o mês.

## Coordenadas

As do STL original da tampa: Y é a vertical e o eixo do poço da válvula está em
X 61,97 / Z 102,68. Nada foi recentrado — por isso a tampa e o datador caem um no
outro sem alinhamento nenhum.

## Como refazer

```bash
python3 gera.py     # lê os STL, embute no modelo.html e escreve Chrono_Datador.html
python3 prova.py    # abre no Chromium headless, fotografa os 4 modos e acusa erro de console
```

`modelo.html` é o template com `__MALHAS__` e `__TRIANGULOS__` — é ele que se
edita. O `Chrono_Datador.html` é gerado e não deve ser editado à mão.

Cada malha entra como `f32 mn[3] · f32 sc[3] · u32 nv · u32 nf · u16 pos[nv*3] ·
u16 idx[nf*3]`: posição quantizada em 16 bits dentro da própria caixa, o que dá
passo de ~0,0007 mm numa peça de 44 mm — uma ordem de grandeza abaixo da
tesselação do STL. Índice em `u16` limita cada peça a 65.536 vértices; a tampa é
recortada em Ø60 e decimada para 24.000 faces para caber.

## Conferido

108.967 triângulos, 4 modos, sem erro de console (só o aviso de certificado da
fonte, que é do sandbox). As fotos de cada modo estão em `prova/`.
