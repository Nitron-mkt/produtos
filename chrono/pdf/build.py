import json, base64, pathlib, subprocess, sys
S='assets'
tpl=pathlib.Path('dossie.template.html').read_text(encoding='utf8')

# fontes embutidas
faces=json.load(open(f'{S}/fonts_min.json'))
css="\n".join(
 f"@font-face{{font-family:'{f['family']}';font-style:normal;font-weight:{f['weight']};"
 f"font-display:block;src:url(data:font/woff2;base64,{f['b64']}) format('woff2');"
 f"unicode-range:{f['range']};}}" for f in faces)
tpl=tpl.replace('__FONTS__',css)

# geometria
tpl=tpl.replace('__GEO__', pathlib.Path(f'{S}/geo.json').read_text(encoding='utf8'))
tpl=tpl.replace('__DRAW__', pathlib.Path('draw.js').read_text(encoding='utf8'))

# figuras
def img(p):
    return "data:image/png;base64,"+base64.b64encode(pathlib.Path(p).read_bytes()).decode()
for key,fn in [('__FIG_ISO__','fig_montado_iso.png'),('__FIG_PINO__','fig_pino.png'),
               ('__FIG_DIA__','fig_dia.png'),('__FIG_MES__','fig_mes.png'),
               ('__FIG_DIA2__','fig_dia.png'),('__FIG_MAPA__','fig_dia_mapa.png'),
               ('__FIG_TOPO__','fig_montado_topo.png'),('__FIG_FUNDO__','fig_dia_fundo.png')]:
    tpl=tpl.replace(key, img(f'{S}/{fn}'))
pathlib.Path('dossie.build.html').write_text(tpl,encoding='utf8')
print('html', round(len(tpl)/1e6,2),'MB')

from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    pg=b.new_page(color_scheme='light')
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto(pathlib.Path('dossie.build.html').absolute().as_uri())
    pg.wait_for_timeout(2500)
    pg.emulate_media(media='print')
    foot=('<div style="width:100%;font-family:\'IBM Plex Mono\',monospace;font-size:6.6pt;color:#7B8587;'
          'padding:0 17mm;display:flex;justify-content:space-between;border-top:0.4pt solid #C2CACA;'
          'padding-top:2mm;margin-top:2mm;">'
          '<span>Nitron &middot; Chrono — datador em três peças &middot; conceito, 31 ago 2026</span>'
          '<span><span class="pageNumber"></span>/<span class="totalPages"></span></span></div>')
    pg.pdf(path='/home/user/produtos/chrono/pdf/Chrono_Datador_dossie.pdf', format='A4',
           print_background=True, display_header_footer=True,
           header_template='<div></div>', footer_template=foot,
           margin={'top':'19mm','right':'17mm','bottom':'17mm','left':'17mm'},
           prefer_css_page_size=False)
    b.close()
print('erros JS:', errs or 'nenhum')
