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
from geometria import DEG, Contorno, Malha, banda, tubo_roundrect

AMOSTRA = [2.6, 14]      # passo de amostragem do contorno / pontos por canto
SAIDA_GR = 5.0
TAN = math.tan(SAIDA_GR * DEG)
RHO_PP = 0.905

TAMANHOS = {
    "P": dict(nome="MODULA P", X=300.0, Y=200.0, H=150.0, e=2.0, R=26.0),
    "M": dict(nome="MODULA M", X=400.0, Y=300.0, H=200.0, e=2.2, R=36.0),
    "G": dict(nome="MODULA G", X=600.0, Y=400.0, H=250.0, e=2.5, R=46.0),
}


def suave(t):
    return t * t * (3 - 2 * t)


def parametros(k):
    s = dict(TAMANHOS[k])
    X, Y, H, e, R = s["X"], s["Y"], s["H"], s["e"], s["R"]
    s["conic"] = con = H * TAN
    s["folga_pe"] = fp = 3.5                      # o pe passa por fora da saia
    s["aba"] = aba = round(10.0 + 0.008 * X, 1)
    s["saia"] = round(12.0 + 0.014 * H, 1)
    s["aro_ext"] = X / 2 - fp                     # face externa do aro
    s["Xt"] = X - 2 * (fp + aba)                  # parede no topo
    s["Yt"] = Y - 2 * (fp + aba)
    s["Xb"], s["Yb"] = s["Xt"] - 2 * con, s["Yt"] - 2 * con
    s["Rt"] = R - fp - aba
    s["Rb"] = max(7.0, s["Rt"] - con)
    s["hf"] = round(0.40 * H)
    s["mergulho"] = round(0.28 * s["hf"])
    s["hb"] = round(14.0 + 0.05 * H)              # faixa cheia junto ao fundo
    s["h_aro"] = round(8.0 + 0.030 * H)           # parede cheia sob o aro
    s["z_fundo"] = 6.0
    s["ef"] = e + 0.5
    s["ripa"] = round(7.0 + 0.005 * X, 1)
    s["vao"] = round(14.0 + 0.012 * X, 1)
    s["fileiras"] = 3 if H >= 230 else 2
    s["passo_ninho"] = round(e / TAN + 2.0, 1)
    s["sal_pe"] = round(fp + aba + con, 1)        # o quanto o pe avanca
    # metade do trecho reto da lateral (constante em qualquer altura)
    s["b"] = s["Yt"] / 2 - s["Rt"]
    s["ax"] = s["Xt"] / 2 - s["Rt"]
    s["larg_pe"] = round(24.0 + 0.025 * X, 1)
    s["larg_ress"] = round(s["larg_pe"] - 14, 1)
    s["h_ress"] = round(8.0 + 0.012 * H, 1)
    s["h_pe"] = round(s["h_ress"] + e + 8, 1)
    s["y_pe_f"] = round(0.85 * s["b"], 1)
    s["y_pe_t"] = round(-0.42 * s["b"], 1)
    s["etiqueta"] = round(0.24 * X)
    folga = (s["y_pe_f"] + s["y_pe_t"]) - (s["larg_pe"] + s["larg_ress"]) / 2
    assert folga > 0, f"{k}: pe girado bate no ressalto (folga {folga:.1f} mm)"
    s["folga_giro"] = round(folga, 1)
    return s


def ritmo(meia, passo_alvo, larg):
    """Posicoes simetricas em torno de zero dentro de [-meia, meia]."""
    nj = max(1, int(round(meia / passo_alvo)))
    p = meia / nj
    return [(j + 0.5) * p for j in range(nj)], p


