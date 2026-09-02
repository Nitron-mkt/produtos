# -*- coding: utf-8 -*-
"""
Tampa de Correr — plataforma Aro Comum (Nitron)

Corpo AC-21 (2,1 L) + Tampa + Cursor (porta de correr) + 2 Travas de correr
+ 2 aneis de TPE (aro e boca).

Cotas em milimetro. Z para cima, origem no centro do fundo externo do corpo.
Este arquivo e a FONTE UNICA das cotas: STL, blob do visualizador, corte
cotado e tabela saem do mesmo dicionario P.
"""
import math, os, sys, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import outline, zone, zsum, zval, Mesh, SEG, STR

# ============================================================================
# 1. PARAMETROS
# ============================================================================
P = dict(
    # --- aro comum: face externa do ARO (topo), 105 x 206 R14 ---
    HX=52.5, HY=103.0, RC=14.0,
    # --- corpo ---
    H=120.0, WALL=1.30, FLOOR=2.00, DRAFT=1.5,
    RECUO=1.10,                   # a parede abaixo do aro e recuada; o aro engrossa
    Z_FLARE0=115.60, Z_FLARE1=118.00,
    # aba de encosto da trava (2 zonas nas faces longas)
    ABA_D=2.05, ABA_Z0=111.00, ABA_Z1=113.00, ABA_Z2=114.20,
    ABA_YC=13.75, ABA_W=11.25,
    # --- tampa ---
    PLATE=1.60, BORDA=1.00, BORDA_W=8.00,
    Z_PLATE_B=120.00, LEG_IN=0.35, LEG_OUT=1.95, Z_SKIRT=114.40,
    LIP_ROOT=-2.70, LIP_IN=-3.90, LIP_TIP=113.20,
    SEAM=-9.00,
    # canaleta da junta do aro
    GR_D0=-1.90, GR_D1=-0.50, GR_Z=121.60,
    # --- pista da porta de correr ---
    TK_HX=40.0, TK_HY=82.0, TK_RC=8.0, TK_CY=8.0,
    Z_TRACK=119.20, Z_SLAB=116.80,
    RAIL_W=2.60, RAIL_LIP=0.40, RAIL_Z=122.20, RAIL_LIP_Z=121.60,
    RAIL_Y0=-74.0, RAIL_Y1=90.0,
    PAD_H=0.55, PAD_X0=35.5, PAD_X1=39.6, PAD_RAMP=4.0,
    PAD_A0=-72.0, PAD_A1=10.0, PAD_B0=22.0, PAD_B1=78.0,
    SK_X0=35.5, SK_X1=39.4, SK_A0=12.0, SK_A1=20.0, SK_B0=80.0, SK_B1=88.0,
    # boca e junta da boca
    BC_HX=31.0, BC_HY=32.0, BC_RC=12.0, BC_CY=50.0,
    GB_D0=2.40, GB_D1=3.80, GB_Z=117.55,
    # --- cursor (porta de correr) ---
    CU_HX=39.4, CU_HY=38.0, CU_RC=7.0, CU_CY=50.0,
    CU_T=1.80, CU_CURSO=56.0,
    # --- trava de correr (faces longas) ---
    RAIL_D0=1.95, RAIL_D1=2.75, RAIL_D2=3.55,
    TRV_Z0=115.40, TRV_Z1=116.00, TRV_Z2=118.60, TRV_Z3=119.20,
    TRV_Y0=-27.0, TRV_Y1=27.0,
    TR_HALF=13.0, TR_CURSO=22.0, TR_C=11.0,
    TR_ZB=114.70, TR_D3=5.15, TR_Z_TOP=120.00, TR_Z_BOT=107.80,
    TG_HALF=12.0, TG_D=-0.90, TG_BOT=107.80,
    TG_LAND=111.00, TG_RAMP=110.45, TG_RAMP_L=8.0,
    # --- juntas de TPE ---
    TPE_W=1.40, TPE_H=1.40, TPE_SEAT=1.00,   # secao e quanto entra na canaleta
    TPE_SHORE=45,
    # --- material ---
    RHO=0.905, RHO_TPE=0.89,
)
K = math.tan(math.radians(P['DRAFT']))
P['Z_PLATE_T'] = P['Z_PLATE_B'] + P['PLATE']
P['Z_BORDA'] = P['Z_PLATE_T'] + P['BORDA']
P['TPE_OUT'] = P['TPE_H'] - P['TPE_SEAT']        # quanto sobra para fora = aperto

