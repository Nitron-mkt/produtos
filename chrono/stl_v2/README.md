# Chrono · datador — 3 moldes sobre a válvula que a Nitron já injeta

> **Mercado internacional:** os meses são **numerais de 1 a 12**, não abreviações em
> português. Nada no produto depende de idioma.

Gerado de `Mont_pote_com_valvula__prova_valvula1.STL`. **A tampa não foi tocada.**
A parte de baixo da válvula é a original, bit a bit: tudo abaixo de Y 37,23 saiu do
seu arquivo, e a prova disso é a interferência contra a tampa (abaixo).

| Arquivo | Peça | Gira? | Massa PP |
|---|---|---|---|
| `Chrono_M01_Valvula_Dias.stl` | válvula + 31 dias, **furada no eixo** | **não** — é a válvula | 2,13 g |
| `Chrono_M02_Aro_Meses.stl` | aro dos 12 meses | **sim** | 0,30 g |
| `Chrono_M03_Travinha_Seta.stl` | travinha com seta e **pino passante** | **sim, solta no pino** | 0,14 g |
| `Chrono_M04_Conjunto.stl` | os três montados, só para ver | — | 2,57 g |

Válvula original: 2,04 g. O datador inteiro custa **+0,53 g de PP** por tampa.

## Como se lê — e por que a seta gira

Duas peças giram porque **um único giro só marca um número**. Com o dia fixo na
válvula e só o aro dos meses girando, dia e mês ficariam amarrados: escolher o mês
escolheria o dia. Então:

- **dia** → a seta da travinha gira e aponta um dos 31 números da válvula;
- **mês** → o aro gira e o mês para embaixo do **índice fixo ▼ às 12 h**, que é
  moldado na própria válvula.

Dois giros independentes, três moldes, o dia fixo na válvula como você pediu.
Dia e mês ficam **em pé quando lidos às 12 h** — a mesma convenção para os dois.

## O acionamento — a concha das 12 h

Medindo a sua válvula, ela tem **uma concha de 1,02 mm de fundo às 12 h**
(setor ~55°–125°, r 8 a 18) e tinha **um ressalto de aperto às 6 h** (r 7,5–17,
subindo até Y 38,24). São as duas pontas do gangorra: *"aperta em uma das pontas,
ela fecha, e se você aperta na outra ponta ela abre."*

O ressalto das 6 h ficava acima de Y 37,23 e saiu junto com o topo antigo. No lugar
dele entrou a **mesa dos dias** — um anel plano de 0,18 mm, de r 14,20 a 18,75, que
também faz ponte sobre a concha para que os 31 números nasçam todos na mesma altura.

O aperto passa a ser **na banda dos dias, às 6 h e às 12 h**. Isso não é perda:

| | ressalto original (6 h) | mesa dos dias |
|---|---|---|
| raio onde o dedo cai | ~12,2 mm | **16,6 mm** |
| braço de alavanca sobre o eixo das orelhas | 12,2 mm | **16,6 mm — 36% maior** |

O eixo do gangorra passa pelas orelhas (3 h/9 h), então o braço é a distância até
elas: a mesa aperta **com mais vantagem** que o ressalto que substituiu. A concha
funda (r < 14,20) continua aberta como poço de polegar; o aro dos meses passa por
cima dela sem encostar (1,04 mm de ar).

## Conferência numérica

```
ENTRE AS TRES PECAS
  valvula x aro                           0.0000 mm3  ok
  valvula x travinha                      0.0000 mm3  ok
  aro x travinha                          0.0000 mm3  ok

CONTRA A TAMPA — a tampa NAO foi tocada
  aro x tampa                             0.0000 mm3  ok
  travinha x tampa                        0.0000 mm3  ok
  valvula nova x tampa                    1.6357 mm3
  valvula ORIGINAL x tampa                1.6357 mm3  <- a que voce ja injeta
  diferenca +0.0000 mm3  nenhum aperto novo

VARREDURA (24 posicoes de giro)
  travinha, pior caso                     0.0000 mm3  ok
  aro nas 12 posicoes de encaixe          0.0000 mm3  ok
  aro entre encaixes                      0.0580 mm3  <- o detente, e de projeto

ALTURAS (aro de empilhamento da tampa em Y 39,72)
  M01 valvula+dias     Y 32.57 .. 38.05   folga 1.67 mm
  M02 aro dos meses    Y 37.25 .. 38.35   folga 1.37 mm
  M03 travinha/seta    Y 34.00 .. 38.95   folga 0.77 mm

PINO PASSANTE
  ponta do pino chega a Y 34.00  — passa 1.40 mm alem da chapa da valvula
  raio do furo na saida 2.50  |  raio da farpa 2.90  ->  encaixe radial 0.40 mm
  folga ate o fundo do poco da tampa (Y 32,15): 1.85 mm

CURSO DO GANGORRA (pivo em Y 34,69, meia altura das orelhas)
  graus   conjunto novo   valvula original
  -3.60         0.236            0.236
  -1.80         0.075            0.075
  +0.00         1.636            1.636
  +1.80        28.159           28.159
  +3.60        77.038           77.038
  -> curva IDENTICA: o pino nao rouba curso do gangorra
```

