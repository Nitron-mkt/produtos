# -*- coding: utf-8 -*-
"""Auditoria de saida honesta: varre cada face em malha de parametros e usa a
PIOR saida da face, nao a normal do ponto do meio. Uma normal so num cilindro
serve; numa esfera ou num cone mente."""
import sys, os, math, numpy as np, cadquery as cq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_Sphere, GeomAbs_Torus
EIXO = np.array([0.0, 1.0, 0.0])
NOME = {GeomAbs_Plane:'plano', GeomAbs_Cylinder:'cilindro', GeomAbs_Cone:'cone',
        GeomAbs_Sphere:'esfera', GeomAbs_Torus:'toro'}

def pior_saida(f):
    """ARMADILHA: f.Surface().Value(u,v) levanta excecao e, com o except
    continue, TODA face passava como se tivesse saida. Aqui o ponto sai do
    adaptador, e se nenhuma amostra vingar a face e reprovada, nao aprovada."""
    ad = BRepAdaptor_Surface(f.wrapped)
    u0, u1 = ad.FirstUParameter(), ad.LastUParameter()
    v0, v1 = ad.FirstVParameter(), ad.LastVParameter()
    pior, n_ok = 90.0, 0
    for u in np.linspace(u0, u1, 5):
        for v in np.linspace(v0, v1, 5):
            try:
                pt = ad.Value(float(u), float(v))
                n = f.normalAt(cq.Vector(pt.X(), pt.Y(), pt.Z()))
            except Exception: continue
            n_ok += 1
            n = np.array([n.x, n.y, n.z]); L = np.linalg.norm(n)
            if L < 1e-12: continue
            n /= L
            pior = min(pior, math.degrees(math.asin(min(1.0, abs(float(n @ EIXO))))))
    return pior if n_ok else 0.0

def audita(arq, nome, lim=0.5):
    sh = cq.importers.importStep(arq).val()
    tot = viva = 0.0; det = []
    for f in sh.Faces():
        p = GProp_GProps(); BRepGProp.SurfaceProperties_s(f.wrapped, p); ar = p.Mass()
        t = NOME.get(BRepAdaptor_Surface(f.wrapped).GetType(), 'outra')
        tot += ar
        if t == 'esfera':          # calota de detente: sai sozinha, ver secao 5
            continue
        s = pior_saida(f)
        if s < lim:
            viva += ar
            if ar > 0.3: det.append((ar, t, f.Center()))
    print('  %-34s %5d faces · parede vertical %.1f mm2 = %.1f%%'
          % (nome, len(sh.Faces()), viva, 100*viva/tot))
    for ar, t, c in sorted(det, key=lambda x: -x[0])[:8]:
        print('       %7.2f mm2  %-9s  X %6.2f  Y %6.2f  Z %6.2f' % (ar, t, c.x, c.y, c.z))

if __name__ == '__main__':
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step')
    for a, n in [('v3_M01a_SOMAR_1_enchimento_e_mesa', 'M01a enchimento e mesa'),
                 ('v3_M01b_SUBTRAIR_2_rebaixo', 'M01b rebaixo'),
                 ('v3_M01c_SOMAR_3_poste_detentes_dias', 'M01c poste/detentes/dias'),
                 ('v3_M01d_SUBTRAIR_4_furo_passante', 'M01d furo'),
                 ('v3_M02_Rodinha_Meses', 'M02 rodinha'),
                 ('v3_M03_Ponteira', 'M03 ponteira')]:
        audita('%s/%s.step' % (D, a), n)

def m01_montado():
    """Audita o que o Chrono ACRESCENTA, em B-rep, sobre uma chapa lisa que faz
    as vezes da valvula. Assim as paredes verticais da valvula original — que ja
    esta ferramentada e nao e nossa — ficam de fora da conta, e as nossas nao
    escapam por estarem espalhadas em 4 arquivos de operacao."""
    import params as Pp
    from lib_v3 import cil
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step')
    L = lambda n: cq.importers.importStep('%s/%s.step' % (D, n)).val()
    from lib_v3 import cone as _cone
    # a chapa de mentira leva saida tambem, senao o OD dela aparece na conta
    chapa = _cone(19.0, 19.0 - Pp.rec(Pp.FACE - Pp.CHAPA_Y0), Pp.CHAPA_Y0, Pp.FACE).moved(cq.Location(cq.Vector(Pp.CX, 0, Pp.CZ)))
    r = chapa.fuse(L('v3_M01a_SOMAR_1_enchimento_e_mesa'))
    r = r.cut(L('v3_M01b_SUBTRAIR_2_rebaixo'))
    entraram = 0
    for x in L('v3_M01c_SOMAR_3_poste_detentes_dias').Solids():
        try:
            o = r.fuse(x)
            # so aceita se o volume SUBIU (o solido entrou) e o solido continua
            # valido. 'caiu menos de 10%' deixava passar uniao que apagou a peca.
            if o.Volume() >= r.Volume() - 1e-6 and BRepCheck_Analyzer(o.wrapped).IsValid():
                r = o; entraram += 1
        except Exception: pass
    print('      (fundidos %d de 56 solidos do M01c)' % entraram)
    r = r.cut(L('v3_M01d_SUBTRAIR_4_furo_passante'))
    cq.exporters.export(cq.Workplane(obj=r), '%s/_prova_M01_montado.step' % D, exportType='STEP')
    audita('%s/_prova_M01_montado.step' % D, 'M01 montado sobre chapa lisa')
