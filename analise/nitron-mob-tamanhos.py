#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planilha de todas as possibilidades de tamanho do modulo Nitron Mob.

Tudo e formula sobre a aba Parametros: as cotas de encaixe vieram das malhas
STL e ainda nao foram conferidas em peca fisica -- quando forem, muda-se a
celula e o resto recalcula. Gera dados/44-nitron-mob-tamanhos.xlsx.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / 'dados' / '44-nitron-mob-tamanhos.xlsx'
F = 'Arial'
fh = Font(name=F, bold=True, size=10, color='FFFFFF')
fb = Font(name=F, size=10)
fB = Font(name=F, size=10, bold=True)
fin = Font(name=F, size=10, color='0000FF')            # entrada
flink = Font(name=F, size=10, color='008000')          # link de outra aba
ft = Font(name=F, size=14, bold=True)
fnote = Font(name=F, size=9, italic=True, color='555555')
HEAD = PatternFill('solid', fgColor='1EA7AC')
YEL = PatternFill('solid', fgColor='FFFF00')
GREY = PatternFill('solid', fgColor='F2F2F2')
thin = Side(style='thin', color='BFBFBF')
box = Border(left=thin, right=thin, top=thin, bottom=thin)
C = Alignment(horizontal='center', vertical='center')
R = Alignment(horizontal='right')
WR = Alignment(wrap_text=True, vertical='top')
MM = '#,##0.0'; MM0 = '#,##0'

wb = Workbook()

def title(ws, t, sub=None):
    ws['A1'] = t; ws['A1'].font = ft
    if sub: ws['A2'] = sub; ws['A2'].font = fnote
def header(ws, row, cols, start=1):
    for i, c in enumerate(cols):
        cell = ws.cell(row=row, column=start+i, value=c)
        cell.font = fh; cell.fill = HEAD; cell.alignment = C; cell.border = box
def widths(ws, w):
    for i, x in enumerate(w, 1): ws.column_dimensions[L(i)].width = x

# ============================================================ Parametros
P = wb.active; P.title = 'Parametros'
title(P, 'Nitron Mob — parâmetros do sistema',
      'Células azuis são entradas. As amarelas vieram da malha STL e ainda não foram conferidas com trena: mude aqui e tudo recalcula.')
header(P, 4, ['Parâmetro', 'Símbolo', 'Valor (mm)', 'Origem', 'Como conferir'])
params = [
 ('Profundidade do encaixe da ripa no nó', 'ENC', 40.60, 'malha STL', 'ripa dentro da trizeta até o fundo', True),
 ('Trizeta · eixo do comprimento', 'NOX', 61.61, 'malha STL', 'largura externa da trizeta', True),
 ('Cruzeta · eixo do comprimento', 'NOXC', 101.30, 'malha STL', 'largura externa da cruzeta', True),
 ('Trizeta · eixo da profundidade', 'NOY', 83.23, 'malha STL', 'PROFUNDIDADE externa com painel de 200 deve dar 285,3', True),
 ('Trizeta · eixo vertical (passo do nó)', 'NOZ', 73.08, 'malha STL', 'PASSO VERTICAL de uma baia de 270 deve dar 261,88 (rival: 335,0)', True),
 ('Peça L · sobra por lado (coroa)', 'NOL', 21.92, 'malha STL', 'SOBRA da peça L por lado deve dar 21,62', True),
 ('Pé exposto abaixo do primeiro nó', 'PE', 19.40, 'malha STL', 'do chão à face inferior da trizeta', True),
 ('Espessura do painel (pinus)', 'PANT', 15.00, 'informado', 'paquímetro no painel', False),
 ('Ripa consome no total (2 × ENC)', 'CONSOME', '=2*C5', 'fórmula', '', False),
 ('Regra de proporção do painel · mínimo', 'RAZ_MIN', 1.3, 'decisão', 'comprimento ÷ largura', False),
 ('Regra de proporção do painel · máximo', 'RAZ_MAX', 2.6, 'decisão', 'comprimento ÷ largura', False),
]
for i, (nome, sim, val, org, conf, chk) in enumerate(params):
    r = 5+i
    P.cell(r, 1, nome).font = fb
    P.cell(r, 2, sim).font = fB
    c = P.cell(r, 3, val); c.number_format = '0.00'
    c.font = fb if isinstance(val, str) else fin
    if chk: c.fill = YEL
    P.cell(r, 4, org).font = fb; P.cell(r, 5, conf).font = fnote
    for k in range(1, 6): P.cell(r, k).border = box
