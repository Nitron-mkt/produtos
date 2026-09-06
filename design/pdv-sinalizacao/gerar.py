# -*- coding: utf-8 -*-
"""Gera os artboards da sinalizacao do PDV Nitron Mob a partir dos vetores
oficiais do kit de marca (marca.nitron.com.br). Nada de logo redesenhado:
os paths sao os do .ai, compostos segundo as proporcoes do lockup vertical."""
import re, pathlib, json
K = pathlib.Path('/tmp/claude-0/-home-user-produtos/a90e79dc-9d6b-5cf3-8b87-00e7e5301ee0/scratchpad/marca')
def paths(f):
    s = (K/'nitron-logos'/'logos'/f).read_text()
    return ''.join(re.findall(r'<path[^>]*/>', s))
MARK, WORD, TAG, FULL = paths('nitron-mark.svg'), paths('nitron-word.svg'), paths('nitron-tag.svg'), paths('nitron-full.svg')
def icon(name):
    s = (K/'nitron-icones'/'icones'/name).read_text()
    vb = re.search(r'viewBox="([^"]*)"', s).group(1)
    inner = re.sub(r'^.*?<svg[^>]*>', '', s, flags=re.S); inner = re.sub(r'</svg>\s*$', '', inner, flags=re.S)
    return vb, inner

# geometria do lockup vertical, lida do proprio SVG (108.05..255.31 x 105.49..245.95)
MW, MH = 67.16, 80.01          # simbolo
WW, WH = 147.26, 40.78         # lettering
TW, TH = 110.45, 11.71         # assinatura "toda casa tem"
GAP_WT = 234.24 - 226.28       # 7.96 entre lettering e assinatura, como no lockup oficial
STACK_H = WH + GAP_WT + TH     # 60.45
s_m = STACK_H / MH             # simbolo ocupa a altura da pilha lettering+assinatura
mw = MW * s_m                  # 50.74
GAP_MW = 12
HX = mw + GAP_MW               # 62.74
TX = HX + (WW - TW) / 2        # assinatura centrada no eixo do lettering
HW = HX + WW                   # 210.0

def lockup_h(cls='', slogan=True, style=''):
    """Lockup horizontal: simbolo + lettering, assinatura sob o lettering (75%, centrada)."""
    g = ('<g transform="scale(%.5f) translate(-148.10,-105.49)">%s</g>' % (s_m, MARK) +
         '<g transform="translate(%.2f,0) translate(-108.05,-185.50)">%s</g>' % (HX, WORD))
    if slogan:
        g += '<g transform="translate(%.2f,%.2f) translate(-126.45,-234.24)">%s</g>' % (TX, WH+GAP_WT, TAG)
    h = STACK_H if slogan else WH
    return ('<svg viewBox="0 0 %.2f %.2f" fill="currentColor" fill-rule="nonzero" class="%s" style="%s" '
            'role="img" aria-label="Nitron%s">%s</svg>' % (HW, h, cls, style, ' · toda casa tem' if slogan else '', g))
def lockup_v(cls='', slogan=True, style=''):
    if slogan:
        return '<svg viewBox="108.05 105.49 147.26 140.45" fill="currentColor" fill-rule="nonzero" class="%s" style="%s" role="img" aria-label="Nitron · toda casa tem">%s</svg>' % (cls, style, FULL)
    return '<svg viewBox="108.05 105.49 147.26 120.79" fill="currentColor" fill-rule="nonzero" class="%s" style="%s" role="img" aria-label="Nitron">%s%s</svg>' % (cls, style, MARK, WORD)
def nested(svg, w, h):
    """Um <svg> dentro de outro precisa de width E height explicitos."""
    return svg.replace('<svg ', '<svg width="%s" height="%s" ' % (w, h), 1)

def word(cls='', style=''):
    return '<svg viewBox="108.05 185.50 147.26 40.78" fill="currentColor" fill-rule="nonzero" class="%s" style="%s" role="img" aria-label="Nitron">%s</svg>' % (cls, style, WORD)
