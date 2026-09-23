import asyncio, pathlib
from playwright.async_api import async_playwright
ARQ = pathlib.Path(__file__).parent / 'Chrono_Datador.html'
OUT = pathlib.Path(__file__).parent / 'prova'; OUT.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
              args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        pg = await b.new_page(viewport={'width':1100,'height':1000}, device_scale_factor=2)
        await pg.goto(ARQ.as_uri()); await pg.wait_for_timeout(3500)
        await pg.click('#btGira')
        await pg.click('.modo[data-modo="data"]')
        await pg.click('#btTopo'); await pg.wait_for_timeout(600)
        await pg.click('#btArestas')                       # sem arestas: numeral mais legivel
        for alvo in [(1,1),(8,3),(16,6),(28,12)]:
            d,m = alvo
            await pg.evaluate("() => { for (const b of document.querySelectorAll('.passo')) b.dataset.x=1; }")
            # zera e anda ate o alvo clicando (o estado vive em closure)
            await pg.click('#btHoje'); await pg.wait_for_timeout(50)
            cur_d = int(await pg.inner_text('#vDia')); cur_m = int(await pg.inner_text('#vMes'))
            for _ in range((d - cur_d) % 31): await pg.click('.passo[data-passo="dia"][data-d="1"]')
            for _ in range((m - cur_m) % 12): await pg.click('.passo[data-passo="mes"][data-d="1"]')
            await pg.wait_for_timeout(500)
            got = (await pg.inner_text('#vDia'), await pg.inner_text('#vMes'))
            await pg.locator('#stage').screenshot(path=str(OUT/('data_%02d_%02d.png'%(d,m))))
            print('  pedido %02d/%02d -> tela %s/%s' % (d, m, *got))
        await b.close()
asyncio.run(main())
