#!/usr/bin/env python3
"""Atualiza 09-pdv-sistema-modular.html — Rev. 4.

Rev. 3 fechou a medida fixa (12 paineis, 9 ripas).
Rev. 4 corta a grade para 7 paineis pela regra da proporcao, entra com a peca L
como no de topo (coroa) e libera pilha de baias de altura mista. Traz tambem a
cobertura da curva medida no cadastro de dimensao do produto.

Idempotente: pode rodar de novo sobre um caderno ja convertido.
Reescreve cabecalho, conclusoes do §1, §2/§3/§4/§5/§6/§8 e o rodape. Mantem §7.
"""
import pathlib, re

ENC, NOX, NOXC, NOL, NOY, NOZ = 40.60, 61.61, 101.30, 83.23, 83.23, 73.08
PE = 60-ENC; CONSOME = 2*ENC; SOL = NOL-NOX; PANT = 15
GMM, RSKG, DENS = 0.22628, 19.03, 0.556/1000
C_TZ, C_CZ, C_L, C_T, C_H = 0.3874596, 0.4951, 0.3003, 0.00968649, 0.0872
M_TZ, M_CZ, M_L, M_T, M_H = 44.31, 56.62, 32.0, 1.10, 10.2
RAZ_MIN, RAZ_MAX = 1.30, 2.60

COMPS = [('PSC-01',315,360), ('PSC-02',415,450), ('PSC-03',595,634), ('PSC-04',717,754)]
LARGS = [('BLA-01-AC',200,200), ('BLA-03-AC',287,300), ('PSC-02',415,460)]
COB_LADO   = {200:56.8, 300:90.5, 460:99.9}
COB_FRENTE = {200:18.1, 300:67.0, 460:96.1}
COB_ALT    = {270:79.1, 513:98.2}

ext_comp = lambda B, N: 2*NOX+(N-1)*NOXC+N*(B-CONSOME)
ext_prof = lambda B:    B+2*(NOY-ENC)
passo_v  = lambda B, k=1: (B-CONSOME)+k*NOZ

def altura(pilha, coroa=None, k=1):
    ripas = list(pilha)+([coroa] if coroa else [])
    return PE + (len(ripas)+1)*k*NOZ + sum(r-CONSOME for r in ripas)

FAM = [
  dict(nome='Checkout', slug='CHECKOUT', bc='PSC-02', bcv=415, bl='BLA-03-AC', blv=287,
       pan=(300,450), vaos=(1,2,3), pilha=[270,270,270,270], coroa=270, ganch=True,
       fundo=False, deck=True, casinha=False, faces=4,
       lede='Face unica para o cliente na fila, profundidade media de <strong>372 mm</strong> — '
            'a que acomoda <strong>90,5% da curva</strong> de lado. Cinco prateleiras de '
            'passo curto e uma <strong>coroa em peca L</strong> no topo, com gancheira de '
            'ripa 415 e porta-hastes para blister e cartela.',
       cap='A coroa e o que diferencia o checkout: a peca L fecha o poste acima da ultima '
           'prateleira e segura a ripa da gancheira. Ela passa 21,62 mm de cada lado do corpo, '
           'e a cabeceira acompanha essa cota.'),
  dict(nome='Ilha', slug='ILHA', bc='PSC-03', bcv=595, bl='PSC-02', blv=415,
       pan=(460,634), vaos=(1,2,3), pilha=[270,270,270], coroa=None, ganch=False,
       fundo=False, deck=True, casinha=False, faces=4,
       lede='A mais funda das quatro: <strong>500 mm</strong>, que acomodam '
            '<strong>99,9% da curva</strong> de lado e 96,1% de frente. Aberta pelas '
            '<strong>quatro faces</strong>, altura de balcao (<strong>878 mm</strong>), '
            '<strong>top deck</strong> de painel inteiro na prateleira de cima.',
       cap='A ilha e a unica que usa a ripa de largura PSC-02 de 415 mm, e a unica sem coroa: '
           'ela precisa ficar na altura do balcao para trabalhar pelas quatro faces.'),
  dict(nome='Ponta de gondola', slug='PONTA-DE-GONDOLA', bc='PSC-03', bcv=595,
       bl='BLA-03-AC', blv=287, pan=(300,634), vaos=(1,2,3),
       pilha=[270,270,270,270,270], coroa=513, ganch=False,
       fundo=True, deck=False, casinha=True, faces=1,
       lede='Seis prateleiras de passo curto e uma <strong>coroa de 513</strong> no topo, '
            'que da <strong>504,88 mm</strong> de altura sem somar prateleira — e onde a '
            'casinha se apoia. Fundo fechado, encosta na corrida da gondola.',
       cap='A coroa de 513 mostra o que a peca L resolve: altura de comunicacao no topo sem '
           'gastar uma prateleira. O painel de fundo, porem, exige corte dedicado por baia.'),
  dict(nome='Paredao', slug='PAREDAO', bc='PSC-04', bcv=717, bl='BLA-03-AC', blv=287,
       pan=(300,754), vaos=(3,4,5), pilha=[270]*7, coroa=None, ganch=False,
       fundo=True, deck=False, casinha=False, faces=1,
       lede='O vao mais longo da lista (<strong>PSC-04 717</strong>) na profundidade media. '
            'Era 200 × 754 na Rev. 3 e passou a <strong>300 × 754</strong>: o painel de razao '
            '3,77 caiu pela regra, e a profundidade subiu de 285 para 372 mm — '
            '<strong>de 56,8% para 90,5% da curva</strong>. A corrida nao mudou.',
       cap='O paredao e a corrida: cada vao a mais soma 737 mm e uma faixa de categoria. '
           'Oito prateleiras de passo curto, fundo fechado, uma face de acesso.'),
]