def tag(cls='', style=''):
    return '<svg viewBox="126.45 234.24 110.45 11.71" fill="currentColor" fill-rule="nonzero" class="%s" style="%s" role="img" aria-label="toda casa tem">%s</svg>' % (cls, style, TAG)

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Montserrat:wght@400;500;700;900&amp;family=Aleo:ital,wght@0,400;0,700;1,400&amp;display=swap">'
BASE_CSS = '''
    body{margin:0;background:#FFF7EA;font-family:Montserrat,Gotham,"Segoe UI",sans-serif;color:#131E29;-webkit-font-smoothing:antialiased}
    a{color:#131E29} a:hover{color:#1EA7AC}
    .bebas{font-family:"Bebas Neue","Bebas Neue Pro",Impact,sans-serif;letter-spacing:.14em}
    .aleo{font-family:Aleo,Georgia,serif}
    .spec{font-family:"Bebas Neue",Impact,sans-serif;letter-spacing:.12em;font-size:13px;color:#6B7680}
    .cota{font-family:Montserrat,sans-serif;font-size:11px;color:#6B7680;font-variant-numeric:tabular-nums}
'''
PROPS = '{"verde":{"editor":"color","default":"#08a9b1","options":["#08a9b1","#1EA7AC","#00AFAA"],"section":"Marca"}}'
LOGIC = '''<script data-dc-script data-props='%s'>
class Component extends DCLogic {
  renderVals() { return { verde: this.props.verde ?? '#08a9b1' }; }
}
</script>''' % PROPS

def page(body, css='', w=None, h=None):
    return ('<!doctype html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n  %s\n  <style>%s%s</style>\n</helmet>\n%s\n</x-dc>\n%s\n</body>\n</html>\n'
            % (FONTS, BASE_CSS, css, body, LOGIC))

# ================================================================ TESTEIRA
# 754 x 200 mm a 2 px/mm. Manual: fundo verde solido, lockup horizontal com
# assinatura, centrado, 55% da largura util. Area de protecao = 1x altura do simbolo.
def testeira():
    W, H = 1508, 400
    logo_w = int(W * 0.55)              # 829 px = 415 mm
    body = f'''
<div style="width:{W}px;padding:0 0 28px 0;display:flex;flex-direction:column;gap:14px">
  <div style="width:{W}px;height:{H}px;background:{{{{verde}}}};display:flex;align-items:center;justify-content:center;color:#fff">
    {lockup_h(style=f'width:{logo_w}px;height:auto;display:block')}
  </div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;padding:0 4px">
    <span class="spec">TESTEIRA · 1 POR VÃO · 754 × 200 mm · ESCALA 2 px/mm</span>
    <span class="cota">lockup horizontal com assinatura · 55% da largura útil = 415 mm · fundo sólido · nunca dividida entre marcas · montada em hastes nos nós de topo, base a 1.900 mm</span>
  </div>
</div>'''
    return page(body), W, H+60

# ================================================================ FAIXA
# 754 x 40 mm. Manual: >= 30 mm, lettering isolado a esquerda, categoria em Bebas a direita.
AMB = [('COZINHA','1-02-COZINHA.svg'),('ORGANIZAÇÃO','1-01-ORGANIZACAO.svg'),
       ('BANHO E LAVANDERIA','1-06-BANHEIRO.svg'),('FRASQUEIRAS E INFANTIL','0-03-FRASQUEIRAS.svg')]
def faixa():
    W, H = 1508, 80
    rows = ''
    for nome, ic in AMB:
        rows += f'''
  <div style="width:{W}px;height:{H}px;background:{{{{verde}}}};display:flex;align-items:center;justify-content:space-between;padding:0 28px;color:#fff">
    {word(style='height:34px;width:auto;display:block')}
    <span class="bebas" style="font-size:44px;line-height:1;letter-spacing:.14em;padding-top:4px">{nome}</span>
  </div>'''
    body = f'''
<div style="width:{W}px;display:flex;flex-direction:column;gap:22px;padding-bottom:28px">{rows}
  <div style="display:flex;justify-content:space-between;align-items:baseline;padding:0 4px">
    <span class="spec">FAIXA DE PRATELEIRA · 1 POR VÃO · 754 × 40 mm · ESCALA 2 px/mm</span>
    <span class="cota">altura mínima do manual 30 mm; 40 cobre a borda de 15 mm do painel com sobra · lettering isolado à esquerda, categoria em Bebas +14% à direita</span>
  </div>
</div>'''
    return page(body), W, 4*H+3*22+60

