#!/usr/bin/env python3
"""Cota externa real do modulo Nitron Mob — Rev. 2.

A ripa entra dentro do no; a medida final NAO e a soma das ripas. Este script
fecha as contas a partir das grandezas medidas nas malhas STL das pecas de
linha e cruza o resultado com a lista fixa de paineis e ripas.

Rev. 2 acrescenta:
  - a REGRA DA PROPORCAO, que reduz a grade de 12 para 7 paineis
  - a PECA L como no de topo (coroa), que da altura sem somar prateleira
  - a pilha de baias de altura mista

Gera:
  dados/22-mob-cota-modelo.csv       as constantes e as formulas
  dados/23-mob-paineis-grade.csv     as 12 combinacoes com a decisao de cada
  dados/24-mob-cota-corridas.csv     comprimento externo por numero de vaos
  dados/25-mob-cota-alturas.csv      altura externa por pilha e por coroa
"""
import csv, pathlib

# grandezas medidas nas malhas (fechadas, 0 arestas nao-manifold)
ENC  = 40.60    # profundidade do encaixe: quanto a ripa entra no no
NOX  = 61.61    # extensao da trizeta no eixo do COMPRIMENTO
NOXC = 101.30   # extensao da CRUZETA no eixo do comprimento
NOL  = 83.23    # extensao da peca L no eixo em que ela trabalha
NOY  = 83.23    # extensao do no no eixo da PROFUNDIDADE
NOZ  = 73.08    # extensao do no no eixo VERTICAL — igual na trizeta e no L
PE   = 60 - ENC # pe BPE-01-AC de 60 mm menos o encaixe = trecho exposto
CONSOME = 2*ENC # 81,20 mm que os dois nos comem de cada ripa
PANT = 15       # espessura do painel

# a regra: comprimento entre 1,3 e 2,6 vezes a largura
RAZ_MIN, RAZ_MAX = 1.30, 2.60

COMPS = [('PSC-01',315,360), ('PSC-02',415,450), ('PSC-03',595,634), ('PSC-04',717,754)]
LARGS = [('BLA-01-AC',200,200,'rasa'), ('BLA-03-AC',287,300,'media'), ('PSC-02',415,460,'funda')]
ALTS  = [('BAL-02-AC',270), ('PSA-05',513)]

# cobertura da curva: TGFPRO.LARGURA/ALTURA/ESPESSURA (cm), 2.742 de 3.079 PAs
# ativos preenchidos; 1.273 SKUs de marca propria, R$ 83,8 M em 12 M ate 24/08/2026
COB_LADO   = {200:56.8, 300:90.5, 460:99.9}
COB_FRENTE = {200:18.1, 300:67.0, 460:96.1}
COB_ALT    = {270:79.1, 513:98.2}

ext_comp = lambda B, N: 2*NOX + (N-1)*NOXC + N*(B-CONSOME)
ext_prof = lambda B:    B + 2*(NOY-ENC)
passo_v  = lambda B, k=1: (B-CONSOME) + k*NOZ

def altura(pilha, coroa=None, k=1):
    """pilha = lista de ripas verticais de baixo para cima, uma por baia."""
    ripas = list(pilha) + ([coroa] if coroa else [])
    nos = len(ripas) + 1
    return PE + nos*k*NOZ + sum(r - CONSOME for r in ripas)

D = pathlib.Path(__file__).resolve().parent.parent / 'dados'

