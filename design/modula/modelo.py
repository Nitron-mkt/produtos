"""
MODULA rev.25 — familia de organizadores modulares Nitron (3 moldes).

FORMA
  Planta de cantos arredondados; nenhuma quina viva. Parede vazada com o
  PATTERN oficial da marca (grafismo/pattern-nitron.ai), reproduzido exato. Aro em perfil L (aba + saia) que e viga, apoio e pega ao
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

  rev.24: isso vale tambem para o ARO. No ninho a peca de cima entra girada
  180 graus, e a frente rebaixada dela (o mergulho) desce dentro da traseira
  alta da de baixo: um aro em L nessa frente atravessava a parede de baixo em
  10 mm (medido: 22 mil vertices). Desde a rev.24 o aro (aba + saia) so existe
  onde a borda esta na altura cheia; no mergulho a borda e a propria parede,
  lisa e arredondada no molde.

A CADEIA (rev.25) — EM CIMA, nao dentro
  Dois P acoplados lado a lado pousam EM CIMA de um M; tres P em cima de um G.
  O P tem quatro COLUNAS DE CANTO: casca vertical no contorno do aro, do aro ao
  chao, sobre o arco do canto e PE_RETA de cada reta, fechada por uma alma em
  cada ponta e aberta embaixo (sai do molde por baixo: a parede se afasta da
  casca com os 7,5 graus). Sao os unicos pes do P — nao ha copos.
  Quem trava e o grande: PINOS de 7 x 6 x 10 sobem do patamar do aro do M e do
  G, onde cai cada coluna do P, e entram no oco da coluna por baixo. A coluna
  e o proprio bolsao; o P pousa com a sola inteira da coluna no patamar. Os
  pinos sao compativeis com o ninho do M e do G: entram no oco da aba da peca
  de cima (que e aberto embaixo) com 0,9 mm da saia dela.
  Para o pino do meio ter aro embaixo, a frente do M tem um PILAR de altura
  cheia no meio (dois vaos) e a do G tem dois (tres vaos): cada vao fica sob
  um P. Os cantos de M, G e P passam a ter altura cheia; o mergulho e so no vao.
  O P deixa de ninhar (as colunas ocupam o contorno do aro).
"""
import math
from geometria import DEG, Contorno, Malha, banda, perfurada
import grafismo as G

AMOSTRA = [1.3, 20]      # passo de amostragem do contorno / pontos por canto
                         # (rev.19: 1,3 mm — o pattern tem arestas a 65 graus,
                         # e com 2,6 mm a borda do furo saia em escadinha)
SAIDA_GR = 7.5
TAN = math.tan(SAIDA_GR * DEG)
T05 = math.tan(0.5 * DEG)         # saida minima de face "vertical"
T1 = math.tan(1.0 * DEG)          # saida de nervura e de face de postico
# rev.20: a face interna da coluna precisa de saida GRANDE. No ninho profundo a
# peca 3 (mesma orientacao da 1, dois passos acima) tem a coluna no mesmo raio
# da peca 1: com 0,5 grau elas se deslocavam 0,3 mm e as duas cascas de 2 mm
# colidiam. Com 4,5 graus deslocam 2*passo*tan = 2,7 mm (M): passam com folga.
T_COL = math.tan(4.5 * DEG)
RHO_PP = 0.905

