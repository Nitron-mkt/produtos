"""
MODULA rev.18 — familia de organizadores modulares Nitron (3 moldes).

FORMA
  Planta de cantos arredondados; nenhuma quina viva. Parede vazada com o
  grafismo da marca. Aro em perfil L (aba + saia) que e viga, apoio e pega ao
  mesmo tempo. Fundo em grelha diagonal de nervuras altas, sobre um vao de
  50 mm (a perna), fechado por um rodape recuado e quatro pes de canto.

MECANICA (rev.09 + rev.18)
  Pilha (0 graus): o rodape da peca de cima pousa num CANAL no topo de quatro
  colunas internas, entre o labio da coluna e uma guia chanfrada.
  Ninho (180 graus): a janela do rodape deixa a coluna passar; a parede desce
  rente a parede de baixo (passo = espessura / tan(saida) + folga); e os pes,
  que sao COPOS abertos para cima, entram nos copos da peca de baixo — pela
  mesma conta, com a mesma folga.

  O copo e o que fez a rev.18. Antes o pe era uma casca fechada por fora e
  aberta para o vao: (a) no ninho ele atravessava o fundo da peca de baixo
  (o passo real era 54,5 mm, nao 17); (b) o vao sob o fundo afunilava para
  baixo — contra-saida de 6,6 mm no postico da cavidade. O copo resolve os
  dois: sua face externa sai pela cavidade, a interna pelo macho (atraves do
  recorte do canto no fundo), e o vao entre os copos e formado por um
  postico que alarga para baixo, porque as paredes do copo inclinam para o
  canto conforme descem.

REGRA QUE GOVERNA TUDO
  Toda superficie que desliza no ninho tem os mesmos 7,5 graus: parede,
  face externa do copo, paredes internas do copo. E a PAREDE E LISA POR
  FORA — nenhum relevo, senao o ninho trava a meio caminho.
"""
import math
from geometria import DEG, Contorno, Malha, banda, perfurada
import grafismo as G

AMOSTRA = [2.6, 14]      # passo de amostragem do contorno / pontos por canto
SAIDA_GR = 7.5
TAN = math.tan(SAIDA_GR * DEG)
T05 = math.tan(0.5 * DEG)         # saida minima de face "vertical"
T1 = math.tan(1.0 * DEG)          # saida de nervura e de face de postico
RHO_PP = 0.905

# X, Y = cota EXTERNA no aro. Modulo de palete menos 4 mm (396 x 296 cabe 12x
# em 1000 x 1200 com folga; 400 x 300 exatos nao cabem).
# barra = largura da nervura do fundo (= espessura da parede); vao_fundo = furo.
# O P e o mais fechado de proposito: e a peca que vai a vista em casa e a que
# guarda coisa pequena. O G e o mais aberto: e caixa de estoque.
TAMANHOS = {
    # H = altura TOTAL (chao ate o aro). A cesta e H - perna.
    "P": dict(nome="MODULA P", X=296.0, Y=196.0, H=185.0, perna=50.0, e=1.8, R=26.0,
              barra=1.8, vao_fundo=9.0, graf_esc=0.135, graf_ku=0.80, graf_kz=0.65, graf_eixo_gr=-55.0),
    "M": dict(nome="MODULA M", X=396.0, Y=296.0, H=245.0, perna=50.0, e=2.0, R=36.0,
              barra=2.0, vao_fundo=18.0, graf_esc=0.110, graf_ku=0.80, graf_kz=0.65, graf_eixo_gr=-55.0),
    "G": dict(nome="MODULA G", X=596.0, Y=396.0, H=370.0, perna=50.0, e=2.5, R=46.0,
              barra=2.5, vao_fundo=22.0, graf_esc=0.110, graf_ku=0.80, graf_kz=0.65, graf_eixo_gr=-55.0),
}

CANTOS = {"canto_fd": (1, 1), "canto_fe": (-1, 1), "canto_te": (-1, -1), "canto_td": (1, -1)}


def suave(t):
    return t * t * (3 - 2 * t)


