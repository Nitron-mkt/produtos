# Chrono v3 — o que mudou, e o que eu decidi por conta

Revisão sobre os apontamentos de moldabilidade. Tudo refeito em B-rep
(OpenCASCADE), não em malha — é o que permite raio de canto e saída de verdade.

---

## 1. Saída de extração

**1,5° em toda parede vertical** (a faixa pedida era 1 a 3). Convenção: molde
abre em +Y, partição na face de baixo de cada peça — logo parede externa
**estreita para cima** e furo **alarga para cima**.

Medido face a face na peça pronta, com o auditor conferido contra um cilindro
reto (tem de reprovar) e um cone de 1,5° (tem de passar):

| | parede vertical antes | depois |
|---|---|---|
| M01 (só o que o Chrono acrescenta) | 45,6 mm² | **~20 mm², só a lateral dos numerais** |
| M02 rodinha | 234,5 mm² · 21,8% | **8,1 mm² · 0,8%**, só a lateral dos numerais |
| M03 ponteira | 234,7 mm² · 29,0% | **6,6 mm² · 0,8%**, só MÊS e o ícone |

**Toda parede estrutural está com 1,5°.** A única parede vertical que sobrou é o
flanco de 0,10 mm dos caracteres em auto relevo — ver a seção 9a: com saída, o
STEP não abria.

Os 167 mm² de parede vertical que sobram na M01 são **do corpo da válvula
original**, que já está ferramentado e não é nosso.

O que estava sem saída e ganhou: rebaixo, poste, furo passante, mesa, aro
externo e interno da rodinha, 12 entalhes de unha, contorno da gota, janela,
chanfro da janela, fendas do pino, drenos e o furo interno do pino.

## 2. Cantos abaulados

| onde | raio |
|---|---|
| contorno da gota, topo | 0,30 |
| contorno da gota, base · borda da janela · faces da rodinha · topo da mesa | 0,15 |
| canto piso/parede do rebaixo (côncavo, é o que enche primeiro) | 0,15 |
| **pé do poste** | **0,15** |
| contorno de cada caractere, em planta | 0,06 |

**O pé do poste não levou 0,30 e isso é medido, não arbitrado:** a folga radial
para a rodinha é 0,20 e a face de baixo dela passa a 0,02 mm do piso. Com raio
0,30 a concordância chegaria a Ø13,585 na altura crítica e encostaria na
rodinha. Com 0,15 sobram 0,125 mm. Se quiserem 0,30, o furo da rodinha tem de
abrir para Ø13,90.

Achado no caminho: o corte do rebaixo parava exatamente em Ø13,20, o mesmo
diâmetro nominal do poste. Com o poste ganhando saída, sobrava uma **aleta de
0,03 mm de espessura por 0,60 de altura** entre os dois. O corte agora entra
até Ø10,00, bem dentro do poste.

## 3. Escala dos dias

Você estava certo: o vão extra em 1..9 é o espaço do zero que sobrou. Agora o
que é igual é o **vão entre as bordas**: **5,81° entre todos os 31**.

Consequência que preciso registrar: **o passo do dia deixa de ser constante.**
O centro do dia 9 anda de 182,9° para 162,6°. Para o Chrono tanto faz — o dia
não tem detente, quem alinha é a mão e quem lê é o olho. Mas fecha a porta para
um dia detentado no futuro. Se preferirem passo constante, é uma linha.

## 4. O rebaixo do anexo 01

Não era o rebaixo da rodinha — era a **concha das 12 h aflorando no piso dele**.
A cunha foi enchida de ponta a ponta, da face de baixo (Y 35,40) até a face
(37,23), e o piso ficou plano.

Medi antes de encher: o fundo da concha só desce até **Y 36,214** e a face de
baixo da válvula naquela região **não passa de 35,400** em lugar nenhum. Então o
enchimento não acrescenta nada por baixo, não fecha vazio nenhum, e a parede
naquela cunha passa a ter **1,83 mm — a mesma do resto da chapa**. Era antes que
estava fina e irregular.

## 5. Detente

