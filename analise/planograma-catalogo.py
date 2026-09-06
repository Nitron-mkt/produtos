#!/usr/bin/env python3
"""Planograma do showroom restrito as referencias do catalogo oficial.

Universo: as 633 referencias impressas em CatalogoNitron.pdf (112 paginas),
extraidas por coordenada do PDF -- nao o catalogo ativo inteiro do ERP.

Entradas
  dados/36-catalogo-pdf-refs.csv       ref, pagina, categoria, nome, COM/LAR/ALT, litragem
  dados/37-catalogo-pdf-x-erp.csv      cruzamento com TGFPRO (codprod, ativo, cotas do ERP)
  dados/38-catalogo-pdf-faturamento.csv faturamento 12 M por referencia

Saidas
  dados/39-catalogo-planograma-skus.csv   uma linha por referencia, com ambiente e frente
  dados/40-catalogo-planograma-ambientes.csv
  dados/41-catalogo-planograma-modulos.csv
"""
import csv, pathlib, collections
RAIZ = pathlib.Path(__file__).resolve().parent.parent
D = RAIZ/'dados'

# ---------------------------------------------------------------- geometria
NOZ, PEX, PANT, CONSOME = 73.08, 19.4, 15, 81.2
VAO_270, VAO_513 = 261.88 - 15, 504.88 - 15   # altura livre util de cada baia

def prateleiras(pilha):
    z, out = PEX, []
    for i in range(len(pilha)+1):
        out.append(round(z + NOZ + PANT/2))
        if i < len(pilha): z = z + NOZ + (pilha[i]-CONSOME)
    return out

def zona(h):
    if h <= 800:  return 'chao'
    if h <= 1400: return 'maos'
    if h <= 1700: return 'olhos'
    return 'topo'

# ------------------------------------------------ categoria -> ambiente
# Frasqueiras nao e impulso: o SKU numero 1 do catalogo inteiro e a Frasqueira
# Medicamentos 2,8L (R$ 1,67 M, 1.162 clientes) e a linha cresce 8,6%. Ganha
# parede propria. DECOR e gadget de cozinha (hamburgueira, churros) -- vai para
# a cozinha, nao para o caixa.
AMBIENTE = {
 'POTES':'COZINHA', 'COZINHA':'COZINHA', 'JARRAS':'COZINHA', 'MICRO-ONDAS':'COZINHA',
 'GELADEIRA':'COZINHA', 'POP':'COZINHA', 'TECA':'COZINHA', 'DECOR':'COZINHA',
 'ORGANIZACAO':'ORGANIZACAO',
 'BANHEIRO':'BANHO E LAVANDERIA', 'LIXEIRAS':'BANHO E LAVANDERIA',
 'LIMPEZA':'BANHO E LAVANDERIA',
 'FRASQUEIRAS':'FRASQUEIRAS E INFANTIL', 'INFANTIL':'FRASQUEIRAS E INFANTIL',
 'REALCE':'FRASQUEIRAS E INFANTIL',
 'NITRON-MOB':'NITRON-MOB',
}

# --------------------------------------------------------- os modulos
# O catalogo cabe inteiro no PERIMETRO. As quatro paredes somam 32,68 m de
# corrida; com a pilha abaixo dao 24 prateleiras e 202,1 m de frente, contra
# 97,4 m de demanda a 1 facing. O miolo do showroom -- gondolas, pontas, ilhas
# e o corredor de checkout -- nao e preciso para EXPOR o catalogo, e por isso
# entra aqui como piso de demonstracao, nao como prateleira de catalogo.
#
# Profundidade: a gondola AFINA com a altura (norma de varejo: base 300-500 mm,
# superior 200-400). Sem isso a parede norte, rasa, rejeita 47 blocos.
def profundidade(h):
    if h <= 800:  return 500      # painel 460 · lixeira, cesto, caixa grande
    if h <= 1400: return 372      # painel 300 · pote, organizador
    return 285                    # painel 200 · produto de mao

