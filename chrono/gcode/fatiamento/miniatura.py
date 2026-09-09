"""Injeta miniatura 230x110 PNG no formato que PrusaSlicer/Orca escrevem
   (; thumbnail begin LxA tamanho_base64) — e a Kobra 3 le."""
import base64, io, sys, pathlib
from PIL import Image
def bloco(png_path, W=230, H=110):
    im=Image.open(png_path).convert('RGB')
    im.thumbnail((W,H), Image.LANCZOS)
    cv=Image.new('RGB',(W,H),(243,245,245))
    cv.paste(im, ((W-im.width)//2, (H-im.height)//2))
    buf=io.BytesIO(); cv.save(buf,'PNG',optimize=True)
    b64=base64.b64encode(buf.getvalue()).decode()
    ls=['; thumbnail begin %dx%d %d'%(W,H,len(b64))]
    ls += ['; '+b64[i:i+76] for i in range(0,len(b64),76)]
    ls.append('; thumbnail end'); ls.append(';')
    return '\n'.join(ls)+'\n'
def injeta(gcode, png):
    p=pathlib.Path(gcode); L=p.read_text(errors='ignore').splitlines(keepends=True)
    if any('thumbnail begin' in l for l in L[:60]): print('  ja tem miniatura'); return
    L.insert(1, bloco(png)); p.write_text(''.join(L))
    print('  %-22s miniatura de %d bytes injetada'%(p.name, len(bloco(png))))
if __name__=='__main__':
    injeta(sys.argv[1], sys.argv[2])
