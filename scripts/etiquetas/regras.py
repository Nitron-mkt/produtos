# -*- coding: utf-8 -*-
"""Tabelas de regra do preenchimento automatico da matriz de etiquetas.

Este ficheiro e o unico ponto a editar quando o Marketing quiser mudar
criterio. Depois de editar, correr de novo:

    python3 scripts/etiquetas/gerar_matriz.py

Tudo o que esta aqui e PROPOSTA. Nada aqui e informacao vinda do Sankhya.
"""

# ---------------------------------------------------------------------------
# 1. LAYOUTS  (separador Layouts)
#    largura_mm / altura_mm = bobina pre-impressa encomendada a grafica.
#    janela_* = area branca central reservada para a impressao interna.
#    corpo_pt / linhas = tipografia do nome no componente, serve para
#    calcular MAX CARAC NOME. Ver Regras_Auto no ficheiro gerado.
# ---------------------------------------------------------------------------
LAYOUTS = {
    1: dict(largura_mm=60,  altura_mm=40, janela_larg_mm=50, janela_alt_mm=24,
            corpo_pt=8,  linhas=1, teto_editorial=28,
            max_selos=3, max_aplic=3, tem_qr="S"),
    2: dict(largura_mm=80,  altura_mm=50, janela_larg_mm=70, janela_alt_mm=28,
            corpo_pt=9,  linhas=1, teto_editorial=34,
            max_selos=4, max_aplic=4, tem_qr="S"),
    3: dict(largura_mm=100, altura_mm=70, janela_larg_mm=88, janela_alt_mm=36,
            corpo_pt=11, linhas=2, teto_editorial=40,
            max_selos=6, max_aplic=6, tem_qr="S"),
    4: dict(largura_mm=120, altura_mm=80, janela_larg_mm=106, janela_alt_mm=40,
            corpo_pt=12, linhas=2, teto_editorial=44,
            max_selos=6, max_aplic=8, tem_qr="S"),
}

# Largura media de caractere em Arial = FATOR x corpo. 0.52 e o valor medido
# para texto em caixa mista. Margem de seguranca de 2 mm por lado na janela.
FATOR_CARACTERE = 0.52
MARGEM_JANELA_MM = 2.0
MM_POR_PONTO = 0.3528


def cabe_fisicamente(layout):
    """Quantos caracteres cabem na janela branca, so por geometria."""
    cfg = LAYOUTS[layout]
    util = cfg["janela_larg_mm"] - 2 * MARGEM_JANELA_MM
    larg_car = cfg["corpo_pt"] * MM_POR_PONTO * FATOR_CARACTERE
    return int(util / larg_car) * cfg["linhas"]


def max_caracteres(layout):
    """MAX CARAC NOME = o menor entre o que cabe e o teto editorial.

    O teto editorial existe porque um nome que cabe nem sempre le bem na
    gondola. Acima dele o nome deixa de funcionar como identificacao rapida,
    mesmo que a tipografia aguente.
    """
    return min(cabe_fisicamente(layout), LAYOUTS[layout]["teto_editorial"])


# Regra de atribuicao de layout. A precedencia e de cima para baixo.
# Categorias que sao organizador ou maleta vao para o layout 4 independente
# da capacidade, porque a face de aplicacao da etiqueta e grande.
CATEGORIA_LAYOUT_FIXO = {
    "Organização": 4,
    "Teca": 4,
    "Frasqueiras": 4,
    "Nitron-Mob": 4,
    "Lixeiras": 3,
}

# Faixas de capacidade em ml (limite superior inclusive) -> layout
FAIXAS_CAPACIDADE = [(400, 1), (1000, 2), (float("inf"), 3)]

# Fallback sem capacidade: area da face (LARG x ALT em cm2) -> layout
FAIXAS_AREA_FACE = [(100, 1), (250, 2), (float("inf"), 3)]


