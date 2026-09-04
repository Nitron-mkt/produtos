GMM=0.22628
BAR={'BPE-01-AC':60,'BLA-03-AC':287,'PSA-03':424,'PSC-03':595,'PST-02':617}
C_TZ,C_CZ,C_T,C_H = 0.3874596, 0.4951, 0.00968649, 0.08717841
M_TZ,M_CZ,M_T,M_H = 44.31, 56.62, 1.10, 10.22
RS_KG_PINUS = 19.03    # R$/kg de pinus + conversao, derivado do modulo de 1 vao
NIV = 5                 # niveis de prateleira

def run(N):
    """corrida de N vaos encadeada. Devolve pecas, massa, custo."""
    linhas = N+1                       # linhas de montante
    p = {
      '850-TZ': 4*NIV,                 # so as 4 quinas das duas pontas
      '850-CZ': 2*(N-1)*NIV,           # nos de meio de vao
      '850-T':  2*linhas,
      '850-H':  10*N*NIV,
      'PSC-03': 2*N*NIV,
      'BLA-03-AC': linhas*NIV,
      'PST-02': 5*N*NIV,
      'PSA-03': 2*linhas*(NIV-1),
      'BPE-01-AC': 2*linhas,
    }
    conn = p['850-TZ']*C_TZ + p['850-CZ']*C_CZ + p['850-T']*C_T + p['850-H']*C_H
    mad  = sum(BAR[k]*GMM*v for k,v in p.items() if k in BAR)
    plast= p['850-TZ']*M_TZ + p['850-CZ']*M_CZ + p['850-T']*M_T + p['850-H']*M_H
    custo = conn + mad/1000*RS_KG_PINUS
    return p, conn, mad, plast, custo

print("=== ALGEBRA DOS NOS (por nivel de prateleira)")
print("   trizetas = 4  (fixo, so as duas pontas)")
print("   cruzetas = 2 x (N - 1)")
print("   montantes = 2 x (N + 1)\n")
print(f"{'N vaos':>7}{'largura ext':>13}{'trizetas':>10}{'cruzetas':>10}{'montantes':>11}{'peso kg':>9}{'custo':>10}{'2x custo':>10}")
for N in (1,2,3,4,5,6):
    p,conn,mad,plast,custo = run(N)
    larg = N*680.3 + (N-1)*0
    print(f"{N:7}{larg:11.0f} mm{p['850-TZ']:10}{p['850-CZ']:10}{2*(N+1):11}{(mad+plast)/1000:9.2f}{custo:10.2f}{2*custo:10.2f}")

print("\n=== ENCADEAR vs MODULOS SEPARADOS (3 vaos)")
p3,conn3,mad3,pl3,cst3 = run(3)
p1,conn1,mad1,pl1,cst1 = run(1)
print(f"   3 modulos de 1 vao : {3*cst1:8.2f}  | 60 trizetas, 0 cruzetas, 12 montantes")
print(f"   1 parede de 3 vaos : {cst3:8.2f}  | {p3['850-TZ']} trizetas, {p3['850-CZ']} cruzetas, {2*4} montantes")
print(f"   ECONOMIA           : {3*cst1-cst3:8.2f}  ({(1-cst3/(3*cst1))*100:.1f}%)")
print(f"   pecas poupadas: {60-p3['850-TZ']-p3['850-CZ']} nos, {12*4-p3['PSA-03']} montantes, "
      f"{30-p3['BLA-03-AC']} barras de profundidade, {12-p3['BPE-01-AC']} pes, {12-p3['850-T']} tampas")

print("\n=== CARGA: a cruzeta e o no de meio de vao, carrega o DOBRO de um canto")
print("   por vao, carga L: cada linha de montante de PONTA pega L/2 -> L/4 por montante")
print("                     cada linha INTERMEDIARIA pega 2 x L/2 = L -> L/2 por montante")
print("   secao continua minima medida: trizeta 288 mm2 | CRUZETA 258 mm2 (10% MENOR)")
print("   chapa 1 (fundo do encaixe):   trizeta 2,90 mm | CRUZETA 2,75 mm (5% MAIS FINA)\n")
for kg in (20,30,40):
    L = kg*NIV*9.81
    Ptz, Pcz = L/4, L/2
    print(f"   {kg} kg/prat ({kg*NIV} kg/vao):")
    print(f"      HIP. A parede em compressao: trizeta {Ptz/288:.2f} MPa (FS {10/(Ptz/288):.1f}x) | "
          f"cruzeta {Pcz/258:.2f} MPa (FS {10/(Pcz/258):.1f}x)")
    for lbl,coef in (("apoiada",0.0906),("engastada",0.0417)):
        s_tz = 6*coef*(Ptz/424)*15.7**2/2.90**2
        s_cz = 6*coef*(Pcz/424)*15.7**2/2.75**2
        f=lambda s: f"{s:5.1f} MPa {'ACIMA' if s>10 else 'FS %.1fx'%(10/s)}"
        print(f"      HIP. B chapa 1 em flexao, borda {lbl:10}: trizeta {f(s_tz)} | cruzeta {f(s_cz)}")
    print(f"      HIP. C chapa de topo: trizeta {Ptz/3114:.2f} MPa | cruzeta {Pcz/4370:.2f} MPa  -> irrelevante")

print("\n=== O MOLDE: quanto ele pode custar")
cont_inj = p3['850-CZ']*C_CZ          # contribuicao a 2x custo = 1x custo por peca
cont_prod = cst3                      # margem do produto a 2x custo
econ = 3*cst1-cst3
print(f"   cruzetas numa parede de 3 vaos: {p3['850-CZ']} un")
print(f"   (a) contribuicao da INJECAO so (2x custo da peca): R$ {cont_inj:.2f} por parede")
print(f"   (b) economia de encadear vs modulos separados:      R$ {econ:.2f} por parede")
print(f"   (c) margem do PRODUTO que a cruzeta viabiliza (2x):  R$ {cont_prod:.2f} por parede")
print(f"\n   {'molde R$':>10}{'(a) meses':>12}{'(b) meses':>12}{'(c) meses':>12}   a 3 paredes/mes")
for M in (20000,30000,50000,80000):
    print(f"   {M:10,}{M/(cont_inj*3):12.0f}{M/(econ*3):12.0f}{M/(cont_prod*3):12.1f}")
print(f"\n   {'molde R$':>10}{'(a) meses':>12}{'(b) meses':>12}{'(c) meses':>12}   a 10 paredes/mes")
for M in (20000,30000,50000,80000):
    print(f"   {M:10,}{M/(cont_inj*10):12.0f}{M/(econ*10):12.0f}{M/(cont_prod*10):12.1f}")
