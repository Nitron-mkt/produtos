# -*- coding: utf-8 -*-
"""Chrono v3 — revisao de moldabilidade. Solido B-rep (OpenCASCADE).

O que mudou em relacao a v2, tudo a pedido da ferramentaria:
  · 1,5 grau de saida em TODA parede vertical (pedido: 1 a 3)
  · arestas abauladas em vez de cantos vivos
  · escala dos dias com o VAO igual entre numeros (o "espaco do zero" que
    sobrou de 01..09 foi redistribuido nos 31)
  · a concha das 12 h nao aflora mais no piso do rebaixo: a cunha foi enchida
    e o piso ficou plano
  · detente centrado na faixa do rebaixo (r 10,10) e com base de 2,00 mm;
    as 12 covinhas da rodinha no mesmo lugar, invertidas
  · TODA letra e numero: 1,50 de altura de caractere, 0,10 de AUTO RELEVO
  · ponteira: "D" removido, "M" virou "MES", icone de gravado para auto relevo

Convencao de saida: molde abre em +Y, particao na face de baixo de cada peca.
Logo, parede externa ESTREITA para cima e furo ALARGA para cima.

  python3 build_v3.py
"""
import sys, os, numpy as np, cadquery as cq
from math import pi, radians, degrees, cos, sin, tan
from shapely.geometry import Polygon as SP, LineString as SL
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'medicao_v2'))
import params as P
from lib_v3 import (arredonda, limpa_contorno, glifos, largura, prisma, prisma_wire, gota_wire,
                    ret_wire, estadio_wire, rev_perfil,
                    place, deitado, rev, cil, cone,
                    esfera, fundir, tirar, letras, aplica_letras, angulos_dias, arred,
                    valido, face_sp, VARIANTES, mergulha)
import icone_v3

STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step')
os.makedirs(STEP, exist_ok=True)
r_ = P.rec

