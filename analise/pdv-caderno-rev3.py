#!/usr/bin/env python3
"""Atualiza o caderno 09-pdv-sistema-modular.html para a Rev. 3 — medida fixa.

A Rev. 2 tratava largura como fixa e comprimento/altura/profundidade como
moduláveis num catálogo de 19 barras. A Rev. 3 fecha tudo: 4 ripas de
comprimento, 3 de largura, 2 verticais e 12 painéis. Nada fora dessa lista.

Reescreve o cabeçalho, as conclusões do §1, os §2/§3/§4 inteiros, o §5 com as
elevações regeradas por pdv-familias-svg.py, o §8 e o rodapé. Mantém §6 e §7.
"""
import math, pathlib, re

ENC, NOX, NOXC, NOY, NOZ = 40.60, 61.61, 101.30, 83.23, 73.08
PE = 60-ENC; CONSOME = 2*ENC
GMM, RSKG, DENS, PANT = 0.22628, 19.03, 0.556/1000, 15
C_TZ, C_CZ, C_T = 0.3874596, 0.4951, 0.00968649
M_TZ, M_CZ, M_T = 44.31, 56.62, 1.10
BV = 270

ext_comp = lambda B, N: 2*NOX+(N-1)*NOXC+N*(B-CONSOME)
ext_prof = lambda B:    B+2*(NOY-ENC)
ext_alt  = lambda B, n, k=1: n*k*NOZ+(n-1)*(B-CONSOME)+PE
passo_v  = lambda B, k=1: (B-CONSOME)+k*NOZ

COMPS = [('PSC-01', 315, 360), ('PSC-02', 415, 450), ('PSC-03', 595, 634), ('PSC-04', 717, 754)]
LARGS = [('BLA-01-AC', 200, 200), ('BLA-03-AC', 287, 300), ('PSC-02', 415, 460)]

FAM = [
  dict(nome='Checkout', slug='CHECKOUT', bc='PSC-02', bcv=415, bl='BLA-03-AC', blv=287,
       pan=(300, 450), vaos=(1, 2, 3), n=5, fundo=False, deck=True, peg=True,
       casinha=False, faces=4,
       lede='Face única para o cliente na fila, profundidade média de <strong>372 mm</strong>, '
            'altura de <strong>1.140 mm</strong> — a mais próxima do balcão de caixa. Cinco '
            'prateleiras: cestos na base, <strong>gancheira</strong> com ripa de 415 e ganchos '
            'no meio, e bandeja no topo. Cápsula de ativação suspensa no vão de cima.',
       cap='A gancheira é o que diferencia o checkout: uma ripa de 415 mm entre duas '
           'prateleiras, com ganchos, para blister e cartela. A planta mostra as quatro '
           'faces livres — o checkout fica em ilha ao lado do caixa.'),
  dict(nome='Ilha', slug='ILHA', bc='PSC-03', bcv=595, bl='PSC-02', blv=415,
       pan=(460, 634), vaos=(1, 2, 3), n=4, fundo=False, deck=True, peg=False,
       casinha=False, faces=4,
       lede='A mais funda das quatro: <strong>500 mm</strong>, vencidos pela ripa de largura '
            'de 415 mm — a maior da lista. Aberta pelas <strong>quatro faces</strong>, altura '
            'de balcão (<strong>878 mm</strong>). <strong>Top deck</strong> de painel inteiro '
            'na prateleira de cima para exposição, as de baixo para estoque.',
       cap='A ilha é a única que usa a ripa de largura PSC-02 de 415 mm. Sem linha de '
           'montante no meio da profundidade, ela fica acessível dos dois lados.'),
  dict(nome='Ponta de gôndola', slug='PONTA-DE-GONDOLA', bc='PSC-03', bcv=595,
       bl='BLA-03-AC', blv=287, pan=(300, 634), vaos=(1, 2, 3), n=7, fundo=True,
       deck=False, peg=False, casinha=True, faces=1,
       lede='Alta e de profundidade média: <strong>1.664 mm</strong> em sete prateleiras, '
            '<strong>372 mm</strong> de profundidade. <strong>Painel de fundo</strong> fecha a '
            'face de trás e <strong>topper casinha</strong> marca o topo. Encosta na corrida '
            'da gôndola, então só a face da frente trabalha.',
       cap='A ponta é a única com casinha. O painel de fundo fecha a face de trás — a planta '
           'mostra uma face de acesso só.'),
  dict(nome='Paredão', slug='PAREDAO', bc='PSC-04', bcv=717, bl='BLA-01-AC', blv=200,
       pan=(200, 754), vaos=(3, 4, 5), n=8, fundo=True, deck=False, peg=False,
       casinha=False, faces=1,
       lede='O vão mais longo (<strong>PSC-04 717</strong>) e a menor profundidade '
            '(<strong>285 mm</strong>), oito prateleiras a <strong>1.926 mm</strong>. A '
            'corrida não tem limite de vãos: cada um recebe uma <strong>faixa de '
            'categoria</strong> de 90 mm na cabeceira.',
       cap='O paredão é a corrida: cada vão a mais soma 737 mm e uma faixa de categoria. '
           'Fundo fechado, uma face de acesso.'),
]

