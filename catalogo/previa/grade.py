import csv, html, sys, json
exec(open('preview.py').read().split('def svg')[0])   # bits()
MOD=0.264
def svg(e,h):
    b=bits(e);q=9*MOD;r=[];i=0
    while i<95:
        if b[i]=="1":
            s=i
            while i<95 and b[i]=="1": i+=1
            g=s<=2 or 45<=s<=49 or s>=92
            r.append(f'<rect x="{q+s*MOD:.3f}" y="0" width="{(i-s)*MOD:.3f}" height="{h+(1.2 if g else 0):.2f}"/>')
        else: i+=1
    W=q+95*MOD+7*MOD; th=2.3
    t=(f'<text x="{q-0.35:.2f}" y="{h+th}" text-anchor="end">{e[0]}</text>'
       f'<text x="{q+24*MOD:.2f}" y="{h+th}" text-anchor="middle">{e[1:7]}</text>'
       f'<text x="{q+71*MOD:.2f}" y="{h+th}" text-anchor="middle">{e[7:]}</text>')
    return f'<svg width="{W:.2f}mm" height="{h+th+0.3:.2f}mm" viewBox="0 0 {W:.2f} {h+th+0.3:.2f}" style="font:400 2.1px Montserrat;display:block;flex-shrink:0">{"".join(r)}{t}</svg>'

rows=list(csv.DictReader(open('../saida/catalogo_indesign.csv',encoding='utf-8'),delimiter=';'))
PAGE_W,PAGE_H=210,297; ML,MR,MT,MB=12,12,30,16; GUT=4
AREA_W=PAGE_W-ML-MR; AREA_H=PAGE_H-MT-MB
# tamanhos de texto por opção
OPC={3:dict(rows=3,pt=7.5,lang=6,spec=6,price=11,bar=8),
     4:dict(rows=4,pt=6.5,lang=5.3,spec=5.3,price=9.5,bar=7),
     5:dict(rows=5,pt=6,lang=4.8,spec=4.8,price=8.5,bar=6.5)}
CSS='''@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
@page{size:210mm 297mm;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Montserrat,Arial;background:#fff}
.pg{width:210mm;height:297mm;position:relative;background:#fff;overflow:hidden;page-break-after:always}
.h{position:absolute;top:0;left:0;right:0;height:22mm;background:#00406b;color:#fff;padding:7mm 12mm 0}
.h b{font-weight:700;font-size:16pt;display:block;line-height:1}.h i{font-style:normal;font-size:8pt;opacity:.85}
.tag{position:absolute;top:7.5mm;right:12mm;color:#fff;font-size:7pt;text-align:right;line-height:1.3}
.g{position:absolute;display:grid}
.c{border:.5pt solid #d9d9d9;display:flex;flex-direction:column;padding:1.6mm;overflow:hidden}
.f{flex:1;background:#efefef;color:#999;display:flex;align-items:center;justify-content:center;text-align:center;font-size:5pt;min-height:0}
.t{margin-top:1.4mm;color:#1a1a1a;line-height:1.18}.t b{display:block;font-weight:700}.t .l{display:block;color:#7a7a7a}
.t .s{display:block}.ft{display:flex;align-items:flex-end;justify-content:space-between;margin-top:1.2mm;gap:1mm}
.p{font-weight:700;color:#00406b;white-space:nowrap;line-height:1}
.r{position:absolute;bottom:5mm;left:12mm;right:12mm;font-size:6pt;color:#7a7a7a;display:flex;justify-content:space-between}
.guides{position:absolute;top:0;left:0;width:210mm;height:297mm;pointer-events:none}'''
def page(cols,itens,preco,guias=False):
    o=OPC[cols]; nrows=o['rows']
    cw=(AREA_W-(cols-1)*GUT)/cols; ch=(AREA_H-(nrows-1)*GUT)/nrows
    narrow= cw<50
    cards=""
    for r in itens[:cols*nrows]:
        cor=" / ".join(x for x in [r['COR_PT'],r['COR_EN'],r['COR_ES']] if x)
        spec="  ·  ".join(x for x in [cor,r['VOLUME'],r['TAMANHO']] if x)
        p=f'<span class="p" style="font-size:{o["price"]}pt">{r["PRECO"]}</span>' if preco else '<span></span>'
        bar=svg(r['EAN13'],o['bar'])
        foot=(f'<div class="ft" style="flex-direction:column;align-items:stretch;gap:.8mm"><div style="text-align:right;min-height:{o["price"]*0.36:.1f}mm">{p}</div>{bar}</div>' if narrow
              else f'<div class="ft">{bar}{p}</div>')
        cards+=(f'<div class="c"><div class="f">FOTO<br>{r["FOTO"]}</div><div class="t">'
                f'<b style="font-size:{o["pt"]}pt">{html.escape(r["NOME_PT"])}</b>'
                f'<span class="l" style="font-size:{o["lang"]}pt">{html.escape(r["NOME_EN"])}</span>'
                f'<span class="l" style="font-size:{o["lang"]}pt;margin-bottom:.6mm">{html.escape(r["NOME_ES"])}</span>'
                f'<span class="s" style="font-size:{o["spec"]}pt">{html.escape(spec)}</span>'
                f'<span class="s" style="font-size:{o["spec"]}pt">Ref. {r["REFERENCIA"]} · Cx {r["QTD_CAIXA"]} un</span></div>{foot}</div>')
    g=f'<div class="g" style="top:{MT}mm;left:{ML}mm;width:{AREA_W}mm;height:{AREA_H}mm;grid-template-columns:repeat({cols},1fr);grid-template-rows:repeat({nrows},1fr);gap:{GUT}mm">{cards}</div>'
    gd=guides(cols,nrows) if guias else ""
    rod='Preços da tabela padrão, sujeitos a alteração sem aviso prévio.' if preco else ''
    return (f'<div class="pg"><div class="h"><b>{itens[0]["LINHA_PT"]}</b><i>{itens[0]["LINHA_EN"]}  ·  {itens[0]["LINHA_ES"]}</i></div>'
            f'<div class="tag">{cols} por linha · {cols*nrows} por página<br>card {cw:.1f} × {ch:.1f} mm · {"com" if preco else "sem"} preço</div>'
            f'{g}{gd}<div class="r"><span>Nitron  ·  {cols}</span><span>{rod}</span></div></div>')
