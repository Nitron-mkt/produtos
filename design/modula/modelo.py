"""
MODULA rev.02 — familia de organizadores modulares Nitron (3 moldes).

FORMA
  Planta de cantos arredondados; nenhuma quina viva. Parede inteira vazada em
  ripas verticais de ritmo simetrico. Aro em perfil L (aba + saia) que e viga,
  apoio e pega ao mesmo tempo. Fundo em grelha, recuado 6 mm, de modo que a
  peca se apoia na propria saia.

MECANICA — PE + PINO
  Aro: 4 PINOS ocos sobre a aba.
  Base: 4 PES ocos, embutidos na faixa inferior; o vazio do pe e o soquete.

  . alinhada 0 grau   -> o pe pousa na aba e o pino entra no soquete: PLUGA.
                         passo = altura da peca.
  . girada 180 graus  -> cada pe cai onde falta uma ripa (a JANELA, na posicao
                         espelhada) e desce por dentro: NINHO.
                         passo = espessura / tan(saida).

  As ripas de cada lateral sao distribuidas simetricamente em torno de y=0, de
  modo que a posicao espelhada de uma ripa e sempre outra ripa. Os pinos ficam
  em duas dessas ripas; as duas ripas espelhadas correspondentes sao removidas
  e viram as janelas. A janela e, literalmente, uma ripa que falta — o ritmo da
  parede continua inteiro.

  Como o contorno cresce por OFFSET (e nao por escala), o trecho reto da
  lateral tem o mesmo comprimento em qualquer altura: o pe da peca de cima cai
  exatamente sobre o pino da de baixo, sem correcao de escala.

REGRA QUE GOVERNA TUDO
  Saliencia externa so e permitida na faixa do topo — altura menor que o passo
  do ninho — porque essa faixa nunca precisa entrar dentro de outra peca.
  Abaixo dela a parede e lisa por fora e todo o vazado e coplanar. E por isso
  que a peca nao tem friso horizontal: ele mataria o ninho.
"""
import math
from geometria import DEG, Contorno, Malha, banda

AMOSTRA = [2.6, 14]      # passo de amostragem do contorno / pontos por canto
SAIDA_GR = 5.0
TAN = math.tan(SAIDA_GR * DEG)
RHO_PP = 0.905

TAMANHOS = {
    "P": dict(nome="MODULA P", X=300.0, Y=200.0, H=150.0, e=2.0, R=22.0),
    "M": dict(nome="MODULA M", X=400.0, Y=300.0, H=200.0, e=2.2, R=30.0),
    "G": dict(nome="MODULA G", X=600.0, Y=400.0, H=250.0, e=2.5, R=40.0),
}


def suave(t):
    return t * t * (3 - 2 * t)