- calota de **Ø2,00 de base e 0,25 de altura** (esfera R 2,125), contra Ø0,84 e 0,18
- **centrada na faixa do rebaixo, em r 10,10** — meio exato entre o poste (6,60)
  e a parede (13,60); antes estava em 7,80, encostada no poste
- as 12 covinhas da rodinha usam a **mesma esfera, invertida**

Uma diferença proposital: cada uma é referida à **sua própria face** (piso 36,63
e face de baixo da rodinha 36,65). Assim a folga de montagem de 0,02 mm se
mantém e o par não trava. Folga mínima medida no conjunto: **0,017 mm** — que é
o que um detente tem de ter.

Nenhuma das duas é undercut: a barriga da esfera fica abaixo da face, a calota
só estreita para cima e sai sozinha do molde.

## 6. Letras e números

**0,10 mm de auto relevo, 1,50 mm de altura de caractere, em tudo** — dias,
meses e MÊS.

⚠️ **Duas leituras que eu tive de fazer, e que você confirma ou corrige:**

**a) "espessura 1,5 mm" eu li como altura do caractere, não espessura do traço.**
Um traço de 1,5 mm exigiria caractere de ~8 mm de altura; a faixa da mesa tem
4,55 mm. Não cabe. Com 1,50 de caractere o traço sai em **0,28 mm**. Se o que
você quis foi traço mínimo, me diga o valor que eu engrosso a fonte.

**b) A saída do caractere é 15°, não 1,5°.** Com 0,10 de relevo, 1,5° dá **2,6
micra** de recuo — o aço não guarda isso. 15° custam 0,027 mm por lado e a letra
continua legível. Se a casa trabalha com outro número para letra rasa, é um
parâmetro.

**E um aviso honesto:** a 0,10 mm de relevo os números ficam **bem mais discretos**
que os 0,25/0,30 de antes. No 3D dá para ler, mas em peça injetada cinza vai
depender de contraste de acabamento (fundo texturizado e topo polido, ou o
contrário). Se a leitura for prioridade sobre o ciclo, 0,15 já muda bastante.

## 7. Ponteira

- **"D" removido**
- **"M" virou "MÊS"**, em auto relevo (4 contornos, com o acento)
- **ícone da Nitron de gravado para auto relevo**

Para não piorar o orçamento de altura, o corpo da lâmina passou de 1,60 para
**1,50** e o relevo devolve os 0,10. **O envelope não mudou:** topo em Y 39,950,
os mesmos +0,188 mm sobre o ponto mais alto da tampa. Mesma coisa na rodinha
(1,50 de corpo + 0,10 de numeral).

## 8. Conferido

| | |
|---|---|
| interferência M01×M02, M01×M03, M02×M03 | 0,0000 mm³ |
| folga do detente | 0,017 mm |
| folga ponteira × rodinha | 0,100 mm |
| encaixe da farpa | 0,40 mm (inalterado) |
| folga poste × furo da rodinha | 0,242 mm |
| folga pino × furo, no ponto mais estreito | 0,100 mm |
| topo do conjunto | Y 39,950 · +0,188 sobre a tampa |
| massa | 2,907 g (v2: 2,908 g) |
| B-rep dos 6 arquivos | válido no BRepCheck |

## 9. Correção de 29/09 — o STEP abria "fatiado" no SolidWorks

Duas coisas, e a segunda é grave.

### a) Aresta curta demais

O arquivo **já era sólido** (`MANIFOLD_SOLID_BREP` + `CLOSED_SHELL`). O que
quebrava a importação era **aresta de micra**: 763 arestas abaixo de 0,01 mm, a
menor com **0,0015 mm**. Todo importador de STEP colapsa aresta nessa ordem, e
aí a costura do sólido se desfaz e a peça abre como superfície solta — "toda
fatiada, pontinhada".

A origem: **a extrusão cônica do OpenCASCADE degenera no canto de um contorno de
letra.** Medido, fundindo os 12 numerais da rodinha:

