import asyncio, sys, pathlib, glob
from playwright.async_api import async_playwright
ARQ = pathlib.Path(__file__).parent / 'Chrono_Detalhes.html'
OUT = pathlib.Path(__file__).parent / 'prova_det'; OUT.mkdir(exist_ok=True)
EXE = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'))[-1]

async def main():
    erros = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=EXE,
            args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg = await b.new_page(viewport={'width':1280,'height':820}, device_scale_factor=2)
        pg.on('console', lambda m: erros.append('console.%s: %s'%(m.type,m.text)) if m.type=='error' else None)
        pg.on('pageerror', lambda e: erros.append('pageerror: %s'%e))
        await pg.goto(ARQ.as_uri()); await pg.wait_for_timeout(5000)
        print('WebGL2:', await pg.evaluate("!!document.createElement('canvas').getContext('webgl2')"))
        print('carregou:', await pg.evaluate("document.getElementById('carregando').hidden"))
        for modo in ('m01','m02','m03','conjunto'):
            await pg.click('.modo[data-modo="%s"]'%modo); await pg.wait_for_timeout(900)
            print('  %-9s %s | %s'%(modo, await pg.inner_text('#fTitulo'), await pg.inner_text('#escala')))
            await pg.screenshot(path=str(OUT/('%s.png'%modo)))
            await pg.click('#btVirar'); await pg.wait_for_timeout(700)
            await pg.screenshot(path=str(OUT/('%s_baixo.png'%modo)))
            await pg.click('#btVirar'); await pg.wait_for_timeout(300)
        # mapa de altura
        await pg.click('#btMapa'); await pg.wait_for_timeout(300)
        for modo in ('m03','m01','m02'):
            await pg.click('.modo[data-modo="%s"]'%modo); await pg.wait_for_timeout(700)
            await pg.screenshot(path=str(OUT/('mapa_%s.png'%modo)))
            await pg.click('#btVirar'); await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(OUT/('mapa_%s_baixo.png'%modo)))
            await pg.click('#btVirar'); await pg.wait_for_timeout(200)
        print('  escala com mapa:', await pg.inner_text('#escala'))
        await pg.click('#btMapa'); await pg.wait_for_timeout(200)
        # corte no conjunto
        await pg.click('.modo[data-modo="conjunto"]'); await pg.wait_for_timeout(600)
        await pg.click('#btCorte'); await pg.wait_for_timeout(300)
        print('  barra de corte visivel:', not await pg.get_attribute('#corteBarra','hidden') is not None)
        await pg.fill('#corteSlider','0'); await pg.dispatch_event('#corteSlider','input')
        await pg.wait_for_timeout(800)
        print('  corte em', await pg.inner_text('#corteVal'))
        await pg.screenshot(path=str(OUT/'conjunto_corte.png'))
        await b.close()
    print('\nerros:', erros if erros else 'nenhum')
    return 1 if erros else 0
sys.exit(asyncio.run(main()))