# nomes das celulas
NAMES = dict(ENC='Parametros!$C$5', NOX='Parametros!$C$6', NOXC='Parametros!$C$7', NOY='Parametros!$C$8',
             NOZ='Parametros!$C$9', NOL='Parametros!$C$10', PE='Parametros!$C$11', PANT='Parametros!$C$12',
             CONSOME='Parametros!$C$13', RAZ_MIN='Parametros!$C$14', RAZ_MAX='Parametros!$C$15')

r0 = 18
P.cell(r0, 1, 'Ripas de LARGURA (fixam a profundidade — uma por módulo)').font = fB
header(P, r0+1, ['Código', 'Largura (mm)', 'Painel (largura)'])
LARG = [('BLA-01-AC', 200, 200), ('BLA-03-AC', 287, 300), ('PSC-02', 415, 460)]
for i, (c, v, p) in enumerate(LARG):
    r = r0+2+i
    P.cell(r, 1, c).font = fb; P.cell(r, 2, v).font = fin; P.cell(r, 3, p).font = fin
    for k in range(1, 4): P.cell(r, k).border = box
r1 = r0+2+len(LARG)+1
P.cell(r1, 1, 'Ripas de COMPRIMENTO (uma por vão)').font = fB
header(P, r1+1, ['Código', 'Comprimento (mm)', 'Painel (comprimento)'])
COMP = [('PSC-01', 315, 360), ('PSC-02', 415, 450), ('PSC-03', 595, 634), ('PSC-04', 717, 754)]
for i, (c, v, p) in enumerate(COMP):
    r = r1+2+i
    P.cell(r, 1, c).font = fb; P.cell(r, 2, v).font = fin; P.cell(r, 3, p).font = fin
    for k in range(1, 4): P.cell(r, k).border = box
r2 = r1+2+len(COMP)+1
P.cell(r2, 1, 'Ripas de ALTURA (uma por baia; a peça L usa a mesma ripa como coroa)').font = fB
header(P, r2+1, ['Código', 'Altura (mm)'])
ALT = [('BAL-02-AC', 270), ('PSA-05', 513)]
for i, (c, v) in enumerate(ALT):
    r = r2+2+i
    P.cell(r, 1, c).font = fb; P.cell(r, 2, v).font = fin
    for k in range(1, 3): P.cell(r, k).border = box
LARG_ROWS = {v: r0+2+i for i, (_, v, _) in enumerate(LARG)}
COMP_ROWS = {v: r1+2+i for i, (_, v, _) in enumerate(COMP)}
ALT_ROWS = {v: r2+2+i for i, (_, v) in enumerate(ALT)}
r3 = r2+2+len(ALT)+1
P.cell(r3, 1, 'Fonte: malhas STL das cinco peças (trizeta, cruzeta, peça L, porta-haste, tampa) medidas em 04/09/2026; ripas e painéis conforme lista fixada pelo marketing em 05/09/2026. '
              'Corroboração: ripas 315/415/595/717 + 42,02 dão 357/457/637/759 contra painéis 360/450/634/754 — quatro em quatro dentro de ±7 mm.').font = fnote
P.cell(r3, 1).alignment = WR; P.merge_cells(start_row=r3, start_column=1, end_row=r3+2, end_column=5)
widths(P, [46, 12, 13, 12, 62])
P.freeze_panes = 'A5'

# ============================================================ Comprimento
W = wb.create_sheet('Comprimento')
title(W, 'Comprimento externo do módulo (mm)',
      'Fórmula: 2 × NOX + (N − 1) × NOXC + N × (ripa − CONSOME). A coroa (peça L) acrescenta 2 × NOL de cada lado do topo — não muda a base.')
header(W, 4, ['N vãos'] + [f'{c} · {v}' for c, v, _ in COMP] + [''] + [f'{c} com coroa' for c, v, _ in COMP])
W.cell(5, 1, 'painel →').font = fnote
for j, (c, v, p) in enumerate(COMP):
    W.cell(5, 2+j, f'{p} mm').font = fnote; W.cell(5, 2+j).alignment = C