**+0,0000 mm³** é o número que importa: a válvula nova aperta a tampa exatamente
como a que já está em linha. Nada mudou embaixo.

## Cotas

| | |
|---|---|
| face de topo da válvula (datum) | Y 37,23 |
| mesa dos dias | r 14,20–18,75 · Y 37,23→37,41 |
| 31 dias | r 16,65 (banda 15,80–17,50) · caixa alta **1,70** · relevo **0,25** |
| passo e folga dos dias | passo 3,37 mm de arco · **0,98 mm** entre dois números |
| traço mais fino dos dias | **0,32 mm** |
| grafia dos dias | **1 a 9 sem zero**, 10 a 31 com dois dígitos |
| índice fixo do mês | 12 h · r 14,25–15,30 · relevo 0,30 |
| poste central | r 5,40 · topo Y 38,05 · **reto, sem rebaixo** |
| furo passante na válvula | Ø5,00 · de Y 35,40 a 38,05 · chanfro 0,35 na entrada |
| pino da travinha | Ø4,80 (folga radial 0,10) · canal interno Ø3,10 aberto nas duas pontas |
| farpa | Ø5,80 · encaixe radial **0,40** · ombro a **90°** · ponta a 31° |
| pernas do pino | 4 · vão 2,75 · parede 0,85 na raiz → 0,55 na farpa |
| aro dos meses | r 5,60–12,90 · espessura 0,80 · Y 37,25→38,05 |
| 12 meses | r 10,80 · caixa alta 1,90 condensada 0,78 · relevo 0,30 |
| folga entre dois meses | **1,39 mm** (palavra 4,26 em passo 5,65) |
| entalhes de unha | 12 · r 1,00 centrados em r 13,30 |
| detente | 2 molas r 0,42 na válvula × 12 covinhas r 0,55 no aro, em r 7,50 |
| curso do detente | **0,16 mm** de interferência entre encaixes |
| travinha | colar r 5,55–**6,90** · braço **2,10** de largura, 0,50 de espessura |
| ponta da seta | cabeça triangular de r 14,45 a **r 15,65** — para rente à borda de dentro dos dias |
| espigão do dorso | 0,80 × 0,60, de r 14,45 a 15,30 · topo Y 39,05 |

## O que ainda não está resolvido

- **Traço de 0,32 mm nos dias** (0,36 nos meses). Em molde é relevo fino mas viável
  em PP — o sulco no aço fica 0,32 de largura por 0,25 de fundo, proporção < 1, que
  enche. O contraste tem de vir de **acabamento de molde** (caractere polido sobre
  campo VDI 27-30), não de tampografia. Em impressão 3D com bico de 0,40 o traço é
  **menor que uma extrusão: o número não forma**. Para provar a leitura, bico de
  0,25 mm ou escala ≥ 2×.
- **Força de inserção do pino.** As quatro pernas flexionam 0,40 mm num vão de
  2,75 — **2,6% de deformação** contra os 8% que o PP aceita numa montagem única.
  A conta fecha com folga, mas quem decide é a prensa de montagem.
- **A seta não tem detente.** O aro dos meses trava em 12 posições, mas o dia é
  posicionado a olho. Se quiser estalo também no dia, cabem 31 dentes no colar
  (passo de 1,12 mm em r 5,55) — é detalhe fino de molde, e não está desenhado.
- **Rigidez do braço da seta.** O braço tem 0,50 mm de espessura, e só 0,24 mm de
  folga sobre os números. Com a seta curta o vão livre caiu para ~1,2 mm e o
  **espigão de 0,60 mm no dorso** passou a ser folga, não necessidade — ficou porque
  lê como o nervo da seta. Se ainda raspar, a correção é subir o braço externo
  (37,95 → 38,05), não engrossá-lo.
