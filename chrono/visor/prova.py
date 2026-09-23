import asyncio, sys, pathlib
from playwright.async_api import async_playwright
ARQ = pathlib.Path(__file__).parent / 'Chrono_Datador.html'
OUT = pathlib.Path(__file__).parent / 'prova'
OUT.mkdir(exist_ok=True)

async def main():
    erros = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--use-gl=angle','--use-angle=swiftshader',
                                          '--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width':1180,'height':760})
        pg.on('console', lambda m: erros.append('console.%s: %s' % (m.type, m.text)) if m.type in ('error','warning') else None)
        pg.on('pageerror', lambda e: erros.append('pageerror: %s' % e))
        await pg.goto(ARQ.as_uri())
        await pg.wait_for_timeout(4000)
        print('WebGL2:', await pg.evaluate("!!document.createElement('canvas').getContext('webgl2')"))
        print('carregando escondido:', await pg.evaluate("document.getElementById('carregando').hidden"))
        print('texto do carregando:', (await pg.inner_text('#carregando')).replace('\n',' | '))
        # trava o giro para a foto sair igual
        await pg.click('#btGira')
        for modo, extra in [('peca',None), ('moldes',None), ('tampa',None), ('data','datas')]:
            await pg.click('.modo[data-modo="%s"]' % modo)
            await pg.wait_for_timeout(900)
            print('  %-7s ficha: %s' % (modo, await pg.inner_text('#fTitulo')))
            await pg.screenshot(path=str(OUT/('%s.png'%modo)))
            if extra:
                await pg.click('#btTopo'); await pg.wait_for_timeout(700)
                await pg.screenshot(path=str(OUT/'data_topo.png'))
                for _ in range(5): await pg.click('.passo[data-passo="dia"][data-d="1"]')
                for _ in range(3): await pg.click('.passo[data-passo="mes"][data-d="1"]')
                await pg.wait_for_timeout(700)
                print('       dia/mes agora: %s / %s' % (await pg.inner_text('#vDia'), await pg.inner_text('#vMes')))
                await pg.screenshot(path=str(OUT/'data_topo_mudada.png'))
        await b.close()
    print('\nerros/avisos:', erros if erros else 'nenhum')
    return 1 if any('pageerror' in e or 'console.error' in e for e in erros) else 0

sys.exit(asyncio.run(main()))
