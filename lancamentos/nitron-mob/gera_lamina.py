"""Gera a lâmina de lançamento Nitron Mob (HTML -> PNG via Chromium headless).

Preço = Tabela Padrão (CODTAB 0, PV0003), vigência 24/06/2026, consultado em 14/10/2026.
Sugerido = preço x 2 (markup de 100%).
"""
import pathlib, subprocess

AQUI = pathlib.Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

def brl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

# ---------- ícones (traço simples, ilustrativos) ----------
STK = 'fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'

def ico_arara():
    return f'''<svg viewBox="0 0 200 160" {STK}>
      <path d="M40 30 H160"/><path d="M50 30 V140"/><path d="M150 30 V140"/>
      <path d="M30 140 H70"/><path d="M130 140 H170"/><path d="M50 112 H150"/>
      <path d="M78 30 v10 l-16 22 h32 z"/><path d="M110 30 v10 l-14 22 h28 z"/>
      <path d="M134 30 v10 l-10 22 h20 z"/></svg>'''

def ico_sapateira(n):
    h = 30 + n * 28
    y0 = 150 - h
    lines = "".join(f'<path d="M45 {y0 + 14 + i*28} H155"/><path d="M60 {y0 + 36 + i*28} q8 -10 22 -4 h10 v4 h-32 z" stroke-width="4"/><path d="M110 {y0 + 36 + i*28} q8 -10 22 -4 h10 v4 h-32 z" stroke-width="4"/>' for i in range(n))
    return f'''<svg viewBox="0 0 200 160" {STK}>
      <rect x="40" y="{y0}" width="120" height="{h}" rx="6"/>{lines}</svg>'''

def ico_suporte():
    return f'''<svg viewBox="0 0 200 160" {STK}>
      <path d="M30 70 H170"/><path d="M55 70 V110 L80 70"/><path d="M145 70 V110 L120 70"/>
      <path d="M55 40 v30"/><path d="M62 70 c0 -22 10 -28 18 -28 c8 0 10 14 4 28"/>
      <rect x="120" y="42" width="26" height="28" rx="3"/></svg>'''

def ico_prateleira(n, w):
    W = {"P": 70, "M": 100, "G": 130}[w]
    x0 = 100 - W / 2
    h = 120
    ys = [30 + i * (h / (n - 1)) for i in range(n)]
    tiers = "".join(f'<path d="M{x0-6} {y:.0f} H{x0+W+6}"/>' for y in ys)
    return f'''<svg viewBox="0 0 200 160" {STK}>
      <path d="M{x0} 24 V152"/><path d="M{x0+W} 24 V152"/>{tiers}</svg>'''

# ---------- produtos ----------
DESTAQUES = [
    ("Arara de Roupa", "850.004.N03", 180.19, ico_arara()),
    ("Sapateira Pequena", "851.004.N03", 64.01, ico_sapateira(2)),
    ("Sapateira Grande", "852.004.N03", 149.68, ico_sapateira(4)),
    ("Kit Suporte Decorativo M", "853.004.N03", 122.99, ico_suporte()),
]
PRATELEIRAS = {  # (tamanho, prateleiras): (ref, preço)
    ("P", 2): ("861.004.N03", 94.06), ("P", 3): ("862.004.N03", 133.61), ("P", 4): ("863.004.N03", 170.82),
    ("M", 2): ("858.004.N03", 97.66), ("M", 3): ("859.004.N03", 143.15), ("M", 4): ("860.004.N03", 187.16),
    ("G", 2): ("855.004.N03", 114.36), ("G", 3): ("856.004.N03", 168.32), ("G", 4): ("857.004.N03", 218.24),
}

def preco_html(v, grande=True):
    r, c = brl(v).split(",")
    return f'''<div class="preco {'grande' if grande else ''}"><span class="rs">R$</span><span class="int">{r}</span><span class="cent">,{c}</span></div>
      <div class="sug"><span>Preço sugerido de venda</span><b>R$ {brl(v*2)}</b></div>'''

cards = "".join(f'''<div class="card">
    <div class="ico">{svg}</div>
    <div class="nome">{nome}</div><div class="ref">Ref. {ref}</div>
    {preco_html(p)}</div>''' for nome, ref, p, svg in DESTAQUES)

prat = ""
for n in (2, 3, 4):
    for t in ("P", "M", "G"):
        ref, p = PRATELEIRAS[(t, n)]
        prat += f'''<div class="cell">
      <div class="ico sm">{ico_prateleira(n, t)}</div>
      <div class="nome">Prateleira Multiuso <span class="tag">{t} · {n}P</span></div><div class="ref">Ref. {ref}</div>
      {preco_html(p, grande=False)}</div>'''