# ---------------------------------------------------------------------------
# 2. CATEGORIAS  (normalizacao das 20 grafias do ficheiro de origem)
# ---------------------------------------------------------------------------
CATEGORIA_CANONICA = {
    "teca": "Teca",
    "Microondas": "Micro-ondas",
}


# ---------------------------------------------------------------------------
# 3. SELOS por categoria  (proposta - exige validacao de Engenharia/Qualidade)
#    BRA aplica-se a todos, ver SELOS_UNIVERSAIS.
#    A ordem e a prioridade: quando o layout nao chega para todos, ficam os
#    primeiros da lista.
# ---------------------------------------------------------------------------
SELOS_UNIVERSAIS = ["BRA"]

SELOS_POR_CATEGORIA = {
    "Potes":             ["BPA", "ATX", "LAV", "EMP"],
    "POP":               ["BPA", "ATX", "LAV", "EMP"],
    "Coloratto":         ["BPA", "ATX", "LAV", "EMP"],
    "Realce":            ["BPA", "ATX", "LAV"],
    "Micro-ondas":       ["BPA", "ATX", "MIC", "LAV"],
    "Geladeira":         ["BPA", "ATX", "FRZ", "LAV", "EMP"],
    "Cozinha":           ["BPA", "ATX", "LAV"],
    "Jarras":            ["BPA", "ATX", "LAV"],
    "Infantil":          ["BPA", "ATX", "LAV"],
    "Lixeiras":          ["HIG", "FCL", "RCL"],
    "Organização":       ["EMP", "FCL", "RCL"],
    "Banheiro":          ["FCL", "HIG", "RCL"],
    "Limpeza":           ["ATX", "FCL", "RCL"],
    "Teca":              ["EMP", "FCL"],
    "Frasqueiras":       ["FCL", "EMP"],
    "Nitron-Mob":        ["FCL", "RCL"],
    "Decor-Chef":        ["ATX", "LAV", "FCL"],
    "Decor-Confeitaria": ["ATX", "LAV", "FCL"],
}

# Selos deduzidos do texto (nome ou descricao). Vencem a proposta por
# categoria: sao evidencia escrita, nao inferencia.
SELOS_POR_PALAVRA = [
    (r"micro-?ondas",                     "MIC"),
    (r"freezer|congelador|congelamento",  "FRZ"),
    (r"hermétic|hermetic|vedaç|vedac|com travas?\b", "HER"),
    (r"válvula|valvula",                  "VLV"),
    (r"empilh",                           "EMP"),
    (r"pedal",                            "PED"),
    (r"basculante",                       "TBA"),
    (r"reciclad",                         "REC"),
    (r"reciclá|recicla",                  "RCL"),
    (r"lava-?louç|lavável na máquina",    "LAV"),
    (r"atóxic|atoxic",                    "ATX"),
    (r"sem bpa|livre de bpa",             "BPA"),
    (r"higiên|higien",                    "HIG"),
    (r"fácil de limpar|facil de limpar",  "FCL"),
]

# Selo de cor: aplicado quando o SKU e transparente.
SELO_TRANSPARENTE = "TRP"

# Prioridade global de selos quando ha corte pelo MAX SELOS do layout.
# BRA e igual nos 635 SKUs: o mais barato e imprimi-lo na arte pre-impressa
# da bobina e libertar aqui um lugar. Enquanto isso nao acontecer, fica a
# frente no corte, porque origem e argumento de venda.
PRIORIDADE_SELOS = ["BPA", "ATX", "BRA", "MIC", "FRZ", "HER", "VLV", "LAV",
                    "EMP", "PED", "TBA", "HIG", "FCL", "TRP", "REC", "RCL"]


