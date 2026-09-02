# -*- coding: utf-8 -*-
"""Rasterizador z-buffer em Python puro — so para conferir a geometria."""
import math, zlib, struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pecas

W, H = 760, 560


def norm(v):
    L = math.sqrt(sum(c * c for c in v)) or 1.0
    return [c / L for c in v]


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def render(items, eye, tgt, fov=32.0, clip=None, bg=(18, 22, 24), path='out.png'):
    up = [0, 0, 1]
    zc = norm([eye[i]-tgt[i] for i in range(3)])
    xc = norm(cross(up, zc)); yc = cross(zc, xc)
    f = 1.0 / math.tan(math.radians(fov) / 2)
    zbuf = [1e30] * (W * H)
    img = [bg[0], bg[1], bg[2]] * (W * H)
    L1, L2, L3 = norm([-0.45, -0.8, 0.75]), norm([0.85, 0.25, 0.35]), norm([0.1, 0.9, -0.5])
    for (m, color, xf) in items:
        for (ia, ib, ic) in m.F:
            P = []
            ok = True
            for idx in (ia, ib, ic):
                p = m.V[idx]
                if xf: p = xf(p)
                if clip and clip(p): ok = False; break
                P.append(p)
            if not ok: continue
            u = [P[1][i]-P[0][i] for i in range(3)]
            v = [P[2][i]-P[0][i] for i in range(3)]
            n = norm(cross(u, v))
            S = []
            for p in P:
                d = [p[i]-eye[i] for i in range(3)]
                cx = sum(d[i]*xc[i] for i in range(3))
                cy = sum(d[i]*yc[i] for i in range(3))
                cz = sum(d[i]*zc[i] for i in range(3))
                if cz > -1e-3: ok = False; break
                S.append((W/2 + f*cx/(-cz)*(H/2), H/2 - f*cy/(-cz)*(H/2), -cz))
            if not ok: continue
            ax = (S[1][0]-S[0][0])*(S[2][1]-S[0][1]) - (S[1][1]-S[0][1])*(S[2][0]-S[0][0])
            if ax >= 0: continue                      # backface
            sh = (0.30 + 0.62*max(0.0, sum(n[i]*L1[i] for i in range(3)))
                  + 0.26*max(0.0, sum(n[i]*L2[i] for i in range(3)))
                  + 0.14*max(0.0, sum(n[i]*L3[i] for i in range(3))))
            col = [min(255, int(c*sh)) for c in color]
            x0 = max(0, int(min(s[0] for s in S))); x1 = min(W-1, int(max(s[0] for s in S))+1)
            y0 = max(0, int(min(s[1] for s in S))); y1 = min(H-1, int(max(s[1] for s in S))+1)
            if x1 < x0 or y1 < y0: continue
            (px0, py0, pz0), (px1, py1, pz1), (px2, py2, pz2) = S
            den = (py1-py2)*(px0-px2) + (px2-px1)*(py0-py2)
            if abs(den) < 1e-9: continue
            for py in range(y0, y1+1):
                yy = py + 0.5
                for px in range(x0, x1+1):
                    xx = px + 0.5
                    w0 = ((py1-py2)*(xx-px2) + (px2-px1)*(yy-py2)) / den
                    if w0 < 0: continue
                    w1 = ((py2-py0)*(xx-px2) + (px0-px2)*(yy-py2)) / den
                    if w1 < 0: continue
                    w2 = 1 - w0 - w1
                    if w2 < 0: continue
                    z = w0*pz0 + w1*pz1 + w2*pz2
                    o = py*W + px
                    if z < zbuf[o]:
                        zbuf[o] = z
                        img[o*3], img[o*3+1], img[o*3+2] = col
    raw = b''.join(b'\x00' + bytes(img[y*W*3:(y+1)*W*3]) for y in range(H))
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))
    open(path, 'wb').write(png)
    return path


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    corpo, tampa, porta = pecas.corpo(), pecas.tampa(), pecas.portinhola()
    PP = (196, 208, 212); TP = (36, 150, 160); PO = (222, 226, 224)
    up = lambda dz: (lambda p: (p[0], p[1], p[2]+dz))
    def rot(th):
        hy, hz = pecas.P['HINGE_Y'], pecas.P['HINGE_Z']
        c, s = math.cos(th), math.sin(th)
        return lambda p: (p[0], hy + (p[1]-hy)*c - (p[2]-hz)*s, hz + (p[1]-hy)*s + (p[2]-hz)*c)
    tgt = (0, 0, 68)
    render([(corpo, PP, None), (tampa, TP, None), (porta, PO, None)],
           (330, -430, 300), tgt, path=os.path.join(here, 'web/v-montado.png'))
    render([(corpo, PP, None), (tampa, TP, up(48)), (porta, PO, up(96))],
           (330, -430, 330), (0, 0, 90), path=os.path.join(here, 'web/v-explodido.png'))
    render([(corpo, PP, None), (tampa, TP, None), (porta, PO, rot(1.4))],
           (250, -400, 330), (0, 20, 95), fov=26, path=os.path.join(here, 'web/v-aberta.png'))
    render([(corpo, PP, None), (tampa, TP, None), (porta, PO, None)],
           (300, -60, 128), (0, 60, 112), fov=14,
           clip=lambda p: p[0] > 0.5, path=os.path.join(here, 'web/v-secao.png'))
    print('ok')