def wr(nome, cab, linhas):
    with open(D/nome, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(cab); w.writerows(linhas)
    print(f'{nome}: {len(linhas)} linhas')

# ---------------------------------------------------------------- 22 modelo
wr('22-mob-cota-modelo.csv',
   ['grandeza','valor_mm','origem','o_que_significa'],
   [['encaixe (ENC)', ENC, 'face +Y da peca L, mediana de 1.666 raios',
     'quanto a ripa entra dentro do no, dos dois lados'],
    ['trizeta no comprimento (NOX)', NOX, 'malha da trizeta',
     f'sobra {NOX-ENC:.2f} mm por extremidade: externo = ripa + {2*(NOX-ENC):.2f}'],
    ['cruzeta no comprimento (NOXC)', NOXC, 'malha da cruzeta',
     f'no do meio do vao: consome {CONSOME:.1f} e soma {NOXC-CONSOME:.2f} de passo'],
    ['peca L no eixo de trabalho (NOL)', NOL, 'malha da peca L (bbox 21,92 x 83,23 x 73,08)',
     f'no de topo: passa {NOL-NOX:.2f} mm por lado alem da trizeta'],
    ['no na profundidade (NOY)', NOY, 'malha da trizeta',
     f'sobra {NOY-ENC:.2f} mm por extremidade: externo = ripa + {2*(NOY-ENC):.2f}'],
    ['no no vertical (NOZ)', NOZ, 'malha da trizeta E da peca L',
     'a peca L tem o mesmo passo vertical da trizeta — e por isso serve de no de topo'],
    ['pe exposto (PE)', PE, 'BPE-01-AC de 60 mm menos o encaixe',
     'soma uma vez na altura total'],
    ['consumido por ripa', CONSOME, '2 x encaixe',
     'o que os dois nos comem do comprimento nominal da ripa'],
    ['razao minima do painel', RAZ_MIN, 'regra de proporcao',
     'abaixo disso o painel e quadrado, ou mais fundo que longo'],
    ['razao maxima do painel', RAZ_MAX, 'regra de proporcao',
     'acima disso o painel e tira estreita e comprida'],
    ['FORMULA comprimento', 0, f'2*{NOX} + (N-1)*{NOXC} + N*(ripa - {CONSOME:.1f})',
     'N = numero de vaos na corrida'],
    ['FORMULA profundidade', 0, f'ripa + 2*{NOY-ENC:.2f}', 'uma ripa de largura por linha de no'],
    ['FORMULA altura', 0, f'{PE:.1f} + n_nos*{NOZ} + SOMA(ripa_i - {CONSOME:.1f})',
     'uma ripa por baia; n_nos = prateleiras + 1 se houver coroa'],
    ['FORMULA coroa', 0, f'a coroa acrescenta (ripa - {CONSOME:.1f}) + {NOZ}',
     f'= ripa - {CONSOME-NOZ:.2f} mm de altura, sem somar prateleira'],
    ['FORMULA comprimento da coroa', 0, f'comprimento + 2*{NOL-NOX:.2f}',
     'a coroa passa da estrutura porque a peca L e mais longa nesse eixo que a trizeta']])

# ------------------------------------------------------- 23 grade de paineis
linhas = []
for lref, lb, lpan, apelido in LARGS:
    for cref, cb, cpan in COMPS:
        raz = cpan/lpan
        dentro = RAZ_MIN <= raz <= RAZ_MAX
        if dentro:
            motivo = 'mantido'
        elif raz < RAZ_MIN:
            motivo = 'cortado: quadrado ou mais fundo que longo'
        else:
            motivo = 'cortado: tira estreita e comprida'
        ext = ext_comp(cb, 1)
        linhas.append([f'{lpan}x{cpan}', lpan, cpan, round(raz,2),
                       'SIM' if dentro else 'NAO', motivo, apelido,
                       cref, cb, lref, lb,
                       round(ext,2), round(ext_prof(lb),2),
                       round(cpan-ext,2), round((lpan-lb)/2,2), round(cb-CONSOME,2),
                       COB_LADO[lpan], COB_FRENTE[lpan]])
wr('23-mob-paineis-grade.csv',
   ['painel','largura_mm','comprimento_mm','razao','mantido','motivo','profundidade',
    'ripa_comprimento','ripa_comprimento_mm','ripa_largura','ripa_largura_mm',
    'vao_externo_mm','profundidade_externa_mm','painel_menos_vao_mm',
    'sobressai_por_lado_mm','vao_livre_entre_nos_mm',
    'pct_curva_de_lado','pct_curva_de_frente'], linhas)
print('   mantidos:', sum(1 for l in linhas if l[4] == 'SIM'), 'de', len(linhas))

# -------------------------------------------------------------- 24 corridas
wr('24-mob-cota-corridas.csv',
   ['ripa_comprimento','ripa_mm','painel_mm','passo_por_vao_mm',
    '1_vao','2_vaos','3_vaos','4_vaos','5_vaos','6_vaos'],
   [[cref, cb, cpan, round(cb+NOXC-CONSOME,2)] +
    [round(ext_comp(cb,N)) for N in range(1,7)] for cref, cb, cpan in COMPS])

# -------------------------------------------------------------- 25 alturas
linhas = []
for aref, ab in ALTS:
    for mod, k in (('A',1), ('B',2)):
        for cor in (None, 270, 513):
            row = [aref, ab, mod, 'nenhuma' if not cor else f'ripa {cor}',
                   round(passo_v(ab,k),2), round(COB_ALT[ab],1)]
            row += [round(altura([ab]*(n-1), cor, k)) for n in range(2,9)]
            linhas.append(row)
wr('25-mob-cota-alturas.csv',
   ['ripa_vertical','ripa_mm','modelo_no','coroa','passo_mm','pct_curva_na_baia',
    '2_prat','3_prat','4_prat','5_prat','6_prat','7_prat','8_prat'], linhas)

# ------------------------------------------------ 26 cobertura da curva
wr('26-mob-cobertura-curva.csv',
   ['eixo','opcao_mm','cota_externa_mm','livre_mm','pct_faturamento','orientacao','fonte'],
   [['profundidade', 200, round(ext_prof(200),1), '', COB_LADO[200], 'produto de lado',
     'TGFPRO.LARGURA/ESPESSURA x faturamento 12M marca propria'],
    ['profundidade', 200, round(ext_prof(200),1), '', COB_FRENTE[200], 'produto de frente', 'idem'],
    ['profundidade', 300, round(ext_prof(287),1), '', COB_LADO[300], 'produto de lado', 'idem'],
    ['profundidade', 300, round(ext_prof(287),1), '', COB_FRENTE[300], 'produto de frente', 'idem'],
    ['profundidade', 460, round(ext_prof(415),1), '', COB_LADO[460], 'produto de lado', 'idem'],
    ['profundidade', 460, round(ext_prof(415),1), '', COB_FRENTE[460], 'produto de frente', 'idem'],
    ['altura da baia', 270, '', round(passo_v(270)-PANT,1), COB_ALT[270], 'produto em pe',
     'TGFPRO.ALTURA x faturamento 12M marca propria'],
    ['altura da baia', 513, '', round(passo_v(513)-PANT,1), COB_ALT[513], 'produto em pe', 'idem']])
