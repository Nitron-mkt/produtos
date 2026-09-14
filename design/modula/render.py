"""Rasterizador proprio (painter + flat shading) para as vistas da familia."""
import math
import numpy as np
from PIL import Image, ImageFilter

FUNDO = (247, 246, 243)

PALETA = {
    "laranja": (226, 88, 30),
    "chumbo": (74, 79, 86),
    "branco": (232, 232, 228),
    "destaque": (255, 178, 44),
    "critico": (30, 120, 200),
}


def camera(az=38.0, el=26.0):
    a, e = math.radians(az), math.radians(el)
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    r = np.cross(d, np.array([0.0, 0.0, 1.0]))
    r /= np.linalg.norm(r)
    u = np.cross(r, d)
    return d, r, u


def cena(grupos, largura=1400, altura=1000, az=38.0, el=26.0, ss=2,
         margem=0.06, fundo=FUNDO, luz=(-0.45, -0.72, 0.52), normais=None,
         sombra=True, z_chao=0.0):
    """grupos = [(triangulos, cor_rgb_por_tag_dict_ou_rgb, normais_opcionais), ...]
    normais_opcionais = lista paralela de (n0,n1,n2) por triangulo -> sombreado
    suave (Gouraud). Sem ela, sombreado plano."""
    W, H = largura * ss, altura * ss
    d, r, u = camera(az, el)
    L = np.array(luz, float)
    L /= np.linalg.norm(L)

    verts, cores, nvert = [], [], []
    for grupo in grupos:
        tris, cor = grupo[0], grupo[1]
        ns = grupo[2] if len(grupo) > 2 else None
        for k, (a, b, c, tag) in enumerate(tris):
            verts.append((a, b, c))
            cores.append(cor[tag] if isinstance(cor, dict) else cor)
            nvert.append(ns[k] if ns is not None else None)
    if not verts:
        raise SystemExit("cena vazia")
    P = np.array(verts, dtype=np.float64)                 # (n,3,3)
    C = np.array(cores, dtype=np.float64)                 # (n,3)

    sx = P @ r
    sy = P @ u
    sz = P @ d
    x0, x1 = sx.min(), sx.max()
    y0, y1 = sy.min(), sy.max()
    esc = min(W * (1 - 2 * margem) / max(x1 - x0, 1e-6),
              H * (1 - 2 * margem) / max(y1 - y0, 1e-6))
    px = (sx - (x0 + x1) / 2) * esc + W / 2
    py = H / 2 - (sy - (y0 + y1) / 2) * esc

    n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    ln[ln == 0] = 1
    n = n / ln
    frente = (n @ d) > 0
    n[~frente] *= -1

    L2 = -L * np.array([1.0, 1.0, -0.4])
    L2 /= np.linalg.norm(L2)
    # base clara para cores claras: imita a inter-reflexao, que e o que faz um
    # branco parecer branco e nao cinza
    lum = (0.30 * C[:, 0] + 0.60 * C[:, 1] + 0.10 * C[:, 2]) / 255.0
    base = 0.40 + 0.36 * lum

    def brilho(vn, bs):
        dif = np.clip(vn @ L, 0, 1)
        fill = np.clip(vn @ L2, 0, 1)
        topo = np.clip(vn @ np.array([0.0, 0.0, 1.0]), 0, 1)
        sombra = np.clip(0.52 * dif + 0.22 * fill + 0.26 * topo, 0, 1)
        return bs + (1.0 - bs) * sombra

    inten = brilho(n, base)
    RGB = np.clip(C * inten[:, None], 0, 255)

    # normais por canto (Gouraud) quando disponiveis
    NV = np.zeros((len(verts), 3, 3))
    tem_suave = np.zeros(len(verts), dtype=bool)
    for i, ns in enumerate(nvert):
        if ns is None:
            continue
        m3 = np.array(ns, dtype=np.float64)
        if (m3 @ d).mean() < 0:
            m3 = -m3
        NV[i] = m3
        tem_suave[i] = True
    IV = np.zeros((len(verts), 3))
    if tem_suave.any():
        flat = NV[tem_suave].reshape(-1, 3)
        bs = np.repeat(base[tem_suave], 3)
        IV[tem_suave] = brilho(flat, bs).reshape(-1, 3)

    img = np.zeros((H, W, 3), dtype=np.float32)
    img[:, :] = fundo

    # ---- sombra de contato: silhueta achatada no chao, borrada -------------
    if sombra:
        Pc = P.copy()
        Pc[:, :, 2] = z_chao
        sxc = (Pc @ r - (x0 + x1) / 2) * esc + W / 2
        syc = H / 2 - (Pc @ u - (y0 + y1) / 2) * esc
        masc = np.zeros((H, W), dtype=np.float32)
        for i in range(len(Pc)):
            ax_, ay_ = sxc[i, 0], syc[i, 0]
            bx_, by_ = sxc[i, 1], syc[i, 1]
            cx_, cy_ = sxc[i, 2], syc[i, 2]
            mnx = max(int(min(ax_, bx_, cx_)), 0); mxx = min(int(max(ax_, bx_, cx_)) + 2, W)
            mny = max(int(min(ay_, by_, cy_)), 0); mxy = min(int(max(ay_, by_, cy_)) + 2, H)
            if mnx >= mxx or mny >= mxy:
                continue
            det = (by_ - cy_) * (ax_ - cx_) + (cx_ - bx_) * (ay_ - cy_)
            if abs(det) < 1e-9:
                continue
            yy, xx = np.mgrid[mny:mxy, mnx:mxx]
            xc, yc = xx + 0.5, yy + 0.5
            l1 = ((by_ - cy_) * (xc - cx_) + (cx_ - bx_) * (yc - cy_)) / det
            l2 = ((cy_ - ay_) * (xc - cx_) + (ax_ - cx_) * (yc - cy_)) / det
            mm = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
            if mm.any():
                masc[mny:mxy, mnx:mxx][mm] = 1.0
        b = Image.fromarray((masc * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius=max(6, W // 90)))
        masc = np.asarray(b, dtype=np.float32) / 255.0 * 0.34
        img *= (1.0 - masc[:, :, None] * 0.9)

    zbuf = np.full((H, W), -1e18, dtype=np.float64)

    ordem = np.argsort(sz.mean(axis=1))
    for i in ordem:
        ax_, ay_ = px[i, 0], py[i, 0]
        bx_, by_ = px[i, 1], py[i, 1]
        cx_, cy_ = px[i, 2], py[i, 2]
        minx = max(int(math.floor(min(ax_, bx_, cx_))), 0)
        maxx = min(int(math.ceil(max(ax_, bx_, cx_))) + 1, W)
        miny = max(int(math.floor(min(ay_, by_, cy_))), 0)
        maxy = min(int(math.ceil(max(ay_, by_, cy_))) + 1, H)
        if minx >= maxx or miny >= maxy:
            continue
        det = (by_ - cy_) * (ax_ - cx_) + (cx_ - bx_) * (ay_ - cy_)
        if abs(det) < 1e-9:
            continue
        yy, xx = np.mgrid[miny:maxy, minx:maxx]
        xxc = xx + 0.5
        yyc = yy + 0.5
        l1 = ((by_ - cy_) * (xxc - cx_) + (cx_ - bx_) * (yyc - cy_)) / det
        l2 = ((cy_ - ay_) * (xxc - cx_) + (ax_ - cx_) * (yyc - cy_)) / det
        l3 = 1.0 - l1 - l2
        m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        if not m.any():
            continue
        prof = l1 * sz[i, 0] + l2 * sz[i, 1] + l3 * sz[i, 2]
        alvo = zbuf[miny:maxy, minx:maxx]
        m &= prof > alvo
        if not m.any():
            continue
        alvo[m] = prof[m]
        if tem_suave[i]:
            ii = (l1 * IV[i, 0] + l2 * IV[i, 1] + l3 * IV[i, 2])[m]
            img[miny:maxy, minx:maxx][m] = np.clip(
                C[i][None, :] * ii[:, None], 0, 255)
        else:
            img[miny:maxy, minx:maxx][m] = RGB[i]

    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if ss > 1:
        out = out.resize((largura, altura), Image.LANCZOS)
    return out