def parametros(k):
    s = dict(TAMANHOS[k])
    X, Y, e, R = s["X"], s["Y"], s["e"], s["R"]
    s["H_total"] = s["H"]
    s["hc"] = H = s["H"] - s["perna"]          # altura da cesta
    s["conic"] = con = H * TAN
    s["aba"] = aba = round(8.0 + 0.006 * X, 1)
    s["passo_ninho"] = pn = round(e / TAN + 2.0, 1)
    s["saia"] = round(pn - 4.0, 1)                # a saia tem de caber no passo
    s["aro_ext"] = X / 2                          # face externa do aro
    s["Xt"] = X - 2 * aba                         # parede no topo
    s["Yt"] = Y - 2 * aba
    s["Xb"], s["Yb"] = s["Xt"] - 2 * con, s["Yt"] - 2 * con
    s["Rt"] = s["Rb"] = R - aba                   # raio constante em toda a altura
    s["hf"] = round(0.40 * H)
    s["mergulho"] = round(0.28 * s["hf"])
    s["hb"] = round(16.0 + 0.055 * H)             # faixa cheia junto ao fundo
    s["h_aro"] = round(8.0 + 0.030 * H)           # parede cheia sob o aro
    # rev.18: o fundo assenta no plano do rodape (era 2 mm acima, e a base
    # ficava SOLTA do corpo — nada ligava as duas cascas).
    s["z_fundo"] = 0.0
    s["ef"] = e + 0.5
    s["sal_pe"] = 0.0                             # o pe nao sai do vulto
    s["b"] = s["Yt"] / 2 - s["Rt"]                # meio trecho reto da lateral (no topo)
    s["ax"] = s["Xt"] / 2 - s["Rt"]
    s["etiqueta"] = round(0.24 * X)
    s["graf_L"] = round(s["graf_esc"] * X, 1)
    s["graf_giro"] = round(s["graf_eixo_gr"] - G.ANG_EIXO, 2)

    # ---- base: rodape recuado, copos de canto, vao com saida ---------------
    s["recuo"] = rec = round(e + 3.2, 1)          # recuo do rodape (linha de sombra)
    # o rodape passa raspando o fundo da peca de baixo no ninho
    s["h_rodape"] = hro = round(min(0.22 * s["perna"], pn - s["z_fundo"] - s["ef"] - 1.5), 1)
    s["h_copo"] = hcp = round(s["perna"] - hro, 1)      # altura livre do copo
    # A parede interna do copo e a unica peca que NAO pode engrossar: no ninho
    # ela desce dentro do bolsao de baixo, e so cabe se for <= passo*tan - 0,26
    # = e. Um mm a mais e colisao (o teste de ninho pegou isso na primeira build).
    s["e_copo"] = ec = e
    s["colar"] = 1.5                                    # reforco so na laje do fundo
    # nervura do fundo: alta e afunilada, pendurada no vao. No ninho a ponta
    # dela para acima do fundo da peca de baixo.
    s["alt_nerv"] = round(min(pn - 1.5, 8.0 + 0.006 * X), 1)
    s["larg_nerv"] = s["barra"]
    s["w_mold"] = round(9.0 + 0.010 * X, 1)             # moldura do fundo

    # ---- coluna interna: o que trava o empilhamento (rev.09) --------------
    # Quatro colunas por dentro da parede, do fundo ate o aro. A face interna
    # tem 0,5 grau de saida (rev.18; era vertical). O topo e um CANAL onde o
    # rodape da peca de cima pousa: labio da coluna por dentro, guia chanfrada
    # por fora. rev.18 tambem recuou as colunas de 0,72b/0,24b para
    # 0,66b/0,22b, para o copo do P caber entre a janela e o canto.
    s["y_col"] = (round(0.66 * s["b"], 1), round(-0.22 * s["b"], 1))
    s["w_col"] = round(0.17 * s["b"], 1)
    s["rampa_col"] = round(min(5.5, 0.055 * s["b"]), 1)
    vao_col = 0.44 * s["b"]
    assert s["w_col"] + 2 * s["rampa_col"] + 6 < vao_col, \
        f"{k}: coluna e janela se encostam ({vao_col:.0f} mm de vao)"
    # faces do rodape na sua aresta de baixo (meia-largura absoluta - Xb/2):
    # face externa afina 0,5 grau para baixo (cavidade), interna alarga 1 grau
    # para baixo (postico do vao). Ficou quase vertical, e por isso sobra
    # 1,3 mm proud em relacao ao copo: a linha de gota do rodape.
    s["ro_out_b"] = ro_out_b = round(-rec - hro * T05, 2)
    s["ro_in_b"] = ro_in_b = round(-rec - e + hro * T1, 2)
    s["tol_pilha_in"] = tin = 3.0                  # folga para dentro no canal
    s["tol_pilha_out"] = tout = 1.0                # folga para fora, ate a guia
    s["prof_canal"] = 3.0
    s["r_col_top"] = s["Xb"] / 2 + ro_in_b - tin          # labio da coluna, no aro
    s["r_col_b"] = round(s["r_col_top"] - H * T05, 2)     # face interna, no fundo
    s["r_col"] = s["r_col_b"]
    s["canal_out_abs"] = s["Xb"] / 2 + ro_out_b + tout    # face interna da guia
    s["larg_canal"] = round(s["canal_out_abs"] - s["r_col_top"], 1)
    # a ponte fecha o bolsao atras da coluna ate 1,5 mm da parede de cima no
    # ninho: e o que faz o degrau ter 25 mm em vez de 2.
    s["ponte_out_rel"] = round(-pn * TAN - e - 1.5, 2)    # offset ao contorno, cte em z
    s["larg_ponte"] = round((s["Xb"] / 2 + H * TAN + s["ponte_out_rel"]) - s["r_col_top"], 1)
    assert s["larg_ponte"] > s["larg_canal"] + 4.0, f"{k}: nao sobra guia na ponte"
    s["passo_pilha"] = round(H + hro - s["prof_canal"], 1)

    def r_col(z):
        return s["r_col_b"] + z * T05
    s["fn_r_col"] = r_col

    # ---- o copo de canto, dimensionado pela janela -------------------------
    # meia-corda do pe no chao, medida no contorno a partir do centro do canto.
    # A parede interna do copo inclina 7,5 graus, entao a corda cresce TAN por
    # mm subindo: no rodape e hw + h_copo*TAN, e isso tem de parar 4 mm antes
    # da janela.
    s["arco_canto"] = ac = math.pi * s["Rb"] / 4
    dist_jan = 0.34 * s["b"] + ac - (s["w_col"] / 2 + s["rampa_col"])
    s["hw_pe"] = hw = round(min(0.30 * min(s["b"], s["ax"]), dist_jan - 4.0 - hcp * TAN), 1)
    assert hw > 0.15 * min(s["b"], s["ax"]), f"{k}: pe estreito demais ({2*hw:.0f} mm)"
    assert hw > ac + 3.0, f"{k}: o copo nao alcanca a reta ({hw:.1f} vs arco {ac:.1f})"
    s["hw_topo"] = round(hw + hcp * TAN, 1)
    s["larg_pe"] = round(2 * hw, 1)
    # paredes internas do copo (face do lado do bolsao), no chao (z = -perna):
    zc = -s["perna"]
    s["y_wf"] = (s["Yb"] / 2 + zc * TAN - s["Rb"]) - (hw - ac)
    s["x_wf"] = (s["Xb"] / 2 + zc * TAN - s["Rb"]) - (hw - ac)

    def x_w(z):
        return s["x_wf"] - (z + s["perna"]) * TAN

    def y_w(z):
        return s["y_wf"] - (z + s["perna"]) * TAN
    s["fn_x_w"], s["fn_y_w"] = x_w, y_w

    # ---- folgas do ninho e da pilha (asserts: a build quebra se violar) ----
    zt = s["z_fundo"] + s["ef"]                    # topo do fundo
    # (1) parede de cima x coluna de baixo, na cota mais apertada (z = pn)
    s["f_par"] = f_par = round((s["Xb"] / 2 - e) - (r_col(pn) + e), 2)
    assert f_par > 1.5, f"{k}: a parede do ninho raspa na coluna ({f_par:.1f} mm)"
    # (2) rodape de cima x fundo de baixo
    s["f_fun"] = f_fun = round(pn - (zt + hro), 2)
    assert f_fun > 0.8, f"{k}: rodape bate no fundo no ninho ({f_fun:.1f} mm)"
    # (3) nervura de cima x fundo de baixo
    s["f_nerv"] = f_nerv = round(pn - s["alt_nerv"], 2)
    assert f_nerv > 0.8, f"{k}: nervura bate no fundo no ninho ({f_nerv:.1f} mm)"
    # (4) fundo do copo de cima x sola do copo de baixo
    s["f_copo"] = f_copo = round(pn - s["ef"], 2)
    assert f_copo > 0.8, f"{k}: copo bate na sola no ninho ({f_copo:.1f} mm)"
    # (5) moldura/nervura de cima x coluna de baixo (na janela)
    hx_led = s["Xb"] / 2 + s["z_fundo"] * TAN - e - s["w_mold"]
    s["f_gre"] = f_gre = round(r_col(pn) - hx_led, 2)
    assert f_gre > 1.5, f"{k}: a grelha alcanca a coluna no ninho ({f_gre:.1f} mm)"
    # (6) a copo de cima entra no de baixo com a folga do passo (por construcao)
    s["f_copo_par"] = round(pn * TAN - ec + (ec - e), 2)   # = pn*TAN - e
    s["folga_degrau"] = round(min(f_par, f_gre), 1)
    return s