def construir(k):
    s = parametros(k)
    X, Y, H, e = s["X"], s["Y"], s["H"], s["e"]
    aba, hf, hb, h_aro = s["aba"], s["hf"], s["hb"], s["h_aro"]
    cont = Contorno(s["Xb"], s["Yb"], s["Rb"], TAN,
                    passo=AMOSTRA[0], n_arco=int(AMOSTRA[1]))
    m = Malha()
    n = cont.n
    passo_alvo = s["ripa"] + s["vao"]

    # ---- perfil do aro: continuo, com 4 cristas de apoio ------------------
    hr, lr = s["h_ress"], s["larg_ress"]
    rampa = 22.0
    h_geral = H - hr                       # o aro corre 'hr' abaixo do topo

    def crista(i):
        """Elevacao suave do aro nas 4 posicoes de apoio."""
        tr, _ = cont.amostras[i % n]
        if tr not in ("lat_d", "lat_e"):
            return 0.0
        y = cont.y_de(i)
        for yc in (s["y_pe_f"], s["y_pe_t"]):
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

    # ---- ritmo das ripas (uniforme, sem excecao) --------------------------
    pos_lat, _ = ritmo(s["b"], passo_alvo, s["ripa"])
    pos_fre, _ = ritmo(s["ax"], passo_alvo, s["ripa"])

    def classifica(i):
        tr, t = cont.amostras[i % n]
        if tr in ("lat_d", "lat_e"):
            y = cont.y_de(i)
            return "ripa" if any(abs(abs(y) - p) <= s["ripa"] / 2 for p in pos_lat) else "vao"
        if tr in ("frente", "traseira"):
            x = cont.ponto(i, 0.0)[0]
            if tr == "frente" and abs(x) <= s["etiqueta"] / 2:
                return "ripa"                       # painel liso para etiqueta
            return "ripa" if any(abs(abs(x) - p) <= s["ripa"] / 2 for p in pos_fre) else "vao"
        return "ripa" if 0.32 <= t <= 0.68 else "vao"   # uma ripa por canto

    tipo = [classifica(i) for i in range(n)]
    eh_ripa = lambda i: tipo[i % n] == "ripa"

    # ---- pontas arredondadas dos rasgos -----------------------------------
    dist_borda = [0.0] * n
    i = 0
    while i < n:
        if tipo[i] != "vao":
            i += 1
            continue
        j = i
        while j < n and tipo[j % n] == "vao":
            j += 1
        s0, s1 = cont.s[i], cont.s[j]
        for q in range(i, j):
            sm = (cont.s[q] + cont.s[q + 1]) / 2
            dist_borda[q] = min(sm - s0, s1 - sm)
        i = j
    r_furo = min(9.0, s["vao"] / 2.1)

    def dz(i):
        i %= n
        if tipo[i] != "vao":
            return 0.0
        d = min(dist_borda[i], r_furo)
        return r_furo - math.sqrt(max(0.0, r_furo * r_furo - (r_furo - d) ** 2))

    # ---- travessas coplanares entre as fileiras ---------------------------
    w_trav = round(6.0 + 0.006 * X, 1)
    nfil = s["fileiras"]

    def z_aro_inf(i):
        return ztopo(i) - h_aro

    def travessas(i):
        """Faixas horizontais de material dentro do rasgo, em (z0, z1).
        Sempre devolve nfil-1 faixas; degeneradas onde o rasgo e baixo."""
        alt = max(0.0, z_aro_inf(i) - hb)
        fs = []
        for q in range(1, nfil):
            c = hb + alt * q / nfil
            meia = w_trav / 2 if alt >= 0.30 * H else 0.0
            fs.append((c - meia, c + meia))
        return fs

    # ---- emissao de bandas continuas --------------------------------------
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

    z0 = lambda i: 0.0
    emitir(lambda i: True, 0.0, -e, z0, lambda i: hb + dz(i), "faixa")
    emitir(eh_ripa, 0.0, -e, lambda i: hb, ztopo, "ripa")
    for q in range(nfil - 1):
        def faz(q=q):
            emitir(lambda i: (not eh_ripa(i))
                   and travessas(i)[q][1] > travessas(i)[q][0], 0.0, -e,
                   lambda i: travessas(i)[q][0] - dz(i),
                   lambda i: travessas(i)[q][1] + dz(i), "ripa")
        faz()
    emitir(lambda i: not eh_ripa(i), 0.0, -e,
           lambda i: z_aro_inf(i) - dz(i), ztopo, "aro")

    # ---- aro: continuo, fechado, com topo em tres degraus (vira filete) ----
    A, S = aba, s["saia"]
    todos = lambda i: True
    emitir(todos, A - 2.0, -e, lambda i: ztopo(i) - e - 1.6, lambda i: ztopo(i) - 1.6, "aro")
    emitir(todos, A - 3.2, -e + 1.2, lambda i: ztopo(i) - 1.6, lambda i: ztopo(i) - 0.5, "aro")
    emitir(todos, A - 4.6, -e + 2.6, lambda i: ztopo(i) - 0.5, ztopo, "aro")
    emitir(todos, A, A - e, lambda i: ztopo(i) - S, lambda i: ztopo(i) - 1.6, "aro")
    emitir(todos, A, A - 2.0, lambda i: ztopo(i) - 2.6, lambda i: ztopo(i) - 1.4, "aro")

    # ---- fundo em grelha ---------------------------------------------------
    zf, ef = s["z_fundo"], s["ef"]
    w_mold = round(9.0 + 0.010 * X, 1)
    banda(m, cont, 0, n, -e, -e - w_mold, lambda i: zf, lambda i: zf + ef, "fundo")
    hx = s["Xb"] / 2 + zf * TAN - e - w_mold
    hy = s["Yb"] / 2 + zf * TAN - e - w_mold
    r = max(2.0, s["Rb"] + zf * TAN - e - w_mold)

    def lim(c, ha, hb_, rr):
        d = abs(c) - (ha - rr)
        return hb_ if d <= 0 else (hb_ - rr) + math.sqrt(max(0.0, rr * rr - d * d))

    barra = round(5.0 + 0.0035 * X, 1)
    passo_f = barra + 10.0 + 0.010 * X
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

    # ---- pes (na base) -----------------------------------------------------
    lpe, hpe = s["larg_pe"], s["h_pe"]
    largura_pe = X / 2 - (s["Xb"] / 2 - e) + 4.0        # cobre da parede ao envelope
    for lado in (1, -1):
        for yc in (s["y_pe_f"], s["y_pe_t"]):
            cxp = lado * (X / 2 - largura_pe / 2)
            tubo_roundrect(m, cxp, yc, largura_pe, lpe, min(11.0, lpe / 3),
                           0.0, hpe, e, "pe", n_arco=6, cone=1.6)

    # ---- etiqueta a crista (para poder destaca-la no render e no visualizador)
    lim_crista = h_geral + 1.5
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
    s["litros_total"] = integra(s["z_fundo"] + s["ef"], s["H"])
    ap = s["X"] * s["Y"] / 100.0
    s["area_projetada_cm2"] = ap
    s["ton_min"] = ap / 1e4 * 300 * 10.2
    s["ton_max"] = ap / 1e4 * 400 * 10.2
    s["n_triangulos"] = len(m.tris)
    return m, s


if __name__ == "__main__":
    for k in ("P", "M", "G"):
        m, s = ficha(k)
        print(f"{s['nome']:9s} {s['X']:.0f}x{s['Y']:.0f}x{s['H']:.0f} R={s['R']:.0f} | "
              f"{s['massa_g']:5.0f} g | {s['litros_total']:5.1f} L | ninho "
              f"{s['passo_ninho']:.0f} mm | ripa {s['ripa']}/{s['vao']} ({s['fileiras']} fil) | "
              f"pe y={s['y_pe_f']:.0f} e {s['y_pe_t']:.0f}, avanca {s['sal_pe']:.0f} mm | "
              f"folga do giro {s['folga_giro']:.0f} mm | {s['n_triangulos']} tri")