# ================================================================ STOPPER
# 100 x 150 mm, duas faces. Face A (manual): lockup vertical, logo 70% da largura,
# assinatura embaixo. Face B: a frase da campanha -- complemento no titulo, nunca no logo.
COPY = {
 'COZINHA':                 ('toda casa tem', 'comida guardada'),
 'ORGANIZAÇÃO':             ('toda casa tem', 'bagunça'),
 'BANHO E LAVANDERIA':      ('toda casa tem', 'roupa pra lavar'),
 'FRASQUEIRAS E INFANTIL':  ('toda casa tem', 'remédio guardado'),
}
def stopper():
    W, H = 200, 300   # 100 x 150 mm
    logo_w = int(W*0.70)
    faces = ''
    for nome,_ in AMB:
        a, b = COPY[nome]
        faces += f'''
  <div style="display:flex;flex-direction:column;gap:10px;align-items:center">
    <div style="display:flex;gap:16px">
      <div style="width:{W}px;height:{H}px;background:{{{{verde}}}};border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:26px 0 22px;color:#fff">
        {lockup_v(slogan=False, style=f'width:{logo_w}px;height:auto;display:block')}
        {tag(style=f'width:{int(logo_w*0.75)}px;height:auto;display:block')}
      </div>
      <div style="width:{W}px;height:{H}px;background:#FFF7EA;border:1.5px solid {{{{verde}}}};border-radius:6px;display:flex;flex-direction:column;justify-content:space-between;padding:22px 18px 18px;color:#131E29">
        <div class="aleo" style="font-size:24px;line-height:1.18;text-wrap:balance"><span style="color:{{{{verde}}}}">{a}</span><br>{b}</div>
        {word(style='width:64px;height:auto;display:block;color:#131E29')}
      </div>
    </div>
    <span class="cota">{nome.title().replace(' E ',' e ')}</span>
  </div>'''
    body = f'''
<div style="display:flex;flex-direction:column;gap:22px;padding-bottom:28px">
  <div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:36px 44px">{faces}</div>
  <div style="display:flex;flex-direction:column;gap:4px;padding:0 4px;max-width:900px">
    <span class="spec">STOPPER · 2 FACES · 100 × 150 mm · ESCALA 2 px/mm · 1 POR PONTA DE PAREDE, NA PRIMEIRA PRATELEIRA DA ZONA DOS OLHOS</span>
    <span class="cota">face A é o manual: logo 70% da largura, sem assinatura no lockup, assinatura volta embaixo. Face B é a campanha: o complemento vive no título, em Aleo, minúsculas, sem ponto — nunca dentro do logo.</span>
  </div>
</div>'''
    return page(body), 2*(2*W+16)+44+8, 2*(H+30)+36+90

# ================================================================ WOBBLER
# diametro 100 mm. Manual: logo 65% do diametro, sem assinatura; amarelo permitido
# (regra dos 5%), logo em grafite sobre amarelo.
WOB = [('Pote 2 L', 'cabe a sobra do almoço'),
       ('Frasqueira Medicamentos', 'o remédio no lugar'),
       ('Lixeira Rattan com Pedal', 'abre sem encostar a mão'),
       ('Organizador Multiuso', 'a gaveta fecha de novo')]
def wobbler():
    D = 200
    logo_w = int(D*0.65)
    items = f'''
  <div style="display:flex;flex-direction:column;align-items:center;gap:10px">
    <div style="flex:none;width:{D}px;height:{D}px;border-radius:50%;background:#FFD500;display:flex;align-items:center;justify-content:center;color:#131E29">
      {lockup_v(slogan=False, style=f'width:{logo_w}px;height:auto;display:block')}
    </div><span class="cota">frente · manual</span>
  </div>'''
    for prod, frase in WOB:
        items += f'''
  <div style="display:flex;flex-direction:column;align-items:center;gap:10px">
    <div style="flex:none;width:{D}px;height:{D}px;border-radius:50%;background:#FFD500;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:0 22px;text-align:center;color:#131E29">
      <span class="aleo" style="font-size:19px;line-height:1.15;text-wrap:balance">{frase}</span>
      {word(style='width:54px;height:auto;display:block')}
    </div><span class="cota">verso · {prod}</span>
  </div>'''
    body = f'''
<div style="display:flex;flex-direction:column;gap:22px;padding-bottom:28px">
  <div style="display:flex;gap:28px">{items}</div>
  <div style="display:flex;flex-direction:column;gap:4px;padding:0 4px;max-width:1000px">
    <span class="spec">WOBBLER · Ø 100 mm · ESCALA 2 px/mm · SÓ NOS 25 SKUs ACIMA DE R$ 500 MIL</span>
    <span class="cota">amarelo #FFD500 é o acento de 5% do manual, e o wobbler é onde ele mora. Logo em grafite sobre amarelo, 65% do diâmetro, sem assinatura. O verso leva a cena do produto — frase curta, presente, sem superlativo.</span>
  </div>
</div>'''
    return page(body), 5*D+4*28+8, D+30+90

