"""
GRADE DE ENCAIXE (rev.26) — o 4o e o 5o molde.

Peca plana que pousa no aro do M (grade M) ou do G (grade G) e recebe os
copos de n P acoplados lado a lado (2 no M, 3 no G). E a ponte entre o P,
que afunila 7,5 graus para ninhar e por isso tem os pes 30 mm dentro da boca
do grande, e o M/G, que tambem ninham e por isso nao podem ter nada dentro da
boca. Como e uma peca separada, sai antes de ninhar.

  - ANEL: placa de 4 mm do bordo externo do aro ate 12 mm dentro da parede.
    Pousa no patamar do aro e no topo da parede; na frente (mergulho) vence o
    vao apoiada nos cantos altos.
  - ABA: flange de 12 mm que desce dentro da boca, a 1 mm da parede: localiza.
  - BOLSOES: um por copo do P (8 no M, 12 no G), 15 mm acima da placa, com
    as quatro faces a 7,5 graus — o copo do P, que alarga para cima com o
    mesmo angulo, assenta na sola e trava nas faces. Folga 0,4 mm por lado.
  - BARRAS: longitudinais (uma por coluna de bolsoes) e uma transversal,
    12 x 4 mm, ligando bolsoes e anel. O resto e aberto.
"""
import math
from geometria import Contorno, Malha, banda
import modelo
from modelo import parametros, ficha, encaixe_topo, RHO_PP, DEG

T_PLACA = 4.0        # espessura da placa
H_BOLSAO = 15.0      # altura do bolsao acima da placa
E_BOLSAO = 1.8       # parede do bolsao
FOLGA_BOLSAO = 0.4   # por lado, na sola
H_ABA = 12.0         # flange que desce na boca
FOLGA_ABA = 1.0      # aba x face interna da parede do grande
LARG_ANEL_IN = 12.0  # anel para dentro da face interna da parede
LARG_BARRA = 12.0
TAN = math.tan(7.5 * DEG)


def solas_do_copo(kp="P"):
    """Caixa envolvente da sola de cada um dos 4 copos do filho (no chao), no
    sistema do filho: [(x0, x1, y0, y1), ...]."""
    m, s = ficha(kp)
    caixas = {}
    for a, b, c, t in m.tris:
        if t != "pe":
            continue
        for p in (a, b, c):
            if p[2] > 0.5:
                continue
            q = (1 if p[0] > 0 else -1, 1 if p[1] > 0 else -1)
            cx = caixas.setdefault(q, [1e9, -1e9, 1e9, -1e9])
            cx[0] = min(cx[0], p[0]); cx[1] = max(cx[1], p[0])
            cx[2] = min(cx[2], p[1]); cx[3] = max(cx[3], p[1])
    return [tuple(round(v, 2) for v in cx) for cx in caixas.values()], s