def em_copo(s, x, y, z, folga=0.0):
    """O ponto (x, y) esta dentro de um dos quatro bolsoes do copo na cota z
    (coordenadas da cesta: z = 0 no plano do rodape)? 'folga' aperta o teste."""
    ax_, ay_ = abs(x), abs(y)
    if not (ax_ > s["fn_x_w"](z) + folga and ay_ > s["fn_y_w"](z) + folga):
        return False
    hx = s["Xb"] / 2 + z * TAN - s["recuo"] - s["e"]     # face interna da casca do copo
    hy = s["Yb"] / 2 + z * TAN - s["recuo"] - s["e"]
    r = s["Rb"] - s["recuo"] - s["e"]
    if ax_ > hx - folga or ay_ > hy - folga:
        return False
    dx, dy = ax_ - (hx - r), ay_ - (hy - r)
    if dx > 0 and dy > 0 and math.hypot(dx, dy) > r - folga:
        return False
    return True


def grafismo(s, cont, zlo, zhi):
    """A trama da marca: o elemento oficial nos dois passos do simbolo."""
    tr, info = G.monta(s["graf_L"], cont.perimetro, zlo, zhi,
                       s["graf_ku"], s["graf_kz"], s["graf_giro"])
    s.update({"graf_" + q: v for q, v in info.items() if q != "L"})
    assert s["graf_alma"] > 4.0, \
        f"alma do grafismo fina demais ({s['graf_alma']:.1f} mm)"
    return tr