NMAX = 20
for n in range(1, NMAX+1):
    r = 5+n
    W.cell(r, 1, n).font = fB; W.cell(r, 1).alignment = C; W.cell(r, 1).border = box
    for j, (c, v, p) in enumerate(COMP):
        ripa = f'Parametros!$B${COMP_ROWS[v]}'
        f = f'=2*{NAMES["NOX"]}+(A{r}-1)*{NAMES["NOXC"]}+A{r}*({ripa}-{NAMES["CONSOME"]})'
        cell = W.cell(r, 2+j, f); cell.number_format = MM; cell.font = fb; cell.border = box
        g = W.cell(r, 7+j, f'={L(2+j)}{r}+2*{NAMES["NOL"]}'); g.number_format = MM; g.font = fb; g.border = box
W.cell(6+NMAX+1, 1, 'Conferência com o showroom: PSC-04 × 18 = 13.290 (parede sul 13.350, folga 60) · PSC-01 × 18 = 6.054 (norte 6.100) · PSC-03 × 11 = 6.788 (fundo 6.873) · PSC-02 × 15 = 6.548 (entrada).').font = fnote
widths(W, [9, 15, 15, 15, 15, 3, 17, 17, 17, 17])
W.freeze_panes = 'B6'

# ============================================================ Profundidade
D = wb.create_sheet('Profundidade')
title(D, 'Profundidade externa do módulo (mm)',
      'Fórmula: ripa de largura + 2 × (NOY − ENC). UMA profundidade por módulo: a ripa de largura fixa a distância entre os postes, e os postes são contínuos.')
header(D, 4, ['Ripa de largura', 'Ripa (mm)', 'Profundidade externa', 'Painel (largura)', 'Sobra do painel por lado', 'Painel vs. externo'])
for i, (c, v, p) in enumerate(LARG):
    r = 5+i
    D.cell(r, 1, c).font = fb
    D.cell(r, 2, f'=Parametros!$B${LARG_ROWS[v]}').font = flink
    x = D.cell(r, 3, f'=B{r}+2*({NAMES["NOY"]}-{NAMES["ENC"]})'); x.number_format = MM; x.font = fB
    D.cell(r, 4, f'=Parametros!$C${LARG_ROWS[v]}').font = flink
    y = D.cell(r, 5, f'=(D{r}-B{r})/2'); y.number_format = MM; y.font = fb
    z = D.cell(r, 6, f'=D{r}-C{r}'); z.number_format = MM; z.font = fb
    for k in range(1, 7): D.cell(r, k).border = box
D.cell(9, 1, 'O painel apoia nas duas ripas de largura e sobressai (D−B)/2 de cada lado: 0 no de 200, 6,5 no de 300, 22,5 no de 460. Ele nunca alcança a cota externa — o nó sobra 42,63 por lado.').font = fnote
D.cell(10, 1, 'Padrão de varejo para referência: prateleira superior 200–400 mm, base 300–500 mm, gôndola dupla face 813–1.219 mm.').font = fnote
widths(D, [18, 11, 20, 15, 22, 18])

# ============================================================ Altura
A = wb.create_sheet('Altura')
title(A, 'Altura externa do módulo por composição de baias (mm)',
      'Fórmula: PE + (n_baias + 1) × NOZ + Σ(ripa − CONSOME). Só as CONTAGENS importam para a altura total; a ORDEM muda as faces (ver aba Pilha). Prateleiras = baias + 1.')
def bloco(ws, top, rot, coroa):
    ws.cell(top, 1, rot).font = fB
    header(ws, top+1, ['baias de 270 ↓ / baias de 513 →'] + [str(k) for k in range(0, 5)])
    for i in range(0, 8):
        r = top+2+i
        ws.cell(r, 1, i).font = fB; ws.cell(r, 1).alignment = C; ws.cell(r, 1).border = box
        for k in range(0, 5):
            n270 = f'$A{r}'; n513 = f'{L(2+k)}${top+1}'
            extra = f'+({NAMES["NOZ"]}+Parametros!$B${ALT_ROWS[coroa]}-{NAMES["CONSOME"]})' if coroa else ''
            f = (f'=IF({n270}+{n513}=0,"",{NAMES["PE"]}+({n270}+{n513}+1)*{NAMES["NOZ"]}'
                 f'+{n270}*(Parametros!$B${ALT_ROWS[270]}-{NAMES["CONSOME"]})'
                 f'+{n513}*(Parametros!$B${ALT_ROWS[513]}-{NAMES["CONSOME"]}){extra})')
            c = ws.cell(r, 2+k, f); c.number_format = MM0; c.font = fb; c.border = box; c.alignment = C
    return top+2+8