# ---------------------------------------------------------------------------
# 4. APLICACOES por categoria  (ordem = ordem de impressao = prioridade)
# ---------------------------------------------------------------------------
APLICACOES_POR_CATEGORIA = {
    "Potes":             ["MANT", "GRAO", "CAFE", "ACUC", "FARI", "MASS", "BISC", "TEMP"],
    "POP":               ["MANT", "GRAO", "CAFE", "ACUC", "FARI", "MASS"],
    "Coloratto":         ["SOBR", "MANT", "FRIO", "MASS"],
    "Realce":            ["BEBI"],
    "Jarras":            ["BEBI", "COZI"],
    "Micro-ondas":       ["SOBR", "FRIO", "COZI"],
    "Geladeira":         ["FRIO", "SOBR", "MANT"],
    "Cozinha":           ["COZI", "MANT", "TEMP"],
    "Infantil":          ["BEBI", "BRIN"],
    "Lixeiras":          ["LIXO", "COZI", "BANH"],
    "Organização":       ["PECA", "FERR", "ESCR", "BRIN", "DOCU", "ROUP"],
    "Banheiro":          ["BANH", "HIGI", "COSM"],
    "Limpeza":           ["LIMP", "ROUP", "BANH"],
    "Teca":              ["ROUP", "BRIN", "DOCU", "DECO"],
    "Frasqueiras":       ["MEDI", "COSM", "MAQU", "HIGI"],
    "Nitron-Mob":        ["DECO", "ROUP", "DOCU"],
    "Decor-Chef":        ["COZI", "MANT"],
    "Decor-Confeitaria": ["CONF", "COZI"],
}

# Aplicacoes deduzidas do texto. Entram a frente das da categoria.
APLICACOES_POR_PALAVRA = [
    (r"sal grosso|açúcar|acucar|açucar",  "ACUC"),
    (r"farinha",                          "FARI"),
    (r"café|cafe(?!ter)",                 "CAFE"),
    (r"arroz|feijão|feijao|grão|grao",    "GRAO"),
    (r"tempero|condiment",                "TEMP"),
    (r"biscoit|bolacha",                  "BISC"),
    (r"massa|macarr",                     "MASS"),
    (r"marmita|sobra",                     "SOBR"),
    (r"medicament|farmác|farmac",         "MEDI"),
    (r"ferrament",                        "FERR"),
    (r"parafus|prego",                    "PREG"),
    (r"costura|linha de costura",         "COST"),
    (r"artesanat",                        "ARTE"),
    (r"brinquedo",                        "BRIN"),
    (r"ração|racao|pet",                  "PET"),
    (r"sabão|sabao|detergente",           "LIMP"),
    (r"roupa|cabide|arara",               "ROUP"),
    (r"sapat|calçad|calcad",              "CALC"),
    (r"escov|shampoo|sabonet",            "HIGI"),
    (r"maquiagem|maquilhagem",            "MAQU"),
    (r"jardin|planta|vaso",               "JARD"),
    (r"leite em pó|leite em po",          "MANT"),
    (r"jarra|copo|caneca|suco|espremedor", "BEBI"),
    (r"bolo|confeit|churros|donut|cupcake", "CONF"),
]

# Utensilios e moveis nao guardam mantimentos: a aplicacao deles e o
# ambiente de uso, nao o conteudo. A primeira expressao que casar com o
# inicio do nome substitui toda a lista da categoria.
APLICACOES_OVERRIDE_NOME = [
    (r"^(cabide|arara|cesto de roupas)",                      ["ROUP"]),
    (r"^suporte para botij",                                  ["COZI"]),
    (r"^(prateleira|suporte|cantoneira|kit suporte)",         ["DECO"]),
    (r"^(saboneteira|porta escovas|porta shampoo)",           ["BANH", "HIGI"]),
    (r"^(bico|kit decorador|kit biscoito|kit churros|"
     r"kit donuts|conjunto bico)",                            ["CONF"]),
    (r"^(pá de lixo|pa de lixo|balde|vassoura|tanquinho)",     ["LIMP"]),
    (r"^(tábua|tabua|ralador|cortador|abridor|escorredor|"
     r"hamburgueira|forma de|tampa para|porta talheres|"
     r"descanso)",                                            ["COZI"]),
]