| saída do caractere | arestas < 0,05 mm | menor aresta | micro-faces |
|---|---|---|---|
| 15° | 700 | 0,00065 | 205 |
| 7° | 529 | 0,00006 | 212 |
| 3° | 367 | 0,00032 | 177 |
| **0°** | **0** | **0,100** | **0** |

Tentei curar depois (`ShapeUpgrade_UnifySameDomain`, `ShapeFix_Wireframe`):
derruba de 700 para 75, mas devolve o sólido **inválido**, com face de área
negativa. Não serve.

**Decisão: saída ZERO na parede lateral dos caracteres.** E não faz falta — o
que solta uma letra de 0,10 mm de relevo do aço não é a saída da parede
lateral, é a própria altura de 0,10. Se a ferramentaria quiser saída nos
caracteres, o caminho limpo é aplicar no CAD dela, com a operação de draft
nativa; o kernel do SolidWorks faz isso sem gerar lasca.

Também entraram: segmento mínimo de 0,10 mm em todo contorno de letra; raio da
mesa de 0,15 para 0,08 (0,15 comia 0,15 dos 0,18 de parede e sobrava aresta de
0,034); pé do poste com 5 pontos de arco em vez de 10; e fenda e dreno da
ponteira com a meia-cana em **arco exato** em vez de polígono.

**Porteiro novo: `qualidade.py`.** Reprova qualquer arquivo com mais de um
sólido, com aresta < 0,05 mm ou face < 0,002 mm². Os seis passam.

### b) ⚠️ Duas bolhas penduradas embaixo da válvula

Na estrutura antiga a mola do detente era uma **esfera inteira somada** à peça
depois do corte do rebaixo. A calota de 0,25 acima do piso era o que eu queria —
mas os outros **72% da esfera (28,9 mm³ cada, 57,8 mm³ no total)** ficavam
pendurados **abaixo** da chapa da válvula, em r 10,10, descendo até Y 32,63
contra os 35,40 da face de baixo. Material solto dentro do pote, bem onde a
válvula balança.

Estava no STEP que eu entreguei. Foi erro meu de estrutura, não de cota.

**Corrigido invertendo a ordem:** as duas esferas agora são **subtraídas do
cortador do rebaixo**. O corte já deixa as duas molas de pé e nada mais. Medido
na peça montada: superfície em Y 36,873 nas duas posições (piso 36,63 + 0,243) e
**ponto mais baixo da peça igual ao da válvula original, 32,570** — nada
acrescentado por baixo.

## 10. Os arquivos

STEP em `v3/step/`. A M01 continua em receita, agora com 4 passos **e a ordem
importa**:

```
válvula final = (((CAD original + M01a) − M01b) + M01c) − M01d
```

1. **somar** `v3_M01a_SOMAR_1_enchimento_e_mesa`
2. **subtrair** `v3_M01b_SUBTRAIR_2_rebaixo`
3. **somar** `v3_M01c_SOMAR_3_poste_detentes_dias` (56 sólidos soltos: poste,
   2 detentes e os 53 contornos dos 31 numerais)
4. **subtrair** `v3_M01d_SUBTRAIR_4_furo_passante`

O enchimento entra antes do rebaixo (senão o rebaixo não tem o que cortar) e os
detentes entram depois (senão o rebaixo raspa as molas).

`v3_M02_Rodinha_Meses` e `v3_M03_Ponteira` são peças inteiras, um sólido cada.
Os STL em `v3/stl/` são para ver e imprimir, não para ferramenta.

---

# Revisão de 06/10 — os 5 apontamentos (IMG01 a IMG05)

## 11. IMG01 — a janela do mês

**Tirado o relevo em volta do furo.** O que aparecia como moldura era um chanfro
postiço que eu tinha somado para "marcar" a janela. Saiu. O furo agora é só furo.

**Raio nas duas arestas, R0,30** — em cima (Y 39,85) e embaixo (Y 38,35), as
duas de uma vez. Antes só a de cima tinha quebra, e era chanfro, não raio.