def construir(k):
    s = parametros(k)
    X, Y, e = s["X"], s["Y"], s["e"]
    H = s["hc"]                    # dentro daqui, H e a altura da CESTA
    aba, hf, hb, h_aro = s["aba"], s["hf"], s["hb"], s["h_aro"]
    cont = Contorno(s["Xb"], s["Yb"], s["Rb"], TAN,
                    passo=AMOSTRA[0], n_arco=int(AMOSTRA[1]))
    m = Malha()
    n = cont.n
    perna, hro, rec, ec = s["perna"], s["h_rodape"], s["recuo"], s["e_copo"]
    zf, ef = s["z_fundo"], s["ef"]
    zt = zf + ef                                   # topo do fundo
    x_w, y_w, r_col = s["fn_x_w"], s["fn_y_w"], s["fn_r_col"]

    # ---- perfil do aro: continuo em toda a volta --------------------------
    h_geral = H

    def ztopo(i):
        tr, t = cont.amostras[i % n]
        if tr == "canto_fd":
            return h_geral - (h_geral - hf) * suave(t)
        if tr == "canto_fe":
            return hf + (h_geral - hf) * suave(t)
        if tr == "frente":
            return hf - s["mergulho"] * 0.5 * (1 - math.cos(2 * math.pi * t))
        return h_geral

    # ---- coluna interna e janela do rodape --------------------------------
    yc_col = s["y_col"]
    yc_jan = tuple(-y for y in yc_col)          # espelho: por onde a coluna passa
    wc, rc = s["w_col"] / 2, s["rampa_col"]

    def perfil(i, alvos):
        """1 no centro do recurso, 0 fora dele, com rampa suave."""
        tr, _ = cont.amostras[i % n]
        if tr not in ("lat_d", "lat_e"):
            return 0.0
        y = cont.y_de(i % n)
        f = 0.0
        for yc in alvos:
            d = abs(y - yc)
            if d <= wc:
                f = 1.0
            elif d <= wc + rc:
                f = max(f, 1 - suave((d - wc) / rc))
        return f

    fcol = [perfil(i, yc_col) for i in range(n)]
    fjan = [perfil(i, yc_jan) for i in range(n)]

    def o_col(z):
        """Deslocamento que poe a face interna da coluna no raio r_col(z)."""
        return r_col(z) - (s["Xb"] / 2 + z * TAN)

    def OE(i, z):                                # face externa da casca
        f = fcol[i % n]
        return 0.0 if f <= 0 else f * (o_col(z) + e)

    def OI(i, z):                                # face interna da casca
        f = fcol[i % n]
        return -e if f <= 0 else (1 - f) * (-e) + f * o_col(z)

    # ---- o vazado: o grao da marca, deitado (rev.10) ----------------------
    z_g0 = hb
    z_g1 = h_geral - h_aro
    gra = grafismo(s, cont, z_g0, z_g1)

    def furo(sarc, z):
        return gra.dentro(sarc % cont.perimetro, z)

    def cheio(i):
        """Sem furo na coluna (e poste de carga) e no painel da etiqueta."""
        if fcol[i % n] > 0.10:
            return True
        tr, _ = cont.amostras[i % n]
        if tr == "frente":
            return abs(cont.ponto(i % n, 0.0)[0]) <= s["etiqueta"] / 2
        return False

    def emitir(quer, o_ext, o_int, zde, zate, tag):
        marcas = [quer(i) for i in range(n)]
        if all(marcas):
            banda(m, cont, 0, n, o_ext, o_int, zde, zate, tag,
                  tampa_ini=False, tampa_fim=False)
            return
        if not any(marcas):
            return
        ini = next(i for i in range(n) if not marcas[i])
        i = 0
        while i < n:
            if not marcas[(ini + i) % n]:
                i += 1
                continue
            j = i
            while j < n and marcas[(ini + j) % n]:
                j += 1
            banda(m, cont, ini + i, ini + j, o_ext, o_int, zde, zate, tag)
            i = j

    # faixa cheia junto ao fundo, casca vazada no meio, faixa cheia sob o aro
    emitir(lambda i: True, OE, OI, lambda i: 0.0, lambda i: hb, "faixa")
    perfurada(m, cont, OE, OI, lambda i: hb,
              lambda i: ztopo(i) - h_aro, furo, "ripa", cheio=cheio)
    emitir(lambda i: True, OE, OI, lambda i: ztopo(i) - h_aro, ztopo, "aro")

    # ---- aro: continuo, fechado, com topo em tres degraus (vira filete) ----
    A, S = aba, s["saia"]
    todos = lambda i: True
    ext = lambda d: (lambda i, z: A - d)
    emitir(todos, ext(2.0), -e, lambda i: ztopo(i) - e - 1.6, lambda i: ztopo(i) - 1.6, "aro")
    emitir(todos, ext(3.2), -e + 1.2, lambda i: ztopo(i) - 1.6, lambda i: ztopo(i) - 0.5, "aro")
    emitir(todos, ext(4.6), -e + 2.6, lambda i: ztopo(i) - 0.5, ztopo, "aro")
    emitir(todos, ext(0.0), A - e,
           lambda i: ztopo(i) - S, lambda i: ztopo(i) - 1.6, "aro")
    emitir(todos, ext(0.0), A - 2.0,
           lambda i: ztopo(i) - 2.6, lambda i: ztopo(i) - 1.4, "aro")

    # ---- ponte, canal e guia no topo da coluna (rev.18) --------------------
    # O bolsao atras da coluna era aberto em cima: o rodape pousava numa
    # aresta de 2 mm ao lado de uma vala de 30. A ponte fecha o bolsao ate
    # 1,5 mm da parede de cima (que passa por ali no ninho). Entre o labio da
    # coluna e a guia fica o canal onde o rodape assenta, 3 mm abaixo do aro.
    pc, ponte_out = s["prof_canal"], s["ponte_out_rel"]
    esp_ponte = 2.5

    def canal_out(z):                            # face interna da guia
        return s["canal_out_abs"] - (s["Xb"] / 2 + z * TAN)

    na_col = lambda i: fcol[i % n] > 0.02
    emitir(na_col, lambda i, z: canal_out(z), lambda i, z: OI(i, z) - 0.6,
           lambda i: ztopo(i) - pc - esp_ponte, lambda i: ztopo(i) - pc, "aro")
    emitir(na_col, lambda i, z: ponte_out,
           lambda i, z: canal_out(z) - 0.6 + max(0.0, z - (ztopo(i) - 2.0)),
           lambda i: ztopo(i) - pc - esp_ponte, ztopo, "aro")

    # ---- base (rev.18): rodape + copos numa so casca recuada ---------------
    # A casca recuada 'rec' corre em toda a volta. Entre os cantos ela e o
    # RODAPE (h_rodape); nos cantos ela desce ate o chao e e a face externa do
    # COPO. A fronteira e onde a parede interna do copo (que inclina 7,5 graus
    # para o canto conforme desce) cruza a casca — por isso o pe alarga TAN
    # por mm subindo, e nasce do rodape sem degrau.
    def no_copo(i, z, o=-rec):
        p = cont.pt(i % n, z, o)
        return abs(p[0]) > x_w(z) and abs(p[1]) > y_w(z)

    def z_base_calc(i):
        if no_copo(i, -perna):
            return -perna
        if not no_copo(i, -hro):
            return -hro
        lo, hi = -perna, -hro                     # lo fora, hi dentro
        for _ in range(24):
            md = (lo + hi) / 2
            if no_copo(i, md):
                hi = md
            else:
                lo = md
        return hi
    z_base = [z_base_calc(i) for i in range(n)]
    e_copo_idx = [z_base[i] < -hro - 0.01 for i in range(n)]
    bolsao_idx = [no_copo(i, zt, -rec - e + 0.3) for i in range(n)]

    def o_ext_base(i, z):
        if z >= 0.0 or z < -hro:
            return -rec
        return -rec + (-z) * (TAN - T05)         # rodape quase vertical (0,5 graus)

    def o_int_base(i, z):
        if e_copo_idx[i % n] or z >= 0.0:
            return -rec - e                      # face do bolsao: saida do macho
        return -rec - e + (-z) * (TAN + T1)      # face do vao: saida do postico

    livre = lambda i: fjan[i % n] < 0.15
    emitir(livre, o_ext_base, o_int_base, lambda i: z_base[i % n], lambda i: zt, "saia")

    # ---- moldura do fundo: inteira fora do copo, so a tira sobre ele -------
    w_mold = s["w_mold"]
    emitir(lambda i: livre(i) and not bolsao_idx[i % n], -e, -e - w_mold,
           lambda i: zf, lambda i: zt, "fundo")
    emitir(lambda i: livre(i) and bolsao_idx[i % n], -e, -rec - e + 0.6,
           lambda i: zf, lambda i: zt, "fundo")

    # ---- paredes internas e sola dos copos ---------------------------------
    def copo(sx, sy):
        def P(x, y):
            return (sx * x, sy * y)

        def hexa(base, topo, tag):
            if sx * sy < 0:
                base, topo = base[::-1], topo[::-1]
            m.hexa(base, topo, tag)
        z0, z1 = -perna, zt
        # parede A: paralela a x, em y = y_w, do canto interno ate a casca
        def quadA(z):
            xs = s["Xb"] / 2 + z * TAN - rec - e + 0.6
            xw, yw = x_w(z), y_w(z)
            return [P(xw - ec, yw - ec), P(xs, yw - ec), P(xs, yw), P(xw - ec, yw)]

        def quadB(z):
            ys = s["Yb"] / 2 + z * TAN - rec - e + 0.6
            xw, yw = x_w(z), y_w(z)
            return [P(xw - ec, yw - ec), P(xw, yw - ec), P(xw, ys), P(xw - ec, ys)]
        hexa([(x, y, z0) for x, y in quadA(z0)], [(x, y, z1) for x, y in quadA(z1)], "pe")
        hexa([(x, y, z0) for x, y in quadB(z0)], [(x, y, z1) for x, y in quadB(z1)], "pe")
        # colar: na laje do fundo (z 0..zt) a parede engrossa 'colar' para o lado
        # do vao, para a moldura e a nervura sempre encontrarem material. Essa
        # faixa nunca entra no bolsao da peca de baixo, entao nao custa folga.
        cl = s["colar"]
        xw, yw = x_w(z1), y_w(z1)
        xs1 = s["Xb"] / 2 + z1 * TAN - rec - e + 0.6
        ys1 = s["Yb"] / 2 + z1 * TAN - rec - e + 0.6
        qa = [P(xw - ec - cl, yw - ec - cl), P(xs1, yw - ec - cl), P(xs1, yw - ec + 0.3), P(xw - ec - cl, yw - ec + 0.3)]
        qb = [P(xw - ec - cl, yw - ec - cl), P(xw - ec + 0.3, yw - ec - cl), P(xw - ec + 0.3, ys1), P(xw - ec - cl, ys1)]
        hexa([(x, y, 0.0) for x, y in qa], [(x, y, z1) for x, y in qa], "pe")
        hexa([(x, y, 0.0) for x, y in qb], [(x, y, z1) for x, y in qb], "pe")
        # sola: poligono da boca do copo no chao (face externa + paredes)
        idx = [i for i in range(n) if z_base[i] <= -perna + 0.01
               and (lambda p: p[0] * sx > 0 and p[1] * sy > 0)(cont.pt(i, z0, -rec))]
        idx.sort(key=lambda i: cont.s[i])
        # os indices do canto sao contiguos no contorno, exceto quando o canto
        # cruza a origem do parametro (canto_td): reordena pela continuidade
        if idx and idx[-1] - idx[0] > n / 2:
            a = [i for i in idx if i > n / 2]; b = [i for i in idx if i <= n / 2]
            idx = a + b
        pts = [cont.pt(i, z0, -rec) for i in idx]
        xw, yw = x_w(z0), y_w(z0)
        # monta em coordenadas do canto fd (tudo positivo) e espelha
        fd = [(abs(p[0]), abs(p[1])) for p in pts]
        fd.sort(key=lambda p: math.atan2(p[1] - (s["Yb"] / 2 + z0 * TAN - s["Rb"]),
                                         p[0] - (s["Xb"] / 2 + z0 * TAN - s["Rb"])))
        xs = s["Xb"] / 2 + z0 * TAN - rec
        ys = s["Yb"] / 2 + z0 * TAN - rec
        fd = [(xs, yw - ec)] + fd + [(xw - ec, ys), (xw - ec, yw - ec)]
        poly = [P(x, y) for x, y in fd]
        if sx * sy < 0:
            poly = poly[::-1]
        m.prisma(poly, z0, z0 + ef, "pe")
        area = abs(sum(fd[i][0] * fd[i - 1][1] - fd[i - 1][0] * fd[i][1]
                       for i in range(len(fd)))) / 2
        return area
    s["apoio_cm2"] = round(sum(copo(sx, sy) for sx, sy in CANTOS.values()) / 100.0, 1)

    # ---- fundo em grelha diagonal de nervuras altas ------------------------
    hx = s["Xb"] / 2 + zf * TAN - e - w_mold
    hy = s["Yb"] / 2 + zf * TAN - e - w_mold
    r = max(2.0, s["Rb"] + zf * TAN - e - w_mold)
    larg, alt = s["larg_nerv"], s["alt_nerv"]
    passo_f = larg + s["vao_fundo"]      # medido perpendicular a nervura
    # a nervura para 1 mm dentro da parede do copo no topo (a parede inclina
    # 7,5 graus, entao embaixo ela fica ate 1,6 mm aquem — folga de malha, nao
    # de molde). Nunca alem da face do bolsao.
    xw_v, yw_v = x_w(zt) - ec - 0.5, y_w(zt) - ec - 0.5

    def dentro_fundo(x, y):
        """Planta util do fundo: canto arredondado, menos os quatro copos."""
        if abs(x) > hx or abs(y) > hy:
            return False
        if abs(x) > xw_v and abs(y) > yw_v:
            return False
        dx, dy = abs(x) - (hx - r), abs(y) - (hy - r)
        return dx <= 0 or dy <= 0 or dx * dx + dy * dy <= r * r

    def corta(cx, cy, ux, uy):
        """Trechos da reta (cx,cy)+t(ux,uy) dentro da planta do fundo."""
        trechos, t0, passo = [], None, 0.5
        t = -(hx + hy)
        while t <= hx + hy:
            d = dentro_fundo(cx + t * ux, cy + t * uy)
            if d and t0 is None:
                t0 = t
            if not d and t0 is not None:
                trechos.append((t0, t - passo)); t0 = None
            t += passo
        if t0 is not None:
            trechos.append((t0, t - passo))
        return [(a, b) for a, b in trechos if b - a > 2 * larg]

    q = math.sqrt(0.5)
    for sinal in (+1, -1):
        ux, uy = q, sinal * q
        nd = int((hx + hy) / passo_f)
        for i in range(-nd, nd + 1):
            d = i * passo_f
            cx, cy = -uy * d, ux * d
            for t0, t1 in corta(cx, cy, ux, uy):
                t0, t1 = t0 - 1.5, t1 + 1.5           # penetra na moldura/parede
                m.viga((cx + t0 * ux, cy + t0 * uy), (cx + t1 * ux, cy + t1 * uy),
                       larg, zt - alt, zt, "fundo", larg0=larg - 2 * alt * T1)

    m.mover(perna)
    s["cont"], s["ztopo"] = cont, ztopo
    return m, s


