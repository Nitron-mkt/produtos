"""Vistas de inspecao e de secao do M para o dossie em PDF (out/det-*.png).

Usa secao.corta() para cortar a malha por planos: e assim que se ve o copo de
cima dentro do copo de baixo no ninho e o rodape dentro do canal na pilha,
sem CAD. Roda depois de exporta.py:  python3 detalhes.py
"""
import os
import modelo, render as R, secao
from modelo import ficha
from exporta import paleta, COR_CORPO

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def main(k="M"):
    modelo.AMOSTRA = [2.6, 14]
    sol, s = ficha(k)
    ns = sol.normais_suaves(42)
    cor = paleta(COR_CORPO[k])
    cinza = dict.fromkeys(cor, (125, 125, 125))
    claro = dict.fromkeys(cor, (215, 205, 195))
    perna, pn, pp = s["perna"], s["passo_ninho"], s["passo_pilha"]
    Xb2, Yb2, H = s["Xb"] / 2, s["Yb"] / 2, s["hc"]
    yc = s["y_col"][0] * 1.17          # a coluna deriva com a conicidade

    def peca(off=(0, 0, 0), giro=False):
        return sol.triangulos(offset=off, giro180=giro)

    def clip(tris, *planos):
        for p0, n in planos:
            tris = secao.corta(tris, p0, n)
        return tris

    def salva(nome, grupos, W, Hh, az, el, sombra=False):
        R.cena(grupos, W, Hh, az=az, el=el, sombra=sombra).save(os.path.join(OUT, f"det-{nome}.png"))

    # isometrica e por baixo
    salva("iso", [(peca(), cor, ns)], 1800, 1300, 42, 23, True)
    salva("baixo", [(peca(), cor, ns)], 1600, 1150, 35, -28)
    # meia peca (x > 0) vista de lado: aro, parede, fundo nervurado, copo
    salva("meia", [(clip(peca(), ((0, 0, 0), (1, 0, 0))), cor, None)], 1400, 1000, 270, 8)
    # o canto cortado, visto de dentro
    q = [((Xb2 - 85, 0, 0), (1, 0, 0)), ((0, Yb2 - 85, 0), (0, 1, 0)), ((0, 0, perna + 40), (0, 0, -1))]
    salva("canto", [(clip(peca(), *q), cor, None)], 1200, 950, 225, 40)
    # topo da coluna: ponte, canal, guia
    pc = [((Xb2 - 70, 0, 0), (1, 0, 0)), ((0, yc - 40, 0), (0, 1, 0)), ((0, yc + 40, 0), (0, -1, 0)),
          ((0, 0, perna + H - 40), (0, 0, 1))]
    salva("canal", [(clip(peca(), *pc), cor, None)], 1200, 950, 250, 38)
    # ninho: tres pecas cortadas pelos copos do lado +x
    corte_x = ((Xb2 - 26, 0, 0), (-1, 0, 0))
    cores = [cinza, cor, claro]
    salva("ninho-secao", [(clip(peca((0, 0, i * pn), bool(i % 2)), corte_x), cores[i], None) for i in range(3)],
          1500, 950, 18, 14)
    rec = [corte_x, ((Xb2 - 130, 0, 0), (1, 0, 0)), ((0, Yb2 - 130, 0), (0, 1, 0)), ((0, 0, perna + 40), (0, 0, -1))]
    salva("ninho-canto", [(clip(peca(), *rec), cinza, None), (clip(peca((0, 0, pn), True), *rec), cor, None)],
          1200, 950, 25, 18)
    # pilha: duas pecas cortadas pela coluna
    corte_y = ((0, yc, 0), (0, -1, 0))
    salva("pilha-secao", [(clip(peca(), corte_y), cinza, None), (clip(peca((0, 0, pp)), corte_y), cor, None)],
          1000, 1300, 62, 12)
    rec = [corte_y, ((0, yc - 70, 0), (0, 1, 0)), ((Xb2 - 80, 0, 0), (1, 0, 0)),
           ((0, 0, perna + H - 50), (0, 0, 1)), ((0, 0, perna + H + 50), (0, 0, -1))]
    salva("pilha-assento", [(clip(peca(), *rec), cinza, None), (clip(peca((0, 0, pp)), *rec), cor, None)],
          1200, 950, 62, 16)
    print("  detalhes em", OUT)


if __name__ == "__main__":
    main()
