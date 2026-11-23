import csv, html, sys
L=["0001101","0011001","0010011","0111101","0100011","0110001","0101111","0111011","0110111","0001011"]
G=["0100111","0110011","0011011","0100001","0011101","0111001","0000101","0010001","0001001","0010111"]
R=["1110010","1100110","1101100","1000010","1011100","1001110","1010000","1000100","1001000","1110100"]
P=["LLLLLL","LLGLGG","LLGGLG","LLGGGL","LGLLGG","LGGLLG","LGGGLL","LGLGLG","LGLGGL","LGGLGL"]
def bits(e):
    p=P[int(e[0])];b="101"
    for i in range(1,7): b+=(L if p[i-1]=="L" else G)[int(e[i])]
    b+="01010"
    for i in range(7,13): b+=R[int(e[i])]
    return b+"101"
def svg(e,m=0.264,h=14):
    b=bits(e);q=9*m;r=[];i=0
    while i<95:
        if b[i]=="1":
            s=i
            while i<95 and b[i]=="1": i+=1
            g=s<=2 or 45<=s<=49 or s>=92
            r.append(f'<rect x="{q+s*m:.3f}" y="0" width="{(i-s)*m:.3f}" height="{h+(1.6 if g else 0)}"/>')
        else: i+=1
    W=q+95*m+7*m
    t=f'<text x="{q-0.4:.2f}" y="{h+2.6}" text-anchor="end">{e[0]}</text><text x="{q+24*m:.2f}" y="{h+2.6}" text-anchor="middle">{e[1:7]}</text><text x="{q+71*m:.2f}" y="{h+2.6}" text-anchor="middle">{e[7:]}</text>'
    return f'<svg width="{W:.2f}mm" height="{h+3.2}mm" viewBox="0 0 {W:.2f} {h+3.2}" style="font:2.3px monospace">{"".join(r)}{t}</svg>'
rows=list(csv.DictReader(open(sys.argv[1],encoding='utf-8'),delimiter=';'))
sec=sys.argv[2]; preco=sys.argv[3]=="1"
it=[r for r in rows if r['LINHA_PT']==sec][:9]
cards=""
for r in it:
    spec1="  ·  ".join(x for x in [" / ".join(x for x in [r['COR_PT'],r['COR_EN'],r['COR_ES']] if x), r['VOLUME'], r['TAMANHO']] if x)
    cards+=f'''<div class="c"><div class="f">SEM FOTO<br>{r['FOTO']}</div><div class="t"><b>{html.escape(r['NOME_PT'])}</b><i>{html.escape(r['NOME_EN'])}</i><i class="es">{html.escape(r['NOME_ES'])}</i><span>{html.escape(spec1)}</span><span>Ref. {r['REFERENCIA']}   ·   Cx {r['QTD_CAIXA']} un</span></div><div class="b">{svg(r['EAN13'])}</div>{f'<div class="p">{r["PRECO"]}</div>' if preco else ''}</div>'''
pg=f'''<html><head><meta charset="utf-8"><style>
@page{{size:210mm 297mm;margin:0}}body{{margin:0;font-family:Arial}}
.pg{{width:210mm;height:297mm;position:relative;background:#fff}}
.h{{position:absolute;top:0;left:0;right:0;height:22mm;background:#00406b;color:#fff;padding:7mm 12mm 0;box-sizing:border-box}}
.h b{{font-size:16pt;display:block}}.h i{{font-size:8pt}}
.g{{position:absolute;top:30mm;left:12mm;width:186mm;height:251mm;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:4mm}}
.c{{border:0.5pt solid #d9d9d9;position:relative}}
.f{{position:absolute;top:2mm;left:2mm;right:2mm;height:36mm;background:#eee;color:#888;font-size:6pt;display:flex;align-items:center;justify-content:center;text-align:center}}
.t{{position:absolute;top:40mm;left:3mm;right:3mm;font-size:6.2pt;line-height:1.15;color:#1a1a1a}}
.t b{{display:block;font-size:8pt;margin-bottom:.6mm}}.t i{{display:block;color:#737373}}.t .es{{margin-bottom:.8mm}}.t span{{display:block}}
.b{{position:absolute;bottom:3mm;left:1mm}}.p{{position:absolute;bottom:2.5mm;right:3mm;font-size:11pt;font-weight:bold;color:#00406b}}
.r{{position:absolute;bottom:5mm;left:12mm;right:12mm;font-size:6pt;color:#737373;display:flex;justify-content:space-between}}
</style></head><body><div class="pg"><div class="h"><b>{it[0]['LINHA_PT']}</b><i>{it[0]['LINHA_EN']}  ·  {it[0]['LINHA_ES']}</i></div><div class="g">{cards}</div>
<div class="r"><span>Nitron  ·  1</span><span>{'Preços da tabela padrão, sujeitos a alteração sem aviso prévio.' if preco else ''}</span></div></div></body></html>'''
open(sys.argv[4],'w',encoding='utf-8').write(pg)
