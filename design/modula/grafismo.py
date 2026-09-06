"""O grafismo da Nitron como furo de parede.

O traco do logo foi medido no PNG da marca: lente de duas arestas curvas, razao
comprimento/largura 2,22, preenchimento 0,60 da caixa (retangulo seria 1,00,
elipse 0,785), eixo maior a 63 graus da horizontal.

Aqui ele entra GIRADO 90 graus — o mesmo grao, deitado — porque e isso que
transforma o vazado vertical de hoje em vazado horizontal sem perder a marca.
"""
import math

RAZAO = 4.07          # o traco longo do logo (o curto e 2,22 — mesma familia)
ANG = 22.0            # o angulo do logo (63 graus) deitado, arredondado
PU = 0.745            # periodo na volta, em comprimentos de grao
PZ = 0.520            # periodo na altura


def sdf_grao(u, v, a, b, rt):
    """Distancia com sinal ate o grao: intersecao de dois discos, pontas
    arredondadas em rt (max suave). Negativo = dentro."""
    R = (a * a + b * b) / (2 * b)
    c = R - b
    d1 = math.hypot(u, v + c) - R
    d2 = math.hypot(u, v - c) - R
    h = max(rt - abs(d1 - d2), 0.0) / rt
    return max(d1, d2) + h * h * rt * 0.25


class Grafismo:
    """Malha alternada de graos, periodica em u (fecha a volta sem emenda)."""

    def __init__(self, a, b, rt, pu, pz, z_ref, ang=ANG, desloc=0.5):
        self.a, self.b, self.rt = a, b, rt
        self.pu, self.pz, self.z_ref = pu, pz, z_ref
        self.desloc = desloc          # deslocamento de uma fileira para a outra
        self.co = math.cos(math.radians(ang))
        self.si = math.sin(math.radians(ang))

    def centros(self, u, z):
        """Os 9 graos vizinhos de (u, z)."""
        jz = math.floor((z - self.z_ref) / self.pz + 0.5)
        for dj in (-1, 0, 1):
            j = jz + dj
            zc = self.z_ref + j * self.pz
            off = (j * self.desloc * self.pu) % self.pu
            ju = math.floor((u - off) / self.pu + 0.5)
            for di in (-1, 0, 1):
                yield off + (ju + di) * self.pu, zc

    def dist(self, u, z):
        d = 1e9
        for uc, zc in self.centros(u, z):
            du, dv = u - uc, z - zc
            x = du * self.co + dv * self.si
            y = -du * self.si + dv * self.co
            d = min(d, sdf_grao(x, y, self.a, self.b, self.rt))
        return d

    def dentro(self, u, z):
        return self.dist(u, z) < 0.0

    # -- verificacao ------------------------------------------------------
    def medidas(self, n=110, nb=200):
        """(fracao vazada, menor alma entre dois furos vizinhos)."""
        area = 0.0
        for i in range(n):
            u = (i + 0.5) * self.pu / n
            for j in range(n):
                z = self.z_ref + (j + 0.5) * 2 * self.pz / n
                if self.dentro(u, z):
                    area += 1
        vazado = area / (n * n)
        # contorno do grao central contra os vizinhos
        alma = 1e9
        for k in range(nb):
            th = 2 * math.pi * k / nb
            lo, hi = 0.0, self.a * 1.5
            dx, dy = math.cos(th), math.sin(th)
            for _ in range(26):
                mid = (lo + hi) / 2
                if sdf_grao(mid * dx, mid * dy, self.a, self.b, self.rt) < 0:
                    lo = mid
                else:
                    hi = mid
            x, y = lo * dx, lo * dy
            u = self.z_ref * 0 + x * self.co - y * self.si
            z = self.z_ref + x * self.si + y * self.co
            for uc, zc in self.centros(u, z):
                if abs(uc) < 1e-6 and abs(zc - self.z_ref) < 1e-6:
                    continue
                du, dv = u - uc, z - zc
                xx = du * self.co + dv * self.si
                yy = -du * self.si + dv * self.co
                alma = min(alma, sdf_grao(xx, yy, self.a, self.b, self.rt))
        return vazado, alma
