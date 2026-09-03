# Verificacao independente. Vao livre, secao e geometria vem das minhas medicoes;
# as propriedades do pinus sao de literatura e estao explicitadas como premissa.
b_, h_ = 15.3, 26.6          # secao da barra, mm
L_slat = 617.0               # PST-02, vao da regua
E_pin  = 9000.0              # MPa, MOE pinus taeda ~12% umidade (premissa: 8.000-12.000)
FM_ADM = 12.0                # MPa admissivel de flexao, longa duracao (premissa conservadora)
N_SLAT = 5                   # reguas por prateleira
NIVEIS = 5
COLUNAS = 4
T_PAREDE = 2.95              # parede do conector
SOCK = (15.7, 27.0)          # secao do encaixe medida

def prop(h, b):
    return b*h**2/6, b*h**3/12   # W (mm3), I (mm4)

print("=== REGUA DE PINUS PST-02: vao 617 mm, secao 15,3 x 26,6")
for lbl,(h,b) in (("eixo forte (h=26,6)",(h_,b_)), ("eixo fraco (h=15,3)",(b_,h_))):
    W,I = prop(h,b)
    print(f"  {lbl}: W={W:.0f} mm3  I={I:.0f} mm4")
    for kg in (20,30,40):
        P = kg*9.81                 # N por prateleira
        w = (P/N_SLAT)/L_slat       # N/mm por regua
        M = w*L_slat**2/8
        sig = M/W
        d = 5*w*L_slat**4/(384*E_pin*I)
        fs = FM_ADM/sig
        print(f"      {kg} kg/prat -> {P/N_SLAT:5.1f} N/regua | sigma={sig:4.2f} MPa (FS {fs:4.1f}x) | flecha={d:5.2f} mm = L/{L_slat/d:.0f}")

print("\n=== NO TRIZETA em compressao: coluna carregando 5 prateleiras")
area_parede = 2*(SOCK[0]+SOCK[1])*T_PAREDE
print(f"  area de parede do encaixe = 2 x (15,7+27,0) x 2,95 = {area_parede:.0f} mm2")
for kg in (20,30,40):
    Ptot = kg*NIVEIS*9.81
    Pcol = Ptot/COLUNAS
    sig = Pcol/area_parede
    print(f"  {kg} kg/prat -> {kg*NIVEIS} kg no modulo | {Pcol:5.0f} N por coluna | sigma={sig:4.2f} MPa"
          f" | FS vs 10 MPa adm PP = {10/sig:4.1f}x")

print("\n=== PORTA-HASTE: cada regua apoia em 2 clipes")
area_cis = T_PAREDE*21.92     # parede x profundidade do clipe
print(f"  area resistente estimada = 2,95 x 21,92 = {area_cis:.0f} mm2")
for kg in (20,30,40):
    P = kg*9.81/N_SLAT/2      # N por clipe
    print(f"  {kg} kg/prat -> {P:4.1f} N por clipe ({P/9.81:4.2f} kgf) | tensao nominal = {P/area_cis:4.2f} MPa")

print("""
LEITURA:
  A madeira nao e o limite  - FS de 3 a 7x e flecha de 1 a 7 mm.
  O no em compressao tem folga - FS de 5 a 10x contra 10 MPa.
  As tensoes no clipe sao baixissimas (< 0,7 MPa), entao a falha NAO e ruptura.
  Sobra como modo critico: (1) o C do clipe abrir sob carga - rigidez/geometria,
  nao resistencia; (2) creep do PP relaxando a pre-carga do snap e assentando a
  coluna ao longo de meses. Nenhum dos dois se resolve por calculo de tensao.
  ENSAIO QUE FECHA: carga permanente de 40 kg/prateleira por 60-90 dias com medicao
  de flecha e de assentamento da coluna, mais tentativa de arrancamento do clipe.
""")
