"""O grafismo da Nitron como furo de parede — medido, nao estimado.

MEDIDO NO PNG DA MARCA (grafismo/logo-nitron.png)
-------------------------------------------------
Elemento ("grao"), no referencial ponta-a-ponta:

  comprimento L = 85,6 px, largura W = 39,8 px  ->  L/W = 2,15
  preenchimento da caixa = 0,578
  eixo maior a 75,8 graus da horizontal
  perfil de meia-largura     hw(t) = (W/2) * (1 - (2t-1)^2)^1,3
  linha de centro em S       vc(t) = -0,152 * (W/2) * sin(2*pi*t)

O grao NAO e uma lente simetrica: ele tem simetria de PONTO (gira 180 graus em
torno do centro e cai em si mesmo), nao simetria de espelho. E o S da linha de
centro que da o ar de trama ao logo — e foi exatamente o que a rev.10 perdeu ao
tratar o grao como lente.

Rede, medida a partir dos 28 centros do logo (linhas em y = -91,5 e y = -201
dao o periodo horizontal; a linha intermediaria em y = -148,7 da o desvio):

  a1 = ( 57,2 ;   0,0)   ->  periodo horizontal, 0,668 L
  a2 = (-12,6 ; -57,2)   ->  descendo uma fileira, anda 12,6 px para a ESQUERDA

  area da celula = 3.272 px2 contra 1.966 px2 do grao  ->  60% de cobertura

O sinal de a2 e o detalhe que decide tudo: com ele invertido, a2 fica paralela
ao eixo do grao (-76 graus) e os graos se emendam ponta com ponta virando
fitas continuas. Com o sinal certo, a2 cruza o eixo a 27 graus e nasce a trama.
A reconstrucao foi conferida contra a marca pixel a pixel.

DEITADO NA PECA
---------------
Tudo gira +90 graus, que e o que troca o vazado vertical pelo horizontal sem
perder a marca:

  eixo do grao      +14,2 graus (quase horizontal, subindo para a direita)
  periodo na volta  0,668 L
  periodo na altura 0,668 L
  descida por coluna 0,147 L

A rede entra com a MESMA forma do logo, so afastada por um fator de escala ate
o vazado cair de 60% para o alvo da peca — o desenho e o mesmo, o que muda e o
espacamento, que na peca tem de deixar alma entre os furos.
"""
import math

# --- constantes medidas ---------------------------------------------------
RAZAO = 2.15          # L / W
EXPO = 1.3            # expoente do perfil de meia-largura
ESSE = 0.152          # amplitude do S, em meias-larguras
ANG = 14.2            # eixo do grao, deitado
PU = 0.668            # periodo na volta, em comprimentos de grao
DZ = -0.147           # descida por coluna
PZ = 0.668            # periodo na altura
COBERTURA_LOGO = 0.601


class Grao:
    """O traco do logo. Origem no centro, x ao longo do eixo."""

    def __init__(self, L, W, rt):
        self.L, self.hw, self.rt = L, W / 2, rt
        # onde a meia-largura vale rt: dali para a ponta e calota
        lo, hi = 0.0, 0.5
        for _ in range(40):
            t = (lo + hi) / 2
            if self._hw(t) < rt:
                lo = t
            else:
                hi = t
        self.tc = hi
        self.xc = (self.tc - 0.5) * L          # x da calota (negativo)
        self.yc = self._vc(self.tc)

    def _hw(self, t):
        s = 2 * t - 1
        return self.hw * (max(0.0, 1 - s * s)) ** EXPO

    def _vc(self, t):
        return -ESSE * self.hw * math.sin(2 * math.pi * t)

    def dentro(self, x, y):
        t = x / self.L + 0.5
        if self.tc <= t <= 1 - self.tc:
            return abs(y - self._vc(t)) <= self._hw(t)
        # calotas das duas pontas (simetria de ponto)
        if x < 0:
            return math.hypot(x - self.xc, y - self.yc) <= self.rt
        return math.hypot(x + self.xc, y + self.yc) <= self.rt

    def dist_ext(self, x, y):
        """Aproximacao da distancia ate o grao (>=0 fora). Usada so na alma."""
        t = min(max(x / self.L + 0.5, 0.0), 1.0)
        if self.tc <= t <= 1 - self.tc:
            return abs(y - self._vc(t)) - self._hw(t)
        if x < 0:
            return math.hypot(x - self.xc, y - self.yc) - self.rt
        return math.hypot(x + self.xc, y + self.yc) - self.rt


