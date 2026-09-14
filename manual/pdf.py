#!/usr/bin/env python3
"""Gera o PDF A4 do manual, com as fontes embutidas.

O Chromium desta máquina não alcança o fonts.googleapis.com, e mesmo onde
alcança um PDF que depende de rede é frágil. Então as fontes entram no
arquivo como data URI antes de imprimir.

    python3 manual/pdf.py
"""
import base64, pathlib, re, subprocess, sys, tempfile, urllib.request

BASE = pathlib.Path(__file__).parent
ENTRADA = BASE / 'manual-850-004-N03.html'
SAIDA = BASE / 'manual-850-004-N03.pdf'
CHROME = next((p for p in (
    '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',
    '/opt/pw-browsers/chromium-1194/chrome-linux/chrome') if pathlib.Path(p).exists()), None)
META = '<meta charset="utf-8">\n'
UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/120.0.0.0 Safari/537.36')          # sem isto o Google devolve ttf, não woff2


def busca(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    return urllib.request.urlopen(req, timeout=60).read()


def fontes_embutidas(url_css):
    css = busca(url_css).decode('utf-8')
    for u in sorted(set(re.findall(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', css))):
        dado = base64.b64encode(busca(u)).decode('ascii')
        css = css.replace(u, f'data:font/woff2;base64,{dado}')
        print(f'  embutida  {u.rsplit("/", 1)[-1]:<28} {len(dado)//1024:>4} KB')
    return css


def main():
    if CHROME is None:
        sys.exit('Chromium não encontrado.')
    # sem isto o Chromium le o arquivo como windows-1252 e todo acento
    # vira mojibake ('PEÃ§AS'). O manual publicado nao precisa porque a
    # plataforma injeta o charset; um arquivo solto precisa.
    html = META + ENTRADA.read_text(encoding='utf-8')
    m = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">', html)
    if not m:
        sys.exit('Não achei o <link> das fontes no manual.')
    html = html.replace(m.group(0), f'<style>{fontes_embutidas(m.group(1))}</style>')

    with tempfile.TemporaryDirectory() as tmp:
        alvo = pathlib.Path(tmp) / 'manual.html'
        alvo.write_text(html, encoding='utf-8')
        subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                        '--no-pdf-header-footer', '--virtual-time-budget=9000',
                        '--window-size=1400,1200', f'--print-to-pdf={SAIDA}', str(alvo)],
                       check=True, capture_output=True)

    d = SAIDA.read_bytes()
    caixa = re.search(rb'/MediaBox\s*\[([^\]]*)\]', d)
    mm = [round(float(x) / 72 * 25.4, 1) for x in caixa.group(1).split()] if caixa else []
    paginas = len(re.findall(rb'/Type\s*/Page[^s]', d))
    tam = f'{mm[2]} x {mm[3]} mm' if mm else 'tamanho desconhecido'
    print(f'\n-> {SAIDA.relative_to(BASE.parent)}  {len(d)//1024} KB  '
          f'{paginas} página  {tam}')
    # o PDF guarda os nomes fora dos streams comprimidos
    usadas = [f for f in ('Archivo', 'Figtree') if d.count(f.encode())]
    caiu = [f for f in ('Liberation', 'Helvetica', 'DejaVu') if d.count(f.encode())]
    print('   fontes embutidas:', ', '.join(usadas) or 'NENHUMA')
    if caiu:
        print('   ATENÇÃO — caiu para', ', '.join(caiu), ': o PDF não está com a tipografia certa.')


if __name__ == '__main__':
    main()
