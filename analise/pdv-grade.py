import json
ENC,NOX,NOXC,NOY,NOZ = 40.60,61.61,101.30,83.23,73.08
PE=19.4
BAR={'BPS-01-AC':167,'BCO-01-AC':180,'BAL-01-AC':183,'BLA-01-AC':200,'BLA-02-AC':207,
     'BAL-02-AC':270,'BLA-03-AC':287,'PSC-01':315,'BPS-01':337,'PSA-02':346,'PSC-02':415,
     'PSA-03':424,'PST-01':437,'PSA-04':474,'PSA-05':513,'PSC-03':595,'PST-02':617,
     'PSA-01':654,'PSC-04':717}
LARG = {'SAPATEIRA':('PSC-02',415),'MULTIUSO':('PSC-03',595),'ARARA':('PSC-04',717)}

def corrida(B,N): return 2*NOX+(N-1)*NOXC+N*(B-2*ENC)
def prof(B):      return B+2*(NOY-ENC)
def alt(B,n):     return n*NOZ+(n-1)*(B-2*ENC)+PE
def passo(B):     return B+20.1

print("="*88); print("1. AS TRES LARGURAS FIXAS  (barra PSC = campo COMPRIMENTO do cadastro)"); print("="*88)
print(f"{'referencia':12}{'barra':9}{'B':>5}{'1 vao':>9}{'passo':>9}   corrida = N vaos")
for k,(r,B) in LARG.items():
    lad=' · '.join(f"{corrida(B,N):.0f}" for N in range(1,7))
    print(f"{k:12}{r:9}{B:5}{corrida(B,1):9.0f}{passo(B):9.1f}   {lad}")

print("\n"+"="*88); print("2. COMPRIMENTO (a corrida) — modular por N vaos, nada de barra nova"); print("="*88)
print(f"{'N vaos':>7}" + "".join(f"{k:>14}" for k in LARG))
for N in range(1,8):
    print(f"{N:7}" + "".join(f"{corrida(B,N):13.0f} " for r,B in LARG.values()))
print(f"{'trizetas':>7}" + "".join(f"{'4 / nivel':>14}" for k in LARG))
print(f"{'cruzetas':>7}" + "".join(f"{'2(N-1)/niv':>14}" for k in LARG))

print("\n"+"="*88); print("3. PROFUNDIDADE — modular, escolha livre entre os 19 PIs de barra"); print("="*88)
for r,B in sorted(BAR.items(), key=lambda kv:kv[1]):
    print(f"   {r:12} {B:4} mm  ->  {prof(B):7.1f} mm externo")

print("\n"+"="*88); print("4. ALTURA — modular, cruzada com os padroes de PDV do mercado"); print("="*88)
PADROES=[('Mesa de ilha / display baixo',750),('Mesa de ilha alta',850),
         ('Balcao / checkout (altura de balcao)',900),('Ilha media',1000),
         ('Gondola central baixa',1200),('Checkout com display / ilha alta',1400),
         ('Ponta de gondola media',1600),('Ponta de gondola alta',1800),
         ('Gondola de parede',2000),('Parede alta',2200)]
print(f"{'padrao de mercado':38}{'alvo':>6}{'barra':>11}{'niveis':>8}{'altura':>9}{'erro':>8}{'passo':>8}")
alturas={}
for nome,alvo in PADROES:
    best=[]
    for r,B in BAR.items():
        for n in range(2,9):
            best.append((abs(alt(B,n)-alvo), r,B,n,alt(B,n)))
    best.sort(); d,r,B,n,A=best[0]
    print(f"{nome:38}{alvo:6}{r:>11}{n:8}{A:9.0f}{A-alvo:+8.0f}{(B-2*ENC)+NOZ:8.1f}")
    alturas[nome]=dict(alvo=alvo, barra=r, B=B, niveis=n, altura=round(A), passo=round((B-2*ENC)+NOZ,1))
json.dump(dict(larg={k:{'barra':v[0],'B':v[1],'corridas':[round(corrida(v[1],N)) for N in range(1,8)],
                        'passo':round(passo(v[1]),1)} for k,v in LARG.items()},
               alturas=alturas,
               prof={r:round(prof(B),1) for r,B in BAR.items()}), open('grade2.json','w'), ensure_ascii=False, indent=1)