**"MÊS" desceu 1,50 mm**, de r 7,40 para **r 5,90**. O acento chegava a r 8,33 e
a janela começa em 8,25 — ele era cortado pela borda do furo, por 0,08 mm. Agora
o texto ocupa **r 4,97 a 6,83**: sobra **1,42 mm** até a janela e **1,07 mm** até
o ícone. Nada mais se toca.

## 12. IMG02 — as 4 cavas

**Retiradas.** Eram drenos que eu tinha posto para o ar sair da fenda do cubo.
O projetista não vê necessidade e ele tem a palavra: na prática a fenda já respira
pela folga de 0,10 mm do encaixe com a M02.

Sobre a suspeita de que estavam **vazando o pino**: o projetista leu certo a
imagem. As cavas desciam a r 9,50 e o pino de encaixe vive em r ≤ 3,40 — no
sólido elas não se cruzavam —, **mas** a renderização ficava ambígua porque as
duas coisas apareciam na mesma silhueta. Medido agora sem as cavas:
**interferência M01×M03 = 0,0000 mm³** e **M02×M03 = 0,0000 mm³**. Sem perfil
negativo em lugar nenhum.

## 13. IMG03 — numeral do mês e janela maiores

Os dois cresceram **juntos**, senão não adianta:

| | antes | agora |
|---|---|---|
| altura de caixa alta do mês | 1,50 | **2,20** (+47%) |
| janela, raio | 8,60 – 11,00 | **8,25 – 11,35** |
| janela, meia-largura | 1,55 | **1,93** |
| raio de canto da janela | 0,70 | 0,70 |

Folga do numeral dentro da janela, medida no pior caso (**mês 9**, o mais largo):
**0,45 mm** em volta. Da borda da janela até o contorno da gota da ponteira:
**1,09 mm** — a janela cresceu sem comer a parede.

## 14. IMG04 — os dias juntos e maiores

Altura de caixa alta dos dias: **1,50 → 2,40 mm (+60%)**.

O espaçamento não é mais por centro, é **por borda**: cada numeral recebe o arco
que ele realmente ocupa, e o vão entre dois vizinhos é o mesmo nos 31 —
**0,69 mm**. É por isso que o "1" e o "11" não ficam mais com buraco de um lado.
2,40 é o maior valor em que os 31 ainda fecham a volta com vão positivo; acima
disso o "28" encosta no "29".

## 15. IMG05 — o 1,33° quebrado

**Não consigo reproduzir esse valor.** Auditei todas as faces cônicas dos seis
STEP, uma a uma, pelo ângulo do cone no B-rep:

```
M01_1  1,500° (2 faces)
M01_2  1,500° (1)
M01_3  1,500° (1) · 45,000° (1, chanfro de topo do poste)
M01_4  1,500° (1) · 45,000° (1, chanfro do furo)
M02    1,500° (25)
M03    1,500° (14) · 5,000° (4) · 30,000° (4, rampa da farpa)
ângulos quebrados: 0
```

O furo da M02 — que é o candidato mais provável ao que ele mediu — dá
**1,500° exatos**. Duas coisas que de fato estavam quebradas no arquivo anterior
e foram corrigidas nesta rodada:

- **saída do poste em 1,884°** e do furo passante em 1,617°: o recuo era calculado
  sobre a altura até o topo e aplicado 0,30 mm abaixo dele. Agora o raio é função
  linear de Y, dá 1,500° em qualquer corte.
- **a concordância do pé do poste eram 4 facetas de cone** (11,25° / 33,75° /
  56,25° / 78,75°), não um raio. Virou toro de verdade (R0,15 revolucionado).

Se o 1,33° saiu de uma **medição de face** no SolidWorks, pode ser isso: medir o
ângulo entre duas faces adjacentes de um sólido **com raio de concordância** dá o
ângulo da tangente no ponto clicado, não a saída. **Me diga qual face ele cotou**
que eu confiro essa específica — mas pelo B-rep não há 1,33° em lugar nenhum.

## 16. O que foi verificado nesta rodada

**Os seis STEP passam no portão de qualidade** (o mesmo que pegou o problema do
"fatiado"):

