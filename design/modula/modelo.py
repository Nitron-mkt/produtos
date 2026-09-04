"""
MODULA — familia de organizadores modulares Nitron (3 tamanhos, 3 moldes).

ARQUITETURA
  Corpo tronco-piramidal de frente aberta, com 4 CANAIS VERTICAIS por lateral
  (8 no total). Os canais sao vincos da propria parede (parede deslocada para
  fora), nao nervuras macicas — numa peca que encaixa em ninho toda nervura
  precisa ser vinco e o conjunto de vincos precisa ser simetrico frente/verso,
  senao a peca de cima nao desce.

  Na base, 4 TALISCAS nascem dentro de 4 desses canais.
  No topo, 2 canais por lateral tem o topo FECHADO (assento, com bolsao que
  captura a talisca) e 2 tem o topo ABERTO (guia do ninho).
  As posicoes fechadas e abertas sao espelhadas entre si:

      fechado  y = +0,42Y  e  y = -0,12Y
      aberto   y = -0,42Y  e  y = +0,12Y

  -> alinhado (0 grau):  talisca cai no assento     => EMPILHA, passo = altura
  -> girado (180 graus): talisca desce pelo canal   => NINHO,  passo = e/tan(saida)

  Tudo sai na direcao de abertura do molde: nenhuma gaveta, nenhum movimento
  lateral, nenhuma saida forcada.
"""
import math
from geometria import DEG, Solido, painel, grade_furos

SAIDA_GR = 4.0                    # angulo de saida de todas as paredes
TAN = math.tan(SAIDA_GR * DEG)
RHO_PP = 0.905                    # g/cm3

TAMANHOS = {
    "P": dict(nome="MODULA P", X=300.0, Y=200.0, H=150.0, e=2.0, fundo="fechado"),
    "M": dict(nome="MODULA M", X=400.0, Y=300.0, H=200.0, e=2.2, fundo="fechado"),
    "G": dict(nome="MODULA G", X=600.0, Y=400.0, H=250.0, e=2.6, fundo="grelha"),
}

# posicoes dos canais, em fracao de Y medida NO TOPO
CANAIS = [(+0.42, "fechado"), (+0.12, "aberto"),
          (-0.12, "fechado"), (-0.42, "aberto")]


def _perfil_em(perfil, u):
    if u <= perfil[0][0]:
        return perfil[0][1]
    for (ua, za), (ub, zb) in zip(perfil, perfil[1:]):
        if ua <= u <= ub:
            return za + (zb - za) * ((u - ua) / (ub - ua)) if ub > ua else zb
    return perfil[-1][1]


def parametros(k):
    s = dict(TAMANHOS[k])
    X, Y, H, e = s["X"], s["Y"], s["H"], s["e"]
    s["conic"] = con = H * TAN                 # quanto a base recua por lado
    s["v_topo"] = v = 1.10 * (con + 17.0)      # profundidade do canal no aro
    s["sal"] = con + 12.0                      # saliencia da talisca (12 mm de apoio)
    s["Xt"] = Xt = X - 2 * v                   # painel lateral no topo
    s["Yt"] = Yt = Y
    s["Xb"] = Xb = Xt - 2 * con
    s["Yb"] = Yb = Yt - 2 * con
    s["ax"], s["ay"] = Xb / 2.0, Yb / 2.0
    s["v_base"] = v * Xb / Xt
    s["ef"] = e + 0.4
    s["hf"] = round(0.42 * H)                  # parede frontal
    s["ky"] = Yt / Yb
    s["kx"] = Xt / Xb
    s["passo_ninho"] = e / TAN + 2.0
    s["larg_canal"] = max(26.0, 0.085 * Y)
    return s