# ================================================================ ONDE VAI
# Elevacao da parede de entrada: modulo 6.548 x 1.626, testeira 200, parede ate 3.400.
def onde():
    S = 0.20                    # px por mm
    LW, MH_, TH_, CEIL = 6548, 1626, 200, 3400
    TB = 1900               # base da testeira: 1633 da ultima face + ~270 de produto
    W = int(LW*S); H = int(CEIL*S)
    x0, y_floor = 130, 40+H
    def y(mm): return y_floor - mm*S
    vao = 415+42.02             # 457 externo por vao (PSC-02)
    N = 15
    faces = [100,605,1110,1372,1633]
    els = []
    # parede do predio
    els.append(f'<rect x="{x0}" y="{y(CEIL):.1f}" width="{W}" height="{H}" fill="#F3EDE0"/>')
    els.append(f'<rect x="{x0}" y="{y(MH_):.1f}" width="{W}" height="{MH_*S:.1f}" fill="#FAF6EC"/>')
    # manifesto na parede, acima da testeira
    mid = x0 + W/2
    els.append(f'<g transform="translate({mid-85:.1f},{y(3180):.1f})">' + nested(lockup_v(style='color:#131E29'), 170, 162) + '</g>')
    els.append(f'<text x="{mid:.1f}" y="{y(2200):.1f}" text-anchor="middle" class="aleo" font-size="15" fill="#131E29">toda casa tem uma frasqueira <tspan fill="#8A939B">— e uma história dentro dela</tspan></text>')
    # testeira
    # hastes a partir dos nos de topo (porta-haste), sustentando a testeira acima do produto
    for i in range(0, N+1, 3):
        xp = x0 + i*vao*S
        els.append(f'<rect x="{xp-0.8:.1f}" y="{y(TB):.1f}" width="1.6" height="{(TB-MH_)*S:.1f}" fill="#8A939B"/>')
    els.append(f'<rect x="{x0}" y="{y(TB+TH_):.1f}" width="{W}" height="{TH_*S:.1f}" fill="{{{{verde}}}}"/>')
    els.append(f'<g transform="translate({mid-45:.1f},{y(TB+TH_)+7:.1f})">' + nested(lockup_h(style='color:#fff'), 90, 26) + '</g>')
    # modulo: postes, prateleiras, faixas
    for i in range(N+1):
        xp = x0 + i*vao*S
        els.append(f'<rect x="{xp-1.2:.1f}" y="{y(MH_):.1f}" width="2.4" height="{MH_*S:.1f}" fill="#B6BFC6"/>')
    for k,h in enumerate(faces):
        els.append(f'<rect x="{x0}" y="{y(h)-3:.1f}" width="{W}" height="3" fill="#C4CCD2"/>')
        els.append(f'<rect x="{x0}" y="{y(h):.1f}" width="{W}" height="{40*S:.1f}" fill="{{{{verde}}}}" opacity=".9"/>')   # faixa 40 mm
    # produto (frasqueiras) na de 1633 e 1372
    import random; random.seed(3)
    for h,n in ((1633,34),(1372,5)):
        xs = x0+8
        for j in range(n):
            w_ = random.choice([22,26,30]); hh = random.choice([26,34,40])
            if xs+w_ > x0+W-8: break
            els.append(f'<rect x="{xs:.1f}" y="{y(h)-3-hh:.1f}" width="{w_}" height="{hh}" rx="2" fill="#fff" stroke="#C4CCD2"/>')
            xs += w_+6
    # stopper na ponta direita, prateleira 1372
    els.append(f'<rect x="{x0+W+4}" y="{y(1372)-30:.1f}" width="20" height="30" rx="1.5" fill="{{{{verde}}}}"/>')
    # wobbler na de 1633, a 1/3
    wx = x0 + W*0.33
    els.append(f'<line x1="{wx:.1f}" y1="{y(1633):.1f}" x2="{wx:.1f}" y2="{y(1633)+22:.1f}" stroke="#8A939B" stroke-width="1"/>')
    els.append(f'<circle cx="{wx:.1f}" cy="{y(1633)+32:.1f}" r="10" fill="#FFD500"/>')
    # ancoragem: 4 pontos na ripa traseira do topo, em nós (a cada 4 vaos)
    for i in (0,4,8,12):
        xp = x0 + (i+0.5)*vao*S
        els.append(f'<circle cx="{xp:.1f}" cy="{y(MH_)+6:.1f}" r="3.2" fill="none" stroke="#131E29" stroke-width="1.2"/>')
        els.append(f'<line x1="{xp-2:.1f}" y1="{y(MH_)+6:.1f}" x2="{xp+2:.1f}" y2="{y(MH_)+6:.1f}" stroke="#131E29" stroke-width="1.2"/>')
    # piso
    els.append(f'<rect x="{x0-20}" y="{y_floor:.1f}" width="{W+60}" height="14" fill="#E4DCCB"/>')
    # cotas
    def cota(y_, txt, x=None):
        els.append(f'<text x="{x0-8}" y="{y_+4:.1f}" text-anchor="end" class="cota">{txt}</text>')
    for h in (1372,1110,605,100): cota(y(h), f'{h}')
    cota(y(TB+TH_), f'{TB+TH_} topo da testeira')
    cota(y(TB), f'{TB} base da testeira')
    cota(y(MH_), f'{MH_} topo · face 1633')
    cota(y(CEIL), f'{CEIL} teto')
    # callouts numerados
    def call(n, x_, y_, dx=14, dy=-14):
        els.append(f'<line x1="{x_:.1f}" y1="{y_:.1f}" x2="{x_+dx:.1f}" y2="{y_+dy:.1f}" stroke="#131E29" stroke-width="1"/>')
        els.append(f'<circle cx="{x_+dx+8:.1f}" cy="{y_+dy-6:.1f}" r="9" fill="#131E29"/>')
        els.append(f'<text x="{x_+dx+8:.1f}" y="{y_+dy-6+3.5:.1f}" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="10" fill="#fff">{n}</text>')
    call(1, mid+110, y(3050), 40, -6)
    call(2, x0+W-60, y(TB+TH_/2), 30, -30)
    call(3, x0+W*0.6, y(1110)+4, 30, 34)
    call(4, x0+W+14, y(1372)-15, 26, -20)
    call(5, wx+10, y(1633)+32, 40, 6)
    call(6, x0+(4.5)*vao*S, y(MH_)+6, -30, 30)
    leg = [('1','Manifesto na parede do prédio, acima do móvel — o único lugar onde o "toda casa tem" ganha complemento, e ele vive no título, não no logo. Lockup vertical em grafite sobre creme.'),
           ('2','Testeira, 754 × 200 mm por vão, fundo verde, lockup horizontal a 55% da largura. Sobe em hastes a partir dos nós de topo — base a 1.900, para o produto da prateleira de 1.633 não ficar escondido atrás dela.'),
           ('3','Faixa de prateleira, 40 mm, em todas as prateleiras. Lettering isolado à esquerda, ambiente em Bebas à direita.'),
           ('4','Stopper de duas faces na ponta da parede, na prateleira de 1.372 mm — quem entra vê a face da campanha, quem sai vê o logo.'),
           ('5','Wobbler amarelo só nos campeões — aqui a Frasqueira Medicamentos 2,8 L, o SKU nº 1 do catálogo, a 1.633 mm.'),
           ('6','Ancoragem: 4 pontos pela ripa de largura traseira do último nível, sempre num nó, a cada 4 vãos. Passo de montagem, não acessório.')]
    legend = ''.join(f'<div style="display:flex;gap:10px;align-items:flex-start"><span style="flex:none;width:20px;height:20px;border-radius:50%;background:#131E29;color:#fff;font:700 11px/20px Montserrat,sans-serif;text-align:center">{n}</span><span style="font-size:12.5px;line-height:1.45;color:#131E29">{t}</span></div>' for n,t in leg)
    body = f'''
<div style="width:{W+120}px;display:flex;flex-direction:column;gap:18px;padding-bottom:24px">
  <div style="display:flex;justify-content:space-between;align-items:baseline;padding:0 4px">
    <span class="spec">ONDE VAI · PAREDE DE ENTRADA · 6.548 mm DE CORRIDA · 15 VÃOS DE 457 · ESCALA 1:5</span>
    <span class="cota">módulo 1.626 · testeira 1.900–2.100 em hastes · teto 3.400 · cotas em mm</span>
  </div>
  <svg viewBox="0 0 {W+120} {H+70}" width="{W+120}" height="{H+70}" style="display:block">{''.join(els)}</svg>
  <div style="display:grid;grid-template-columns:repeat(2, minmax(0, 1fr));gap:10px 28px;padding:0 4px">{legend}</div>
</div>'''
    return page(body), W+120, H+70+40+140

