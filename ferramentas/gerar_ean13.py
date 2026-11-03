#!/usr/bin/env python3
"""Gera código de barras EAN-13 em CMYK (100% K), 30 x 8 mm.

Saídas em codigos_barras/<referencia>_<ean>.{tif,pdf}
  - .tif : raster CMYK, 300 dpi, sem anti-alias (barras 0/100% K)
  - .pdf : vetorial CMYK (preferir este para a gráfica)

Uso: python3 ferramentas/gerar_ean13.py 062.012.002 7896779606245 [largura_mm altura_mm dpi]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

L = ["0001101","0011001","0010011","0111101","0100011","0110001","0101111","0111011","0110111","0001011"]
G = ["0100111","0110011","0011011","0100001","0011101","0111001","0000101","0010001","0001001","0010111"]
R = ["1110010","1100110","1101100","1000010","1011100","1001110","1010000","1000100","1001000","1110100"]
PARIDADE = ["LLLLLL","LLGLGG","LLGGLG","LLGGGL","LGLLGG","LGGLLG","LGGGLL","LGLGLG","LGLGGL","LGGLGL"]
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
QZ_E, QZ_D = 11, 7          # zonas de silêncio (módulos)
TOTAL = QZ_E + 95 + QZ_D    # 113 módulos

def digito(ean12):
    s = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(ean12))
    return str((10 - s % 10) % 10)

def modulos(ean):
    bits, guarda = "101", [1, 1, 1]
    for d, p in zip(ean[1:7], PARIDADE[int(ean[0])]):
        bits += (L if p == "L" else G)[int(d)]
    bits += "01010"
    for d in ean[7:]:
        bits += R[int(d)]
    bits += "101"
    g = set(range(0, 3)) | set(range(45, 50)) | set(range(92, 95))
    return bits, g

def geometria(alt):
    # alturas em mm a partir do topo
    texto = alt * 0.30
    return alt - texto, alt - texto * 0.55, texto * 0.80  # barra normal, barra de guarda, corpo do texto

def tif(ean, bits, g, larg, alt, dpi, saida):
    px = lambda v: round(v / 25.4 * dpi)
    W, H = px(larg), px(alt)
    x_mm = larg / TOTAL
    b_norm, b_guarda, corpo = geometria(alt)
    img = Image.new("L", (W, H), 255)  # desenha em escala, converte p/ K puro
    dr = ImageDraw.Draw(img)
    for i, b in enumerate(bits):
        if b == "1":
            x0 = px((QZ_E + i) * x_mm); x1 = px((QZ_E + i + 1) * x_mm)
            dr.rectangle([x0, 0, x1 - 1, px(b_guarda if i in g else b_norm) - 1], fill=0)
    f = ImageFont.truetype(FONTE, max(8, px(corpo)))
    def txt(s, cx_mod):
        w = dr.textlength(s, font=f)
        dr.text((px(cx_mod * x_mm) - w / 2, px(alt) - 1), s, font=f, fill=0, anchor="ls")
    txt(ean[0], QZ_E / 2)
    txt(ean[1:7], QZ_E + 3 + 21)
    txt(ean[7:], QZ_E + 50 + 21)
    img = img.point(lambda v: 0 if v < 128 else 255)  # binariza (sem cinza)
    k = img.point(lambda v: 255 - v)
    zero = Image.new("L", (W, H), 0)
    Image.merge("CMYK", (zero, zero, zero, k)).save(saida, dpi=(dpi, dpi), compression="tiff_lzw")
    return W, H

def pdf(ean, bits, g, larg, alt, saida):
    pdfmetrics.registerFont(TTFont("Mono", FONTE))
    c = canvas.Canvas(saida, pagesize=(larg * mm, alt * mm))
    c.setFillColorCMYK(0, 0, 0, 1); c.setStrokeColorCMYK(0, 0, 0, 1)
    x_mm = larg / TOTAL
    b_norm, b_guarda, corpo = geometria(alt)
    i = 0
    while i < 95:  # agrupa módulos pretos contíguos em uma barra
        if bits[i] == "1":
            j = i
            while j < 95 and bits[j] == "1" and ((j in g) == (i in g)):
                j += 1
            h = b_guarda if i in g else b_norm
            c.rect((QZ_E + i) * x_mm * mm, (alt - h) * mm, (j - i) * x_mm * mm, h * mm, stroke=0, fill=1)
            i = j
        else:
            i += 1
    c.setFont("Mono", corpo / 25.4 * 72)
    y = 0.35 * mm
    c.drawCentredString(QZ_E / 2 * x_mm * mm, y, ean[0])
    c.drawCentredString((QZ_E + 24) * x_mm * mm, y, ean[1:7])
    c.drawCentredString((QZ_E + 71) * x_mm * mm, y, ean[7:])
    c.showPage(); c.save()

def main():
    ref, ean = sys.argv[1], sys.argv[2]
    larg = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0
    alt = float(sys.argv[4]) if len(sys.argv) > 4 else 8.0
    dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 300
    if not (ean.isdigit() and len(ean) == 13):
        sys.exit("EAN precisa ter 13 dígitos")
    if digito(ean[:12]) != ean[12]:
        sys.exit(f"Dígito verificador inválido: esperado {digito(ean[:12])}")
    bits, g = modulos(ean)
    pasta = os.path.join(os.path.dirname(__file__), "..", "codigos_barras")
    os.makedirs(pasta, exist_ok=True)
    base = os.path.join(pasta, f"{ref}_{ean}")
    W, H = tif(ean, bits, g, larg, alt, dpi, base + ".tif")
    pdf(ean, bits, g, larg, alt, base + ".pdf")
    print(f"{base}.tif  {W}x{H}px  {dpi}dpi CMYK")
    print(f"{base}.pdf  vetorial CMYK  {larg}x{alt} mm")
    print(f"módulo X = {larg/TOTAL:.4f} mm  (ampliação {larg/TOTAL/0.33*100:.1f}%)")

if __name__ == "__main__":
    main()
