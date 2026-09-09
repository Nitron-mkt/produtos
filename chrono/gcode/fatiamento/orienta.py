import trimesh, numpy as np
D='/home/user/produtos/chrono/stl/'
def prep(fn, flip, dx=0.0, dy=0.0):
    m=trimesh.load(D+fn)
    ang=-np.pi/2 if flip else np.pi/2         # eixo da peca (Y do STL) -> Z
    m.apply_transform(trimesh.transformations.rotation_matrix(ang,[1,0,0]))
    c=(m.bounds[0]+m.bounds[1])/2
    m.apply_translation([-c[0]+dx+110, -c[1]+dy+110, -m.bounds[0][2]])  # centro da mesa 110,110; apoia em z=0
    return m
P=prep('Chrono_01_Pino_Travinha.stl', True)    # invertido: face de topo na mesa
A=prep('Chrono_02_Anel_Dia.stl',      False)   # plano, numeros para cima
M=prep('Chrono_03_Anel_Mes.stl',      False)
for n,m in [('pino',P),('anel_dia',A),('anel_mes',M)]:
    b=m.bounds
    print('%-9s XY %.2f x %.2f  altura %.2f  watertight=%s'%(n, b[1][0]-b[0][0], b[1][1]-b[0][1], b[1][2], m.is_watertight))
    m.export(f'{n}.stl')
# chapa com as tres: pino a esquerda, anel de dia a direita, anel de mes embaixo
P2=prep('Chrono_01_Pino_Travinha.stl', True,  -26, 12)
A2=prep('Chrono_02_Anel_Dia.stl',      False,  26, 12)
M2=prep('Chrono_03_Anel_Mes.stl',      False,   0,-26)
for n,m in [('chapa_pino',P2),('chapa_dia',A2),('chapa_mes',M2)]: m.export(f'{n}.stl')
u=trimesh.util.concatenate([P2,A2,M2]); b=u.bounds
print('chapa: XY %.1f x %.1f mm'%(b[1][0]-b[0][0], b[1][1]-b[0][1]))