# ===================================================== M01 — sobre a valvula
def m01():
    print('  M01 acrescimos na valvula')
    # --- SOMAR 1: enchimento da cunha das 12 h + mesa dos dias ---------------
    # a concha aflorava no piso do rebaixo (o "rebaixo" do anexo 01). Enche a
    # cunha inteira de CHAPA_Y0 ate a face: a face de baixo naquela regiao nao
    # passa de 35,400 (medido), entao nada e acrescentado por baixo e a parede
    # fica uniforme em 1,83 mm, igual ao resto da chapa.
    pol = [(0.0, 0.0)] + [(P.CUNHA_RE*cos(radians(a)), P.CUNHA_RE*sin(radians(a)))
                          for a in np.linspace(P.CUNHA_A0, P.CUNHA_A1, 96)]
    ench = deitado(SP(pol), P.FACE - P.CHAPA_Y0, P.CHAPA_Y0)
    mesa_topo = P.FACE + P.MESA_H
    mesa = rev([(P.MESA_RI,           P.FACE - 0.60),
                (P.MESA_RE,           P.FACE - 0.60),
                (P.MESA_RE,           P.FACE),
                (P.MESA_RE - r_(P.MESA_H), mesa_topo),
                (P.MESA_RI + r_(P.MESA_H), mesa_topo),
                (P.MESA_RI,           P.FACE)])
    somar1 = fundir([ench, mesa])
    # 0,08 e nao 0,15: a mesa tem 0,18 de parede e o raio de 0,15 deixava so
    # 0,03 de aresta reta — aresta curta que trava a importacao
    somar1 = arred(somar1, 0.08,
                   lambda e: e.Center().y > P.FACE + 0.01, 'mesa: aresta de topo')
    # os 31 numerais entram AQUI, fundidos na mesa: assim o arquivo abre como UM
    # solido no CAD do cliente, e nao como 53 corpinhos soltos boiando

    # --- SUBTRAIR 2: o rebaixo, com saida (alarga para cima) -----------------
    piso = P.FACE - P.REB_H
    # O corte entra ATE r 5,00, bem dentro do poste. Parando exatamente em
    # POST_R sobrava uma aleta de 0,03 mm de espessura e 0,60 de altura entre o
    # corte reto e o poste ja com saida — parede vertical e, pior, quebradica.
    reb = rev([(5.00,                   piso),
               (P.REB_RE - r_(P.REB_H), piso),
               (P.REB_RE,               P.FACE),
               (P.REB_RE,               P.FACE + 0.5),
               (5.00,                   P.FACE + 0.5)])
    # o canto piso/parede do rebaixo e concavo: abaula para o fluxo e a extracao
    reb = arred(reb, P.RAIO_FINO, lambda e: abs(e.Center().y - piso) < 1e-6, 'rebaixo: canto do piso')

    ang, arco, folga = angulos_dias(cap=P.DIA_CAP)
    somar1 = aplica_letras(somar1, [(radians(ang[d-1]), str(d)) for d in range(1, 32)],
                           P.DIA_R, mesa_topo, cap=P.DIA_CAP, nome='mesa: 31 numerais')

    # --- SUBTRAIR 2 leva as 2 covinhas do detente descontadas: assim o corte do
    # rebaixo JA deixa as duas molas de pe, e some um passo da receita ---------
    # --- SOMAR 3: so o poste -------------------------------------------------
    # pe do poste com concordancia, nao canto vivo. O raio nao e o padrao de
    # 0,30: a folga radial para a rodinha e de 0,20 e a face de baixo dela passa
    # a 0,02 do piso, entao um raio de 0,30 encostaria nela. 0,15 deixa 0,125 de
    # folga no ponto critico — medido, nao arbitrado.
    rc = P.RAIO_FINO
    cx, cy = P.POST_R + rc, piso + rc
    # r(y) LINEAR. Antes o recuo era calculado ate POST_TOP e aplicado em
    # POST_TOP-0,30: o cone saia com 1,884 grau em vez de 1,500. Era esse o
    # "angulo quebrado" — e bem na parede onde a rodinha gira.
    rp = lambda y: P.POST_R - r_(y - cy)
    rtop = rp(P.POST_TOP - P.CHANFRO)
    meia = (cx - rc*0.7071067811865476, cy - rc*0.7071067811865476)
    poste = rev_perfil(cq.Workplane("XY")
        .moveTo(P.POST_R + rc, P.CHAPA_Y0)
        .lineTo(P.POST_R + rc, piso)
        .threePointArc(meia, (P.POST_R, piso + rc))          # pe em ARCO R0,15
        .lineTo(rtop, P.POST_TOP - P.CHANFRO)
        .lineTo(rtop - P.CHANFRO, P.POST_TOP)                # chanfro de 45,000
        .lineTo(P.FURO_R, P.POST_TOP)
        .lineTo(P.FURO_R, P.CHAPA_Y0))
    yc = piso + P.DET_ALT - P.DET_ESF
    det = [esfera(P.DET_ESF, P.DET_R*cos(radians(a)), yc, P.DET_R*sin(radians(a)))
           for a in (0, 180)]
    reb = tirar(reb, det)          # o cortador guarda as molas
    somar3 = poste
    print('      dias: cap %.2f mm · vao igual de %.2f graus = %.2f mm entre bordas'
          % (P.DIA_CAP, folga, radians(folga)*P.DIA_R))

    # --- SUBTRAIR 4: furo passante, alargando para cima ----------------------
    # UM perfil so. Montado como cone + chanfro separados, as duas superficies
    # coincidiam no mesmo raio, o fuse recusava, saia composto de 2 solidos — e
    # cortar com esse composto virava a peca do avesso (volume negativo).
    # r(y) LINEAR aqui tambem: calculado ate POST_TOP e aplicado em
    # POST_TOP-FURO_CH, o furo saia com 1,617 grau em vez de 1,500.
    rf = lambda y: P.FURO_R + r_(y - P.CHAPA_Y0)
    y0 = P.CHAPA_Y0 - 2.0
    rt = rf(P.POST_TOP - P.FURO_CH)
    furo = rev([(0.0,            y0),
                (rf(y0),         y0),
                (rt,             P.POST_TOP - P.FURO_CH),
                (rt + P.FURO_CH, P.POST_TOP),                 # chanfro de 45,000
                (rt + P.FURO_CH, P.POST_TOP + 0.5),
                (0.0,            P.POST_TOP + 0.5)])
    return somar1, reb, somar3, furo

