"""Saidas do P rev.28: vistas, mecanica (pilha e ninho), detalhes, STL, GLB."""
import os, sys, math
import p28, render as R, secao
from exporta import paleta, COR_CORPO, escreve_stl
from celular import glb

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
SP = os.environ.get("P28_OUT", OUT)


def cena(nome, grupos, W, H, az, el, sombra=True, z_chao=None):
    kw = dict(az=az, el=el, sombra=sombra)
    if z_chao is not None:
        kw["z_chao"] = z_chao
    R.cena(grupos, W, H, **kw).save(os.path.join(SP, f"p28-{nome}.png"))


def main(quais=("vistas", "mecanica", "detalhes", "arquivos")):
    m, s = p28.ficha()
    ns = m.normais_suaves(42)
    cor = paleta(COR_CORPO["P"])
    cinza = dict.fromkeys(cor, (125, 125, 125))
    claro = dict.fromkeys(cor, (215, 205, 195))
    terra = paleta(COR_CORPO["M"])
    hp = s["h_pe"]
    tri = lambda off=(0, 0, 0), giro=False: m.triangulos(offset=off, giro180=giro)

    if "vistas" in quais:
        cena("iso", [(tri(), cor, ns)], 1600, 1150, 42, 23, z_chao=-hp)
        cena("frente", [(tri(), cor, ns)], 1400, 1100, 90, 6, z_chao=-hp)
        cena("lado", [(tri(), cor, ns)], 1600, 1100, 0, 6, z_chao=-hp)
        cena("tras", [(tri(), cor, ns)], 1400, 1100, 270, 12, z_chao=-hp)
        cena("baixo", [(tri(), cor, ns)], 1500, 1100, 35, -28, sombra=False)
    if "mecanica" in quais:
        pp, pn = s["passo_pilha"], s["passo_ninho"]
        # tres empilhados (0 graus): lingueta no entalhe
        cena("pilha", [(tri((0, 0, k * pp)), [cor, terra, cor][k], ns) for k in range(3)], 1100, 1500, 30, 10, z_chao=-hp)
        # quatro ninhados (alternando 180 graus)
        cena("ninho", [(tri((0, 0, k * pn), bool(k % 2)), [cor, terra, claro, cinza][k], ns) for k in range(4)], 1300, 1300, 35, 14, z_chao=-hp)
        # corte do ninho pela lateral: as linguetas nos rasgos
        xcut = s["Xb"] / 2 - 30
        def clip(t, *planos):
            for p0, nrm in planos:
                t = secao.corta(t, p0, nrm)
            return t
        grupos = []
        for k in range(3):
            grupos.append((clip(tri((0, 0, k * pn), bool(k % 2)), ((xcut, 0, 0), (1, 0, 0))), [cor, terra, claro][k], None))
        cena("ninho-corte", grupos, 1500, 1200, 0, 8, sombra=False)
    if "detalhes" in quais:
        pp = s["passo_pilha"]
        y_f, Xb2, Hw = s["y_f"], s["Xb"] / 2, s["Hw"]
        # o pe da frente (lateral direita) entrando no entalhe da peca de baixo
        rec = [((Xb2 - 40, 0, 0), (1, 0, 0)), ((0, y_f - 35, 0), (0, 1, 0)), ((0, y_f + 35, 0), (0, -1, 0)),
               ((0, 0, Hw - 40), (0, 0, 1)), ((0, 0, Hw + 40), (0, 0, -1))]
        def clip(t, *planos):
            for p0, nrm in planos:
                t = secao.corta(t, p0, nrm)
            return t
        cena("pe-entalhe", [(clip(tri(), *rec), cor, None), (clip(tri((0, 0, pp)), *rec), terra, None)], 1300, 1000, 60, 18, sombra=False)
        cena("pe-entalhe-fora", [(clip(tri(), *rec), cor, None), (clip(tri((0, 0, pp)), *rec), terra, None)], 1300, 1000, -30, 12, sombra=False)
        # so o pe, por baixo
        recp = [((Xb2 - 40, 0, 0), (1, 0, 0)), ((0, y_f - 30, 0), (0, 1, 0)), ((0, y_f + 30, 0), (0, -1, 0)), ((0, 0, 30), (0, 0, -1))]
        cena("pe", [(clip(tri(), *recp), cor, None)], 1200, 900, 40, -25, sombra=False)
        # a lateral de frente, bolinhas
        lat = [tt for tt in tri() if all(p[0] > Xb2 - 30 for p in tt[:3])]
        cena("bolinhas", [(lat, cor, None)], 1700, 1100, 0, 0, sombra=False)
        # o acoplador: dois P lado a lado, corte na altura da saia
        cena("acoplados", [(tri(), cor, ns), (tri((s["X"], 0, 0)), terra, ns)], 1700, 1000, 25, 16, z_chao=-hp)
    if "arquivos" in quais:
        n = escreve_stl(m, os.path.join(SP, "modula-P28.stl"), "MODULA P rev.28")
        t, b = glb(m, os.path.join(SP, "modula-P28.glb"), "MODULA P rev.28", (0.86, 0.86, 0.84))
        print(f"  STL {n} tri; GLB {t} tri {b/1e6:.2f} MB")
    print("ok", SP)