PAREDES = [
 # id, nome, corrida_mm, faces, pilha, ambiente
 (1,'Paredao sul',        13290,1,[270]*6,             'COZINHA'),
 (2,'Paredao norte',       6054,1,[270]*6,             'ORGANIZACAO'),
 (3,'Paredao do fundo',    6788,1,[513,513,270,270],   'BANHO E LAVANDERIA'),
 # a pilha 513+270+270+270 poe a ultima face em 1.390 mm e perde a zona dos
# olhos por 10 mm. Com 513+513+270+270 ela sobe para 1.633.
 (4,'Parede de entrada',   6548,1,[513,513,270,270],   'FRASQUEIRAS E INFANTIL'),
]
# o miolo, mantido no salao para demonstrar o PDV -- fora do planograma de catalogo
MIOLO = [
 (10,'Gondola A, face corredor 1',4328,1,[513,270,270],'demonstracao'),
 (11,'Gondola A, face corredor 2',4328,1,[513,270,270],'demonstracao'),
 (12,'Gondola B, face corredor 2',4328,1,[513,270,270],'demonstracao'),
 (13,'Gondola B, face corredor 3',4328,1,[513,270,270],'demonstracao'),
 (20,'Ponta 1',892,1,[513,270,270],'demonstracao'),
 (21,'Ponta 2',892,1,[513,270,270],'demonstracao'),
 (22,'Ponta 3',892,1,[513,270,270],'demonstracao'),
 (23,'Ponta 4',892,1,[513,270,270],'demonstracao'),
 (40,'Ilha 1',1867,2,[513,270],'demonstracao'),
 (41,'Ilha 2',1867,2,[513,270],'demonstracao'),
 (50,'Corredor de checkout A',1762,2,[513,270],'demonstracao'),
 (51,'Corredor de checkout B',1762,2,[513,270],'demonstracao'),
 (30,'Modulo caixa-pilar',457,1,[513,270,270],'demonstracao'),
 (31,'Torre de servico',357,1,[513,270,270],'demonstracao'),
]
MODULOS = PAREDES

# ---------------------------------------------------------------- cotas
# No TGFPRO as cotas estao em centimetros e ESPESSURA guarda o COMPRIMENTO:
# conferido em 368 pares contra o PDF, 299 batem dentro de 1 cm (81%).
# Ordem de confianca: ERP limpo > cota impressa no catalogo > sem cota.
SUJA = 1000.0   # acima disso e serial de data do Excel, nao centimetro

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return 0.0

def cotas(erp, pdf):
    """(comprimento, largura, altura) em mm, e a fonte."""
    if erp:
        c, l, a = num(erp['espessura']), num(erp['largura']), num(erp['altura'])
        if min(c, l, a) > 0 and max(c, l, a) < SUJA:
            return c*10, l*10, a*10, 'erp'
    if pdf and pdf['com_cm'] and pdf['lar_cm'] and pdf['alt_cm']:
        return (float(pdf['com_cm'])*10, float(pdf['lar_cm'])*10,
                float(pdf['alt_cm'])*10, 'catalogo')
    return None, None, None, 'sem cota'

# ---------------------------------------------------------------- entrada
def ler():
    pdf = {r['referencia']: r for r in csv.DictReader(open(D/'36-catalogo-pdf-refs.csv'))}
    erp = {r['referencia']: r for r in
           csv.DictReader(open(D/'37-catalogo-pdf-x-erp.csv'), delimiter=';')
           if r['achou'] == 'S'}
    fat = {r['referencia']: r for r in
           csv.DictReader(open(D/'38-catalogo-pdf-faturamento.csv'), delimiter=';')}
    skus = []
    for ref, p in sorted(pdf.items()):
        e = erp.get(ref)
        if not e:
            continue                      # as 4 lidas errado do PDF
        c, l, a, fonte = cotas(e, p)
        cat = p['categoria_catalogo']
        # o titulo do PDF as vezes cai numa linha de continuacao ("com 3 Divisorias"):
        # nesses casos a descricao do ERP e mais confiavel.
        nome = p['nome_catalogo']
        if not nome or len(nome) < 8 or nome[0].islower():
            nome = e['descrprod'].title()
        skus.append(dict(
            ref=ref, codprod=e['codprod'], nome=nome,
            pagina=int(p['pagina']), categoria=cat, ambiente=AMBIENTE[cat],
            linha_erp=e['nomegrupo'], comp=c, larg=l, alt=a, fonte=fonte,
            fat=num(fat.get(ref, {}).get('faturamento_12m')),
            clientes=int(num(fat.get(ref, {}).get('qtd_clientes'))),
        ))
    return skus

# ------------------------------------------------------- classificacao
PROFS = (285, 372, 500)

