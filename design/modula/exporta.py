"""Gera STL, JSON (visualizador web) e as vistas renderizadas da familia MODULA."""
import base64, json, math, os, sys
import numpy as np
import modelo
from modelo import construir, ficha, TAN, RHO_PP
import render as R

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(SAIDA, exist_ok=True)

COR_CORPO = {"P": R.PALETA["laranja"], "M": R.PALETA["laranja"], "G": R.PALETA["chumbo"]}


def paleta(base, destaque=False):
    c = dict.fromkeys(["faixa", "ripa", "aro", "fundo", "pino", "pe"], base)
    c["pe"] = R.PALETA["destaque"] if destaque else base
    c["pino"] = R.PALETA["critico"] if destaque else base
    c["fundo"] = tuple(int(v * 0.95) for v in base)
    c["aro"] = tuple(min(255, int(v * 1.07)) for v in base)
    return c


TAGS = ["faixa", "ripa", "aro", "fundo", "pino", "pe"]


def malha_json(m, s):
    """Triangulos quantizados em 0,25 mm -> int16 -> base64."""
    esc = 4.0
    vals = []
    grupos = {t: [] for t in ("corpo", "pino", "pe")}
    for a, b, c, tag in m.tris:
        g = "pino" if tag == "pino" else ("pe" if tag == "pe" else "corpo")
        grupos[g].append((a, b, c))
    saida = {}
    for g, tris in grupos.items():
        buf = []
        for a, b, c in tris:
            for v in (a, b, c):
                buf += [int(round(v[0] * esc)), int(round(v[2] * esc)),
                        int(round(-v[1] * esc))]          # z sobe -> y do three
        arr = np.array(buf, dtype="<i2")
        saida[g] = base64.b64encode(arr.tobytes()).decode()
    return dict(
        X=s["X"], Y=s["Y"], H=s["H"], hf=s["hf"], e=s["e"], R=s["R"],
        passo=s["passo_ninho"], massa=round(s["massa_g"]),
        total=round(s["litros_total"], 1), boca=round(s["litros_boca"], 1),
        aba=s["aba"], pe=s["sal_pe"], esc=esc, malha=saida)


def main():
    fichas, dados = {}, {}
    for k in ("P", "M", "G"):
        sol, s = ficha(k)
        fichas[k] = (sol, s)
        print(f"  {k}: {len(sol.tris)} triangulos, {s['massa_g']:.0f} g")
    modelo.AMOSTRA = [4.4, 9]                       # malha leve para o navegador
    for k in ("P", "M", "G"):
        leve, sl = ficha(k)
        dados[k] = malha_json(leve, sl)
    modelo.AMOSTRA = [2.6, 14]
    with open(os.path.join(SAIDA, "modula.json"), "w") as f:
        json.dump(dados, f, separators=(",", ":"))

    # ---- 01 familia -------------------------------------------------------
    grupos, x = [], 0.0
    for k in ("P", "M", "G"):
        sol, s = fichas[k]
        x += s["X"] / 2 + 46
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
         (sol.triangulos(offset=(0, 0, s["H"] + 60)), paleta(COR_CORPO["M"], destaque=True))]
    R.cena(g, 1200, 1000, az=52, el=16).save(os.path.join(SAIDA, "05-mecanismo.png"))

    # ---- 06 ninho x pilha lado a lado ------------------------------------
    g = []
    for i in range(6):
        g.append((sol.triangulos(offset=(-320, 0, i * s["passo_ninho"]), giro180=bool(i % 2)),
                  paleta(COR_CORPO["M"])))
    for i in range(3):
        g.append((sol.triangulos(offset=(320, 0, i * s["H"])), paleta(COR_CORPO["G"])))
    R.cena(g, 1400, 900, az=40, el=16).save(os.path.join(SAIDA, "06-ninho-x-pilha.png"))

    # ---- 07 detalhe do pe e do pino ---------------------------------------
    solG, sG = fichas["G"]
    g = [(solG.triangulos(), paleta(R.PALETA["chumbo"], destaque=True)),
         (solG.triangulos(offset=(0, 0, sG["H"] + 70)),
          paleta(R.PALETA["chumbo"], destaque=True))]
    R.cena(g, 1100, 1000, az=64, el=12).save(os.path.join(SAIDA, "07-G-encaixe.png"))
    print("  imagens em", SAIDA)


if __name__ == "__main__":
    main()