- **Onde o detente trava.** 0,16 mm de interferência num aro de 0,80 mm de PP é
  firme; se ficar duro demais, a correção é a mola (0,42 → 0,35), não a covinha.

## Como regerar

```bash
cd ../medicao_v2
python3 build.py     # gera os 4 STL em ../stl_v2
python3 check.py     # interferencia entre as pecas, contra a tampa, e varredura de giro
python3 mapa.py      # mapas de altura para conferir que os numeros formaram
```

## O pino passante — por que ele existe e o que ele custa

A travinha antiga estalava numa canaleta na lateral do poste. Numa pia, com o pote
ensaboado, isso solta. Agora ela tem um **pino que atravessa a válvula** e abre do
outro lado.

O que o STL da sua válvula permitiu:

| | |
|---|---|
| chapa maciça no eixo | **1,83 mm** (Y 35,40 → 37,23) |
| ar livre embaixo, até o fundo do poço da tampa | **3,25 mm** |
| o pino passa da chapa | 1,40 mm |
| ainda sobra até a tampa | 1,85 mm |

**O furo não estraga a vedação.** Medido no corte das 12 h: a válvula fecha contra um
ressalto que cerca o respiro Ø8,12, com **0,20 mm** de folga em repouso. A cavidade
debaixo da válvula já respira para fora pela folga de **0,22 mm** em volta do disco
Ø38,09 dentro do alojamento Ø38,54, mais as fendas das orelhas. Ou seja: o espaço que
o furo abre já era ligado ao lado de fora. A fronteira vedada é pote ↔ respiro ↔
ressalto ↔ ponta de 12 h da válvula, e nada disso fica a menos de 8 mm do eixo.

**O gangorra continua igual.** Basculando de −3,6° a +3,6° em torno do eixo das
orelhas (pivô em Y 34,69, meia altura medida no seu STL), a curva de interferência
contra a tampa do conjunto novo é **idêntica** à da válvula original em todos os
ângulos. O eixo do pino fica **em cima** da linha de pivô, então ele gira mas não
sobe nem desce.

**É montagem única.** O ombro da farpa volta a **90°**. Empurra uma vez e não sai
mais com a mão — que é o que "não perder na pia" quer dizer. Se quiser que seja
desmontável, o ombro a 45° resolve, ao custo de soltar com um puxão firme.

**Um undercut a menos no molde de M01.** O rebaixo de estalo ficava na *lateral de
fora* do poste — undercut, pedia gaveta ou arranque forçado. O poste agora é reto e
o furo é pino de macho reto. O molde ficou mais simples do que era antes do pino.

**Higiene.** O canal de Ø3,10 no meio do pino fica **aberto em cima e embaixo**: água
entra por cima, atravessa e escorre. Cavidade cega que junta água é o que não pode.

## As duas versões da ponteira

A ponteira passou a ler **as duas escalas**, e por isso o índice fixo ▼ que ficava na
válvula **saiu**. Como os dias são fixos na válvula, o ângulo da ponteira escolhe o
dia; o aro gira até o mês pedido cair sob ela. Continuam dois graus de liberdade
independentes, agora numa linha de leitura só.

| | `M03a` M / D | `M03b` rasgo |
|---|---|---|
| largura da lâmina | **3,20 mm**, cintura de 0,90 sobre a faixa do mês | **5,40 mm** |
| abertura | nenhuma | **rasgo 3,40 × 9,40**, de r 8,30 a 17,70 |
| lê o **dia** | ponta em r 15,65, aponta de dentro — numeral inteiro à vista | numeral **enquadrado** no rasgo |
| lê o **mês** | a lâmina cobre o numeral | numeral **enquadrado** no rasgo |
| massa | 0,12 g | 0,13 g |
| Ø | 21,95 | 25,40 |

**A diferença que decide.** Uma lâmina cheia não consegue mostrar o numeral em que
está por cima — ela tem 3,20 mm e o numeral do mês tem 1,4 a 2,8. Na `M03a` a cintura
de 0,90 mm reduz o estrago: os meses vizinhos aparecem dos dois lados e você lê como
lê ponteiro de relógio ("está entre o 2 e o 4, logo é 3"). Funciona, mas é inferência.
Na `M03b` o rasgo **enquadra** os dois numerais de uma vez — mês na ponta de dentro,
dia na de fora, `M` e `D` gravados nas extremidades. É o jeito do calendário de relógio,
e é o que eu recomendo.