def bom(f, N):
    n = f['n']; linhas = N+1
    tz, cz, tp = 4*n, 2*(N-1)*n, 2*linhas
    qbc = 2*N*n + (N if f['peg'] else 0)
    qbl, qba, pes = linhas*n, 2*linhas*(n-1), 2*linhas
    mad = (qbc*f['bcv'] + qbl*f['blv'] + qba*BV + pes*60)*GMM
    np_ = N*n + (N*(n-1) if f['fundo'] else 0)
    madp = np_*f['pan'][0]*f['pan'][1]*PANT*DENS
    conn = tz*C_TZ + cz*C_CZ + tp*C_T
    plast = tz*M_TZ + cz*M_CZ + tp*M_T
    custo = conn + (mad+madp)/1000*RSKG
    return dict(tz=tz, cz=cz, tp=tp, qbc=qbc, qbl=qbl, qba=qba, pes=pes, np=np_,
                kg=(mad+madp+plast)/1000, custo=custo,
                L=round(ext_comp(f['bcv'], N)), P=round(ext_prof(f['blv'])),
                A=round(ext_alt(BV, n)))

br = lambda v: f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
mil = lambda v: f'{v:,.0f}'.replace(',', '.')

# ------------------------------------------------------------------ cabecalho
HEADER = '''<header>
  <div class="eyeb"><span class="lab">NITRON · DESENVOLVIMENTO DE PRODUTOS</span>
  <span class="lab">CADERNO DE ESPECIFICAÇÃO · PDV</span><span class="lab">REV. 3 · 04/09/2026</span></div>
  <div class="hg">
    <div><h1>Sistema PDV<br>Nitron Mob</h1><p class="slog">toda casa tem</p>
    <p class="thesis">Medida fixa. <strong>4 ripas de comprimento, 3 de largura, 2 verticais e 12 painéis</strong> — nada fora dessa lista. A cota externa não é a soma das ripas: cada ripa entra <strong>40,60 mm</strong> dentro do nó, e o nó sobra para fora. <strong>Nenhuma ripa nova.</strong></p></div>
    <div class="bars">
      <div class="bar"><b>+42,02</b><span>eixo do <strong>COMPRIMENTO</strong> · nó de 61,61<i>externo = ripa + 42,02 · confirmado pelos 4 painéis</i></span></div>
      <div class="bar"><b>+85,26</b><span>eixo da <strong>PROFUNDIDADE</strong> · nó de 83,23<i>externo = ripa + 85,26 · a tábua apoia e sobressai</i></span></div>
      <div class="bar"><b>+20,10</b><span>cada <strong>VÃO</strong> a mais · cruzeta de 101,30<i>a cruzeta come os mesmos 81,20 e ocupa 101,30</i></span></div>
      <div class="bar"><b>261,9</b><span>passo <strong>VERTICAL</strong> · ripa BAL-02-AC 270<i>modelo A do nó — falta a fita no showroom</i></span></div>
    </div>
  </div>
</header>'''

