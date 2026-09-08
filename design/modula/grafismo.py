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

    def extensao_z(self):
        """Altura que o elemento ocupa, ja girado. E ela que decide onde a
        primeira e a ultima fileira podem ficar sem serem cortadas ao meio."""
        return max(q[1] for q in self.p) - min(q[1] for q in self.p)


class Trama:
    """O grafismo: o elemento repetido nos dois passos da marca."""

    def __init__(self, el, t1, t2, u0=0.0, z0=0.0, jmin=None, jmax=None):
        self.el, self.t1, self.t2 = el, t1, t2
        self.u0, self.z0 = u0, z0
        # limite de fileiras: fora dele nao nasce elemento. E o que impede o
        # grafismo de ser cortado ao meio pelas faixas cheias do topo e do pe.
        self.jmin, self.jmax = jmin, jmax
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
                if self.jmin is not None and j < self.jmin: continue
                if self.jmax is not None and j > self.jmax: continue
                yield (self.u0 + i*self.t1[0] + j*self.t2[0],
                       self.z0 + i*self.t1[1] + j*self.t2[1])

    def dentro(self, u, z):
        for cu, cz in self.vizinhos(u, z):
            if self.el.dentro(u - cu, z - cz):
                return True
        return False

    def medidas(self):
        """(fracao vazada, menor alma entre dois furos vizinhos).

        Mede o miolo da trama: os limites de fileira sao suspensos aqui, senao
        a fileira de baixo nao teria vizinha e a alma sairia otimista.
        """
        lim = (self.jmin, self.jmax)
        self.jmin = self.jmax = None
        vaz = self.el.area / self.area_celula
        alma = 1e9
        for bx, by in self.el.borda():
            u, z = self.u0 + bx, self.z0 + by
            for cu, cz in self.vizinhos(u, z, r=2):
                if abs(cu - self.u0) < 1e-9 and abs(cz - self.z0) < 1e-9:
                    continue
                alma = min(alma, self.el.dist(u - cu, z - cz))
        self.jmin, self.jmax = lim
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
    # As fileiras andam entre os CENTROS extremos, recuados meia altura de
    # elemento das duas faixas cheias: assim nenhuma fileira sai cortada.
    Ez = el.extensao_z()
    util = max(1.0, (zhi - zlo) - Ez)
    nz = max(1, int(round(util / (k_z * L))))
    pz = util / nz
    tr = Trama(el, (pu, 0.0), (desloc * pu, pz), 0.0, zlo + Ez / 2,
               jmin=0, jmax=nz)
    vaz, alma = tr.medidas()
    info = dict(L=round(L, 1), esc=round(el.esc, 4), colunas=nu, fileiras=nz + 1,
                pu=round(pu, 1), pz=round(pz, 1), desloc=desloc,
                largura=round(largura_faixa() * el.esc, 1),
                alt_elem=round(Ez, 1),
                eixo=round(ANG_EIXO + giro, 1),
                area_el=round(el.area, 1), celula=round(tr.area_celula, 1),
                vazado=vaz, alma=alma)
    return tr, info


