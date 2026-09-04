"""
Nucleo geometrico da familia MODULA — organizador modular Nitron.

Modelo de estudo construido por prismas retos (hexaedros) com topo opcionalmente
inclinado. Toda a peca e desenhada no referencial da BASE (secao menor) e a
conicidade e aplicada na emissao dos vertices como escalonamento em torno do
eixo vertical:

    x' = x * (1 + 2*z*tan(ax) / Xb)
    y' = y * (1 + 2*z*tan(ay) / Yb)

Isso reproduz um tronco de piramide com erro < 0,2 mm nas faces internas.
"""
import math

DEG = math.pi / 180.0


class Prisma:
    """Hexaedro: base retangular, topo podendo inclinar linearmente em y."""

    __slots__ = ("x0", "x1", "y0", "y1", "z0", "z1a", "z1b", "tag")

    def __init__(self, x0, x1, y0, y1, z0, z1, z1b=None, tag="corpo"):
        self.x0, self.x1 = min(x0, x1), max(x0, x1)
        self.y0, self.y1 = min(y0, y1), max(y0, y1)
        self.z0 = z0
        self.z1a = z1
        self.z1b = z1 if z1b is None else z1b
        self.tag = tag

    def volume(self):
        return (self.x1 - self.x0) * (self.y1 - self.y0) * (
            (self.z1a + self.z1b) / 2.0 - self.z0)


class Solido:
    """Colecao de prismas + a lei de conicidade."""

    def __init__(self, Xb, Yb, tan_x, tan_y):
        self.Xb, self.Yb = Xb, Yb
        self.tx, self.ty = tan_x, tan_y
        self.pecas = []

    def add(self, x0, x1, y0, y1, z0, z1, z1b=None, tag="corpo"):
        if abs(x1 - x0) < 1e-6 or abs(y1 - y0) < 1e-6:
            return
        if max(z1, z1 if z1b is None else z1b) - z0 < 1e-6:
            return
        self.pecas.append(Prisma(x0, x1, y0, y1, z0, z1, z1b, tag))

    # -- conicidade -------------------------------------------------------
    def sx(self, z):
        return 1.0 + 2.0 * z * self.tx / self.Xb

    def sy(self, z):
        return 1.0 + 2.0 * z * self.ty / self.Yb

    def ponto(self, x, y, z):
        return (x * self.sx(z), y * self.sy(z), z)

    # -- malha ------------------------------------------------------------
    def triangulos(self, offset=(0.0, 0.0, 0.0), giro180=False):
        """Devolve [(v0,v1,v2,tag), ...] ja no espaco global."""
        ox, oy, oz = offset
        tris = []
        for p in self.pecas:
            zt = {(p.y0): p.z1a, (p.y1): p.z1b}
            def V(x, y, top):
                z = (p.z1a + (p.z1b - p.z1a) * ((y - p.y0) / (p.y1 - p.y0))) if top else p.z0
                vx, vy, vz = self.ponto(x, y, z)
                if giro180:
                    vx, vy = -vx, -vy
                return (vx + ox, vy + oy, vz + oz)
            b0, b1, b2, b3 = V(p.x0, p.y0, 0), V(p.x1, p.y0, 0), V(p.x1, p.y1, 0), V(p.x0, p.y1, 0)
            t0, t1, t2, t3 = V(p.x0, p.y0, 1), V(p.x1, p.y0, 1), V(p.x1, p.y1, 1), V(p.x0, p.y1, 1)
            quads = [
                (b0, b3, b2, b1),   # fundo  (normal -z)
                (t0, t1, t2, t3),   # topo   (normal +z)
                (b0, b1, t1, t0),   # y-
                (b2, b3, t3, t2),   # y+
                (b3, b0, t0, t3),   # x-
                (b1, b2, t2, t1),   # x+
            ]
            if giro180:
                quads = [tuple(reversed(q)) for q in quads]
            for q in quads:
                tris.append((q[0], q[1], q[2], p.tag))
                tris.append((q[0], q[2], q[3], p.tag))
        return tris

    def volume_material(self):
        """cm3 — soma dos prismas (construidos sem sobreposicao)."""
        v = 0.0
        for p in self.pecas:
            v += p.volume() * self.sx((p.z0 + max(p.z1a, p.z1b)) / 2.0) \
                            * self.sy((p.z0 + max(p.z1a, p.z1b)) / 2.0)
        return v / 1000.0