HTML = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
:root {{ --bg:#1f2326; --bg2:#2a2f33; --card:#ffffff; --ink:#1f2326; --mut:#6b7378; --lar:#ff6a13; --line:#e6e8ea; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ width:1440px; font-family:'Inter',sans-serif; background:var(--bg); color:#fff; }}
.wrap {{ padding:72px 72px 56px; background:
   radial-gradient(1200px 500px at 85% -5%, rgba(255,106,19,.28), transparent 60%), var(--bg); }}
header {{ display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:48px; }}
.kicker {{ font-weight:700; letter-spacing:.32em; font-size:22px; color:var(--lar); text-transform:uppercase; }}
h1 {{ font-family:'Inter Display','Inter',sans-serif; font-weight:900; font-size:132px; line-height:.9; letter-spacing:-.035em; margin-top:14px; }}
h1 span {{ color:var(--lar); }}
.sub {{ font-size:28px; color:#c9cdd0; margin-top:20px; font-weight:400; }}
.selo {{ width:210px; height:210px; border-radius:50%; background:var(--lar); display:flex; flex-direction:column;
   align-items:center; justify-content:center; text-align:center; transform:rotate(-8deg); flex:none; color:#fff;
   box-shadow:0 0 0 10px rgba(255,106,19,.25); }}
.selo b {{ font-size:64px; font-weight:900; line-height:1; letter-spacing:-.03em; }}
.selo small {{ font-size:17px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; line-height:1.25; margin-top:6px; }}
.grid4 {{ display:grid; grid-template-columns:repeat(4,1fr); gap:24px; }}
.card, .cell {{ background:var(--card); color:var(--ink); border-radius:22px; padding:26px 26px 24px; display:flex; flex-direction:column; }}
.ico {{ height:150px; color:var(--ink); display:flex; align-items:center; justify-content:center;
   background:#f3f4f5; border-radius:14px; margin-bottom:20px; }}
.ico svg {{ height:120px; }}
.ico.sm {{ height:120px; }} .ico.sm svg {{ height:96px; }}
.nome {{ font-weight:800; font-size:26px; line-height:1.15; letter-spacing:-.01em; }}
.ref {{ font-size:16px; color:var(--mut); margin-top:6px; font-weight:500; }}
.preco {{ display:flex; align-items:flex-start; color:var(--lar); margin:16px 0 18px; line-height:1; }}
.preco .rs {{ font-size:22px; font-weight:800; margin:8px 6px 0 0; }}
.preco .int {{ font-size:66px; font-weight:900; letter-spacing:-.04em; }}
.preco .cent {{ font-size:30px; font-weight:800; margin-top:6px; }}
.preco:not(.grande) .int {{ font-size:54px; }}
.sug {{ margin-top:auto; padding-top:14px; border-top:2px dashed var(--line); font-size:17px; color:var(--mut); display:flex; flex-direction:column; gap:4px; }}
.sug b {{ color:var(--ink); font-weight:800; font-size:28px; letter-spacing:-.01em; }}
.sec {{ display:flex; align-items:baseline; gap:20px; margin:56px 0 22px; }}
.sec h2 {{ font-size:44px; font-weight:900; letter-spacing:-.02em; }}
.sec p {{ font-size:22px; color:#c9cdd0; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }}
.tag {{ display:inline-block; background:var(--ink); color:#fff; border-radius:8px; padding:3px 10px; font-size:20px; vertical-align:2px; margin-left:4px; }}
footer {{ margin-top:48px; display:flex; justify-content:space-between; align-items:flex-end; gap:40px; }}
.brand {{ font-family:'Inter Display','Inter',sans-serif; font-size:56px; font-weight:900; letter-spacing:-.03em; }}
.brand span {{ color:var(--lar); }}
.nota {{ font-size:16px; color:#9aa1a6; line-height:1.55; max-width:820px; text-align:right; }}
</style></head><body><div class="wrap">
<header>
  <div><div class="kicker">Lançamento oficial</div>
    <h1>NITRON<span>-</span>MOB</h1>
    <div class="sub">Móveis e organização para todos os cômodos da casa.</div></div>
  <div class="selo"><b>100%</b><small>de markup<br>sugerido</small></div>
</header>
<div class="grid4">{cards}</div>
<div class="sec"><h2>Prateleira Multiuso</h2><p>3 tamanhos (P · M · G) &nbsp;×&nbsp; 2, 3 ou 4P</p></div>
<div class="grid3">{prat}</div>
<footer>
  <div class="brand">nitron<span>.</span></div>
  <div class="nota">Preço por peça na Tabela Padrão Nitron, vigente desde 24/06/2026. Venda em múltiplos de 4 unidades.<br>
  Preço sugerido de venda ao consumidor = 2× o preço de compra (markup de 100%). Imagens meramente ilustrativas.</div>
</footer>
</div></body></html>'''

html = AQUI / "lamina-nitron-mob.html"
html.write_text(HTML, encoding="utf-8")
png = AQUI / "lamina-nitron-mob.png"
subprocess.run([CHROME, "--headless", "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=2",
                "--window-size=1440,2480", f"--screenshot={png}", html.as_uri()], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(png)