# ================================================================ COPY
def copy_sheet():
    W = 794  # A4 a 96 dpi, flow
    linhas = ''.join(f'<tr><td style="padding:10px 12px 10px 0;border-bottom:1px solid #E4DCCB;font-family:Montserrat;font-weight:700;font-size:13px;letter-spacing:.06em;color:#6B7680;white-space:nowrap">{n.title().replace(" E "," e ")}</td><td class="aleo" style="padding:10px 0;border-bottom:1px solid #E4DCCB;font-size:22px;line-height:1.2"><span style="color:{{{{verde}}}}">{a}</span> {b}</td></tr>' for n,(a,b) in COPY.items())
    wob = ''.join(f'<tr><td style="padding:8px 12px 8px 0;border-bottom:1px solid #E4DCCB;font-size:13px;color:#6B7680;white-space:nowrap">{p}</td><td class="aleo" style="padding:8px 0;border-bottom:1px solid #E4DCCB;font-size:19px">{f}</td></tr>' for p,f in WOB)
    body = f'''
<div style="width:{W}px;padding:56px 64px 64px;box-sizing:border-box;display:flex;flex-direction:column;gap:28px;background:#FFF7EA">
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div>
      <div class="spec" style="margin-bottom:8px">SHOWROOM NITRON MOB · COPY DE PDV · RASCUNHO PARA APROVAÇÃO</div>
      <h1 style="margin:0;font-family:Montserrat;font-weight:900;font-size:34px;line-height:1.05;letter-spacing:-.02em">O que está escrito<br>na loja</h1>
    </div>
    {lockup_v(style='width:96px;height:auto;color:#131E29;display:block')}
  </div>
  <p class="aleo" style="margin:0;font-size:17px;line-height:1.55;color:#131E29;max-width:60ch">Uma regra do manual organiza tudo: <strong>«toda casa tem» mais uma cena.</strong> Minúsculas, presente, sem ponto, sem superlativo. O complemento vive no título — o logo fica só com «toda casa tem».</p>

  <div>
    <div class="spec" style="margin-bottom:6px">STOPPER · FACE B · UMA POR AMBIENTE</div>
    <table style="border-collapse:collapse;width:100%">{linhas}</table>
    <p style="margin:10px 0 0;font-size:12.5px;line-height:1.5;color:#6B7680">«comida guardada» e «bagunça» são exemplos do próprio manual. As outras duas seguem a mesma gramática: cena de casa, não argumento de produto.</p>
  </div>

  <div>
    <div class="spec" style="margin-bottom:6px">WOBBLER · VERSO · SÓ NOS 25 CAMPEÕES</div>
    <table style="border-collapse:collapse;width:100%">{wob}</table>
    <p style="margin:10px 0 0;font-size:12.5px;line-height:1.5;color:#6B7680">Cada frase descreve o que o produto faz na cena, não o que ele é. «cabe a sobra do almoço» segura o pote de 2 L — a faixa de litragem que cresce 28,9% — sem dizer «hermético», claim que só 3% do mercado usa e que a Nitron não sustenta em norma.</p>
  </div>

  <div>
    <div class="spec" style="margin-bottom:6px">FAIXA DE PRATELEIRA · O NOME DO AMBIENTE, EM BEBAS</div>
    <p class="bebas" style="margin:0;font-size:26px;line-height:1.5;color:#131E29">COZINHA · ORGANIZAÇÃO · BANHO E LAVANDERIA · FRASQUEIRAS E INFANTIL</p>
    <p style="margin:6px 0 0;font-size:12.5px;line-height:1.5;color:#6B7680">Quatro ambientes, não dezesseis categorias de fábrica — a lição da Casa Riachuelo. A faixa é o único lugar em caixa alta, porque é rótulo, não frase.</p>
  </div>

  <div>
    <div class="spec" style="margin-bottom:6px">PAREDE DE ENTRADA · MANIFESTO</div>
    <p class="aleo" style="margin:0;font-size:26px;line-height:1.25;color:#131E29">toda casa tem uma frasqueira <span style="color:#8A939B">— e uma história dentro dela</span></p>
    <p style="margin:6px 0 0;font-size:12.5px;line-height:1.5;color:#6B7680">A única frase longa da loja, no único lugar em Aleo grande: a parede do prédio acima do móvel de entrada, que recebe as frasqueiras. O travessão é a exceção de pontuação — é a voz do manifesto, não do logo.</p>
  </div>

  <div style="border-top:1.5px solid #131E29;padding-top:14px;display:flex;flex-direction:column;gap:6px">
    <div class="spec">O QUE NÃO ENTRA</div>
    <p style="margin:0;font-size:12.5px;line-height:1.55;color:#131E29">«TODA CASA TEM» em caixa alta · «o melhor», «revolucionário», «incomparável» · «polipropileno virgem atóxico» sem tradução · «hermético» · «toda casa tem preço baixo» · tom de manual («o consumidor deve observar…»)</p>
  </div>
</div>'''
    return page(body), W, 1400

