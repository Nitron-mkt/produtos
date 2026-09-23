# -*- coding: utf-8 -*-
"""Monta o visor HTML do Chrono: embute os solidos em base64 no modelo.html.

Formato de cada malha (o mesmo do visor do cesto P):
  f32 mn[3] · f32 sc[3] · u32 nv · u32 nf · u16 pos[nv*3] · u16 idx[nf*3]
Posicao quantizada em 16 bits dentro da propria caixa: passo de ~0,0007 mm numa
peca de 44 mm, uma ordem de grandeza abaixo da tesselacao do STL.

  python3 gera.py
"""
import base64, os, struct, numpy as np, trimesh

AQUI = os.path.dirname(os.path.abspath(__file__))
STL  = os.path.join(AQUI, '..', 'stl_v2')
UP   = '/root/.claude/uploads/25a64868-b28d-5a69-b1c3-502a4891561f/'
TAMPA = UP + '1c50a47b-Mont_pote_com_valvula__Tampa_Pote_025_Pequeno_Cav1.STL'
CX, CZ = 61.97, 102.68
SAIDA = os.path.join(AQUI, 'Chrono_Datador.html')

def empacota(m):
    v = np.asarray(m.vertices, dtype=np.float64)
    f = np.asarray(m.faces, dtype=np.int64)
    if len(v) > 65536:
        raise SystemExit('malha com %d vertices: indice u16 nao alcanca' % len(v))
    mn, mx = v.min(0), v.max(0)
    sc = np.where(mx - mn > 1e-12, (mx - mn) / 65535.0, 1.0)
    q = np.clip(np.round((v - mn) / sc), 0, 65535).astype('<u2')
    b = struct.pack('<6f2I', *mn.astype('f4'), *sc.astype('f4'), len(v), len(f))
    b += q.tobytes() + f.astype('<u2').tobytes()
    return base64.b64encode(b).decode('ascii'), len(f)

def limpa(m):
    m.merge_vertices(digits_vertex=6)
    m.update_faces(m.nondegenerate_faces()); m.update_faces(m.unique_faces())
    m.remove_unreferenced_vertices()
    return m

print('carregando os solidos')
pecas = {}
for k, arq in [('m01','Chrono_M01_Valvula_Dias.stl'),
               ('m02','Chrono_M02_Rodinha_Meses.stl'),
               ('m03','Chrono_M03_Ponteira.stl')]:
    pecas[k] = limpa(trimesh.load(os.path.join(STL, arq)))

# tampa: recorte de O60 em volta do poco, para dar contexto sem carregar 148 k
# triangulos. Booleano de verdade (nao selecao de face) para o corte sair limpo.
print('recortando a tampa em O60 no poco da valvula')
t = trimesh.load(TAMPA)
cil = trimesh.creation.cylinder(radius=30.0, height=40.0, sections=192)
cil.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1,0,0]))
cil.apply_translation([CX, 35.0, CZ])
disco = trimesh.boolean.boolean_manifold([t, cil], operation='intersection')
alvo = 24000
if len(disco.faces) > alvo:
    antes = len(disco.faces)
    disco = disco.simplify_quadric_decimation(face_count=alvo)
    print('  %d -> %d faces' % (antes, len(disco.faces)))
pecas['tampa'] = limpa(disco)

partes, total = [], 0
for k, m in pecas.items():
    b64, nf = empacota(m)
    total += nf
    partes.append('  %s: "%s"' % (k, b64))
    print('  %-6s %6d vert  %6d faces  %7.0f KB em base64' % (k, len(m.vertices), nf, len(b64)/1024))

html = open(os.path.join(AQUI, 'modelo.html'), encoding='utf-8').read()
html = html.replace('__MALHAS__', '{\n' + ',\n'.join(partes) + '\n}')
html = html.replace('__TRIANGULOS__', '{:,}'.format(total).replace(',', '.'))
open(SAIDA, 'w', encoding='utf-8').write(html)
print('\n%s  ->  %.2f MB, %s triangulos' % (os.path.basename(SAIDA),
      os.path.getsize(SAIDA)/1e6, '{:,}'.format(total).replace(',', '.')))
