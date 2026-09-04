#!/usr/bin/env python3
"""Elevacoes frontais cotadas das 4 familias de PDV — Rev. 2.

Rev. 2: pilha de baias de altura mista (uma ripa vertical por baia) e coroa em
peca L no topo, que da altura sem somar prateleira.

Gera analise/render/pdv-fam-<FAMILIA>.svg — SVG inline, sem dependencia externa,
usando as variaveis CSS do caderno (--wood, --no-tz, --dim...) para acompanhar
o tema claro/escuro do documento que o embute.

Cotas conforme analise/11-nitron-mob-cota-final.md.
"""
import pathlib

ENC, NOX, NOXC, NOL, NOY, NOZ = 40.60, 61.61, 101.30, 83.23, 83.23, 73.08
PE = 60 - ENC
SOL = NOL - NOX          # 21,62 mm que a coroa passa da estrutura, por lado
V  = '#08a9b1'
CONSOME = 2*ENC

ext_comp = lambda B, N: 2*NOX + (N-1)*NOXC + N*(B-CONSOME)
ext_prof = lambda B:    B + 2*(NOY-ENC)
passo_x  = lambda B:    B + NOXC - CONSOME

FAM = [
  dict(familia='CHECKOUT',         bc=415, bl=287, pan=(300,450), N=2,
       pilha=[270,270,270,270], coroa=270, ganch=True,
       fundo=False, deck=True,  casinha=False, capsula=True),
  dict(familia='ILHA',             bc=595, bl=415, pan=(460,634), N=2,
       pilha=[270,270,270], coroa=None, ganch=False,
       fundo=False, deck=True,  casinha=False, capsula=True),
  dict(familia='PONTA DE GONDOLA', bc=595, bl=287, pan=(300,634), N=2,
       pilha=[270,270,270,270,270], coroa=513, ganch=False,
       fundo=True,  deck=False, casinha=True,  capsula=True),
  dict(familia='PAREDAO',          bc=717, bl=287, pan=(300,754), N=4,
       pilha=[270]*7, coroa=None, ganch=False,
       fundo=True,  deck=False, casinha=False, capsula=False),
]

def nos(f):
    """Nos de baixo para cima: (zb, zt, e_coroa)."""
    ripas = list(f['pilha']) + ([f['coroa']] if f['coroa'] else [])
    out, z = [], PE
    for i in range(len(ripas)+1):
        out.append((z, z+NOZ, bool(f['coroa']) and i == len(ripas)))
        if i < len(ripas):
            z = z + NOZ + (ripas[i] - CONSOME)
    return out

