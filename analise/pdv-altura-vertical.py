import json
ENC,NOZ,PE=40.60,73.08,19.4
BAR={'BAL-02-AC':270,'BLA-03-AC':287,'PSC-01':315,'BPS-01':337,'PSA-02':346,
     'PSA-03':424,'PST-01':437,'PSA-04':474,'PSA-05':513}
ALVOS=[750,850,900,1000,1200,1400,1600,1800,2000,2200]
def alt(B,n): return n*NOZ+(n-1)*(B-2*ENC)+PE
def pitch(B): return (B-2*ENC)+NOZ

print("Qual barra vertical unica cobre melhor os padroes de PDV?")
print("(passo utilizavel p/ utilidade domestica: 250 a 450 mm)\n")
print(f"{'barra':11}{'B':>5}{'passo':>8}{'alturas de 2 a 8 niveis':>52}{'acertos':>9}")
res=[]
for r,B in sorted(BAR.items(), key=lambda kv:kv[1]):
    hs=[alt(B,n) for n in range(2,9)]
    hit=sum(1 for a in ALVOS if min(abs(a-h) for h in hs)/a <= 0.05)
    p=pitch(B)
    ok = 250 <= p <= 450
    lad=' '.join(f"{h:.0f}" for h in hs)
    print(f"{r:11}{B:5}{p:8.1f}{lad:>52}{hit:6}/10 {'' if ok else '  passo fora'}")
    if ok: res.append((hit,-abs(p-340),r,B,p,hs))
res.sort(reverse=True)
hit,_,r,B,p,hs = res[0]
print(f"\n>>> ESCOLHIDA: {r} ({B} mm) — passo de {p:.1f} mm, acerta {hit} dos 10 padroes\n")
print(f"{'niveis':>7}{'altura':>9}   padrao de PDV mais proximo")
NOME={750:'mesa de ilha baixa',850:'mesa de ilha alta',900:'balcao / checkout',
      1000:'ilha media',1200:'gondola central baixa',1400:'checkout c/ display',
      1600:'ponta de gondola media',1800:'ponta de gondola alta',
      2000:'gondola de parede',2200:'parede alta'}
esc=[]
for n,h in zip(range(2,9),hs):
    a=min(ALVOS, key=lambda a:abs(a-h)); e=(h-a)/a*100
    tag=f"{NOME[a]} ({a})  {e:+.1f}%" if abs(e)<=8 else "— fora dos padroes"
    print(f"{n:7}{h:9.0f}   {tag}")
    esc.append(dict(niveis=n, altura=round(h), padrao=NOME[a] if abs(e)<=8 else None,
                    alvo=a if abs(e)<=8 else None, erro_pct=round(e,1)))
json.dump(dict(barra=r,B=B,passo=round(p,1),escada=esc), open('vert.json','w'), ensure_ascii=False, indent=1)
