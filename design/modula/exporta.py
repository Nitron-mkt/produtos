"""Gera STL, JSON (visualizador web) e as vistas renderizadas da familia MODULA."""
import base64, json, math, os, sys
import numpy as np
import modelo
from modelo import construir, ficha, TAN, RHO_PP
import render as R

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(SAIDA, exist_ok=True)

COR_CORPO = {"P": (243, 241, 236), "M": (206, 80, 38), "G": (66, 71, 78)}


def paleta(base, destaque=False):
    c = dict.fromkeys(["faixa", "ripa", "aro", "fundo", "pe", "crista", "saia"], base)
    c["pe"] = R.PALETA["destaque"] if destaque else base
    c["saia"] = R.PALETA["destaque"] if destaque else base
    c["crista"] = R.PALETA["critico"] if destaque else tuple(
        min(255, int(v * 1.06)) for v in base)
    c["fundo"] = tuple(int(v * 0.95) for v in base)
    c["aro"] = tuple(min(255, int(v * 1.06)) for v in base)
    return c


def malha_json(m, s):
    """Posicoes (int16, 0,25 mm) + normais suaves (int8) -> base64.
    Separa tres grupos: corpo, pe e crista (o apoio elevado do aro)."""
    esc = 4.0
    ns = m.normais_suaves(42)
    grupos = {"corpo": [], "pe": [], "crista": []}
    for k, (a, b, c, tag) in enumerate(m.tris):
        g = "pe" if tag in ("pe", "saia") else ("crista" if tag == "crista" else "corpo")
        grupos[g].append((a, b, c, ns[k]))
    saida = {}
    for g, tris in grupos.items():
        pos, nor = [], []
        for a, b, c, n3 in tris:
            for v, nv in zip((a, b, c), n3):
                pos += [int(round(v[0] * esc)), int(round(v[2] * esc)),
                        int(round(-v[1] * esc))]
                nor += [max(-127, min(127, int(round(nv[0] * 127)))),
                        max(-127, min(127, int(round(nv[2] * 127)))),
                        max(-127, min(127, int(round(-nv[1] * 127))))]
        saida[g] = dict(
            p=base64.b64encode(np.array(pos, dtype="<i2").tobytes()).decode(),
            n=base64.b64encode(np.array(nor, dtype="i1").tobytes()).decode())
    return dict(
        X=s["X"], Y=s["Y"], H=s["H"], hf=s["hf"], e=s["e"], R=s["R"],
        passo=s["passo_ninho"], massa=round(s["massa_g"]),
        total=round(s["litros_total"], 1), boca=round(s["litros_boca"], 1),
        aba=s["aba"], pe=round(s["sal_pe"], 1),
        grao=s["graf_L"], vazado=round(s["graf_vazado"], 3),
        alma=round(s["graf_alma"], 1),
        cesta=s["hc"], perna=s["perna"], pilha=s["passo_pilha"],
        esc=esc, malha=saida)