# ================================================================ gera
out = pathlib.Path('.')
specs = {}
for name, fn in [('Main', onde), ('Testeira', testeira), ('Faixa', faixa), ('Stopper', stopper), ('Wobbler', wobbler), ('Copy', copy_sheet)]:
    html, w, h = fn()
    (out/f'{name}.dc.html').write_text(html, encoding='utf-8')
    specs[name] = (w, h)
    print('%-9s %5d x %5d  %6d bytes' % (name, w, h, len(html.encode())))

# layout: mapa em cima, pecas embaixo em ordem de altura no modulo, copy a direita
A = []
x = 0
A.append(dict(file='Main.dc.html', x=0, y=0, w=specs['Main'][0], h=specs['Main'][1], title='Onde vai · parede de entrada'))
A.append(dict(file='Copy.dc.html', x=specs['Main'][0]+120, y=0, w=specs['Copy'][0], h=specs['Copy'][1], title='Copy · o que está escrito na loja', print='flow'))
y2 = specs['Main'][1] + 160
A.append(dict(file='Testeira.dc.html', x=0, y=y2, w=specs['Testeira'][0], h=specs['Testeira'][1], title='Testeira · 754 × 200 mm'))
y3 = y2 + specs['Testeira'][1] + 140
A.append(dict(file='Faixa.dc.html', x=0, y=y3, w=specs['Faixa'][0], h=specs['Faixa'][1], title='Faixa de prateleira · 754 × 40 mm'))
y4 = y3 + specs['Faixa'][1] + 140
A.append(dict(file='Stopper.dc.html', x=0, y=y4, w=specs['Stopper'][0], h=specs['Stopper'][1], title='Stopper · 100 × 150 mm · 2 faces'))
A.append(dict(file='Wobbler.dc.html', x=specs['Stopper'][0]+120, y=y4, w=specs['Wobbler'][0], h=specs['Wobbler'][1], title='Wobbler · Ø 100 mm'))
canvas = dict(artboards=A,
  annotations=[dict(id='verde', x=0, y=-150, w=520,
    text='O verde: o manual (19/08/2026) diz #1EA7AC; a instrução foi #08a9b1. O canvas usa #08a9b1 e o ajuste "verde" troca em tudo de uma vez. Decidir antes da arte-final.'),
    dict(id='vetores', x=560, y=-150, w=520,
    text='Nenhum logo foi redesenhado: símbolo, lettering e assinatura são os paths do kit oficial. O lockup horizontal é composto com as proporções do vertical (assinatura 75%, gap 7,96/40,78).')],
  launch=dict(view='canvas'))
(out/'canvas.json').write_text(json.dumps(canvas, ensure_ascii=False, indent=1), encoding='utf-8')
print('canvas.json ok')