def parametros(k):
    s = dict(TAMANHOS[k])
    X, Y, H, e, R = s["X"], s["Y"], s["H"], s["e"], s["R"]
    s["conic"] = con = H * TAN
    s["aba"] = aba = round(9.0 + 0.008 * X, 1)
    s["saia"] = round(11.0 + 0.014 * H, 1)
    s["Xt"], s["Yt"] = X - 2 * aba, Y - 2 * aba
    s["Xb"], s["Yb"] = s["Xt"] - 2 * con, s["Yt"] - 2 * con
    s["Rb"] = max(6.0, R - aba - con)
    s["hf"] = round(0.40 * H)
    s["mergulho"] = round(0.26 * s["hf"])
    s["hb"] = round(12.0 + 0.06 * H)
    s["h_aro"] = round(9.0 + 0.035 * H)
    s["z_fundo"] = 6.0
    s["ef"] = e + 0.5
    s["ripa"] = round(8.0 + 0.006 * X, 1)
    s["vao"] = round(13.5 + 0.013 * X, 1)
    s["passo_ninho"] = round(e / TAN + 2.0, 1)
    s["sal_pe"] = aba + con
    # metade do trecho reto da lateral (constante em qualquer altura)
    s["b"] = (Y - 2 * aba) / 2 - (R - aba)
    s["ax"] = (X - 2 * aba) / 2 - (R - aba)      # idem para frente/traseira
    s["larg_pino"] = round(min(0.24 * s["b"], 18.0 + 0.02 * X), 1)
    s["larg_pe"] = round(s["larg_pino"] + 2 * e + 4, 1)
    s["h_pino"] = round(8.0 + 0.018 * H)
    s["h_pe"] = round(s["h_pino"] + 7)
    s["h_janela"] = 12.0
    s["etiqueta"] = round(0.24 * X)               # painel cheio na frente
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

    # ---- perfil do aro ----------------------------------------------------
    def ztopo(i):
        tr, t = cont.amostras[i % n]
        if tr == "canto_fd":
            return H - (H - hf) * suave(t)
        if tr == "canto_fe":
            return hf + (H - hf) * suave(t)
        if tr == "frente":
            return hf - s["mergulho"] * 0.5 * (1 - math.cos(2 * math.pi * t))
        return H

    # ---- ritmo das ripas ---------------------------------------------------
    pos_lat, passo_lat = ritmo(s["b"], passo_alvo, s["ripa"])
    pos_fre, _ = ritmo(s["ax"], passo_alvo, s["ripa"])

    # as duas ripas que recebem pino, e as duas espelhadas que viram janela
    y_pino_f = min(pos_lat, key=lambda p: abs(p - 0.87 * s["b"]))
    y_pino_t = -min(pos_lat, key=lambda p: abs(p - 0.62 * s["b"]))
    s["y_pino_f"], s["y_pino_t"] = y_pino_f, y_pino_t
    s["y_janela_f"], s["y_janela_t"] = -y_pino_t, -y_pino_f
    s["abertura"] = round(2 * passo_lat - s["ripa"], 1)
    s["passo_lat"] = round(passo_lat, 1)

    janelas_y = (s["y_janela_f"], s["y_janela_t"])
    meia_jan = passo_lat - s["ripa"] / 2

    def classifica(i):
        tr, t = cont.amostras[i % n]
        if tr in ("lat_d", "lat_e"):
            y = cont.y_de(i)
            for jy in janelas_y:
                if abs(y - jy) <= meia_jan:
                    return "janela"
            for p in pos_lat:
                if abs(abs(y) - p) <= s["ripa"] / 2:
                    return "ripa"
            return "vao"
        if tr == "traseira":
            x = cont.ponto(i, 0.0)[0]
            for p in pos_fre:
                if abs(abs(x) - p) <= s["ripa"] / 2:
                    return "ripa"
            return "vao"
        if tr == "frente":
            x = cont.ponto(i, 0.0)[0]
            if abs(x) <= s["etiqueta"] / 2:
                return "ripa"                       # painel de etiqueta
            for p in pos_fre:
                if abs(abs(x) - p) <= s["ripa"] / 2:
                    return "ripa"
            return "vao"
        return "ripa" if 0.34 <= t <= 0.66 else "vao"   # uma ripa por canto

    tipo = [classifica(i) for i in range(n)]
    eh_ripa = lambda i: tipo[i % n] == "ripa"
    eh_janela = lambda i: tipo[i % n] == "janela"

    # ---- arredondamento das pontas dos rasgos ------------------------------
    # para cada aresta de vao, distancia (em mm de perimetro) ate a borda do vao
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
    r_furo = min(9.0, s["vao"] / 2.2)

    def dz(i):
        i %= n
        if tipo[i] != "vao":
            return 0.0
        d = min(dist_borda[i], r_furo)
        return r_furo - math.sqrt(max(0.0, r_furo * r_furo - (r_furo - d) ** 2))

    # ---- travessa coplanar a meia altura (so onde o rasgo e alto) ----------
    w_trav = round(6.0 + 0.008 * X, 1)
    def z_aro_inf(i):
        return ztopo(i) - h_aro
    def alto(i):
        return (z_aro_inf(i) - hb) > 0.42 * H
    def z_trav(i):
        c = (hb + z_aro_inf(i)) / 2
        return c - w_trav / 2, c + w_trav / 2

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
    emitir(lambda i: not eh_janela(i), 0.0, -e, z0, lambda i: hb + dz(i), "faixa")
    emitir(eh_janela, 0.0, -e, z0, lambda i: s["h_janela"], "faixa")
    emitir(eh_ripa, 0.0, -e, lambda i: hb, ztopo, "ripa")
    emitir(lambda i: tipo[i % n] == "vao" and alto(i), 0.0, -e,
           lambda i: z_trav(i)[0] - dz(i), lambda i: z_trav(i)[1] + dz(i), "ripa")
    emitir(lambda i: not (eh_ripa(i) or eh_janela(i)),
           0.0, -e, lambda i: z_aro_inf(i) - dz(i), ztopo, "aro")
    sem_jan = lambda i: not eh_janela(i)
    emitir(sem_jan, aba, 0.0, lambda i: ztopo(i) - e, ztopo, "aro")
    emitir(sem_jan, aba, aba - e, lambda i: ztopo(i) - s["saia"],
           lambda i: ztopo(i) - e, "aro")

    # ---- fundo em grelha ---------------------------------------------------
    zf, ef = s["z_fundo"], s["ef"]
    w_mold = round(10.0 + 0.012 * X, 1)
    banda(m, cont, 0, n, -e, -e - w_mold, lambda i: zf, lambda i: zf + ef, "fundo")
    hx = s["Xb"] / 2 + zf * TAN - e - w_mold
    hy = s["Yb"] / 2 + zf * TAN - e - w_mold
    r = max(2.0, s["Rb"] + zf * TAN - e - w_mold)

    def lim(c, ha, hb_, rr):
        d = abs(c) - (ha - rr)
        return hb_ if d <= 0 else (hb_ - rr) + math.sqrt(max(0.0, rr * rr - d * d))

    barra = round(5.5 + 0.004 * X, 1)
    passo_f = barra + 11.0 + 0.011 * X
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

    # ---- pinos e pes -------------------------------------------------------
    lp, hpin, hpe, lpe = s["larg_pino"], s["h_pino"], s["h_pe"], s["larg_pe"]
    for lado in (1, -1):
        for yc in (y_pino_f, y_pino_t):
            xa, xb = sorted([lado * (X / 2 - 1.5), lado * (X / 2 - aba + 1.5)])
            m.caixa_oca(xa, xb, yc - lp / 2, yc + lp / 2, H, H + hpin, e,
                        "pino", tampa="topo")
            xc, xd = sorted([lado * (s["Xb"] / 2 - e), lado * (X / 2)])
            m.caixa_oca(xc, xd, yc - lpe / 2, yc + lpe / 2, 0.0, hpe, e,
                        "pe", tampa="topo")
            xp, xq = sorted([lado * (X / 2 - aba - 3.0 - e), lado * (X / 2 - aba - 3.0)])
            m.bloco(xp, xq, yc - lpe / 2 + e, yc + lpe / 2 - e, 0.0, hpe, "pe")

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
              f"{s['passo_ninho']:.0f} mm | ripa {s['ripa']}/{s['vao']} mm | "
              f"pino y={s['y_pino_f']:.0f} e {s['y_pino_t']:.0f} | janela y="
              f"{s['y_janela_f']:.0f} e {s['y_janela_t']:.0f} | abertura "
              f"{s['abertura']:.0f} mm > pe {s['larg_pe']:.0f} mm | {s['n_triangulos']} tri")
