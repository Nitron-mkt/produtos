"""
MODULA rev.02 — familia de organizadores modulares Nitron (3 moldes).

FORMA
  Planta de cantos arredondados; nenhuma quina viva. Parede inteira vazada em
  ripas verticais de ritmo simetrico. Aro em perfil L (aba + saia) que e viga,
  apoio e pega ao mesmo tempo. Fundo em grelha, recuado 6 mm, de modo que a
  peca se apoia na propria saia.

MECANICA — PE POR FORA (rev.03)
  Aro: continuo e fechado em toda a volta, sem um unico recorte. Sobre ele, em
  4 posicoes, RESSALTOS de apoio.
  Base: 4 PES que avancam para FORA, alem da saia do aro.

  . alinhada 0 grau   -> o pe pousa no aro e o ressalto entra no vazio do pe:
                         PLUGA. passo = altura da peca.
  . girada 180 graus  -> o pe cai nas posicoes espelhadas, onde nao ha
                         ressalto, e desce POR FORA da peca de baixo: NINHO.
                         passo = espessura / tan(saida).

  E o "por fora" que liberta o aro. Na rev.02 o pe descia por dentro e por isso
  precisava de uma janela rasgada no aro — quatro buracos na borda superior,
  que faziam a peca parecer solta. Agora nada atravessa o aro: a borda de cima
  e uma peca inteira, arredondada, continua.

  Como o contorno cresce por OFFSET (e nao por escala), o trecho reto da
  lateral tem o mesmo comprimento em qualquer altura: o pe da peca de cima cai
  exatamente sobre o ressalto da de baixo, sem correcao de escala.

REGRA QUE GOVERNA TUDO
  A PAREDE e lisa por fora: todo o vazado e coplanar, nenhum relevo. E que a
  parede da peca de cima desliza rente a da de baixo no ninho — um friso
  horizontal de 2 mm ja trava a peca a meio caminho.

  As excecoes sao as duas pontas: o ARO (que no ninho fica sempre acima do aro
  da peca de baixo) e os PES (que passam por fora de tudo). Sao os dois unicos
  lugares onde a peca pode ter volume.
"""
import math
from geometria import DEG, Contorno, Malha, banda, perfurada
import grafismo as G

AMOSTRA = [2.6, 14]      # passo de amostragem do contorno / pontos por canto
SAIDA_GR = 7.5
TAN = math.tan(SAIDA_GR * DEG)
RHO_PP = 0.905

# ripa = largura do material entre furos; vao = largura do furo.
# O P e o mais fechado de proposito: e a peca que vai a vista em casa e a que
# guarda coisa pequena. O G e o mais aberto: e caixa de estoque.
TAMANHOS = {
    # H = altura TOTAL (chao ate o aro). A cesta e H - perna.
    "P": dict(nome="MODULA P", X=300.0, Y=200.0, H=185.0, perna=50.0, e=1.8, R=26.0,
              barra=9.0, vao_fundo=6.0, graf_esc=0.120, graf_ku=0.80, graf_kz=0.65, graf_eixo_gr=-55.0),
    "M": dict(nome="MODULA M", X=400.0, Y=300.0, H=245.0, perna=50.0, e=2.0, R=36.0,
              barra=7.5, vao_fundo=11.0, graf_esc=0.110, graf_ku=0.80, graf_kz=0.65, graf_eixo_gr=-55.0),
    "G": dict(nome="MODULA G", X=600.0, Y=400.0, H=370.0, perna=50.0, e=2.3, R=46.0,
              barra=7.5, vao_fundo=17.0, graf_esc=0.110, graf_ku=0.80, graf_kz=0.65, graf_eixo_gr=-55.0),
}


def suave(t):
    return t * t * (3 - 2 * t)


def meia_pe(s, d):
    """Meia-largura do pe a 'd' mm do chao: tronco de 7 graus por lado e
    concordancia circular com o rodape. Fora do intervalo, zero."""
    hh, hw, kk, rf = s["hh_pe"], s["hw_pe"], s["k_pe"], s["rf_pe"]
    if d < 0.0 or d > hh:
        return 0.0
    q = math.hypot(1.0, kk)
    uc = hw + kk * (hh - rf) + rf * q          # centro da concordancia
    d1 = (hh - rf) + rf * kk / q               # onde o tronco vira arco
    if d <= d1:
        return hw + d * kk
    return uc - math.sqrt(max(0.0, rf * rf - (d - (hh - rf)) ** 2))