# ------------------------------------------------------------ §1 conclusoes
CALL1 = '''  <div class="call">
    <span class="lab">O CADASTRO JÁ SEPARA OS DOIS EIXOS — E A LISTA FIXA RESPEITA ISSO</span>
    <p>A família <code>BLA</code> (campo <code>LARGURA</code>) é a ripa que vai da frente ao fundo; a família <code>PSC</code> (campo <code>COMPRIMENTO</code>) é a que vence o vão. A lista fixa usa cada uma no seu papel: <strong>BLA-01-AC 200 · BLA-03-AC 287 · PSC-02 415</strong> na profundidade, <strong>PSC-01 315 · PSC-02 415 · PSC-03 595 · PSC-04 717</strong> no comprimento.</p>
    <p>A <code>PSC-02</code> aparece nas duas listas — é a mesma ripa fazendo dois papéis, o que já acontece no cadastro: ela é comprimento na sapateira e serve de largura na ilha.</p>
  </div>
  <div class="call stop">
    <span class="lab">A LEITURA ANTERIOR — “TRÊS LARGURAS DAS TRÊS REFERÊNCIAS” — FOI SUBSTITUÍDA</span>
    <p>A Rev. 2 fixava três larguras (415 sapateira · 595 multiuso · 717 arara) e deixava profundidade livre entre 19 barras. A Rev. 3 fecha os dois eixos, e o que era “largura fixa” virou o <strong>eixo do comprimento</strong>, com quatro valores em vez de três. Os números de corrida não mudaram — 457, 892, 1.252, 1.496 continuam valendo. O que mudou é que <strong>a profundidade também é fixa</strong>, em três valores, e vem casada com o painel.</p>
  </div>'''

# ----------------------------------------------------------------------- §2
rows = ''.join(
    ('<tr class="hl">' if N in (2, 3) else '<tr>') + f'<td class="n">{N}</td>' +
    ''.join(f'<td class="n">{"<strong>" if N in (2,3) else ""}{mil(round(ext_comp(b,N)))}'
            f'{"</strong>" if N in (2,3) else ""}</td>' for _, b, _ in COMPS) +
    f'<td class="n">4/nível</td><td class="n">{2*(N-1)}/nível</td></tr>'
    for N in range(1, 7))
S2 = f'''  <div class="sh"><span class="snum">§2</span><h2>Comprimento · as 4 ripas e a corrida</h2></div>
  <p class="lede">Quatro ripas de comprimento, cada uma casada com um painel. O <strong>comprimento é a corrida</strong>: N vãos daquela ripa, encadeados pela cruzeta. A trizeta fica fixa em 4 por nível; só a cruzeta cresce, a 2 × (N−1) por nível.</p>
  <div class="tw"><table>
    <caption>Cota externa da corrida em milímetros. Fórmula: 2 × 61,61 + (N−1) × 101,30 + N × (ripa − 81,20).</caption>
    <thead><tr><th>N vãos</th><th>PSC-01 · 315</th><th>PSC-02 · 415</th><th>PSC-03 · 595</th><th>PSC-04 · 717</th><th>Trizetas</th><th>Cruzetas</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <div class="call">
    <span class="lab">A CONFERÊNCIA QUE FECHA O MODELO</span>
    <p>As quatro ripas dão <strong>357,02 · 457,02 · 637,02 · 759,02</strong> mm de cota externa por vão. Os quatro painéis fixados são <strong>360 · 450 · 634 · 754</strong>. Diferença de <strong>+2,98 / −7,02 / −3,02 / −5,02</strong> mm — quatro em quatro dentro de ±7 mm.</p>
    <p>Isso prova que o painel foi cortado na <strong>cota externa do vão</strong>: ele deita sobre os nós e cobre o vão de ponta a ponta. Se fosse cortado no vão livre entre nós, daria 233,8 / 333,8 / 513,8 / 635,8 — e não é o que está na lista.</p>
  </div>'''

