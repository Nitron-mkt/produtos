import re, glob, os, base64, io
from collections import Counter
from PIL import Image
BEDX=BEDY=255.0
for fn in sorted(glob.glob('k3/*.gcode')):
    txt=open(fn,errors='ignore').read()
    body=txt.split('; ---- fim ----')[0]
    X=[];Y=[];zmax=-1e9;zmin=1e9
    for ln in body.splitlines():
        if ln[:3] not in ('G1 ','G0 '): continue
        for t in ln.split()[1:]:
            if t[:1] in 'XYZ':
                try: v=float(t[1:])
                except: continue
                if t[0]=='X': X.append(v)
                elif t[0]=='Y': Y.append(v)
                else: zmax=max(zmax,v); zmin=min(zmin,v)
    Zl={float(m) for m in re.findall(r'^;Z:([\d.]+)',body,re.M)}
    cmds=Counter(m for m in re.findall(r'^([GM]\d+)',txt,re.M))
    g=lambda p:(re.search(p,txt).group(1) if re.search(p,txt) else '?')
    # miniatura
    mb=re.search(r'; thumbnail begin (\d+)x(\d+) (\d+)\n((?:; .*\n)+?); thumbnail end', txt)
    mini='ausente'
    if mb:
        b64=''.join(l[2:] for l in mb.group(4).splitlines())
        ok = len(b64)==int(mb.group(3))
        try:
            im=Image.open(io.BytesIO(base64.b64decode(b64))); mini='%s %s (base64 %s)'%(mb.group(1)+'x'+mb.group(2), im.format, 'confere' if ok else 'TAMANHO ERRADO')
        except Exception as e: mini='ILEGIVEL: %s'%e
    objs=sorted(set(re.findall(r'; printing object (\S+)',txt)))
    print('=== %-22s %5.2f MB'%(os.path.basename(fn), os.path.getsize(fn)/1e6))
    print('    G9111 presente:      %s'%('SIM  ->  '+g(r'(G9111 [^\n]+)') if 'G9111' in txt else '*** NAO ***'))
    print('    mesa 255x255:        X %.1f..%.1f  Y %.1f..%.1f  -> %s'%(min(X),max(X),min(Y),max(Y),
          'DENTRO' if (min(X)>=0 and max(X)<=BEDX and min(Y)>=0 and max(Y)<=BEDY) else '*** FORA ***'))
    print('    Z %.2f..%.2f   camadas %d   1a camada %.2f'%(zmin,zmax,len(Zl),min(Zl)))
    print('    miniatura:           %s'%mini)
    print('    %s mm de filamento = %s g   |  %s'%(g(r'; filament used \[mm\] = ([\d.]+)'),
          g(r'; total filament used \[g\] = ([\d.]+)'), g(r'; estimated printing time \(normal mode\) = (.+)')))
    print('    objetos:             %s'%', '.join(objs))
    print('    comandos usados:     %s'%'  '.join('%s×%d'%(k,v) for k,v in sorted(cmds.items())))
    print()
