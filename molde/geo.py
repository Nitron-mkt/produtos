# -*- coding: utf-8 -*-
"""
Kernel de geometria parametrica — sem dependencia externa.
Convencao: milimetro, Z para cima, origem no centro do fundo externo do corpo.

Todo contorno e um retangulo arredondado amostrado sempre com o MESMO numero de
pontos, o que permite:
  - deslocar o contorno por um offset d (a posicao do ponto e p + d*n);
  - costurar dois contornos diferentes por indice.

Normais sao analiticas por segmento de perfil (aresta viva entre segmentos),
que e o aspecto certo para leitura de peca injetada.
"""
import math, struct

SEG = 14   # pontos por canto de 90 graus
STR = 26   # pontos por trecho reto


def outline(hx, hy, rc, ox=0.0, oy=0.0):
    """Retangulo arredondado CCW: [(px,py,nx,ny)]."""
    cx = [hx - rc, -(hx - rc), -(hx - rc), hx - rc]
    cy = [hy - rc, hy - rc, -(hy - rc), -(hy - rc)]
    pts = []
    for c in range(4):
        a0 = c * math.pi / 2
        for i in range(SEG + 1):
            a = a0 + (i / SEG) * (math.pi / 2)
            nx, ny = math.cos(a), math.sin(a)
            pts.append((cx[c] + rc * nx + ox, cy[c] + rc * ny + oy, nx, ny))
        ae = a0 + math.pi / 2
        nx, ny = math.cos(ae), math.sin(ae)
        sx, sy = cx[c] + rc * nx + ox, cy[c] + rc * ny + oy
        c2 = (c + 1) % 4
        a2 = c2 * math.pi / 2
        ex = cx[c2] + rc * math.cos(a2) + ox
        ey = cy[c2] + rc * math.sin(a2) + oy
        for i in range(1, STR):
            t = i / STR
            pts.append((sx + (ex - sx) * t, sy + (ey - sy) * t, nx, ny))
    return pts


def zval(value, x, xc=0.0, half=17.0, feather=1.6, hole=0.0):
    """Amplitude do recurso num x qualquer — usada pelo mesh e pelo desenho."""
    t = (half - abs(x - xc)) / feather
    f = max(0.0, min(1.0, t))
    if hole > 0.0:
        u = (abs(x - xc) - hole) / feather
        f *= max(0.0, min(1.0, u))
    return value * f * f * (3 - 2 * f)


def zone(ol, value, edge, xc=0.0, half=17.0, feather=1.6, hole=0.0):
    """Amplitude por indice do contorno.

    edge(px,py) -> True na face onde o recurso existe;
    |px-xc| < half define a largura, com transicao suave de `feather` mm;
    `hole` abre uma janela central sem recurso.
    """
    out = []
    for (px, py, nx, ny) in ol:
        out.append(zval(value, px, xc, half, feather, hole) if edge(px, py) else 0.0)
    return out


def zsum(*zs):
    return [sum(v) for v in zip(*zs)]