def guides(cols,nrows):
    # grade mestra de 60 colunas (desenha só as linhas que dividem cards nesta opção) + margens
    s=[f'<rect x="{ML}" y="{MT}" width="{AREA_W}" height="{AREA_H}" fill="none" stroke="#e5007e" stroke-width=".25"/>']
    cw=(AREA_W-(cols-1)*GUT)/cols
    for k in range(cols):
        x=ML+k*(cw+GUT)
        s.append(f'<rect x="{x:.2f}" y="{MT}" width="{cw:.2f}" height="{AREA_H}" fill="#7c4dff" fill-opacity=".10" stroke="#7c4dff" stroke-width=".25"/>')
    return f'<svg class="guides" viewBox="0 0 210 297">{"".join(s)}</svg>'

# diagrama do grid mestre: 60 colunas -> 3/4/5
def diagrama():
    col=(AREA_W-59*1.0)/60  # 60 colunas com medianiz de 1mm? só ilustrativo: usamos medianiz de cards = 4mm
    out='<div class="pg"><div class="h"><b>Grade do projeto</b><i>Uma grade que aceita 3, 4 e 5 produtos por linha</i></div>'
    out+=f'<div style="position:absolute;top:30mm;left:12mm;right:12mm;font-size:8pt;line-height:1.45;color:#1a1a1a">'
    out+='''<p style="margin:0 0 3mm"><b>Área útil:</b> A4 (210 × 297 mm), margens 12 mm nas laterais, 30 mm no topo (faixa de título de 22 mm) e 16 mm na base.
    Largura útil <b>186 mm</b>, medianiz (espaço entre cards) <b>4 mm</b> em todas as opções.</p>
    <p style="margin:0 0 4mm">3, 4 e 5 só dividem juntos o número <b>60</b> (o menor múltiplo comum). Por isso há dois caminhos:</p></div>'''
    y=58
    for cols,nrows in ((3,3),(4,4),(5,5)):
        cw=(AREA_W-(cols-1)*GUT)/cols
        out+=f'<div style="position:absolute;top:{y}mm;left:12mm;font-size:8pt;font-weight:700">{cols} por linha — card {cw:.2f} mm, ocupa {60//cols} das 60 colunas</div>'
        bars=""
        for k in range(cols):
            x=k*(cw+GUT)
            bars+=f'<rect x="{x:.2f}" y="0" width="{cw:.2f}" height="10" fill="#00406b" fill-opacity=".85"/><text x="{x+cw/2:.2f}" y="6.3" fill="#fff" font-size="3" text-anchor="middle" font-family="Montserrat" font-weight="700">{cw:.1f} mm</text>'
        out+=f'<svg style="position:absolute;top:{y+4}mm;left:12mm" width="186mm" height="10mm" viewBox="0 0 186 10">{bars}</svg>'
        y+=20
    out+='''<div style="position:absolute;top:120mm;left:12mm;right:12mm;font-size:8pt;line-height:1.45;color:#1a1a1a">
    <p style="margin:0 0 2mm"><b>Caminho A — três páginas-mestre (recomendado).</b> Mesmas margens e mesma medianiz de 4 mm; o que muda é o número de colunas da mestra:</p>
    <table style="border-collapse:collapse;font-size:7.5pt;margin-bottom:4mm">
    <tr style="background:#00406b;color:#fff"><th style="padding:1mm 3mm;text-align:left">Página-mestre</th><th style="padding:1mm 3mm">Colunas</th><th style="padding:1mm 3mm">Medianiz</th><th style="padding:1mm 3mm">Largura do card</th><th style="padding:1mm 3mm">Linhas</th><th style="padding:1mm 3mm">Produtos/página</th></tr>
    <tr><td style="padding:1mm 3mm">A-3 por linha</td><td align=center>3</td><td align=center>4 mm</td><td align=center>59,33 mm</td><td align=center>3</td><td align=center>9</td></tr>
    <tr style="background:#f2f2f2"><td style="padding:1mm 3mm">B-4 por linha</td><td align=center>4</td><td align=center>4 mm</td><td align=center>43,50 mm</td><td align=center>4</td><td align=center>16</td></tr>
    <tr><td style="padding:1mm 3mm">C-5 por linha</td><td align=center>5</td><td align=center>4 mm</td><td align=center>34,00 mm</td><td align=center>5</td><td align=center>25</td></tr></table>
    <p style="margin:0 0 2mm">Na prática: cada seção do catálogo usa a mestra que combina com ela (Teca e Nitron Mob em 3, potes e organização em 4 ou 5), e trocar de grade é só aplicar outra mestra. O script cria as três mestras; a grade de cada seção vem da coluna POR_LINHA de linhas.csv (Teca e Nitron Mob já estão em 3), e as demais usam a que você escolher ao rodar.</p>
    <p style="margin:0 0 2mm"><b>Caminho B — uma grade única de 60 colunas.</b> É o único número que 3, 4 e 5 dividem juntos, mas o espaço entre cards passa a ser o espaço entre colunas da grade: para 60 colunas caberem em 186 mm ele fica em ~0,8 mm (coluna de 2,3 mm). Os 4 mm de respiro somem, e as guias ficam densas demais para diagramar à mão. Só vale se vocês quiserem misturar 3, 4 e 5 na <b>mesma página</b>.</p>
    <p style="margin:0 0 2mm"><b>Linhas horizontais:</b> a altura do card sai da divisão da altura útil (251 mm) pelo número de linhas. Com 4 mm entre linhas: 3 linhas = 80,3 mm · 4 linhas = 59,8 mm · 5 linhas = 47,0 mm.</p>
    <p style="margin:0"><b>Código de barras mais baixo:</b> mantive a largura mínima recomendada (80%: 29,8 mm com as margens de silêncio, que não podem ser cortadas) e baixei só a altura: 8 mm (3/linha), 7 mm (4/linha), 6,5 mm (5/linha), contra 22,85 mm do tamanho nominal. Em embalagem que passa no caixa não se corta a altura; num catálogo, sim — mas imprimam e testem a leitura antes de rodar.</p></div></div>'''
    return out
pot=[r for r in rows if r['LINHA_PT']=='Potes']
pages=[diagrama()]
for c in (3,4,5):
    pages.append(page(c,pot,True)); pages.append(page(c,pot,False))
pages.append(page(4,pot,True,guias=True))
open('grades.html','w',encoding='utf-8').write(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
print(len(pages))