# ---------------------------------------------------------------------------
# painel com furos: decomposicao exata em prismas
# ---------------------------------------------------------------------------
def painel(sol, esp_a, esp_b, u_de, u_ate, perfil, furos, tag="corpo", eixo="y"):
    """
    Emite um painel plano de espessura [esp_a, esp_b] (coordenada normal),
    varrendo u de u_de ate u_ate, com topo dado por 'perfil' (lista de (u, z)
    interpolada linearmente) e descontando 'furos' = [(u0,u1,z0,z1), ...].

    eixo='y'  -> painel no plano y-z (parede lateral); u = y, normal = x
    eixo='x'  -> painel no plano x-z (parede frontal/traseira); u = x, normal = y
    """
    cortes = {u_de, u_ate}
    for u, _ in perfil:
        if u_de < u < u_ate:
            cortes.add(u)
    for f in furos:
        for u in (f[0], f[1]):
            if u_de < u < u_ate:
                cortes.add(u)
    cortes = sorted(cortes)

    def ztopo(u):
        if u <= perfil[0][0]:
            return perfil[0][1]
        for (ua, za), (ub, zb) in zip(perfil, perfil[1:]):
            if ua <= u <= ub:
                return za + (zb - za) * ((u - ua) / (ub - ua)) if ub > ua else zb
        return perfil[-1][1]

    for ua, ub in zip(cortes, cortes[1:]):
        if ub - ua < 1e-6:
            continue
        um = (ua + ub) / 2.0
        za, zb = ztopo(ua), ztopo(ub)
        zmax = max(za, zb)
        # intervalos solidos em z = [0, topo] - furos que cobrem 'um'
        cortados = sorted([(f[2], f[3]) for f in furos if f[0] - 1e-6 <= um <= f[1] + 1e-6])
        intervalos = []
        z = 0.0
        for h0, h1 in cortados:
            h0, h1 = max(0.0, h0), min(zmax, h1)
            if h1 <= z:
                continue
            if h0 > z:
                intervalos.append((z, h0))
            z = max(z, h1)
        intervalos.append((z, None))            # ultimo pedaco vai ate o perfil
        for z0, z1 in intervalos:
            if z1 is None:
                if zmax - z0 < 0.2:
                    continue
                ta = max(z0, za)
                tb = max(z0, zb)
                if eixo == "y":
                    sol.add(esp_a, esp_b, ua, ub, z0, ta, tb, tag)
                else:
                    sol.add(ua, ub, esp_a, esp_b, z0, (ta + tb) / 2.0, None, tag)
            else:
                if z1 - z0 < 0.2:
                    continue
                if eixo == "y":
                    sol.add(esp_a, esp_b, ua, ub, z0, z1, None, tag)
                else:
                    sol.add(ua, ub, esp_a, esp_b, z0, z1, None, tag)


def grade_furos(u0, u1, z0, z1, n_col, n_lin, larg, alt, tag=None):
    """Distribui n_col x n_lin furos (larg x alt) centrados na regiao dada."""
    furos = []
    if n_col <= 0 or n_lin <= 0:
        return furos
    passo_u = (u1 - u0) / n_col
    passo_z = (z1 - z0) / n_lin
    for i in range(n_col):
        cu = u0 + passo_u * (i + 0.5)
        for j in range(n_lin):
            cz = z0 + passo_z * (j + 0.5)
            furos.append((cu - larg / 2, cu + larg / 2, cz - alt / 2, cz + alt / 2))
    return furos