def construir(k):
    s = parametros(k)
    X, Y, H, e = s["X"], s["Y"], s["H"], s["e"]
    ax, ay, ef, hf = s["ax"], s["ay"], s["ef"], s["hf"]
    ky, sal, vb, wc = s["ky"], s["sal"], s["v_base"], s["larg_canal"]
    sol = Solido(s["Xb"], s["Yb"], TAN, TAN)

    canais = [(f * Y / ky, tipo, f) for f, tipo in CANAIS]      # centro na base
    fechados = [c for c in canais if c[1] == "fechado"]
    y_diag = -0.05 * Y / ky                                      # inicio da diagonal
    perfil = [(-ay, H), (y_diag, H), (ay, hf)]

    # ---------------- fundo -------------------------------------------------
    if s["fundo"] == "fechado":
        sol.add(-ax, ax, -ay, ay, 0.0, ef, tag="fundo")
        nerv = max(7.0, 0.04 * H)
        for i in (-1, 1):
            sol.add(i * 0.34 * ax - e / 2, i * 0.34 * ax + e / 2, -ay + e, ay - e,
                    ef, ef + nerv, tag="nervura")
        for j in (-1, 1):
            sol.add(-ax + e, ax - e, j * 0.34 * ay - e / 2, j * 0.34 * ay + e / 2,
                    ef, ef + nerv, tag="nervura")
    else:
        b, mo = 9.0, 26.0
        sol.add(-ax, ax, -ay, -ay + mo, 0.0, ef, tag="fundo")
        sol.add(-ax, ax, ay - mo, ay, 0.0, ef, tag="fundo")
        sol.add(-ax, -ax + mo, -ay + mo, ay - mo, 0.0, ef, tag="fundo")
        sol.add(ax - mo, ax, -ay + mo, ay - mo, 0.0, ef, tag="fundo")
        nx = int((2 * ax - 2 * mo) / 46.0)
        ny = int((2 * ay - 2 * mo) / 46.0)
        for i in range(1, nx):
            c = -ax + mo + (2 * ax - 2 * mo) * i / nx
            sol.add(c - b / 2, c + b / 2, -ay + mo, ay - mo, 0.0, ef, tag="fundo")
        for j in range(1, ny):
            c = -ay + mo + (2 * ay - 2 * mo) * j / ny
            sol.add(-ax + mo, ax - mo, c - b / 2, c + b / 2, 0.0, ef, tag="fundo")

    # ---------------- paineis laterais -------------------------------------
    banda = max(20.0, 0.13 * H)
    furos_lat = []
    livres = []                     # trechos de painel entre canais
    bordas = sorted([(c[0] - wc / 2, c[0] + wc / 2) for c in canais])
    pos = -ay
    for a, b in bordas:
        if a > pos:
            livres.append((pos, a))
        pos = max(pos, b)
    if pos < ay:
        livres.append((pos, ay))
    for a, b in livres:
        n = max(1, int((b - a) / 30.0))
        zt = min(_perfil_em(perfil, a), _perfil_em(perfil, b))
        nlin = 3 if zt - banda > 0.42 * H else 2
        furos_lat += grade_furos(a + 11, b - 11, banda + 6, zt - 14, n, nlin, 11.0, 24.0)
    for a, b in bordas:                                   # o canal ocupa o painel
        furos_lat.append((a, b, -5.0, H + 5.0))

    for lado in (-1, 1):
        painel(sol, lado * (ax - e), lado * ax, -ay, ay, perfil, furos_lat,
               tag="lateral", eixo="y")
        # rebordo: engrossa os ultimos 12 mm do topo do painel
        for a, b in livres:
            n = max(2, int((b - a) / 10))
            for i in range(n):
                ya = a + (b - a) * i / n
                yb = a + (b - a) * (i + 1) / n
                za, zb = _perfil_em(perfil, ya), _perfil_em(perfil, yb)
                sol.add(lado * ax, lado * (ax + 2.6), ya, yb,
                        min(za, zb) - 12.0, za, zb, tag="rebordo")

        # ---- canais verticais ----
        for cy, tipo, frac in canais:
            y0, y1 = cy - wc / 2, cy + wc / 2
            xi, xo = lado * ax, lado * (ax + vb)
            # canal fechado sobe ate o topo (vira a orelha dianteira);
            # canal aberto acompanha o perfil — a talisca entra por cima dele
            if tipo == "fechado":
                za = zb = H
            else:
                za, zb = _perfil_em(perfil, y0), _perfil_em(perfil, y1)
            sol.add(xi, xo, y0, y0 + e, 0.0, za, zb, tag="canal")
            sol.add(xi, xo, y1 - e, y1, 0.0, za, zb, tag="canal")
            sol.add(xo - lado * e, xo, y0, y1, 0.0, za, zb, tag="canal")
            if tipo == "fechado":
                sol.add(xi, xo, y0, y1, H - e - 4.0, H, tag="assento")
                sol.add(xo - lado * e, xo, y0, y1, H, H + 3.5, tag="assento")
                sol.add(xi, xi + lado * (e + 1.5), y0, y1, H, H + 3.5, tag="assento")

    # ---------------- parede traseira --------------------------------------
    ncx = max(5, int(round((2 * ax - 70) / 36.0)))
    furos_tras = grade_furos(-ax + 28, ax - 28, banda + 6, H - 54, ncx, 3, 13.0, 26.0)
    pega = min(0.34 * ax, 95.0)
    furos_tras.append((-pega, pega, H - 42, H - 42 + 26.0))
    painel(sol, -ay, -ay + e, -ax, ax, [(-ax, H), (ax, H)], furos_tras,
           tag="traseira", eixo="x")
    sol.add(-ax, ax, -ay - 2.6, -ay, H - 12.0, H, tag="rebordo")

    # ---------------- parede frontal ---------------------------------------
    dip = 0.72 * hf
    meia = 0.30 * ax
    perfil_frente = [(-ax, hf), (-meia - 26, hf), (-meia, dip), (meia, dip),
                     (meia + 26, hf), (ax, hf)]
    furos_frente = grade_furos(-meia + 8, meia - 8, banda, dip - 14,
                               max(3, int(round(2 * meia / 42.0))), 1, 12.0, 22.0)
    painel(sol, ay - e, ay, -ax, ax, perfil_frente, furos_frente,
           tag="frontal", eixo="x")
    n = 26
    for i in range(n):
        xa = -ax + 2 * ax * i / n
        xb = -ax + 2 * ax * (i + 1) / n
        zt = min(_perfil_em(perfil_frente, xa), _perfil_em(perfil_frente, xb))
        sol.add(xa, xb, ay, ay + 2.6, zt - 10.0, zt, tag="rebordo")

    # ---------------- taliscas ---------------------------------------------
    lug_alt = max(20.0, 0.11 * H)
    lug_len = max(18.0, 0.06 * Y)
    for lado in (-1, 1):
        for cy, tipo, frac in fechados:
            c = frac * Y                       # posicao ABSOLUTA do assento no topo
            sol.add(lado * ax, lado * (ax + sal), c - lug_len / 2, c + lug_len / 2,
                    0.0, lug_alt, tag="talisca")
            sol.add(lado * ax, lado * (ax + sal * 0.55), c - lug_len / 2 - 12,
                    c - lug_len / 2, 0.0, lug_alt * 0.6, tag="talisca")
            sol.add(lado * ax, lado * (ax + sal * 0.55), c + lug_len / 2,
                    c + lug_len / 2 + 12, 0.0, lug_alt * 0.6, tag="talisca")

    s.update(dict(canais=canais, fechados=fechados, perfil=perfil,
                  lug_alt=lug_alt, lug_len=lug_len, y_diag=y_diag))
    return sol, s