def bom(f, N):
    pilha, coroa, ganch = f['pilha'], f['coroa'], f['ganch']
    n = len(pilha)+1; linhas = N+1; cor = bool(coroa)
    tz = 4*n; lp = 4 if cor else 0; cz = 2*(N-1)*(n+(1 if cor else 0)); tp = 2*linhas
    ph = 2*N if (cor and ganch) else 0
    qbc = 2*N*n + (2*N if cor else 0) + (N if (cor and ganch) else 0)
    qbl = linhas*n
    vert = {}
    for r in pilha: vert[r] = vert.get(r,0)+2*linhas
    if cor: vert[coroa] = vert.get(coroa,0)+2*linhas
    pes = 2*linhas
    mad = (qbc*f['bcv'] + qbl*f['blv'] + sum(k*v for k,v in vert.items()) + pes*60)*GMM
    np_ = N*n
    madp = np_*f['pan'][0]*f['pan'][1]*PANT*DENS
    madf = 0; fundos = {}
    if f['fundo']:
        for r in pilha:
            h = round(passo_v(r)-PANT)
            fundos[h] = fundos.get(h,0)+N
        for h,q in fundos.items(): madf += q*f['pan'][1]*h*PANT*DENS
    conn = tz*C_TZ+cz*C_CZ+lp*C_L+tp*C_T+ph*C_H
    plast = tz*M_TZ+cz*M_CZ+lp*M_L+tp*M_T+ph*M_H
    custo = conn+(mad+madp+madf)/1000*RSKG
    A = altura(pilha, coroa)
    return dict(tz=tz, lp=lp, cz=cz, tp=tp, ph=ph, qbc=qbc, qbl=qbl, vert=vert, pes=pes,
                np=np_, fundos=fundos, kg=(mad+madp+madf+plast)/1000, custo=custo,
                L=round(ext_comp(f['bcv'],N)), P=round(ext_prof(f['blv'])), A=round(A),
                Lc=round(ext_comp(f['bcv'],N)+2*SOL) if cor else 0, n=n)

br  = lambda v: f'{v:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
mil = lambda v: f'{v:,.0f}'.replace(',','.')

