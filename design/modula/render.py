"""Rasterizador proprio (painter + flat shading) para as vistas da familia."""
import math
import numpy as np
from PIL import Image

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
         margem=0.06, fundo=FUNDO, luz=(-0.45, -0.72, 0.52)):
    """grupos = [(triangulos, cor_rgb_por_tag_dict_ou_rgb), ...]"""
    W, H = largura * ss, altura * ss
    d, r, u = camera(az, el)
    L = np.array(luz, float)
    L /= np.linalg.norm(L)

    verts, cores = [], []
    for tris, cor in grupos:
        for (a, b, c, tag) in tris:
            verts.append((a, b, c))
            cores.append(cor[tag] if isinstance(cor, dict) else cor)
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

    dif = np.clip(n @ L, 0, 1)
    topo = np.clip(n @ np.array([0.0, 0.0, 1.0]), 0, 1)
    inten = 0.36 + 0.50 * dif + 0.16 * topo
    RGB = np.clip(C * inten[:, None], 0, 255)

    img = np.zeros((H, W, 3), dtype=np.float32)
    img[:, :] = fundo
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
        img[miny:maxy, minx:maxx][m] = RGB[i]

    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if ss > 1:
        out = out.resize((largura, altura), Image.LANCZOS)
    return out
