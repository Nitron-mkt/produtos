# -*- coding: utf-8 -*-
"""
Tampa Portinhola — plataforma Aro Comum (Nitron)
Corpo AC-21 (2,1 L) + Tampa D (portinhola) + Portinhola.

Todas as cotas em milimetro. Z para cima, origem no centro do fundo externo.
Este arquivo e a FONTE UNICA das cotas: STL, blob do visualizador e o
desenho de secao saem daqui.
"""
import math, os, sys, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import outline, zone, zsum, Mesh, SEG, STR

# ============================================================================
# 1. PARAMETROS
# ============================================================================
P = dict(
    # --- aro comum (face externa do aro do corpo, no topo) ---
    HX=52.5, HY=103.0, RC=14.0,          # 105 x 206, R14 — base do Porta Sabao 008
    # --- corpo ---
    H=120.0, WALL=1.30, FLOOR=2.00, DRAFT=1.5,
    Z_SEAL0=112.4, Z_SEAL1=118.6,        # banda de vedacao interna, saida 0 grau
    CATCH_Z0=105.40, CATCH_Z1=106.20, CATCH_Z2=108.60,   # ressalto de trava
    CATCH_D=1.20, CATCH_W=17.0,          # projecao e meia-largura (34 mm)
    # --- tampa ---
    PLATE=1.60, LEG_T=1.60, LEG_IN=0.35, Z_SKIRT=112.60,
    Z_PLATE_B=120.00,
    LIP_T=1.00, LIP_ROOT=-1.75, FOLGA_LABIO=0.35,
    Z_CREST=115.40, LIP_TIP=112.20,
    SEAM=-9.00,
    # --- rebaixo da portinhola e gargalo ---
    PK_HX=38.0, PK_HY=48.0, PK_RC=18.0, PK_CY=40.0,      # rebaixo
    TH_HX=31.0, TH_HY=41.0, TH_RC=12.0,                  # boca (garganta)
    COLLAR_Z=115.20, COLLAR_W=1.20, COLLAR_DRAFT=3.0,
    BEAD=-0.90,                          # ressalto de retencao da portinhola
    SCALLOP=4.50,                        # concha do dedo
    # --- portinhola ---
    GAP=0.35,                            # folga da aba no rebaixo
    LIP2_T=1.00, LIP2_TIP=116.20, FOLGA_PORTA=0.30,
    HINGE_Y=-5.0, HINGE_Z=124.00, HINGE_R=1.30,
    # --- material ---
    RHO=0.905,                           # g/cm3 — PP
)
P['Z_PLATE_T'] = P['Z_PLATE_B'] + P['PLATE']
P['Z_PK'] = P['Z_PLATE_T'] - P['PLATE']          # piso do rebaixo
P['Z_SLAB_B'] = P['Z_PK'] - P['PLATE']           # face inferior da laje rebaixada
P['LEG_OUT'] = P['LEG_IN'] + P['LEG_T']
P['LIP_IN'] = P['LIP_ROOT'] - P['LIP_T']
P['BEAD_Z'] = P['Z_PK'] + 0.9 * P['PLATE']
P['LIP2_IN'] = -P['LIP2_T'] - 0.30
P['Z_CREST2'] = P['Z_PK'] - 1.60

K = math.tan(math.radians(P['DRAFT']))
KC = math.tan(math.radians(P['COLLAR_DRAFT']))
P['DI_SEAL'] = -(P['H'] - P['Z_SEAL1']) * K - P['WALL']
P['LIP_CREST'] = P['DI_SEAL'] + P['FOLGA_LABIO']
P['LIP2_CREST'] = P['FOLGA_PORTA'] - KC * (P['Z_PK'] - (P['Z_PK'] - 1.60))

OUT = outline(P['HX'], P['HY'], P['RC'])
PK = outline(P['PK_HX'], P['PK_HY'], P['PK_RC'], 0.0, P['PK_CY'])
TH = outline(P['TH_HX'], P['TH_HY'], P['TH_RC'], 0.0, P['PK_CY'])

PK_FRONT = P['PK_CY'] + P['PK_HY'] - 0.01      # y da face frontal do rebaixo
do = lambda z: -(P['H'] - z) * K                # offset da face externa do corpo
di = lambda z: do(z) - P['WALL']                # offset da face interna
DI_SEAL = P['DI_SEAL']