# ------------------------------------------------------------------ cabecalho
HEADER = '''<header>
  <div class="eyeb"><span class="lab">NITRON · DESENVOLVIMENTO DE PRODUTOS</span>
  <span class="lab">CADERNO DE ESPECIFICAÇÃO · PDV</span><span class="lab">REV. 4 · 04/09/2026</span></div>
  <div class="hg">
    <div><h1>Sistema PDV<br>Nitron Mob</h1><p class="slog">toda casa tem</p>
    <p class="thesis">Largura, comprimento e altura — nessa ordem. <strong>7 painéis e 9 ripas</strong>, e nada fora dessa lista. Cada baia tem a sua ripa, então o mesmo módulo mistura prateleira baixa e vão alto; a <strong>peça L</strong> fecha o poste no topo e dá altura sem somar prateleira. <strong>Nenhuma ripa nova.</strong></p></div>
    <div class="bars">
      <div class="bar"><b>1,3–2,6</b><span>a <strong>REGRA DA PROPORÇÃO</strong> do painel<i>comprimento ÷ largura · corta a grade de 12 para 7</i></span></div>
      <div class="bar"><b>90,5%</b><span>da <strong>CURVA</strong> na profundidade de 300<i>contra 56,8% em 200 e 99,9% em 460</i></span></div>
      <div class="bar"><b>73,08</b><span>a <strong>PEÇA L</strong> no eixo vertical<i>igual à trizeta — é por isso que ela é nó de topo</i></span></div>
      <div class="bar"><b>+42,02</b><span>eixo do <strong>COMPRIMENTO</strong> · nó de 61,61<i>externo = ripa + 42,02 · confirmado pelos painéis</i></span></div>
    </div>
  </div>
</header>'''

CALL1 = '''  <div class="call">
    <span class="lab">O CADASTRO JÁ SEPARA OS DOIS EIXOS — E A LISTA FIXA RESPEITA ISSO</span>
    <p>A família <code>BLA</code> (campo <code>LARGURA</code>) é a ripa que vai da frente ao fundo; a família <code>PSC</code> (campo <code>COMPRIMENTO</code>) é a que vence o vão. A lista fixa usa cada uma no seu papel: <strong>BLA-01-AC 200 · BLA-03-AC 287 · PSC-02 415</strong> na largura, <strong>PSC-01 315 · PSC-02 415 · PSC-03 595 · PSC-04 717</strong> no comprimento.</p>
    <p>A <code>PSC-02</code> aparece nas duas listas — é a mesma ripa fazendo dois papéis, o que já acontece no cadastro: ela é comprimento na sapateira e serve de largura na ilha.</p>
  </div>
  <div class="call stop">
    <span class="lab">E O CADASTRO AINDA RESPONDE O QUE CABE NA PRATELEIRA</span>
    <p><code>TGFPRO.LARGURA</code>, <code>ALTURA</code> e <code>ESPESSURA</code> (em centímetros) estão preenchidas em <strong>2.742 dos 3.079 PAs ativos</strong>. Cruzando com o faturamento de marca própria de 12 meses — 1.273 SKUs, <strong>R$ 83,8 M</strong>, tabelas 84 e 3 fora — dá para medir a cobertura de cada profundidade e de cada altura de baia, em vez de estimar. É o que decide o §4 e o §3.</p>
  </div>'''

rows2 = ''.join(
    ('<tr class="hl">' if N in (2,3) else '<tr>') + f'<td class="n">{N}</td>' +
    ''.join(f'<td class="n">{"<strong>" if N in (2,3) else ""}{mil(round(ext_comp(b,N)))}'
            f'{"</strong>" if N in (2,3) else ""}</td>' for _, b, _ in COMPS) +
    f'<td class="n">4/nível</td><td class="n">{2*(N-1)}/nível</td></tr>'
    for N in range(1,7))
S2 = f'''  <div class="sh"><span class="snum">§2</span><h2>Comprimento · as 4 ripas e a corrida</h2></div>
  <p class="lede">Quatro ripas de comprimento. O <strong>comprimento é a corrida</strong>: N vãos daquela ripa, encadeados pela cruzeta. A trizeta fica fixa em 4 por nível; só a cruzeta cresce, a 2 × (N−1) por nível.</p>
  <div class="tw"><table>
    <caption>Cota externa da corrida em milímetros. Fórmula: 2 × 61,61 + (N−1) × 101,30 + N × (ripa − 81,20).</caption>
    <thead><tr><th>N vãos</th><th>PSC-01 · 315</th><th>PSC-02 · 415</th><th>PSC-03 · 595</th><th>PSC-04 · 717</th><th>Trizetas</th><th>Cruzetas</th></tr></thead>
    <tbody>{rows2}</tbody>
  </table></div>
  <div class="call">
    <span class="lab">A CONFERÊNCIA QUE FECHA O MODELO</span>
    <p>As quatro ripas dão <strong>357,02 · 457,02 · 637,02 · 759,02</strong> mm de cota externa por vão. Os quatro painéis são <strong>360 · 450 · 634 · 754</strong>. Diferença de <strong>+2,98 / −7,02 / −3,02 / −5,02</strong> mm — quatro em quatro dentro de ±7 mm.</p>
    <p>Isso prova que o painel foi cortado na <strong>cota externa do vão</strong>: ele deita sobre os nós e cobre o vão de ponta a ponta. E é por isso que o painel <strong>não</strong> é a peça que estica o móvel: <strong>o comprimento vem da corrida</strong>, não da tábua.</p>
  </div>'''

