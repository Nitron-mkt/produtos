# A peça descola da mesa quando começa — o que fazer

"Descola **quando começa**" é diagnóstico, não sintoma vago: a primeira camada nunca
grudou de verdade. Isso quase sempre é **altura do bico** ou **chapa engordurada**, não
fatiamento. Por isso a ordem abaixo começa na impressora.

## 1. Teste de primeira camada — faça este antes de qualquer outra coisa

`Chrono_0_Teste_Primeira_Camada.gcode` · ~10 min · 0,98 g

Cinco quadrados de 28 mm — quatro cantos e o centro — **uma camada só** de 0,20 mm.
Não é peça, é instrumento de medida. Imprima e olhe o cordão:

| O que você vê | O que significa | O que fazer |
|---|---|---|
| Fios redondos, com **vão entre eles**, dá para ver a chapa | bico **alto demais** | baixar o Z offset em 0,02 a 0,05 |
| Superfície lisa, fios **fundidos sem linha entre eles**, canto quadrado | **certo** | não mexe |
| Superfície translúcida, rebarba nas bordas, bico raspando | bico **baixo demais** | subir 0,02 a 0,05 |
| Certo no centro e alto nos cantos (ou o contrário) | chapa **não nivelada** | refazer o nivelamento automático |

Na Kobra 3 o Z offset se ajusta **durante a impressão**, então dá para corrigir olhando
e voltar a imprimir sem refatiar. Ajuste em passos de 0,02 mm — 0,1 mm já é muito.

## 2. Lavar a chapa. De verdade.

Gordura de dedo é a causa número um e não se vê. Álcool isopropílico **não tira óleo de
pele** — ele espalha. O jeito certo:

1. tire a chapa, lave com **água quente e detergente de louça**, esfregando com a mão;
2. enxágue bem e seque com pano limpo ou papel;
3. daí para frente, pegue a chapa **só pelas bordas**.

Numa chapa PEI texturizada isso costuma resolver sozinho. Refaça a cada 5 a 10 impressões.

## 3. O que eu mudei nos arquivos

Perfil `chrono_kobra3_adesao.ini`. Sete mudanças, todas na largada:

| Ajuste | Antes | Agora | Por quê |
|---|---|---|---|
| `brim_separation` | 0,1 | **0** | a aba estava com 0,1 mm de folga da peça — ela acompanhava sem segurar. Colada, ela puxa. |
| `brim_width` | 3 | **8 a 10 mm** | mais área de ancoragem |
| `elefant_foot_compensation` | 0,1 | **0** | encolhia 0,1 mm todo contorno da 1ª camada: é área de adesão jogada fora |
| `first_layer_extrusion_width` | 0,42 | **0,50** | cordão mais gordo esmaga mais contra a chapa |
| `first_layer_bed_temperature` | 60 | **65 °C** | só na primeira camada |
| `disable_fan_first_layers` | 1 | **3** | a ventoinha ligava na 2ª camada |
| `full_fan_speed_layer` | 3 | **8** | e ia a 100% na 3ª. PLA que esfria rápido encolhe, e o que encolhe descola. |

As duas primeiras são as que mais pesam. `brim_separation = 0,1` era um defeito real do
perfil: aba com folga é decoração.

## 4. Se ainda descolar: a válvula com raft

`Chrono_1_de_4_Valvula_COM_RAFT.gcode` · 56 min · 4,25 g (contra 55 min e 4,06 g)

A válvula é a peça de risco: o corpo é um disco com saia e toca a chapa por só **11 mm²**
de face plana. O raft põe uma base de 3 camadas debaixo dela e transforma esses 11 mm²
em ~1.200 mm² de contato. Custa 1 minuto e 0,2 g, e a face de baixo sai rugosa — o que
numa cópia em FDM não é funcional de qualquer jeito.

Use este só se o item 1 e o 2 não resolverem. Raft é remendo, Z offset é conserto.

## 5. Coisas que parecem causa e não são

- **Cola bastão / laquê.** Funciona, mas mascara o Z offset errado. Se precisar de cola
  numa chapa PEI limpa, o bico está alto.
- **Aumentar a temperatura do bico.** Ajuda pouco na adesão à chapa e piora o
  escorrimento e o detalhe dos números, que aqui têm 0,32 mm de traço.
- **Mesa muito mais quente.** Acima de ~70 °C o PLA amolece na base e a peça entorta em
  vez de grudar melhor.
- **Corrente de ar.** Janela aberta ou ventilador de ambiente soprando na mesa derruba
  peça pequena. Vale mais que qualquer ajuste de fatiador.