```
arquivo                                        sol.  aresta min  curtas  face min
M01_1 SOMAR enchimento+mesa+dias                 1     0,0500      0      0,01005
M01_2 SUBTRAIR rebaixo com detentes              1     0,2317      0      3,33794
M01_3 SOMAR poste                                1     0,2356      0      9,85160
M01_4 SUBTRAIR furo passante                     1     0,4950      0     10,07790
M02   Rodinha Meses                              1     0,0710      0      0,01002
M03   Ponteira                                   1     0,1000      0      0,01001
```

Um sólido por arquivo, B-rep válido, **nenhuma aresta abaixo de 0,05 mm** e
nenhuma face abaixo de 0,002 mm². Era aresta de 0,0015 mm que desmanchava a
costura na importação.

Montagem:

| | |
|---|---|
| interferência M01×M02, M01×M03, M02×M03 | **0,0000 mm³** |
| folga do detente | 0,0174 mm |
| folga ponteira × rodinha | 0,100 mm |
| contato da farpa | 0,0000 (é o encaixe, por projeto) |
| parede na ponta do pino | **0,444 mm** (era 0,242 — fio de faca que rebarba) |
| topo do conjunto | Y 39,950 |

## 17. O que continua aberto

1. **O conjunto fica 0,188 mm acima do ponto mais alto da tampa.** Isso nunca foi
   decidido. Ou aceita (a tampa empilha com 0,19 mm de desencontro), ou eu rebaixo
   a ponteira 0,20 mm — o que come 0,20 dos 1,50 de espessura dela. Preciso da
   decisão.
2. **Qual face deu 1,33°** — seção 15.
3. **O STL do conjunto completo não dá para regerar** sem o
   `Mont_pote_com_valvula__prova_valvula1.STL` e o STL da tampa. O container foi
   recriado e a pasta de uploads foi junto. A **M01 destes STEP continua correta**
   — ela é receita de somar/subtrair sobre o CAD original, não depende do STL —,
   mas para eu conferir de novo contra a válvula real, ou regerar o visor de
   apresentação, os dois arquivos precisam voltar.

O ícone da Nitron, que vinha do PDF e também sumiu com a pasta, foi **recuperado
de uma seção do STEP anterior e está versionado no repositório** (`icone_nitron.json`).
Não some mais.

---

## 18. "Não veio a válvula" — as 3 peças inteiras

O projetista abriu a M01 e achou só o que o Chrono acrescenta, sem corpo. Era o
esperado pela estrutura do arquivo, mas receita não se abre — e ele tem razão em
querer ver a peça. Agora existem **duas pastas**:

| pasta | o que tem | para quê |
|---|---|---|
| `v3/step/` | a receita de 4 passos da M01, mais M02 e M03 | **vai para a ferramenta** |
| `v3/step_completo/` | **3 arquivos, 1 sólido cada** | abrir, medir, ver |

A M01 completa é montada sobre uma **chapa de prova** — disco de Ø38,00 com a
mesma saída, de Y 35,40 a 37,23 — porque o STL da válvula injetada saiu da sessão
quando o container foi recriado. **Os datums e tudo o que o Chrono acrescenta
estão exatos**; a saia e os pés da válvula, abaixo de Y 35,40, não estão. O nome
do arquivo diz isso (`__CHAPA_DE_PROVA`) para ninguém mandar cortar aço por ele.

Com o STL da válvula de volta, `completas.py` gera a peça inteira de verdade sem
mais nenhuma mudança. E, de todo modo, **o certo é aplicar a receita no CAD mestre
da válvula**: é o único jeito de a geometria já ferramentada sair bit a bit igual.

Os três passam no mesmo portão: 1 sólido, B-rep válido, aresta mínima 0,0500 /
0,0710 / 0,1000 mm, nenhuma face abaixo de 0,002 mm².

O visor ganhou dois modos novos — **As 3 montadas** (agora o modo de entrada) e
**As 3 explodidas**, com as peças separadas no eixo para ver as faces que se
encostam. Os cinco modos continuam com corte, arestas e mapa de altura.