def construir(kg):
    g = parametros(kg)
    en = encaixe_topo(kg)
    solas, sP = solas_do_copo(en["filho"])
    m = Malha()
    e = g["e"]
    cont = Contorno(g["Xt"], g["Yt"], g["Rt"], 0.0, passo=2.0, n_arco=16)   # contorno da parede no aro, reto
    n = cont.n
    A = g["aba"]
    # anel
    banda(m, cont, 0, n, lambda i, z: A, lambda i, z: -e - LARG_ANEL_IN, lambda i: 0.0, lambda i: T_PLACA,
          "grade", tampa_ini=False, tampa_fim=False)
    # aba que desce na boca
    banda(m, cont, 0, n, lambda i, z: -e - FOLGA_ABA, lambda i, z: -e - FOLGA_ABA - 2.0,
          lambda i: -H_ABA, lambda i: 0.0, "grade", tampa_ini=False, tampa_fim=False)
    xin = g["Xt"] / 2 - e - LARG_ANEL_IN + 1.0
    yin = g["Yt"] / 2 - e - LARG_ANEL_IN + 1.0
    # bolsoes: um por copo de cada filho
    bolsoes = []
    for c in en["centros"]:
        for (x0, x1, y0, y1) in solas:
            bolsoes.append((c + x0 - FOLGA_BOLSAO, c + x1 + FOLGA_BOLSAO, y0 - FOLGA_BOLSAO, y1 + FOLGA_BOLSAO))
    # barras longitudinais: uma por coluna de bolsoes (x distintos)
    xs_barras = sorted({round((b[0] + b[1]) / 2, 1) for b in bolsoes})
    for xb in xs_barras:
        m.bloco(xb - LARG_BARRA / 2, xb + LARG_BARRA / 2, -yin, yin, 0.0, T_PLACA, "grade")
    m.bloco(-xin, xin, -LARG_BARRA / 2, LARG_BARRA / 2, 0.0, T_PLACA, "grade")   # transversal
    d = H_BOLSAO * TAN                                    # abertura extra na boca do bolsao
    for (x0, x1, y0, y1) in bolsoes:
        # placa sob o bolsao
        m.bloco(x0 - E_BOLSAO, x1 + E_BOLSAO, y0 - E_BOLSAO, y1 + E_BOLSAO, 0.0, T_PLACA, "grade")
        # quatro paredes conicas: face interna abre 7,5 graus subindo; externa acompanha
        z0, z1 = T_PLACA, T_PLACA + H_BOLSAO
        def par(xa, xb_, ya, yb_):
            m.hexa([(xa, ya, z0), (xb_, ya, z0), (xb_, yb_, z0), (xa, yb_, z0)],
                   [(xa - d if xa < (x0 + x1) / 2 else xa + d, ya - d if ya < (y0 + y1) / 2 else ya + d, z1),
                    (xb_ - d if xb_ < (x0 + x1) / 2 else xb_ + d, ya - d if ya < (y0 + y1) / 2 else ya + d, z1),
                    (xb_ - d if xb_ < (x0 + x1) / 2 else xb_ + d, yb_ - d if yb_ < (y0 + y1) / 2 else yb_ + d, z1),
                    (xa - d if xa < (x0 + x1) / 2 else xa + d, yb_ - d if yb_ < (y0 + y1) / 2 else yb_ + d, z1)], "grade")
        par(x0 - E_BOLSAO, x0, y0 - E_BOLSAO, y1 + E_BOLSAO)      # parede em x0
        par(x1, x1 + E_BOLSAO, y0 - E_BOLSAO, y1 + E_BOLSAO)      # parede em x1
        par(x0, x1, y0 - E_BOLSAO, y0)                            # parede em y0
        par(x0, x1, y1, y1 + E_BOLSAO)                            # parede em y1
    info = dict(nome=f"GRADE {kg}", X=g["X"], Y=g["Y"], H=T_PLACA + H_BOLSAO, aba_desce=H_ABA,
                bolsoes=len(bolsoes), barras=len(xs_barras) + 1, filho=en["filho"], n=en["n"],
                z_filho=g["H"] + T_PLACA, folga_aba=FOLGA_ABA, folga_bolsao=FOLGA_BOLSAO,
                massa_g=round(m.volume() * RHO_PP), solas=solas)
    # o bolsao mais externo tem de ficar dentro do anel, e a aba nao pode tocar a guia da coluna
    xmax = max(b[1] for b in bolsoes) + E_BOLSAO
    assert xmax < g["Xt"] / 2 - e - 0.5, f"{kg}: bolsao entra na parede ({xmax:.1f} vs {g['Xt']/2 - e:.1f})"
    assert -e - FOLGA_ABA - 2.0 > g["ponte_out_rel"] + 0.5, f"{kg}: aba da grade toca a guia da coluna"
    return m, info


if __name__ == "__main__":
    for kg in ("M", "G"):
        m, info = construir(kg)
        print(info["nome"], f"{info['X']:.0f} x {info['Y']:.0f} x {info['H']:.0f} mm", f"{info['massa_g']} g",
              info["bolsoes"], "bolsoes", info["barras"], "barras", len(m.tris), "tris")
