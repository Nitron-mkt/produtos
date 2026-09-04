#!/usr/bin/env python3
"""Elevacoes frontais cotadas das 4 familias de PDV, na estrutura de medida fixa.

Gera analise/render/pdv-fam-<FAMILIA>.svg — SVG inline, sem dependencia externa,
usando as variaveis CSS do caderno (--wood, --no-tz, --dim...) para acompanhar
o tema claro/escuro do documento que o embute.

Cotas conforme analise/11-nitron-mob-cota-final.md.
"""
import pathlib

ENC, NOX, NOXC, NOY, NOZ = 40.60, 61.61, 101.30, 83.23, 73.08
PE = 60 - ENC
V  = '#08a9b1'                       # verde da marca
CONSOME = 2*ENC

ext_comp = lambda B, N: 2*NOX + (N-1)*NOXC + N*(B-CONSOME)
ext_prof = lambda B:    B + 2*(NOY-ENC)
ext_alt  = lambda B, n: n*NOZ + (n-1)*(B-CONSOME) + PE
passo_x  = lambda B:    B + NOXC - CONSOME
passo_v  = lambda B:    (B-CONSOME) + NOZ

BV = 270                             # BAL-02-AC — a vertical das quatro familias

FAM = [
  dict(familia='CHECKOUT',          bc=415, bl=287, pan=(300,450), N=2, n=5,
       fundo=False, deck=True,  peg=True,  casinha=False, capsula=True),
  dict(familia='ILHA',              bc=595, bl=415, pan=(460,634), N=2, n=4,
       fundo=False, deck=True,  peg=False, casinha=False, capsula=True),
  dict(familia='PONTA DE GONDOLA',  bc=595, bl=287, pan=(300,634), N=2, n=7,
       fundo=True,  deck=False, peg=False, casinha=True,  capsula=True),
  dict(familia='PAREDAO',           bc=717, bl=200, pan=(200,754), N=4, n=8,
       fundo=True,  deck=False, peg=False, casinha=False, capsula=False),
]