# ----------------------------------------------------------------------- §3
ar = ''.join(
    ('<tr class="hl">' if n in (4,5,7,8) else '<tr>') + f'<td class="n">{n}</td>'
    f'<td class="n">{"<strong>" if n in (4,5,7,8) else ""}{mil(round(ext_alt(BV,n)))}'
    f'{"</strong>" if n in (4,5,7,8) else ""}</td>'
    f'<td class="n">{mil(round(ext_alt(BV,n,2)))}</td>'
    f'<td class="n">{mil(round(ext_alt(513,n)))}</td>'
    f'<td>{uso}</td></tr>'
    for n, uso in [(2, 'mesa baixa'), (3, 'mesa de exposição'), (4, '<strong>ilha</strong> · balcão 900'),
                   (5, '<strong>checkout</strong> · display 1.200'), (6, 'gôndola central'),
                   (7, '<strong>ponta de gôndola</strong> · 1.600'), (8, '<strong>paredão</strong> · parede 2.000')])
S3 = f'''  <div class="sh"><span class="snum">§3</span><h2>Altura · duas ripas e uma medida em falta</h2></div>
  <p class="lede">Duas ripas verticais na lista: <strong><code>BAL-02-AC</code> 270</strong>, que dá o passo curto usável para pote, balde e lixeira em pé, e <strong><code>PSA-05</code> 513</strong> para vão alto. Trocar de altura é trocar a contagem de prateleiras, nunca a ripa. As quatro famílias usam a de 270.</p>
  <div class="tw"><table>
    <caption>Altura externa em milímetros. Fórmula: n × 73,08 + (n−1) × (ripa − 81,20) + 19,40 no modelo A.</caption>
    <thead><tr><th>Prateleiras</th><th>BAL-02-AC · modelo A</th><th>BAL-02-AC · modelo B</th><th>PSA-05 · modelo A</th><th>Uso</th></tr></thead>
    <tbody>{ar}</tbody>
  </table></div>
  <div class="call stop">
    <span class="lab">O QUE FALTA MEDIR — E É UMA FITA, NÃO UM ENSAIO</span>
    <p>O encaixe vertical da trizeta <strong>abre para baixo</strong> e a face de topo é fechada (chapa medida em z relativo 70,0–72,9 mm). Por isso a peça sai em <strong>par espelhado ESQ/DIR</strong>, e isso deixa duas leituras do passo: <strong>261,88 mm</strong> (um nó por nível) ou <strong>334,96 mm</strong> (par espelhado). A lista de painéis não resolve — ela só restringe os eixos horizontais.</p>
    <p>Monte duas prateleiras com a ripa de 270 e meça de apoio a apoio. <strong>261,9 → modelo A. 335,0 → modelo B.</strong> Não tem meio. Este caderno usa o modelo A.</p>
  </div>'''

# ----------------------------------------------------------------------- §4
pr = ''.join(
    f'<tr><td class="n">{lp}</td><td class="n">{lr} · {lb}</td>'
    f'<td class="n"><strong>{mil(round(ext_prof(lb)))}</strong></td>'
    f'<td class="n">{"0,00" if lp==lb else br((lp-lb)/2)}</td>'
    f'<td class="n">{mil(lb-CONSOME)}</td><td>{uso}</td></tr>'
    for (lr, lb, lp), uso in zip(LARGS, ['paredão · ponta rasa', 'checkout · ponta', 'ilha']))
paineis = ''.join(
    '<tr>' + f'<td class="n"><strong>{lp}</strong></td>' +
    ''.join(f'<td class="n">{lp} × {cp}</td>' for _, _, cp in COMPS) +
    f'<td class="n">{mil(round(ext_prof(lb)))}</td></tr>'
    for lr, lb, lp in LARGS)
