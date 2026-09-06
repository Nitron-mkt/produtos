import sys, os, json, struct, math
sys.path.insert(0, "/home/user/produtos/design/modula")
os.chdir("/home/user/produtos/design/modula")
import numpy as np
from PIL import Image
import modelo, render as R
from modelo import ficha
from exporta import paleta, COR_CORPO
SAIDA = "out"

# ---------------- GLB (glTF 2.0 binario) ----------------
def glb(malha, caminho, nome="MODULA", cor=(0.77, 0.29, 0.14)):
    """Y para cima, escala em metros — e assim que os visualizadores de
    celular esperam receber."""
    pos, nor = [], []
    ns = malha.normais_suaves(42)
    for (a, b, c, _), n3 in zip(malha.tris, ns):
        for v, nv in zip((a, b, c), n3):
            pos += [v[0] / 1000.0, v[2] / 1000.0, -v[1] / 1000.0]
            nor += [nv[0], nv[2], -nv[1]]
    P = np.array(pos, dtype="<f4"); N = np.array(nor, dtype="<f4")
    nv = len(P) // 3
    bp, bn = P.tobytes(), N.tobytes()
    while len(bp) % 4: bp += b"\0"
    binario = bp + bn
    while len(binario) % 4: binario += b"\0"
    mn = [float(P[0::3].min()), float(P[1::3].min()), float(P[2::3].min())]
    mx = [float(P[0::3].max()), float(P[1::3].max()), float(P[2::3].max())]
    j = {
      "asset": {"version": "2.0", "generator": "Nitron MODULA"},
      "scene": 0, "scenes": [{"nodes": [0]}],
      "nodes": [{"mesh": 0, "name": nome}],
      "meshes": [{"name": nome, "primitives": [
          {"attributes": {"POSITION": 0, "NORMAL": 1}, "material": 0, "mode": 4}]}],
      "materials": [{"name": "PP", "doubleSided": True, "pbrMetallicRoughness": {
          "baseColorFactor": [cor[0], cor[1], cor[2], 1.0],
          "metallicFactor": 0.0, "roughnessFactor": 0.62}}],
      "accessors": [
          {"bufferView": 0, "componentType": 5126, "count": nv, "type": "VEC3",
           "min": mn, "max": mx},
          {"bufferView": 1, "componentType": 5126, "count": nv, "type": "VEC3"}],
      "bufferViews": [
          {"buffer": 0, "byteOffset": 0, "byteLength": len(bp), "target": 34962},
          {"buffer": 0, "byteOffset": len(bp), "byteLength": len(bn), "target": 34962}],
      "buffers": [{"byteLength": len(binario)}],
    }
    jb = json.dumps(j, separators=(",", ":")).encode()
    while len(jb) % 4: jb += b" "
    total = 12 + 8 + len(jb) + 8 + len(binario)
    with open(caminho, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, total))
        f.write(struct.pack("<II", len(jb), 0x4E4F534A)); f.write(jb)
        f.write(struct.pack("<II", len(binario), 0x004E4942)); f.write(binario)
    return nv // 3, os.path.getsize(caminho)

# ---------------- giro em GIF ----------------
def giro(k, quadros=30, lado=560, nome="out/modula-M-giro.gif"):
    sol, s = ficha(k)
    ns = sol.normais_suaves(42)
    ims = []
    for q in range(quadros):
        az = 360.0 * q / quadros
        im = R.cena([(sol.triangulos(), paleta(COR_CORPO[k]), ns)],
                    lado, lado, az=az, el=16)
        ims.append(im.convert("P", palette=Image.ADAPTIVE, colors=64))
    ims[0].save(nome, save_all=True, append_images=ims[1:],
                duration=90, loop=0, optimize=True)
    return os.path.getsize(nome)

# ---------------- prancha de vistas ----------------
def prancha(k, nome=None):
    nome = nome or f"{SAIDA}/modula-{k}-vistas.png"
    sol, s = ficha(k)
    ns = sol.normais_suaves(42)
    g = lambda: (sol.triangulos(), paleta(COR_CORPO[k]), ns)
    W, H = 760, 620
    vistas = [("PERSPECTIVA", 38, 16), ("FRENTE", 0, 0), ("LATERAL", 90, 0),
              ("SUPERIOR", 0, 89), ("3/4 TRASEIRA", 218, 20), ("RASANTE", 55, 4)]
    tiles = []
    for rot, az, el in vistas:
        im = R.cena([g()], W, H, az=az, el=el)
        tiles.append((rot, im))
    fundo = (246, 244, 239)
    from PIL import ImageDraw, ImageFont
    def fonte(px):
        for c in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            try: return ImageFont.truetype(c, px)
            except Exception: pass
        return ImageFont.load_default()
    f_tit, f_rot = fonte(40), fonte(22)
    topo = 116
    # A cota vem SEMPRE da malha de producao, nunca de arquivo a parte: a
    # prancha ja saiu uma vez com a massa da revisao anterior no cabecalho.
    amostra = modelo.AMOSTRA
    modelo.AMOSTRA = [2.6, 14]
    _, fp = ficha(k)
    modelo.AMOSTRA = amostra
    FIC = dict(X=fp["X"], Y=fp["Y"], H=fp["H"],
               L=fp["litros_total"], g=fp["massa_g"])
    folha = Image.new("RGB", (W*3, H*2 + topo + 40), fundo)
    d = ImageDraw.Draw(folha)
    d.text((26, 20), f"MODULA {k}", fill=(19, 30, 41), font=f_tit)
    d.text((26 + d.textlength(f"MODULA {k}", font=f_tit) + 26, 30),
           f"{FIC['X']/10:.1f} x {FIC['Y']/10:.1f} x {FIC['H']/10:.1f} cm    "
           f"{FIC['L']:.1f} L    {FIC['g']:.0f} g".replace(".", ","),
           fill=(94, 107, 112), font=f_rot)
    d.line([(0, topo-40), (W*3, topo-40)], fill=(19, 30, 41), width=3)
    for i, (rot, im) in enumerate(tiles):
        x, y = (i % 3)*W, (i//3)*(H+34) + topo + 6
        folha.paste(im, (x, y))
        d.text((x+22, y-28), rot, fill=(30, 167, 172), font=f_rot)
    folha = folha.crop((0, 0, W*3, topo + 6 + 2*(H+34)))
    folha.save(nome)
    return os.path.getsize(nome)

if __name__ == "__main__":
    modelo.AMOSTRA = [4.6, 9]           # malha media: leve para celular
    for k in ("P", "M", "G"):
        sol, s = ficha(k)
        n, tam = glb(sol, f"{SAIDA}/modula-{k}.glb", s["nome"],
                     tuple(c/255 for c in COR_CORPO[k]))
        print(f"  GLB {k}: {n} tri, {tam/1e6:.2f} MB")
    modelo.AMOSTRA = [3.4, 10]
    print(f"  prancha: {prancha('M')/1e6:.2f} MB")
    modelo.AMOSTRA = [4.6, 9]
    print(f"  giro: {giro('M')/1e6:.2f} MB")
