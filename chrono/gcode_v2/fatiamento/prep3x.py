"""Chapa 3x: disco de prova + aro + travinha, escalados e posicionados a mao
(o --scale do CLI escala em torno do centro do objeto e bagunca o arranjo)."""
import trimesh, numpy as np, os
S='/home/user/produtos/chrono/stl_v2/'; K=3.0; os.makedirs('prep3x',exist_ok=True)
POS={'disco':(70,135),'aro':(190,175),'travinha':(190,75)}
ARQ={'disco':'Chrono_M01_Disco_Prova.stl','aro':'Chrono_M02_Aro_Meses.stl',
     'travinha':'Chrono_M03_Travinha_Seta.stl'}
cx={}
for n,f in ARQ.items():
    m=trimesh.load(S+f)
    # a travinha vai INVERTIDA: com o pino para baixo ela apoiaria na ponta dele
    ang = -np.pi/2 if n=='travinha' else np.pi/2
    m.apply_transform(trimesh.transformations.rotation_matrix(ang,[1,0,0]))  # Y -> Z
    m.apply_scale(K)
    c=(m.bounds[0]+m.bounds[1])/2
    m.apply_translation([-c[0]+POS[n][0], -c[1]+POS[n][1], -m.bounds[0][2]])
    b=m.bounds; cx[n]=b
    print('%-9s X %6.1f..%6.1f  Y %6.1f..%6.1f  altura %5.1f  %s'
          %(n,b[0][0],b[1][0],b[0][1],b[1][1],b[1][2],
            'FORA' if (b[0][0]<0 or b[1][0]>255 or b[0][1]<0 or b[1][1]>255) else 'ok'))
    m.export(f'prep3x/3x_{n}.stl')
k=list(cx); 
for i in range(len(k)):
    for j in range(i+1,len(k)):
        a,b=cx[k[i]],cx[k[j]]
        if a[0][0]<b[1][0] and b[0][0]<a[1][0] and a[0][1]<b[1][1] and b[0][1]<a[1][1]:
            print('*** %s e %s se sobrepoem'%(k[i],k[j]))
