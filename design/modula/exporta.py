"""Gera STL, JSON (visualizador web) e as vistas renderizadas da familia MODULA."""
import json, math, os, struct, sys
import numpy as np
from modelo import construir, ficha, TAN, RHO_PP
import render as R

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(SAIDA, exist_ok=True)

COR_CORPO = {"P": R.PALETA["laranja"], "M": R.PALETA["laranja"], "G": R.PALETA["chumbo"]}


def paleta(base, destaque=False):
    c = dict.fromkeys(
        ["corpo", "fundo", "nervura", "lateral", "traseira", "frontal",
         "aro", "vinco", "poste", "canal", "rebordo"], base)
    c["talisca"] = R.PALETA["destaque"] if destaque else base
    c["assento"] = R.PALETA["critico"] if destaque else base
    c["canal"] = tuple(int(v * 0.94) for v in base)
    c["rebordo"] = tuple(min(255, int(v * 1.08)) for v in base)
    return c


def stl(tris, caminho, nome):
    with open(caminho, "wb") as f:
        f.write(struct.pack("<80sI", nome.encode()[:80].ljust(80, b" "), len(tris)))
        for a, b, c, _ in tris:
            n = np.cross(np.subtract(b, a), np.subtract(c, a))
            ln = np.linalg.norm(n)
            n = n / ln if ln else n
            f.write(struct.pack("<12f H", *n, *a, *b, *c, 0))


def caixas_json(sol, s):
    return dict(
        Xb=sol.Xb, Yb=sol.Yb, tx=sol.tx, ty=sol.ty,
        X=s["X"], Y=s["Y"], H=s["H"], hf=s["hf"], e=s["e"],
        passo=s["passo_ninho"], massa=round(s["massa_g"]),
        util=round(s["litros_boca"], 1), total=round(s["litros_total"], 1),
        pecas=[[round(p.x0, 2), round(p.x1, 2), round(p.y0, 2), round(p.y1, 2),
                round(p.z0, 2), round(p.z1a, 2), round(p.z1b, 2),
                ["corpo", "talisca", "assento", "canal", "rebordo"].index(p.tag)
                if p.tag in ("corpo", "talisca", "assento", "canal", "rebordo") else 0]
               for p in sol.pecas])


def main():
    fichas, dados = {}, {}
    for k in ("P", "M", "G"):
        sol, s = ficha(k)
        fichas[k] = (sol, s)
        tris = sol.triangulos()
        stl(tris, os.path.join(SAIDA, f"modula-{k}.stl"), f"MODULA {k}")
        dados[k] = caixas_json(sol, s)
        print(f"  STL {k}: {len(tris)} triangulos")
    with open(os.path.join(SAIDA, "modula.json"), "w") as f:
        json.dump(dados, f, separators=(",", ":"))

    # ---- 01 familia -------------------------------------------------------
    grupos, x = [], 0.0
    for k in ("P", "M", "G"):
        sol, s = fichas[k]
        x += s["X"] / 2 + 40
        grupos.append((sol.triangulos(offset=(x, 0, 0)), paleta(COR_CORPO[k])))
        x += s["X"] / 2
    R.cena(grupos, 1500, 620, az=34, el=22).save(os.path.join(SAIDA, "01-familia.png"))

    # ---- 02 MODULA M isometrico ------------------------------------------
    sol, s = fichas["M"]
    R.cena([(sol.triangulos(), paleta(COR_CORPO["M"]))], 1200, 950, az=42, el=24) \
        .save(os.path.join(SAIDA, "02-M-iso.png"))

    # ---- 03 ninho (transporte) -------------------------------------------
    g = []
    for i in range(6):
        g.append((sol.triangulos(offset=(0, 0, i * s["passo_ninho"]), giro180=bool(i % 2)),
                  paleta(COR_CORPO["M"])))
    R.cena(g, 1200, 950, az=42, el=20).save(os.path.join(SAIDA, "03-ninho.png"))

    # ---- 04 pilha (uso) --------------------------------------------------
    g = [(sol.triangulos(offset=(0, 0, i * s["H"])), paleta(COR_CORPO["M"]))
         for i in range(3)]
    R.cena(g, 900, 1150, az=42, el=14).save(os.path.join(SAIDA, "04-pilha.png"))

    # ---- 05 mecanismo (talisca + assento em destaque) --------------------
    g = [(sol.triangulos(), paleta(COR_CORPO["M"], destaque=True)),
         (sol.triangulos(offset=(0, 0, s["H"] + 55)), paleta(COR_CORPO["M"], destaque=True))]
    R.cena(g, 1200, 1000, az=52, el=16).save(os.path.join(SAIDA, "05-mecanismo.png"))

    # ---- 06 ninho x pilha lado a lado ------------------------------------
    g = []
    for i in range(6):
        g.append((sol.triangulos(offset=(-320, 0, i * s["passo_ninho"]), giro180=bool(i % 2)),
                  paleta(COR_CORPO["M"])))
    for i in range(3):
        g.append((sol.triangulos(offset=(320, 0, i * s["H"])), paleta(COR_CORPO["G"])))
    R.cena(g, 1400, 900, az=40, el=16).save(os.path.join(SAIDA, "06-ninho-x-pilha.png"))

    # ---- 07 torre mista (andares) ----------------------------------------
    g = []
    solG, sG = fichas["G"]
    solM, sM = fichas["M"]
    solP, sP = fichas["P"]
    g.append((solG.triangulos(), paleta(R.PALETA["chumbo"])))
    g.append((solG.triangulos(offset=(0, 0, sG["H"])), paleta(R.PALETA["chumbo"])))
    for i, ox in ((0, -sM["X"] / 2 - 4), (1, sM["X"] / 2 + 4)):
        g.append((solM.triangulos(offset=(0, 0, 0)), paleta(R.PALETA["laranja"])))
    R.cena(g[:2], 1000, 1000, az=40, el=16).save(os.path.join(SAIDA, "07-G-pilha.png"))
    print("  imagens em", SAIDA)


if __name__ == "__main__":
    main()
