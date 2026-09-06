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
AMBIENTE = {
 'POTES':'COZINHA', 'COZINHA':'COZINHA', 'JARRAS':'COZINHA', 'MICRO-ONDAS':'COZINHA',
 'GELADEIRA':'COZINHA', 'POP':'COZINHA', 'TECA':'COZINHA',
 'ORGANIZACAO':'ORGANIZACAO',
 'BANHEIRO':'BANHO E LAVANDERIA', 'LIXEIRAS':'BANHO E LAVANDERIA',
 'LIMPEZA':'BANHO E LAVANDERIA',
 'FRASQUEIRAS':'IMPULSO', 'INFANTIL':'IMPULSO', 'REALCE':'IMPULSO', 'DECOR':'IMPULSO',
 'NITRON-MOB':'NITRON-MOB',
}

# --------------------------------------------------------- os modulos
MODULOS = [
 (1,'Paredao sul',            13290,1,[270]*7,               372,'COZINHA'),
 (2,'Paredao norte',           6054,1,[270]*7,               285,'ORGANIZACAO'),
 (3,'Paredao do fundo',        6788,1,[513,270,270,270,270,270],500,'BANHO E LAVANDERIA'),
 (4,'Parede de entrada',       6548,1,[270,270,270],          285,'NITRON-MOB'),
 (10,'Gondola A, face corredor 1',4328,1,[270]*5,             500,'COZINHA'),
 (11,'Gondola A, face corredor 2',4328,1,[270]*5,             500,'COZINHA'),
 (12,'Gondola B, face corredor 2',4328,1,[270]*5,             500,'ORGANIZACAO'),
 (13,'Gondola B, face corredor 3',4328,1,[270]*5,             500,'ORGANIZACAO'),
 (20,'Ponta 1',                 892,1,[270]*5,                372,'COZINHA'),
 (21,'Ponta 2',                 892,1,[270]*5,                372,'COZINHA'),
 (22,'Ponta 3',                 892,1,[270]*5,                372,'ORGANIZACAO'),
 (23,'Ponta 4',                 892,1,[270]*5,                372,'ORGANIZACAO'),
 (40,'Ilha 1',                 1867,2,[270,270,270],          500,'COZINHA'),
 (41,'Ilha 2',                 1867,2,[270,270,270],          500,'ORGANIZACAO'),
 (50,'Corredor de checkout A', 1762,2,[270,270,270],          372,'IMPULSO'),
 (51,'Corredor de checkout B', 1762,2,[270,270,270],          372,'IMPULSO'),
 (30,'Modulo caixa-pilar',      457,1,[270,270,270],          372,'IMPULSO'),
 (31,'Torre de servico',        357,1,[270]*4,                285,'IMPULSO'),
]
