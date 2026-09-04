import json, math
ENC,NOX,NOXC,NOY,NOZ = 40.60,61.61,101.30,83.23,73.08
PE=19.4; GMM=0.22628; RS_KG=19.03
C_TZ,C_CZ,C_T = 0.3874596,0.4951,0.00968649
M_TZ,M_CZ,M_T = 44.31,56.62,1.10
B_VERT=270           # BAL-02-AC
PAN_L,PAN_W,PAN_T,DENS = 1200,200,15,0.556/1000
LARG={'SAPATEIRA':415,'MULTIUSO':595,'ARARA':717}

def corrida(B,N): return 2*NOX+(N-1)*NOXC+N*(B-2*ENC)
def prof(B):      return B+2*(NOY-ENC)
def alt(n):       return n*NOZ+(n-1)*(B_VERT-2*ENC)+PE
def passo(B):     return B+20.1

FAM=[
 dict(nome='CHECKOUT', larg='SAPATEIRA', pb=346, niv=6, vaos=[2,3,4],
      fundo=False, deck=True, peg=True, casinha=False, capsula=True,
      ref='120 × 45 × 140 cm'),
 dict(nome='ILHA', larg='MULTIUSO', pb=717, niv=4, vaos=[1,2,3],
      fundo=False, deck=True, peg=False, casinha=False, capsula=True,
      ref='132 × 80 × 85 e 198 × 100 × 105 cm'),
 dict(nome='PONTA DE GONDOLA', larg='SAPATEIRA', pb=346, niv=8, vaos=[1,2,3],
      fundo=True, deck=False, peg=False, casinha=True, capsula=True,
      ref='~100 × 45 × 200 cm'),
 dict(nome='PAREDAO', larg='MULTIUSO', pb=287, niv=8, vaos=[3,4,5],
      fundo=True, deck=False, peg=False, casinha=False, capsula=False,
      ref='5 vãos, ~220 cm'),
]
def bom(f,N):
    B=LARG[f['larg']]; pb=f['pb']; n=f['niv']; linhas=N+1
    p={'850-TZ':4*n, '850-CZ':2*(N-1)*n, '850-T':2*linhas,
       'BAR_LARG':2*N*n, 'BAR_PROF':linhas*n, 'BAR_VERT':2*linhas*(n-1), 'PE':2*linhas}
    if f['peg']: p['BAR_LARG']+=N        # barra de gancheira
    mad=(p['BAR_LARG']*B + p['BAR_PROF']*pb + p['BAR_VERT']*B_VERT + p['PE']*60)*GMM
    pit=passo(B); pl,pp=pit,prof(pb)
    n_pain=N*n
    if f['fundo']: n_pain+=N*(n-1)       # painel de fundo por vao entre niveis
    mad_p=n_pain*pl*pp*PAN_T*DENS
    tiras=math.ceil(pp/PAN_W); porchapa=max(1,int(PAN_L//pl))
    chapas=math.ceil(n_pain*tiras/porchapa)
    conn=p['850-TZ']*C_TZ+p['850-CZ']*C_CZ+p['850-T']*C_T
    plast=p['850-TZ']*M_TZ+p['850-CZ']*M_CZ+p['850-T']*M_T
    return dict(**p, n_pain=n_pain, chapas=chapas, painel=f"{pl:.0f}×{pp:.0f}",
                kg=round((mad+mad_p+plast)/1000,1), custo=round(conn+(mad+mad_p)/1000*RS_KG,2),
                larg=round(corrida(B,N)), profu=round(prof(pb)), altu=round(alt(n)),
                barra_larg=B, barra_prof=pb)

print("="*100)
print(f"{'familia':18}{'largura fixa':14}{'ver':4}{'L x P x A (mm)':>22}{'niv':>4}{'TZ':>4}{'CZ':>4}{'pain':>5}{'kg':>7}{'custo':>9}{'2x':>9}")
print("="*100)
out=[]
for f in FAM:
    for i,N in enumerate(f['vaos']):
        b=bom(f,N); ver=['P','M','G'][i]
        print(f"{f['nome']:18}{f['larg']+' '+str(b['barra_larg']):14}{ver:4}"
              f"{b['larg']}×{b['profu']}×{b['altu']:>6}{f['niv']:>4}{b['850-TZ']:4}{b['850-CZ']:4}"
              f"{b['n_pain']:5}{b['kg']:7.1f}{b['custo']:9.2f}{2*b['custo']:9.2f}")
        out.append(dict(familia=f['nome'], versao=ver, vaos=N, **b, larg_ref=f['larg'],
                        niveis=f['niv'], ref_imagem=f['ref'],
                        fundo=f['fundo'], deck=f['deck'], peg=f['peg'], casinha=f['casinha'], capsula=f['capsula']))
json.dump(out, open('fam.json','w'), ensure_ascii=False, indent=1)
print(f"\n  ALTURAS disponiveis (BAL-02-AC 270, passo {(B_VERT-2*ENC)+NOZ:.1f} mm):")
for n in range(3,9):
    print(f"     {n} niveis = {alt(n):.0f} mm")
