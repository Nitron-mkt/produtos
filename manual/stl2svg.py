import numpy as np, struct, os, sys, math, json

def load(path):
    d = open(path,'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    raw = np.frombuffer(d[84:84+n*50], dtype=np.uint8).reshape(n,50)
    fl = raw[:,:48].copy().view(np.float32).reshape(n,4,3)
    return fl[:,1:,:].astype(np.float64)   # (n,3,3)

def weld(tris, tol=4):
    v = tris.reshape(-1,3)
    key = np.round(v, tol)
    uniq, inv = np.unique(key, axis=0, return_inverse=True)
    return uniq, inv.reshape(-1,3)

def basis(eye, up=(0,0,1.0)):
    f = np.array(eye, float); f /= np.linalg.norm(f)     # points from origin toward camera
    up = np.array(up, float)
    r = np.cross(up, f); r /= np.linalg.norm(r)
    u = np.cross(f, r)
    return r, u, f

def rasterize(P, D, faces, W, H):
    """painter z-buffer; P (m,2) px coords, D (m,) depth (larger = closer)."""
    zb = np.full((H, W), -1e18)
    a, b, c = P[faces[:,0]], P[faces[:,1]], P[faces[:,2]]
    da, db, dc = D[faces[:,0]], D[faces[:,1]], D[faces[:,2]]
    area = (b[:,0]-a[:,0])*(c[:,1]-a[:,1]) - (b[:,1]-a[:,1])*(c[:,0]-a[:,0])
    keep = np.abs(area) > 1e-9
    for i in np.nonzero(keep)[0]:
        x0 = max(int(np.floor(min(a[i,0],b[i,0],c[i,0]))), 0)
        x1 = min(int(np.ceil (max(a[i,0],b[i,0],c[i,0]))), W-1)
        y0 = max(int(np.floor(min(a[i,1],b[i,1],c[i,1]))), 0)
        y1 = min(int(np.ceil (max(a[i,1],b[i,1],c[i,1]))), H-1)
        if x1 < x0 or y1 < y0: continue
        xs = np.arange(x0, x1+1) + 0.5
        ys = np.arange(y0, y1+1) + 0.5
        gx, gy = np.meshgrid(xs, ys)
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

def render(path, out, eye=(1.0,-1.0,0.62), up=(0,0,1.0), size=760, pad=28,
           crease_deg=22.0, res=1100):
    tris = load(path)
    verts, faces = weld(tris)
    r, u, f = basis(eye, up)
    verts = verts - verts.mean(0)

    X = verts @ r; Y = verts @ u; Z = verts @ f      # Z: larger = closer to camera
    sx = (size - 2*pad) / max(X.max()-X.min(), 1e-9)
    sy = (size - 2*pad) / max(Y.max()-Y.min(), 1e-9)
    s = min(sx, sy)
    w = (X.max()-X.min())*s + 2*pad
    h = (Y.max()-Y.min())*s + 2*pad
    px = (X - X.min())*s + pad
    py = (Y.max() - Y)*s + pad                        # flip for SVG
    P = np.column_stack([px, py])

    # face normals / orientation
    A, B, C = verts[faces[:,0]], verts[faces[:,1]], verts[faces[:,2]]
    N = np.cross(B-A, C-A)
    ln = np.linalg.norm(N, axis=1, keepdims=True); ln[ln==0] = 1
    N = N/ln
    front = (N @ f) > 0

    # edge -> adjacent faces
    emap = {}
    for fi, tri in enumerate(faces):
        for k in range(3):
            a_, b_ = tri[k], tri[(k+1) % 3]
            key = (a_, b_) if a_ < b_ else (b_, a_)
            emap.setdefault(key, []).append(fi)

    cos_t = math.cos(math.radians(crease_deg))
    feats = []      # (i, j, is_silhouette)
    for (a_, b_), fl_ in emap.items():
        if len(fl_) == 1:
            feats.append((a_, b_, True)); continue
        f0, f1 = fl_[0], fl_[1]
        sil = front[f0] != front[f1]
        if sil:
            feats.append((a_, b_, True))
        elif (front[f0] or front[f1]) and float(N[f0] @ N[f1]) < cos_t:
            feats.append((a_, b_, False))

    # z-buffer at higher res, then sample edges for visibility
    scale = res / max(w, h)
    RW, RH = int(w*scale)+2, int(h*scale)+2
    zb = rasterize(P*scale, Z, faces, RW, RH)
    span = max(Z.max()-Z.min(), 1e-9)
    bias = span * 0.007

    out_sil, out_cre = [], []
    for (a_, b_, sil) in feats:
        p0, p1 = P[a_], P[b_]
        z0, z1 = Z[a_], Z[b_]
        L = np.hypot(*(p1-p0))
        n = max(2, int(L/1.6)+1)
        t = np.linspace(0, 1, n)
        sp = p0[None,:]*(1-t)[:,None] + p1[None,:]*t[:,None]
        sz = z0*(1-t) + z1*t
        ix = np.clip((sp[:,0]*scale).astype(int), 0, RW-1)
        iy = np.clip((sp[:,1]*scale).astype(int), 0, RH-1)
        vis = sz + bias >= zb[iy, ix]
        # group runs
        start = None
        for k in range(n):
            if vis[k] and start is None: start = k
            if (not vis[k] or k == n-1) and start is not None:
                end = k if vis[k] else k-1
                if end - start >= 1 or n == 2:
                    q0, q1 = sp[start], sp[end]
                    if np.hypot(*(q1-q0)) > 0.8:
                        (out_sil if sil else out_cre).append((q0, q1))
                start = None

    def d(segs):
        return " ".join(f"M{a[0]:.2f} {a[1]:.2f}L{b[0]:.2f} {b[1]:.2f}" for a, b in segs)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}">
<g fill="none" stroke="#111" stroke-linecap="round" stroke-linejoin="round">
<path class="crease" d="{d(out_cre)}" stroke-width="1.5" opacity="0.85"/>
<path class="outline" d="{d(out_sil)}" stroke-width="2.6"/>
</g>
</svg>'''
    open(out,'w').write(svg)
    print(f"{os.path.basename(out):28s} {w:.0f}x{h:.0f}  sil={len(out_sil):5d} crease={len(out_cre):5d}")

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--eye', default='1,-1,0.62')
    ap.add_argument('--crease', type=float, default=22.0)
    a = ap.parse_args()
    render(a.src, a.dst, eye=tuple(float(x) for x in a.eye.split(',')), crease_deg=a.crease)