ar = ''.join(
    ('<tr class="hl">' if n in (4,5,6,8) else '<tr>') + f'<td class="n">{n}</td>'
    f'<td class="n">{"<strong>" if n in (4,5,6,8) else ""}{mil(round(altura([270]*(n-1))))}'
    f'{"</strong>" if n in (4,5,6,8) else ""}</td>'
    f'<td class="n">{mil(round(altura([270]*(n-1),270)))}</td>'
    f'<td class="n">{mil(round(altura([270]*(n-1),513)))}</td>'
    f'<td class="n">{mil(round(altura([270]*(n-2)+[513])))}</td>'
    f'<td>{uso}</td></tr>'
    for n, uso in [(2,'mesa baixa'),(3,'mesa de exposição'),(4,'<strong>ilha</strong> · balcão 900'),
                   (5,'<strong>checkout</strong> com coroa'),(6,'<strong>ponta</strong> com coroa 513'),
                   (7,'gôndola alta'),(8,'<strong>paredão</strong> · parede 2.000')])
S3 = f'''  <div class="sh"><span class="snum">§3</span><h2>Altura · uma ripa por baia, e a peça L no topo</h2></div>
  <p class="lede">A altura deixou de ser <em>n × uma ripa só</em>. <strong>Cada baia tem a sua ripa</strong> — <code>BAL-02-AC</code> 270 ou <code>PSA-05</code> 513 — e a soma é o que fecha a cota. No topo, a <strong>peça L</strong> fecha o poste e segura uma ripa atravessada, sem prateleira: é a coroa.</p>
  <div class="tw"><table>
    <caption>Altura externa em milímetros. Fórmula: 19,40 + n_nós × 73,08 + Σ (ripa − 81,20). A coroa acrescenta um nó.</caption>
    <thead><tr><th>Prateleiras</th><th>Só 270</th><th>+ coroa 270</th><th>+ coroa 513</th><th>Baia de cima 513</th><th>Uso</th></tr></thead>
    <tbody>{ar}</tbody>
  </table></div>
  <div class="call">
    <span class="lab">A PEÇA L TEM O MESMO PASSO VERTICAL DA TRIZETA — E ISSO É O ACHADO</span>
    <p>Bounding box da peça L: <strong>21,92 × 83,23 × 73,08 mm</strong>. O <strong>73,08</strong> é idêntico ao da trizeta, então ela <strong>empilha no poste como um nó de prateleira</strong>. Mas tem só <strong>2 vias coplanares</strong>: segura uma ripa atravessada e nada mais. É assim que a arara ganha altura sem ganhar prateleira.</p>
    <p>A coroa acrescenta <code>(ripa − 81,20) + 73,08</code>, ou seja <strong>ripa − 8,12 mm</strong>: <strong>+261,88</strong> com a ripa 270 e <strong>+504,88</strong> com a 513. E ela é <strong>mais larga que a estrutura</strong>: o L tem 83,23 mm nesse eixo contra 61,61 da trizeta, então passa <strong>21,62 mm por lado</strong> — a cabeceira acompanha essa cota.</p>
  </div>
  <div class="tw" style="margin-top:22px"><table>
    <caption>Altura livre da baia contra a altura do produto. <code>TGFPRO.ALTURA</code> × faturamento de 12 M.</caption>
    <thead><tr><th>Ripa vertical</th><th>Passo</th><th>Livre (menos o painel)</th><th>% do faturamento em pé</th></tr></thead>
    <tbody>
      <tr><td class="n">BAL-02-AC 270</td><td class="n">{br(passo_v(270))}</td><td class="n"><strong>{round(passo_v(270)-PANT)} mm</strong></td><td class="n">{COB_ALT[270]}%</td></tr>
      <tr><td class="n">PSA-05 513</td><td class="n">{br(passo_v(513))}</td><td class="n"><strong>{round(passo_v(513)-PANT)} mm</strong></td><td class="n">{COB_ALT[513]}%</td></tr>
    </tbody>
  </table></div>
  <div class="call stop">
    <span class="lab">POR QUE A ALTURA MISTA NÃO É LUXO</span>
    <p>Um módulo só de ripa 270 deixa <strong>21% do faturamento de fora</strong> — o que não fica de pé em 247 mm. Um módulo só de 513 desperdiça altura em 79% dos casos. <strong>Misturar as duas na mesma pilha é o que cobre o catálogo inteiro.</strong></p>
    <p>E continua faltando uma fita: o encaixe vertical da trizeta abre para <strong>baixo</strong> e o topo é fechado (chapa em z 70,0–72,9 mm), por isso ela sai em <strong>par espelhado</strong>. O passo é <strong>261,88 mm</strong> se o par empilha um nó por nível, <strong>334,96 mm</strong> se empilha dois. Este caderno usa o primeiro.</p>
  </div>'''