def ficha(k):
    sol, s = construir(k)
    X, Y, H, e = s["X"], s["Y"], s["H"], s["e"]
    vol = sol.volume_material()
    s["volume_material_cm3"] = vol
    s["massa_g"] = vol * RHO_PP

    def area_int(z):
        return ((s["Xb"] - 2 * e) * sol.sx(z)) * ((s["Yb"] - 2 * e) * sol.sy(z))

    def integra(z0, z1, n=400):
        h = (z1 - z0) / n
        return sum(area_int(z0 + h * (i + .5)) for i in range(n)) * h / 1e6

    s["litros_boca"] = integra(s["ef"], s["hf"])
    s["litros_total"] = integra(s["ef"], H)
    s["area_projetada_cm2"] = ap = X * Y / 100.0
    s["ton_min"] = ap / 1e4 * 300 * 10.2
    s["ton_max"] = ap / 1e4 * 400 * 10.2
    s["n_triangulos"] = len(sol.pecas) * 12
    return sol, s


if __name__ == "__main__":
    import collections
    for k in ("P", "M", "G"):
        sol, s = ficha(k)
        d = collections.Counter()
        for p in sol.pecas:
            zm = (p.z0 + max(p.z1a, p.z1b)) / 2
            d[p.tag] += p.volume() * sol.sx(zm) * sol.sy(zm) / 1000. * RHO_PP
        print(f"{s['nome']:9s} {s['X']:.0f}x{s['Y']:.0f}x{s['H']:.0f} | painel topo "
              f"{s['Xt']:.0f}x{s['Yt']:.0f} | base {s['Xb']:.0f}x{s['Yb']:.0f} | "
              f"e={s['e']} | {s['massa_g']:5.0f} g | util {s['litros_boca']:5.1f} L | "
              f"total {s['litros_total']:5.1f} L | ninho {s['passo_ninho']:.0f} mm | "
              f"canal {s['v_topo']:.0f} mm | talisca {s['sal']:.0f} mm | "
              f"{s['ton_min']:.0f}-{s['ton_max']:.0f} tf | {s['n_triangulos']} tri")
        print("         ", {t: round(g) for t, g in d.most_common()})
