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
SAIDA_GR = 7.5
TAN = math.tan(SAIDA_GR * DEG)
RHO_PP = 0.905

# ripa = largura do material entre furos; vao = largura do furo.
# O P e o mais fechado de proposito: e a peca que vai a vista em casa e a que
# guarda coisa pequena. O G e o mais aberto: e caixa de estoque.
TAMANHOS = {
    # H = altura TOTAL (chao ate o aro). A cesta e H - perna.
    "P": dict(nome="MODULA P", X=300.0, Y=200.0, H=200.0, perna=50.0, e=1.8, R=26.0,
              ripa=15.0, vao=6.0, fileiras=4, trav=10.0, barra=9.0, vao_fundo=6.0),
    "M": dict(nome="MODULA M", X=400.0, Y=300.0, H=250.0, perna=50.0, e=2.0, R=36.0,
              ripa=12.0, vao=10.0, fileiras=3, trav=9.0, barra=7.5, vao_fundo=11.0),
    "G": dict(nome="MODULA G", X=600.0, Y=400.0, H=300.0, perna=50.0, e=2.3, R=46.0,
              ripa=12.0, vao=16.0, fileiras=3, trav=9.0, barra=7.5, vao_fundo=17.0),
}


def suave(t):
    return t * t * (3 - 2 * t)


def parametros(k):
    s = dict(TAMANHOS[k])
    X, Y, e, R = s["X"], s["Y"], s["e"], s["R"]
    s["H_total"] = s["H"]
    s["hc"] = H = s["H"] - s["perna"]          # altura da cesta
    s["conic"] = con = H * TAN
    s["folga_pe"] = fp = 3.0                      # o pe passa por fora da saia
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
    s["z_fundo"] = 6.0
    s["ef"] = e + 0.5

    s["sal_pe"] = round(fp + aba + con, 1)        # o quanto o pe avanca
    # metade do trecho reto da lateral (constante em qualquer altura)
    s["b"] = s["Yt"] / 2 - s["Rt"]
    s["ax"] = s["Xt"] / 2 - s["Rt"]
    s["larg_pe"] = 0.0                            # definido abaixo, a partir de b
    s["h_ress"] = round(7.0 + 0.010 * H, 1)
    s["h_pe"] = s["perna"]
    s["cone_pe"] = 6.5                          # recuo do topo da perna, por lado
    s["y_pe_f"] = round(0.86 * s["b"], 1)
    s["y_pe_t"] = round(-0.40 * s["b"], 1)
    dif = s["y_pe_f"] + s["y_pe_t"]               # |c| - |d|
    s["larg_pe"] = round(dif - 8.0, 1)            # perna comprida, sobra 8 mm de folga
    s["larg_ress"] = round(min(s["larg_pe"] - 14, 0.55 * dif), 1)
    s["etiqueta"] = round(0.24 * X)
    f_ress = dif - (s["larg_pe"] + s["larg_ress"]) / 2
    f_pe = dif - s["larg_pe"]
    assert f_ress > 2, f"{k}: pe girado bate na crista (folga {f_ress:.1f} mm)"
    assert f_pe > 2, f"{k}: pe girado bate no pe de baixo (folga {f_pe:.1f} mm)"
    assert s["saia"] < s["passo_ninho"] - 2, f"{k}: saia nao cabe no passo do ninho"
    # a perna da peca i+2 tem de envolver a da peca i, que esta a 2 passos
    s["passo_perna"] = round(e / (s["cone_pe"] / s["perna"]), 1)
    assert s["passo_perna"] < 2 * s["passo_ninho"] - 3, \
        f"{k}: perna nao ninha ({s['passo_perna']:.0f} > {2*s['passo_ninho']:.0f} mm)"
    s["folga_giro"] = round(min(f_ress, f_pe), 1)
    return s


def ritmo(meia, passo_alvo, larg):
    """Posicoes simetricas em torno de zero dentro de [-meia, meia]."""
    nj = max(1, int(round(meia / passo_alvo)))
    p = meia / nj
    return [(j + 0.5) * p for j in range(nj)], p


def construir(k):
    s = parametros(k)
    X, Y, e = s["X"], s["Y"], s["e"]
    H = s["hc"]                    # dentro daqui, H e a altura da CESTA
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
    w_trav = s["trav"]
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

    # ---- saia: a parede continua para baixo, com recortes em arco ---------
    # Como ela tem a MESMA conicidade da parede, ninha junto com o corpo — e e
    # isso que deixa o pe integrado em vez de pendurado.
    perna = s["perna"]
    h_arco = perna * 0.56
    y_pes = (s["y_pe_f"], s["y_pe_t"])
    meia_pe = s["larg_pe"] / 2

    def sobre_perna(i):
        """Trecho em que a saia desce reta ate o chao (o pe)."""
        tr, _ = cont.amostras[i % n]
        if tr not in ("lat_d", "lat_e"):
            return False
        y = cont.y_de(i)
        return any(abs(y - yc) <= meia_pe for yc in y_pes)

    # poucos arcos, largos e circulares; entre eles sobra o pe da saia
    alvo_ciclo = 92.0 + 0.11 * X
    n_arcos = max(6, int(round(cont.perimetro / alvo_ciclo)))
    ciclo = cont.perimetro / n_arcos
    w_pe_saia = 0.30 * ciclo

    def z_saia(i):
        if sobre_perna(i):
            return -perna
        sm = (cont.s[i % n] + cont.s[(i % n) + 1]) / 2
        t = sm % ciclo
        if t < w_pe_saia / 2 or t > ciclo - w_pe_saia / 2:
            return -perna
        u = (t - w_pe_saia / 2) / (ciclo - w_pe_saia)      # 0..1 dentro do vao
        return -perna + h_arco * math.sqrt(max(0.0, 1 - (2 * u - 1) ** 2))

    # nas 4 posicoes de apoio a saia se abre para fora conforme desce, ate
    # alcancar o envelope na base: e ali que ela pousa na crista da peca de baixo
    sal = X / 2 - (s["Xb"] / 2 - perna * TAN) - 2.0
    rampa_pe = s["larg_pe"] * 0.85

    def fator_pe(i):
        tr, _ = cont.amostras[i % n]
        if tr not in ("lat_d", "lat_e"):
            return 0.0
        y = cont.y_de(i % n)
        melhor = 0.0
        for yc in y_pes:
            d = abs(y - yc)
            if d <= meia_pe:
                melhor = 1.0
            elif d <= meia_pe + rampa_pe:
                melhor = max(melhor, 1 - suave((d - meia_pe) / rampa_pe))
        return melhor

    def off_pe(i, z):
        f = fator_pe(i)
        return 0.0 if f <= 0 else sal * f * suave(min(1.0, max(0.0, -z / perna)))

    banda(m, cont, 0, n,
          lambda i, z: off_pe(i, z),
          lambda i, z: off_pe(i, z) - e,
          z_saia, lambda i: 0.0, "saia", tampa_ini=False, tampa_fim=False)
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
              f"ninho {s['passo_ninho']:.0f} mm (perna {s['passo_perna']:.0f}) | "
              f"cubagem 10p {10*s['H']/(s['H']+9*s['passo_ninho']):.1f}x | "
              f"folga do giro {s['folga_giro']:.0f} mm | {s['n_triangulos']} tri")