OUT = outline(P['HX'], P['HY'], P['RC'])
TK = outline(P['TK_HX'], P['TK_HY'], P['TK_RC'], 0.0, P['TK_CY'])
BC = outline(P['BC_HX'], P['BC_HY'], P['BC_RC'], 0.0, P['BC_CY'])
CU = outline(P['CU_HX'], P['CU_HY'], P['CU_RC'], 0.0, P['CU_CY'])

do = lambda z: -(P['H'] - z) * K                  # face externa do ARO
dw = lambda z: do(z) - P['RECUO']                 # parede abaixo do aro
di = lambda z: do(z) - P['RECUO'] - P['WALL']     # face interna (continua)

# zona da aba: faces longas (x = +-HX), corrida em Y
def zona_y(ol, value, yc, half, feather=1.6):
    return [zval(value, py, yc, half, feather) if abs(px) > P['HX'] - 0.01 else 0.0
            for (px, py, nx, ny) in ol]

Z_ABA = zona_y(OUT, P['ABA_D'], P['ABA_YC'], P['ABA_W'])


# ============================================================================
# 2. CORPO AC-21
# ============================================================================
def corpo():
    m = Mesh('corpo')
    a0, a1, a2 = P['ABA_Z0'], P['ABA_Z1'], P['ABA_Z2']
    W = P['WALL'] + P['RECUO']                    # espessura no aro
    prof = [
        (dw(0.0) - 1.20, 0.00),                   # face de apoio
        (dw(1.20), 1.20),                         # chanfro do pe
        (dw(a0 - 0.10), a0 - 0.10),
        (dw(a0), a0),                             # face inferior da aba (encosto)
        (dw(a1), a1),
        (dw(a2), a2),                             # rampa de volta a parede
        (dw(P['Z_FLARE0']), P['Z_FLARE0']),
        (do(P['Z_FLARE1']), P['Z_FLARE1']),       # engrossamento do aro
        (do(119.70), 119.70),
        (-0.20, P['H']),                          # chanfro externo do aro
        (-W + 0.20, P['H']),                      # TOPO DO ARO = batente da tampa
        (-W, 119.70),
        (di(P['FLOOR']), P['FLOOR']),
    ]
    Z = [0.0] * len(OUT)
    amps = [Z, Z, Z, Z_ABA, Z_ABA, Z, Z, Z, Z, Z, Z, Z, Z]
    m.sweep(OUT, prof, amps)
    m.fan(OUT, dw(0.0) - 1.20, 0.0, up=False)
    m.fan(OUT, di(P['FLOOR']), P['FLOOR'], up=True)
    return m


