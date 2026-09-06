"""O grafismo da Nitron — reproduzido do vetor oficial da marca.

FONTE
-----
`marca.nitron.com.br` -> nitron-logos.zip -> `nitron-mark.svg`. O simbolo tem
tres elementos: um longo e dois curtos, todos a mesma faixa dobrada.

Cada elemento e um contorno de seis trechos: reta curta na ponta, curva de
concordancia (o "cotovelo"), reta longa, reta curta na outra ponta, outra curva,
reta longa de volta. As duas retas longas sao PARALELAS — e uma faixa de largura
constante com um dobra de 21 graus no meio. Nao e lente, nao e losango: e a
JUNCAO, que e a ideia do grafismo.

Conferencia: o elemento curto do PNG oficial do grafismo (75x40 px) casa com o
vetor curto na escala 1,533 com **IoU 0,970**; o de 127x75 px casa com o vetor
longo na escala 1,564 com **IoU 0,977**. Mesma escala, mesmos dois elementos —
o grafismo e o simbolo repetido, e nada mais.

REDE
----
Tirada da propria marca, que ja mostra a juncao:

  lado  = ponta do 3o elemento - ponta do 2o = (-40,80 ; -25,47), |v| = 48,10
  eixo  = ponta a ponta do elemento          = ( 15,42 ; -47,61), |v| = 50,04

`lado` e o passo de uma faixa para a vizinha; `eixo` repete a faixa ao longo de
si mesma. Com `eixo` puro as faixas se emendam ponta com ponta e viram fitas
continuas — na marca elas tem folga, e e essa folga que separa um elemento do
outro. Por isso os dois passos entram multiplicados por um fator, que na peca
tambem paga a alma entre os furos.
"""
import math

# --- contorno oficial: seis trechos, coordenadas do SVG (y para baixo) -------
CURTO = [("M", 153.5625, 134.925781), ("L", 149.414062, 147.871094),
         ("C", 148.097656, 151.964844, 148.882812, 156.441406, 151.507812, 159.847656),
         ("L", 168.984375, 182.53125), ("L", 173.136719, 169.589844),
         ("C", 174.449219, 165.492188, 173.667969, 161.015625, 171.042969, 157.609375)]
LONGO = [("M", 163.0, 105.492188), ("L", 159.097656, 117.660156),
         ("C", 157.160156, 123.714844, 158.3125, 130.339844, 162.183594, 135.382812),
         ("L", 200.667969, 185.503906), ("L", 204.570312, 173.335938),
         ("C", 206.511719, 167.28125, 205.359375, 160.652344, 201.484375, 155.613281)]

LADO = (-40.804688, -25.472656)      # ja em y para cima
EIXO = (15.421875, -47.605469)
ANG_EIXO = math.degrees(math.atan2(EIXO[1], EIXO[0]))     # -72,05 graus


def contorno(cmds, n=14):
    """Achata o path em poligono, y para cima, centrado na origem."""
    p, cur = [], None
    for c in cmds:
        if c[0] in "ML":
            cur = (c[1], -c[2]); p.append(cur)
        else:
            p1, p2, p3 = (c[1], -c[2]), (c[3], -c[4]), (c[5], -c[6])
            p0 = cur
            for k in range(1, n + 1):
                u = k / n; w = 1 - u
                p.append((w**3*p0[0] + 3*w*w*u*p1[0] + 3*w*u*u*p2[0] + u**3*p3[0],
                          w**3*p0[1] + 3*w*w*u*p1[1] + 3*w*u*u*p2[1] + u**3*p3[1]))
            cur = p3
    cx = sum(q[0] for q in p) / len(p); cy = sum(q[1] for q in p) / len(p)
    return [(q[0] - cx, q[1] - cy) for q in p]


def _area(p):
    return abs(sum(p[i][0]*p[i-1][1] - p[i-1][0]*p[i][1] for i in range(len(p)))) / 2


def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy) / (dx*dx + dy*dy)))
    return math.hypot(px - (ax + t*dx), py - (ay + t*dy))