# ===================================================== M02 — rodinha dos meses
def m02():
    print('  M02 rodinha dos meses')
    y0, y1 = P.ARO_Y0, P.ARO_Y1
    h = P.ARO_ESP
    aro = rev([(P.ARO_RI,            y0),
               (P.ARO_RE,            y0),
               (P.ARO_RE - r_(h),    y1),
               (P.ARO_RI + r_(h),    y1)])
    # 12 entalhes de unha: cavidade no molde de cima, alarga para cima
    ent = [cone(P.ENT_RC, P.ENT_RC + r_(h + 2.0), y0 - 1.0, y1 + 1.0,
                P.ENT_R*cos(radians(90 + (i + 0.5)*30)),
                P.ENT_R*sin(radians(90 + (i + 0.5)*30))) for i in range(12)]
    # 12 covinhas: MESMA esfera do detente da valvula, so que invertida.
    # Cada uma e referida a sua propria face, entao a folga de montagem de
    # 0,02 mm se mantem e o conjunto nao trava.
    yc = y0 + P.DET_ALT - P.DET_ESF
    cov = [esfera(P.DET_ESF, P.DET_R*cos(radians(90 + i*30)), yc, P.DET_R*sin(radians(90 + i*30)))
           for i in range(12)]
    corpo = tirar(aro, ent + cov)
    corpo = arred(corpo, P.RAIO_FINO,
                  lambda e: abs(e.Center().y - y1) < 1e-6 or abs(e.Center().y - y0) < 1e-6,
                  'rodinha: arestas de face')
    return aplica_letras(corpo, [(radians(90 + i*30), str(i + 1)) for i in range(12)],
                         P.MES_R, y1, cap=P.MES_CAP, nome='rodinha: 12 numerais')

# ===================================================== M03 — ponteira
def gota():
    return gota_wire(P.BULBO_R, P.BULBO_OFF, P.NARIZ_R, P.NARIZ_Y)

def ret_arred(r0, r1, meia, rc):
    return ret_wire(r0, r1, meia, rc)