# ============================================================================
# 3. TAMPA
# ============================================================================
def tampa():
    m = Mesh('tampa')
    ZT, ZB, ZBD = P['Z_PLATE_T'], P['Z_PLATE_B'], P['Z_BORDA']
    # --- periferia: saia externa, borda alta e mesa ---
    m.sweep(OUT, [
        (P['LEG_OUT'], P['Z_SKIRT']),
        (P['LEG_OUT'], ZBD - 0.60),
        (P['LEG_OUT'] - 0.40, ZBD),
        (-P['BORDA_W'], ZBD),
        (-P['BORDA_W'], ZT),
        (P['SEAM'], ZT),
    ])
    # --- periferia: face inferior, labio-guia, canaleta da junta e perna ---
    m.sweep(OUT, [
        (P['SEAM'], ZB),
        (P['LIP_IN'], ZB),
        (P['LIP_IN'], P['LIP_TIP'] + 0.40),
        (P['LIP_IN'] + 0.40, P['LIP_TIP']),
        (P['LIP_ROOT'] - 0.20, P['LIP_TIP'] + 0.40),
        (P['LIP_ROOT'], P['LIP_TIP'] + 1.40),
        (P['LIP_ROOT'], ZB),
        (P['GR_D0'], ZB),                     # encosto interno
        (P['GR_D0'], P['GR_Z']),              # canaleta da junta de TPE
        (P['GR_D1'], P['GR_Z']),
        (P['GR_D1'], ZB),
        (P['LEG_IN'], ZB),                    # encosto externo
        (P['LEG_IN'], P['Z_SKIRT']),
        (P['LEG_OUT'], P['Z_SKIRT']),
    ])
    # --- pista: mesa -> rebaixo -> boca ---
    m.flat(TK, 0.0, OUT, P['SEAM'], ZT, up=True)
    m.sweep(TK, [(0.0, ZT), (0.0, P['Z_TRACK'])])
    m.flat(BC, P['GB_D1'], TK, 0.0, P['Z_TRACK'], up=True)
    m.sweep(BC, [(P['GB_D1'], P['Z_TRACK']), (P['GB_D1'], P['GB_Z']),
                 (P['GB_D0'], P['GB_Z']), (P['GB_D0'], P['Z_TRACK'])])
    m.flat(BC, 0.0, BC, P['GB_D0'], P['Z_TRACK'], up=True)
    m.sweep(BC, [(0.0, P['Z_TRACK']), (0.0, P['Z_SLAB'])])
    m.flat(BC, 0.0, TK, 0.0, P['Z_SLAB'], up=False)
    m.sweep(TK, [(0.0, P['Z_SLAB']), (0.0, ZB)])
    m.flat(TK, 0.0, OUT, P['SEAM'], ZB, up=False)
    # --- trilhos da porta, pistas de came e trilhos das travas ---
    for s in (1, -1):
        trilho_porta(m, s)
        rampa_came(m, s)
        trilho_trava(m, s)
    return m


def trilho_porta(m, s):
    """Trilho em C da porta: parede + labio que segura o cursor."""
    x0, x1 = P['TK_HX'], P['TK_HX'] + P['RAIL_W']
    lp = P['TK_HX'] - P['RAIL_LIP']
    poly = [(x0, P['Z_TRACK']), (x1, P['Z_TRACK']), (x1, P['RAIL_Z']),
            (lp, P['RAIL_Z']), (lp, P['RAIL_LIP_Z']), (x0, P['RAIL_LIP_Z'])]
    p = [(s * a, b) for (a, b) in poly]
    if s < 0:
        p = p[::-1]
    m.prismY(p, P['RAIL_Y0'], P['RAIL_Y1'])


def rampa_came(m, s):
    """Pistas elevadas: o cursor corre 0,55 mm acima do piso e desce so no fim.

    Dois trechos, com folga onde os quatro patins pousam na posicao fechada —
    os quatro descem juntos, entao o cursor nao inclina em nenhum ponto do curso.
    """
    zt, h, r = P['Z_TRACK'], P['PAD_H'], P['PAD_RAMP']
    alto = [(P['PAD_X0'], zt), (P['PAD_X1'], zt), (P['PAD_X1'], zt + h), (P['PAD_X0'], zt + h)]
    baixo = [(P['PAD_X0'], zt), (P['PAD_X1'], zt),
             (P['PAD_X1'], zt + 0.05), (P['PAD_X0'], zt + 0.05)]
    p = lambda q: ([(s * a, b) for (a, b) in q][::-1] if s < 0
                   else [(s * a, b) for (a, b) in q])
    for (y0, y1, r0, r1) in ((P['PAD_A0'], P['PAD_A1'], 0, 1),
                             (P['PAD_B0'], P['PAD_B1'], 1, 1)):
        a, b = y0 + (r if r0 else 0), y1 - (r if r1 else 0)
        m.prismY(p(alto), a, b)
        if r0:
            m.loftY(p(baixo), p(alto), y0, a)
        if r1:
            m.loftY(p(alto), p(baixo), b, y1)