nxt = bloco(A, 4, 'SEM coroa — módulo termina na última prateleira', None)
nxt = bloco(A, nxt+1, 'COM coroa de 270 (peça L no topo, ganha um nível sem prateleira — gancheira ou arara)', 270)
nxt = bloco(A, nxt+1, 'COM coroa de 513', 513)
A.cell(nxt+1, 1, 'Conferência: 270 × 6 = 1.664 (paredões sul e norte) · 513·513·270·270 = 1.626 (fundo e entrada). Nada acima de 1.700 fica na zona do topo do varejo; a coroa NÃO conta como prateleira.').font = fnote
A.cell(nxt+2, 1, 'Cabe na baia: 270 → vão livre de ' ).font = fnote
A.cell(nxt+2, 2, f'=Parametros!$B${ALT_ROWS[270]}-{NAMES["CONSOME"]}+{NAMES["NOZ"]}-{NAMES["PANT"]}').number_format = MM
A.cell(nxt+2, 3, 'mm · 513 → ').font = fnote
A.cell(nxt+2, 4, f'=Parametros!$B${ALT_ROWS[513]}-{NAMES["CONSOME"]}+{NAMES["NOZ"]}-{NAMES["PANT"]}').number_format = MM
A.cell(nxt+2, 5, 'mm (produto mais alto que isso não entra)').font = fnote
widths(A, [34, 10, 10, 10, 10, 10])

# ============================================================ Pilha (calculadora)
Q = wb.create_sheet('Pilha')
title(Q, 'Calculadora de pilha — altura de cada prateleira',
      'Digite a ripa de cada baia (270 ou 513) de baixo para cima nas células azuis; deixe em branco as que não usar. Face da prateleira = topo do nó + metade do painel.')
header(Q, 4, ['Baia (de baixo p/ cima)', 'Ripa (mm)', 'Prateleira nº', 'Face da prateleira (mm)', 'Vão livre acima (mm)', 'Zona do varejo'])
DEF = [270, 270, 270, 270, 270, 270, '', '']
for i in range(8):
    r = 5+i
    Q.cell(r, 1, i+1).font = fB; Q.cell(r, 1).alignment = C
    b = Q.cell(r, 2, DEF[i]); b.font = fin; b.fill = YEL; b.alignment = C
    Q.cell(r, 3, f'=IF(OR(B{r}<>"",A{r}=1),A{r},"")').alignment = C
    # face_i = PE + i*NOZ + soma_{j<i}(ripa_j - CONSOME) + PANT/2   (i = nº do nível, 1-based)
    soma = f'SUM($B$5:B{r-1})-COUNT($B$5:B{r-1})*{NAMES["CONSOME"]}' if i > 0 else '0'
    f = f'=IF(C{r}="","",{NAMES["PE"]}+A{r}*{NAMES["NOZ"]}+{soma}+{NAMES["PANT"]}/2)'
    c = Q.cell(r, 4, f); c.number_format = MM0; c.font = fB; c.alignment = C
    v = Q.cell(r, 5, f'=IF(B{r}="","",B{r}-{NAMES["CONSOME"]}+{NAMES["NOZ"]}-{NAMES["PANT"]})'); v.number_format = MM0; v.alignment = C
    z = Q.cell(r, 6, f'=IF(D{r}="","",IF(D{r}<=800,"chão",IF(D{r}<=1400,"mãos",IF(D{r}<=1700,"olhos","topo"))))'); z.alignment = C
    for k in range(1, 7): Q.cell(r, k).border = box
# a ultima prateleira (topo do modulo) = nivel n+1
r = 13
Q.cell(r, 1, 'topo').font = fB; Q.cell(r, 1).alignment = C
Q.cell(r, 3, '=COUNT(B5:B12)+1').alignment = C
Q.cell(r, 4, f'={NAMES["PE"]}+C{r}*{NAMES["NOZ"]}+SUM(B5:B12)-COUNT(B5:B12)*{NAMES["CONSOME"]}+{NAMES["PANT"]}/2').number_format = MM0
Q.cell(r, 4).font = fB; Q.cell(r, 4).alignment = C
Q.cell(r, 6, f'=IF(D{r}<=800,"chão",IF(D{r}<=1400,"mãos",IF(D{r}<=1700,"olhos","topo")))').alignment = C
for k in range(1, 7): Q.cell(r, k).border = box
Q.cell(15, 1, 'Altura externa do módulo').font = fB
Q.cell(15, 4, f'={NAMES["PE"]}+(COUNT(B5:B12)+1)*{NAMES["NOZ"]}+SUM(B5:B12)-COUNT(B5:B12)*{NAMES["CONSOME"]}').number_format = MM
Q.cell(15, 4).font = fB
Q.cell(16, 1, 'Prateleiras').font = fB; Q.cell(16, 4, '=COUNT(B5:B12)+1').font = fB
Q.cell(17, 1, 'Razão altura ÷ base (500 mm)').font = fB; Q.cell(17, 4, '=D15/Profundidade!C7').number_format = '0.00'
Q.cell(17, 5, ': 1  · acima de 3 pede ancoragem na parede').font = fnote
Q.cell(19, 1, 'Zonas do varejo: chão até 800 · mãos 800–1.400 · olhos 1.400–1.700 (vende 35–50% mais) · topo acima de 1.700. Exemplo carregado: 270 × 6 = paredão sul, faces 100 · 362 · 624 · 886 · 1.148 · 1.409 · 1.671.').font = fnote
widths(Q, [24, 11, 13, 22, 20, 15])

