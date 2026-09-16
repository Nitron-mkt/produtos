"""
MODULA P rev.28 — o P recomecado do zero.

PREMISSAS (do pedido)
  01 P acopla P–P pela lateral, macho e femea, discreto.
  02 P empilha sobre P: o PE entra num ENTALHE na borda da peca de baixo.
  03 P ninha em P (girado 180 graus) para cubagem.
  04 Parede vazada em BOLINHAS, grandes em cima e pequenas embaixo; base fechada;
     peca mais leve.

A REGRA QUE GOVERNA (descoberta ao testar o ninho de tres pecas)
  Quem empilha e quem ninha giram 180 graus entre si, mas a TERCEIRA peca do
  ninho tem a mesma orientacao da primeira. O que segura o pe da peca empilhada
  (o entalhe) segura tambem o pe da terceira peca ninhada, no mesmo lugar. Logo
  o passo de ninho nao pode ser menor que METADE do passo de pilha:
      2 * pn = passo_pilha = H_total - profundidade_do_entalhe
  Com o pe na borda (entalhe de 8 mm), pn = 85,5 mm: 10 P ninhados = 949 mm
  (1,9x). Querer mais cubagem = afundar a pilha (cada 2 mm de afundamento compram
  1 mm de passo). A familia anterior (rev.09–27) ignorava isso: o "10 P
  ninhados" nunca existiu — a terceira peca parava no canal da primeira.

O QUE A REGRA LIBERA
  Com pn = 85,5 a saida nao precisa de 7,5 graus: 2 graus bastam (folga de
  parede no ninho = pn*tan - e = 1,4 mm). A caixa fica quase reta, ganha 55% de
  volume e o pe fica a 6 mm da linha da borda — o entalhe vira um rasgo de
  4,6 x 8 mm, e nao uma coluna.

MECANICA
  Quatro pes sob o fundo, cada um com uma LINGUETA de 4 mm (largura ao longo da
  parede) que sai 5,7 mm para fora da linha da base. Posicoes assimetricas S:
  dois pes nas laterais junto a frente, dois na traseira. Na pilha (0 graus) a
  lingueta cai no ENTALHE do topo da parede em S. No ninho (180 graus) ela
  chega em R(S): na frente e vao (nada a cortar); no fundo das laterais e um
  RASGO de 4,6 mm que vai da borda ate o assento do ninho (93 mm), e cujo fundo
  segura a peca girada no passo pn. Nada por dentro da boca: a parede interna e
  lisa, e o ninho e parede-em-parede com 1,4 mm de folga.

  Tudo conferido em toda build: descida da peca 2 (girada) e da peca 3 (nao
  girada) contra parede, aba, fundo, entalhes e rasgos da peca 1.
"""
import math
from geometria import DEG, Contorno, Malha, banda, perfurada
import grafismo as G

AMOSTRA = [1.3, 20]
RHO_PP = 0.905
RAMPA_FRENTE = 14.0

P = dict(
    nome="MODULA P", X=192.0, Y=289.0, H=179.0,
    e=1.6, ef=1.8, aba=12.0, t_aba=2.0, saia=9.0, saida=2.0, Rb=14.0,
    hf=55.0, mergulho=15.0, hb=16.0, h_aro=10.0,
    h_pe=6.0, pe_larg=14.0, pe_prof=10.0, tab_w=4.0, folga_tab=0.6, d_seat=8.0,
    rodape=3.0, recuo=2.0,
    dots=(10.0, 4.0, 3.0),          # d_max, d_min, alma
    ac=(4.5, 10.0, 0.3),            # haste, cabeca, folga do acoplador
)