def draw(f):
    B, N = f['bc'], f['N']
    ns = nos(f)
    nprat = len(f['pilha']) + 1
    L = round(ext_comp(B, N)); P = round(ext_prof(f['bl'])); A = round(ns[-1][1])
    Lc = L + 2*SOL if f['coroa'] else L
    dx = SOL if f['coroa'] else 0
    PX = passo_x(B)
    cab = int(0.13*A/10)*10
    fh  = int(0.22*L) if f['casinha'] else 0
    catb = 120 if f['familia'] == 'PAREDAO' else 0
    ml, mr, mt, mb = 250+dx, 820+dx, 70+cab+fh+40+catb, 300
    W, H = L+ml+mr, A+mt+mb
    Y = lambda z: A - z

    s = [f'<svg viewBox="{-ml} {-mt} {W} {H}" role="img" aria-label="Elevacao frontal cotada: '
         f'{f["familia"]}, {L} por {P} por {A} milimetros, {N} vaos, {nprat} prateleiras'
         + (' e coroa em peca L' if f['coroa'] else '') + '">']
    ty = -(cab+40)

    def lead(y, txt, col='var(--dim-t)'):
        return (f'<path d="M{L+24} {y:.0f} H{L+96}" stroke="var(--dim)" stroke-width="4" fill="none"/>'
                f'<text class="sbn" x="{L+112}" y="{y:.0f}" dominant-baseline="middle" '
                f'font-size="50" fill="{col}">{txt}</text>')

    if f['casinha']:
        s.append(f'<path d="M{-dx:.0f} {ty} L{L/2:.0f} {ty-fh} L{L+dx:.0f} {ty} Z" fill="{V}"/>')
        s.append(lead(ty-fh/2, f'casinha · frontao {fh} mm', 'var(--brand-deep)'))
    s.append(f'<rect x="{-dx:.0f}" y="{ty}" width="{Lc:.0f}" height="{cab}" fill="{V}"/>')
    s.append(f'<text class="sbn" x="{L/2:.0f}" y="{ty+cab*0.56:.0f}" text-anchor="middle" '
             f'font-size="{cab*0.44:.0f}" fill="#fff">NITRON</text>')
    s.append(f'<text class="sal" x="{L/2:.0f}" y="{ty+cab*0.87:.0f}" text-anchor="middle" '
             f'font-size="{cab*0.19:.0f}" fill="#fff">toda casa tem</text>')
    s.append(lead(ty+cab/2, f'cabeceira {cab} mm' + (f' · {Lc:.0f} mm de largura' if f['coroa'] else '')))

    if catb:
        for i in range(N):
            x = NOX+i*PX+10
            s.append(f'<rect x="{x:.0f}" y="{ty-108}" width="{min(PX-40,L-x-10):.0f}" '
                     f'height="92" fill="{V}" rx="10"/>')
        s.append(lead(ty-62, 'faixa de categoria 90 mm'))

    if f['fundo']:
        for b in range(len(f['pilha'])):
            y0, y1 = Y(ns[b+1][0]), Y(ns[b][1])
            s.append(f'<rect x="{NOX}" y="{y0:.0f}" width="{L-2*NOX:.0f}" height="{y1-y0:.0f}" '
                     f'fill="var(--wood)" opacity=".28"/>')
        s.append(lead((Y(ns[-1][0])+Y(ns[0][1]))/2, 'painel de fundo · corte dedicado por baia'))

    for k in range(nprat):
        yc = Y(ns[k][0] + NOZ/2)
        deck = f['deck'] and k == nprat-1
        h = 40 if deck else 28
        s.append(f'<rect x="0" y="{yc-h/2:.0f}" width="{L}" height="{h}" '
                 f'fill="{"var(--wood2)" if deck else "var(--wood)"}"/>')
        for i in range(N):
            x0 = NOX+i*PX+12; w = min(PX-44, L-x0-12)
            s.append(f'<rect x="{x0:.0f}" y="{yc+16:.0f}" width="{w:.0f}" height="40" '
                     f'fill="{V}" opacity=".92"/>')
    if f['deck']: s.append(lead(Y(ns[nprat-1][0]+NOZ/2), 'top deck · painel inteiro', 'var(--brand-deep)'))
    s.append(lead(Y(ns[0][0]+NOZ/2)+36, 'faixa de preco 40 mm'))

    # montantes e nos
    for i in range(N+1):
        borda = (i == 0 or i == N)
        x = 0 if i == 0 else (L-NOX if i == N else NOX+i*PX-NOXC)
        w = NOX if borda else NOXC
        s.append(f'<rect x="{x:.0f}" y="{Y(ns[-1][1]):.0f}" width="{w:.0f}" '
                 f'height="{Y(PE)-Y(ns[-1][1]):.0f}" fill="var(--wood2)"/>')
        for (zb, zt, cor) in ns:
            if cor and borda:
                cx, cw, col = (-SOL if i == 0 else L-NOX-SOL), NOL, 'var(--brand-deep)'
            else:
                cx, cw = x, w
                col = 'var(--no-tz)' if borda else 'var(--no-cz)'
            s.append(f'<rect x="{cx:.0f}" y="{Y(zt):.0f}" width="{cw:.0f}" '
                     f'height="{NOZ:.0f}" fill="{col}"/>')
        s.append(f'<rect x="{x+w/2-16:.0f}" y="{Y(PE):.0f}" width="32" height="{PE}" fill="var(--wood2)"/>')
    if N > 1: s.append(lead(Y(ns[1][0]+NOZ/2), 'cruzeta · no de meio de vao', 'var(--brand-deep)'))

    # coroa: peca L + ripa atravessada + ganchos
    if f['coroa']:
        yk = Y(ns[-1][0] + NOZ/2)
        s.append(f'<rect x="{-SOL:.0f}" y="{yk-13:.0f}" width="{Lc:.0f}" height="26" fill="var(--wood2)"/>')
        s.append(lead(Y(ns[-1][1])+NOZ/2,
                      f'coroa · peca L fecha o poste · +{SOL:.2f} mm por lado', 'var(--brand-deep)'))
        if f['ganch']:
            yg = Y(ns[-1][0])
            s.append(f'<rect x="{NOX}" y="{yg+34:.0f}" width="{L-2*NOX:.0f}" height="22" fill="var(--no-tz)"/>')
            for i in range(int((L-2*NOX)//110)):
                hx = NOX+55+i*110
                s.append(f'<path d="M{hx:.0f} {yg+56:.0f} v46 a15 15 0 0 0 30 0" '
                         f'stroke="var(--no-tz)" stroke-width="7" fill="none"/>')
            s.append(lead(yg+80, f'gancheira · ripa {B} + porta-hastes', 'var(--brand-deep)'))

    # capsula de ativacao na baia mais alta sem gancheira
    if f['capsula']:
        lim = len(f['pilha']) if (f['coroa'] and f['ganch']) else len(f['pilha'])+(1 if f['coroa'] else 0)
        iv, melhor = 0, 0
        for v in range(lim):
            alt = ns[v+1][0]-ns[v][1]
            if alt >= melhor: melhor, iv = alt, v
        cw = min(380, L*0.42); cx = (L-cw)/2
        yv = (Y(ns[iv+1][0])+Y(ns[iv][1]))/2 - 36
        s.append(f'<rect x="{cx:.0f}" y="{yv:.0f}" width="{cw:.0f}" height="72" rx="36" fill="{V}"/>')
        s.append(f'<text class="sbn" x="{L/2:.0f}" y="{yv+50:.0f}" text-anchor="middle" '
                 f'font-size="44" fill="#fff">LEVE MAIS</text>')

    # placa lateral na baia de baixo
    plw = min(PX-70, 340); plh = min(ns[1][0]-ns[0][1]-30, 215)
    if plh > 70 and plw > 110:
        pyt = Y(ns[0][1])-plh-14; pxc = NOX+22+plw/2
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
    s.append(dv(-70-dx, ty-fh, A, f'{A+cab+40+fh} mm total'))
    s.append(dv(-176-dx, Y(ns[1][0]), Y(ns[0][0]), f'passo {ns[1][0]-ns[0][0]:.0f}'))
    if f['coroa']:
        s.append(dv(-282-dx, Y(ns[-1][0]), Y(ns[-2][0]), f'coroa {ns[-1][0]-ns[-2][0]:.0f}'))

    px0, py0, esc = 0, A+330, 0.42
    pw, ph = L*esc, P*esc
    s.append(f'<g transform="translate({px0},{py0})">')
    s.append(f'<rect x="0" y="0" width="{pw:.0f}" height="{ph:.0f}" fill="var(--wood)" '
             f'opacity=".45" stroke="var(--dim)" stroke-width="4"/>')
    if not f['fundo']:
        for ax, ay, r in ((pw/2,-40,0), (pw/2,ph+40,180), (-40,ph/2,270), (pw+40,ph/2,90)):
            s.append(f'<path d="M{ax:.0f} {ay:.0f} l-26 -22 h52 z" '
                     f'transform="rotate({r},{ax:.0f},{ay:.0f})" fill="var(--brand-deep)"/>')
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
    return '\n'.join(s), (L, P, A, nprat)

if __name__ == '__main__':
    out = pathlib.Path(__file__).resolve().parent / 'render'
    out.mkdir(exist_ok=True)
    for f in FAM:
        svg, (L, P, A, npr) = draw(f)
        nome = f['familia'].replace(' ', '-')
        (out / f'pdv-fam-{nome}.svg').write_text(svg, encoding='utf-8')
        cor = f'coroa {f["coroa"]}' if f['coroa'] else 'sem coroa'
        print(f"{f['familia']:20} {L:5} x {P:4} x {A:5} mm   painel {f['pan'][0]}x{f['pan'][1]}   "
              f"{npr} prat · {cor:11} {len(svg)} bytes")