# ============================================================ Paineis
PN = wb.create_sheet('Paineis')
title(PN, 'A grade de painéis e a regra da proporção',
      'Das 12 combinações largura × comprimento, ficam as que têm comprimento ÷ largura entre RAZ_MIN e RAZ_MAX. As demais saem para não estocar peça que empena (200 estreito e longo) ou quase quadrado.')
header(PN, 4, ['Largura ↓ / Comprimento →'] + [str(p) for _, _, p in COMP])
for i, (c, v, p) in enumerate(LARG):
    r = 5+i
    PN.cell(r, 1, p).font = fB; PN.cell(r, 1).alignment = C; PN.cell(r, 1).border = box
    for j, (cc, vv, pp) in enumerate(COMP):
        f = f'=IF(AND({L(2+j)}$4/$A{r}>={NAMES["RAZ_MIN"]},{L(2+j)}$4/$A{r}<={NAMES["RAZ_MAX"]}),TEXT({L(2+j)}$4/$A{r},"0.00")&" ✔","sai · "&TEXT({L(2+j)}$4/$A{r},"0.00"))'
        cell = PN.cell(r, 2+j, f); cell.font = fb; cell.alignment = C; cell.border = box
PN.cell(9, 1, 'Painéis que ficam (7):').font = fB
PN.cell(9, 2, '=SUMPRODUCT(--(RIGHT(B5:E7,1)="✔"))').font = fB
PN.cell(10, 1, 'Os sete: 200×360 · 200×450 · 300×450 · 300×634 · 300×754 · 460×634 · 460×754. Saem: 200×634 e 200×754 (empenam), 300×360, 460×360 e 460×450 (quase quadrados).').font = fnote
widths(PN, [26, 12, 12, 12, 12])

# ============================================================ Modulos
M = wb.create_sheet('Modulos')
title(M, 'Todas as combinações de painel × número de vãos',
      'Um módulo = uma ripa de largura (profundidade) + uma ripa de comprimento (vão) × N vãos + uma pilha de baias (altura). Aqui variam painel e N; a altura vem da aba Altura ou da calculadora Pilha.')
M.cell(4, 1, 'Nº de prateleiras para a contagem de peças →').font = fB
nb = M.cell(4, 5, 7); nb.font = fin; nb.fill = YEL; nb.alignment = C
M.cell(4, 6, '(baias + 1; o exemplo é a pilha 270 × 6)').font = fnote
header(M, 6, ['Painel', 'Largura (ripa)', 'Comprimento (ripa)', 'N vãos', 'Comprimento externo', 'Profundidade externa', 'Área de piso (m²)',
              'Frente por prateleira (m)', 'Trizetas', 'Cruzetas', 'Peças L (coroa)', 'Tampas', 'Painéis', 'Ripas de comprimento', 'Ripas de largura', 'Ripas verticais'])