def confere_ninho(m, s):
    """Gira a peca 180 graus, sobe 'passo_ninho' e confere se algum vertice da
    base/fundo dela fica abaixo do topo do fundo da peca de baixo SEM estar
    dentro de um copo. E o teste que faltou da rev.05 a rev.17."""
    pn, perna = s["passo_ninho"], s["perna"]
    zt = s["z_fundo"] + s["ef"]
    viol, total, folga = 0, 0, 1e9
    for a, b, c, tag in m.tris:
        if tag not in ("saia", "pe", "fundo"):
            continue
        for p in (a, b, c):
            zA = p[2] + pn                         # cota na peca de baixo (pos-mover)
            if zA >= perna + zt - 0.01:
                continue
            total += 1
            x, y = -p[0], -p[1]
            if not em_copo(s, x, y, zA - perna, folga=0.05):
                viol += 1
                if viol <= 5:
                    print(f"    ninho: {tag} ({p[0]:.1f}, {p[1]:.1f}, {p[2]:.1f}) -> z_baixo {zA - perna:.1f}")
    return viol, total


def area_interna(s, z):
    W = s["Xb"] + 2 * z * TAN - 2 * s["e"]
    D = s["Yb"] + 2 * z * TAN - 2 * s["e"]
    r = max(0.0, s["Rb"] + z * TAN - s["e"])
    return W * D - (4 - math.pi) * r * r


