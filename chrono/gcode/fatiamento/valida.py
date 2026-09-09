import re, glob, os
def check(fn):
    txt=open(fn,errors='ignore').read()
    body=txt.split('; ---- fim ----')[0]          # exclui o end_gcode
    X=[];Y=[];Zl=set(); zmax=-1e9; zmin=1e9
    for ln in body.splitlines():
        if not (ln.startswith('G1 ') or ln.startswith('G0 ')): continue
        d={t[0]:t[1:] for t in ln.split()[1:] if t and t[0] in 'XYZE'}
        if 'X' in d:
            try: X.append(float(d['X']))
            except: pass
        if 'Y' in d:
            try: Y.append(float(d['Y']))
            except: pass
        if 'Z' in d:
            try:
                z=float(d['Z']); zmax=max(zmax,z); zmin=min(zmin,z)
            except: pass
    Zl={float(m) for m in re.findall(r'^;Z:([\d.]+)', body, re.M)}
    g=lambda p: (re.search(p,txt).group(1) if re.search(p,txt) else '?')
    objs=sorted(set(re.findall(r'; printing object (\S+)', txt)))
    print('=== %-22s %6.2f MB'%(os.path.basename(fn), os.path.getsize(fn)/1e6))
    print('    mesa: X %.1f..%.1f  Y %.1f..%.1f   ->  %s'%(min(X),max(X),min(Y),max(Y),
          'DENTRO de 220x220' if (min(X)>=0 and max(X)<=220 and min(Y)>=0 and max(Y)<=220) else '*** FORA DA MESA ***'))
    print('    Z: %.2f .. %.2f   camadas: %d   1a camada: %s'%(zmin,zmax,len(Zl), min(Zl) if Zl else '?'))
    print('    bico %s C / mesa %s C   |  %s mm de filamento = %s g'%(
          g(r'; first_layer_temperature = (\d+)'), g(r'; first_layer_bed_temperature = (\d+)'),
          g(r'; filament used \[mm\] = ([\d.]+)'), g(r'; total filament used \[g\] = ([\d.]+)')))
    print('    tempo estimado: %s   |  objetos: %s'%(g(r'; estimated printing time \(normal mode\) = (.+)'), ', '.join(objs)))
    assert zmin>=0, 'Z negativo!'
for f in sorted(glob.glob('out/*.gcode')): check(f)
