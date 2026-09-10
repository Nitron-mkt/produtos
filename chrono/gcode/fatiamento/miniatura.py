#!/usr/bin/env python3
"""Renderiza o STL de cima e injeta a miniatura 230x110 PNG no .gcode, no formato
que PrusaSlicer/Orca escrevem e a Kobra 3 le. O CLI do PrusaSlicer nao gera
miniatura sem interface grafica, por isso este passo existe.

    python3 miniatura.py saida.gcode peca.stl [mais.stl ...]
"""
import base64, io, sys, pathlib
import numpy as np, trimesh
from PIL import Image

W, H = 230, 110
FUNDO = (243, 245, 245)
COR = (206, 214, 220)
LUZ = np.array([0.12, 0.24, 0.96]); LUZ /= np.linalg.norm(LUZ)

def render(stls, W2=920, H2=440):
    tris = np.vstack([trimesh.load(s).triangles for s in stls])
    # vista de cima do STL ja preparado (Z para cima): tela X = X, tela Y = Y,
    # profundidade = Z. Nao troca eixo nenhum — trocar espelha a peca.
    V = tris.copy()
    p = V.reshape(-1, 3); mn, mx = p.min(0), p.max(0)
    c = (mn + mx) / 2; sp = (mx - mn) * 1.08
    # cabe a peca inteira no quadro deitado 230x110, sem cortar
    sc = min(W2 / max(sp[0], 1e-6), H2 / max(sp[1], 1e-6))
    img = np.full((H2, W2, 3), float(FUNDO[0])); img[:] = FUNDO
    zb = np.full((H2, W2), -1e18)
    n = np.cross(V[:, 1] - V[:, 0], V[:, 2] - V[:, 0])
    ln = np.linalg.norm(n, axis=1); ok = ln > 1e-12
    V, n = V[ok], n[ok] / ln[ok][:, None]
    sh = np.clip(np.abs(n @ LUZ), 0, 1) * 0.74 + 0.26
    sx = (V[:, :, 0] - c[0]) * sc + W2 / 2
    sy = H2 / 2 - (V[:, :, 1] - c[1]) * sc
    sz = V[:, :, 2]
    for i in range(len(V)):
        ax, ay = sx[i, 0], sy[i, 0]; bx, by = sx[i, 1], sy[i, 1]; cx, cy = sx[i, 2], sy[i, 2]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9: continue
        X0 = max(int(min(ax, bx, cx)), 0); X1 = min(int(max(ax, bx, cx)) + 1, W2 - 1)
        Y0 = max(int(min(ay, by, cy)), 0); Y1 = min(int(max(ay, by, cy)) + 1, H2 - 1)
        if X1 < X0 or Y1 < Y0: continue
        gx, gy = np.meshgrid(np.arange(X0, X1 + 1) + .5, np.arange(Y0, Y1 + 1) + .5)
        l1 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / den
        l2 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / den
        m = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
        if not m.any(): continue
        z = l1 * sz[i, 0] + l2 * sz[i, 1] + (1 - l1 - l2) * sz[i, 2]
        sub = zb[Y0:Y1+1, X0:X1+1]; up = m & (z > sub); sub[up] = z[up]
        img[Y0:Y1+1, X0:X1+1][up] = np.array(COR) * sh[i]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

def bloco(im):
    im = im.copy(); im.thumbnail((W, H), Image.LANCZOS)
    cv = Image.new('RGB', (W, H), FUNDO)
    cv.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    buf = io.BytesIO(); cv.save(buf, 'PNG', optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    ls = ['; thumbnail begin %dx%d %d' % (W, H, len(b64))]
    ls += ['; ' + b64[i:i+76] for i in range(0, len(b64), 76)]
    ls += ['; thumbnail end', ';']
    return '\n'.join(ls) + '\n'

g = pathlib.Path(sys.argv[1]); stls = sys.argv[2:]
L = g.read_text(errors='ignore').splitlines(keepends=True)
if any('thumbnail begin' in l for l in L[:80]):
    print('%s ja tem miniatura' % g.name)
else:
    b = bloco(render(stls))
    L.insert(1, b); g.write_text(''.join(L))
    print('%-26s miniatura 230x110 injetada (%d bytes)' % (g.name, len(b)))