S4 = f'''  <div class="sh"><span class="snum">§4</span><h2>Profundidade · 3 ripas, 12 painéis</h2></div>
  <p class="lede">A profundidade também é fixa agora: três ripas de largura, cada uma casada com uma tábua. A tábua <strong>não</strong> alcança a cota externa — o nó sobra 42,63 mm por lado. Ela apoia nas duas ripas e sobressai um pouco para a frente e para o fundo.</p>
  <div class="tw"><table>
    <caption>Cota externa = ripa + 85,26 mm. A tábua apoia na ripa, não no nó.</caption>
    <thead><tr><th>Tábua</th><th>Ripa de largura</th><th>Profundidade externa</th><th>Sobressai/lado</th><th>Vão livre entre nós</th><th>Onde entra</th></tr></thead>
    <tbody>{pr}</tbody>
  </table></div>
  <div class="tw" style="margin-top:22px"><table>
    <caption>As 12 combinações. Linha = tábua e profundidade; coluna = ripa de comprimento.</caption>
    <thead><tr><th>Tábua</th><th>PSC-01 · vão 357</th><th>PSC-02 · vão 457</th><th>PSC-03 · vão 637</th><th>PSC-04 · vão 759</th><th>Prof. externa</th></tr></thead>
    <tbody>{paineis}</tbody>
  </table></div>
  <div class="call stop"><span class="lab">O LIMITE — E ELE MUDOU DE LUGAR</span>
    <p>A Rev. 2 esbarrava no comprimento de barra (717 mm dava 802 mm de profundidade). A Rev. 3 esbarra na <strong>chapa crua</strong>: a <code>PAN-01</code> tem <strong>200 mm de largura</strong>. A tábua de 200 sai direto; as de <strong>300 e 460 exigem emenda ou chapa mais larga</strong>. É o único item novo de fornecimento em toda a grade — e ele atinge 8 dos 12 painéis.</p></div>'''

# ----------------------------------------------------------------------- §5
render = pathlib.Path(__file__).resolve().parent / 'render'
blocos = ['''  <div class="sh"><span class="snum">§5</span><h2>As quatro famílias</h2></div>
  <p class="lede">Cada uma nasce numa combinação distinta de painel, corrida e altura — não é o mesmo quadro em três tamanhos. Nenhuma repete o painel de outra. O que muda: painel de fundo, top deck, gancheira, casinha e o número de faces de acesso.</p>''']
for f in FAM:
    vs = f['vaos']; mM = vs[1]
    b0 = bom(f, mM)
    tr = ''
    for lab, N in zip('PMG', vs):
        b = bom(f, N)
        tr += (f'<tr><td><strong>{lab}</strong></td><td class="n">{N}</td>'
               f'<td class="n">{"<strong>" if lab=="M" else ""}{b["L"]} × {b["P"]} × {b["A"]}'
               f'{"</strong>" if lab=="M" else ""}</td>'
               f'<td class="n">{b["tz"]}</td><td class="n">{b["cz"]}</td><td class="n">{b["tp"]}</td>'
               f'<td class="n">{b["qbc"]}</td><td class="n">{b["qbl"]}</td><td class="n">{b["qba"]}</td>'
               f'<td class="n">{b["np"]}</td><td class="n">{br(b["kg"])} kg</td>'
               f'<td class="n">R$ {br(b["custo"])}</td><td class="n">R$ {br(2*b["custo"])}</td></tr>')
    svg = (render / f'pdv-fam-{f["slug"]}.svg').read_text(encoding='utf-8')
    blocos.append(f'''
  <h3 style="margin-top:46px;font-size:21px">{f["nome"]} · painel {f["pan"][0]} × {f["pan"][1]} · {f["n"]} prateleiras · {mil(b0["A"])} mm</h3>
  <p class="lede" style="font-size:14.5px">{f["lede"]}</p>
  <div class="tw"><table>
    <caption>Ripa de comprimento <code>{f["bc"]}</code> {f["bcv"]} · ripa de largura <code>{f["bl"]}</code> {f["blv"]} · vertical <code>BAL-02-AC</code> 270. Custo por escala de massa, não apurado.</caption>
    <thead><tr><th>Ver.</th><th>Vãos</th><th>L × P × A (mm)</th><th>Trizeta</th><th>Cruzeta</th><th>Tampa</th>
    <th>Ripa {f["bcv"]}</th><th>Ripa {f["blv"]}</th><th>Ripa 270</th><th>Painéis</th><th>Peso</th><th>Custo</th><th>2× custo</th></tr></thead>
    <tbody>{tr}</tbody></table></div>
  <figure class="plate"><div class="pin">{svg}</div><figcaption>{f["nome"]} M — {mil(b0["L"])} × {b0["P"]} × {mil(b0["A"])} mm, {mM} vão{"s" if mM>1 else ""}, painel {f["pan"][0]} × {f["pan"][1]}. {f["cap"]}</figcaption></figure>''')