def trilho_trava(m, s):
    """Trilho em T da trava, na face longa. Secao constante em Y: gaveta reta."""
    x = lambda d: P['HX'] + d
    for poly in ([(x(P['RAIL_D0']), P['TRV_Z1']), (x(P['RAIL_D1']), P['TRV_Z1']),
                  (x(P['RAIL_D1']), P['TRV_Z2']), (x(P['RAIL_D0']), P['TRV_Z2'])],
                 [(x(P['RAIL_D1']), P['TRV_Z0']), (x(P['RAIL_D2']), P['TRV_Z0']),
                  (x(P['RAIL_D2']), P['TRV_Z3']), (x(P['RAIL_D1']), P['TRV_Z3'])]):
        p = [(s * a, b) for (a, b) in poly]
        if s < 0:
            p = p[::-1]
        m.prismY(p, P['TRV_Y0'], P['TRV_Y1'])


# ============================================================================
# 4. CURSOR — a porta de correr (posicao fechada)
# ============================================================================
def cursor():
    m = Mesh('cursor')
    z0 = P['Z_TRACK']
    z1 = z0 + P['CU_T']
    m.sweep(CU, [(0.0, z0), (0.0, z1 - 0.30), (-0.30, z1)])
    m.fan(CU, -0.30, z1, up=True, cy=P['CU_CY'])
    m.fan(CU, 0.0, z0, up=False, cy=P['CU_CY'])
    for s in (1, -1):
        for (a, b) in ((P['SK_A0'], P['SK_A1']), (P['SK_B0'], P['SK_B1'])):
            xa, xb = s * P['SK_X0'], s * P['SK_X1']
            m.box(min(xa, xb), max(xa, xb), a, b, z0 - P['PAD_H'], z0)   # patins
    y0 = P['CU_CY'] - P['CU_HY']
    m.box(-15.0, 15.0, y0 + 2.0, y0 + 8.0, z1, z1 + 1.40)       # pegador
    for s in (1, -1):
        m.box(s * 19.4, s * 20.6, y0 + 3.0, P['CU_CY'] + P['CU_HY'] - 3.0,
              z1, z1 + 1.00) if s > 0 else m.box(-20.6, -19.4, y0 + 3.0,
              P['CU_CY'] + P['CU_HY'] - 3.0, z1, z1 + 1.00)     # nervuras
    return m