# X, Y = cota EXTERNA no aro. Modulo de palete menos 4 mm (396 x 296 cabe 12x
# em 1000 x 1200 com folga; 400 x 300 exatos nao cabem).
# barra = largura da nervura do fundo (= espessura da parede); vao_fundo = furo.
# O P e a peca de coisa pequena: fundo CHAPADO (rev.20). M e G tem fundo em
# grelha, para pesar menos. Parede: 1,8 / 2,0 / 2,3 mm — fina de proposito.
PHI = (1 + 5 ** 0.5) / 2
# rev.25 — a cadeia EM CIMA: n P acoplados (passo X_P) pousam no aro do grande
# com 3 mm de folga por lado: X_g = n*X_P + 6, Y_g = Y_P + 6. H = X / phi.
TAMANHOS = {
    # H = altura TOTAL (chao ate o aro). A cesta e H - perna.
    # rev.23: o P abre pelo lado CURTO (frente de 192), como os cestos de
    # referencia; os acopladores ficam nos lados longos e a fileira tem passo 192.
    "P": dict(nome="MODULA P", X=192.0, Y=289.0, H=179.0, perna=30.0, e=1.8, R=26.0, aba=12.9,
              barra=1.8, vao_fundo=9.0, graf_alma=4.2, graf_espelho=False, fundo_chapado=True,
              acoplador=True, pes_canto=True, ninha=False),
    "M": dict(nome="MODULA M", X=390.0, Y=295.0, H=241.0, perna=50.0, e=2.0, R=26.0, aba=12.4,
              barra=2.0, vao_fundo=18.0, graf_alma=4.0, graf_espelho=False, fundo_chapado=False,
              acoplador=True, sobre=("P", 2)),
    "G": dict(nome="MODULA G", X=582.0, Y=295.0, H=360.0, perna=50.0, e=2.3, R=26.0, aba=12.4,
              barra=2.3, vao_fundo=22.0, graf_alma=4.5, graf_espelho=False, fundo_chapado=False,
              acoplador=True, sobre=("P", 3)),
}
MODULO = {192.0: 200, 289.0: 300, 390.0: 400, 582.0: 600, 596.0: 600}
PINO = dict(w=7.0, alt=10.0, o0=1.2, o1=7.2)   # pino do aro do grande: largura, altura, offsets ao contorno dele
PE_RETA = 8.0        # quanto a coluna de canto avanca pelo trecho reto, alem do arco
E_POSTE = 1.8        # casca do pe de canto (= parede do P)
RAMPA_FRENTE = 14.0  # rampa entre a borda alta e o vao

CANTOS = {"canto_fd": (1, 1), "canto_fe": (-1, 1), "canto_te": (-1, -1), "canto_td": (1, -1)}


def suave(t):
    return t * t * (3 - 2 * t)