grade = ''
for lref, lb, lpan in LARGS:
    cel = ''
    for cref, cb, cpan in COMPS:
        raz = cpan/lpan
        ok = RAZ_MIN <= raz <= RAZ_MAX
        cel += (f'<td class="n">{"<strong>" if ok else ""}{br(raz)}{"</strong>" if ok else ""}'
                f' {"✅" if ok else "❌"}</td>')
    grade += (f'<tr><td class="n"><strong>{lpan}</strong></td>{cel}'
              f'<td class="n">{mil(round(ext_prof(lb)))}</td>'
              f'<td class="n">{COB_LADO[lpan]}%</td><td class="n">{COB_FRENTE[lpan]}%</td></tr>')
S4 = f'''  <div class="sh"><span class="snum">§4</span><h2>Largura · 3 ripas, e a grade que caiu de 12 para 7</h2></div>
  <p class="lede">Três ripas de largura, cada uma casada com uma tábua. A tábua <strong>não</strong> alcança a cota externa — o nó sobra 42,63 mm por lado. Ela apoia nas duas ripas e sobressai: 0,00 mm na de 200, +6,50 na de 300, +22,50 na de 460.</p>
  <div class="tw"><table>
    <caption>A regra: comprimento entre <strong>1,3 e 2,6 ×</strong> a largura. Cada célula é a razão. Sete passam, cinco caem.</caption>
    <thead><tr><th>Tábua</th><th>360</th><th>450</th><th>634</th><th>754</th><th>Prof. externa</th><th>Curva de lado</th><th>De frente</th></tr></thead>
    <tbody>{grade}</tbody>
  </table></div>
  <div class="call">
    <span class="lab">OS CINCO CORTES SÃO UM ÚNICO CRITÉRIO</span>
    <p>Fora ficaram <strong>200×634 e 200×754</strong> (razão 3,17 e 3,77 — tira estreita e comprida) e <strong>300×360, 460×360 e 460×450</strong> (razão 1,20, 0,78 e 0,98 — quadrado, ou mais fundo que longo). A banda que sobra é <strong>1,38 a 2,51</strong>, e os vizinhos excluídos estão em 1,20 e 3,17: folga confortável dos dois lados, então a regra é critério, não ajuste de curva.</p>
    <p>Lida na diagonal, a tabela dá a frase do catálogo: <strong>quanto mais funda a prateleira, mais longo o vão.</strong> Nenhuma ripa sai da lista — <strong>só o estoque de painel cai 42%</strong>.</p>
  </div>
  <div class="call stop">
    <span class="lab">SOBRE O EMPENAMENTO, O MECANISMO É OUTRO</span>
    <p>O painel <strong>não</strong> é apoiado só nas pontas: ele deita sobre as duas ripas de comprimento e sobre as duas de largura, apoiado nos quatro lados, e flexiona na direção <strong>curta</strong>. Sob carga, o painel de 200 é o <strong>mais rígido</strong> dos três. Sag não é o problema.</p>
    <p>O que existe de real numa tábua de 15 mm em proporção 3,8:1 é <strong>arqueamento e torção</strong> ao longo do comprimento — instabilidade dimensional, não flexão. O argumento decisivo, porém, é o da direita da tabela: <strong>a prateleira de 200 acomoda 56,8% do faturamento de lado e 18,1% de frente.</strong> Seria a maior área de exposição do sistema servindo a menor parte do catálogo.</p>
  </div>
  <div class="call stop"><span class="lab">O LIMITE DE FORNECIMENTO NÃO SE RESOLVEU</span>
    <p>A chapa crua <code>PAN-01</code> tem <strong>200 mm de largura</strong>. Dos 7 painéis, <strong>5 são de 300 ou 460</strong> e exigem emenda ou chapa mais larga. E o <strong>painel de fundo não sai da lista</strong>: fechar uma baia pede um corte de comprimento × altura livre (634 × 247, 754 × 247…), que não existe na grade.</p></div>'''