S5 = '\n'.join(blocos)

# ----------------------------------------------------------------------- §8
S8 = '''  <div class="sh"><span class="snum">§8</span><h2>O que falta</h2></div>
  <ol class="steps">
    <li><span><strong>A fita do passo vertical.</strong> Monte duas prateleiras com a ripa <code>BAL-02-AC</code> de 270 e meça de apoio a apoio: <strong>261,9 mm confirma o modelo A, 335,0 mm o modelo B.</strong> É a única cota do sistema que a lista de painéis não fecha, e ela muda todas as alturas deste caderno.</span></li>
    <li><span><strong>A profundidade externa montada.</strong> Um nó com a ripa <code>BLA-01-AC</code> de 200, medindo face externa a face externa, deve dar <strong>285,3 mm</strong>. Se der outro número, a extensão de 83,23 mm do nó nesse eixo precisa ser remedida.</span></li>
    <li><span><strong>A decisão do painel.</strong> A chapa <code>PAN-01</code> (1.200 × 200 × 15) só tem 200 mm de largura. <strong>8 dos 12 painéis</strong> — todos os de 300 e 460 — precisam de emenda, tira aparente ou chapa nova.</span></li>
    <li><span><strong>Ferramentaria: onde está o molde da cruzeta?</strong> Só as versões de 1 vão (ilha P e ponta P) rodam sem ela. Primeira de cinco cadastrada em 17/07/2026, quatro já injetadas; ainda não sabemos se as 2 cavidades são o par esq/dir.</span></li>
    <li><span><strong>Montar um nó de cruzeta e carregá-lo.</strong> A chapa 1 da trizeta está em z relativo 40,0 mm, exatamente onde o encaixe de 40,60 mm termina — a ripa apoia numa chapa de 2,9 mm, dando 8,5–18,4 MPa. A carga de 20 kg por prateleira é provisória.</span></li>
    <li><span><strong>Aprovação de marca para o verde</strong> <code>#08a9b1</code> contra o <code>#1EA7AC</code> declarado no manual.</span></li>
    <li><span><strong>A tampinha</strong> — STL não recebido. São 8 a 12 tampas por módulo, entrando na conta pelo peso cadastrado (1,10 g).</span></li>
  </ol>'''

FOOTER = '''<footer><p>Papéis das ripas extraídos de <code>VW_COMPOSICAO_NIT</code> para as 13 PAs com estrutura. Cotas de nó, encaixe e parede medidas nas malhas STL — as cinco fechadas, zero arestas não-manifold. Painéis e ripas conforme a lista fixa do usuário. Identidade visual, tipografia e regras de PDV do manual oficial em <a href="https://marca.nitron.com.br/">marca.nitron.com.br</a>. Cotas externas pelo modelo de encaixe de 40,60 mm em nó de 61,61 mm no eixo do comprimento, 83,23 mm no da profundidade e 73,08 mm no vertical — o eixo do comprimento está confirmado pela própria lista de painéis; <strong>o vertical depende do modelo de nó, ainda não medido fisicamente</strong>. Custos estimados por escala de massa, não apurados. Nada gravado em <code>pdp_lancamento</code>.</p></footer>'''

