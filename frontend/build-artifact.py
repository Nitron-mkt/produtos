#!/usr/bin/env python3
"""Gera a versao do artefato a partir do HTML autonomo.

O arquivo publicavel (monte-seu-pdv.html) e um documento completo, para
subir em qualquer host. O visualizador de artefato injeta o proprio
esqueleto <!doctype>/<head>/<body>, entao a versao dele precisa ser so o
conteudo. Este script tira o envelope e mantem uma unica fonte de verdade.
"""
import re, sys, pathlib
src = pathlib.Path(__file__).parent / 'monte-seu-pdv.html'
dst = pathlib.Path(__file__).parent / '_artifact-monte-seu-pdv.html'
h = src.read_text(encoding='utf-8')

# tira o envelope de documento e o que o esqueleto do artefato ja fornece
for pat in (r'<!doctype html>\s*', r'</?html[^>]*>\s*', r'</?head>\s*',
            r'</?body>\s*', r'<meta charset[^>]*>\s*',
            r'<meta name="viewport"[^>]*>\s*', r'<link rel="preconnect"[^>]*>\s*'):
    h = re.sub(pat, '', h, flags=re.I)
h = h.strip() + '\n'

for tag in ('<!doctype', '<html', '<head>', '<body>'):
    if re.search(re.escape(tag), h, flags=re.I):
        sys.exit(f'ERRO: sobrou {tag} na versao do artefato')
if '<title>' not in h or '<style>' not in h:
    sys.exit('ERRO: title ou style perdidos')

dst.write_text(h, encoding='utf-8')
print(f'{dst.name}: {len(h)} bytes (de {len(src.read_text(encoding="utf-8"))})')
