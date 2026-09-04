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
    c = dict.fromkeys(["faixa", "ripa", "aro", "fundo", "pe", "crista"], base)
    c["pe"] = R.PALETA["destaque"] if destaque else base
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
        g = tag if tag in ("pe", "crista") else "corpo"
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
        aba=s["aba"], pe=round(s["sal_pe"], 1), ripa=s["ripa"], vao=s["vao"],
        esc=esc, malha=saida)


def main():
    fichas, dados = {}, {}
    for k in ("P", "M", "G"):
        sol, s = ficha(k)
        fichas[k] = (sol, s)
        print(f"  {k}: {len(sol.tris)} triangulos, {s['massa_g']:.0f} g")
    modelo.AMOSTRA = [5.8, 7]                       # malha leve para o navegador
    for k in ("P", "M", "G"):
        leve, sl = ficha(k)
        dados[k] = malha_json(leve, sl)
    modelo.AMOSTRA = [2.6, 14]
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
    g = [grupo("M", offset=(0, 0, i * s["H"])) for i in range(3)]
    R.cena(g, 900, 1180, az=44, el=13).save(os.path.join(SAIDA, "04-pilha.png"))

    # ---- 05 o encaixe em destaque ----------------------------------------
    g = [grupo("M", destaque=True),
         grupo("M", offset=(0, 0, s["H"] + 70), destaque=True)]
    R.cena(g, 1150, 1000, az=58, el=14).save(os.path.join(SAIDA, "05-encaixe.png"))

    # ---- 06 ninho x pilha -------------------------------------------------
    g = [grupo("M", offset=(-340, 0, i * s["passo_ninho"]), giro=bool(i % 2))
         for i in range(10)]
    g += [grupo("M", offset=(340, 0, i * s["H"]), cor=COR_CORPO["G"]) for i in range(3)]
    R.cena(g, 1450, 900, az=40, el=15).save(os.path.join(SAIDA, "06-ninho-x-pilha.png"))

    # ---- 07 a peca de casa: torre de tres P em branco ---------------------
    sP = fichas["P"][1]
    g = [grupo("P", offset=(0, 0, i * sP["H"])) for i in range(3)]
    R.cena(g, 900, 1100, az=48, el=13, fundo=(212, 207, 199)) \
        .save(os.path.join(SAIDA, "07-torre-casa.png"))

    print("  imagens em", SAIDA)


if __name__ == "__main__":
    main()