def draw(f):
    B, N, n = f['bc'], f['N'], f['n']
    L = round(ext_comp(B, N)); P = round(ext_prof(f['bl'])); A = round(ext_alt(BV, n))
    PX = passo_x(B); pv = passo_v(BV)
    cab = int(0.13*A/10)*10
    fh  = int(0.22*L) if f['casinha'] else 0
    catb = 120 if f['familia'] == 'PAREDAO' else 0
    ml, mr, mt, mb = 250, 820, 70+cab+fh+40+catb, 300
    W, H = L+ml+mr, A+mt+mb
    s = [f'<svg viewBox="{-ml} {-mt} {W} {H}" role="img" aria-label="Elevacao frontal cotada: '
         f'{f["familia"]}, {L} por {P} por {A} milimetros, {N} vaos e {n} prateleiras">']
    ty = -(cab+40)

    def lead(y, txt, col='var(--dim-t)'):
        return (f'<path d="M{L+24} {y:.0f} H{L+96}" stroke="var(--dim)" stroke-width="4" fill="none"/>'
                f'<text class="sbn" x="{L+112}" y="{y:.0f}" dominant-baseline="middle" '
                f'font-size="50" fill="{col}">{txt}</text>')

    if f['casinha']:
        s.append(f'<path d="M0 {ty} L{L/2:.0f} {ty-fh} L{L} {ty} Z" fill="{V}"/>')
        s.append(lead(ty-fh/2, f'casinha · frontao {fh} mm', 'var(--brand-deep)'))
    s.append(f'<rect x="0" y="{ty}" width="{L}" height="{cab}" fill="{V}"/>')
    s.append(f'<text class="sbn" x="{L/2:.0f}" y="{ty+cab*0.56:.0f}" text-anchor="middle" '
             f'font-size="{cab*0.44:.0f}" fill="#fff">NITRON</text>')
    s.append(f'<text class="sal" x="{L/2:.0f}" y="{ty+cab*0.87:.0f}" text-anchor="middle" '
             f'font-size="{cab*0.19:.0f}" fill="#fff">toda casa tem</text>')
    s.append(lead(ty+cab/2, f'cabeceira {cab} mm'))

    ys = [A-PE-i*pv-NOZ/2 for i in range(n)]

    if f['fundo']:
        s.append(f'<rect x="{NOX}" y="{ys[-1]:.0f}" width="{L-2*NOX:.0f}" '
                 f'height="{ys[0]-ys[-1]:.0f}" fill="var(--wood)" opacity=".28"/>')
        s.append(lead((ys[0]+ys[-1])/2, 'painel de fundo · fecha a face'))

    for k, y in enumerate(ys):
        deck = f['deck'] and k == len(ys)-1
        if deck:
            s.append(f'<rect x="0" y="{y-20:.0f}" width="{L}" height="40" fill="var(--wood2)"/>')
        else:
            s.append(f'<rect x="0" y="{y-14:.0f}" width="{L}" height="28" fill="var(--wood)"/>')
        for i in range(N):
            x0 = NOX+i*PX+12; w = min(PX-44, L-x0-12)
            s.append(f'<rect x="{x0:.0f}" y="{y+16:.0f}" width="{w:.0f}" height="40" '
                     f'fill="{V}" opacity=".92"/>')
    if f['deck']: s.append(lead(ys[-1], 'top deck · painel inteiro', 'var(--brand-deep)'))
    s.append(lead(ys[0]+36, 'faixa de preco 40 mm'))

    if f['peg']:
        gy = (ys[-2]+ys[-3])/2
        s.append(f'<rect x="{NOX}" y="{gy-13:.0f}" width="{L-2*NOX:.0f}" height="26" fill="var(--no-tz)"/>')
        for i in range(int((L-2*NOX)//90)):
            hx = NOX+45+i*90
            s.append(f'<path d="M{hx} {gy+13} v46 a16 16 0 0 0 32 0" stroke="var(--no-tz)" '
                     f'stroke-width="7" fill="none"/>')
        s.append(lead(gy+30, f'gancheira · ripa {B} + ganchos', 'var(--brand-deep)'))

    if catb:
        for i in range(N):
            x = NOX+i*PX+10
            s.append(f'<rect x="{x:.0f}" y="{ty-108}" width="{min(PX-40,L-x-10):.0f}" '
                     f'height="92" fill="{V}" rx="10"/>')
        s.append(lead(ty-62, 'faixa de categoria 90 mm'))

    for i in range(N+1):
        x = 0 if i == 0 else (L-NOX if i == N else NOX+i*PX-NOXC)
        w = NOX if i in (0, N) else NOXC
        s.append(f'<rect x="{x:.0f}" y="{ys[-1]:.0f}" width="{w:.0f}" '
                 f'height="{A-PE-ys[-1]:.0f}" fill="var(--wood2)"/>')
        for y in ys:
            cor = 'var(--no-cz)' if 0 < i < N else 'var(--no-tz)'
            s.append(f'<rect x="{x:.0f}" y="{y-NOZ/2:.0f}" width="{w:.0f}" '
                     f'height="{NOZ:.0f}" fill="{cor}"/>')
        s.append(f'<rect x="{x+w/2-16:.0f}" y="{A-PE}" width="32" height="{PE}" fill="var(--wood2)"/>')
    if N > 1: s.append(lead(ys[1], 'cruzeta · no de meio de vao', 'var(--brand-deep)'))

    if f['capsula']:
        cw = min(380, L*0.42); cx = (L-cw)/2
        cyt = (ys[-1]+ys[-2])/2-36 if n > 1 else ys[-1]+56
        s.append(f'<rect x="{cx:.0f}" y="{cyt:.0f}" width="{cw:.0f}" height="72" rx="36" fill="{V}"/>')
        s.append(f'<text class="sbn" x="{L/2:.0f}" y="{cyt+50:.0f}" text-anchor="middle" '
                 f'font-size="44" fill="#fff">LEVE MAIS</text>')

    plw = min(PX-70, 340); plh = min(pv-92, 215); py = ys[min(1, n-1)]
    if plh > 70 and plw > 110:
        pyt = py-20-plh; pxc = NOX+22+plw/2
        s.append(f'<rect x="{NOX+22:.0f}" y="{pyt:.0f}" width="{plw:.0f}" height="{plh:.0f}" '
                 f'fill="{V}" rx="12"/>')
        s.append(f'<text class="sbn" x="{pxc:.0f}" y="{pyt+plh*0.56:.0f}" text-anchor="middle" '
                 f'font-size="{plh*0.4:.0f}" fill="#fff">NITRON</text>')
        s.append(f'<text class="sal" x="{pxc:.0f}" y="{pyt+plh*0.82:.0f}" text-anchor="middle" '
                 f'font-size="{plh*0.16:.0f}" fill="#fff">toda casa tem</text>')

    def dh(y, x0, x1, t):
        return (f'<g stroke="var(--dim)" stroke-width="4" fill="none"><path d="M{x0:.0f} {y} H{x1:.0f}"/>'
                f'<path d="M{x0:.0f} {y-24} V{y+24}"/><path d="M{x1:.0f} {y-24} V{y+24}"/></g>'
                f'<text class="sbn" x="{(x0+x1)/2:.0f}" y="{y-32}" text-anchor="middle" '
                f'font-size="58" fill="var(--dim-t)">{t}</text>')
    def dv(x, y0, y1, t):
        return (f'<g stroke="var(--dim)" stroke-width="4" fill="none"><path d="M{x} {y0:.0f} V{y1:.0f}"/>'
                f'<path d="M{x-24} {y0:.0f} H{x+24}"/><path d="M{x-24} {y1:.0f} H{x+24}"/></g>'
                f'<text class="sbn" transform="translate({x-30},{(y0+y1)/2:.0f}) rotate(-90)" '
                f'text-anchor="middle" font-size="50" fill="var(--dim-t)">{t}</text>')
    s.append(dh(A+120, 0, L, f'{L} mm'))
    s.append(dh(A+225, NOX, NOX+PX, f'vao {PX:.0f}'))
    s.append(dv(-70, ty-fh, A, f'{A+cab+40+fh} mm total'))
    s.append(dv(-176, ys[1] if n > 1 else ys[0], ys[0], f'passo {passo_v(BV):.0f}'))

    px0, py0, esc = 0, A+330, 0.42
    pw, ph = L*esc, P*esc
    s.append(f'<g transform="translate({px0},{py0})">')
    s.append(f'<rect x="0" y="0" width="{pw:.0f}" height="{ph:.0f}" fill="var(--wood)" '
             f'opacity=".45" stroke="var(--dim)" stroke-width="4"/>')
    if not f['fundo']:
        for dx, dy, r in ((pw/2,-40,0), (pw/2,ph+40,180), (-40,ph/2,270), (pw+40,ph/2,90)):
            s.append(f'<path d="M{dx:.0f} {dy:.0f} l-26 -22 h52 z" '
                     f'transform="rotate({r},{dx:.0f},{dy:.0f})" fill="var(--brand-deep)"/>')
        s.append(f'<text class="sbn" x="{pw+80:.0f}" y="{ph/2:.0f}" dominant-baseline="middle" '
                 f'font-size="50" fill="var(--brand-deep)">planta · acesso pelas 4 faces</text>')
    else:
        s.append(f'<rect x="0" y="-34" width="{pw:.0f}" height="26" fill="var(--no-tz)"/>')
        s.append(f'<path d="M{pw/2:.0f} {ph+40:.0f} l-26 -22 h52 z" fill="var(--brand-deep)"/>')
        s.append(f'<text class="sbn" x="{pw+80:.0f}" y="{ph/2:.0f}" dominant-baseline="middle" '
                 f'font-size="50" fill="var(--brand-deep)">planta · face unica · fundo fechado</text>')
    s.append(f'<text class="sbn" x="{pw/2:.0f}" y="{ph+96:.0f}" text-anchor="middle" '
             f'font-size="50" fill="var(--dim-t)">{L} × {P} mm</text>')
    s.append('</g></svg>')
    return '\n'.join(s), (L, P, A)

if __name__ == '__main__':
    out = pathlib.Path(__file__).resolve().parent / 'render'
    out.mkdir(exist_ok=True)
    for f in FAM:
        svg, (L, P, A) = draw(f)
        nome = f['familia'].replace(' ', '-')
        (out / f'pdv-fam-{nome}.svg').write_text(svg, encoding='utf-8')
        print(f"{f['familia']:20} {L:5} x {P:4} x {A:5} mm   painel {f['pan'][0]}x{f['pan'][1]}   "
              f"{len(svg)} bytes")
