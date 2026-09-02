// Gera o PDF A4 de um relatorio da pasta analise/ a partir do HTML dele.
//
// Uso:  node analise/build-pdf.mjs [nome-base ...]
//       node analise/build-pdf.mjs                      # gera todos os relatorios conhecidos
//       node analise/build-pdf.mjs 07-cnae-mercado-rondonia
// Requer: playwright + Chromium (PLAYWRIGHT_BROWSERS_PATH aponta para o browser)
//
// Duas armadilhas que custaram tempo e estao resolvidas aqui:
//
//  1. NAO declarar `margin` em @page. A margem de @page sobrepoe a passada ao
//     page.pdf(), o conteudo passa a usar a pagina inteira e colide com o rodape.
//
//  2. Pedir as fontes ao Google com User-Agent ANTIGO. Com UA moderno o Google
//     serve fontes VARIAVEIS, e o Chromium as embute como Type 3 (glifos
//     desenhados), o que aperta o espaco entre palavras e incha o arquivo. Com
//     UA de Chrome 60 ele serve instancias ESTATICAS, embutidas como CID TrueType.
//     As fontes vao embutidas em data URI porque o Chromium deste ambiente nao
//     alcanca fonts.googleapis.com pelo proxy (o curl alcanca).

import { chromium } from 'playwright';
import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve(import.meta.dirname, '..');
const CACHE = path.join(ROOT, '.fontcache');
const RELATORIOS = ['06-filial-cd-rondonia', '07-cnae-mercado-rondonia'];
const alvos = process.argv.slice(2).length ? process.argv.slice(2) : RELATORIOS;

const UA_LEGACY = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
  + '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36';
const FAMILIES = [
  'Archivo:wght@500;600;700',
  'Source+Serif+4:ital,wght@0,400;0,600;1,400',
  'IBM+Plex+Mono:wght@400;500;600',
];
const SUBSETS = new Set(['latin', 'latin-ext']);

const curl = (url) => execFileSync('curl', ['-sSf', '-A', UA_LEGACY, url], { maxBuffer: 1 << 26 });

function embeddedFontCss() {
  fs.mkdirSync(CACHE, { recursive: true });
  const blocks = [];
  for (const spec of FAMILIES) {
    const css = curl(`https://fonts.googleapis.com/css2?family=${spec}&display=swap`).toString();
    const re = /\/\*\s*([\w-]+)\s*\*\/\s*(@font-face\s*\{[\s\S]*?\})/g;
    for (const m of css.matchAll(re)) {
      if (!SUBSETS.has(m[1])) continue;
      const u = m[2].match(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+\.woff2)\)/);
      if (!u) continue;
      const file = path.join(CACHE, path.basename(u[1]));
      if (!fs.existsSync(file)) fs.writeFileSync(file, curl(u[1]));
      const buf = fs.readFileSync(file);
      if (buf.subarray(0, 4).toString() !== 'wOF2') throw new Error('woff2 invalido: ' + file);
      blocks.push(m[2]
        .replace(u[1], 'data:font/woff2;base64,' + buf.toString('base64'))
        .replace(/\s*unicode-range:[^;]+;/, ''));
    }
  }
  if (!blocks.length) throw new Error('nenhuma fonte embutida');
  return blocks.join('\n');
}

