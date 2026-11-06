#!/usr/bin/env python3
"""Gera código de barras EAN-13 em CMYK (100% K), 30 x 8 mm.

Saídas em codigos_barras/<referencia>_<ean>.{tif,pdf}
  - .tif : raster CMYK, 300 dpi, sem anti-alias (barras 0/100% K)
  - .pdf : vetorial CMYK (preferir este para a gráfica)

Uso:
  python3 ferramentas/gerar_ean13.py 062.012.002 7896779606245 [largura_mm altura_mm dpi]
  python3 ferramentas/gerar_ean13.py --lote lista.xlsx [--escala 1.3] [--fonte 2]
     --escala: multiplica 30x8 mm (1.3 -> 39 x 10,4 mm); --fonte: soma pontos ao texto
     -> só JPG CMYK 300 dpi, nome <referencia sem pontos>_<ean>.jpg,
        em codigos_barras/jpg/ + um .zip com todos + relatório de erros.
     A planilha precisa de uma coluna com "ref" e outra com "ean" no cabeçalho.
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

FONTE_PT_EXTRA = 0.0  # pontos somados ao corpo padrão (--fonte +2)

def geometria(alt):
    """alturas em mm a partir do topo: barra normal, barra de guarda, corpo do texto (mm)"""
    corpo = alt * 0.24 + FONTE_PT_EXTRA * 25.4 / 72
    zona = corpo * 0.74 + 0.45          # altura do algarismo + respiro
    return alt - zona, alt - zona * 0.5, corpo

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
    # texto em camada própria, com anti-alias (não binariza: senão serrilha)
    f = ImageFont.truetype(FONTE, corpo / 25.4 * dpi)
    tx = Image.new("L", (W, H), 255)
    dt = ImageDraw.Draw(tx)
    base_y = alt * dpi / 25.4 - 0.15 / 25.4 * dpi
    def txt(s, cx_mod):
        dt.text((cx_mod * x_mm / 25.4 * dpi, base_y), s, font=f, fill=0, anchor="ms")
    txt(ean[0], QZ_E / 2)
    txt(ean[1:7], QZ_E + 3 + 21)
    txt(ean[7:], QZ_E + 50 + 21)
    from PIL import ImageChops
    img = ImageChops.darker(img, tx)
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
    y = 0.15 * mm
    c.drawCentredString(QZ_E / 2 * x_mm * mm, y, ean[0])
    c.drawCentredString((QZ_E + 24) * x_mm * mm, y, ean[1:7])
    c.drawCentredString((QZ_E + 71) * x_mm * mm, y, ean[7:])
    c.showPage(); c.save()

def jpg(ean, bits, g, larg, alt, dpi, saida):
    tmp = saida + ".tmp.tif"
    tif(ean, bits, g, larg, alt, dpi, tmp)
    Image.open(tmp).save(saida, "JPEG", quality=100, subsampling=0, dpi=(dpi, dpi))
    os.remove(tmp)

def ler_lista(arq):
    if arq.lower().endswith(".csv"):
        import csv
        with open(arq, newline="", encoding="utf-8-sig") as f:
            texto = f.read()
        sep = ";" if texto.splitlines()[0].count(";") >= texto.splitlines()[0].count(",") else ","
        linhas = list(csv.reader(texto.splitlines(), delimiter=sep))
    else:
        import openpyxl
        ws = openpyxl.load_workbook(arq, data_only=True, read_only=True).active
        linhas = [list(r) for r in ws.iter_rows(values_only=True)]
    cab = [str(c or "").strip().lower() for c in linhas[0]]
    i_ref = next(i for i, c in enumerate(cab) if "ref" in c)
    i_ean = next(i for i, c in enumerate(cab) if "ean" in c or "barra" in c)
    for n, r in enumerate(linhas[1:], start=2):
        if r[i_ref] is None and r[i_ean] is None:
            continue
        yield n, str(r[i_ref] or "").strip(), r[i_ean]

def lote(arq, larg=30.0, alt=8.0):
    import zipfile
    pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "codigos_barras", "jpg")
    os.makedirs(pasta, exist_ok=True)
    ok, erros, vistos = [], [], set()
    for n, ref, ean in ler_lista(arq):
        if isinstance(ean, float):
            ean = f"{ean:.0f}"
        ean = "".join(ch for ch in str(ean or "") if ch.isdigit())
        nome_ref = ref.replace(".", "").replace("/", "-").strip()
        if not nome_ref:
            erros.append((n, ref, ean, "referência vazia")); continue
        if len(ean) != 13:
            erros.append((n, ref, ean, f"EAN com {len(ean)} dígitos")); continue
        if digito(ean[:12]) != ean[12]:
            erros.append((n, ref, ean, f"dígito verificador errado (esperado {digito(ean[:12])})")); continue
        nome = f"{nome_ref}_{ean}.jpg"
        if nome in vistos:
            erros.append((n, ref, ean, "linha duplicada")); continue
        vistos.add(nome)
        bits, g = modulos(ean)
        jpg(ean, bits, g, larg, alt, 300, os.path.join(pasta, nome))
        ok.append(nome)
    base = os.path.splitext(os.path.basename(arq))[0]
    zp = os.path.join(pasta, "..", f"{base}_jpg.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for nome in ok:
            z.write(os.path.join(pasta, nome), nome)
    rel = os.path.join(pasta, "..", f"{base}_erros.csv")
    with open(rel, "w", encoding="utf-8-sig") as f:
        f.write("linha;referencia;ean;problema\n")
        for e in erros:
            f.write(";".join(map(str, e)) + "\n")
    print(f"gerados: {len(ok)}  erros: {len(erros)}")
    print(os.path.abspath(zp)); print(os.path.abspath(rel))

def main():
    global FONTE_PT_EXTRA
    args = sys.argv[1:]
    escala = 1.0
    if "--escala" in args:
        i = args.index("--escala"); escala = float(args[i + 1]); del args[i:i + 2]
    if "--fonte" in args:
        i = args.index("--fonte"); FONTE_PT_EXTRA = float(args[i + 1]); del args[i:i + 2]
    sys.argv = [sys.argv[0]] + args
    if sys.argv[1] == "--lote":
        return lote(sys.argv[2], 30.0 * escala, 8.0 * escala)
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
