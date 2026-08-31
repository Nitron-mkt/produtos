# Dossiê em PDF

`Chrono_Datador_dossie.pdf` — 12 páginas A4, para imprimir e levar à ferramentaria.
Mesmo conteúdo da apresentação em HTML, recomposto para papel: capa, sete seções e o
Anexo A com a tabela completa de cotas.

## Como reconstruir

```
python3 build.py
```

Monta `dossie.build.html` a partir de `dossie.template.html` + `draw.js` + `assets/`
e imprime em PDF pelo Chromium (Playwright). Precisa de `playwright` instalado e do
Chromium em `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.

| Arquivo | O que é |
|---|---|
| `dossie.template.html` | o documento, com marcadores `__FONTS__`, `__GEO__`, `__DRAW__`, `__FIG_*__` |
| `draw.js` | gera as três pranchas vetoriais (planta, corte, datador) a partir da geometria medida |
| `assets/geo.json` | contornos extraídos das malhas STL, usados pelas pranchas |
| `assets/fonts_min.json` | Archivo, IBM Plex Sans e IBM Plex Mono em base64, embutidas no PDF |
| `assets/fig_*.png` | renders das peças geradas, a partir dos STL de `../stl/` |
| `dossie.build.html` | intermediário, não versionado |

As figuras vêm de `../medicao/` (render z-buffer sobre as malhas) e a geometria vetorial
de `../medicao/emit2.py`. Nada no PDF é desenhado à mão: cota, contorno e render saem
todos das malhas.