def ficha(k):
    m, s = construir(k)
    s["volume_material_cm3"] = v = m.volume()
    s["massa_g"] = v * RHO_PP

    def integra(z0, z1, nn=400):
        h = (z1 - z0) / nn
        return sum(area_interna(s, z0 + h * (i + .5)) for i in range(nn)) * h / 1e6

    s["litros_boca"] = integra(s["z_fundo"] + s["ef"], s["hf"])
    s["litros_total"] = integra(s["z_fundo"] + s["ef"], s["hc"])
    ap = s["X"] * s["Y"] / 100.0
    s["area_projetada_cm2"] = ap
    s["ton_min"] = ap / 1e4 * 300 * 10.2
    s["ton_max"] = ap / 1e4 * 400 * 10.2
    s["n_triangulos"] = len(m.tris)
    viol, total = confere_ninho(m, s)
    s["ninho_viol"], s["ninho_pts"] = viol, total
    assert viol == 0, f"{k}: {viol} vertices da base atravessam a peca de baixo no ninho"
    return m, s


if __name__ == "__main__":
    for k in ("P", "M", "G"):
        m, s = ficha(k)
        print(f"{s['nome']:9s} {s['X']:.0f}x{s['Y']:.0f}x{s['H']:.0f} (cesta {s['hc']:.0f}"
              f" + perna {s['perna']:.0f}) | {s['massa_g']:5.0f} g | {s['litros_total']:5.1f} L | "
              f"pilha {s['passo_pilha']:.0f} / ninho {s['passo_ninho']:.0f} mm | "
              f"cubagem 10p {10*s['H']/(s['H']+9*s['passo_ninho']):.1f}x | "
              f"pe {s['larg_pe']:.0f}->{2*s['hw_topo']:.0f} mm, apoio {s['apoio_cm2']} cm2 | "
              f"canal {s['larg_canal']} / ponte {s['larg_ponte']} mm | "
              f"ninho: {s['ninho_pts']} pts abaixo do fundo, {s['ninho_viol']} fora do copo | "
              f"{s['n_triangulos']} tri")
