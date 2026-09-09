"""Dossie em PDF da familia MODULA: capa, familia, pranchas P/M/G, mecanica,
encaixe em detalhe, base e secao, ficha tecnica e pendencias.

    python3 exporta.py && python3 celular.py && python3 detalhes.py && python3 dossie_pdf.py

As vistas vem de out/: pranchas de celular.py, cenas de exporta.py e as vistas
de inspecao/secao (det-*.png) de detalhes.py.
"""
import os, sys, datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

import modelo
from modelo import ficha

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "out")
W, H = landscape(A4)
M = 36                                   # margem
TINTA = (19 / 255, 30 / 255, 41 / 255)
CINZA = (94 / 255, 107 / 255, 112 / 255)
TEAL = (30 / 255, 167 / 255, 172 / 255)
TERRA = (206 / 255, 80 / 255, 38 / 255)

for nome, arq in (("DV", "DejaVuSans.ttf"), ("DVB", "DejaVuSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(nome, f"/usr/share/fonts/truetype/dejavu/{arq}"))


def fmt(v, casas=1):
    s = f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


class Dossie:
    def __init__(self, caminho):
        self.c = canvas.Canvas(caminho, pagesize=(W, H))
        self.c.setTitle("MODULA rev.21 — dossiê 3D")
        self.c.setAuthor("Nitron — Desenvolvimento de Produtos")
        self.pag = 0

    def rodape(self, titulo):
        c = self.c
        self.pag += 1
        c.setStrokeColorRGB(*TINTA); c.setLineWidth(1.2)
        c.line(M, H - M - 30, W - M, H - M - 30)
        c.setFillColorRGB(*TINTA); c.setFont("DVB", 15)
        c.drawString(M, H - M - 20, titulo)
        c.setFillColorRGB(*CINZA); c.setFont("DV", 8.5)
        c.drawRightString(W - M, H - M - 20, "MODULA · rev.21 · Nitron")
        c.drawRightString(W - M, M - 14, str(self.pag))
        c.drawString(M, M - 14, "Estudo de geometria e mecânica — não é desenho de molde. Malha para forma, medida e impressão 3D.")

    def imagem(self, caminho, x, y, w, h, legenda=None):
        """Encaixa a imagem em (x, y, w, h) mantendo proporcao; y e a base."""
        im = Image.open(caminho)
        iw, ih = im.size
        esc = min(w / iw, h / ih)
        dw, dh = iw * esc, ih * esc
        dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
        self.c.drawImage(ImageReader(im), dx, dy, dw, dh)
        if legenda:
            self.c.setFillColorRGB(*CINZA); self.c.setFont("DV", 8.5)
            self.c.drawCentredString(x + w / 2, y - 11, legenda)

    def texto(self, x, y, linhas, tam=9.5, cor=TINTA, entre=1.38, larg=None, fonte="DV"):
        """Paragrafos com quebra por largura e negrito inline entre **...**."""
        c = self.c
        c.setFillColorRGB(*cor)
        yy = y
        larg = larg or (W - 2 * M)
        for ln in linhas:
            if ln == "":
                yy -= tam * entre * 0.6
                continue
            # tokens (palavra, negrito)
            toks, neg = [], False
            for i, parte in enumerate(ln.split("**")):
                if i > 0:
                    neg = not neg
                for p in parte.split(" "):
                    if p:
                        toks.append((p, neg))
            linha, lw = [], 0.0
            esp = pdfmetrics.stringWidth(" ", fonte, tam)

            def despeja(linha):
                xx = x
                for p, ng in linha:
                    f = "DVB" if ng else fonte
                    c.setFont(f, tam); c.drawString(xx, yy, p)
                    xx += pdfmetrics.stringWidth(p, f, tam) + esp
            for p, ng in toks:
                w = pdfmetrics.stringWidth(p, "DVB" if ng else fonte, tam)
                if linha and lw + w > larg:
                    despeja(linha); yy -= tam * entre
                    linha, lw = [], 0.0
                linha.append((p, ng)); lw += w + esp
            if linha:
                despeja(linha); yy -= tam * entre
        return yy

    def tabela(self, x, y, colunas, linhas, largs, tam=9, alt=15):
        c = self.c
        c.setFont("DVB", tam); c.setFillColorRGB(*TINTA)
        xx = x
        for col, lw in zip(colunas, largs):
            c.drawString(xx + 4, y, col); xx += lw
        c.setStrokeColorRGB(*TINTA); c.setLineWidth(0.8)
        c.line(x, y - 4, x + sum(largs), y - 4)
        yy = y - alt
        for i, ln in enumerate(linhas):
            xx = x
            for j, (cel, lw) in enumerate(zip(ln, largs)):
                c.setFont("DVB" if j == 0 else "DV", tam)
                c.setFillColorRGB(*TINTA)
                c.drawString(xx + 4, yy, str(cel)); xx += lw
            c.setStrokeColorRGB(0.85, 0.85, 0.85); c.setLineWidth(0.4)
            c.line(x, yy - 4, x + sum(largs), yy - 4)
            yy -= alt
        return yy

    def nova(self):
        self.c.showPage()

    def salvar(self):
        self.c.save()


def main():
    modelo.AMOSTRA = [1.3, 20]           # a mesma malha do STL: a cota tem de bater
    F = {k: ficha(k)[1] for k in "PMG"}
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    saida = os.path.join(OUT, "modula-rev21.pdf")
    d = Dossie(saida)
    c = d.c

    # ---------------- capa ----------------
    d.imagem(os.path.join(OUT, "det-iso.png"), W * 0.42, M + 30, W * 0.58 - M, H - 2 * M - 60)
    c.setFillColorRGB(*TINTA); c.setFont("DVB", 44)
    c.drawString(M, H - 150, "MODULA")
    c.setFont("DV", 15); c.setFillColorRGB(*CINZA)
    c.drawString(M, H - 178, "Família de organizadores modulares")
    c.drawString(M, H - 198, "de frente aberta — 3 moldes: P, M, G")
    c.setFillColorRGB(*TERRA); c.setFont("DVB", 12)
    c.drawString(M, H - 240, "rev.21 — modelo 3D paramétrico")
    y = d.texto(M, H - 268, [
        "Encaixa quase colado no transporte (ninho de 17 mm no M), pluga um sobre o outro no uso (pilha com canal e guia), "
        "pé em copo aberto para cima, fundo chapado no P e vazado no M e no G, parede com o pattern oficial da marca. "
        "Dois P penduram pela aba no aro de um M; dois M no de um G.",
    ], tam=10.5, larg=W * 0.40 - M)
    y = d.tabela(M, y - 14, ["", "Externo (mm)", "Capacidade", "Massa"],
                 [[k, f"{fmt(F[k]['X'],0)} × {fmt(F[k]['Y'],0)} × {fmt(F[k]['H'],0)}",
                   f"{fmt(F[k]['litros_total'])} L", f"{fmt(F[k]['massa_g'],0)} g"] for k in "PMG"],
                 [26, 120, 80, 70], tam=10, alt=17)
    d.texto(M, y - 16, [
        f"Nitron — Desenvolvimento de Produtos · {hoje}",
        "Arquivos 3D: modula-P/M/G.stl (mm, 1:1) e .glb (celular), em design/modula/out/",
    ], tam=9, cor=CINZA, larg=W * 0.40 - M)
    d.nova()

    # ---------------- familia ----------------
    d.rodape("A família — P, M, G no palete 1 : 2 : 4")
    d.imagem(os.path.join(OUT, "01-familia.png"), M, H - M - 300, W - 2 * M, 255)
    cols = ["", "Externo (mm)", "Cesta + perna", "Parede", "Massa PP", "Capacidade", "Passo pilha", "Passo ninho", "Cubagem 10 pç", "Fechamento"]
    largs = [28, 120, 88, 55, 68, 78, 78, 80, 88, 86]
    lin = []
    for k in "PMG":
        s = F[k]
        lin.append([k, f"{fmt(s['X'],0)} × {fmt(s['Y'],0)} × {fmt(s['H'],0)}", f"{fmt(s['hc'],0)} + {fmt(s['perna'],0)}",
                    f"{fmt(s['e'])} mm", f"{fmt(s['massa_g'],0)} g", f"{fmt(s['litros_total'])} L",
                    f"{fmt(s['passo_pilha'],0)} mm", f"{fmt(s['passo_ninho'])} mm",
                    f"{fmt(10*s['H']/(s['H']+9*s['passo_ninho']))}×", f"{fmt(s['ton_min'],0)}–{fmt(s['ton_max'],0)} tf"])
    y = d.tabela(M, H - M - 330, cols, lin, largs)
    d.texto(M, y - 12, [
        "Módulo de palete menos 4 mm: 396 × 296 cabe doze vezes em 1000 × 1200 com folga; 400 × 300 exatos não cabem. "
        "Dois P dão um M, dois M dão um G. A altura segue a proporção áurea (X : H = 1,618).",
        "O passo de ninho é conferido em toda build contra a malha real: a peça é girada 180°, subida o passo, e nenhum "
        "vértice da base pode ficar abaixo do fundo da peça de baixo fora de um copo. Fechamento = área projetada × 300–400 bar.",
    ], larg=W - 2 * M)
    d.nova()

    # ---------------- pranchas ----------------
    for k in "PMG":
        s = F[k]
        d.rodape(f"MODULA {k} — seis vistas   ·   {fmt(s['X']/10)} × {fmt(s['Y']/10)} × {fmt(s['H']/10)} cm   ·   {fmt(s['litros_total'])} L   ·   {fmt(s['massa_g'],0)} g")
        im = Image.open(os.path.join(OUT, f"modula-{k}-vistas.png"))
        # corta o cabecalho da prancha (ja esta no titulo da pagina)
        im = im.crop((0, 66, im.size[0], im.size[1]))
        tmp = os.path.join(OUT, f"_prancha_{k}.png"); im.save(tmp)
        d.imagem(tmp, M, M + 6, W - 2 * M, H - 2 * M - 46)
        d.nova()

    # ---------------- mecanica ----------------
    d.rodape("A mecânica — ninho a 180°, pilha a 0°")
    cw = (W - 2 * M - 20) / 2
    d.imagem(os.path.join(OUT, "03-ninho.png"), M, H - M - 330, cw, 285, "Dez M ninhadas: 245 + 9 × 17,2 = 400 mm de altura (cubagem 6,1×)")
    d.imagem(os.path.join(OUT, "04-pilha.png"), M + cw + 20, H - M - 330, cw, 285, "Três M plugadas: passo 203 mm, os andares entrelaçam 42 mm")
    s = F["M"]
    d.texto(M, H - M - 362, [
        "**Ninho (girada 180°).** A parede desce rente à parede de baixo: passo = espessura ÷ tan 7,5° + 2 mm de folga = "
        f"{fmt(s['passo_ninho'])} mm no M. Os pés são copos abertos para cima com as mesmas faces a 7,5°, então o copo de cima entra no copo "
        "de baixo com a mesma folga (0,26 mm). A janela do rodapé deixa a coluna interna passar.",
        "**Pilha (alinhada 0°).** O rodapé da peça de cima pousa num canal no topo de quatro colunas internas — lábio da coluna por dentro, "
        f"guia chanfrada por fora — 3 mm abaixo do aro. Degrau de {fmt(s['larg_ponte'])} mm (ponte), canal de {fmt(s['larg_canal'])} mm, "
        "tolerância lateral −3 / +1 mm. O aro continua um anel fechado.",
        "**A regra.** Toda superfície que desliza no ninho tem os mesmos 7,5°, e a parede é lisa por fora: um friso de 2 mm já trava o ninho a meio caminho.",
    ], larg=W - 2 * M)
    d.nova()
    d.rodape("Em seção — três M ninhadas e duas M plugadas (cortes)")
    d.imagem(os.path.join(OUT, "det-ninho-secao.png"), M, M + 40, (W - 2 * M) * 0.62, H - 2 * M - 90,
             "Ninho, corte pelos copos: cada peça desce 17,2 mm dentro da anterior, copo dentro de copo")
    d.imagem(os.path.join(OUT, "det-pilha-secao.png"), M + (W - 2 * M) * 0.64, M + 40, (W - 2 * M) * 0.36, H - 2 * M - 90,
             "Pilha, corte pela coluna: rodapé no canal, 42 mm de entrelace")
    d.nova()

    # ---------------- encaixe em detalhe ----------------
    d.rodape("O encaixe em detalhe (M) — peça de baixo em cinza")
    gw = (W - 2 * M - 20) / 2
    gh = (H - 2 * M - 60 - 30) / 2
    y1 = H - M - 44 - gh
    y0 = y1 - 26 - gh
    d.imagem(os.path.join(OUT, "det-ninho-canto.png"), M, y1, gw, gh, "Ninho, corte pelo canto: copo de cima (terracota) dentro do copo de baixo (cinza)")
    d.imagem(os.path.join(OUT, "det-pilha-assento.png"), M + gw + 20, y1, gw, gh, "Pilha, corte pela coluna: o rodapé de cima no canal, entre lábio e guia")
    d.imagem(os.path.join(OUT, "det-canto.png"), M, y0, gw, gh, "O canto cortado: o copo visto de dentro, bolsão de 40 × 40 mm")
    d.imagem(os.path.join(OUT, "det-canal.png"), M + gw + 20, y0, gw, gh, "Topo da coluna: ponte, canal de 5,7 mm, guia e a fenda da parede de cima")
    d.nova()

    # ---------------- a pendura ----------------
    d.rodape("O encaixe cruzado — dois P num M, dois M num G, pendurados pela aba")
    d.imagem(os.path.join(OUT, "08-pendura.png"), M, H - M - 320, (W - 2 * M) * 0.62, 275,
             "Dois P girados 90° no aro de um M (esq.) e dois M no aro de um G (dir.)")
    d.imagem(os.path.join(OUT, "09-pendura-lateral.png"), M + (W - 2 * M) * 0.64, H - M - 320, (W - 2 * M) * 0.36, 275,
             "De lado: o aro do P fica 10 mm acima do aro do M; a base, 20 mm acima do fundo")
    pp, pm = F["P"]["pendura"], F["M"]["pendura"]
    cols = ["", "dois no vão", "folga parede x / y", "folga na fenda da ponte", "apoio na aba", "aro acima", "base sobre o fundo"]
    d.tabela(M, H - M - 352, cols, [
        ["P em M", f"{fmt(pp['largura_dois'],0)} em {fmt(pp['vao_grande'],0)}", f"{fmt(pp['f_par_x'])} / {fmt(pp['f_par_y'])} mm", f"{fmt(pp['f_ponte'])} mm", f"{fmt(pp['apoio_x'])} mm", f"{fmt(pp['sobe'])} mm", f"{fmt(pp['f_fundo'])} mm"],
        ["M em G", f"{fmt(pm['largura_dois'],0)} em {fmt(pm['vao_grande'],0)}", f"{fmt(pm['f_par_x'])} / {fmt(pm['f_par_y'])} mm", f"{fmt(pm['f_ponte'])} mm", f"{fmt(pm['apoio_x'])} mm", f"{fmt(pm['sobe'])} mm", f"{fmt(pm['f_fundo'])} mm"],
    ], [60, 90, 120, 130, 90, 80, 110], tam=8.8, alt=14)
    d.texto(M, H - M - 405, [
        "**A cadeia de pendura.** A parede do pequeno tem de passar por dentro da aba do grande com folga. Por isso cada cota do pequeno é o módulo do grande "
        "menos 6 mm (289 × 192 / 390 × 295 / 596 × 396), e a aba cresce para dentro da família: 11,6 no G, 12,4 no M, 12,9 no P. A altura é X ÷ φ. "
        "Tudo abaixo do módulo de palete: dois P dão um M, dois M dão um G, 16 / 8 / 4 por camada em 1200 × 800.",
        "**Por que pendurado, e não em cima.** Os 7,5° que fazem o ninho de 17 mm deixam a base do P com 231 × 131 mm — cai 52 mm para dentro da parede do M. "
        "Apoiar por baixo exigiria estrutura interna simétrica, que a regra do giro de 180° proíbe, ou travessas que não saem do molde sem lâmina. "
        "Pendurar pela aba não muda nenhum mecanismo e sai reto do molde. A função `pendura()` confere as folgas em toda build.",
    ], larg=W - 2 * M)
    d.nova()

    # ---------------- o grafismo ----------------
    d.rodape("O grafismo — o pattern oficial da marca, furo a furo")
    d.imagem(os.path.join(AQUI, "grafismo", "pattern-tile.png"), M, H - M - 300, (W - 2 * M) * 0.38, 250,
             "O ladrilho do arquivo da marca: célula de 230 × 280 pt")
    d.imagem(os.path.join(OUT, "det-parede.png"), M + (W - 2 * M) * 0.40, H - M - 300, (W - 2 * M) * 0.60, 250,
             "A lateral do M: o mesmo ladrilho, alma de 4,0 mm entre furos")
    s = F["M"]
    d.texto(M, H - M - 335, [
        "**Reprodução exata.** O arquivo .ai traz o grafismo como PDF tiling pattern. Os quatro caminhos (A curto, B longo, C médio e D = C girado 180°) "
        "e as posições do motivo foram lidos do próprio arquivo, e a reconstrução foi conferida pixel a pixel contra o ladrilho original: 0 pixels de diferença.",
        f"**Escala pela alma.** O que limita a densidade é o molde: a alma mínima entre dois furos vizinhos vale 12,18 pt no ladrilho, e a peça pede 4 mm. "
        f"Isso fixa a escala em {fmt(s['graf_esc'],3)} mm/pt no M: elemento curto de {fmt(s['graf_alt_elem'])} mm, longo de {fmt(s['graf_alt_longo'])} mm, "
        f"furo de {fmt(s['graf_largura'])} mm de largura, período de {fmt(s['graf_pu'])} mm ao longo da parede — ajustado para fechar a volta sem emenda. "
        f"Vazado {s['graf_vazado']*100:.0f} %.",
        "**Onde não há furo.** As quatro colunas do encaixe, o painel da etiqueta na frente, a faixa cheia junto ao fundo e a faixa sob o aro continuam inteiros. "
        "Elemento que ficaria com menos de 45 % da área entre as faixas não nasce — evita o caco.",
    ], larg=W - 2 * M)
    d.nova()

    # ---------------- base e secao ----------------
    d.rodape("A base e a seção (M)")
    d.imagem(os.path.join(OUT, "det-baixo.png"), M, M + 40, gw + 40, H - 2 * M - 90, "Por baixo: quatro copos com sola fechada, rodapé recuado, nervuras a 45° e o vão com saída positiva")
    d.imagem(os.path.join(OUT, "det-meia.png"), M + gw + 60, M + 40, gw - 40, H - 2 * M - 90, "Meia peça: aro em L, parede a 7,5°, fundo nervurado e o copo do pé")
    d.nova()

    # ---------------- ficha tecnica ----------------
    d.rodape("Ficha técnica")
    cols = ["Parâmetro", "P", "M", "G"]
    largs = [300, 150, 150, 150]

    def r(nome, f, casas=1, suf=""):
        return [nome] + [f"{fmt(f(F[k]), casas)}{suf}" for k in "PMG"]
    lin = [
        ["Externo X × Y × H (mm)"] + [f"{fmt(F[k]['X'],0)} × {fmt(F[k]['Y'],0)} × {fmt(F[k]['H'],0)}" for k in "PMG"],
        ["Cesta + perna (mm)"] + [f"{fmt(F[k]['hc'],0)} + {fmt(F[k]['perna'],0)}" for k in "PMG"],
        r("Espessura da parede (mm)", lambda s: s["e"]),
        r("Espessura do fundo (mm)", lambda s: s["ef"]),
        r("Saída da parede (graus)", lambda s: modelo.SAIDA_GR),
        r("Raio do canto no aro (mm)", lambda s: s["R"], 0),
        r("Aba do aro (mm)", lambda s: s["aba"]),
        r("Massa PP (g)", lambda s: s["massa_g"], 0),
        r("Capacidade total (L)", lambda s: s["litros_total"]),
        r("Capacidade até a boca da frente (L)", lambda s: s["litros_boca"]),
        r("Passo de ninho (mm)", lambda s: s["passo_ninho"]),
        r("Passo de pilha (mm)", lambda s: s["passo_pilha"], 0),
        r("Cubagem de 10 peças ninhadas", lambda s: 10 * s["H"] / (s["H"] + 9 * s["passo_ninho"]), 1, "×"),
        r("Pé: corda no chão → no rodapé (mm)", lambda s: s["larg_pe"], 0),
        ["Apoio no piso, 4 pés (cm²)"] + [fmt(F[k]["apoio_cm2"]) for k in "PMG"],
        r("Rodapé: altura / recuo (mm)", lambda s: s["h_rodape"], 0),
        ["Coluna: largura / janela (mm)"] + [f"{fmt(F[k]['w_col'])} / {fmt(F[k]['w_col'] + 2*F[k]['rampa_col'])}" for k in "PMG"],
        ["Degrau da pilha: ponte / canal (mm)"] + [f"{fmt(F[k]['larg_ponte'])} / {fmt(F[k]['larg_canal'])}" for k in "PMG"],
        ["Fundo: nervura (larg × alt) / vão (mm)"] + [f"{fmt(F[k]['larg_nerv'])} × {fmt(F[k]['alt_nerv'])} / {fmt(F[k]['vao_fundo'],0)}" for k in "PMG"],
        ["Grafismo: largura do furo / alma (mm)"] + [f"{fmt(F[k]['graf_largura'])} / {fmt(F[k]['graf_alma'])}" for k in "PMG"],
        ["Grafismo: fração vazada"] + [f"{F[k]['graf_vazado']*100:.0f} %" for k in "PMG"],
        r("Área projetada (cm²)", lambda s: s["area_projetada_cm2"], 0),
        ["Fechamento 300–400 bar (tf)"] + [f"{fmt(F[k]['ton_min'],0)} – {fmt(F[k]['ton_max'],0)}" for k in "PMG"],
        ["Ninho: vértices da base abaixo do fundo / fora do copo"] + [f"{F[k]['ninho_pts']} / {F[k]['ninho_viol']}" for k in "PMG"],
    ]
    # corda do pe: chao -> rodape
    for ln in lin:
        if ln[0].startswith("Pé: corda"):
            for j, k in enumerate("PMG"):
                ln[j + 1] = f"{fmt(F[k]['larg_pe'],0)} → {fmt(2*F[k]['hw_topo'],0)}"
        if ln[0].startswith("Rodapé"):
            for j, k in enumerate("PMG"):
                ln[j + 1] = f"{fmt(F[k]['h_rodape'],0)} / {fmt(F[k]['recuo'])}"
    d.tabela(M, H - M - 52, cols, lin, largs, tam=8.6, alt=13.6)
    d.nova()

    # ---------------- pendencias ----------------
    d.rodape("O que a fábrica precisa decidir — e o que continua aberto")
    col_w = (W - 2 * M - 30) / 2
    d.texto(M, H - M - 56, [
        "**1. Câmara quente no G.** Área projetada de 2.360 cm²: 722 tf a 300 bar, 963 tf a 400 bar. Com parede de 2,5 mm vazada em 46 %, "
        "a relação fluxo/espessura é 213:1 — pede 3–4 pontos de injeção. É essa decisão, não o desenho, que define a máquina do G.",
        "",
        "**2. Qual PP.** Caixa sob carga pede copolímero de impacto, não o H 105 clarificado. Seja qual for, tem de continuar PP: o ciclo de "
        "moído só funciona porque o refugo é mono-resina.",
        "",
        "**3. Ensaio de compressão e fluência** antes do aço: rodapé apoiado no canal de 4 colunas, 5 andares a 15 kg. PP senta sob carga "
        "constante; com parede vazada isso decide a espessura final.",
        "",
        "**4. Vão do fundo e bolsões de canto.** Grelha de 9 / 18 / 22 mm e quatro copos abertos para dentro da cesta (40 × 40 mm no M, "
        "27 × 27 no P). Indiferentes para farmácia e e-commerce, decisivos para quarto infantil e cozinha. Alternativa sem mexer no molde: "
        "tapete de fundo avulso, que vira item de venda.",
        "",
        "**5. Cor só por Coloratto.** Branco (farmácia e casa), chumbo (e-commerce), terracota (linha). Cor divide demanda; produto novo cria.",
    ], larg=col_w)
    d.texto(M + col_w + 30, H - M - 56, [
        "**Aberto no modelo**",
        "• A malha não é estanque (1,5–2,0 % de arestas ímpares, das emendas de banda): serve para forma, medida e impressão 3D, não para usinar.",
        "• Guia, ponte e face interna da coluna sem raio de concordância — trabalho de CAD.",
        "• Furo do P com 14,8 mm de largura: fora da faixa de aprisionamento de dedo (7–12 mm).",
        "• O P encolheu para 4,5 L e o M para 15,1 L pela cadeia de pendura; a aba maior come 2,5 mm de boca por lado no P.",
        "• O `engenheiro-molde` ainda não validou a parede do G.",
        "",
        "**Verificado nesta revisão**",
        "• Ninho: peça girada 180° e subida o passo — 0 vértices da base fora de um copo (P, M, G).",
        "• Saída de molde: face externa do copo pela cavidade, interna pelo macho; vão sob o fundo alarga para baixo; coluna com 0,5°; "
        "nervura afunilada 1°.",
        "• Pilha: rodapé cai no canal com −3 / +1 mm; a parede de cima passa na fenda entre ponte e aba com 1,5 mm.",
        "• Parede vazada conferida por integral independente: razão 0,98.",
        "",
        "**Arquivos**",
        "design/modula/out/modula-{P,M,G}.stl — binário, mm, 1:1",
        "design/modula/out/modula-{P,M,G}.glb — glTF, abre no celular",
        "design/modula/modelo.py — o modelo paramétrico; `python3 modelo.py` imprime a ficha e quebra se o ninho colidir",
    ], larg=col_w)
    d.salvar()
    print(saida, os.path.getsize(saida) / 1e6, "MB", d.pag + 1, "paginas")


if __name__ == "__main__":
    main()