const printCss = `<style>/* NAO declarar margin aqui: @page.margin sobrepoe a margem passada ao pdf() e o
   conteudo passa a usar a pagina inteira, colidindo com o rodape. */
@page { size: A4; }
html, body { background:#FFFFFF !important; }
body {
  font-size: 10.4pt; line-height: 1.55;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.wrap { max-width: none; padding: 0 0 0 0; }
#tip { display: none !important; }

/* --- ritmo de pagina --- */
header { padding-top: 0; }
h1 { font-size: 30pt; letter-spacing:-.02em; }
.standfirst { font-size: 13pt; max-width: 52ch; }
.byline { font-size: 8pt; }
.eyebrow { font-size: 7.6pt; }

.verdict { break-inside: avoid; margin-top: 22pt; padding: 16pt 18pt; }
.verdict h2 { font-size: 16pt; }
.verdict p { font-size: 10.4pt; }

.figs { break-inside: avoid; margin-top: 16pt; grid-template-columns: repeat(4, 1fr); }
.fig { padding: 10pt 12pt 9pt; }
.fig dt { font-size: 7.4pt; margin-bottom: 5pt; }
.fig dd { font-size: 17pt; }
.fig .sub { font-size: 8.4pt; margin-top: 4pt; }

/* pagina 1 = masthead + recomendacao + numeros; as secoes fluem naturalmente depois */
section { margin-top: 24pt; break-before: auto; }
section:first-of-type { break-before: page; margin-top: 0; }
.snum, h2.sec, h3 { break-after: avoid; }
h2.sec + p, h2.sec + .col, .snum + h2.sec { break-before: avoid; }
h2.sec { font-size: 18pt; padding-bottom: 8pt; break-after: avoid; }
.snum { font-size: 8pt; margin-bottom: 6pt; break-after: avoid; }
h3 { font-size: 12pt; margin: 18pt 0 6pt; break-after: avoid; }
p { margin-bottom: 10pt; orphans: 3; widows: 3; }
.col { max-width: 62ch; }

/* --- tabelas: cabem na largura da pagina, nao quebram no meio --- */
.tw { break-inside: avoid; overflow: visible; margin: 14pt 0 6pt; }
table { min-width: 0; width: 100%; font-size: 8.4pt; table-layout: auto; }
caption { font-size: 7.4pt; padding: 9pt 10pt 6pt; }
th, td { padding: 5pt 10pt; white-space: normal; }
thead th { font-size: 7.6pt; }
tbody td { font-size: 8.2pt; }
tbody td:first-child, tbody td.tl { font-size: 8.8pt; }
th:first-child, td:first-child { min-width: 0; }
th.tl, td.tl { min-width: 0; }
.tnote { font-size: 8.4pt; margin-bottom: 2pt; }

/* --- graficos --- */
figure { break-inside: avoid; margin: 18pt 0 6pt; padding: 14pt 14pt 10pt; }
figure h4 { font-size: 11.5pt; }
figure .sub { font-size: 8.8pt; margin-bottom: 10pt; }
figure svg { width: 100%; }
figcaption { font-size: 8.4pt; margin-top: 9pt; max-width: none; }
.cw { overflow: visible; }
.cl { font-size: 11.5px; } .ct { font-size: 10.5px; } .cv { font-size: 11px; }
.bar:hover { opacity: 1; }

.note { break-inside: avoid; margin: 16pt 0; padding: 13pt 15pt; }
.note p { font-size: 10pt; margin-bottom: 8pt; }
.note .lab { font-size: 7.6pt; margin-bottom: 6pt; }

ul, ol { margin-bottom: 10pt; break-inside: auto; }
li { margin-bottom: 7pt; break-inside: auto; orphans: 2; widows: 2; }

.gate { break-inside: avoid; margin-top: 14pt; }
.gate .row { padding: 10pt 13pt; }
.gate .row div { font-size: 9.6pt; }
.gate .row .k { font-size: 7.4pt; }
.gate .box { width: 11px; height: 11px; margin-top: 3px; }

footer { margin-top: 26pt; padding-top: 12pt; font-size: 8.6pt; max-width: none; break-inside: avoid; }
footer .lab { font-size: 7.6pt; }</style>`;
const footTemplate = `<div style="width:100%; padding:0 16mm; font-family:'IBM Plex Mono',monospace; font-size:7pt; color:#7C847E;
            display:flex; justify-content:space-between; align-items:center; border-top:0.5pt solid #DBDED7; padding-top:3mm;">
  <span>Nitron &middot; Projeto de Desenvolvimento de Produtos &middot; __TITULO__</span>
  <span>02 set 2026 &middot; <span class="pageNumber"></span>/<span class="totalPages"></span></span>
</div>`;

const fontCss = embeddedFontCss();   // baixa uma vez, reusa em todos os relatorios

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });

for (const base of alvos) {
  const SRC = path.join(ROOT, `analise/${base}.html`);
  const OUT = path.join(ROOT, `analise/${base}.pdf`);
  if (!fs.existsSync(SRC)) { console.error('sem HTML para ' + base + ', pulando'); continue; }

  const report = fs.readFileSync(SRC, 'utf8')
    .replace(/<link rel="preconnect"[^>]*>\s*/g, '')
    .replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>/,
             '<style>' + fontCss + '</style>');
  if (report.includes('fonts.googleapis.com')) throw new Error('link do Google Fonts nao foi substituido em ' + base);

  const titulo = (report.match(/<title>(.*?)<\/title>/) || [, base])[1];

  // o artifact e um fragmento: envolve no mesmo esqueleto que o publicador usa
  const html = '<!doctype html><html lang="pt-BR" data-theme="light"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width,initial-scale=1">'
    + '<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'
    + '</head><body>' + report + printCss + '</body></html>';
  const tmp = path.join(ROOT, `.print-${base}.html`);
  fs.writeFileSync(tmp, html);

  const page = await browser.newPage();
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(2500);
  await page.pdf({
    path: OUT,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: footTemplate.replace('__TITULO__', titulo),
    margin: { top: '16mm', right: '16mm', bottom: '20mm', left: '16mm' },
  });
  await page.close();
  fs.unlinkSync(tmp);
  console.log('gerado: ' + path.relative(ROOT, OUT));
}
await browser.close();