# Aplicacoes que ainda nao existem no catalogo do modelo. O gerador
# acrescenta-as ao separador Cat_Aplicacoes com NOVO = S.
# Cada uma obriga a desenhar um icone novo.
APLICACOES_NOVAS = [
    # cod, pt, en, es
    ("BEBI", "Bebidas",             "Beverages",          "Bebidas"),
    ("CONF", "Confeitaria e bolos", "Baking and Cakes",   "Reposteria y tartas"),
    ("DECO", "Decoracao",           "Home Decor",         "Decoracion"),
]


# ---------------------------------------------------------------------------
# 5. LIMPEZA DE NOME
# ---------------------------------------------------------------------------
# Cores do portfolio (dados/06-performance-por-cor.csv) e variantes de grafia.
CORES_PT = [
    "Transparente", "Branca", "Branco", "Brancp", "Preta", "Preto", "Chumbo",
    "Fumê", "Fume", "Rosa", "Vermelha", "Vermelho", "Azul", "Amarela",
    "Amarelo", "Verde", "Marrom", "Terracota", "Cinza", "Grafite", "Areia",
    "Bege", "Sortida", "Sortido", "Laranja", "Natural", "Cristal", "Nude",
]
CORES_EN = [
    "Transparent", "Clear", "White", "Black", "Lead", "Smoked", "Smoke",
    "Pink", "Red", "Blue", "Yellow", "Green", "Brown", "Terracotta", "Grey",
    "Gray", "Graphite", "Sand", "Beige", "Assorted", "Orange", "Natural",
]
CORES_ES = [
    "Transparente", "Blanca", "Blanco", "Negra", "Negro", "Plomo", "Humo",
    "Rosa", "Roja", "Rojo", "Azul", "Amarilla", "Amarillo", "Verde", "Marron",
    "Terracota", "Gris", "Grafito", "Arena", "Beige", "Surtido", "Surtida",
    "Naranja", "Natural",
]

# Abreviaturas aplicadas por ordem, e so quando o nome excede o limite
# do layout. Cada aplicacao e registada no separador Auditoria.
ABREVIATURAS_PT = [
    ("Transparente", ""), ("Sortido", ""), ("Sortida", ""),
    ("Organizadora", "Organiz."), ("Organizador", "Organiz."),
    ("Divisórias", "Div."), ("Divisória", "Div."),
    ("Retangular", "Retang."), ("Retang.", "Retang."),
    ("Medicamentos", "Medicam."), ("Medicamento", "Medicam."),
    ("Confeiteiro", "Confeit."), ("Prateleira", "Prat."),
    ("Micro-ondas", "Microondas"), ("Espremedor", "Espremed."),
    ("Peças", "Pçs"), ("Peça", "Pç"), (" com ", " c/ "),
    ("Conjunto", "Conj."), ("Quadrado", "Quad."), ("Acoplado", "Acopl."),
    ("Omeleteira", "Omelet."), ("Talheres", "Talher."),
]
ABREVIATURAS_EN = [
    ("Transparent", ""), ("Assorted", ""),
    ("Compartments", "Comp."), ("Compartment", "Comp."),
    ("Rectangular", "Rect."), ("Microwave", "Microw."),
    ("Pieces", "pcs"), ("Piece", "pc"), (" with ", " w/ "),
]
ABREVIATURAS_ES = [
    ("Transparente", ""), ("Surtido", ""),
    ("Divisores", "Div."), ("Divisor", "Div."),
    ("Rectangular", "Rect."), ("Microondas", "Microond."),
    ("Medicamentos", "Medicam."),
    ("Piezas", "pzs"), ("Pieza", "pz"), (" con ", " c/ "),
]

# Base do URL do QR code. O sufixo e a REFERENCIA do produto.
BASE_URL_QR = "nitron.com.br/p/"