# zonas locais
Z_CATCH = zone(OUT, P['CATCH_D'], lambda x, y: abs(y) > P['HY'] - 0.01,
               0.0, P['CATCH_W'], 2.0)
Z_BEAD = zsum(zone(PK, P['BEAD'], lambda x, y: y > PK_FRONT, 16.0, 8.0, 1.5),
              zone(PK, P['BEAD'], lambda x, y: y > PK_FRONT, -16.0, 8.0, 1.5))
Z_SCAL = zone(PK, P['SCALLOP'], lambda x, y: y > PK_FRONT, 0.0, 7.0, 1.5)
Z_TONG = zone(PK, 4.00, lambda x, y: y > PK_FRONT, 0.0, 6.0, 1.5)
Z_CHAM = zsum(zone(PK, -0.60, lambda x, y: y > PK_FRONT, 16.0, 9.0, 1.5),
              zone(PK, -0.60, lambda x, y: y > PK_FRONT, -16.0, 9.0, 1.5))
ZERO_PK = [0.0] * len(PK)


# ============================================================================
# 2. CORPO AC-21
# ============================================================================
def corpo():
    m = Mesh('corpo')
    z0, zc0, zc1, zc2 = 0.0, P['CATCH_Z0'], P['CATCH_Z1'], P['CATCH_Z2']
    prof = [
        (do(0.0) - 1.20, 0.00),          # face de apoio
        (do(1.20), 1.20),                # chanfro do pe
        (do(zc0 - 0.05), zc0 - 0.05),
        (do(zc0), zc0),                  # face de retencao (encosto da trava)
        (do(zc1), zc1),
        (do(zc2), zc2),                  # rampa de entrada 25 graus
        (do(119.70), 119.70),
        (-0.20, P['H']),                 # chanfro do aro
        (-P['WALL'] + 0.20, P['H']),     # topo do aro (batente da tampa)
        (-P['WALL'], 119.70),
        (DI_SEAL, P['Z_SEAL1']),
        (DI_SEAL, P['Z_SEAL0']),         # banda de vedacao, saida 0 grau
        (di(P['Z_SEAL0'] - 0.40), P['Z_SEAL0'] - 0.40),
        (di(P['FLOOR']), P['FLOOR']),
    ]
    Z = [0.0] * len(OUT)
    amps = [Z, Z, Z, Z_CATCH, Z_CATCH, Z, Z, Z, Z, Z, Z, Z, Z, Z]
    m.sweep(OUT, prof, amps)
    m.fan(OUT, do(0.0) - 1.20, 0.0, up=False)          # fundo externo
    m.fan(OUT, di(P['FLOOR']), P['FLOOR'], up=True)    # fundo interno
    return m


# ============================================================================
# 3. TAMPA D — portinhola
# ============================================================================
def tampa():
    m = Mesh('tampa')
    ZP = P['Z_PLATE_T']
    # --- periferia: saia externa e mesa (ate a costura em SEAM) ---
    m.sweep(OUT, [
        (P['LEG_OUT'], P['Z_SKIRT']),
        (P['LEG_OUT'], ZP - 1.00),
        (P['LEG_OUT'] - 0.45, ZP),
        (P['SEAM'], ZP),
    ])
    # --- periferia: face inferior, labio de vedacao, canal e perna ---
    m.sweep(OUT, [
        (P['SEAM'], P['Z_PLATE_B']),
        (P['LIP_IN'], P['Z_PLATE_B']),          # face inferior da mesa
        (P['LIP_IN'], P['LIP_TIP'] + 0.40),     # face interna do labio
        (P['LIP_IN'] + 0.55, P['LIP_TIP']),     # ponta do labio
        (-2.30, P['LIP_TIP'] + 0.60),           # entrada conica
        (P['LIP_CREST'], P['Z_CREST']),         # crista de vedacao (interferencia)
        (P['LIP_ROOT'], P['Z_CREST'] + 1.80),   # alivio acima da crista
        (P['LIP_ROOT'], P['Z_PLATE_B']),
        (P['LEG_IN'], P['Z_PLATE_B']),          # teto do canal = batente
        (P['LEG_IN'], P['Z_SKIRT']),
        (P['LEG_OUT'], P['Z_SKIRT']),
    ])
    # --- transicao mesa -> rebaixo ---
    m.flat(PK, 0.0, OUT, P['SEAM'], ZP, up=True, amp_in=Z_SCAL)          # T1
    m.sweep(PK, [(0.0, ZP), (0.0, P['BEAD_Z']), (0.0, P['Z_PK'])],
            amps=[Z_SCAL, zsum(Z_SCAL, Z_BEAD), Z_SCAL])                 # T2 parede
    m.flat(TH, 0.0, PK, 0.0, P['Z_PK'], up=True, amp_out=Z_SCAL)         # T3 piso
    # --- gargalo ---
    cw = P['COLLAR_W']
    dcb = -KC * (P['Z_PK'] - P['COLLAR_Z'])
    m.sweep(TH, [(0.0, P['Z_PK']), (dcb, P['COLLAR_Z'])])                # T4 assento
    m.flat(TH, dcb, TH, cw, P['COLLAR_Z'], up=False)                     # T5
    m.sweep(TH, [(cw, P['COLLAR_Z']), (cw, P['Z_SLAB_B'])])              # T6
    m.flat(TH, cw, PK, 0.0, P['Z_SLAB_B'], up=False, amp_out=Z_SCAL)     # T7
    m.sweep(PK, [(0.0, P['Z_SLAB_B']), (0.0, P['Z_PLATE_B'])],
            amps=[Z_SCAL, Z_SCAL])                                       # T8
    m.flat(PK, 0.0, OUT, P['SEAM'], P['Z_PLATE_B'], up=False, amp_in=Z_SCAL)  # T9
    # --- travas de alavanca (2) e orelhas da dobradica (2) ---
    for s in (1, -1):
        alavanca(m, s)
        orelha(m, s)
    return m


