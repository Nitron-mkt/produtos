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
from grafismo import Grafismo, RAZAO, PU, PZ

AMOSTRA = [2.6, 14]      # passo de amostragem do contorno / pontos por canto
SAIDA_GR = 7.5
TAN = math.tan(SAIDA_GR * DEG)
RHO_PP = 0.905

# ripa = largura do material entre furos; vao = largura do furo.
# O P e o mais fechado de proposito: e a peca que vai a vista em casa e a que
# guarda coisa pequena. O G e o mais aberto: e caixa de estoque.
TAMANHOS = {
    # H = altura TOTAL (chao ate o aro). A cesta e H - perna.
    "P": dict(nome="MODULA P", X=300.0, Y=200.0, H=200.0, perna=50.0, e=1.8, R=26.0,
              barra=9.0, vao_fundo=6.0, graf_esc=0.125),
    "M": dict(nome="MODULA M", X=400.0, Y=300.0, H=250.0, perna=50.0, e=2.0, R=36.0,
              barra=7.5, vao_fundo=11.0, graf_esc=0.140),
    "G": dict(nome="MODULA G", X=600.0, Y=400.0, H=300.0, perna=50.0, e=2.3, R=46.0,
              barra=7.5, vao_fundo=17.0, graf_esc=0.120),
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
    s["folga_pe"] = fp = 5.0                      # o pe passa por fora do aro
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
    s["h_ress"] = round(7.0 + 0.010 * H, 1)
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
    s["h_rodape"] = hro = round(0.20 * s["perna"], 1)
    s["h_avental"] = round(0.16 * s["perna"], 1)   # frente e traseira sobem
    s["hh_pe"] = hh = round(s["perna"] - hro, 1)   # altura livre do pe
    s["hw_pe"] = hw = round(0.155 * min(s["b"], s["ax"]), 1)  # meia-largura no chao
    s["k_pe"] = kk = math.tan(7.0 * DEG)           # conicidade do pe, por lado
    s["rf_pe"] = round(0.10 * min(s["b"], s["ax"]), 1)   # raio da concordancia
    s["hw_max"] = round(meia_pe(s, hh), 1)         # meia-largura na raiz
    s["rampa_pe"] = round(max(5.0, 0.06 * s["b"]), 1)
    s["larg_pe"] = round(2 * hw, 1)                # o pe no chao
    s["sal_pe"] = 0.0        # o pe NAO sai do vulto da peca (ver README, rev.08)
    s["sal_crista"] = round(fp - 1.5, 1)           # a crista avanca para receber o pe
    s["rampa_crista"] = round(min(18.0, 0.34 * dif), 1)
    s["larg_ress"] = round(2 * hw + 6.0, 1)
    s["etiqueta"] = round(0.24 * X)
    # ---- grafismo (rev.10): o grao da marca, deitado ----------------------
    s["graf_L"] = round(s["graf_esc"] * X, 1)
    s["graf_W"] = round(s["graf_L"] / RAZAO, 1)
    s["graf_rt"] = round(min(2.2, s["graf_W"] / 4), 1)

    # ---- o que a base ainda tem de respeitar ------------------------------
    # Com o pe dentro do vulto, ele nao colide com nada no ninho: desce junto
    # com a parede, no mesmo passo. So resta nao encostar no pe vizinho.
    # ---- coluna interna: o que trava o empilhamento (rev.09) --------------
    # Quatro colunas verticais por dentro da parede, do fundo ate o aro. O topo
    # delas e o degrau onde o rodape da peca de cima pousa. A face interna e
    # VERTICAL (raio constante), entao o macho sai com quatro nervuras retas e
    # o bolsao atras da coluna afunila para baixo — nada de contra-saida.
    s["y_col"] = (round(0.90 * s["b"], 1), round(-0.30 * s["b"], 1))
    s["w_col"] = round(0.24 * s["b"], 1)
    s["rampa_col"] = round(min(7.0, 0.075 * s["b"]), 1)
    s["r_col"] = round(s["Xb"] / 2 - s["h_rodape"] * TAN - s["recuo"] - e, 2)
    s["passo_pilha"] = round(s["hc"] + s["h_rodape"], 1)
    vao_col = 0.60 * s["b"]     # otimo: p1/3 iguala os dois vaos
    assert s["w_col"] + 2 * s["rampa_col"] + 6 < vao_col, \
        f"{k}: coluna e janela se encostam ({vao_col:.0f} mm de vao)"
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
    """Instancia a malha de graos: periodos inteiros na volta e na altura."""
    L, W = s["graf_L"], s["graf_W"]
    nu = max(6, int(round(cont.perimetro / (PU * L))))
    nz = max(2, int(round((zhi - zlo) / (PZ * L))))
    pu, pz = cont.perimetro / nu, (zhi - zlo) / nz
    g = Grafismo(L / 2, W / 2, s["graf_rt"], pu, pz, zlo + pz / 2)
    s["graf_nu"], s["graf_nz"] = nu, nz
    s["graf_pu"], s["graf_pz"] = round(pu, 1), round(pz, 1)
    s["graf_vazado"], s["graf_alma"] = g.medidas()
    assert s["graf_alma"] > 4.0, \
        f"alma do grafismo fina demais ({s['graf_alma']:.1f} mm)"
    return g


def construir(k):
    s = parametros(k)
    X, Y, e = s["X"], s["Y"], s["e"]
    H = s["hc"]                    # dentro daqui, H e a altura da CESTA
    aba, hf, hb, h_aro = s["aba"], s["hf"], s["hb"], s["h_aro"]
    cont = Contorno(s["Xb"], s["Yb"], s["Rb"], TAN,
                    passo=AMOSTRA[0], n_arco=int(AMOSTRA[1]))
    m = Malha()
    n = cont.n

    # ---- perfil do aro: continuo, com 4 cristas de apoio ------------------
    hr, lr = s["h_ress"], s["larg_ress"]
    rampa = s["rampa_crista"]
    h_geral = H - hr                       # o aro corre 'hr' abaixo do topo

    def crista(i):
        """Elevacao suave do aro nas 4 posicoes de apoio."""
        tr, _ = cont.amostras[i % n]
        if tr not in ("lat_d", "lat_e"):
            return 0.0
        y = cont.y_de(i)
        for yc in ():
            d = abs(y - yc)
            if d <= lr / 2:
                return hr
            if d <= lr / 2 + rampa:
                return hr * (1 - suave((d - lr / 2) / rampa))
        return 0.0

    def ztopo(i):
        tr, t = cont.amostras[i % n]
        if tr == "canto_fd":
            return h_geral - (h_geral - hf) * suave(t)
        if tr == "canto_fe":
            return hf + (h_geral - hf) * suave(t)
        if tr == "frente":
            return hf - s["mergulho"] * 0.5 * (1 - math.cos(2 * math.pi * t))
        return h_geral + crista(i)

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

    barra = s["barra"]
    passo_f = barra + s["vao_fundo"]
    nx = max(2, int(round(2 * hx / passo_f)))
    ny = max(2, int(round(2 * hy / passo_f)))
    for i in range(1, nx):
        c = -hx + 2 * hx * i / nx
        L = lim(c, hx, hy, r) - 0.8
        m.bloco(c - barra / 2, c + barra / 2, -L, L, zf, zf + ef, "fundo")
    for j in range(1, ny):
        c = -hy + 2 * hy * j / ny
        L = lim(c, hy, hx, r) - 0.8
        m.bloco(-L, L, c - barra / 2, c + barra / 2, zf, zf + ef, "fundo")

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
    m.mover(perna)

    # ---- etiqueta a crista (para poder destaca-la no render e no visualizador)
    lim_crista = h_geral + s["perna"] + 1.5
    for i, (a, b, c, tag) in enumerate(m.tris):
        if tag != "pe" and (a[2] + b[2] + c[2]) / 3 > lim_crista:
            m.tris[i] = (a, b, c, "crista")

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