class Elemento:
    """A faixa dobrada da marca, escalada e girada."""

    def __init__(self, L, cmds=CURTO, giro=0.0):
        p = contorno(cmds)
        base = math.hypot(EIXO[0], EIXO[1])          # ponta a ponta do curto
        s = L / base
        c, sn = math.cos(math.radians(giro)), math.sin(math.radians(giro))
        self.p = [(s*(x*c - y*sn), s*(x*sn + y*c)) for x, y in p]
        self.r = max(math.hypot(x, y) for x, y in self.p)
        self.area = _area(self.p)
        self.esc = s

    def dentro(self, x, y):
        if x*x + y*y > self.r * self.r:
            return False
        p = self.p; n = len(p); d = False
        j = n - 1
        for i in range(n):
            if (p[i][1] > y) != (p[j][1] > y) and \
               x < (p[j][0]-p[i][0]) * (y-p[i][1]) / (p[j][1]-p[i][1]) + p[i][0]:
                d = not d
            j = i
        return d

    def dist(self, x, y):
        p = self.p
        d = min(_dist_seg(x, y, p[i-1][0], p[i-1][1], p[i][0], p[i][1])
                for i in range(len(p)))
        return -d if self.dentro(x, y) else d

    def borda(self, n=260):
        p = self.p; m = len(p)
        return [p[int(k * m / n) % m] for k in range(n)]


class Trama:
    """O grafismo: o elemento repetido nos dois passos da marca."""

    def __init__(self, el, t1, t2, u0=0.0, z0=0.0):
        self.el, self.t1, self.t2 = el, t1, t2
        self.u0, self.z0 = u0, z0
        det = t1[0]*t2[1] - t1[1]*t2[0]
        self.inv = ((t2[1]/det, -t2[0]/det), (-t1[1]/det, t1[0]/det))
        self.area_celula = abs(det)

    def _ij(self, u, z):
        du, dz = u - self.u0, z - self.z0
        return (self.inv[0][0]*du + self.inv[0][1]*dz,
                self.inv[1][0]*du + self.inv[1][1]*dz)

    def vizinhos(self, u, z, r=1):
        fi, fj = self._ij(u, z)
        i0, j0 = math.floor(fi + 0.5), math.floor(fj + 0.5)
        for di in range(-r, r+1):
            for dj in range(-r, r+1):
                i, j = i0+di, j0+dj
                yield (self.u0 + i*self.t1[0] + j*self.t2[0],
                       self.z0 + i*self.t1[1] + j*self.t2[1])

    def dentro(self, u, z):
        for cu, cz in self.vizinhos(u, z):
            if self.el.dentro(u - cu, z - cz):
                return True
        return False

    def medidas(self):
        """(fracao vazada, menor alma entre dois furos vizinhos)."""
        vaz = self.el.area / self.area_celula
        alma = 1e9
        for bx, by in self.el.borda():
            u, z = self.u0 + bx, self.z0 + by
            for cu, cz in self.vizinhos(u, z, r=2):
                if abs(cu - self.u0) < 1e-9 and abs(cz - self.z0) < 1e-9:
                    continue
                alma = min(alma, self.el.dist(u - cu, z - cz))
        return vaz, alma


def largura_faixa(cmds=CURTO):
    """Largura perpendicular da faixa (as duas retas longas sao paralelas)."""
    p = contorno(cmds, n=2)
    # o trecho longo vai do fim da 1a curva ate a ponta oposta
    a, b = p[3], p[4]
    d = math.hypot(b[0]-a[0], b[1]-a[1])
    ux, uy = (b[0]-a[0])/d, (b[1]-a[1])/d
    c = p[7]                                   # ponto da outra reta longa
    return abs((c[0]-a[0])*(-uy) + (c[1]-a[1])*ux)


def monta(L, perimetro, zlo, zhi, k_u, k_z, giro=0.0, desloc=0.0):
    """Grade ALINHADA: colunas e fileiras, como o vazado antigo, so que o furo
    e o elemento da marca e ele entra na diagonal.

    Os elementos de colunas e fileiras vizinhas ficam lado a lado; os da
    diagonal ficam ponta com ponta, na direcao do proprio elemento — e isso que
    forma as linhas diagonais tracejadas e mantem a composicao linear.
    """
    el = Elemento(L, CURTO, giro)
    nu = max(4, int(round(perimetro / (k_u * L))))
    pu = perimetro / nu
    nz = max(2, int(round((zhi - zlo) / (k_z * L))))
    pz = (zhi - zlo) / nz
    tr = Trama(el, (pu, 0.0), (desloc * pu, pz), 0.0, zlo + pz / 2)
    vaz, alma = tr.medidas()
    info = dict(L=round(L, 1), esc=round(el.esc, 4), colunas=nu, fileiras=nz,
                pu=round(pu, 1), pz=round(pz, 1), desloc=desloc,
                largura=round(largura_faixa() * el.esc, 1),
                eixo=round(ANG_EIXO + giro, 1),
                area_el=round(el.area, 1), celula=round(tr.area_celula, 1),
                vazado=vaz, alma=alma)
    return tr, info