# =============================================================================
# O PATTERN OFICIAL (rev.19) — ladrilho do arquivo da marca
# =============================================================================
# `grafismo/pattern-nitron.ai` traz o grafismo como PDF tiling pattern:
# celula de 230 x 280 pt com 10 elementos, em quatro formas. A celula e uma
# rede retangular CENTRADA: o motivo de 5 elementos se repete em
# (115, 140) e (230, 0). Coordenadas em pt, y para cima, como no arquivo.
#
#   A  elemento curto  (99,7 pt de altura, faixa de 38,9 pt)   x2 por motivo
#   B  elemento longo  (184,9 pt)                               x1
#   C  elemento medio  (110 pt)  e  D = C girado 180 graus      x1 + x1
#
# Vazado 58,2 %, alma minima 12,18 pt (entre dois B). A escala da peca sai
# da alma: s = alma_minima_mm / 12,18.
TILE_FORMAS = {
    "A": [("M", 0, 0), ("L", 9.442, 29.336),
          ("C", 12.584, 39.099, 10.704, 49.784, 4.418, 57.889),
          ("L", -27.99, 99.736), ("L", -37.374, 70.161),
          ("C", -40.463, 60.428, -38.57, 49.8, -32.313, 41.731)],
    "B": [("M", 0, 0), ("L", -89.855, 116.26), ("L", -98.994, 87.865),
          ("C", -103.42, 74.114, -100.786, 59.066, -91.952, 47.636),
          ("L", -2.098, -68.627), ("L", 7.042, -40.229),
          ("C", 11.468, -26.478, 8.834, -11.43, 0, 0)],
    "C": [("M", 0, 0), ("L", 9.442, 29.336),
          ("C", 12.584, 39.099, 10.704, 49.784, 4.418, 57.889),
          ("L", -36.054, 110.066), ("L", -45.439, 80.491),
          ("C", -48.527, 70.758, -46.635, 60.13, -40.377, 52.061)],
    "D": [("M", 0, 0), ("L", -9.443, -29.338),
          ("C", -12.585, -39.101, -10.705, -49.786, -4.419, -57.89),
          ("L", 36.035, -110.047), ("L", 45.422, -80.457),
          ("C", 48.51, -70.724, 46.616, -60.096, 40.358, -52.028)],
}
TILE_MOTIVO = [("A", 4.081, 55.007), ("A", 23.852, 125.257), ("B", 161.008, 116.204),
               ("D", 164.24, 24.383), ("C", 180.761, 115.467)]
TILE_A1 = (115.0, 140.0)
TILE_A2 = (230.0, 0.0)
TILE_ALMA_PT = 12.18
TILE_VAZADO = 0.582
TILE_LARG_A_PT = 38.9          # faixa do elemento curto (entre as retas longas)


def _poli(cmds, n=10):
    """Achata o path em poligono, no proprio referencial (y para cima)."""
    p, cur = [], None
    for c in cmds:
        if c[0] in "ML":
            cur = (c[1], c[2]); p.append(cur)
        else:
            p1, p2, p3 = (c[1], c[2]), (c[3], c[4]), (c[5], c[6])
            p0 = cur
            for k in range(1, n + 1):
                u = k / n; w = 1 - u
                p.append((w**3*p0[0] + 3*w*w*u*p1[0] + 3*w*u*u*p2[0] + u**3*p3[0],
                          w**3*p0[1] + 3*w*w*u*p1[1] + 3*w*u*u*p2[1] + u**3*p3[1]))
            cur = p3
    return p


def _dentro_poli(p, x, y):
    n = len(p); d = False; j = n - 1
    for i in range(n):
        if (p[i][1] > y) != (p[j][1] > y) and \
           x < (p[j][0]-p[i][0]) * (y-p[i][1]) / (p[j][1]-p[i][1]) + p[i][0]:
            d = not d
        j = i
    return d


def _area_faixa_z(p, zlo, zhi):
    """Fracao da area do poligono que fica entre zlo e zhi (clip horizontal)."""
    def clip(poly, lim, acima):
        out = []
        for i in range(len(poly)):
            a, b = poly[i - 1], poly[i]
            ia = (a[1] >= lim) if acima else (a[1] <= lim)
            ib = (b[1] >= lim) if acima else (b[1] <= lim)
            if ia and ib:
                out.append(b)
            elif ia != ib:
                t = (lim - a[1]) / (b[1] - a[1])
                q = (a[0] + t * (b[0] - a[0]), lim)
                out.append(q)
                if ib:
                    out.append(b)
        return out
    tot = _area(p)
    c = clip(clip(p, zlo, True), zhi, False)
    return (_area(c) / tot) if len(c) >= 3 and tot > 0 else 0.0