def classificar(s):
    """Onde o produto pode ir: prateleira, e com que profundidade minima."""
    if s['comp'] is None:
        return 'sem cota', None, None
    frente, fundo = min(s['comp'], s['larg']), max(s['comp'], s['larg'])
    if fundo > 500:
        return 'fora de gondola', frente, None
    prof = next(p for p in PROFS if fundo <= p)
    return 'gondola', frente, prof

def baia(alt):
    """Menor baia que aceita a altura do produto (mm de ripa)."""
    if alt is None:      return None
    if alt <= VAO_270:   return 270
    if alt <= VAO_513:   return 513
    return None

# ---------------------------------------------------------------- oferta
def oferta(mods=None):
    mods = MODULOS if mods is None else mods
    linhas, por_amb, por_zona, por_prof = [], collections.Counter(), collections.Counter(), collections.Counter()
    for mid, nome, L, faces, pilha, amb in mods:
        for k, h in enumerate(prateleiras(pilha)):
            m = L/1000*faces
            prof = profundidade(h)
            linhas.append([mid, nome, k+1, h, zona(h), prof, faces, round(m,2), amb])
            por_amb[amb] += m; por_zona[zona(h)] += m; por_prof[prof] += m
    return linhas, por_amb, por_zona, por_prof

# --------------------------------------------------------------- alocacao
# Regra, na ordem: (1) o que nao cabe na baia de 270 desce para a baia alta;
# (2) o resto sobe por faturamento -- olhos primeiro, depois maos, depois chao;
# (3) as cores de uma mesma referencia-base ficam juntas, sempre.
ORDEM_ZONA = ['olhos', 'maos', 'chao', 'topo']

def alocar(skus, linhas):
    prat = collections.defaultdict(list)          # ambiente -> prateleiras livres
    for mid, nome, k, h, z, prof, faces, mts, amb in linhas:
        prat[amb].append(dict(mid=mid, modulo=nome, n=k, h=h, zona=z, prof=prof,
                              livre=mts*1000, cap=mts*1000))
    for amb in prat:
        prat[amb].sort(key=lambda p: (ORDEM_ZONA.index(p['zona']), -p['h']))

    blocos = collections.defaultdict(list)        # (ambiente, ref-base) -> skus
    for s in skus:
        if s['classe'] == 'gondola':
            blocos[(s['ambiente'], s['ref'].split('.')[0])].append(s)
    ordem = sorted(blocos.items(), key=lambda kv: -sum(x['fat'] for x in kv[1]))

    fora = []
    for (amb, base), bl in ordem:
        larg = sum(x['frente'] for x in bl)
        alta = any(x['baia'] != 270 for x in bl)          # bloco volumoso
        alvo = None
        for p in prat[amb]:
            if p['livre'] < larg: continue
            if max(x['prof'] for x in bl) > p['prof']: continue
            if alta and p['zona'] != 'chao': continue     # baia alta so no chao
            alvo = p; break
        if alvo is None:
            fora.append((amb, base, larg)); continue
        alvo['livre'] -= larg
        for x in bl:
            x['modulo'], x['prat_n'], x['prat_h'], x['prat_zona'] = \
                alvo['modulo'], alvo['n'], alvo['h'], alvo['zona']
    return prat, fora