r = 7
validos = [(lp, cp) for lp in LARG for cp in COMP if 1.3 <= cp[2]/lp[2] <= 2.6]
for (lc, lv, lp), (cc, cv, cp) in validos:
    for n in range(1, 19):
        M.cell(r, 1, f'{lp}×{cp}').font = fB
        M.cell(r, 2, f'=Parametros!$B${LARG_ROWS[lv]}').font = flink
        M.cell(r, 3, f'=Parametros!$B${COMP_ROWS[cv]}').font = flink
        M.cell(r, 4, n).font = fin
        e = M.cell(r, 5, f'=2*{NAMES["NOX"]}+(D{r}-1)*{NAMES["NOXC"]}+D{r}*(C{r}-{NAMES["CONSOME"]})'); e.number_format = MM
        p_ = M.cell(r, 6, f'=B{r}+2*({NAMES["NOY"]}-{NAMES["ENC"]})'); p_.number_format = MM
        M.cell(r, 7, f'=E{r}*F{r}/1000000').number_format = '0.000'
        M.cell(r, 8, f'=E{r}/1000').number_format = '0.00'
        M.cell(r, 9, f'=4*$E$4')                       # trizetas: 4 cantos por nível
        M.cell(r, 10, f'=2*(D{r}-1)*$E$4')             # cruzetas: 2 por poste interno por nível
        M.cell(r, 11, 0)                                # peças L: 4 se houver coroa (ver nota)
        M.cell(r, 12, f'=2*(D{r}+1)')                  # tampas: uma por poste
        M.cell(r, 13, f'=D{r}*$E$4')                   # painéis: um por vão por prateleira
        M.cell(r, 14, f'=2*D{r}*$E$4')                 # ripas de comprimento: frente e fundo
        M.cell(r, 15, f'=(D{r}+1)*$E$4')               # ripas de largura: uma por linha de postes
        M.cell(r, 16, f'=2*(D{r}+1)*($E$4-1)')         # ripas verticais: 2 por linha de postes por baia
        for k in range(1, 17):
            M.cell(r, k).border = box
            if M.cell(r, k).font == Font(): M.cell(r, k).font = fb
        r += 1
M.cell(r+1, 1, 'Contagem de peças pela lógica do caderno (analise/pdv-caderno.py): trizetas 4 por nível · cruzetas 2 por poste interno por nível · tampas 2 por linha de postes · painéis N por prateleira. '
                'Com coroa (peça L): +4 peças L, +2 tampas por linha, +1 ripa vertical por poste e as cruzetas ganham um nível. Painel de fundo não está contado.').font = fnote
M.cell(r+1, 1).alignment = WR; M.merge_cells(start_row=r+1, start_column=1, end_row=r+2, end_column=10)
M.cell(r+4, 1, 'Cruzetas para as quatro paredes do showroom: 716. Injetadas até hoje: 4.').font = fB
widths(M, [11, 12, 15, 8, 18, 18, 14, 18, 9, 9, 13, 8, 9, 17, 14, 13])
M.freeze_panes = 'E7'
M.auto_filter.ref = f'A6:P{r-1}'

# legenda
LG = wb.create_sheet('Leia-me')
title(LG, 'Como usar esta planilha')
notas = [
 ('Azul', 'entrada — pode mudar'), ('Preto', 'fórmula — não digite em cima'), ('Verde', 'valor puxado da aba Parametros'),
 ('Amarelo', 'cota medida na malha STL e AINDA NÃO conferida em peça física, ou célula de escolha do usuário'),
 ('', ''),
 ('Parametros', 'as cotas do sistema. Três fitas no showroom validam ou derrubam tudo: passo vertical de uma baia de 270 (esperado 261,88), profundidade externa com painel 200 (285,3), sobra da peça L por lado (21,62).'),
 ('Comprimento', 'comprimento externo para cada ripa × N vãos, com e sem coroa'),
 ('Profundidade', 'as três profundidades possíveis — uma por módulo, sem afinar por prateleira'),
 ('Altura', 'altura total por contagem de baias de 270 e 513, sem e com coroa'),
 ('Pilha', 'calculadora: digite a sequência de baias e leia a face de cada prateleira e a zona do varejo'),
 ('Paineis', 'a grade de 12 e a regra da proporção que deixa 7'),
 ('Modulos', 'as 126 combinações painel × N vãos com comprimento, profundidade, área de piso e contagem de peças; filtre pela linha 6'),
]
for i, (a, b) in enumerate(notas):
    LG.cell(3+i, 1, a).font = fB; LG.cell(3+i, 2, b).font = fb; LG.cell(3+i, 2).alignment = WR
LG.cell(3, 1).font = Font(name=F, bold=True, color='0000FF'); LG.cell(5, 1).font = Font(name=F, bold=True, color='008000'); LG.cell(6, 1).fill = YEL
widths(LG, [14, 110])
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if c.font.name != F: c.font = Font(name=F, size=c.font.size or 10, bold=c.font.bold, italic=c.font.italic, color=c.font.color)
wb.move_sheet('Leia-me', offset=-(len(wb.sheetnames)-1))
wb.save(OUT); print('gravado', OUT, '·', len(validos)*18, 'módulos')
