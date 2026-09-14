#!/usr/bin/env python3
"""Gera uma versão estática do manual, pronta para importar no Canva.

O manual normal se desenha por JavaScript. O importador do Canva lê HTML, não
executa a página, então aqui o HTML é renderizado num navegador sem cabeça e o
DOM resultante é gravado: sem a barra de ferramentas, sem o painel de
conferência, com as fontes embutidas e com data-document-role="page" na folha,
que é como o importador reconhece uma página.

    python3 manual/estatico.py
"""
import pathlib, re, subprocess, sys, tempfile

BASE = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE))
from pdf import CHROME, fontes_embutidas          # reaproveita o embutidor de fontes

ENTRADA = BASE / 'manual-850-004-N03.html'
SAIDA = BASE / 'manual-850-004-N03.canva.html'


def main():
    if CHROME is None:
        sys.exit('Chromium não encontrado.')
    with tempfile.TemporaryDirectory() as tmp:
        alvo = pathlib.Path(tmp) / 'm.html'
        alvo.write_text(ENTRADA.read_text(encoding='utf-8'), encoding='utf-8')
        r = subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                            '--virtual-time-budget=8000', '--window-size=1400,1300',
                            '--dump-dom', str(alvo)],
                           check=True, capture_output=True)
    html = r.stdout.decode('utf-8')

    # fora o que é ferramenta de tela, não manual
    for cls in ('barra', 'conferencia'):
        html = re.sub(rf'<div class="{cls}">.*?</div>\s*(?=<div class="folhas">)', '', html,
                      flags=re.S)
        html = re.sub(rf'<section class="{cls}">.*?</section>', '', html, flags=re.S)

    # a folha vira uma página para o importador
    html = html.replace('<section class="folha">',
                        '<section class="folha" data-document-role="page" '
                        'data-label="Manual de Montagem — 850.004.N03">', 1)

    # fontes embutidas: o importador não vai buscar o Google Fonts por nós
    m = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">', html)
    if m:
        html = html.replace(m.group(0), f'<style>{fontes_embutidas(m.group(1))}</style>')
    html = re.sub(r'<link rel="preconnect"[^>]*>', '', html)

    if '<meta charset' not in html.lower():
        html = html.replace('<head>', '<head><meta charset="utf-8">', 1)

    SAIDA.write_text(html, encoding='utf-8')
    print(f'\n-> {SAIDA.relative_to(BASE.parent)}  {len(html)//1024} KB')
    for o in ('data-document-role="page"', 'class="barra"', 'class="conferencia"', '<meta charset'):
        print(f'   {o:34s} {html.count(o)}')


if __name__ == '__main__':
    main()