render = pathlib.Path(__file__).resolve().parent / 'render'
blocos = ['''  <div class="sh"><span class="snum">§5</span><h2>As quatro famílias</h2></div>
  <p class="lede">Cada uma nasce numa combinação distinta de painel, corrida e pilha de baias — não é o mesmo quadro em três tamanhos. Nenhuma repete o painel de outra. Duas usam coroa em peça L, duas não; o que muda além disso: painel de fundo, top deck, gancheira, casinha e o número de faces de acesso.''']
for f in FAM:
    vs = f['vaos']; mM = vs[1]; b0 = bom(f, mM)
    pil = ' · '.join(str(x) for x in f['pilha'])
    cor = f'coroa {f["coroa"]}' + (' + gancheira' if f['ganch'] else '') if f['coroa'] else 'sem coroa'
    tr = ''
    for lab, N in zip('PMG', vs):
        b = bom(f, N)
        vv = ' + '.join(f'{q}×{k}' for k, q in sorted(b['vert'].items()))
        tr += (f'<tr><td><strong>{lab}</strong></td><td class="n">{N}</td>'
               f'<td class="n">{"<strong>" if lab=="M" else ""}{b["L"]} × {b["P"]} × {b["A"]}'
               f'{"</strong>" if lab=="M" else ""}</td>'
               f'<td class="n">{b["tz"]}</td><td class="n">{b["lp"] or "—"}</td>'
               f'<td class="n">{b["cz"]}</td><td class="n">{b["tp"]}</td>'
               f'<td class="n">{b["ph"] or "—"}</td>'
               f'<td class="n">{b["qbc"]}</td><td class="n">{b["qbl"]}</td><td class="n">{vv}</td>'
               f'<td class="n">{b["np"]}</td><td class="n">{br(b["kg"])} kg</td>'
               f'<td class="n">R$ {br(b["custo"])}</td><td class="n">R$ {br(2*b["custo"])}</td></tr>')
    svg = (render / f'pdv-fam-{f["slug"]}.svg').read_text(encoding='utf-8')
    extra = (f' · coroa de {mil(b0["Lc"])} mm' if f['coroa'] else '')
    blocos.append(f'''
  <h3 style="margin-top:46px;font-size:21px">{f["nome"]} · painel {f["pan"][0]} × {f["pan"][1]} · {b0["n"]} prateleiras · {mil(b0["A"])} mm</h3>
  <p class="lede" style="font-size:14.5px">{f["lede"]}</p>
  <div class="tw"><table>
    <caption>Ripa de largura <code>{f["bl"]}</code> {f["blv"]} · comprimento <code>{f["bc"]}</code> {f["bcv"]} · pilha de baias {pil} mm ({cor}). Custo por escala de massa, não apurado.</caption>
    <thead><tr><th>Ver.</th><th>Vãos</th><th>L × P × A (mm)</th><th>Trizeta</th><th>Peça L</th><th>Cruzeta</th><th>Tampa</th><th>Porta-haste</th>
    <th>Ripa {f["bcv"]}</th><th>Ripa {f["blv"]}</th><th>Verticais</th><th>Painéis</th><th>Peso</th><th>Custo</th><th>2× custo</th></tr></thead>
    <tbody>{tr}</tbody></table></div>
  <figure class="plate"><div class="pin">{svg}</div><figcaption>{f["nome"]} M — {mil(b0["L"])} × {b0["P"]} × {mil(b0["A"])} mm, {mM} vão{"s" if mM>1 else ""}, painel {f["pan"][0]} × {f["pan"][1]}{extra}. {f["cap"]}</figcaption></figure>''')