def main():
    fichas, dados = {}, {}
    for k in ("P", "M", "G"):
        sol, s = ficha(k)
        fichas[k] = (sol, s)
        print(f"  {k}: {len(sol.tris)} triangulos, {s['massa_g']:.0f} g")
    modelo.AMOSTRA = [2.6, 14]                      # navegador: o pattern precisa de 2,6 mm
    for k in ("P", "M", "G"):
        leve, sl = ficha(k)
        dados[k] = malha_json(leve, sl)
    modelo.AMOSTRA = [1.3, 20]
    with open(os.path.join(SAIDA, "modula.json"), "w") as f:
        json.dump(dados, f, separators=(",", ":"))

    ns = {k: fichas[k][0].normais_suaves(42) for k in ("P", "M", "G")}

    def grupo(k, offset=(0, 0, 0), giro=False, destaque=False, cor=None):
        sol, sp = fichas[k]
        return (sol.triangulos(offset=offset, giro180=giro),
                paleta(cor or COR_CORPO[k], destaque), ns[k])

    # ---- 01 a familia, nas tres cores de uso ------------------------------
    g, x = [], 0.0
    for k in ("P", "M", "G"):
        x += fichas[k][1]["X"] / 2 + 50
        g.append(grupo(k, offset=(x, 0, 0)))
        x += fichas[k][1]["X"] / 2
    R.cena(g, 1600, 640, az=34, el=21).save(os.path.join(SAIDA, "01-familia.png"))

    sol, s = fichas["M"]

    # ---- 02 a peca --------------------------------------------------------
    R.cena([grupo("M")], 1200, 950, az=42, el=23) \
        .save(os.path.join(SAIDA, "02-M-iso.png"))

    # ---- 03 ninho ---------------------------------------------------------
    g = [grupo("M", offset=(0, 0, i * s["passo_ninho"]), giro=bool(i % 2))
         for i in range(10)]
    R.cena(g, 1100, 950, az=44, el=17).save(os.path.join(SAIDA, "03-ninho.png"))

    # ---- 04 pilha ---------------------------------------------------------
    g = [grupo("M", offset=(0, 0, i * s["passo_pilha"])) for i in range(3)]
    R.cena(g, 900, 1180, az=44, el=13).save(os.path.join(SAIDA, "04-pilha.png"))

    # ---- 05 o encaixe em destaque ----------------------------------------
    g = [grupo("M", destaque=True),
         grupo("M", offset=(0, 0, s["passo_pilha"] + 70), destaque=True)]
    R.cena(g, 1150, 1000, az=58, el=14).save(os.path.join(SAIDA, "05-encaixe.png"))

    # ---- 06 ninho x pilha -------------------------------------------------
    g = [grupo("M", offset=(-340, 0, i * s["passo_ninho"]), giro=bool(i % 2))
         for i in range(10)]
    g += [grupo("M", offset=(340, 0, i * s["passo_pilha"]), cor=COR_CORPO["G"]) for i in range(3)]
    R.cena(g, 1450, 900, az=40, el=15).save(os.path.join(SAIDA, "06-ninho-x-pilha.png"))

    # ---- 07 a peca de casa: torre de tres P em branco ---------------------
    sP = fichas["P"][1]
    g = [grupo("P", offset=(0, 0, i * sP["passo_pilha"])) for i in range(3)]
    R.cena(g, 900, 1100, az=48, el=13, fundo=(212, 207, 199)) \
        .save(os.path.join(SAIDA, "07-torre-casa.png"))

    # ---- 08 em cima (rev.25): dois P sobre um M, tres P sobre um G ----------
    def sobre(kg, cx=0.0):
        sg = fichas[kg][1]
        en = sg["encaixe"]
        return [grupo(kg, offset=(cx, 0, 0))] + [grupo(en["filho"], offset=(cx + c, 0, en["z_filho"]))
                                                 for c in en["centros"]]
    g = sobre("M", cx=-320) + sobre("G", cx=330)
    R.cena(g, 1700, 950, az=36, el=20).save(os.path.join(SAIDA, "08-em-cima.png"))
    R.cena(sobre("G"), 1500, 900, az=90, el=6).save(os.path.join(SAIDA, "09-em-cima-frente.png"))

    # ---- 10 fileiras acopladas: tres P e tres M, passo = X ------------------
    g = [grupo("P", offset=(i * sP["X"], 0, 0)) for i in range(3)]
    g += [grupo("M", offset=(i * s["X"] - 100, -s["Y"] - 140, 0)) for i in range(3)]
    R.cena(g, 1600, 900, az=30, el=22).save(os.path.join(SAIDA, "10-fileiras.png"))

    print("  imagens em", SAIDA)


def escreve_stl(malha, caminho, nome="MODULA"):
    """STL binario, em milimetros, 1:1. Normal por face, orientada para fora."""
    import struct
    tris = [t for t in malha.tris]
    with open(caminho, "wb") as f:
        cab = f"{nome} - Nitron - mm".encode()[:79].ljust(80, b" ")
        f.write(cab)
        f.write(struct.pack("<I", len(tris)))
        for a, b, c, _ in tris:
            ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
            vx, vy, vz = c[0]-a[0], c[1]-a[1], c[2]-a[2]
            nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
            n = math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
            f.write(struct.pack("<12fH", nx/n, ny/n, nz/n,
                                a[0], a[1], a[2], b[0], b[1], b[2],
                                c[0], c[1], c[2], 0))
    return len(tris)


def confere(malha):
    """(arestas totais, arestas abertas, caixa) — diagnostico do solido."""
    import collections
    q = lambda p: (round(p[0], 3), round(p[1], 3), round(p[2], 3))
    cnt = collections.Counter()
    xs = []; ys = []; zs = []
    for a, b, c, _ in malha.tris:
        A, B, C = q(a), q(b), q(c)
        for p in (A, B, C):
            xs.append(p[0]); ys.append(p[1]); zs.append(p[2])
        if A == B or B == C or A == C:
            continue
        for e in ((A, B), (B, C), (C, A)):
            cnt[tuple(sorted(e))] += 1
    abertas = sum(1 for v in cnt.values() if v % 2)
    caixa = (max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs))
    return len(cnt), abertas, caixa


def stl():
    import time
    print("STL (malha de producao, AMOSTRA =", modelo.AMOSTRA, ")")
    for k in ("P", "M", "G"):
        t0 = time.time()
        sol, s = ficha(k)
        n = escreve_stl(sol, os.path.join(SAIDA, f"modula-{k}.stl"), s["nome"])
        tot, ab, cx = confere(sol)
        tam = os.path.getsize(os.path.join(SAIDA, f"modula-{k}.stl")) / 1e6
        print(f"  {s['nome']}: {n:6d} tri  {tam:5.1f} MB  caixa "
              f"{cx[0]:.1f} x {cx[1]:.1f} x {cx[2]:.1f} mm  "
              f"arestas abertas {ab}/{tot} ({ab/tot:.2%})  "
              f"{s['massa_g']:.0f} g  {s['litros_total']:.1f} L  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    import sys
    if "stl" in sys.argv:
        stl()
    elif "png" in sys.argv:
        main()
    else:
        main()
        stl()