def prancha(nome="modula-P28-vistas.png"):
    """Seis vistas com cabecalho, como as pranchas da familia."""
    from PIL import Image, ImageDraw, ImageFont
    m, s = p28.ficha()
    ns = m.normais_suaves(42)
    cor = paleta(COR_CORPO["P"])
    g = lambda: (m.triangulos(), cor, ns)
    W, H = 760, 620
    vistas = [("PERSPECTIVA", 38, 16), ("FRENTE", 90, 0), ("LATERAL", 0, 0),
              ("SUPERIOR", 0, 89), ("3/4 TRASEIRA", 218, 20), ("POR BAIXO", 35, -28)]
    tiles = [(rot, R.cena([g()], W, H, az=az, el=el, z_chao=-s["h_pe"], sombra=(el > 0))) for rot, az, el in vistas]
    fundo = (246, 244, 239)
    def fonte(px):
        for c in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            try: return ImageFont.truetype(c, px)
            except Exception: pass
        return ImageFont.load_default()
    f_tit, f_rot, f_sub = fonte(40), fonte(22), fonte(24)
    topo = 116
    folha = Image.new("RGB", (W * 3, H * 2 + topo + 40), fundo)
    d = ImageDraw.Draw(folha)
    d.text((24, 22), "MODULA P  rev.28", font=f_tit, fill=(30, 30, 30))
    d.text((24 + 560, 36), f"{s['X']/10:.1f} x {s['Y']/10:.1f} x {s['H']/10:.1f} cm    {s['litros_total']:.1f} L    {s['massa_g']:.0f} g    "
           f"pilha {s['passo_pilha']:.0f} mm  ·  ninho {s['passo_ninho']:.1f} mm", font=f_sub, fill=(90, 90, 90))
    d.line((24, 78, W * 3 - 24, 78), fill=(180, 180, 180), width=2)
    for k, (rot, im) in enumerate(tiles):
        x, y = (k % 3) * W, topo + (k // 3) * H
        folha.paste(im, (x, y))
        d.text((x + 20, y - 26), rot, font=f_rot, fill=(23, 112, 122))
    folha.save(os.path.join(SP, nome))
    print("  prancha", nome)


def cortes():
    """Corte pelo centro do pe da frente (lateral direita): fica a metade y > y_f,
    vista de frente para a face cortada."""
    m, s = p28.ficha()
    cor = paleta(COR_CORPO["P"]); terra = paleta(COR_CORPO["M"]); claro = dict.fromkeys(cor, (215, 205, 195))
    y_f, Xb2, Hw, pp, pn = s["y_f"], s["Xb"] / 2, s["Hw"], s["passo_pilha"], s["passo_ninho"]
    tri = lambda off=(0, 0, 0), giro=False: m.triangulos(offset=off, giro180=giro)
    def rec(t, yc, x_min, z0, z1):
        for p0, nrm in (((0, yc, 0), (0, 1, 0)), ((x_min, 0, 0), (1, 0, 0)), ((0, 0, z0), (0, 0, 1)), ((0, 0, z1), (0, 0, -1)),
                        ((0, yc + 40, 0), (0, -1, 0))):
            t = secao.corta(t, p0, nrm)
        return t
    z0, z1 = Hw - 28, Hw + 30
    cena("corte-pilha", [(rec(tri(), y_f, Xb2 - 30, z0, z1), cor, None),
                         (rec(tri((0, 0, pp)), y_f, Xb2 - 30, z0, z1), terra, None)], 1300, 900, 285, 12, sombra=False)
    z0, z1 = pn - 28, pn + 30
    cena("corte-ninho", [(rec(tri(), -y_f, Xb2 - 30, z0, z1), cor, None),
                         (rec(tri((0, 0, pn), True), -y_f, Xb2 - 30, z0, z1), terra, None)], 1300, 900, 285, 12, sombra=False)
    print("  cortes")


if __name__ == "__main__":
    quais = tuple(sys.argv[1:]) or ("vistas", "mecanica", "detalhes", "arquivos", "prancha", "cortes")
    main(tuple(q for q in quais if q in ("vistas", "mecanica", "detalhes", "arquivos")))
    if "prancha" in quais:
        prancha()
    if "cortes" in quais:
        cortes()
