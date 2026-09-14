"""Malha -> arte de linha vetorial, com remocao de linha oculta por z-buffer.

Emite dois tracos: 'feito' (o que ja estava montado) e 'novo' (o que entra na
etapa), para a ilustracao mostrar o que muda sem precisar de seta.
"""
import numpy as np, math, struct


# ---------------------------------------------------------------- malhas
def caixa(p0, p1):
    """12 triangulos de um prisma retangular entre dois cantos opostos."""
    (x0, y0, z0), (x1, y1, z1) = p0, p1
    v = np.array([[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],
                  [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]], float)
    f = [(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
         (1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]
    return v[np.array(f)]


def le_stl(path):
    d = open(path, 'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    raw = np.frombuffer(d[84:84 + n * 50], dtype=np.uint8).reshape(n, 50)
    return raw[:, :48].copy().view(np.float32).reshape(n, 4, 3)[:, 1:, :].astype(np.float64)


# ---------------------------------------------------------------- camera
def _base(eye, up=(0, 0, 1.0)):
    f = np.array(eye, float); f /= np.linalg.norm(f)
    up = np.array(up, float)
    r = np.cross(up, f); r /= np.linalg.norm(r)
    return r, np.cross(f, r), f


def _zbuffer(P, D, faces, W, H):
    zb = np.full((H, W), -1e18)
    a, b, c = P[faces[:, 0]], P[faces[:, 1]], P[faces[:, 2]]
    da, db, dc = D[faces[:, 0]], D[faces[:, 1]], D[faces[:, 2]]
    area = (b[:,0]-a[:,0])*(c[:,1]-a[:,1]) - (b[:,1]-a[:,1])*(c[:,0]-a[:,0])
    for i in np.nonzero(np.abs(area) > 1e-9)[0]:
        x0 = max(int(min(a[i,0], b[i,0], c[i,0])), 0); x1 = min(int(max(a[i,0], b[i,0], c[i,0])) + 1, W - 1)
        y0 = max(int(min(a[i,1], b[i,1], c[i,1])), 0); y1 = min(int(max(a[i,1], b[i,1], c[i,1])) + 1, H - 1)
        if x1 < x0 or y1 < y0: continue
        gx, gy = np.meshgrid(np.arange(x0, x1+1) + .5, np.arange(y0, y1+1) + .5)
        w0 = ((b[i,0]-a[i,0])*(gy-a[i,1]) - (b[i,1]-a[i,1])*(gx-a[i,0])) / area[i]
        w1 = ((c[i,0]-b[i,0])*(gy-b[i,1]) - (c[i,1]-b[i,1])*(gx-b[i,0])) / area[i]
        w2 = 1.0 - w0 - w1
        m = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9)
        if not m.any(): continue
        z = w1*da[i] + w2*db[i] + w0*dc[i]
        sub = zb[y0:y1+1, x0:x1+1]
        upd = m & (z > sub)
        sub[upd] = z[upd]
    return zb


# ---------------------------------------------------------------- desenho
def desenha(tris, saida, grupos=None, eye=(1., -1., .62), up=(0, 0, 1.),
            lado=760, pad=26, vinco=22.0, res=1100, traco=(2.6, 1.5), ref=None,
            baloes=None, caixa_mm=(41, 22)):
    """tris (n,3,3); grupos (n,) com 0='feito' e 1='novo' (ou None = tudo novo).

    ref: malha que define o enquadramento. Passando a mesma ref para varias
    etapas, todas saem no mesmo tamanho e a estrutura cresce dentro do quadro.

    baloes: [(ponto3d, numero)] — a identificacao das pecas. O tamanho sai de
    caixa_mm (a area, em mm, onde o desenho vai ser impresso), para o balao
    sair do mesmo tamanho em todas as ilustracoes, qualquer que seja a escala.
    """
    if grupos is None: grupos = np.ones(len(tris), int)
    grupos = np.asarray(grupos, int)

    plano = tris.reshape(-1, 3)
    chave = np.round(plano, 4)
    verts, inv = np.unique(chave, axis=0, return_inverse=True)
    faces = inv.reshape(-1, 3)

    r_, u_, f = _base(eye, up)
    r, u = r_, u_
    moldura = (tris if ref is None else ref).reshape(-1, 3)
    centro = moldura.mean(0)
    verts = verts - centro
    mold = moldura - centro
    MX, MY = mold @ r, mold @ u
    X, Y, Z = verts @ r, verts @ u, verts @ f
    s = min((lado - 2*pad) / max(np.ptp(MX), 1e-9), (lado - 2*pad) / max(np.ptp(MY), 1e-9))
    w, h = np.ptp(MX)*s + 2*pad, np.ptp(MY)*s + 2*pad
    P = np.column_stack([(X - MX.min())*s + pad, (MY.max() - Y)*s + pad])

    A, B, C = verts[faces[:,0]], verts[faces[:,1]], verts[faces[:,2]]
    N = np.cross(B - A, C - A)
    ln = np.linalg.norm(N, axis=1, keepdims=True); ln[ln == 0] = 1
    N /= ln
    frente = (N @ f) > 0

    arestas = {}
    for fi, tri in enumerate(faces):
        for k in range(3):
            a_, b_ = tri[k], tri[(k+1) % 3]
            arestas.setdefault((a_, b_) if a_ < b_ else (b_, a_), []).append(fi)

    cos_t = math.cos(math.radians(vinco))
    feats = []
    for (a_, b_), fl in arestas.items():
        if len(fl) == 1:
            feats.append((a_, b_, True, grupos[fl[0]])); continue
        f0, f1 = fl[0], fl[1]
        g = max(grupos[f0], grupos[f1])
        if frente[f0] != frente[f1]:
            feats.append((a_, b_, True, g))
        elif (frente[f0] or frente[f1]) and float(N[f0] @ N[f1]) < cos_t:
            feats.append((a_, b_, False, g))

    escala = res / max(w, h)
    RW, RH = int(w*escala) + 2, int(h*escala) + 2
    zb = _zbuffer(P*escala, Z, faces, RW, RH)
    vies = max(np.ptp(Z), 1e-9) * 0.007

    saidas = {(g, sil): [] for g in (0, 1) for sil in (0, 1)}
    for (a_, b_, sil, g) in feats:
        p0, p1, z0, z1 = P[a_], P[b_], Z[a_], Z[b_]
        L = float(np.hypot(*(p1 - p0)))
        n = max(2, int(L/1.6) + 1)
        t = np.linspace(0, 1, n)
        sp = p0[None,:]*(1-t)[:,None] + p1[None,:]*t[:,None]
        sz = z0*(1-t) + z1*t
        ix = np.clip((sp[:,0]*escala).astype(int), 0, RW-1)
        iy = np.clip((sp[:,1]*escala).astype(int), 0, RH-1)
        vis = sz + vies >= zb[iy, ix]
        ini = None
        for k in range(n):
            if vis[k] and ini is None: ini = k
            if (not vis[k] or k == n-1) and ini is not None:
                fim = k if vis[k] else k-1
                if fim > ini and np.hypot(*(sp[fim] - sp[ini])) > .8:
                    saidas[(g, int(sil))].append((sp[ini], sp[fim]))
                ini = None

    def d(segs):
        return " ".join(f"M{a[0]:.1f} {a[1]:.1f}L{b[0]:.1f} {b[1]:.1f}" for a, b in segs)

    largo, fino = traco
    camadas = [
        (saidas[(0, 0)], fino * .62, .45), (saidas[(0, 1)], largo * .52, .55),
        (saidas[(1, 0)], fino,       .85), (saidas[(1, 1)], largo,       1.0),
    ]
    corpo = "".join(
        f'<path d="{d(sg)}" stroke-width="{lw:.2f}" opacity="{op}"/>'
        for sg, lw, op in camadas if sg)
    marcas = ''
    if baloes:
        cw, ch = caixa_mm
        mm = min(cw / w, ch / h)                      # mm por unidade do desenho
        r, fs, lw = 1.35 / mm, 1.85 / mm, 0.20 / mm
        for ponto, n in baloes:
            q = np.asarray(ponto, float) - centro
            cx = float((q @ r_) - MX.min()) * s + pad
            cy = (MY.max() - float(q @ u_)) * s + pad
            cx = min(max(cx, r + 1), w - r - 1)
            cy = min(max(cy, r + 1), h - r - 1)
            marcas += (f'<g><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="#fff" '
                       f'stroke="currentColor" stroke-width="{lw:.2f}"/>'
                       f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="{fs:.1f}" '
                       f'text-anchor="middle" dominant-baseline="central" '
                       f'fill="currentColor" stroke="none">{n}</text></g>')
        marcas = f'<g class="baloes">{marcas}</g>'

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" '
           f'width="{w:.0f}" height="{h:.0f}">'
           f'<g fill="none" stroke="currentColor" stroke-linecap="round" '
           f'stroke-linejoin="round">{corpo}</g>{marcas}</svg>')
    open(saida, 'w').write(svg)
    return w, h, sum(len(v) for v in saidas.values())
