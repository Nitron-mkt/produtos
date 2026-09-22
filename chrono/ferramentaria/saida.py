# -*- coding: utf-8 -*-
"""Auditoria de moldabilidade: varre cada face do STEP e mede o angulo de saida
em relacao ao eixo de extracao (Y). Face vertical = 0 grau = nao sai do molde.
  python3 saida.py"""
import sys, math, numpy as np, cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.GeomAbs import (GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone,
                         GeomAbs_Sphere, GeomAbs_Torus, GeomAbs_BSplineSurface)
S = '/home/user/produtos/chrono/step_v2'
EIXO = np.array([0.0, 1.0, 0.0])        # extracao em Y
TIPO = {GeomAbs_Plane:'plano', GeomAbs_Cylinder:'cilindro', GeomAbs_Cone:'cone',
        GeomAbs_Sphere:'esfera', GeomAbs_Torus:'toro', GeomAbs_BSplineSurface:'bspline'}

def area(f):
    p = GProp_GProps(); BRepGProp.SurfaceProperties_s(f.wrapped, p); return p.Mass()

def audita(arq, nome):
    sh = cq.importers.importStep(arq).val()
    linhas = []
    for f in sh.Faces():
        ad = BRepAdaptor_Surface(f.wrapped)
        t = TIPO.get(ad.GetType(), 'outra')
        u0,u1,v0,v1 = f._uvBounds()
        ns = []
        for u in np.linspace(u0,u1,5)[1:-1]:
            for v in np.linspace(v0,v1,5)[1:-1]:
                try:
                    n = f.normalAt(f.Center()) if t=='plano' else None
                except Exception: n = None
                ns.append(n)
        n = f.normalAt()
        n = np.array([n.x, n.y, n.z]); n /= np.linalg.norm(n)
        cos = abs(float(n @ EIXO))
        saida = math.degrees(math.asin(min(1.0, cos)))   # 0 = parede vertical
        linhas.append((t, area(f), saida, f))
    A = sum(l[1] for l in linhas)
    verticais = [l for l in linhas if l[2] < 0.5 and l[0] != 'plano' or (l[0]=='plano' and l[2] < 0.5)]
    av = sum(l[1] for l in verticais)
    print('%s' % nome)
    print('   %d faces, area %.1f mm2' % (len(linhas), A))
    porTipo = {}
    for t, a, s, _ in linhas: porTipo.setdefault(t, [0,0.0,[]]); porTipo[t][0]+=1; porTipo[t][1]+=a; porTipo[t][2].append(s)
    for t,(n,a,ss) in sorted(porTipo.items(), key=lambda k:-k[1][1]):
        print('      %-9s %4d faces  %7.1f mm2  saida min %5.2f  med %5.2f graus' % (t,n,a,min(ss),float(np.mean(ss))))
    print('   PAREDE VERTICAL (saida < 0,5 graus): %d faces, %.1f mm2 = %.0f%% da area' %
          (len(verticais), av, 100*av/A))
    return linhas

for arq, nome in [('Chrono_M02_Rodinha_Meses','M02 rodinha dos meses'),
                  ('Chrono_M03_Ponteira','M03 ponteira'),
                  ('Chrono_M01b_SOMAR_2_poste_mesa_dias_detentes','M01 acrescimos na valvula')]:
    audita(f'{S}/{arq}.step', nome); print()