def alavanca(m, s):
    """Trava de alavanca na face curta; desenhada na posicao FECHADA."""
    yo = P['HY'] + P['LEG_OUT']
    pieces = [
        [(yo, 112.60), (yo + 0.85, 112.60), (yo + 0.85, 113.05), (yo, 113.05)],       # dobradica viva
        [(yo + 0.25, 101.80), (yo + 1.45, 101.80), (yo + 1.45, 113.05), (yo + 0.25, 113.05)],
        [(yo + 0.25, 104.40), (yo + 0.25, 105.35), (103.00, 105.35), (103.75, 104.40)],  # gancho
        [(yo + 0.25, 99.60), (yo + 2.30, 100.20), (yo + 2.30, 101.90), (yo + 0.25, 101.90)],  # pegador
    ]
    for poly in pieces:
        p = [(s * y, z) for (y, z) in poly]
        if s < 0:
            p = p[::-1]
        m.prismX(p, -17.0, 17.0)


def orelha(m, s):
    """Mancal aberto por cima para o munhao da portinhola."""
    hy, hz, r = P['HINGE_Y'], P['HINGE_Z'], P['HINGE_R']
    x0, x1 = s * 30.4, s * 33.6
    if s < 0:
        x0, x1 = x1, x0
    base_t = hz - r - 0.40
    m.box(x0, x1, hy - 3.6, hy + 3.6, P['Z_PLATE_T'], base_t)
    m.box(x0, x1, hy - 3.6, hy - r - 0.15, base_t, hz + 1.6)
    m.box(x0, x1, hy + r + 0.15, hy + 3.6, base_t, hz + 1.6)


# ============================================================================
# 4. PORTINHOLA (posicao fechada)
# ============================================================================
def portinhola():
    m = Mesh('portinhola')
    g = -P['GAP']
    ZP, ZB = P['Z_PLATE_T'], P['Z_PK']
    # aba
    m.sweep(PK, [(g, ZB), (g, ZP - 0.30), (g - 0.30, ZP)],
            amps=[Z_TONG, Z_TONG, zsum(Z_TONG, Z_CHAM)])
    m.fan(PK, g - 0.30, ZP, up=True, cy=P['PK_CY'], amp=zsum(Z_TONG, Z_CHAM))
    # face inferior da aba, ate a saia
    m.flat(TH, -0.30, PK, g, ZB, up=False, amp_out=Z_TONG)
    # saia de vedacao (selo radial)
    m.sweep(TH, [
        (-0.90, P['LIP2_TIP']),
        (-0.55, P['LIP2_TIP'] + 0.80),
        (P['LIP2_CREST'], P['Z_CREST2']),      # crista, interferencia 0,30
        (-0.30, ZB),
    ])
    m.flat(TH, P['LIP2_IN'], TH, -0.90, P['LIP2_TIP'], up=False)
    m.sweep(TH, [(P['LIP2_IN'], ZB), (P['LIP2_IN'], P['LIP2_TIP'])])
    m.fan(TH, P['LIP2_IN'], ZB, up=False, cy=P['PK_CY'])
    # lugs + munhoes da dobradica
    hy, hz, r = P['HINGE_Y'], P['HINGE_Z'], P['HINGE_R']
    for s in (1, -1):
        a, b = s * 26.0, s * 29.0
        if s < 0:
            a, b = b, a
        m.box(a, b, hy - 2.5, hy + 3.0, ZB, hz + r)
        m.box(a, b, hy + 1.0, P['PK_CY'] - P['PK_HY'] + 6.0, ZB, ZP)
        m.cylX(hy, hz, r, s * 29.0 if s > 0 else s * 31.8,
               s * 31.8 if s > 0 else s * 29.0)
    return m