# ------------------------------------------------------------------ main
if __name__ == '__main__':
    skus = ler()
    for s in skus:
        s['classe'], s['frente'], s['prof'] = classificar(s)
        s['baia'] = baia(s['alt'])

    for s in skus:
        if s['ambiente'] == 'NITRON-MOB':
            s['classe'] = 'montado no chao'   # movel: expoe montado, nao em prateleira
    gond = [s for s in skus if s['classe'] == 'gondola']
    m1 = sum(s['frente'] for s in gond)/1000
    print('CATALOGO OFICIAL — %d referencias lidas do PDF, %d confirmadas no ERP' % (633, len(skus)))
    cl = collections.Counter(s['classe'] for s in skus)
    for k, v in cl.most_common():
        mm = sum(s['frente'] for s in skus if s['classe']==k and s['frente'])/1000
        print('  %-16s %4d SKUs · %6.1f m' % (k, v, mm))
    print('  fonte da cota:', dict(collections.Counter(s['fonte'] for s in skus)))
    print('\nDEMANDA A 1 FACING: %.1f m · faturamento R$ %.2f M' %
          (m1, sum(s['fat'] for s in skus)/1e6))

    linhas, o_amb, o_zona, o_prof = oferta()
    with open(D/'41-catalogo-planograma-modulos.csv','w',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['modulo_id','modulo','prateleira','altura_face_mm','zona',
                    'profundidade_mm','faces','metros_lineares','ambiente'])
        w.writerows(linhas)
    print('OFERTA TOTAL: %.1f m' % sum(o_amb.values()))
    print('  por zona:', {k: round(v,1) for k,v in o_zona.items()})

    with open(D/'39-catalogo-planograma-skus.csv','w',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['referencia','codprod','nome','pagina','categoria_catalogo','ambiente',
                    'linha_erp','comprimento_mm','largura_mm','altura_mm','fonte_cota',
                    'classe','frente_mm','profundidade_min_mm','baia_mm',
                    'faturamento_12m','clientes'])
        for s in sorted(skus, key=lambda s: (-s['fat'], s['ref'])):
            w.writerow([s['ref'],s['codprod'],s['nome'],s['pagina'],s['categoria'],s['ambiente'],
                        s['linha_erp'],s['comp'],s['larg'],s['alt'],s['fonte'],s['classe'],
                        s['frente'] and round(s['frente']),s['prof'],s['baia'],
                        round(s['fat'],2),s['clientes']])
    lm,_,_,_ = oferta(MIOLO)
    print('  miolo (fora do planograma de catalogo): %d prateleiras · %.1f m'
          % (len(lm), sum(r[7] for r in lm)))
    print('\nAMBIENTES (demanda a 1 facing x oferta)')
    dem = collections.Counter(); nsk = collections.Counter(); fatb = collections.Counter()
    for s in gond:
        dem[s['ambiente']] += s['frente']/1000
        nsk[s['ambiente']] += 1; fatb[s['ambiente']] += s['fat']
    tot=[0,0,0]
    for amb in sorted(dem, key=lambda a: -fatb[a]):
        print('  %-19s %3d SKUs · demanda %5.1f m · oferta %5.1f m · x%.1f · R$ %5.2f M'
              % (amb, nsk[amb], dem[amb], o_amb.get(amb,0),
                 o_amb.get(amb,0)/dem[amb] if dem[amb] else 0, fatb[amb]/1e6))
        tot[0]+=dem[amb]; tot[1]+=o_amb.get(amb,0); tot[2]+=fatb[amb]
    print('  %-19s %3d SKUs · demanda %5.1f m · oferta %5.1f m · x%.1f · R$ %5.2f M'
          % ('TOTAL', len(gond), tot[0], tot[1], tot[1]/tot[0], tot[2]/1e6))

    prat, fora = alocar(skus, linhas)
    aloc = [s for s in gond if s.get('modulo')]
    print('\nALOCACAO: %d de %d SKUs colocados · %d blocos sem lugar' %
          (len(aloc), len(gond), len(fora)))
    zf = collections.Counter(); zn = collections.Counter()
    for s in aloc:
        zf[s['prat_zona']] += s['fat']; zn[s['prat_zona']] += 1
    tf = sum(zf.values())
    for z in ORDEM_ZONA:
        if zn[z]:
            print('  %-6s %3d SKUs · R$ %5.2f M · %4.1f%% do faturamento'
                  % (z, zn[z], zf[z]/1e6, 100*zf[z]/tf))
    ocup = [p for a in prat for p in prat[a]]
    usadas = [p for p in ocup if p['livre'] < p['cap']]
    print('  prateleiras com produto: %d de %d · ocupacao media %.0f%%'
          % (len(usadas), len(ocup),
             100*sum(1-p['livre']/p['cap'] for p in usadas)/max(len(usadas),1)))
    with open(D/'42-catalogo-planograma-alocacao.csv','w',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['referencia','nome','ambiente','categoria_catalogo','modulo','prateleira',
                    'altura_face_mm','zona','frente_mm','baia_mm','faturamento_12m','clientes'])
        for s in sorted(aloc, key=lambda s: (s['modulo'], s['prat_n'], -s['fat'])):
            w.writerow([s['ref'],s['nome'],s['ambiente'],s['categoria'],s['modulo'],s['prat_n'],
                        s['prat_h'],s['prat_zona'],round(s['frente']),s['baia'],
                        round(s['fat'],2),s['clientes']])