def suave(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def parametros(p=P):
    s = dict(p)
    s["tan"] = math.tan(s["saida"] * DEG)
    s["Hw"] = Hw = s["H"] - s["h_pe"]                 # parede: do fundo (z=0) a borda
    s["Xb"] = s["X"] - 2 * s["aba"] - 2 * Hw * s["tan"]
    s["Yb"] = s["Y"] - 2 * s["aba"] - 2 * Hw * s["tan"]
    s["ax"], s["by"] = s["Xb"] / 2 - s["Rb"], s["Yb"] / 2 - s["Rb"]
    s["x_cheia"] = s["ax"] - 2.0
    s["z_seat"] = Hw - s["d_seat"]                    # fundo do entalhe: sola da peca empilhada
    s["passo_pilha"] = s["z_seat"] + s["h_pe"]        # sola a sola
    s["passo_ninho"] = pn = s["passo_pilha"] / 2      # a regra
    s["folga_ninho"] = pn * s["tan"] - s["e"]
    assert s["folga_ninho"] > 0.3, f"ninho aperta: folga {s['folga_ninho']:.2f}"
    s["z_sola2"] = pn - s["h_pe"]                     # sola da peca girada no ninho
    s["tab_L"] = round(Hw * s["tan"] - 0.6, 2)        # ate 0,6 mm dentro da face externa da borda
    s["W_rasgo"] = s["tab_w"] + 2 * s["folga_tab"]
    # o pe empilhado apoia na espessura da parede cortada: sobra tab_L - (Hw*tan - e)
    s["apoio_tab"] = round(s["tab_L"] - (Hw * s["tan"] - s["e"]), 2)
    assert s["apoio_tab"] > 0.8, "lingueta nao alcanca a parede da borda"
    return s


def construir(p=P):
    s = parametros(p)
    e, ef, Hw, tan = s["e"], s["ef"], s["Hw"], s["tan"]
    cont = Contorno(s["Xb"], s["Yb"], s["Rb"], tan, passo=AMOSTRA[0], n_arco=int(AMOSTRA[1]))
    n = cont.n
    m = Malha()

    # ---- posicoes: pes em S, rasgos em R(S), alinhados as amostras ---------
    inicio = {}
    for i, (tr, _) in enumerate(cont.amostras):
        inicio.setdefault(tr, i)
    ordem = ["lat_d", "canto_fd", "frente", "canto_fe", "lat_e", "canto_te", "traseira", "canto_td"]
    fim = {tr: inicio[ordem[(q + 1) % 8]] if q < 7 else n for q, tr in enumerate(ordem)}
    W_r = s["W_rasgo"]
    n_amostras_rasgo = max(2, int(round(W_r / AMOSTRA[0])))
    s["W_rasgo"] = W_r = n_amostras_rasgo * (cont.s[inicio["lat_d"] + 1] - cont.s[inicio["lat_d"]])

    def coord(i):
        x, y, _, _ = cont.ponto(i % n, 0.0)
        return (x, y)

    def amostras_em(tr, alvo, eixo):
        """indices [i0, i0+n_amostras_rasgo] do trecho reto cujo centro em
        'eixo' (0=x, 1=y) fica mais perto de alvo."""
        idx = list(range(inicio[tr], fim[tr]))
        melhor = None
        for k in range(len(idx) - n_amostras_rasgo):
            c = 0.5 * (coord(idx[k])[eixo] + coord(idx[k + n_amostras_rasgo])[eixo])
            if melhor is None or abs(c - alvo) < abs(melhor[1] - alvo):
                melhor = (k, c)
        k, c = melhor
        return idx[k], idx[k] + n_amostras_rasgo, c

    y_f_alvo = s["by"] - 9.0                  # pe da frente: junto ao canto, na lateral
    x_b_alvo = s["ax"] - 24.0                 # pe de tras: na traseira
    aberturas = []                            # (i0, i1, z_fundo, tipo, trecho, coord_centro)
    pes = []                                  # (x, y, direcao) do centro do pe
    # entalhes (S): lat_d y=+y_f, lat_e y=+y_f, traseira x=+x_b e x=-x_b
    for tr in ("lat_d", "lat_e"):
        i0, i1, c = amostras_em(tr, y_f_alvo, 1)
        aberturas.append((i0, i1, s["z_seat"], "entalhe", tr, c))
        pes.append((math.copysign(s["Xb"] / 2, 1 if tr == "lat_d" else -1), c, "x"))
        j0, j1, c2 = amostras_em(tr, -y_f_alvo, 1)
        aberturas.append((j0, j1, s["z_sola2"], "rasgo", tr, c2))
    for xa in (x_b_alvo, -x_b_alvo):
        i0, i1, c = amostras_em("traseira", xa, 0)
        aberturas.append((i0, i1, s["z_seat"], "entalhe", "traseira", c))
        pes.append((c, -s["Yb"] / 2, "y"))
    s["pes"], s["aberturas"] = pes, aberturas
    s["y_f"] = [a[5] for a in aberturas if a[3] == "entalhe" and a[4] == "lat_d"][0]
    s["x_b"] = abs([a[5] for a in aberturas if a[4] == "traseira"][0])
    em_abertura = {}
    for (i0, i1, zf, tipo, tr, c) in aberturas:
        for i in range(i0, i1):
            em_abertura[i] = zf
    s["em_abertura"] = em_abertura

    # ---- perfil da frente (vao com mergulho entre cantos altos) ------------
    def perfil_frente(x):
        xL, xR = -s["x_cheia"], s["x_cheia"]
        if xL <= x <= xR:
            ramp = RAMPA_FRENTE
            d = min(x - xL, xR - x)
            f = suave(d / ramp) if d < ramp else 1.0
            g = 0.5 * (1 - math.cos(2 * math.pi * (x - xL) / (xR - xL)))
            return Hw - f * ((Hw - s["hf"]) + s["mergulho"] * g)
        return Hw

    def ztopo(i):
        tr, _ = cont.amostras[i % n]
        if tr == "frente":
            return perfil_frente(cont.ponto(i % n, Hw)[0])
        return Hw
    s["fn_ztopo"] = ztopo
    s["fn_perfil_frente"] = perfil_frente

    OE = lambda i, z: 0.0
    OI = lambda i, z: -e

    # ---- bolinhas em gradiente de escala, por face reta --------------------
    z_g0, z_g1 = s["hb"], Hw - s["h_aro"]
    faces = []
    for tr in ("lat_d", "lat_e", "traseira"):
        i0, i1 = inicio[tr], fim[tr]
        p0, p1 = cont.ponto(i0, 0.0), cont.ponto(i1 % n, 0.0)
        eixo = 1 if tr != "traseira" else 0
        proib = []
        for (a0, a1, zf, tipo, trr, c) in aberturas:
            if trr == tr and zf < z_g1:               # o rasgo entra na faixa das bolinhas
                proib.append((c - W_r / 2, c + W_r / 2))
        faces.append(dict(s_a=cont.s[i0], s_b=cont.s[i1] if i1 < n else cont.perimetro,
                          c0=p0[eixo], c1=p1[eixo], cresce=tan, zlo=z_g0, zhi=z_g1,
                          proibido=proib, nome=tr))
    d_max, d_min, alma = s["dots"]
    bol = G.BolinhasEscala(faces, d_max, d_min, alma)
    s.update({"graf_" + q: v for q, v in bol.medidas().items()})

    def furo(sarc, z):
        return bol.dentro(sarc % cont.perimetro, z)

    def cheio(i):
        return cont.amostras[i % n][0] == "frente"

    # ---- a parede: fora das aberturas inteira; nas aberturas so ate o fundo delas
    livres = [i for i in range(n) if i not in em_abertura]
    banda(m, cont, 0, 0, OE, OI, lambda i: 0.0, lambda i: 0.0, "faixa")
    # faixa cheia do pe, casca de bolinhas, faixa do aro — por tira, respeitando aberturas
    def z_ate_par(i):
        return ztopo(i)
    perfurada(m, cont, OE, OI, lambda i: 0.0, lambda i: s["hb"], lambda s_, z: False, "faixa",
              tiras=livres)
    perfurada(m, cont, OE, OI, lambda i: s["hb"], lambda i: max(s["hb"], ztopo(i) - s["h_aro"]),
              furo, "ripa", cheio=cheio, tiras=livres)
    perfurada(m, cont, OE, OI, lambda i: max(s["hb"], ztopo(i) - s["h_aro"]), ztopo, lambda s_, z: False,
              "aro", tiras=livres)
    for (i0, i1, zf, tipo, tr, c) in aberturas:
        tiras = list(range(i0, i1))
        perfurada(m, cont, OE, OI, lambda i: 0.0, lambda i: min(s["hb"], zf), lambda s_, z: False,
                  "faixa", tiras=tiras)
        if zf > s["hb"]:
            perfurada(m, cont, OE, OI, lambda i: s["hb"], lambda i: min(zf, Hw - s["h_aro"]), furo,
                      "ripa", tiras=tiras)
            if zf > Hw - s["h_aro"]:
                perfurada(m, cont, OE, OI, lambda i: Hw - s["h_aro"], lambda i: zf,
                          lambda s_, z: False, "aro", tiras=tiras)
        # tampas laterais da abertura (a espessura da parede, do fundo do rasgo ate a borda)
        for ii, ordem_ in ((i0, 1), (i1, -1)):
            A0 = cont.pt(ii, zf, 0.0); A1 = cont.pt(ii, Hw, 0.0)
            a0 = cont.pt(ii, zf, -e); a1 = cont.pt(ii, Hw, -e)
            q = [(A0[0], A0[1], zf), (A1[0], A1[1], Hw), (a1[0], a1[1], Hw), (a0[0], a0[1], zf)]
            if ordem_ > 0:
                m.quad(q[0], q[1], q[2], q[3], "aro")
            else:
                m.quad(q[0], q[3], q[2], q[1], "aro")

    # ---- aro em L: aba (placa) + saia, so onde a borda esta alta ------------
    A, ta, sh = s["aba"], s["t_aba"], s["saia"]
    com_aro = lambda i: min(ztopo(i), ztopo(i + 1)) >= Hw - 0.5
    o_corte = -0.3                                   # a lingueta para 0,3 antes da face externa

    def emitir(quer, o_ext, o_int, zde, zate, tag):
        marcas = [quer(i) for i in range(n)]
        ini = next((i for i in range(n) if not marcas[i]), None)
        if ini is None:
            banda(m, cont, 0, n, o_ext, o_int, zde, zate, tag, tampa_ini=False, tampa_fim=False)
            return
        i = 0
        while i < n:
            if not marcas[(ini + i) % n]:
                i += 1; continue
            j = i
            while j < n and marcas[(ini + j) % n]:
                j += 1
            banda(m, cont, ini + i, ini + j, o_ext, o_int, zde, zate, tag)
            i = j
    # placa da aba: faixa interna (sobre a parede) recortada nas aberturas; faixa externa inteira
    emitir(lambda i: com_aro(i) and (i % n) not in em_abertura, lambda i, z: o_corte, lambda i, z: -e,
           lambda i: Hw - ta, lambda i: Hw, "aro")
    emitir(com_aro, lambda i, z: A, lambda i, z: o_corte, lambda i: Hw - ta, lambda i: Hw, "aro")
    # saia (com as femeas do acoplador recortadas)
    ac_h, ac_c, ac_f = s["ac"]
    n_ac = max(2, int(round((ac_h + 2 * ac_f) / AMOSTRA[0])))
    femeas, machos = [], []
    for tr, y_m, y_fe in (("lat_d", 45.0, -45.0), ("lat_e", -45.0, 45.0)):
        i0, i1, c = amostras_em(tr, y_fe, 1)
        # a femea usa n_ac amostras
        i1 = i0 + n_ac
        femeas.append((i0, i1, tr, 0.5 * (coord(i0)[1] + coord(i1)[1])))
        machos.append((tr, y_m))
    em_femea = {i for (i0, i1, tr, c) in femeas for i in range(i0, i1)}
    emitir(lambda i: com_aro(i) and (i % n) not in em_femea, lambda i, z: A, lambda i, z: A - e,
           lambda i: Hw - sh, lambda i: Hw - ta, "saia")
    # bolsao da femea: paredes laterais e fundo, atras da saia, sob a aba
    prof = round((s["e"] + 0.4) - e + max(1.8, e) + 0.4, 2)          # cabeca dentro com folga
    s["ac_prof_bolsao"] = prof
    for (i0, i1, tr, c) in femeas:
        sgn = 1 if tr == "lat_d" else -1
        x_out = sgn * (s["Xb"] / 2 + Hw * tan + A - e)                # face interna da saia
        x_in = sgn * (s["Xb"] / 2 + Hw * tan + A - e - prof - 1.6)
        ya, yb = sorted((coord(i0)[1], coord(i1)[1]))
        z0, z1 = Hw - sh, Hw - ta
        for (u0, u1) in ((ya - 1.6, ya), (yb, yb + 1.6)):
            m.bloco(min(x_in, x_out), max(x_in, x_out), u0, u1, z0, z1, "saia")
        xf0, xf1 = sorted((x_in, x_in + sgn * 1.6))
        m.bloco(xf0, xf1, ya - 1.6, yb + 1.6, z0, z1, "saia")
        m.bloco(min(x_in, x_out), max(x_in, x_out), ya - 1.6, yb + 1.6, z0 - 0.0, z0 + 1.2, "saia")  # fundo do bolsao
    # macho em T, na face externa da saia
    hastes = s["e"] + 0.4
    cab = max(1.8, e)
    for (tr, y_m) in machos:
        sgn = 1 if tr == "lat_d" else -1
        x0 = sgn * (s["Xb"] / 2 + Hw * tan + A)
        z0, z1 = Hw - sh + 0.6, Hw - 2.8
        xs0, xs1 = sorted((x0, x0 + sgn * hastes))
        m.bloco(xs0, xs1, y_m - ac_h / 2, y_m + ac_h / 2, z0, z1, "saia")
        xc0, xc1 = sorted((x0 + sgn * hastes, x0 + sgn * (hastes + cab)))
        m.bloco(xc0, xc1, y_m - ac_c / 2, y_m + ac_c / 2, z0, z1, "saia")
    s["machos"], s["femeas"] = machos, [(c, tr) for (i0, i1, tr, c) in femeas]

    # ---- fundo chapado + rodape + nervuras -----------------------------------
    pts = [cont.pt(i, 0.0, -e + 0.2) for i in range(n)]
    cx = sum(q[0] for q in pts) / n; cy = sum(q[1] for q in pts) / n
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        m.tri((cx, cy, ef), (a[0], a[1], ef), (b[0], b[1], ef), "fundo")
        m.tri((cx, cy, 0.0), (b[0], b[1], 0.0), (a[0], a[1], 0.0), "fundo")
    banda(m, cont, 0, n, lambda i, z: -s["recuo"], lambda i, z: -s["recuo"] - e,
          lambda i: -s["rodape"], lambda i: 0.0, "rodape", tampa_ini=False, tampa_fim=False)
    for xr in (-s["Xb"] / 6, s["Xb"] / 6):
        m.bloco(xr - 0.8, xr + 0.8, -s["Yb"] / 2 + s["recuo"] + e, s["Yb"] / 2 - s["recuo"] - e, -4.0, 0.0, "rodape")
    m.bloco(-s["Xb"] / 2 + s["recuo"] + e, s["Xb"] / 2 - s["recuo"] - e, -0.8, 0.8, -4.0, 0.0, "rodape")

    # ---- os quatro pes com lingueta ------------------------------------------
    hp, pl, pp_, tw, L = s["h_pe"], s["pe_larg"], s["pe_prof"], s["tab_w"], s["tab_L"]
    for (px, py, dirc) in pes:
        if dirc == "x":
            sgn = 1 if px > 0 else -1
            xa, xb_ = sorted((px, px - sgn * pp_))
            m.bloco(xa, xb_, py - pl / 2, py + pl / 2, -hp, 0.0, "pe")
            xa, xb_ = sorted((px, px + sgn * L))
            m.bloco(xa, xb_, py - tw / 2, py + tw / 2, -hp, 0.0, "pe")
        else:
            sgn = 1 if py > 0 else -1
            ya, yb_ = sorted((py, py - sgn * pp_))
            m.bloco(px - pl / 2, px + pl / 2, ya, yb_, -hp, 0.0, "pe")
            ya, yb_ = sorted((py, py + sgn * L))
            m.bloco(px - tw / 2, px + tw / 2, ya, yb_, -hp, 0.0, "pe")

    s["n_triangulos"] = len(m.tris)
    s["cont"] = cont
    return m, s


# ============================================================================
# CONFERENCIAS: a peca de cima contra a peca de baixo, ao longo da descida
# ============================================================================
def _sdf(s, x, y, z):
    """Distancia com sinal a face EXTERNA da parede da peca de baixo na cota z
    (>0 fora)."""
    d = z * s["tan"]
    hx, hy, r = s["Xb"] / 2 + d, s["Yb"] / 2 + d, s["Rb"]
    qx, qy = abs(x) - (hx - r), abs(y) - (hy - r)
    if qx > 0 and qy > 0:
        return math.hypot(qx, qy) - r
    return max(qx, qy) - r


def _em_abertura(s, x, y, z):
    """(x,y,z) esta num rasgo/entalhe ou acima do perfil da frente da peca de baixo?"""
    W = s["W_rasgo"] / 2 + 0.05
    for (i0, i1, zf, tipo, tr, c) in s["aberturas"]:
        if z < zf - 0.05:
            continue
        if tr == "lat_d" and x > 0 and abs(y - c) <= W:
            return True
        if tr == "lat_e" and x < 0 and abs(y - c) <= W:
            return True
        if tr == "traseira" and y < 0 and abs(x - c) <= W:
            return True
    if y > 0 and abs(x) < s["ax"] and z > s["fn_perfil_frente"](x) + 0.05:
        return True
    return False


def confere_descida(m, s, giro, d_final, passo=1.0):
    """Peca de cima (girada ou nao) descendo ate a sola ficar em d_final.
    Devolve (pior_n_violacoes, cota_da_sola, exemplo)."""
    e, Hw, A = s["e"], s["Hw"], s["aba"]
    verts = set()
    for a, b, c, t in m.tris:
        for p_ in (a, b, c):
            verts.add((round(p_[0], 2), round(p_[1], 2), round(p_[2], 2)))
    pior = (0, None, None)
    sola = Hw + 0.5
    while sola >= d_final - 1e-6:
        nb, ex = 0, None
        for (x, y, z) in verts:
            zz = z + s["h_pe"] + sola                     # cota na peca de baixo
            if zz < -0.01 or zz > Hw + 0.01:
                continue
            xg, yg = (-x, -y) if giro else (x, y)
            o = _sdf(s, xg, yg, min(zz, Hw))
            viol = False
            if -e - 0.05 <= o <= 0.05:                   # dentro da casca da parede
                viol = not _em_abertura(s, xg, yg, zz)
            if zz >= Hw - s["t_aba"] - 0.05 and -e - 0.05 <= o <= A + 0.05:
                viol = viol or not (_em_abertura(s, xg, yg, zz) and o <= -0.3 + 0.05)
            if zz <= s["ef"] + 0.05 and o < -e:
                viol = True
            if viol:
                nb += 1
                if ex is None:
                    ex = (round(xg, 1), round(yg, 1), round(zz, 1), round(o, 2))
        if nb > pior[0]:
            pior = (nb, round(sola, 1), ex)
        sola -= passo
    return pior


def ficha(p=P):
    m, s = construir(p)
    s["volume_material_cm3"] = v = m.volume()
    s["massa_g"] = v * RHO_PP
    # capacidade: area interna integrada ate a borda (parede) e ate a frente (hf)
    def area(z):
        W = s["Xb"] + 2 * z * s["tan"] - 2 * s["e"]
        D = s["Yb"] + 2 * z * s["tan"] - 2 * s["e"]
        r = max(0.0, s["Rb"] - s["e"])
        return W * D - (4 - math.pi) * r * r
    nn = 200
    s["litros_total"] = sum(area(s["ef"] + (s["Hw"] - s["ef"]) * (k + .5) / nn) for k in range(nn)) * (s["Hw"] - s["ef"]) / nn / 1e6
    s["litros_frente"] = sum(area(s["ef"] + (s["hf"] - s["mergulho"] - s["ef"]) * (k + .5) / nn) for k in range(nn)) * (s["hf"] - s["mergulho"] - s["ef"]) / nn / 1e6
    # descida da peca 2 (girada) ate o passo de ninho; da peca 3 (nao girada) ate o entalhe
    s["viol_ninho2"] = confere_descida(m, s, True, s["z_sola2"])
    s["viol_ninho3"] = confere_descida(m, s, False, s["z_seat"])
    assert s["viol_ninho2"][0] == 0, f"peca 2 (girada) colide na descida: {s['viol_ninho2']}"
    assert s["viol_ninho3"][0] == 0, f"peca 3 / pilha colide na descida: {s['viol_ninho3']}"
    return m, s


if __name__ == "__main__":
    m, s = ficha()
    print(f"{s['nome']} rev.28  {s['X']:.0f}x{s['Y']:.0f}x{s['H']:.0f}  parede {s['e']} mm  saida {s['saida']} graus")
    print(f"  base {s['Xb']:.1f} x {s['Yb']:.1f}  |  {s['massa_g']:.0f} g  |  {s['litros_total']:.1f} L (ate a frente {s['litros_frente']:.1f} L)")
    print(f"  pilha {s['passo_pilha']:.1f}  ninho {s['passo_ninho']:.1f} (folga parede {s['folga_ninho']:.2f})  10 pecas ninhadas {s['H'] + 9*s['passo_ninho']:.0f} mm")
    print(f"  lingueta {s['tab_w']} x {s['tab_L']} mm, apoio {s['apoio_tab']} mm; rasgo {s['W_rasgo']:.1f} mm; pes y_f={s['y_f']:.1f} x_b={s['x_b']:.1f}")
    print(f"  bolinhas: {s['graf_colunas']} furos, {s['graf_fileiras']} fileiras, d {s['graf_largura']}->{s['graf_alt_longo']}, vazado {s['graf_vazado']*100:.0f}%")
    print(f"  descida peca 2: {s['viol_ninho2']}   peca 3: {s['viol_ninho3']}   {s['n_triangulos']} tri")
