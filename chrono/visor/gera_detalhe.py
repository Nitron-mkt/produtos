# -*- coding: utf-8 -*-
"""Monta o visor de inspecao: embute as malhas finas no modelo_detalhe.html."""
import base64, os, struct, numpy as np, trimesh
AQUI = os.path.dirname(os.path.abspath(__file__))
STL  = os.path.join(AQUI, '..', 'v3', 'stl_detalhe')
SAIDA = os.path.join(AQUI, 'Chrono_Detalhes.html')

def empacota(m):
    v = np.asarray(m.vertices, float); f = np.asarray(m.faces, np.int64)
    if len(v) > 65536: raise SystemExit('%d vertices: indice u16 nao alcanca' % len(v))
    mn, mx = v.min(0), v.max(0)
    sc = np.where(mx-mn > 1e-12, (mx-mn)/65535.0, 1.0)
    q = np.clip(np.round((v-mn)/sc), 0, 65535).astype('<u2')
    b = struct.pack('<6f2I', *mn.astype('f4'), *sc.astype('f4'), len(v), len(f))
    return base64.b64encode(b + q.tobytes() + f.astype('<u2').tobytes()).decode(), len(f)

partes, total = [], 0
for k, arq in [('m01','M01.stl'), ('m02','M02.stl'), ('m03','M03.stl'), ('m01c','M01c.stl')]:
    m = trimesh.load(os.path.join(STL, arq))
    b64, nf = empacota(m); total += nf
    partes.append('  %s: "%s"' % (k, b64))
    print('  %-5s %7d faces  %7.0f KB em base64' % (k, nf, len(b64)/1024))

html = open(os.path.join(AQUI, 'modelo_detalhe.html'), encoding='utf-8').read()
html = html.replace('__MALHAS__', '{\n' + ',\n'.join(partes) + '\n}')
html = html.replace('__TRIANGULOS__', '{:,}'.format(total).replace(',', '.'))
open(SAIDA, 'w', encoding='utf-8').write(html)
print('\n%s -> %.2f MB, %s triangulos'
      % (os.path.basename(SAIDA), os.path.getsize(SAIDA)/1e6, '{:,}'.format(total).replace(',', '.')))
