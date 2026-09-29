# -*- coding: utf-8 -*-
"""Porteiro de qualidade do STEP — o teste que faltava.

O projetista abriu a v3 no SolidWorks e a peca veio "toda fatiada, pontinhada,
os pontos nao ligados". Nao era casca: os arquivos ja tinham MANIFOLD_SOLID_BREP
e CLOSED_SHELL. Era ARESTA CURTA DEMAIS — 763 arestas abaixo de 0,01 mm, a menor
com 0,0015 mm, vindas do buffer que arredonda o canto das letras. Importador de
STEP colapsa aresta nessa ordem e a costura do solido se desfaz.

Limites:
  aresta  >= 0,05 mm   (o SolidWorks costura com folga bem menor que isso)
  face    >= 0,002 mm2
  e cada arquivo tem de ser UM solido fechado e valido.

  python3 qualidade.py
"""
import sys, os, glob, numpy as np, cadquery as cq
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepCheck import BRepCheck_Analyzer

MIN_ARESTA, MIN_FACE = 0.05, 0.002
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step')

def medir(arq):
    sh = cq.importers.importStep(arq).val()
    L = []
    for e in sh.Edges():
        p = GProp_GProps(); BRepGProp.LinearProperties_s(e.wrapped, p); L.append(p.Mass())
    A = []
    for f in sh.Faces():
        p = GProp_GProps(); BRepGProp.SurfaceProperties_s(f.wrapped, p); A.append(p.Mass())
    L, A = np.array(L), np.array(A)
    return sh, L, A

ruim = 0
print('%-52s %6s %9s %7s %9s %7s' % ('arquivo', 'sol.', 'aresta min', 'curtas', 'face min', 'micro'))
for arq in sorted(glob.glob(os.path.join(D, 'Chrono_v3_*.step'))):
    sh, L, A = medir(arq)
    ns, nc, nm = len(sh.Solids()), int((L < MIN_ARESTA).sum()), int((A < MIN_FACE).sum())
    ok = (ns == 1 and nc == 0 and nm == 0 and BRepCheck_Analyzer(sh.wrapped).IsValid())
    ruim += 0 if ok else 1
    print('%-52s %6d %9.4f %7d %9.5f %7d  %s'
          % (os.path.basename(arq), ns, L.min(), nc, A.min(), nm, 'ok' if ok else '*** REPROVA ***'))
print()
print('REPROVADOS: %d' % ruim if ruim else 'todos passam: 1 solido, B-rep valido, sem aresta < %.2f mm nem face < %.3f mm2'
      % (MIN_ARESTA, MIN_FACE))
sys.exit(1 if ruim else 0)