O dia, nas duas, é lido igual de bem: a `M03a` aponta de dentro sem cobrir, a `M03b`
enquadra.

## O ícone da Nitron

Extraído em **vetor** do `icone_nitron.pdf` (3 lâminas, sem rasterizar), **7,00 mm** de
altura, **gravado 0,25 mm** no cubo da ponteira. Traço mais fino: **1,68 mm** — cinco
vezes o traço dos números, então é o detalhe mais seguro do molde inteiro.

Gravado e não em relevo por dois motivos: o topo da ponteira continua **raso em Y 38,95**
(o que preserva a folga de 0,77 mm até o aro de empilhamento da tampa e faz a peça
imprimir apoiada no plano inteiro), e logo gravado numa peça que roda na mão pega
sombra em vez de pegar pancada.

O cubo é **maciço**: ele fecha o topo do canal do pino. A água que entra pelas fendas
sai pelos **quatro drenos radiais de 0,30 × 0,25** na face de baixo do cubo e pelo
fundo aberto do pino. Não há cavidade cega.

## Revisão depois do primeiro protótipo montado

Três coisas mudaram por causa da peça na mão, e uma quarta apareceu na conta.

### Rodinha do mês: 0,80 → **1,60 mm** (o dobro)

E para caber, ela **afunda 0,60 mm num rebaixo** aberto na válvula (r 6,80–13,60).
O numeral do mês passou de relevo para **gravado**, o que devolve mais 0,30. Só assim
o dobro coube. Os entalhes de unha ficaram **0,75 mm de fundo** e agora a rodinha
sobra **1,02 mm** acima da face da válvula — dá para girar com a unha de verdade.

### Ponteira: 0,80 → **1,60 mm** (o dobro), lâmina em **gota**

Desenho do cliente. A lâmina é o **fecho convexo de dois círculos** no eixo radial:
uma cabeça de **Ø16,40** com centro **1,00 mm atrás** do eixo, e um nariz de **Ø4,20**
com centro em r 16,80 — ponta em **r 18,90**. O rasgo afina junto com ela.

**Uma cota do desenho não fechou.** O esboço trazia ponta em agulha. Medindo:

| ponta | borda do rasgo em r 15,00 | em r 16,65 | em r 17,50 |
|---|---|---|---|
| agulha (Ø1,4) | 0,70 | 0,16 | **−0,11** |
| nariz Ø2,8 | 1,01 | 0,51 | 0,15 |
| **nariz Ø4,20** | **1,41** | **0,96** | **0,73** |

Com ponta em agulha o rasgo fica **mais largo que a própria lâmina** em r 17,50 — a
borda deixa de existir, que é exatamente o defeito que a gota veio corrigir. Nariz de
Ø4,20 segura 0,73 mm de borda do começo ao fim e a silhueta continua sendo uma gota.

### Circunferência central: Ø10,80 → **Ø13,20**

O poste cresceu, o furo passante foi de Ø5,00 para **Ø6,00**, o pino de Ø4,80 para
**Ø5,80** e o cubo da ponteira de Ø12,60 para **Ø15,20**. Encaixe mais folgado de
montar e pino bem mais rígido, com o mesmo 0,40 de encaixe radial da farpa.

### ⚠️ O conjunto ficou 0,23 mm acima do aro de empilhamento

Da face da válvula (Y 37,23) até o aro de empilhamento da tampa (**Y 39,72**) existem
**2,49 mm**. Rodinha e ponteira no dobro pedem 1,60 + 1,60 + folgas = **3,4 mm**.

Rebaixo de 0,60 + numeral gravado de 0,30 devolveram **0,90 mm**. Sobrou faltando
**0,23 mm**: o conjunto termina em **Y 39,95**.

Na prática isso significa que o datador vira o ponto mais alto da tampa por 0,23 mm.
Se a base do pote que empilha em cima tiver qualquer rebaixo central — e quase toda
base tem — não muda nada. Se tiver que ficar rente, as saídas são:

| Saída | Custo |
|---|---|
| ponteira 1,60 → **1,35** | continua 69% mais grossa que a original |
| rodinha 1,60 → **1,35** | idem |
| rebaixo 0,60 → **0,85** | chapa da válvula cai de 1,83 para 0,98 mm no anel r 6,8–13,6 |

Eu não escolhi sozinho porque quem sabe como o seu pote empilha é você.