def parametros(k):
    s = dict(TAMANHOS[k])
    X, Y, e, R = s["X"], s["Y"], s["e"], s["R"]
    s["H_total"] = s["H"]
    s["hc"] = H = s["H"] - s["perna"]          # altura da cesta
    s["conic"] = con = H * TAN
    aba = s["aba"]
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
    s["r_col_b"] = round(s["r_col_top"] - H * T_COL, 2)   # face interna, no fundo
    s["r_col"] = s["r_col_b"]
    # ---- acoplador lateral (rev.22): macho em T e femea em ranhura, na SAIA ---
    # E o unico lugar da peca onde pode haver relevo por fora: a saia nunca
    # entra em outra peca (no ninho ela fica um passo acima da saia de baixo).
    # Em cada lateral, um macho e uma femea em posicoes espelhadas: o macho
    # direito de A entra na femea esquerda de B, e vice-versa. Passo = X exato.
    s["ac_stem"] = round(e + 0.4, 1)  # haste: atravessa a saia da vizinha (e) e sobra 0,4
    s["ac_cabeca"] = 1.8              # cabeca do T
    s["ac_w_stem"], s["ac_w_cabeca"] = 4.5, 10.0
    s["ac_folga"] = 0.3               # por lado, na ranhura e no bolsao
    s["ac_prof_bolsao"] = round(s["ac_stem"] - e + s["ac_cabeca"] + 0.4, 2)   # cabeca dentro, com folga
    s["ac_saliencia"] = round(s["ac_stem"] + s["ac_cabeca"], 1)
    # o macho vai de ztopo-S+0,6 ate ztopo-2,8: 0,4 abaixo do lintel da vizinha
    s["ac_z1"] = 2.8
    s["ac_y"] = (round(0.29 * s["b"], 1), round(-0.71 * s["b"], 1))   # (macho dir., femea dir.) no aro
    if s.get("acoplador"):
        # fileira de dois: 2X + uma cabeca livre cabe em dois modulos do palete
        assert 2 * X + s["ac_saliencia"] <= 2 * MODULO.get(X, X + 10), \
            f"{k}: macho estoura o modulo do palete"
    # ---- colunas de canto (P) e pinos do aro (M, G) — rev.25 ---------------
    s["y_pe"] = round(s["b"] - PE_RETA, 1)          # onde a coluna termina na lateral
    s["x_pe"] = round(s["ax"] - PE_RETA, 1)         # onde a coluna termina na frente/tras
    s["x_pino"] = round(s["ax"] - 4.0, 1)           # centro do pino que entra na coluna, junto ao arco
    s["pilares"] = []
    s["pinos"] = []
    s["x_cheia"] = s["x_pe"] if s.get("pes_canto") else s["ax"] - 2.0
    s["pilar_meia"] = 0.0
    if s.get("sobre"):
        kf, nf = s["sobre"]
        f = parametros(kf)
        folga_x = (X - nf * f["X"]) / 2
        folga_y = (Y - f["Y"]) / 2
        assert abs(folga_x - 3.0) < 0.01 and abs(folga_y - 3.0) < 0.01, \
            f"{k}: {nf} {kf} nao dao o aro com 3 mm por lado ({folga_x:.1f} / {folga_y:.1f})"
        s["folga_sobre"] = folga_x
        # o pino sobe do patamar C (offsets 0,6..A-4,6) e entra no oco da coluna do
        # filho: a casca dela esta a folga..folga+E_POSTE para dentro da nossa linha
        casca_in = aba - folga_x - E_POSTE            # face interna da casca do filho, em offset nosso
        # cota radial do pino: o mais para fora que cabe com 0,6 da saia da peca
        # de cima no ninho (o passo do G e maior, entao o pino dele recua)
        o1 = round(min(PINO["o1"], (aba - e - pn * TAN) - 0.6, casca_in - 0.3), 1)
        s["pino"] = dict(w=PINO["w"], alt=PINO["alt"], o1=o1, o0=round(max(1.1, o1 - (PINO["o1"] - PINO["o0"])), 1))
        assert s["pino"]["o0"] >= 0.6 + 0.5 and o1 <= aba - 4.6 + 0.01, f"{k}: pino fora do patamar do aro"
        # no ninho o pino entra no oco da aba da peca de cima (aberto embaixo)
        s["f_pino_saia"] = round((aba - e - pn * TAN) - o1, 2)
        assert s["f_pino_saia"] >= 0.6, f"{k}: pino raspa na saia da peca de cima no ninho ({s['f_pino_saia']} mm)"
        s["f_pino_placa"] = round((pn - (e + 1.6 + 1.1 + 0.5)) - PINO["alt"], 1)
        assert s["f_pino_placa"] >= 1.0, f"{k}: pino bate na placa do aro da peca de cima no ninho"
        centros = [-(nf - 1) / 2 * f["X"] + j * f["X"] for j in range(nf)]
        s["centros_sobre"] = centros
        xs = sorted(round(c + sgn * f["x_pino"], 1) for c in centros for sgn in (-1, 1))
        s["pinos"] = [(lado, x) for x in xs for lado in ("frente", "traseira")]
        # o pino tem de cair dentro da coluna do filho: entre a alma (x_pe) e o arco (ax)
        assert f["x_pe"] + 0.5 <= f["x_pino"] - PINO["w"] / 2 and f["x_pino"] + PINO["w"] / 2 <= f["ax"] - 0.3, \
            f"{k}: pino fora da coluna do {kf}"
        assert max(xs) + PINO["w"] / 2 <= s["ax"] - 0.5, f"{k}: pino do canto entra no arco"
        # pilares: entre filhos vizinhos, cobrindo os dois pinos da juncao (e 6 mm de
        # borda alta alem deles: a banda do aro acaba uma amostra depois da mascara)
        s["pilares"] = [round((centros[j] + centros[j + 1]) / 2, 1) for j in range(nf - 1)]
        s["pilar_meia"] = round(f["X"] / 2 - f["x_pino"] + PINO["w"] / 2 + 6.0, 1)
        s["x_cheia"] = round(max(xs) - PINO["w"] / 2 - 6.0, 1)
        s["vao_frente"] = round((s["pilares"][0] - s["pilar_meia"]) - (-s["x_cheia"]), 1) if nf > 1 else 0.0
        s["z_filho"] = s["H"]                                 # a sola da coluna do filho pousa no patamar
        s["engate_pino"] = PINO["alt"]
    if s.get("acoplador"):
        assert s["ac_prof_bolsao"] + 1.8 < aba - e - 0.5, f"{k}: bolsao da femea nao cabe na aba"
    s["canal_out_abs"] = s["Xb"] / 2 + ro_out_b + tout    # face interna da guia
    s["larg_canal"] = round(s["canal_out_abs"] - s["r_col_top"], 1)
    # a ponte fecha o bolsao atras da coluna ate 1,5 mm da parede de cima no
    # ninho: e o que faz o degrau ter 25 mm em vez de 2.
    # rev.21: margem 2,5 (era 1,5) — pela fenda entre a ponte e a parede passa
    # a parede da peca de cima no ninho E a parede do pequeno pendurado.
    s["ponte_out_rel"] = round(-pn * TAN - e - 2.5, 2)    # offset ao contorno, cte em z
    s["larg_ponte"] = round((s["Xb"] / 2 + H * TAN + s["ponte_out_rel"]) - s["r_col_top"], 1)
    assert s["larg_ponte"] > s["larg_canal"] + 4.0, f"{k}: nao sobra guia na ponte"
    s["passo_pilha"] = round(H + hro - s["prof_canal"], 1)

    def r_col(z):
        return s["r_col_b"] + z * T_COL
    s["fn_r_col"] = r_col
    s["saliencia_col_fundo"] = round(s["Xb"] / 2 - s["r_col_b"], 1)
    s["saliencia_col_aro"] = round(s["Xb"] / 2 + H * TAN - s["r_col_top"], 1)

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
    # (5) a moldura do fundo (w_mold) tem de passar por FORA da coluna de baixo
    #     no ninho: assim o rodape e a moldura ficam continuos, sem janela. So a
    #     nervura, que vai ate a moldura, e recortada na sombra da coluna.
    hx_led = s["Xb"] / 2 + s["z_fundo"] * TAN - e - s["w_mold"]
    s["f_gre"] = f_gre = round(hx_led - (r_col(pn) + e), 2)
    assert f_gre > 1.5, f"{k}: a moldura do fundo alcanca a coluna no ninho ({f_gre:.1f} mm)"
    s["r_lim_nerv"] = round(r_col(pn) - 1.5, 2)          # onde a nervura para, na sombra
    # (5b) ninho profundo: coluna da peca 1 x coluna da peca 3
    s["f_col3"] = f_col3 = round(2 * pn * T_COL - e, 2)
    assert f_col3 > 0.3, f"{k}: colunas das pecas 1 e 3 colidem no ninho ({f_col3:.1f} mm)"
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
    """O pattern oficial da marca (grafismo/pattern-nitron.ai), na escala em
    que a alma minima entre furos vale 'graf_alma' — o limite de moldagem."""
    pad, info = G.monta_padrao(cont.perimetro, zlo, zhi, s["graf_alma"], s["graf_espelho"])
    s.update({"graf_" + q: v for q, v in info.items()})
    s["graf_L"] = s["graf_alt_elem"]
    assert s["graf_alma"] > 3.9, \
        f"alma do grafismo fina demais ({s['graf_alma']:.1f} mm)"
    return pad


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

    # rev.25: os cantos ficam na altura cheia; a frente tem zonas cheias (as
    # pontas, onde estao os pes/bolsoes, e os pilares) e VAOS entre elas, cada
    # vao descendo por rampa suave ate hf e mergulhando no meio.
    cheias = sorted([(-1e9, -s["x_cheia"]), (s["x_cheia"], 1e9)] +
                    [(xp - s["pilar_meia"], xp + s["pilar_meia"]) for xp in s["pilares"]])
    vaos = [(cheias[j][1], cheias[j + 1][0]) for j in range(len(cheias) - 1)]

    def perfil_frente(x):
        for xL, xR in vaos:
            if xL <= x <= xR:
                ramp = min(RAMPA_FRENTE, (xR - xL) / 4)
                d = min(x - xL, xR - x)
                f = suave(d / ramp) if d < ramp else 1.0
                g = 0.5 * (1 - math.cos(2 * math.pi * (x - xL) / (xR - xL)))
                return h_geral - f * ((h_geral - hf) + s["mergulho"] * g)
        return h_geral

    def ztopo(i):
        tr, t = cont.amostras[i % n]
        if tr == "frente":
            return perfil_frente(cont.ponto(i % n, H)[0])
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

    # ---- o vazado: o pattern oficial da marca (rev.19) ---------------------
    # Ladrilho do arquivo grafismo/pattern-nitron.ai, reproduzido pixel a pixel
    # (grafismo.Padrao), na escala em que a alma minima vale graf_alma. Continua
    # tudo COPLANAR: nenhum relevo por fora, senao o ninho trava a meio caminho.
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

    # ---- aro: so onde a borda esta na altura cheia (rev.24) ----------------
    # No mergulho a borda e a parede nua: qualquer relevo para fora ali
    # atravessa a parede da peca de baixo no ninho (a peca de cima entra
    # girada, frente sobre traseira). O aro termina no canto, onde a borda
    # comecou a descer 3 mm — a saia de cima ainda passa 1 mm acima do aro de
    # baixo (pn - S = 4).
    A, S = aba, s["saia"]
    com_aro = lambda i: min(ztopo(i), ztopo(i + 1)) >= h_geral - 3.0   # a banda vai ate i+1
    todos = com_aro
    ext = lambda d: (lambda i, z: A - d)
    x_rim = [cont.ponto(i % n, H)[0] for i in range(n)]
    y_rim = [cont.ponto(i % n, H)[1] for i in range(n)]
    lado = [cont.amostras[i % n][0] for i in range(n)]

    def coord(i):                                # coordenada ao longo do lado, no aro
        return x_rim[i % n] if lado[i % n] in ("frente", "traseira") else y_rim[i % n]

    def bloco(l, c0, c1, o0, o1, z0, z1, tag="aro"):
        """Hexaedro num lado reto: coordenada ao longo do lado c0..c1 e offsets
        o0..o1 ao contorno — numeros, ou funcoes de z (a aresta de uma banda
        por amostra abre com a saida; um pe vertical afasta-se da parede)."""
        def val(v, z):
            return v(z) if callable(v) else v

        def quad(z):
            d = z * TAN
            ca, cb = sorted((val(c0, z), val(c1, z)))
            oa, ob = val(o0, z), val(o1, z)
            if l in ("lat_d", "lat_e"):
                sg = 1.0 if l == "lat_d" else -1.0
                xs = sorted(sg * (s["Xb"] / 2 + d + o) for o in (oa, ob))
                return [(xs[0], ca), (xs[1], ca), (xs[1], cb), (xs[0], cb)]
            sg = 1.0 if l == "frente" else -1.0
            ys = sorted(sg * (s["Yb"] / 2 + d + o) for o in (oa, ob))
            return [(ca, ys[0]), (cb, ys[0]), (cb, ys[1]), (ca, ys[1])]
        m.hexa([(x, y, z0) for x, y in quad(z0)], [(x, y, z1) for x, y in quad(z1)], tag)

    def coord_z(i):
        """A coordenada da amostra i ao longo do lado, como funcao de z."""
        ax_ = 0 if lado[i % n] in ("frente", "traseira") else 1
        return lambda z: cont.ponto(i % n, z)[ax_]

    emitir(todos, ext(2.0), -e, lambda i: ztopo(i) - e - 1.6, lambda i: ztopo(i) - 1.6, "aro")
    emitir(todos, ext(3.2), -e + 1.2, lambda i: ztopo(i) - 1.6, lambda i: ztopo(i) - 0.5, "aro")
    emitir(todos, ext(4.6), -e + 2.6, lambda i: ztopo(i) - 0.5, ztopo, "aro")
    # ---- pinos do aro (rev.25): sobem do patamar onde cai cada coluna do filho --
    for l, c in s["pinos"]:
        pn_ = s["pino"]
        bloco(l, c - pn_["w"] / 2, c + pn_["w"] / 2, pn_["o1"], pn_["o0"], H - 1.0, H + pn_["alt"], "aro")

    # ---- acoplador lateral (rev.22) e postes do aro (rev.24) ---------------
    # rev.24: tudo aqui e emitido com COORDENADAS EXATAS (blocos), nao por
    # amostra do contorno: a folga de projeto e 0,3 mm e a amostra e 1,3 mm —
    # por banda, macho e ranhura saiam ate 1,3 mm fora do lugar e a malha
    # mostrava interferencia que o projeto nao tem.
    fg = s["ac_folga"]; ws, wc = s["ac_w_stem"], s["ac_w_cabeca"]
    prof = s["ac_prof_bolsao"]
    feats = []
    if s.get("acoplador"):
        ym, yf = s["ac_y"]
        feats = [("lat_d", ym, "macho"), ("lat_d", yf, "femea"),
                 ("lat_e", yf, "macho"), ("lat_e", ym, "femea")]
    ranhuras = [(l, c) for l, c, t in feats if t == "femea"]
    meia_r = ws / 2 + fg
    larga = meia_r + AMOSTRA[0] * 1.01

    def na_ranhura_larga(i):
        return any(lado[i % n] == l and abs(coord(i) - c) < larga for l, c in ranhuras)

    def no_pe(i):
        """A amostra esta no pe de canto: o arco, ou PE_RETA mm da reta vizinha."""
        if not s.get("pes_canto"):
            return False
        l = lado[i % n]
        if l.startswith("canto"):
            return True
        return abs(coord(i)) > (s["x_pe"] if l in ("frente", "traseira") else s["y_pe"])
    # a saia por banda, parando uma amostra ANTES da ranhura; o que falta ate a
    # aresta exata da ranhura e completado por bloco. Onde ha pe de canto, a
    # casca do pe faz o papel da saia.
    emitir(lambda i: com_aro(i) and not na_ranhura_larga(i) and not no_pe(i), ext(0.0), A - e,
           lambda i: ztopo(i) - S, lambda i: ztopo(i) - 1.6, "aro")
    emitir(todos, ext(0.0), A - 2.0,
           lambda i: ztopo(i) - 2.6, lambda i: ztopo(i) - 1.4, "aro")
    for l, c in ranhuras:
        idx = [i for i in range(n) if lado[i] == l and abs(coord(i) - c) < larga]
        j0, k = min(idx), max(idx) + 1              # a banda vai ate j0 e recomeca em k
        ja, jb = (j0, k) if coord(j0) < coord(k) else (k, j0)
        bloco(l, coord_z(ja), c - meia_r, A, A - e, H - S, H - 1.6)
        bloco(l, c + meia_r, coord_z(jb), A, A - e, H - S, H - 1.6)
        bloco(l, c - meia_r, c + meia_r, A, A - e, H - 2.4, H - 1.6)          # lintel
        # femea: parede de fundo do bolsao e duas bochechas, dentro do oco da aba
        bloco(l, c - wc / 2 - fg, c + wc / 2 + fg, A - e - prof, A - e - prof - e, H - S, H - 1.6)
        bloco(l, c - wc / 2 - fg - e, c - wc / 2 - fg, A - e + 0.3, A - e - prof - e, H - S, H - 1.6)
        bloco(l, c + wc / 2 + fg, c + wc / 2 + fg + e, A - e + 0.3, A - e - prof - e, H - S, H - 1.6)
    for l, c, t in feats:
        if t != "macho":
            continue
        # macho: haste e cabeca do T, para fora da saia. Termina 0,4 abaixo do
        # lintel da vizinha (rev.24; antes invadia o lintel em 0,8 mm).
        bloco(l, c - ws / 2, c + ws / 2, A + s["ac_stem"], A - 0.3, H - S + 0.6, H - s["ac_z1"])
        bloco(l, c - wc / 2, c + wc / 2, A + s["ac_saliencia"], A + s["ac_stem"] - 0.3,
              H - S + 0.6, H - s["ac_z1"])
    # ---- colunas de canto (rev.25) ------------------------------------------
    # Casca vertical (a face externa e a linha do aro, reta ate o chao) sobre
    # o arco do canto e PE_RETA de cada reta; almas nas duas pontas fechando
    # ate a parede. Oco aberto embaixo — o postico entra por baixo e alarga
    # descendo, porque a parede se afasta da casca com os 7,5 graus. O oco e o
    # bolsao onde entra o pino do aro do grande.
    if s.get("pes_canto"):
        rim = lambda z: A + (H - z) * TAN                  # linha do aro, em offset
        emitir(lambda i: no_pe(i) and com_aro(i), lambda i, z: rim(z),
               lambda i, z: rim(z) - E_POSTE, lambda i: -perna, lambda i: ztopo(i) - 1.4, "pe")
        for sx_, sy_ in CANTOS.values():
            lf = "frente" if sy_ > 0 else "traseira"
            ll = "lat_d" if sx_ > 0 else "lat_e"
            xa = sx_ * s["x_pe"]
            bloco(lf, xa, xa - sx_ * E_POSTE, -0.3, lambda z: rim(z) - E_POSTE + 0.3, -perna, H - 1.4, "pe")
            ya = sy_ * s["y_pe"]
            bloco(ll, ya, ya - sy_ * E_POSTE, -0.3, lambda z: rim(z) - E_POSTE + 0.3, -perna, H - 1.4, "pe")

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
        if s.get("pes_canto"):                     # rev.25: as colunas de canto sao os pes
            return False
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

    # rev.20: rodape e moldura CONTINUOS em toda a volta. A coluna de baixo passa
    # por dentro deles no ninho (f_gre); so a nervura e recortada na sombra dela.
    livre = lambda i: True
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
    if s.get("pes_canto"):
        # sola das quatro colunas: casca de E_POSTE sobre arco + 2*PE_RETA
        s["apoio_cm2"] = round(4 * E_POSTE * (math.pi / 2 * (s["R"] - E_POSTE / 2) + 2 * PE_RETA) / 100.0, 1)
    else:
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

    r_lim = s["r_lim_nerv"]
    meia_jan = wc + rc + 1.0

    def na_sombra(x, y):
        """Sombra da coluna de baixo no ninho (posicoes espelhadas): ali a
        nervura para antes da moldura. Quem nao ninha tem fundo inteiro."""
        if not s.get("ninha", True):
            return False
        return abs(x) > r_lim and any(abs(y - yj) < meia_jan for yj in yc_jan)

    def dentro_fundo(x, y):
        """Planta util do fundo: canto arredondado, menos os quatro copos e
        menos a sombra das colunas."""
        if abs(x) > hx or abs(y) > hy:
            return False
        if abs(x) > xw_v and abs(y) > yw_v:
            return False
        if na_sombra(x, y):
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

    if s.get("fundo_chapado"):
        # Laje inteira entre a moldura e os copos, em retangulos convexos que
        # nao se sobrepoem (a massa e por divergencia). As quatro sombras das
        # colunas ficam abertas: e por ali que a coluna de baixo sobe no ninho.
        lajes = [(-xw_v, xw_v, -hy - 1.0, hy + 1.0)]
        for sx in (+1, -1):
            x0, x1 = sorted((sx * xw_v, sx * r_lim))
            lajes.append((x0, x1, -yw_v, yw_v))
            # entre r_lim e a moldura, so fora das sombras
            cortes = sorted([(yj - meia_jan, yj + meia_jan) for yj in yc_jan])
            ya = -yw_v
            for c0, c1 in cortes + [(yw_v, yw_v)]:
                if c0 > ya + 1.0:
                    x0, x1 = sorted((sx * r_lim, sx * (hx + 1.0)))
                    lajes.append((x0, x1, ya, min(c0, yw_v)))
                ya = max(ya, c1)
        for x0, x1, y0, y1 in lajes:
            if x1 - x0 > 0.5 and y1 - y0 > 0.5:
                m.prisma([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], zf, zt, "fundo")

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