def altura_pe(s, u):
    """Inversa de meia_pe: a que altura do chao o pe tem meia-largura u."""
    hh, hw, kk, rf = s["hh_pe"], s["hw_pe"], s["k_pe"], s["rf_pe"]
    if u <= hw:
        return 0.0
    q = math.hypot(1.0, kk)
    uc = hw + kk * (hh - rf) + rf * q
    d1 = (hh - rf) + rf * kk / q
    if u <= hw + d1 * kk:
        return (u - hw) / kk
    if u >= uc:
        return hh
    return (hh - rf) + math.sqrt(max(0.0, rf * rf - (uc - u) ** 2))


def parametros(k):
    s = dict(TAMANHOS[k])
    X, Y, e, R = s["X"], s["Y"], s["e"], s["R"]
    s["H_total"] = s["H"]
    s["hc"] = H = s["H"] - s["perna"]          # altura da cesta
    s["conic"] = con = H * TAN
    # O aro e a face mais externa da peca: X, Y e H sao as cotas REAIS do
    # produto, nao um envelope. O recuo de 5 mm que existia aqui era folga para
    # o pe passar por fora do aro — mecanismo que saiu na rev.08.
    s["folga_pe"] = fp = 0.0
    s["aba"] = aba = round(8.0 + 0.006 * X, 1)
    s["passo_ninho"] = pn = round(e / TAN + 2.0, 1)
    s["saia"] = round(pn - 4.0, 1)                # a saia tem de caber no passo
    s["aro_ext"] = X / 2 - fp                     # face externa do aro
    s["Xt"] = X - 2 * (fp + aba)                  # parede no topo
    s["Yt"] = Y - 2 * (fp + aba)
    s["Xb"], s["Yb"] = s["Xt"] - 2 * con, s["Yt"] - 2 * con
    s["Rt"] = s["Rb"] = R - fp - aba               # raio constante em toda a altura
    s["hf"] = round(0.40 * H)
    s["mergulho"] = round(0.28 * s["hf"])
    s["hb"] = round(16.0 + 0.055 * H)              # faixa cheia junto ao fundo
    s["h_aro"] = round(8.0 + 0.030 * H)           # parede cheia sob o aro
    s["z_fundo"] = 2.0    # o fundo quase encosta no plano do rodape
    s["ef"] = e + 0.5

    s["sal_pe"] = round(fp + aba + con, 1)        # o quanto o pe avanca
    # metade do trecho reto da lateral (constante em qualquer altura)
    s["b"] = s["Yt"] / 2 - s["Rt"]
    s["ax"] = s["Xt"] / 2 - s["Rt"]
    s["larg_pe"] = 0.0                            # definido abaixo, a partir de b
    # A crista de apoio saiu na rev.09 (quem trava a pilha e a coluna interna).
    # Com ela, sai a reserva de altura que encurtava a peca.
    s["h_ress"] = 0.0
    s["h_pe"] = s["perna"]
    s["y_pe_f"] = round(0.86 * s["b"], 1)
    s["y_pe_t"] = round(-0.40 * s["b"], 1)
    dif = s["y_pe_f"] + s["y_pe_t"]               # vao ate o pe espelhado

    # ---- a base (rev.07): rodape recuado + 4 pes conicos ------------------
    # O rodape e uma faixa continua, reta, recuada 1,5 mm da parede: e a linha
    # de sombra que separa a cesta da base. Dele saem quatro pes que se abrem
    # ate o envelope. O pe e conico (7 graus por lado) e encontra o rodape numa
    # concordancia circular — e a concordancia que faz o pe nascer da peca em
    # vez de ficar pendurado nela.
    s["recuo"] = round(e + 3.2, 1)   # recuo do rodape = a folga do degrau
    # Quem limita o rodape e o NINHO, nao a perna: no encaixe girado o rodape
    # da peca de cima passa raspando o fundo da de baixo.
    s["h_rodape"] = hro = round(
        min(0.22 * s["perna"], pn - s["z_fundo"] - s["ef"] - 1.5), 1)
    s["h_avental"] = round(0.16 * s["perna"], 1)   # frente e traseira sobem
    s["hh_pe"] = hh = round(s["perna"] - hro, 1)   # altura livre do pe
    s["k_pe"] = kk = math.tan(7.0 * DEG)           # conicidade do pe, por lado
    s["sal_pe"] = 0.0        # o pe NAO sai do vulto da peca (ver README, rev.08)
    s["etiqueta"] = round(0.24 * X)
    # ---- grafismo (rev.10): o grao da marca, deitado ----------------------
    s["graf_L"] = round(s["graf_esc"] * X, 1)   # ponta a ponta do elemento
    s["graf_giro"] = round(s["graf_eixo_gr"] - G.ANG_EIXO, 2)

    # ---- coluna interna: o que trava o empilhamento (rev.09) --------------
    # Quatro colunas verticais por dentro da parede, do fundo ate o aro. O topo
    # delas e o degrau onde o rodape da peca de cima pousa. A face interna e
    # VERTICAL (raio constante), entao o macho sai com quatro nervuras retas e
    # o bolsao atras da coluna afunila para baixo — nada de contra-saida.
    #
    # rev.17: as colunas recuaram de 0,90b/0,30b para 0,72b/0,24b. As posicoes
    # antigas jogavam a JANELA do rodape em cima do pe de canto — ela comia a
    # borda da area de apoio. Com 0,72b/0,24b os tres vaos do giro continuam
    # iguais (a regra p1/3) e a janela sai de perto do canto.
    s["y_col"] = (round(0.72 * s["b"], 1), round(-0.24 * s["b"], 1))
    s["w_col"] = round(0.17 * s["b"], 1)           # painel cego mais estreito
    s["rampa_col"] = round(min(5.5, 0.055 * s["b"]), 1)
    s["r_col"] = round(s["Xb"] / 2 - s["h_rodape"] * TAN - s["recuo"] - e, 2)
    s["passo_pilha"] = round(s["hc"] + s["h_rodape"], 1)
    vao_col = 0.48 * s["b"]     # otimo: p1/3 iguala os tres vaos
    assert s["w_col"] + 2 * s["rampa_col"] + 6 < vao_col, \
        f"{k}: coluna e janela se encostam ({vao_col:.0f} mm de vao)"

    # ---- o pe de canto, agora dimensionado pela janela --------------------
    # O apoio no chao vai do centro do canto ate onde a janela do rodape comeca,
    # menos 4 mm. Antes era uma fracao fixa e a janela mordia o pe.
    s["arco_canto"] = ac = math.pi * s["Rb"] / 4   # centro do canto -> reta
    dist_jan = 0.28 * s["b"] + ac - (s["w_col"] / 2 + s["rampa_col"])
    s["hw_pe"] = hw = round(min(0.30 * min(s["b"], s["ax"]), dist_jan - 4.0), 1)
    s["rf_pe"] = round(0.062 * min(s["b"], s["ax"]), 1)  # menor que o rodape
    s["hw_max"] = round(meia_pe(s, hh), 1)         # meia-largura na raiz
    s["rampa_pe"] = round(max(5.0, 0.06 * s["b"]), 1)
    s["larg_pe"] = round(2 * hw, 1)                # o pe no chao
    # sola: fecha o pe embaixo. Antes o apoio era a aresta de 'e' mm da casca.
    s["w_sola"] = round(max(6.0, 0.022 * X), 1)
    s["rec_sola"] = 0.6                            # sola recuada: mata o fio
    s["apoio_cm2"] = round(4 * 2 * hw * s["w_sola"] / 100.0, 1)
    assert hw > 0.15 * min(s["b"], s["ax"]), \
        f"{k}: pe estreito demais ({2*hw:.0f} mm de apoio)"
    assert s["rf_pe"] < hro, f"{k}: concordancia maior que o rodape"
    # no ninho a parede da peca de cima desce POR FORA da coluna: a folga e a
    # distancia entre a face interna dessa parede e a face externa da coluna
    f_par = (s["Xb"] / 2 - pn * TAN - e) - (s["r_col"] + e)
    assert f_par > 1.5, f"{k}: a parede do ninho raspa na coluna ({f_par:.1f} mm)"
    # no ninho o rodape da peca de cima passa raspando o fundo da de baixo
    f_fun = pn - (s["z_fundo"] + s["ef"] + s["h_rodape"])
    assert f_fun > 0.8, f"{k}: rodape bate no fundo no ninho ({f_fun:.1f} mm)"
    # a grelha do fundo nao pode alcancar o degrau
    f_gre = s["r_col"] - (s["Xb"] / 2 + s["z_fundo"] * TAN - e - round(9.0 + 0.010 * X, 1))
    assert f_gre > 1.5, f"{k}: a grelha alcanca o degrau ({f_gre:.1f} mm)"
    s["folga_degrau"] = round(min(f_par, f_gre), 1)

    s["u_max"] = um = round(meia_pe(s, hh), 1)
    assert 2 * um < 2 * min(s["b"], s["ax"]) - 10, f"{k}: pes de canto se encontram"
    assert s["saia"] < s["passo_ninho"] - 2, f"{k}: saia nao cabe no passo do ninho"
    s["folga_giro"] = round(2 * min(s["b"], s["ax"]) - 2 * um, 1)
    return s


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

    # ---- perfil do aro: continuo em toda a volta --------------------------
    h_geral = H                            # o aro chega na cota nominal

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
    yc_jan = tuple(-y for y in yc_col)          # espelho: por onde o degrau passa
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
    r_col = s["r_col"]

    def o_col(z):
        """Deslocamento que poe a face interna da coluna no raio r_col."""
        return r_col - (s["Xb"] / 2 + z * TAN)

    def OE(i, z):                                # face externa da casca
        f = fcol[i % n]
        return 0.0 if f <= 0 else f * (o_col(z) + e)

    def OI(i, z):                                # face interna da casca
        f = fcol[i % n]
        return -e if f <= 0 else (1 - f) * (-e) + f * o_col(z)

    # ---- o vazado: o grao da marca, deitado (rev.10) ----------------------
    # A parede deixou de ser ripa vertical. O furo agora e o traco do logo —
    # lente de duas arestas curvas, razao 2,22, pontas arredondadas — girado
    # 90 graus, em malha alternada. Continua tudo COPLANAR: nenhum relevo por
    # fora, senao o ninho trava a meio caminho.
    z_g0 = hb
    z_g1 = h_geral - h_aro          # a altura util da lateral manda no ritmo
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

    # ---- fundo em grelha ---------------------------------------------------
    zf, ef = s["z_fundo"], s["ef"]
    w_mold = round(9.0 + 0.010 * X, 1)
    emitir(lambda i: fjan[i % n] < 0.15, -e, -e - w_mold,
           lambda i: zf, lambda i: zf + ef, "fundo")
    hx = s["Xb"] / 2 + zf * TAN - e - w_mold
    hy = s["Yb"] / 2 + zf * TAN - e - w_mold
    r = max(2.0, s["Rb"] + zf * TAN - e - w_mold)

    def lim(c, ha, hb_, rr):
        d = abs(c) - (ha - rr)
        return hb_ if d <= 0 else (hb_ - rr) + math.sqrt(max(0.0, rr * rr - d * d))

    # A grelha corre a 45 graus, nao ortogonal: e a mesma direcao do vazado da
    # parede, e a agua escorre para o canto em vez de empocar na trama.
    barra = s["barra"]
    passo_f = barra + s["vao_fundo"]     # medido perpendicular a barra

    def dentro_fundo(x, y):
        """Planta util do fundo, com o canto arredondado."""
        if abs(x) > hx or abs(y) > hy:
            return False
        dx, dy = abs(x) - (hx - r), abs(y) - (hy - r)
        return dx <= 0 or dy <= 0 or dx * dx + dy * dy <= r * r

    def corta(cx, cy, ux, uy):
        """Extremos da reta (cx,cy)+t(ux,uy) dentro da planta do fundo."""
        t0, t1, passo = None, None, 0.8
        t = -(hx + hy)
        while t <= hx + hy:
            if dentro_fundo(cx + t * ux, cy + t * uy):
                if t0 is None:
                    t0 = t
                t1 = t
            t += passo
        return (t0, t1) if t0 is not None and t1 - t0 > barra else None

    q = math.sqrt(0.5)
    for sinal in (+1, -1):
        ux, uy = q, sinal * q
        # varre as diagonais pelo eixo perpendicular
        alcance = hx + hy
        nd = int(alcance / passo_f)
        for i in range(-nd, nd + 1):
            d = i * passo_f
            cx, cy = -uy * d, ux * d
            tt = corta(cx, cy, ux, uy)
            if not tt:
                continue
            t0, t1 = tt[0] + 0.4, tt[1] - 0.4
            m.viga((cx + t0 * ux, cy + t0 * uy), (cx + t1 * ux, cy + t1 * uy),
                   barra, zf, zf + ef, "fundo")

    # ---- base: rodape recuado e quatro pes de canto -----------------------
    # O pe deixou de ser o seletor do encaixe (README, rev.08) e por isso pode
    # finalmente ficar onde a peca pede: nos quatro cantos. Cada pe e o proprio
    # canto arredondado que continua para baixo, afinando 7 graus por lado, e
    # encontra o rodape numa concordancia circular. O rodape corre recuado
    # 1,5 mm: e a linha de sombra que separa a cesta da base.
    perna, hro, rec = s["perna"], s["h_rodape"], s["recuo"]
    P = cont.perimetro
    cantos = []
    for tr in ("canto_fd", "canto_fe", "canto_te", "canto_td"):
        idx = [i for i in range(n) if cont.amostras[i][0] == tr]
        cantos.append((cont.s[idx[0]] + cont.s[idx[-1] + 1]) / 2)

    def u_pe(i):
        """Distancia, ao longo do contorno, ao centro do canto mais proximo."""
        sm = (cont.s[i % n] + cont.s[(i % n) + 1]) / 2
        return min(min(abs(sm - c), P - abs(sm - c)) for c in cantos)

    def z_base(i):
        return -perna + altura_pe(s, u_pe(i))

    emitir(lambda i: fjan[i % n] < 0.15, -rec, -rec - e, z_base, lambda i: 0.0,
           "saia")

    # ---- sola: fecha o pe embaixo -----------------------------------------
    # A casca sozinha apoiava numa aresta de 'e' mm — fio de faca no piso e
    # pouca area para a pilha. A sola e uma laje na boca do pe, recuada 0,6 mm
    # da face externa (o recuo tira o fio) e avancando 'w_sola' para dentro.
    hw, ws, rs, ts = s["hw_pe"], s["w_sola"], s["rec_sola"], s["ef"]
    tap = min(9.0, ws + 2.0)          # a sola morre em rampa, nao em degrau

    def o_sola(i, z):
        u = u_pe(i)
        f = 1.0 if u <= hw - tap else max(0.0, (hw - u) / tap)
        return -rec - rs - ws * suave(f)

    emitir(lambda i: u_pe(i) <= hw and fjan[i % n] < 0.15,
           -rec - rs, o_sola,
           lambda i: -perna, lambda i: -perna + ts, "saia")
    m.mover(perna)

    s["cont"], s["ztopo"] = cont, ztopo
    return m, s


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
    return m, s


if __name__ == "__main__":
    for k in ("P", "M", "G"):
        m, s = ficha(k)
        print(f"{s['nome']:9s} {s['X']:.0f}x{s['Y']:.0f}x{s['H']:.0f} (cesta {s['hc']:.0f}"
              f" + perna {s['perna']:.0f}) | {s['massa_g']:5.0f} g | {s['litros_total']:5.1f} L | "
              f"pilha {s['passo_pilha']:.0f} / ninho {s['passo_ninho']:.0f} mm | "
              f"cubagem 10p {10*s['H']/(s['H']+9*s['passo_ninho']):.1f}x | "
              f"folga do giro {s['folga_giro']:.0f} mm | {s['n_triangulos']} tri")
