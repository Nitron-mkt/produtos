#!/usr/bin/env python3
"""Gera o manual final a partir de template.html + as artes SVG em pecas/.

    python3 manual/build.py

Para regerar as artes depois de alterar um STL:
    python3 manual/stl2svg.py caminho/Peca.STL manual/pecas/850TZ1.svg --eye=1,-1,-0.55
"""
import re, json, pathlib

BASE = pathlib.Path(__file__).parent
ARTES = sorted(q.stem for q in (BASE / 'pecas').glob('*.svg'))

def limpa(svg: str) -> str:
    """Mantém o viewBox, tira width/height (o CSS controla o tamanho),
    reduz a precisão dos paths e troca a cor fixa por currentColor."""
    svg = re.sub(r'\s(width|height)="[^"]*"', '', svg, count=2)
    svg = svg.replace('stroke="#111"', 'stroke="currentColor"')
    svg = re.sub(r'(\d+)\.(\d)\d+', r'\1.\2', svg)
    svg = re.sub(r'\n+', '', svg)
    return svg.strip()

art = {}
for ref in ARTES:
    p = BASE / 'pecas' / f'{ref}.svg'
    art[ref] = limpa(p.read_text(encoding='utf-8'))
    print(f'  {ref:8s} {len(art[ref]):6d} bytes')

html = (BASE / 'template.html').read_text(encoding='utf-8')
bloco = 'const ART = ' + json.dumps(art, ensure_ascii=False) + ';'
if '/*__ART__*/' not in html:
    raise SystemExit('template.html nao tem o marcador /*__ART__*/')
html = html.replace('/*__ART__*/', bloco)

saida = BASE / 'manual-850-004-N03.html'
saida.write_text(html, encoding='utf-8')
print(f'\n-> {saida.relative_to(BASE.parent)}  ({len(html)/1024:.0f} KB)')