def m03():
    print('  M03 ponteira')
    h = P.PONT_ESP
    cubo = cone(P.CUBO_R, P.CUBO_R - r_(h), P.CUBO_Y0, P.TOPO)
    # pino: pendura abaixo da particao, entao estreita para BAIXO. A farpa
    # continua sendo undercut de projeto — e ela que segura a ponteira.
    pino = rev([(2.05,                       P.CUBO_Y0),
                (P.PINO_RE,                  P.CUBO_Y0),
                (P.PINO_RE - r_(P.CUBO_Y0 - P.CHAPA_Y0), P.CHAPA_Y0),
                (P.FARPA_R,                  P.CHAPA_Y0),
                (P.FARPA_R - tan(radians(30.0))*(P.CHAPA_Y0 - P.PINO_Y1), P.PINO_Y1),  # rampa de 30,000
                (2.35,                       P.PINO_Y1),
                (2.35 - r_(P.CHAPA_Y0 - P.PINO_Y1), P.CHAPA_Y0),   # furo interno tambem sai
                # fecho do furo interno sob o cubo: 5,00 graus redondos. Antes
                # saia 5,101 — angulo quebrado, que e justo o que a ferramentaria
                # pediu para nao existir.
                (2.35 - r_(P.CHAPA_Y0 - P.PINO_Y1) - tan(radians(5.0))*(P.CUBO_Y0 - P.CHAPA_Y0),
                 P.CUBO_Y0)])
    # abaula o contorno da gota ANTES de furar: depois da janela e dos drenos o
    # OCC ja nao aceita o conjunto de arestas de uma vez
    lam = prisma_wire(gota(), h, P.SAIDA)
    lam = arred(lam, P.RAIO, lambda e: abs(e.Center().z - h) < 1e-6, 'gota: aresta de topo')
    lam = arred(lam, P.RAIO_FINO, lambda e: abs(e.Center().z) < 1e-6, 'gota: aresta de baixo')
    lamina = place(lam, radians(90), 0.0, P.TOPO, h)
    corpo = fundir([cubo, pino, lamina])

    fendas = []
    for i in range(P.FENDAS):
        a = radians(45 + i*360.0/P.FENDAS)
        # Fenda com a RAIZ EM MEIA-CANA, nao em canto vivo. A perna do snap
        # flexiona na montagem e a raiz da fenda e onde a tensao se concentra:
        # canto vivo ali e onde perna de encaixe trinca. Meia-cana de 0,35
        # (= meia largura) e o alivio classico e nao custa nada.
        fendas.append(place(prisma_wire(estadio_wire(0.0, 4.20 - P.FENDA_W/2, P.FENDA_W/2),
                                        P.CUBO_Y0 - P.PINO_Y1 + 0.2, P.SAIDA),
                            a, 0.0, P.CUBO_Y0, P.CUBO_Y0 - P.PINO_Y1 + 0.2))
    jp = ret_arred(P.JAN_R0, P.JAN_R1, P.JAN_M, P.JAN_RC)
    # janela passante: alarga para cima, como todo furo
    jan = place(prisma_wire(jp, h + 0.6, -P.SAIDA), radians(90), 0.0, P.TOPO + 0.3, h + 0.6)
    # O chanfro postico de 0,45 em volta da janela SAIU: ele aparecia como um
    # ressalto em volta do furo, que e o que incomodou. No lugar dele, raio de
    # 0,30 nas duas arestas da janela — a de cima e a de baixo.
    corpo = tirar(corpo, fendas + [jan])
    def borda(y):
        def f(e):
            c = e.Center(); r = (c.x**2 + c.z**2) ** 0.5
            return abs(c.y - y) < 1e-6 and 7.0 < r < 13.0
        return f
    corpo = arred(corpo, P.JAN_RAIO, borda(P.TOPO),    'janela: aresta de cima')
    corpo = arred(corpo, P.JAN_RAIO, borda(P.CUBO_Y0), 'janela: aresta de baixo')

    # "D" saiu; "M" virou "MES"; icone de gravado para AUTO RELEVO
    corpo = aplica_letras(corpo, [(radians(90), 'MÊS')], P.MES_TXT_R, P.TOPO, nome='ponteira: MÊS')
    # contorno ja vem com o canto de 0,10 arredondado (ver icone_v3)
    for sp in icone_v3.laminas():
        q = limpa_contorno(sp)
        for ov, sa in VARIANTES:
            sa = P.LETRA_SAIDA if sa is None else sa
            try:
                o = corpo.fuse(deitado(q, P.LETRA_REL, P.TOPO, sa, ov=ov))
                if valido(o): corpo = o; break
            except Exception:
                continue
        else:
            print('      *** uma lamina do icone nao entrou ***')
    print('      %-26s 3 laminas em auto relevo' % 'ponteira: icone')
    return corpo

# ===================================================== saida
def grava(s, nome):
    t = cq.Location(cq.Vector(P.CX, 0, P.CZ))
    s = s.moved(t)
    cq.exporters.export(cq.Workplane(obj=s), '%s/%s.step' % (STEP, nome), exportType='STEP')
    print('   %-46s solidos=%d faces=%4d vol=%8.2f  B-rep %s'
          % (nome + '.step', len(s.Solids()), len(s.Faces()), s.Volume(),
             'VALIDO' if valido(s) else '*** INVALIDO ***'))
    return s

if __name__ == '__main__':
    alvo = sys.argv[1] if len(sys.argv) > 1 else 'tudo'
    if alvo in ('m01', 'tudo'):
        a, b, c, d = m01()
        grava(a, 'Chrono_v3_M01_1_SOMAR_enchimento_mesa_dias')
        grava(b, 'Chrono_v3_M01_2_SUBTRAIR_rebaixo_com_detentes')
        grava(c, 'Chrono_v3_M01_3_SOMAR_poste')
        grava(d, 'Chrono_v3_M01_4_SUBTRAIR_furo_passante')
    if alvo in ('m02', 'tudo'): grava(m02(), 'Chrono_v3_M02_Rodinha_Meses')
    if alvo in ('m03', 'tudo'): grava(m03(), 'Chrono_v3_M03_Ponteira')