# ============================================================================
# 5. METRICAS
# ============================================================================
def area(d):
    hx, hy, rc = P['HX'] + d, P['HY'] + d, P['RC'] + d
    return 4 * hx * hy - (4 - math.pi) * rc * rc


def volume_litros(z_top):
    n, acc = 400, 0.0
    z0, z1 = P['FLOOR'], z_top
    for i in range(n):
        z = z0 + (i + 0.5) * (z1 - z0) / n
        d = DI_SEAL if z > P['Z_SEAL0'] else di(z)
        acc += area(d) * (z1 - z0) / n
    return acc / 1e6


def metricas():
    return dict(
        area_proj_cm2=round(area(0.0) / 100.0, 1),
        forca_t=round(area(0.0) / 100.0 * 0.35),
        vol_borda_l=round(volume_litros(P['H']), 2),
        vol_util_l=round(volume_litros(P['Z_SEAL0']), 2),
        boca_cm2=round((4 * P['TH_HX'] * P['TH_HY']
                        - (4 - math.pi) * P['TH_RC'] ** 2) / 100.0, 1),
        perimetro_boca_mm=round(2 * (2 * P['TH_HX'] - 2 * P['TH_RC'])
                                + 2 * (2 * P['TH_HY'] - 2 * P['TH_RC'])
                                + 2 * math.pi * P['TH_RC'], 1),
        area_porta_cm2=round((4 * P['PK_HX'] * P['PK_HY']
                              - (4 - math.pi) * P['PK_RC'] ** 2) / 100.0, 1),
        perimetro_vedacao_mm=round(perimetro(P['LIP_CREST']), 1),
        interferencia_aro=round(P['LIP_CREST'] - DI_SEAL, 3),
        interferencia_porta=round(P['LIP2_CREST'] + KC * (P['Z_PK'] - P['Z_CREST2']), 3),
    )


def perimetro(d):
    hx, hy, rc = P['HX'] + d, P['HY'] + d, P['RC'] + d
    return 2 * (2 * hx - 2 * rc) + 2 * (2 * hy - 2 * rc) + 2 * math.pi * rc


# ============================================================================
if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    parts = [corpo(), tampa(), portinhola()]
    for m in parts:
        m.stl(os.path.join(here, 'stl', m.name + '.stl'))
        bb = m.bbox()
        print('%-12s %6d tri  %6.1f cm3  %5.1f g   bbox x[%.1f %.1f] y[%.1f %.1f] z[%.1f %.1f]'
              % (m.name, len(m.F), m.volume_cm3(), m.volume_cm3() * P['RHO'],
                 bb[0], bb[1], bb[2], bb[3], bb[4], bb[5]))
    print(json.dumps(metricas(), indent=1))
    # blob do visualizador
    out = {}
    for m in parts:
        p, n, i = m.buffers()
        out[m.name] = dict(p=base64.b64encode(p).decode(),
                           n=base64.b64encode(n).decode(),
                           i=base64.b64encode(i).decode(),
                           nv=len(m.V), nt=len(m.F),
                           g=round(m.volume_cm3() * P['RHO'], 1))
    out['P'] = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in P.items()}
    out['M'] = metricas()
    js = 'window.GEO=' + json.dumps(out, separators=(',', ':')) + ';'
    open(os.path.join(here, 'web', 'geo.js'), 'w').write(js)
    print('geo.js  %.0f kB' % (len(js) / 1024))