S5 = '\n'.join(blocos)

S6_CAP = ('<caption>O que diferencia as famílias. As seis primeiras linhas são '
          'dimensionais — <strong>nenhuma repete o painel de outra</strong>. As demais saem '
          'de peça que já existe; a gancheira é uma ripa de comprimento presa por '
          'porta-hastes na baia da coroa.</caption>')
S6_ROWS = '''      <tr class="hl"><td><strong>Painel</strong></td><td class="n">300 × 450</td><td class="n">460 × 634</td><td class="n">300 × 634</td><td class="n">300 × 754</td></tr>
      <tr><td><strong>Ripa de largura</strong></td><td class="n">BLA-03-AC · 287</td><td class="n">PSC-02 · 415</td><td class="n">BLA-03-AC · 287</td><td class="n">BLA-03-AC · 287</td></tr>
      <tr><td><strong>Ripa de comprimento</strong></td><td class="n">PSC-02 · 415</td><td class="n">PSC-03 · 595</td><td class="n">PSC-03 · 595</td><td class="n">PSC-04 · 717</td></tr>
      <tr><td><strong>Pilha de baias</strong></td><td class="n">270 × 4</td><td class="n">270 × 3</td><td class="n">270 × 5</td><td class="n">270 × 7</td></tr>
      <tr class="hl"><td><strong>Coroa em peça L</strong></td><td><span class="chip w">270 + gancheira</span></td><td>—</td><td><span class="chip w">513</span></td><td>—</td></tr>
      <tr class="hl"><td><strong>Medida final M</strong></td><td class="n">892 × 372 × 1.402</td><td class="n">1.252 × 500 × 878</td><td class="n">1.252 × 372 × 1.907</td><td class="n">2.970 × 372 × 1.926</td></tr>
'''

S8 = '''  <div class="sh"><span class="snum">§8</span><h2>O que falta</h2></div>
  <ol class="steps">
    <li><span><strong>A fita do passo vertical.</strong> Monte duas prateleiras com a ripa <code>BAL-02-AC</code> de 270 e meça de apoio a apoio: <strong>261,9 mm confirma um nó por nível, 335,0 mm o par espelhado.</strong> É a única cota do sistema que a lista de painéis não fecha, e ela muda todas as alturas deste caderno.</span></li>
    <li><span><strong>A orientação de uso da peça L.</strong> O bounding box (21,92 × 83,23 × 73,08) não diz em que plano ela é montada. Se for no plano da frente, como este caderno assume, a coroa passa <strong>21,62 mm por lado</strong> do corpo. Com a coroa montada, uma fita confirma.</span></li>
    <li><span><strong>A profundidade externa montada.</strong> Um nó com a ripa <code>BLA-01-AC</code> de 200, face externa a face externa, deve dar <strong>285,3 mm</strong>.</span></li>
    <li><span><strong>A decisão do painel.</strong> A <code>PAN-01</code> tem 200 mm de largura e <strong>5 dos 7 painéis</strong> são de 300 ou 460. Some o <strong>painel de fundo, que não sai da grade</strong>: cada baia fechada é um corte de comprimento × altura livre.</span></li>
    <li><span><strong>Ferramentaria: onde está o molde da cruzeta?</strong> Só as versões de 1 vão (ilha P e ponta P) rodam sem ela. Primeira de cinco cadastrada em 17/07/2026, quatro já injetadas; ainda não sabemos se as 2 cavidades são o par esq/dir.</span></li>
    <li><span><strong>Montar um nó de cruzeta e carregá-lo.</strong> A chapa 1 da trizeta está em z relativo 40,0 mm, exatamente onde o encaixe de 40,60 mm termina — a ripa apoia numa chapa de 2,9 mm, dando 8,5–18,4 MPa. A carga de 20 kg por prateleira é provisória.</span></li>
    <li><span><strong>Aprovação de marca para o verde</strong> <code>#08a9b1</code> contra o <code>#1EA7AC</code> declarado no manual.</span></li>
    <li><span><strong>A tampinha</strong> — STL não recebido. Entra na conta pelo peso cadastrado (1,10 g).</span></li>
    <li><span><strong>Um registro sujo no cadastro:</strong> <code>CODPROD</code> 3579 (Kit Potes Acoplados c/ 5 peças) tem <code>ALTURA</code> = 45437 — uma data digitada no campo de altura. Foi excluído da conta de cobertura.</span></li>
  </ol>'''

