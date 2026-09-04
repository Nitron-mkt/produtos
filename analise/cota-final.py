#!/usr/bin/env python3
"""Cota externa real do modulo Nitron Mob.

A ripa entra dentro do no; a medida final NAO e a soma das ripas. Este script
fecha as tres contas a partir das grandezas medidas nas malhas STL das pecas de
linha e cruza o resultado com a lista de paineis e ripas fixadas pelo usuario.

Gera:
  dados/22-mob-cota-modelo.csv     as constantes e as tres formulas
  dados/23-mob-cota-12-paineis.csv as 12 combinacoes painel x ripa
  dados/24-mob-cota-corridas.csv   comprimento externo por numero de vaos
  dados/25-mob-cota-alturas.csv    altura externa por numero de prateleiras
"""
import csv, pathlib

# grandezas medidas nas malhas (fechadas, 0 arestas nao-manifold)
ENC  = 40.60    # profundidade do encaixe: quanto a ripa entra no no
NOX  = 61.61    # extensao da trizeta no eixo do COMPRIMENTO
NOXC = 101.30   # extensao da CRUZETA no eixo do comprimento
NOY  = 83.23    # extensao do no no eixo da PROFUNDIDADE
NOZ  = 73.08    # extensao do no no eixo VERTICAL
PEX  = 60 - ENC # pe BPE-01-AC de 60 mm menos o encaixe = trecho exposto
CONSOME = 2*ENC # 81,20 mm que os dois nos comem de cada ripa

COMPS = [('PSC-01',315,360), ('PSC-02',415,450), ('PSC-03',595,634), ('PSC-04',717,754)]
LARGS = [('BLA-01-AC',200,200,'rasa'), ('BLA-03-AC',287,300,'media'), ('PSC-02',415,460,'funda')]
ALTS  = [('BAL-02-AC',270), ('PSA-05',513)]

ext_comp = lambda B, N: 2*NOX + (N-1)*NOXC + N*(B-CONSOME)
ext_prof = lambda B:    B + 2*(NOY-ENC)
ext_alt  = lambda B, n, k=1: n*k*NOZ + (n-1)*(B-CONSOME) + PEX

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
    ['no no comprimento (NOX)', NOX, 'malha da trizeta',
     f'sobra {NOX-ENC:.2f} mm por extremidade: externo = ripa + {2*(NOX-ENC):.2f}'],
    ['cruzeta no comprimento (NOXC)', NOXC, 'malha da cruzeta',
     f'no do meio do vao: consome {CONSOME:.1f} e soma {NOXC-CONSOME:.2f} de passo'],
    ['no na profundidade (NOY)', NOY, 'malha da trizeta',
     f'sobra {NOY-ENC:.2f} mm por extremidade: externo = ripa + {2*(NOY-ENC):.2f}'],
    ['no no vertical (NOZ)', NOZ, 'malha da trizeta', 'passo do no no eixo Z'],
    ['pe exposto (PEX)', PEX, 'BPE-01-AC de 60 mm menos o encaixe',
     'soma uma vez na altura total'],
    ['consumido por ripa', CONSOME, '2 x encaixe',
     'o que os dois nos comem do comprimento nominal da ripa'],
    ['FORMULA comprimento', 0, f'2*{NOX} + (N-1)*{NOXC} + N*(ripa - {CONSOME:.1f})',
     'N = numero de vaos na corrida'],
    ['FORMULA profundidade', 0, f'ripa + 2*{NOY-ENC:.2f}', 'uma ripa de largura por linha de no'],
    ['FORMULA altura modelo A', 0, f'n*{NOZ} + (n-1)*(ripa - {CONSOME:.1f}) + {PEX:.1f}',
     'n = prateleiras; um no por nivel'],
    ['FORMULA altura modelo B', 0, f'n*2*{NOZ} + (n-1)*(ripa - {CONSOME:.1f}) + {PEX:.1f}',
     'par de trizetas espelhadas por nivel — a ler confirmar no showroom']])

# ------------------------------------------------------------ 23 12 paineis
linhas = []
for lref, lb, lpan, apelido in LARGS:
    for cref, cb, cpan in COMPS:
        ext = ext_comp(cb, 1)
        linhas.append([f'{lpan}x{cpan}', lpan, cpan, apelido,
                       cref, cb, lref, lb,
                       round(ext,2), round(ext_prof(lb),2),
                       round(cpan-ext,2), round((lpan-lb)/2,2),
                       round(cb-CONSOME,2)])
wr('23-mob-cota-12-paineis.csv',
   ['painel','painel_largura_mm','painel_comprimento_mm','profundidade',
    'ripa_comprimento','ripa_comprimento_mm','ripa_largura','ripa_largura_mm',
    'vao_externo_mm','profundidade_externa_mm',
    'painel_menos_vao_mm','sobressai_por_lado_mm','vao_livre_entre_nos_mm'], linhas)

# -------------------------------------------------------------- 24 corridas
linhas = [[cref, cb, cpan, round(cb+NOXC-CONSOME,2)] +
          [round(ext_comp(cb,N)) for N in range(1,7)]
          for cref, cb, cpan in COMPS]
wr('24-mob-cota-corridas.csv',
   ['ripa_comprimento','ripa_mm','painel_mm','passo_por_vao_mm',
    '1_vao','2_vaos','3_vaos','4_vaos','5_vaos','6_vaos'], linhas)

# -------------------------------------------------------------- 25 alturas
linhas = []
for aref, ab in ALTS:
    for mod, k in (('A',1), ('B',2)):
        linhas.append([aref, ab, mod, round((ab-CONSOME)+k*NOZ,2)] +
                       [round(ext_alt(ab,n,k)) for n in range(2,9)])
wr('25-mob-cota-alturas.csv',
   ['ripa_vertical','ripa_mm','modelo_no','passo_mm',
    '2_prat','3_prat','4_prat','5_prat','6_prat','7_prat','8_prat'], linhas)