# ============================================================================
# 5. TRAVA DE CORRER (posicao travada)
# ============================================================================
def trava():
    m = Mesh('trava')
    x = lambda d: P['HX'] + d
    c, h = P['TR_C'], P['TR_HALF']
    y0, y1 = c - h, c + h
    tg0, tg1 = c - P['TG_HALF'], c + P['TG_HALF']
    land = [(x(P['TG_D']), P['TG_BOT']), (x(P['RAIL_D2']), P['TG_BOT']),
            (x(P['RAIL_D2']), P['TG_LAND']), (x(P['TG_D']), P['TG_LAND'])]
    ramp = [(x(P['TG_D']), P['TG_BOT']), (x(P['RAIL_D2']), P['TG_BOT']),
            (x(P['RAIL_D2']), P['TG_RAMP']), (x(P['TG_D']), P['TG_RAMP'])]
    for s in (1, -1):
        M = lambda q: ([(s * a, b) for (a, b) in q][::-1] if s < 0
                       else [(s * a, b) for (a, b) in q])
        m.prismY(M([(x(P['RAIL_D2']), P['TR_ZB']), (x(P['TR_D3']), P['TR_ZB']),
                    (x(P['TR_D3']), P['TR_Z_TOP']), (x(P['RAIL_D2']), P['TR_Z_TOP'])]), y0, y1)
        for (za, zb) in ((P['TR_ZB'], P['TRV_Z0']), (P['TRV_Z3'], P['TR_Z_TOP'])):
            m.prismY(M([(x(P['RAIL_D1'] - 0.20), za), (x(P['RAIL_D2']), za),
                        (x(P['RAIL_D2']), zb), (x(P['RAIL_D1'] - 0.20), zb)]), y0, y1)
        m.prismY(M([(x(P['RAIL_D2']), P['TR_Z_BOT']), (x(P['TR_D3']), P['TR_Z_BOT']),
                    (x(P['TR_D3']), P['TR_ZB']), (x(P['RAIL_D2']), P['TR_ZB'])]), tg0, tg1)
        m.prismY(M(land), tg0, tg1 - P['TG_RAMP_L'])
        m.loftY(M(land), M(ramp), tg1 - P['TG_RAMP_L'], tg1)
        for k in (-7.0, 0.0, 7.0):
            m.prismY(M([(x(P['TR_D3']), 116.2), (x(P['TR_D3'] + 0.60), 116.2),
                        (x(P['TR_D3'] + 0.60), 119.0), (x(P['TR_D3']), 119.0)]),
                     c + k - 0.8, c + k + 0.8)
    return m


# ============================================================================
# 6. JUNTAS DE TPE
# ============================================================================
def junta_perfil(ol, d0, z_top, name):
    """Anel de secao retangular arredondada, assentado numa canaleta."""
    m = Mesh(name)
    w, hh, seat = P['TPE_W'], P['TPE_H'], P['TPE_SEAT']
    d1 = d0 + w
    zb = z_top - hh
    r = 0.35
    m.sweep(ol, [
        (d0 + r, zb), (d1 - r, zb), (d1, zb + r), (d1, z_top - r),
        (d1 - r, z_top), (d0 + r, z_top), (d0, z_top - r), (d0, zb + r),
        (d0 + r, zb),
    ])
    return m


def junta_aro():
    return junta_perfil(OUT, P['GR_D0'] + 0.05,
                        P['Z_PLATE_B'] + P['TPE_SEAT'], 'junta_aro')


def junta_boca():
    return junta_perfil(BC, P['GB_D0'] + 0.05,
                        P['Z_TRACK'] + P['TPE_OUT'], 'junta_boca')


# ============================================================================
# 7. METRICAS
# ============================================================================
def area(d):
    hx, hy, rc = P['HX'] + d, P['HY'] + d, P['RC'] + d
    return 4 * hx * hy - (4 - math.pi) * rc * rc


def perim(d):
    hx, hy, rc = P['HX'] + d, P['HY'] + d, P['RC'] + d
    return 2 * (2 * hx - 2 * rc) + 2 * (2 * hy - 2 * rc) + 2 * math.pi * rc


def perim_bc(d):
    hx, hy, rc = P['BC_HX'] + d, P['BC_HY'] + d, P['BC_RC'] + d
    return 2 * (2 * hx - 2 * rc) + 2 * (2 * hy - 2 * rc) + 2 * math.pi * rc


def volume_litros(z_top):
    n, acc = 400, 0.0
    z0 = P['FLOOR']
    for i in range(n):
        z = z0 + (i + 0.5) * (z_top - z0) / n
        acc += area(di(z)) * (z_top - z0) / n
    return acc / 1e6


def forcas():
    """Estimativa de forca: TPE shore 45A, 30% de aperto ~ 0,22 N/mm."""
    n_mm = 0.22
    aro = perim(P['GR_D0'] + P['TPE_W'] / 2) * n_mm
    boca = perim_bc(P['GB_D0'] + P['TPE_W'] / 2) * n_mm
    ramp = math.degrees(math.atan(P['TPE_OUT'] / P['TG_RAMP_L']))
    mu = 0.30
    f_trava = aro / 2.0
    f_dedo = f_trava * (math.tan(math.radians(ramp)) + mu)
    f_abre = f_trava * (mu - math.tan(math.radians(ramp)))
    return dict(aperto_aro_n=round(aro), aperto_boca_n=round(boca),
                por_trava_n=round(f_trava), rampa_graus=round(ramp, 1),
                dedo_trava_n=round(f_dedo), dedo_destrava_n=round(max(f_abre, 0)))