class Malha:
    """Rede oblíqua do logo, deitada e periodica na volta.

    Centros em (i*pu, z0 + j*pz + i*dz). Fechar a volta so exige que a subida
    acumulada em nu colunas seja um numero inteiro de pz — por isso dz e
    arredondado para pz*k/nu.
    """

    def __init__(self, grao, pu, pz, dz, z0, ang=ANG):
        self.g, self.pu, self.pz, self.dz, self.z0 = grao, pu, pz, dz, z0
        self.co = math.cos(math.radians(ang))
        self.si = math.sin(math.radians(ang))

    def vizinhos(self, u, z):
        ci = u / self.pu
        for di in (-2, -1, 0, 1, 2):
            i = math.floor(ci + 0.5) + di
            uc = i * self.pu
            zb = self.z0 + i * self.dz
            j = math.floor((z - zb) / self.pz + 0.5)
            for dj in (-1, 0, 1):
                yield uc, zb + (j + dj) * self.pz

    def _local(self, u, z, uc, zc):
        du, dv = u - uc, z - zc
        return du * self.co + dv * self.si, -du * self.si + dv * self.co

    def dentro(self, u, z):
        for uc, zc in self.vizinhos(u, z):
            if self.g.dentro(*self._local(u, z, uc, zc)):
                return True
        return False

    # -- verificacao -------------------------------------------------------
    def medidas(self, n=140, nb=240):
        """(fracao vazada, menor alma entre dois furos vizinhos)."""
        dentro = 0
        for i in range(n):
            u = (i + 0.5) * self.pu / n
            for j in range(n):
                z = self.z0 + (j + 0.5) * self.pz / n
                if self.dentro(u, z):
                    dentro += 1
        vazado = dentro / (n * n)
        alma = 1e9
        g = self.g
        for k in range(nb):
            th = 2 * math.pi * k / nb
            dx, dy = math.cos(th), math.sin(th)
            lo, hi = 0.0, g.L
            for _ in range(28):
                mid = (lo + hi) / 2
                if g.dentro(mid * dx, mid * dy):
                    lo = mid
                else:
                    hi = mid
            x, y = lo * dx, lo * dy
            u = x * self.co - y * self.si
            z = self.z0 + x * self.si + y * self.co
            for uc, zc in self.vizinhos(u, z):
                if abs(uc) < 1e-9 and abs(zc - self.z0) < 1e-9:
                    continue
                alma = min(alma, g.dist_ext(*self._local(u, z, uc, zc)))
        return vazado, alma


def monta(L, perimetro, zlo, zhi, rt, folga=1.253):
    """Instancia a rede da marca com um afastamento 'folga' sobre a do logo."""
    W = L / RAZAO
    # a altura manda: nz inteiro para nao sobrar meia fileira na borda.
    nz = max(2, int(round((zhi - zlo) / (PZ * L * folga))))
    pz = (zhi - zlo) / nz
    # a volta acompanha, mantendo a celula na proporcao do logo (pu/pz = PU/PZ)
    nu = max(6, int(round(perimetro / (pz * PU / PZ))))
    pu = perimetro / nu
    k = int(round(nu * DZ / PZ))
    dz = pz * k / nu
    m = Malha(Grao(L, W, rt), pu, pz, dz, zlo + pz / 2)
    return m, dict(nu=nu, nz=nz, pu=round(pu, 1), pz=round(pz, 1),
                   dz=round(dz, 2), k=k, L=L, W=round(W, 1))