# ------------------------------------------------------------------- aplica
# Idempotente: pode rodar de novo sobre um caderno ja convertido.
S6_ROWS = '''      <tr class="hl"><td><strong>Painel</strong></td><td class="n">300 × 450</td><td class="n">460 × 634</td><td class="n">300 × 634</td><td class="n">200 × 754</td></tr>
      <tr><td><strong>Ripa de comprimento</strong></td><td class="n">PSC-02 · 415</td><td class="n">PSC-03 · 595</td><td class="n">PSC-03 · 595</td><td class="n">PSC-04 · 717</td></tr>
      <tr><td><strong>Ripa de largura</strong></td><td class="n">BLA-03-AC · 287</td><td class="n">PSC-02 · 415</td><td class="n">BLA-03-AC · 287</td><td class="n">BLA-01-AC · 200</td></tr>
      <tr class="hl"><td><strong>Medida final M</strong></td><td class="n">892 × 372 × 1.140</td><td class="n">1.252 × 500 × 878</td><td class="n">1.252 × 372 × 1.664</td><td class="n">2.970 × 285 × 1.926</td></tr>
      <tr><td><strong>Prateleiras</strong></td><td class="n">5</td><td class="n">4</td><td class="n">7</td><td class="n">8</td></tr>
'''
S6_CAP = ('<caption>O que diferencia as fam\u00edlias. As cinco primeiras linhas s\u00e3o '
          'dimensionais \u2014 <strong>nenhuma repete o painel de outra</strong>. As demais saem '
          'de pe\u00e7a que j\u00e1 existe; a gancheira \u00e9 uma ripa de comprimento montada '
          'na horizontal.</caption>')

p_doc = pathlib.Path(__file__).resolve().parent / '09-pdv-sistema-modular.html'
h = p_doc.read_text(encoding='utf-8')

# 1. chaves duplicadas: o <style> foi gerado por template e ficou com {{ }}
fim = h.index('</style>')
css, resto = h[:fim], h[fim:]
if ':root{{' in css:
    css = css.replace('{{', '{').replace('}}', '}')
    h = css + resto
    print('  corrigidas chaves duplicadas no <style>')

def troca_secao(h, num, novo):
    pat = re.compile(r'<section>\s*\n(  <div class="sh"><span class="snum">\u00a7' + str(num) +
                     r'</span>.*?)\n</section>', re.S)
    m = pat.search(h)
    assert m, f'\u00a7{num} nao encontrado'
    return h[:m.start()] + '<section>\n' + novo + '\n</section>' + h[m.end():]

m = re.search(r'<header>.*?</header>', h, re.S); assert m
h = h[:m.start()] + HEADER + h[m.end():]

m = re.search(r'  <div class="call(?: stop)?">\s*\n    <span class="lab">'
              r'(?:O CAMPO LARGURA|O CADASTRO J\u00c1 SEPARA).*?\n  </div>\n</section>', h, re.S)
assert m, 'calls do \u00a71 nao encontrados'
h = h[:m.start()] + CALL1 + '\n</section>' + h[m.end():]

for num, novo in ((2, S2), (3, S3), (4, S4), (5, S5), (8, S8)):
    h = troca_secao(h, num, novo)

# 6. as linhas dimensionais do §6
m = re.search(r'    <caption>(?:Os cinco elementos|O que diferencia).*?</caption>', h, re.S)
assert m, 'caption do \u00a76 nao encontrada'
h = h[:m.start()] + '    ' + S6_CAP + h[m.end():]
m = re.search(r'(<tbody>\n)((?:      <tr[^\n]*\n)*?)'
              r'(      <tr><td><strong>Painel de fundo</strong></td>)', h)
assert m, 'tbody do \u00a76 nao encontrado'
h = h[:m.start()] + m.group(1) + S6_ROWS + m.group(3) + h[m.end():]

m = re.search(r'<footer>.*?</footer>', h, re.S); assert m
h = h[:m.start()] + FOOTER + h[m.end():]

p_doc.write_text(h, encoding='utf-8')
print(f'{p_doc.name}: {len(h)} bytes')
for f in FAM:
    b = bom(f, f['vaos'][1])
    print(f"  {f['nome']:20} {b['L']:5} x {b['P']:4} x {b['A']:5}  "
          f"painel {f['pan'][0]}x{f['pan'][1]}  R$ {br(b['custo'])}")