def confere_ninho(m, s, k=1):
    """Poe a peca k passos acima (girada 180 graus se k for impar) e confere se
    algum vertice da base/fundo dela fica abaixo do topo do fundo da peca de
    baixo SEM estar dentro de um copo. E o teste que faltou da rev.05 a rev.17;
    a rev.20 passou a rodar tambem para k=2 (mesma orientacao)."""
    pn, perna = s["passo_ninho"], s["perna"]
    zt = s["z_fundo"] + s["ef"]
    viol, total = 0, 0
    giro = (k % 2 == 1)
    for a, b, c, tag in m.tris:
        if tag not in ("saia", "pe", "fundo"):
            continue
        for p in (a, b, c):
            zA = p[2] + k * pn
            if zA >= perna + zt - 0.01:
                continue
            total += 1
            x, y = (-p[0], -p[1]) if giro else (p[0], p[1])
            if not em_copo(s, x, y, zA - perna, folga=0.05):
                viol += 1
                if viol <= 5:
                    print(f"    ninho k={k}: {tag} ({p[0]:.1f}, {p[1]:.1f}, {p[2]:.1f}) -> z_baixo {zA - perna:.1f}")
    return viol, total


def encaixe_topo(kg):
    """n filhos acoplados em cima de 'kg': onde ficam, os pinos e as folgas."""
    g = parametros(kg)
    kf, nf = g["sobre"]
    f = parametros(kf)
    casca_in = g["aba"] - g["folga_sobre"] - E_POSTE
    return dict(filho=kf, n=nf, centros=g["centros_sobre"], z_filho=g["z_filho"],
                folga=g["folga_sobre"], pinos=list(g["pinos"]), pilares=list(g["pilares"]),
                pilar_larg=round(2 * g["pilar_meia"], 1), vao_frente=g["vao_frente"],
                engate=g["engate_pino"], pino=dict(g["pino"]),
                folga_pino_casca=round(casca_in - g["pino"]["o1"], 2),
                folga_pino_arco=round(f["ax"] - (f["x_pino"] + PINO["w"] / 2), 2),
                folga_pino_alma=round((f["x_pino"] - PINO["w"] / 2) - f["x_pe"], 2),
                f_pino_saia=g["f_pino_saia"], f_pino_placa=g["f_pino_placa"])


