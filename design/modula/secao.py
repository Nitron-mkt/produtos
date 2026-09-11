"""Corte de malha por plano (Sutherland-Hodgman por triangulo): e o que permite
render de secao — a peca aberta ao meio mostrando copo dentro de copo e o
rodape dentro do canal — sem precisar de CAD."""


def corta(tris, p0, n):
    """Mantem a parte de cada triangulo onde (p - p0).n >= 0."""
    def d(p):
        return (p[0]-p0[0])*n[0] + (p[1]-p0[1])*n[1] + (p[2]-p0[2])*n[2]

    def inter(a, b, da, db):
        t = da / (da - db)
        return (a[0] + t*(b[0]-a[0]), a[1] + t*(b[1]-a[1]), a[2] + t*(b[2]-a[2]))
    fora = []
    for a, b, c, tag in tris:
        pts = [a, b, c]
        ds = [d(p) for p in pts]
        if all(v >= 0 for v in ds):
            fora.append((a, b, c, tag)); continue
        if all(v < 0 for v in ds):
            continue
        poly = []
        for i in range(3):
            p, q = pts[i], pts[(i+1) % 3]
            dp, dq = ds[i], ds[(i+1) % 3]
            if dp >= 0:
                poly.append(p)
            if (dp >= 0) != (dq >= 0):
                poly.append(inter(p, q, dp, dq))
        for i in range(1, len(poly) - 1):
            fora.append((poly[0], poly[i], poly[i+1], tag))
    return fora
