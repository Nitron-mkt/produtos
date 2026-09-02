# -*- coding: utf-8 -*-
"""Monta o artefato: injeta o blob de geometria e o corte SVG no template."""
import os
here = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(here, 'artefato.tpl.html')).read()
geo = open(os.path.join(here, 'web/geo.js')).read()
aa = open(os.path.join(here, 'web/secao-aa.svg')).read()
bb = open(os.path.join(here, 'web/secao-bb.svg')).read()
out = (tpl.replace('/*GEO*/', geo)
          .replace('<!--SECAO_AA-->', aa).replace('<!--SECAO_BB-->', bb))
dst = os.path.join(here, '..', 'analise', '06-tampa-portinhola.html')
open(dst, 'w').write(out)
print('%s  %.0f kB' % (os.path.normpath(dst), len(out) / 1024))
