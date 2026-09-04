"""
Nucleo geometrico rev.02 — casca de contorno arredondado.

A peca deixa de ser uma caixa de faces planas: a planta e um retangulo de
cantos arredondados, e a parede e uma CASCA varrida ao longo desse contorno.

Toda a peca e definida por um contorno parametrico avaliavel em qualquer
altura z:

    X(z) = X0 + 2*z*tan(saida)     Y(z) = Y0 + 2*z*tan(saida)
    R(z) = R0 +   z*tan(saida)

Cada amostra do contorno guarda (trecho, t), entao a amostra i em z=0 e a
amostra i em z=H sao o MESMO ponto do perimetro — e um prisma entre duas
alturas fecha sem torcao.
"""
import math

DEG = math.pi / 180.0

TRECHOS_RETOS = ("lat_d", "frente", "lat_e", "traseira")


class Contorno:
    """
    Retangulo de cantos arredondados, avaliavel em qualquer z.

    O RAIO E CONSTANTE em toda a altura; o que cresce sao as meias-dimensoes.
    Isso tem duas consequencias boas: o canto nao degenera quando a saida e
    grande (com offset puro o raio da base ficaria negativo), e a superficie do
    canto fica MAIS inclinada que a dos lados (no vertice a 45 graus, 1,41x),
    o que ajuda o ninho em vez de limita-lo — quem manda no passo continua
    sendo o trecho reto.
    """

    def __init__(self, X, Y, R, tan, passo=5.0, n_arco=9):
        self.X, self.Y, self.R, self.tan = X, Y, R, tan
        hx, hy = X / 2.0, Y / 2.0
        n_lat = max(2, int(round(2 * (hy - R) / passo)))
        n_fre = max(2, int(round(2 * (hx - R) / passo)))
        self.amostras = []                       # (trecho, t)
        for tr, n in (("lat_d", n_lat), ("canto_fd", n_arco), ("frente", n_fre),
                      ("canto_fe", n_arco), ("lat_e", n_lat), ("canto_te", n_arco),
                      ("traseira", n_fre), ("canto_td", n_arco)):
            for i in range(n):
                self.amostras.append((tr, i / n))
        self.n = len(self.amostras)
        base = [self.ponto(i, 0.0) for i in range(self.n)]
        self.s = [0.0]
        for i in range(1, self.n + 1):
            a, b = base[i - 1], base[i % self.n]
            self.s.append(self.s[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        self.perimetro = self.s[-1]

    # -- avaliacao ---------------------------------------------------------
    def ponto(self, i, z):
        """(x, y, nx, ny) da amostra i na altura z; n = normal externa."""
        tr, t = self.amostras[i % self.n]
        d = z * self.tan
        hx, hy, r = self.X / 2 + d, self.Y / 2 + d, self.R
        a, b = hx - r, hy - r
        if tr == "lat_d":
            return (hx, -b + t * 2 * b, 1.0, 0.0)
        if tr == "lat_e":
            return (-hx, b - t * 2 * b, -1.0, 0.0)
        if tr == "frente":
            return (a - t * 2 * a, hy, 0.0, 1.0)
        if tr == "traseira":
            return (-a + t * 2 * a, -hy, 0.0, -1.0)
        cx, cy, ang0 = {"canto_fd": (a, b, 0.0), "canto_fe": (-a, b, 90.0),
                        "canto_te": (-a, -b, 180.0), "canto_td": (a, -b, 270.0)}[tr]
        ang = (ang0 + t * 90.0) * DEG
        return (cx + r * math.cos(ang), cy + r * math.sin(ang),
                math.cos(ang), math.sin(ang))

    def pt(self, i, z, o=0.0):
        """Ponto do contorno na amostra i, altura z, deslocado o pela normal."""
        x, y, nx, ny = self.ponto(i, z)
        return (x + o * nx, y + o * ny)

    def y_de(self, i):
        return self.ponto(i, 0.0)[1]

    def indice_livre(self):
        return 0

    def trecho(self, i):
        return self.amostras[i % self.n][0]

    def indices_por_y(self, lado, y0, y1):
        """Amostras de um trecho lateral cujo y (em z=0) cai na faixa."""
        tr = "lat_d" if lado > 0 else "lat_e"
        return [i for i in range(self.n)
                if self.trecho(i) == tr and y0 <= self.y_de(i) <= y1]


class Malha:
    """Acumula triangulos com etiqueta."""

    def __init__(self):
        self.tris = []

    def tri(self, a, b, c, tag):
        self.tris.append((a, b, c, tag))

    def quad(self, a, b, c, d, tag):
        self.tris.append((a, b, c, tag))
        self.tris.append((a, c, d, tag))

    def hexa(self, base, topo, tag):
        """base/topo = 4 vertices em ordem (mesmo sentido)."""
        b0, b1, b2, b3 = base
        t0, t1, t2, t3 = topo
        self.quad(b0, b3, b2, b1, tag)
        self.quad(t0, t1, t2, t3, tag)
        self.quad(b0, b1, t1, t0, tag)
        self.quad(b1, b2, t2, t1, tag)
        self.quad(b2, b3, t3, t2, tag)
        self.quad(b3, b0, t0, t3, tag)

    def bloco(self, x0, x1, y0, y1, z0, z1, tag):
        self.hexa([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],
                  [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], tag)

    def caixa_oca(self, x0, x1, y0, y1, z0, z1, esp, tag, tampa="topo"):
        """Bloco com as 4 paredes e uma tampa — o vazio vira encaixe."""
        self.bloco(x0, x1, y0, y0 + esp, z0, z1, tag)
        self.bloco(x0, x1, y1 - esp, y1, z0, z1, tag)
        self.bloco(x0, x0 + esp, y0 + esp, y1 - esp, z0, z1, tag)
        self.bloco(x1 - esp, x1, y0 + esp, y1 - esp, z0, z1, tag)
        if tampa == "topo":
            self.bloco(x0, x1, y0, y1, z1 - esp, z1, tag)
        elif tampa == "fundo":
            self.bloco(x0, x1, y0, y1, z0, z0 + esp, tag)

    def normais_suaves(self, crease=42.0):
        """Normal por canto de face, mediando so entre faces quase coplanares.
        Deixa o canto arredondado liso e a quina viva nitida."""
        from collections import defaultdict
        nf = []
        for a, b, c, _ in self.tris:
            u = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
            v = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
            n = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
            L = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2) or 1.0
            nf.append((n[0]/L, n[1]/L, n[2]/L))
        ch = lambda p: (round(p[0]*8), round(p[1]*8), round(p[2]*8))
        viz = defaultdict(list)
        for i, (a, b, c, _) in enumerate(self.tris):
            for p in (a, b, c):
                viz[ch(p)].append(i)
        lim = math.cos(crease * DEG)
        saida = []
        for i, (a, b, c, _) in enumerate(self.tris):
            base = nf[i]
            cantos = []
            for p in (a, b, c):
                ax = ay = az = 0.0
                for j in viz[ch(p)]:
                    o = nf[j]
                    if base[0]*o[0] + base[1]*o[1] + base[2]*o[2] >= lim:
                        ax += o[0]; ay += o[1]; az += o[2]
                L = math.sqrt(ax*ax + ay*ay + az*az)
                cantos.append((ax/L, ay/L, az/L) if L > 1e-9 else base)
            saida.append(cantos)
        return saida

    def volume(self):
        """cm3 pelo teorema da divergencia (malha fechada o suficiente)."""
        v = 0.0
        for a, b, c, _ in self.tris:
            v += (a[0] * (b[1] * c[2] - b[2] * c[1])
                  - a[1] * (b[0] * c[2] - b[2] * c[0])
                  + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
        return abs(v) / 1000.0

    def triangulos(self, offset=(0, 0, 0), giro180=False):
        ox, oy, oz = offset
        fora = []
        for a, b, c, tag in self.tris:
            if giro180:
                a = (-a[0], -a[1], a[2]); b = (-b[0], -b[1], b[2]); c = (-c[0], -c[1], c[2])
                a, b, c = a, c, b
            fora.append(((a[0] + ox, a[1] + oy, a[2] + oz),
                         (b[0] + ox, b[1] + oy, b[2] + oz),
                         (c[0] + ox, c[1] + oy, c[2] + oz), tag))
        return fora


def banda(malha, cont, i0, i1, o_ext, o_int, z_de, z_ate, tag,
          tampa_ini=True, tampa_fim=True):
    """
    Casca continua entre as amostras i0..i1, entre as curvas deslocadas o_ext e
    o_int, da altura z_de(i) ate z_ate(i) (funcoes do indice, para o topo variar).
    Emite face externa, interna, topo, base e as tampas de extremidade.
    """
    if i1 <= i0:
        return
    for i in range(i0, i1):
        za0, za1 = z_de(i), z_ate(i)
        zb0, zb1 = z_de(i + 1), z_ate(i + 1)
        if za1 - za0 < 0.05 and zb1 - zb0 < 0.05:
            continue
        ea0 = cont.pt(i, za0, o_ext); ea1 = cont.pt(i, za1, o_ext)
        ia0 = cont.pt(i, za0, o_int); ia1 = cont.pt(i, za1, o_int)
        eb0 = cont.pt(i + 1, zb0, o_ext); eb1 = cont.pt(i + 1, zb1, o_ext)
        ib0 = cont.pt(i + 1, zb0, o_int); ib1 = cont.pt(i + 1, zb1, o_int)
        A0 = (ea0[0], ea0[1], za0); A1 = (ea1[0], ea1[1], za1)
        B0 = (eb0[0], eb0[1], zb0); B1 = (eb1[0], eb1[1], zb1)
        a0 = (ia0[0], ia0[1], za0); a1 = (ia1[0], ia1[1], za1)
        b0 = (ib0[0], ib0[1], zb0); b1 = (ib1[0], ib1[1], zb1)
        malha.quad(A0, B0, B1, A1, tag)      # externa
        malha.quad(a0, a1, b1, b0, tag)      # interna
        malha.quad(A1, B1, b1, a1, tag)      # topo
        malha.quad(A0, a0, b0, B0, tag)      # base
        if i == i0 and tampa_ini:
            malha.quad(A0, A1, a1, a0, tag)
        if i == i1 - 1 and tampa_fim:
            malha.quad(B0, b0, b1, B1, tag)


def tubo_roundrect(malha, cx, cy, W, D, R, z0, z1, esp, tag, n_arco=6, cone=1.5):
    """Pe: caixa oca de planta arredondada, fechada em cima e aberta embaixo.
    O vazio de dentro e o encaixe. 'cone' = recuo por lado do topo (saida)."""
    R = max(1.5, min(R, min(W, D) / 2 - 0.5))
    pts, ax, ay = [], W / 2 - R, D / 2 - R
    for (qx, qy, a0) in ((ax, ay, 0.0), (-ax, ay, 90.0), (-ax, -ay, 180.0), (ax, -ay, 270.0)):
        for k in range(n_arco + 1):
            a = (a0 + 90.0 * k / n_arco) * DEG
            pts.append((qx + R * math.cos(a), qy + R * math.sin(a)))
    n = len(pts)
    esc1 = 1.0 - 2.0 * cone / max(W, D)

    def V(i, z, dentro, topo):
        x, y = pts[i % n]
        k = esc1 if topo else 1.0
        x, y = x * k, y * k
        if dentro:
            L = math.hypot(x, y) or 1.0
            x, y = x - esp * x / L, y - esp * y / L
        return (cx + x, cy + y, z)

    zt = z1 - esp
    for i in range(n):
        A0, B0 = V(i, z0, 0, 0), V(i + 1, z0, 0, 0)
        A1, B1 = V(i, z1, 0, 1), V(i + 1, z1, 0, 1)
        a0, b0 = V(i, z0, 1, 0), V(i + 1, z0, 1, 0)
        a1, b1 = V(i, zt, 1, 1), V(i + 1, zt, 1, 1)
        malha.quad(A0, B0, B1, A1, tag)          # face externa
        malha.quad(a0, a1, b1, b0, tag)          # face interna
        malha.quad(A0, a0, b0, B0, tag)          # anel de baixo
        malha.quad(a1, A1, B1, b1, tag)          # anel de topo (sob a tampa)
    c1 = (cx, cy, z1)
    ct = (cx, cy, zt)
    for i in range(n):
        A1, B1 = V(i, z1, 0, 1), V(i + 1, z1, 0, 1)
        a1, b1 = V(i, zt, 1, 1), V(i + 1, zt, 1, 1)
        malha.tri(c1, A1, B1, tag)               # topo
        malha.tri(ct, b1, a1, tag)               # face de baixo da tampa