def tensoes():
    """Lingueta em flexao no carregamento de projeto."""
    F = forcas()['por_trava_n'] * 3.0             # fator de projeto 3x (queda)
    b = 2 * P['TG_HALF']
    t = P['TG_LAND'] - P['TG_BOT']
    crest = dw(P['ABA_Z0']) + P['ABA_D']
    arm = P['RAIL_D2'] - (P['TG_D'] + crest) / 2
    Z = b * t * t / 6.0
    return dict(carga_n=round(F), largura_mm=b, espessura_mm=round(t, 2),
                braco_mm=round(arm, 2), sigma_mpa=round(F * arm / Z, 1),
                cisalh_mpa=round(F / (b * t), 1))


def metricas():
    m = dict(
        area_proj_cm2=round(area(0.0) / 100.0, 1),
        forca_t=round(area(0.0) / 100.0 * 0.35),
        vol_borda_l=round(volume_litros(P['H']), 2),
        vol_util_l=round(volume_litros(P['Z_PLATE_B'] - 4.0), 2),
        boca_cm2=round((4 * P['BC_HX'] * P['BC_HY']
                        - (4 - math.pi) * P['BC_RC'] ** 2) / 100.0, 1),
        curso_porta_mm=P['CU_CURSO'],
        abertura_livre_cm2=round((2 * P['BC_HX']) * (P['CU_CURSO'] - 6.0) / 100.0, 1),
        perim_aro_mm=round(perim(P['GR_D0'] + P['TPE_W'] / 2), 1),
        perim_boca_mm=round(perim_bc(P['GB_D0'] + P['TPE_W'] / 2), 1),
        aperto_mm=round(P['TPE_OUT'], 2),
        aperto_pct=round(P['TPE_OUT'] / P['TPE_H'] * 100),
        engate_mm=round((P['ABA_D'] - P['RECUO'] + do(P['ABA_Z0'])) - P['TG_D'], 2),
        puxada_mm=round(P['TG_LAND'] - P['TG_RAMP'], 2),
    )
    m.update(forcas())
    m.update(tensoes())
    return m


# ============================================================================
if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    parts = [corpo(), tampa(), cursor(), trava(), junta_aro(), junta_boca()]
    out = {}
    for p in parts:
        p.stl(os.path.join(here, 'stl', p.name + '.stl'))
        rho = P['RHO_TPE'] if p.name.startswith('junta') else P['RHO']
        bb = p.bbox()
        print('%-11s %6d tri %7.2f cm3 %6.2f g  x[%.1f %.1f] y[%.1f %.1f] z[%.1f %.1f]'
              % (p.name, len(p.F), p.volume_cm3(), p.volume_cm3() * rho,
                 bb[0], bb[1], bb[2], bb[3], bb[4], bb[5]))
        b1, b2, b3 = p.buffers()
        out[p.name] = dict(p=base64.b64encode(b1).decode(),
                           n=base64.b64encode(b2).decode(),
                           i=base64.b64encode(b3).decode(),
                           nv=len(p.V), nt=len(p.F),
                           g=round(p.volume_cm3() * rho, 2))
    M = metricas()
    print(json.dumps(M, indent=1))
    out['P'] = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in P.items()}
    out['M'] = M
    js = 'window.GEO=' + json.dumps(out, separators=(',', ':')) + ';'
    open(os.path.join(here, 'web', 'geo.js'), 'w').write(js)
    print('geo.js  %.0f kB' % (len(js) / 1024))