class Mesh:
    def __init__(self, name):
        self.name = name
        self.V = []
        self.N = []
        self.F = []

    def add(self, x, y, z, nx, ny, nz):
        L = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
        self.V.append((x, y, z))
        self.N.append((nx / L, ny / L, nz / L))
        return len(self.V) - 1

    def tri(self, a, b, c):
        self.F.append((a, b, c))

    def quad(self, a, b, c, d):
        self.tri(a, b, c)
        self.tri(a, c, d)

    # ---- anel de indices sobre um contorno -------------------------------
    def ring(self, ol, d, z, nd=0.0, nz=1.0, amp=None):
        idx = []
        for i, (px, py, nx, ny) in enumerate(ol):
            dd = d + (amp[i] if amp else 0.0)
            idx.append(self.add(px + dd * nx, py + dd * ny, z,
                                nd * nx, nd * ny, nz))
        return idx

    def pts(self, ol, d, z, amp=None):
        return [(px + (d + (amp[i] if amp else 0.0)) * nx,
                 py + (d + (amp[i] if amp else 0.0)) * ny, z)
                for i, (px, py, nx, ny) in enumerate(ol)]

    # ---- varredura de perfil aberto --------------------------------------
    def sweep(self, ol, prof, amps=None):
        """prof: [(d,z)] percorrido em CCW no plano (d,z) -> normais para fora.
        amps: lista paralela a prof, cada item uma lista de amplitude por indice."""
        n = len(ol)
        for k in range(len(prof) - 1):
            d0, z0 = prof[k]
            d1, z1 = prof[k + 1]
            a0 = amps[k] if amps else None
            a1 = amps[k + 1] if amps else None
            if abs(z1 - z0) < 1e-9 and abs(d1 - d0) < 1e-9 and a0 is a1:
                continue
            A, B = [], []
            for i, (px, py, nx, ny) in enumerate(ol):
                dd0 = d0 + (a0[i] if a0 else 0.0)
                dd1 = d1 + (a1[i] if a1 else 0.0)
                dz, dd = z1 - z0, dd1 - dd0
                L = math.hypot(dz, dd)
                nd, nz = (dz / L, -dd / L) if L > 1e-9 else (1.0, 0.0)
                A.append(self.add(px + dd0 * nx, py + dd0 * ny, z0, nd * nx, nd * ny, nz))
                B.append(self.add(px + dd1 * nx, py + dd1 * ny, z1, nd * nx, nd * ny, nz))
            for i in range(n):
                j = (i + 1) % n
                self.quad(A[i], A[j], B[j], B[i])

    # ---- faces planas -----------------------------------------------------
    def stitch(self, inner, outer, up):
        n = len(inner)
        for i in range(n):
            j = (i + 1) % n
            if up:
                self.quad(inner[i], outer[i], outer[j], inner[j])
            else:
                self.quad(inner[i], inner[j], outer[j], outer[i])

    def flat(self, ol_in, d_in, ol_out, d_out, z, up, amp_in=None, amp_out=None):
        nz = 1.0 if up else -1.0
        A = self.ring(ol_in, d_in, z, 0.0, nz, amp_in)
        B = self.ring(ol_out, d_out, z, 0.0, nz, amp_out)
        self.stitch(A, B, up)

    def fan(self, ol, d, z, up, cx=0.0, cy=0.0, amp=None):
        nz = 1.0 if up else -1.0
        R = self.ring(ol, d, z, 0.0, nz, amp)
        c = self.add(cx, cy, z, 0.0, 0.0, nz)
        n = len(R)
        for i in range(n):
            j = (i + 1) % n
            if up:
                self.tri(c, R[i], R[j])
            else:
                self.tri(c, R[j], R[i])

    # ---- prismas convexos ao longo de X ----------------------------------
    def prismX(self, poly, x0, x1):
        """poly: [(y,z)] CCW e convexo."""
        n = len(poly)
        for k in range(n):
            (y0, z0) = poly[k]
            (y1, z1) = poly[(k + 1) % n]
            dy, dz = y1 - y0, z1 - z0
            L = math.hypot(dy, dz) or 1.0
            ny, nz = dz / L, -dy / L
            a = self.add(x0, y0, z0, 0, ny, nz)
            b = self.add(x0, y1, z1, 0, ny, nz)
            c = self.add(x1, y1, z1, 0, ny, nz)
            d = self.add(x1, y0, z0, 0, ny, nz)
            self.quad(a, b, c, d)
        for (x, s) in ((x1, 1.0), (x0, -1.0)):
            idx = [self.add(x, y, z, s, 0, 0) for (y, z) in poly]
            for k in range(1, n - 1):
                if s > 0:
                    self.tri(idx[0], idx[k], idx[k + 1])
                else:
                    self.tri(idx[0], idx[k + 1], idx[k])

    def box(self, x0, x1, y0, y1, z0, z1):
        self.prismX([(y0, z0), (y1, z0), (y1, z1), (y0, z1)], x0, x1)

    def cylX(self, yc, zc, r, x0, x1, seg=20):
        poly = [(yc + r * math.cos(2 * math.pi * i / seg),
                 zc + r * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
        self.prismX(poly, x0, x1)

    # ---- metricas ---------------------------------------------------------
    def volume_cm3(self):
        v = 0.0
        for (a, b, c) in self.F:
            p, q, r = self.V[a], self.V[b], self.V[c]
            v += (p[0] * (q[1] * r[2] - q[2] * r[1])
                  - p[1] * (q[0] * r[2] - q[2] * r[0])
                  + p[2] * (q[0] * r[1] - q[1] * r[0])) / 6.0
        return v / 1000.0

    def bbox(self):
        xs = [v[0] for v in self.V]; ys = [v[1] for v in self.V]; zs = [v[2] for v in self.V]
        return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

    # ---- exportacao -------------------------------------------------------
    def stl(self, path):
        with open(path, 'wb') as f:
            f.write(b'\0' * 80)
            f.write(struct.pack('<I', len(self.F)))
            for (a, b, c) in self.F:
                p, q, r = self.V[a], self.V[b], self.V[c]
                ux, uy, uz = q[0] - p[0], q[1] - p[1], q[2] - p[2]
                vx, vy, vz = r[0] - p[0], r[1] - p[1], r[2] - p[2]
                nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
                L = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
                f.write(struct.pack('<3f', nx / L, ny / L, nz / L))
                for t in (p, q, r):
                    f.write(struct.pack('<3f', *t))
                f.write(b'\0\0')

    def buffers(self):
        pos = struct.pack('<%df' % (3 * len(self.V)), *[c for v in self.V for c in v])
        nrm = struct.pack('<%df' % (3 * len(self.N)), *[c for v in self.N for c in v])
        assert len(self.V) < 65536, '%s: %d vertices' % (self.name, len(self.V))
        idx = struct.pack('<%dH' % (3 * len(self.F)), *[i for f in self.F for i in f])
        return pos, nrm, idx