class Padrao:
    """O ladrilho da marca em (u, z), na escala 's' (mm por pt).

    u0 e z0 posicionam a origem da celula. 'espelho' inverte u (a inclinacao
    dos elementos troca de lado). 'minimo' e a fracao da area de um elemento
    que tem de caber entre zlo e zhi para ele existir — evita o caco cortado
    pelas faixas cheias do topo e do pe.
    """

    def __init__(self, s, u0, z0, zlo, zhi, espelho=False, minimo=0.35):
        self.s, self.u0, self.z0 = s, u0, z0
        self.esp = -1.0 if espelho else 1.0
        self.a1 = (TILE_A1[0] * s, TILE_A1[1] * s)
        self.a2 = (TILE_A2[0] * s, 0.0)
        det = self.a1[0]*self.a2[1] - self.a1[1]*self.a2[0]
        self.inv = ((self.a2[1]/det, -self.a2[0]/det), (-self.a1[1]/det, self.a1[0]/det))
        self.elem = []                        # (poligono em mm, bbox, tx, ty)
        for nome, tx, ty in TILE_MOTIVO:
            p = [(x * s, y * s) for x, y in _poli(TILE_FORMAS[nome])]
            xs = [q[0] for q in p]; ys = [q[1] for q in p]
            self.elem.append((p, (min(xs), max(xs), min(ys), max(ys)), tx * s, ty * s))
        # quais fileiras (indice i da rede ao longo de a1) existem
        self.zlo, self.zhi, self.minimo = zlo, zhi, minimo
        self.keep = {}
        imin = int(math.floor((zlo - z0 - 300 * s) / self.a1[1])) - 1
        imax = int(math.ceil((zhi - z0 + 300 * s) / self.a1[1])) + 1
        for i in range(imin, imax + 1):
            for k, (p, bb, tx, ty) in enumerate(self.elem):
                oz = z0 + i * self.a1[1] + ty
                fr = _area_faixa_z([(x, y + oz) for x, y in p], zlo, zhi)
                self.keep[(i, k)] = fr >= minimo
        self.fileiras = sum(1 for (i, k), v in self.keep.items() if v and k == 0)

    def dentro(self, u, z):
        u = self.esp * u
        du, dz = u - self.u0, z - self.z0
        fi = self.inv[0][0]*du + self.inv[0][1]*dz
        fj = self.inv[1][0]*du + self.inv[1][1]*dz
        i0, j0 = math.floor(fi), math.floor(fj)
        for i in (i0 - 1, i0, i0 + 1):
            for j in (j0 - 1, j0, j0 + 1):
                ou = self.u0 + i*self.a1[0] + j*self.a2[0]
                oz = self.z0 + i*self.a1[1]
                for k, (p, bb, tx, ty) in enumerate(self.elem):
                    if not self.keep.get((i, k), False):
                        continue
                    x, y = u - ou - tx, z - oz - ty
                    if x < bb[0] or x > bb[1] or y < bb[2] or y > bb[3]:
                        continue
                    if _dentro_poli(p, x, y):
                        return True
        return False


def monta_padrao(perimetro, zlo, zhi, alma_min, espelho=False, minimo=0.45):
    """Escolhe a escala pela alma minima e fecha a volta: o periodo em u
    (230 pt x s) tem de dividir o perimetro."""
    s0 = alma_min / TILE_ALMA_PT
    n = max(1, int(round(perimetro / (TILE_A2[0] * s0))))
    s = perimetro / (TILE_A2[0] * n)
    # centra o padrao na faixa util: a celula fica com o meio em (zlo+zhi)/2
    z0 = 0.5 * (zlo + zhi) - 0.5 * TILE_A1[1] * s
    pad = Padrao(s, 0.0, z0, zlo, zhi, espelho, minimo)
    info = dict(esc=round(s, 4), alma=round(TILE_ALMA_PT * s, 2), vazado=TILE_VAZADO,
                largura=round(TILE_LARG_A_PT * s, 1), colunas=n,
                fileiras=pad.fileiras, pu=round(TILE_A2[0] * s, 1), pz=round(TILE_A1[1] * s, 1),
                alt_elem=round(99.7 * s, 1), alt_longo=round(184.9 * s, 1),
                eixo=round(math.degrees(math.atan2(116.26, -89.855)), 1),
                area_el=0, celula=round(abs(TILE_A1[1] * TILE_A2[0]) * s * s, 1))
    return pad, info