def confere_aro_ninho(m, s):
    """rev.24: no ninho, todo vertice do aro da peca de cima que fique abaixo do
    aro de baixo tem de estar DENTRO da parede de baixo (nunca atravessa-la).
    E o teste que faltava desde a rev.01 — a frente rebaixada com aba em L
    atravessava a traseira de baixo em 10 mm."""
    H, perna, pn, e = s["hc"], s["perna"], s["passo_ninho"], s["e"]
    Xb, Yb, Rb = s["Xb"], s["Yb"], s["Rb"]

    def dist_ext(x, y, z):
        d = z * TAN
        hx, hy = Xb / 2 + d, Yb / 2 + d
        qx, qy = abs(x) - (hx - Rb), abs(y) - (hy - Rb)
        if qx > 0 and qy > 0:
            return math.hypot(qx, qy) - Rb
        return max(qx, qy) - Rb
    viol = tot = 0
    for a, b, c, tag in m.tris:
        if tag != "aro":
            continue
        for p in (a, b, c):
            z = p[2] - perna + pn
            if z >= H - 0.5:
                continue
            tot += 1
            if dist_ext(-p[0], -p[1], z) > -e + 0.05:
                viol += 1
    return viol, tot


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
    if s.get("sobre"):
        s["encaixe"] = encaixe_topo(k)
    if s.get("ninha", True):
        viol, total = confere_ninho(m, s, 1)
        viol2, total2 = confere_ninho(m, s, 2)
        viol3, total3 = confere_aro_ninho(m, s)
        s["ninho_viol"], s["ninho_pts"] = viol + viol2 + viol3, total + total2 + total3
        assert viol == 0, f"{k}: {viol} vertices da base atravessam a peca de baixo no ninho"
        assert viol2 == 0, f"{k}: {viol2} vertices da base atravessam a peca DOIS passos abaixo"
        assert viol3 == 0, f"{k}: {viol3} vertices do aro atravessam a parede de baixo no ninho"
    else:
        s["ninho_viol"], s["ninho_pts"] = 0, 0
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