FOOTER = '''<footer><p>Papéis das ripas extraídos de <code>VW_COMPOSICAO_NIT</code> para as 13 PAs com estrutura. Cotas de nó, encaixe e parede medidas nas malhas STL — as cinco fechadas, zero arestas não-manifold. A <strong>peça L</strong> tem bounding box 21,92 × 83,23 × 73,08 mm: o passo vertical de 73,08 é idêntico ao da trizeta, o que a torna um nó de topo. A cobertura da curva vem de <code>TGFPRO.LARGURA/ALTURA/ESPESSURA</code> (cm), preenchidas em 2.742 dos 3.079 PAs ativos, cruzadas com 1.273 SKUs e R$ 83,8 M de faturamento de marca própria em 12 meses até 24/08/2026, tabelas 84 e 3 fora. Identidade visual e regras de PDV do manual oficial em <a href="https://marca.nitron.com.br/">marca.nitron.com.br</a>. Cotas externas pelo modelo de encaixe de 40,60 mm; o eixo do comprimento está confirmado pela própria lista de painéis, <strong>o vertical depende do modelo de nó e a sobra da coroa depende da orientação da peça L — as duas fitas do §8 fecham isso</strong>. Custos estimados por escala de massa, não apurados. Nada gravado em <code>pdp_lancamento</code>.</p></footer>'''

# ------------------------------------------------------------------- aplica
if __name__ == '__main__':
    p_doc = pathlib.Path(__file__).resolve().parent / '09-pdv-sistema-modular.html'
    h = p_doc.read_text(encoding='utf-8')

    fim = h.index('</style>')
    css, resto = h[:fim], h[fim:]
    if ':root{{' in css:
        h = css.replace('{{','{').replace('}}','}') + resto
        print('  corrigidas chaves duplicadas no <style>')

    def troca_secao(h, num, novo):
        pat = re.compile(r'<section>\s*\n(  <div class="sh"><span class="snum">§' + str(num) +
                         r'</span>.*?)\n</section>', re.S)
        m = pat.search(h)
        assert m, f'§{num} nao encontrado'
        return h[:m.start()] + '<section>\n' + novo + '\n</section>' + h[m.end():]

    m = re.search(r'<header>.*?</header>', h, re.S); assert m
    h = h[:m.start()] + HEADER + h[m.end():]

    m = re.search(r'  <div class="call(?: stop)?">\s*\n    <span class="lab">'
                  r'(?:O CAMPO LARGURA|O CADASTRO JÁ SEPARA).*?\n  </div>\n</section>', h, re.S)
    assert m, 'calls do §1 nao encontrados'
    h = h[:m.start()] + CALL1 + '\n</section>' + h[m.end():]

    for num, novo in ((2,S2),(3,S3),(4,S4),(5,S5),(8,S8)):
        h = troca_secao(h, num, novo)

    m = re.search(r'    <caption>(?:Os cinco elementos|O que diferencia).*?</caption>', h, re.S)
    assert m, 'caption do §6 nao encontrada'
    h = h[:m.start()] + '    ' + S6_CAP + h[m.end():]
    m = re.search(r'(<tbody>\n)((?:      <tr[^\n]*\n)*?)'
                  r'(      <tr><td><strong>Painel de fundo</strong></td>)', h)
    assert m, 'tbody do §6 nao encontrado'
    h = h[:m.start()] + m.group(1) + S6_ROWS + m.group(3) + h[m.end():]

    m = re.search(r'<footer>.*?</footer>', h, re.S); assert m
    h = h[:m.start()] + FOOTER + h[m.end():]

    p_doc.write_text(h, encoding='utf-8')
    print(f'{p_doc.name}: {len(h)} bytes')
    for f in FAM:
        b = bom(f, f['vaos'][1])
        print(f"  {f['nome']:20} {b['L']:5} x {b['P']:4} x {b['A']:5}  "
              f"painel {f['pan'][0]}x{f['pan'][1]}  {b['n']} prat  R$ {br(b['custo'])}")
