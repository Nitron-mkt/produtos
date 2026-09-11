# Família MODULA — organizador modular encaixável/empilhável

**rev.25** — **em cima, não dentro.** Dois P acoplados pousam **em cima** de um M e três P em cima de um G. O P vira uma **caixa de parede reta (0,5°)**, borda de 7 mm e **rodapé de 3 mm que cai na boca do grande** — caixa sobre caixa, sem pé, coluna ou pino. A frente do M ganha um **pilar** (dois vãos) e a do G dois (três vãos), um vão sob cada P; cantos na altura cheia nos três. **G encolhe para 582 × 295 × 360.** O P deixa de ninhar. A pendura da rev.21–24 sai.

**rev.24** — a cadeia inteira fecha: **acoplador macho/fêmea nas laterais de P, M e G**; dois P acoplados pousam no aro de um M e dois M (girados, frente com frente) no de um G, **travados por postes em T que sobem do aro do grande** e entram na fêmea que o pequeno já tem na saia. **Correção estrutural**: o aro só existe onde a borda é alta — o aro em L na frente rebaixada atravessava a parede da peça de baixo no ninho em 10 mm desde a rev.01, e o teste de ninho nunca olhou o aro. Larguras inalteradas.

**rev.23** — o **P abre pelo lado curto** (frente de 192 mm, 289 de profundidade), como os cestos de referência; acopladores nos lados longos, fileira com passo 192; macho reduzido a 4,0 mm para caber no módulo de 200.

**rev.22** — **acoplador lateral no P**: macho em T e fêmea em ranhura na saia do aro, espelhados nas duas laterais; dois P se ligam lado a lado com passo = X exato.

**rev.21** — o encaixe cruzado decidido: **dois P penduram pela aba no aro de um M, dois M no de um G** (caminho C). Cotas viraram cadeia de pendura (289 × 192 / 390 × 295 / 596 × 396), abas 12,9 / 12,4 / 11,6, altura = X / φ. Conferido por `pendura()` em toda build.

Estudo 3D paramétrico de **3 moldes** (P, M, G) para uma linha de organizadores de
frente aberta que **encaixam quase colado no transporte** e **plugam um sobre o outro
no uso**, formando andares. Dez peças ninhadas ocupam menos altura que três plugadas.

> STL, GLB (celular), pranchas de vistas e giro em `out/`. A malha serve para forma, medida e impressão 3D; não é estanque para usinagem.

Dossiê interativo (visualizador 3D, mecânica, ficha, riscos):
https://claude.ai/code/artifact/a7b943a0-a481-40ef-9798-b0c76dc870f0

## Os três tamanhos

| | Externo (mm) | Cesta + perna | Parede | Aba | Massa PP | Capacidade | Passo pilha | Passo ninho | Cubagem (10) | Fechamento |
|---|---|---|---|---|---|---|---|---|---|---|
| **P** | 192 × 289 × 179 | 176 + 3 | 1,8 mm | 7,0 | 297 g | 8,1 L | 176 mm | não ninha | — | 170–226 tf |
| **M** | 390 × 295 × 241 | 191 + 50 | 2,0 mm | 12,4 | 491 g | 15,2 L | 199 mm | 17,2 mm | 6,1× | 352–469 tf |
| **G** | 582 × 295 × 360 | 310 + 50 | 2,3 mm | 12,4 | 827 g | 35,3 L | 318 mm | 19,5 mm | 6,7× | 525–700 tf |

Desde a rev.25 as cotas fecham **em cima**: X do grande = n × 192 + 6 e Y = 289 + 6, com
n = 2 para o M e n = 3 para o G, 3 mm de folga por lado entre a fileira de P e o aro do grande.
A altura segue φ (H = X / 1,618). O passo de ninho é conferido em toda build contra a malha real, para a peça
2 e para a peça 3; o passo de pilha inclui os 3 mm que o rodapé afunda no canal.

## Contra as peças de referência

Medidas tiradas da fita nas fotos (≈24 px/cm, erro de ~10%) — **não do paquímetro**:

| Referência | Medida na foto | MODULA | Diferença | Vazado da parede |
|---|---|---|---|---|
| laranja (pequena) | ≈ 26 × 20 cm | **P** 30 × 20 | +4 cm na largura | fechado, furo de 6 mm |
| preta média | ≈ 41 × 34 cm | **M** 40 × 30 | −1 e −4 cm | meio, furo de 10 mm |
| preta grande | ≈ 73 × 49 cm | **G** 60 × 40 | **−13 e −9 cm** | aberto, furo de 16 mm |

**Por que o G não seguiu os 73 × 49.** Ele não fecha palete: em 1200 × 800 cabem duas peças
e sobram 26 cm de faixa morta — 22% da camada jogada fora. Já 600 × 400 entra quatro vezes
sem sobrar nada, e é o que faz a grade 1 : 2 : 4 funcionar. Se o tamanho da referência for
inegociável, a família inteira sobe para `350 × 250 / 500 × 350 / 700 × 500`: a modularidade
se mantém, mas nenhum dos três fecha palete.

### Vazado por tamanho

A parede dos três leva o mesmo pattern (rev.19); o que muda é a **alma mínima** entre furos,
`graf_alma` em `TAMANHOS`: 4,2 mm no P, 4,0 no M, 4,5 no G — e é ela que fixa a escala do
grafismo. O fundo, sim, fecha mais no P (vão de 9 mm) e abre no G (22 mm).

## A saia, no lugar do pezinho

A rev.05 tinha quatro pés achatados colados na base: resolviam o encaixe e não faziam mais nada.
Agora a **parede continua para baixo por 50 mm, com a mesma conicidade**, recortada em arcos.

- Como a conicidade é a mesma, a saia **ninha junto com o corpo** — não custa um milímetro de cubagem.
- Nas 4 posições de apoio ela **se abre para fora conforme desce**, até alcançar o envelope na
  base: é ali que pousa na crista da peça de baixo.
- Resultado: **5 cm de vão entre os andares** (dá para enfiar a mão e pegar o que está embaixo),
  a peça sai do chão, e o apoio é distribuído em toda a volta em vez de quatro pontos.

O único cuidado de projeto: a saia da peça de cima desce exatamente até o topo da de baixo — nem
um milímetro a mais, senão roubaria volume útil de quem está embaixo.

## A lei da cubagem

Ninho fundo e encaixe pequeno são grandezas **inversas**:

```
passo do ninho = espessura / tan(saída)
avanço do pé   = altura × tan(saída)
-------------------------------------------------
passo × avanço ~ espessura × altura   (constante da peça)
```

No M isso dá 2,0 × 200 = **400 mm²**. Com 5° o ninho parava em 27 mm; com 10° fechava em
14 mm, mas a peça ficava afunilada demais para a referência. **7,5° é o ponto de equilíbrio**:
ninho de 17 mm, cubagem de 5,6× e um perfil parecido com o das peças reais.

| | 5° | 7,5° (adotado) | 10° |
|---|---|---|---|
| passo do ninho (M) | 27 mm | **17 mm** | 14 mm |
| 10 peças ninhadas | 444 mm | **355 mm** | 330 mm |
| cubagem (10 peças) | 4,5× | **5,6×** | 6,1× |
| capacidade (M) | 16,2 L | **15,9 L** | 14,9 L |
| avanço do pé (M) | 34 mm | **40 mm** | 49 mm |

### O raio do canto é constante em toda a altura

Com 10° de saída, um contorno gerado por offset puro teria raio negativo na base. O
`Contorno` mantém o **raio fixo** e move só os centros dos arcos. Efeito colateral bom: a
superfície do canto fica mais inclinada que a dos lados (1,41× no vértice a 45°), então
quem manda no passo do ninho continua sendo o trecho reto da lateral.

## A mecânica — pé por fora, crista no aro

O aro corre `h_ress` abaixo do topo e **sobe em quatro pontos**, formando cristas com
rampa suave dos dois lados. Na base, quatro pés avançam para fora, além da saia do aro.

```
MODULA M:  cristas em y = +98 e -41      descidas em y = +41 e -98
           folga do giro 26 mm           o pé avança 40 mm da parede
```

- **Alinhada (0°)** → cada pé pousa numa crista e a abraça; a rampa centraliza sozinha:
  **pluga**. Passo = altura da peça.
- **Girada (180°)** → os pés caem nas posições espelhadas, onde o aro está na altura
  normal, e **descem por fora da peça de baixo**: **ninho**. Passo = `e / tan(5°)`.

É o "por fora" que liberta a borda. Na rev.02 o pé descia por dentro e por isso precisava
de uma janela rasgada no aro — quatro buracos que faziam a peça parecer solta. Agora nada
atravessa o aro: a borda de cima é uma peça só, arredondada, contínua, e é também a pega.

Como o contorno cresce por **offset** (e não por escala), o trecho reto da lateral tem o
mesmo comprimento em qualquer altura: o pé da peça de cima cai exatamente sobre a crista
da de baixo, sem correção.

### A regra que governa a peça inteira

A **parede é lisa por fora**: todo o vazado é coplanar, nenhum relevo. É que a parede da
peça de cima desliza rente à de baixo no ninho — um friso horizontal de 2 mm já trava a
peça a meio caminho. Esse é o erro que aparece na maioria das caixas que "quase" encaixam.

As duas exceções são as pontas: o **aro**, que no ninho fica sempre acima do aro da peça
de baixo, e os **pés**, que passam por fora de tudo. São os dois únicos lugares onde a
peça pode ter volume.

Consequência: **nenhum recurso exige gaveta no molde**. Pé, crista, rasgo de ventilação,
grelha do fundo e aro saem todos na direção de abertura.

## rev.07 — o pé, e o que ele revelou

Refazendo o pé (varredura de referência: perna cônica, pé em bracket, base em
plinto recuado), a conta de colisão do encaixe mostrou que **o mecanismo das
rev.03–rev.06 não ninha**. Não é questão de acabamento: é geometria.

### A prova

O pé precisa terminar no envelope (raio 198,5 mm no M) para pousar na crista do
aro. O corpo, na altura do pé, está no raio 152 mm. Então **existe material do pé
percorrendo todos os raios entre 152 e 198,5 mm** — inclusive a faixa 184,6–195 mm,
que é exatamente onde mora o aro.

Ao encaixar girado, a peça de cima desce e essa faixa do pé passa pela altura do
aro da peça de baixo. Amostrando o perfil do pé do M em 71 pontos, **19 caem
dentro da faixa radial do aro**. A peça trava com as duas ainda a ~225–245 mm de
distância — nunca chega perto do passo de 17 mm.

### Por que isso é geral, e não um erro de ajuste

Para empilhar com passo cheio, o pé tem de alcançar o aro (raio grande). Para
ninhar, o pé tem de descer por fora. Entre o corpo (raio pequeno) e o pé (raio
grande) existe obrigatoriamente material — e esse material varre a faixa do aro
em alguma altura. Como o encaixe percorre todas as alturas, sempre existe um
momento em que essa varredura coincide com o aro da peça de baixo.

A única saída sem passagem no aro seria a ligação pé↔corpo ficar nos **17 mm
finais do topo da peça** (a única faixa que nunca desce até o aro de baixo) — o
que só acontece se o pé pendurar do aro, e aí ele não ninha em si mesmo.

**Por isso toda caixa empilha-e-ninha do mercado tem recorte no aro.** Não é
escolha estética: é consequência.

### rev.08 — o resultado é mais forte do que parecia

Refazendo a conta para **qualquer** profundidade de encaixe (não só a do ninho),
o pé de fora não passa em nenhuma:

- o pé precisa ir do raio do corpo (152 mm no M) ao raio do envelope (198,5 mm);
- portanto existe material dele em **todos** os raios entre 152 e 198,5;
- a parede da peça de baixo tem raio entre 158,3 e 184,6 — sempre dentro dessa faixa;
- o pé fica na faixa de altura `[Δ−50, Δ]`, que cruza a parede `[0, 200]` para
  todo Δ entre −50 e 250 mm.

Ou seja: **não existe Δ em que a peça de cima desça.** Não é o aro que atrapalha,
é a parede inteira. Pé que sai do vulto da peça e ninho são incompatíveis, ponto.

### O que isso liberta

O pé deixou de ser o seletor do encaixe — e com isso **deixou de ter restrição de
posição**. Não precisa mais evitar canto nem centro de face (que eram proibidos
por serem simétricos no giro de 180°), não precisa mais de largura limitada pela
folga do pé espelhado, não precisa alcançar o aro.

Por isso a rev.08 põe o pé onde a peça sempre pediu: **nos quatro cantos**,
simétrico, dentro do vulto. É o **pé de canto sobre plinto recuado** — a mesma
gramática do móvel (perna cônica + base recuada) que a varredura apontou como o
que separa "móvel" de "engradado".

| | valor (M) |
|---|---|
| rodapé | recuado 1,5 mm da parede, 10 mm de altura — a linha de sombra |
| vão livre sob a peça | 40 mm de arco contínuo, 50 mm no total até o piso |
| pé no chão | 35 mm de corda, tronco de 7° por lado |
| pé na raiz | 65 mm, com concordância circular de 11,4 mm no rodapé |
| massa | 428 g (era 472 g na rev.06) |
| ninho | 17 mm, cubagem 6,2× em 10 peças — inalterada |

Tudo sai na direção de abertura: o pé afina para baixo, o rodapé é recuo, e o
aro voltou a ser **uniforme em toda a volta** (a crista saiu junto com o
mecanismo antigo).

### rev.09 — o travamento: coluna interna e janela no rodapé

A recomendação da rev.08 (caneluras na parede) **não fecha**, e vale registrar
por quê. Uma canelura de profundidade constante acompanha a conicidade da
parede, então desloca o degrau e o pé na mesma medida: a diferença entre eles
continua sendo a conicidade inteira. E uma canelura que se aprofunda subindo tem
menos saída que a parede, e é a canelura que passa a mandar no passo do ninho —
com a profundidade necessária (~29 mm), o passo salta para 124 mm.

O que fecha é o contrário: **coluna de raio constante**.

| | |
|---|---|
| **Coluna** | 4 colunas por dentro da parede, do fundo ao aro, nas posições `+0,90 b` e `−0,30 b` das duas laterais. A face interna é **vertical** — raio 149,8 mm no M, o mesmo raio da face interna do rodapé. Sai 4,8 mm da parede junto ao fundo e 31 mm junto ao aro. |
| **Degrau** | o topo da coluna. O rodapé da peça de cima pousa nele com a espessura inteira apoiada. |
| **Janela** | nas 4 posições espelhadas (`−0,90 b` e `+0,30 b`), o rodapé e a moldura do fundo **não existem**: é por ali que o degrau passa quando a peça está girada. |

```
alinhada  0°  -> rodapé encontra degrau            PILHA, passo 210 mm (M)
girada  180°  -> janela encontra degrau, passa     NINHO, passo 17 mm
```

**Por que sai do molde.** A face interna da coluna é vertical, então o macho sai
com quatro nervuras retas e o bolsão atrás da coluna **afunila para baixo** — é
formado por essas mesmas nervuras, que se retiram para cima. Nenhuma contra-saída,
nenhuma gaveta, nenhum postiço.

**Por que não atrapalha o ninho.** No encaixe, as três cascas ficam encaixadas
como bonecas russas: parede de baixo (158,3–156,3), parede de cima (156,0–154,0),
coluna de baixo (151,8–149,8). A folga crítica é a última — 2,3 mm no M.

**Por que o aro continua fechado.** O degrau está no aro, mas a peça que desce
nunca chega ao aro da de baixo: no ninho ela para 17 mm acima, e na pilha ela
pousa antes. A borda de cima segue anel contínuo, sem um recorte.

**O que a pilha custa.** Passo de 210 mm numa peça de 250: as peças **entrelaçam
40 mm**. Não se perde volume — perde-se altura de pilha, e ganha-se travamento
lateral, que é o que faz torre de três não balançar.

| M | valor |
|---|---|
| passo da pilha | 210 mm (peça de 250) |
| passo do ninho | 17 mm — cubagem 6,2× em 10 peças, inalterada |
| massa | 421 g (era 428 na rev.08: a janela devolve o que a coluna gasta) |
| capacidade | 15,8 L |
| folga do degrau | 2,3 mm |
| recuo do rodapé | 5,2 mm — a linha de sombra, e a folga do degrau, são a mesma coisa |

### rev.10 a rev.12 — o vazado vira o grafismo da marca

As rev.10 e rev.11 tentaram deduzir o desenho medindo o PNG do logo. As duas
erraram, e a segunda errou com confiança. A rev.12 foi buscar o **vetor
oficial**.

#### A fonte

`marca.nitron.com.br` → `nitron-logos.zip` → **`nitron-mark.svg`** (cópia em
`grafismo/nitron-mark.svg`). O símbolo tem três elementos — um longo e dois
curtos — e todos são a **mesma faixa dobrada**.

Cada elemento é um contorno de seis trechos: reta curta na ponta, curva de
concordância (o **cotovelo**), reta longa, reta curta na outra ponta, outra
curva, reta longa de volta. As duas retas longas são **paralelas** — é uma faixa
de largura constante com uma dobra no meio. Não é lente (rev.10), não é grão com
linha de centro em S (rev.11): é a **junção**, que é a ideia do grafismo.

#### A conferência

| elemento do PNG oficial | vetor | escala | **IoU** |
|---|---|---|---|
| 75 × 40 px | curto | 1,533 | **0,970** |
| 127 × 75 px | longo | 1,564 | **0,977** |

Mesma escala, mesmos dois elementos: **o grafismo é o símbolo repetido, e nada
mais.** Foi isso que fechou a questão — antes disso eu estava ajustando uma
forma inventada até parecer.

#### A rede

Tirada da própria marca, que já mostra a junção:

```
lado = ponta do 3º elemento − ponta do 2º = (−40,80 ; −25,47)   |v| = 48,10
eixo = ponta a ponta do elemento          = ( 15,42 ; −47,61)   |v| = 50,04
```

`lado` é o passo de uma faixa para a vizinha; `eixo` repete a faixa ao longo de
si mesma. Com `eixo` puro as faixas se emendam ponta com ponta e viram fitas
contínuas — na marca elas têm folga, e é essa folga que separa um elemento do
outro. Por isso os dois passos entram multiplicados por um fator, que na peça
também paga a alma entre os furos.

`grafismo/conferencia-grafismo.png` põe o grafismo oficial ao lado da
reconstrução com esses parâmetros.

#### Na peça: composição linear, furo diagonal (rev.13)

O vazado antigo era **linear** — colunas e fileiras alinhadas, ritmo regular. A
rev.12 trocou isso por uma rede oblíqua tirada da marca, e o resultado ficou
espalhado, sem a disciplina do modelo antigo. A rev.13 volta à **grade
alinhada** e põe o elemento da marca dentro dela, na diagonal.

```
t1 = (pu ;  0)      colunas, como no vazado antigo
t2 = ( 0 ; pz)      fileiras
eixo do elemento    -55 graus
```

Colunas e fileiras vizinhas ficam lado a lado; os elementos da **diagonal**
ficam ponta com ponta, na direção do próprio elemento. É isso que forma as
linhas diagonais tracejadas e mantém a composição linear —
`grafismo/padrao-na-parede.png`.

**Por que −55° e não −45°.** Varrendo eixo × tamanho × passo, a −45° a alma cai
para 4,4 mm no mesmo vazado em que a −55° dá 6,9 mm: quanto mais o eixo do furo
se aproxima da diagonal da célula, mais os vizinhos da diagonal se aproximam
ponta a ponta. E −55° fica mais perto dos −72° do logo, então é também o menor
desvio da regra do guia.

| | P | M | G |
|---|---|---|---|
| furo (compr. × largura) | 30 × 10,1 mm | 40 × 13,5 mm | 60 × 20,2 mm |
| grade (colunas × fileiras) | 29 × 5 | 32 × 6 | 32 × 5 |
| passo | 24,3 × 21,1 | 32,2 × 25,0 | 48,5 × 38,9 |
| vazado | 40,9% | 46,3% | 44,4% |
| **alma mínima** | **7,0 mm** | **6,9 mm** | **11,5 mm** |
| massa | 211 g | 433 g | 1.012 g |

⚠️ **O guia da marca diz que o grafismo "usa a mesma inclinação do logo e nunca
é rotacionado".** O eixo do elemento no logo está a −72°, quase vertical — que é
o vazado que esta revisão veio substituir. A peça está a −55°, um giro de 17°.
`graf_eixo_gr` em `TAMANHOS` é o número que controla isso: `-72.05` devolve a
inclinação exata da marca.

**Como a casca é emitida.** `perfurada()` em `geometria.py`: para cada tira do
contorno, acha os trechos sólidos no meio da tira e refina as bordas por
bisseção **nas duas colunas**. É isso que faz a borda do furo sair curva em vez
de escadinha, sem precisar de malha fina. O intervalo caminha para fora a partir
do centro em vez de saltar até os limites — saltando, uma coluna com dois furos
devolvia um intervalo atravessando o furo do meio.

**O que não mudou.** O vazado continua **coplanar** — nenhum relevo por fora,
senão o ninho trava a meio caminho. Coluna e painel de etiqueta ficam cheios: a
coluna é poste de carga da pilha, não pode ser furada. `grafismo.py` não depende
de nada além de `math`.

### rev.14 — a modulação dos três tamanhos (proporção áurea)

#### A restrição que decide tudo: o palete

Medi cada pegada candidata contra os dois paletes que a Nitron usa:

| pegada | PBR-1 (1000 × 1200) | europeu (800 × 1200) |
|---|---|---|
| **300 × 200** | 20 pç · **100%** | 16 pç · **100%** |
| **400 × 300** | 10 pç · **100%** | 8 pç · **100%** |
| **600 × 400** | 5 pç · **100%** | 4 pç · **100%** |
| 500 × 300 (3:5, o mais áureo) | 8 pç · 100% | 6 pç · 94% |
| 500 × 400 | 6 pç · 100% | 4 pç · 83% |
| 450 × 300 | 8 pç · 90% | 6 pç · 84% |

As três pegadas atuais são **as únicas que fecham os dois paletes a 100%** — e
não por acaso: elas são a série modular do palete, cada uma metade da área da
anterior. A pegada áurea mais próxima (500 × 300 = 1,667) perde 6% de cada
palete europeu, para sempre, em todo frete.

**Então a razão áurea não pode entrar na planta.** Ela entra na altura.

#### Onde φ cabe de graça

Altura não muda a pegada nem a área projetada — logo não muda nem o palete nem a
tonelagem da injetora. É o único eixo livre. A proposta põe φ na **face frontal**,
que é justamente a proporção que se vê na gôndola e em casa:

| | cm (X × Y × H) | face X:H | litros | massa |
|---|---|---|---|---|
| **P** | 30 × 20 × 18,5 | **1,622** | **4,9 L** | 237 g |
| **M** | 40 × 30 × 24,5 | **1,633** | **15,4 L** | 491 g |
| **G** | 60 × 40 × 37,0 | **1,622** | **52,1 L** | 1.116 g |

φ = 1,6180 — as três faces ficam dentro de 1% dele.

O G cai em **600 × 400 × 370**, que é altura de caixa-padrão de mercado; o M em
400 × 300 × 245, entre os padrões de 220 e 270.

#### O que φ **não** consegue ser ao mesmo tempo

As razões de volume saem **3,18×** e **3,38×**, não φ² = 2,618. Não é ajuste
malfeito, é aritmética: a pegada **dobra de área** a cada degrau (é o palete que
manda), o que já põe 2,00 na conta; a altura cresce junto com X para manter a
face áurea, e a conicidade ainda adiciona volume no topo.

Para os volumes andarem em φ² seria preciso **30 × 20 × 22,2 / 40 × 30 × 24,5 /
60 × 40 × 28,5** (5,9 / 15,4 / 40,4 L) — e aí as faces viram 1,35 / 1,63 / 2,10,
o P fica quase tão alto quanto o M e o G fica achatado. A família perde a
hierarquia visual para ganhar uma razão que ninguém enxerga. Não recomendo.

**Dá para ter φ na face ou no volume, não nos dois** — porque a planta está presa
ao palete.

#### O que a altura nova compra

| | col. em 1,9 m | pç/palete (ninhadas) | litros/palete | vs. empilhado |
|---|---|---|---|---|
| P | 110 | 2.200 | 10.673 L | 8,5× |
| M | 97 | 970 | 14.962 L | 10,8× |
| G | 79 | 395 | 20.596 L | **15,8×** |

Um palete de MODULA G leva **20,6 m³ de capacidade** — contra 25 peças se fossem
empilhadas em vez de ninhadas.

Torre de três: P 47,5 cm · M 65,5 cm · G 103 cm.

### rev.15 — o 3D: STL e visualizador

#### Duas cotas que estavam erradas na peça

Gerando o STL, a caixa envolvente não bateu com a ficha: o P saiu
287,4 × 177,9 × **176,7** em vez de 300 × 200 × 185. Eram dois resíduos de
mecanismos que já tinham saído do projeto:

| | era | por quê | virou |
|---|---|---|---|
| `folga_pe` | 5,0 mm | folga para o pé passar **por fora** do aro — mecanismo aposentado na rev.08 | **0** |
| `h_ress` | 7 + 0,010·H | reserva de altura para a crista de apoio — aposentada na rev.09, quando a coluna interna passou a travar a pilha | **0** |

O `folga_pe` recuava o aro 5 mm de cada lado (a peça nascia 10 mm mais estreita
que a ficha) e o `h_ress` cortava 8,3 mm da altura — e, como o aro descia numa
parede cônica, ainda tirava 1,3 mm de cada lado. Zerados os dois, **X, Y e H
passam a ser as cotas reais da peça**, não um envelope.

A cesta ganhou 10 mm em cada direção: P foi de 4,9 para **5,4 L**, M de 15,4
para **16,5 L**, G de 52,1 para **54,7 L**.

#### A caixa envolvente medida no STL

| | X | Y | H |
|---|---|---|---|
| P | 299,6 | 189,0 | 185,0 |
| M | 399,6 | 284,2 | 245,0 |
| G | 599,6 | 374,8 | 370,0 |

Os 0,4 mm que faltam em X são o ponto mais externo do aro estar 1,6 mm abaixo do
topo, numa parede com 7,5° de saída. **O Y é menor de propósito**: a frente é o
rebaixo de pega, e como ela fica mais baixa numa parede cônica, recua 11 mm
(P), 16 mm (M) e 25 mm (G). A peça continua dentro do seu módulo de palete — ela
só não encosta na aresta da frente.

#### Os arquivos

`python3 exporta.py stl` grava em `out/`:

| | triângulos | arquivo | arestas abertas |
|---|---|---|---|
| `modula-P.stl` | 28.276 | 1,4 MB | 1,70% |
| `modula-M.stl` | 39.020 | 2,0 MB | 1,67% |
| `modula-G.stl` | 55.896 | 2,8 MB | 1,29% |

STL binário, **1:1 em milímetros**, normal por face orientada para fora.

⚠️ **Não é um sólido estanque.** As bandas da casca se sobrepõem nas emendas e
1,3 a 1,7% das arestas ficam ímpares. Serve para conferir forma, medir e
imprimir com reparo automático — **não** para usinar direto. A ferramentaria
reconstrói o sólido a partir das cotas, como faria de qualquer jeito.

#### O visualizador

`gera_visor.py` (no scratchpad) monta uma página com a malha embutida — três
tamanhos, três arranjos (peça, pilha, ninho), três cores — e a ficha completa ao
lado. A malha do navegador usa `AMOSTRA = [5.8, 7]`, mais grossa que a de
produção; as cotas da ficha vêm da malha fina.

### rev.16 — saídas para celular

O visualizador em página não abre em qualquer aparelho. `celular.py` gera três
formatos que abrem:

| arquivo | o que é | onde abre |
|---|---|---|
| `modula-{P,M,G}.glb` | glTF binário, **Y para cima e em metros** | Android abre direto; iPhone precisa de app; qualquer visualizador 3D |
| `modula-M-giro.gif` | 30 quadros, volta completa | galeria de qualquer celular |
| `modula-{P,M,G}-vistas.png` | prancha de 6 vistas com a cota no topo | galeria de qualquer celular |

O GLB sai da malha média (`AMOSTRA = [4.6, 9]`, 16 a 32 mil triângulos) — leve o
bastante para girar no telefone. As pranchas usam `[3.4, 10]`, e a cota impressa
no cabeçalho vem da **malha de produção**, não da malha do desenho: massa medida
em malha grossa erra para mais.

`python3 celular.py` refaz os três.

### rev.17 — varredura no M, replicada nos três

Trabalho feito no M e propagado por parâmetro. Cinco achados; o quarto é um
defeito de encaixe, não de acabamento.

#### 1. O pé apoiava numa aresta de 2 mm

A casca do pé descia aberta: o contato com o piso era o fio da parede, 35 mm de
corda × 2 mm. **2,8 cm² nos quatro pés.** Fio de faca no piso, e pouca área para
a pilha.

Agora o pé fecha numa **sola** — laje na boca do pé, recuada 0,6 mm da face
externa (o recuo mata o fio) e avançando para dentro:

| | corda do pé | sola | **apoio** |
|---|---|---|---|
| P | 38 mm | 6,6 mm | 10,0 cm² |
| M | 66 mm | 8,8 mm | **23,1 cm²** |
| G | 92 mm | 13,2 mm | 48,8 cm² |

No M são **8,2× mais área**. A sola morre em rampa nas duas pontas, não em
degrau.

#### 2. A janela do rodapé estava mordendo o pé

As colunas ficavam em `0,90 b` e `0,30 b`. A janela que deixa o degrau passar
tem meia-largura de `w_col/2 + rampa`, e nessa posição ela começava a **10,8 mm**
do centro do canto — dentro dos 17,7 mm do pé. A janela comia a borda da área de
apoio.

As colunas recuaram para **`0,72 b` e `0,24 b`**. Os três vãos do giro continuam
iguais (a regra `p1/3`), e a janela sai de perto do canto. Além disso a largura
do pé deixou de ser fração fixa: agora é **medida a partir da janela**, com 4 mm
de folga, e tem `assert`.

#### 3. O grafismo saía cortado ao meio nas duas bordas

O elemento tem 36 mm de altura (deitado a −55°) e o passo entre fileiras é 29,5
mm: as fileiras se entrelaçam, e as das pontas eram fatiadas pelas faixas cheias
do topo e do pé.

Agora as fileiras andam entre os **centros extremos**, recuados meia altura de
elemento de cada faixa (`Trama.jmin/jmax`). **Nenhum elemento sai cortado.**

#### 4. A coluna cegava um pedaço largo da lateral

Painel cego de `w_col + 2·rampa` = 27,4 + 14 = **41,4 mm**. Estreitou para
19,4 + 11 = **30,4 mm** (−27%), sem perder o degrau: o apoio da pilha continua
sendo a espessura da casca, e 4 × 19,4 × 2 mm bastam para a carga de três caixas.

#### 5. A grelha do fundo era ortogonal

Toda a peça fala diagonal e o fundo falava xadrez. A grelha passou a correr a
**45°**, nas duas mãos (`Malha.viga`, barra reta em qualquer direção). Mesma
linguagem do vazado, e a água escorre para o canto em vez de empoçar na trama.

**O que não mexi.** A janela do rodapé continua aparecendo como quatro entalhes
na base — é o mecanismo, não tem como fechar. O perfil de três degraus do aro e a
faixa cheia sob o rebaixo da frente ficaram como estavam.

**Sobre a cota em Y.** A ficha diz 40 × 30 cm e a caixa medida no STL dá
399,6 × 284,2 mm. Não falta peça: 300 mm é a planta **no aro**, e a frente é
rebaixada 117 mm para a mão entrar. Com os 7,5° de saída do ninho, 117 mm de
queda recuam a boca da frente em 15,4 mm. O fundo do palete continua sendo
400 × 300.

| M | antes | depois |
|---|---|---|
| apoio no piso | 2,8 cm² | **23,1 cm²** |
| painel cego da lateral | 41,4 mm | 30,4 mm |
| grafismo cortado | sim | não |
| massa | 471 g | 465 g |
| litros | 16,5 | 16,5 |

### rev.18 — segunda varredura: o ninho era impossível, e a base não saía do molde

A varredura da rev.17 mediu na malha. Esta mediu **o encaixe** — girando a peça 180°,
subindo o passo e testando vértice a vértice contra a peça de baixo. Dois erros graves
que nenhum render mostrava, seis melhorias.

#### 1. O ninho de 17 mm não existia

O passo do ninho vinha da parede (espessura ÷ tan 7,5° = 17,2 mm). Mas a perna tem 50 mm,
e o pé de canto era uma casca fechada por fora e aberta para o vão. Girada e descida 17,2 mm,
a peça de cima **atravessava o fundo da de baixo**:

| ninho girado, M (rev.17) | |
|---|---|
| vértices do pé abaixo do topo do fundo da peça de baixo | 3.302 de 11.016 |
| até onde o pé descia | 17,2 mm do chão da peça de baixo (o fundo estava em 52–54,5) |
| passo real, com o pé pousando no fundo | **54,5 mm** |
| cubagem real de 10 peças | **3,3×, não 6,1×** |

O rodapé (11 mm) tinha `assert` para passar raspando o fundo. O pé, 39 mm mais fundo,
nunca foi conferido — da rev.05 à rev.17.

#### 2. O vão sob o fundo tinha contra-saída de 6,6 mm

A perna continuava a conicidade da parede para baixo. O vão interno ficava **mais estreito
no chão (150,1 mm de meia-largura) do que junto ao fundo (156,7)**: o postiço da cavidade
que o forma teria de ser mais largo na ponta do que na raiz. Sem gaveta ou macho colapsível,
a base não desmoldava — com ou sem ninho.

#### A solução dos dois: pé em copo

É a solução clássica de caixa stack-nest, e ela resolve os dois erros de uma vez. O pé
passa a ser um **copo aberto para cima**, formado pelo macho através de um recorte no canto
do fundo:

- a **face externa** do copo é a própria casca recuada da base, e sai pela cavidade (afina
  para baixo);
- as **paredes internas** são duas, ortogonais aos lados, inclinadas **7,5° para o canto
  conforme descem**: saem pelo macho (o bolsão alarga para cima) e, do lado do vão, formam
  um postiço que **alarga para baixo** — a contra-saída do item 2 desaparece;
- a **sola** da rev.17 vira o fundo do copo.

E, como todas as faces do copo têm os mesmos 7,5° da parede, **o copo de cima entra no copo
de baixo com a mesma folga que a parede tem** (`passo × tan − e` = 0,26 mm). O ninho de
17 mm voltou a existir — e desta vez está provado: `confere_ninho()` roda dentro de
`ficha()`, gira a peça, sobe o passo e exige que todo vértice da base que fique abaixo do
fundo da peça de baixo esteja dentro de um copo. **A build quebra se violar.**

| ninho girado, M (rev.18) | |
|---|---|
| vértices da base abaixo do topo do fundo da peça de baixo | 2.778 |
| fora de um copo | **0** |

O teste pegou o próprio redesenho na primeira build: eu tinha feito a parede interna do
copo 1 mm mais grossa que a parede (para a moldura sempre encontrar material), e ela
colidia — porque **essa parede só cabe se for ≤ passo × tan − 0,26 = e**. É a única peça
da caixa que não pode engrossar. O reforço foi para um colar de 1,5 mm restrito à laje do
fundo, que nunca entra no bolsão de baixo.

O custo é visível: **quatro bolsões de 39 mm nos cantos do fundo da cesta** — 40 × 40 mm
no M, 27 × 27 no P. Toda caixa stack-nest do mercado tem isso. No P de quarto infantil é
onde peça pequena vai se acumular; se incomodar, o copo do P pode ser mais raso (custa
passo de ninho).

O pé ficou como o rodapé pede: **67 mm de corda no chão, 77 no rodapé** (M), porque a
parede interna inclinada faz a corda crescer `tan 7,5°` por mm subindo. Apoio no piso:
47,9 cm² nos quatro copos (era 23,1 na rev.17, 2,8 na rev.16).

#### 3. O assento da pilha tinha 2 mm, ao lado de uma vala de 30

O rodapé (2 mm) pousava no topo da coluna (2 mm) com alinhamento exato e **tolerância
zero**: 2 mm de deslocamento e ele caía para dentro da coluna ou para dentro do bolsão
aberto atrás dela. Contração de PP em 400 mm varia mais que isso entre ciclos.

Agora o topo da coluna é um **canal**: uma **ponte** fecha o bolsão atrás da coluna até
1,5 mm da parede de cima (que passa por ali no ninho — por isso a ponte não alcança a aba),
o lábio da coluna sobe 3 mm por dentro e uma **guia chanfrada** fecha por fora. O rodapé
assenta 3 mm abaixo do aro, com **3 mm de folga para dentro e 1 mm para fora**, e o chanfro
de 45° o conduz. A face interna da coluna ganhou **0,5° de saída** (195 mm sem saída era
arrasto certo no macho).

| M | rev.17 | rev.18 |
|---|---|---|
| largura do degrau | 2,0 mm | **29,9 mm** (ponte) |
| canal onde o rodapé assenta | — | 5,7 mm, com guia chanfrada |
| tolerância lateral da pilha | ±0 | −3 / +1 mm |

#### 4. O fundo era uma treliça de 2,5 mm sem altura

Barra de 7,5 × 2,5 mm vencendo 285 mm de vão. A mesma massa em **nervura de 2,0 × 10,4 mm**
(`Malha.viga` com afunilamento de 1° por face, raiz larga, ponta fina) dá **~14× a rigidez**
por nervura — e o vão de 50 mm embaixo estava vazio à toa. O passo abriu junto (vão de 18 mm
no M, 22 no G; **9 mm no P**, que guarda coisa pequena). No ninho a ponta da nervura para
5 mm acima do fundo da peça de baixo — é mais um `assert`.

#### 5. A base estava solta do corpo

Achado no meio do caminho: o fundo começava 2 mm acima do plano do rodapé e a casca da base
terminava nele. **Nenhuma face ligava as duas.** Agora o fundo assenta no plano do rodapé e a
casca da base sobe até o topo da moldura.

#### 6. Cota externa igual ao módulo do palete

400 × 300 exatos dão zero folga para 12 peças em 1000 × 1200. Caixa modular real é 396–398
× 296–298. **X e Y baixaram 4 mm nos três.** A largura do furo no P subiu junto de 12,1 para
**13,1 mm**, saindo da faixa de aprisionamento de dedo infantil (7–12 mm, EN 71-8). A parede
do G foi de 2,3 para **2,5 mm**: relação fluxo/espessura de 231 para 213 numa parede vazada
em 46%.

#### 7. A tira dobrada no vazado

Ao mudar X de 400 para 396 a parede do M pulou de 177 para 322 g com o mesmo vazado. Era
`perfurada()`: quando a coluna vizinha era sólida onde o meio da tira tinha furo (o furo
entra em diagonal), o trecho sólido daquela coluna atravessava o furo vizinho e **duas tiras
se sobrepunham**. Dependia do alinhamento entre amostra e trama — por isso nunca apareceu
igual duas vezes. Cada trecho agora é clipado à meia-distância dos trechos vizinhos.
Conferência independente (integral do sólido × largura × espessura): **razão 0,98**.

#### O que a rev.18 custou e o que devolveu

| M | rev.17 | rev.18 |
|---|---|---|
| ninho | 17,2 mm (falso) | **17,2 mm (provado)** |
| vão sob o fundo | contra-saída 6,6 mm | saída positiva |
| apoio no piso | 23,1 cm² | 47,9 cm² |
| degrau da pilha | 2,0 mm | 29,9 mm, com canal e guia |
| rigidez do fundo | 1× | ~14× por nervura |
| massa | 465 g | 499 g |
| litros | 16,5 | 16,2 |
| externo | 400 × 300 | 396 × 296 |

Os 34 g são ~25 g de nervura e ~10 g de copo, guia e ponte. Massa comprada com função.

**O que continua aberto.** O STL segue não estanque (1,3–1,7% de arestas ímpares, das
emendas de banda). A guia do aro, a ponte e a face interna da coluna ainda não têm raio de
concordância — é trabalho de CAD, não de conceito. E o `engenheiro-molde` precisa validar
a parede do G (2,5 mm, fluxo 213:1) antes de fechar cota.

### rev.19 — o pattern oficial na parede

O arquivo `grafismo/pattern-nitron.ai` veio da marca com o grafismo pronto. Por dentro é um
PDF, e o grafismo está lá como **tiling pattern**: uma célula de **230 × 280 pt** com 19
caminhos, que se reduzem a **quatro formas** e a uma rede retangular **centrada** — o motivo
de 5 elementos se repete em (115, 140) e (230, 0) pt.

| forma | o que é | altura | por motivo |
|---|---|---|---|
| A | elemento curto, faixa de 38,9 pt | 99,7 pt | 2 |
| B | elemento longo | 184,9 pt | 1 |
| C | elemento médio | 110,0 pt | 1 |
| D | C girado 180° | 110,1 pt | 1 |

Vazado de **58,2 %**, alma mínima de **12,18 pt** (entre dois B vizinhos). Não é o elemento
único em grade alinhada que eu tinha montado nas rev.10–13: são três comprimentos, em correntes
diagonais a 65°, quase encostados.

#### Reprodução exata, conferida

Os caminhos e as posições foram lidos do próprio stream do PDF (`grafismo.TILE_FORMAS`,
`TILE_MOTIVO`). A classe `Padrao` reconstrói o ladrilho por rede; a conferência rasterizou o
ladrilho original e a reconstrução na mesma janela e comparou pixel a pixel: **0 pixels
diferentes em 515.200**. Antes disso a conferência pegou um erro meu: eu tinha trocado C e D
no motivo, e o B saía em corrente contínua.

#### A escala sai do molde

O que limita a densidade não é o desenho, é a alma entre furos. Fixei o mínimo por tamanho e
a escala veio dele: `s = alma / 12,18 pt`, depois ajustada para o período em u (230 pt × s)
dividir o perímetro — o pattern fecha a volta sem emenda.

| | alma | escala | A (curto) | B (longo) | furo | período u | fileiras | massa |
|---|---|---|---|---|---|---|---|---|
| P | 4,3 mm | 0,355 mm/pt | 35,4 mm | 65,7 mm | 13,8 mm | 81,7 mm | 2 | 250 g |
| M | 4,0 mm | 0,327 mm/pt | 32,6 mm | 60,4 mm | 12,7 mm | 75,1 mm | 3 | 476 g |
| G | 4,4 mm | 0,361 mm/pt | 36,0 mm | 66,8 mm | 14,0 mm | 83,1 mm | 5 | 1.108 g |

Elemento que ficaria com menos de **45 %** da área entre a faixa cheia do pé e a do aro não
nasce — o resto é cortado pelas faixas, como o retângulo do arquivo corta o pattern nas
bordas. Colunas do encaixe, painel da etiqueta e as duas faixas cheias continuam inteiros.

#### O que o pattern forçou no emissor

1. **Amostragem de 1,3 mm** no contorno (era 2,6). As arestas a 65° saíam em escadinha; o
   `AMOSTRA` de produção dobrou, e a malha do M foi de 40 mil para 78 mil triângulos. O
   navegador e o GLB também subiram (2,6 e 2,0 mm): o pattern não sobrevive a malha grossa.
2. **Alma oblíqua e fina.** Entre duas amostras a alma se desloca em z mais do que a própria
   altura; na coluna vizinha o centro do trecho do meio já caía no furo, `_intervalo`
   devolvia nada e dois furos viravam um só. Agora ele procura o trecho sólido **mais
   próximo** (até 9 mm) antes de desistir.

**Sobre o P.** Furo de 13,8 mm de largura — acima da faixa de aprisionamento de dedo
(7–12 mm), mas perto. Se a alma do P baixar para 4,0 o furo cai para 12,8; não baixe.

**Massa.** O pattern é mais vazado (58 % contra 43 %): P −12 g, M −23 g, G −87 g.

### rev.20 — fundo chapado no P, parede fina, e o que a conta do encaixe cruzado revelou

Pedido: duas P encaixam em cima de uma M, duas M em cima de uma G; parede fina; fundo do P
chapado, M e G vazados. Três coisas saíram direto; a quarta é decisão de conceito.

#### O que mudou

- **Fundo do P chapado** (`fundo_chapado`): laje inteira entre a moldura e os copos, com as
  nervuras diagonais por baixo. Só ficam abertas as **quatro sombras das colunas** na borda
  (~22 × 19 mm): é por ali que a coluna da peça de baixo sobe no ninho. P: 250 → **298 g**.
- **Parede do G de volta a 2,3 mm** (era 2,5). G: 1.108 → **1.040 g**. Parede fina é a
  regra da família: 1,8 / 2,0 / 2,3.
- **Coluna com 4,5° de saída na face interna** (era 0,5°). Achado no caminho: no ninho
  profundo a **peça 3** (mesma orientação da 1, dois passos acima) tem a coluna no mesmo
  raio da peça 1 — com 0,5° elas se deslocavam 0,3 mm e as duas cascas de 2 mm **colidiam**.
  O teste de ninho só olhava a peça 2. Com 4,5° o deslocamento é 2 × passo × tan = 2,7 mm
  (M) e sobra 0,7 mm. `confere_ninho` agora roda para k = 1 e k = 2, e há `assert`
  analítico (`f_col3`). Custo: a coluna sai mais da parede — 25 mm no fundo e 36 no aro (M).
- **Base sem janelas.** Com a coluna mais para dentro, o rodapé e a moldura do fundo passam
  por **fora** dela no ninho (`f_gre` = 7,0 mm no M): os quatro entalhes na base, que
  existiam desde a rev.09, **saíram**. Só a nervura é recortada na sombra da coluna.

#### O encaixe cruzado — a conta

A grade do palete já dá o módulo: dois P girados (2 × 196 = 392) cabem numa M (396); dois M
(2 × 296 = 592) numa G (596). O problema é **onde a peça pequena apoia**. Por causa dos 7,5°
que fazem o ninho de 17 mm, a base é muito menor que o aro:

| | aro | base (rodapé) | abertura do M no aro |
|---|---|---|---|
| P | 296 × 196 | **231 × 131** | 371 × 271 |

Dois P lado a lado em cima de uma M têm a base a **52 mm da parede** em x e **20 mm** em y:
cai dentro. Apoiar exige estrutura interna na M, e a regra do seletor de 180° (o que faz o
ninho) proíbe qualquer apoio simétrico ao centro — e dois P lado a lado pedem exatamente um
apoio simétrico. Só resta apoiar em **travessas entre as colunas** (as colunas são o único
lugar assimétrico permitido), e travessa dentro da cesta **não sai do molde** sem uma lâmina
de aço de ~120 mm passando pelo fundo. Divisória que sobe do fundo sai do molde, mas
atravessa o fundo da peça 3 no ninho profundo (só pode ter ~30 mm).

Três caminhos, com produto diferente em cada um:

| | como apoia | ninho | o que muda |
|---|---|---|---|
| **A. Euro-modular** | parede quase reta, base ≈ aro, pequeno apoia no aro do grande | **perde** (cubagem 1×) | joga fora colunas, copos, canal — todo o mecanismo das rev.07–18 |
| **B. Travessas** | duas travessas entre as colunas, 45 mm abaixo do aro | mantém | lâmina de aço de 120 mm no molde: o ferramenteiro vai recusar ou cobrar; o P afunda 45 mm |
| **C. Pendurado no aro** | o P (girado) **pendura pela aba** no aro do M: 8,4 mm de apoio em x, 9,8 em y, em três lados | mantém | **não muda nada** — já cabe: dois P em 392 de 396, dois M em 592 de 596; o P fica 11 mm acima do fundo do M |

O C é o que a geometria dá de graça, e é um produto real (bandeja dentro de bandeja). Mas
não é "em cima" — é "dentro, pendurado". A escolha é de conceito, não de cálculo.

**Sobre φ.** Ele já está na altura (X : H = 1,618) e é dela que sai a torre; a planta é do
palete (1 : 2 : 4). Não forcei φ na conta do apoio porque quem manda ali é a geometria do
ninho.

### rev.21 — o encaixe cruzado: pendurado pela aba

Decisão tomada: caminho **C**. Dois P girados 90° penduram pela aba no aro de um M; dois M
no de um G. Mantém o ninho de 17 mm, não mexe no mecanismo da pilha, e é o único dos três
caminhos que sai do molde sem lâmina.

#### A cadeia de pendura

Para o pequeno pendurar, a **parede** dele (no aro) tem de passar por dentro da **aba** do
grande, com folga. Isso fixa duas coisas de cada vez:

1. **A cota externa** do pequeno é o módulo do grande menos `2 s`, com `s = 3 mm` por lado:
   `Yg 396 → Xm 390`, `Xg 596 → Ym 295`, `Ym 295 → Xp 289`, `Xm 390 → Yp 192`. Todos abaixo
   do módulo de palete (300 × 200 / 400 × 300 / 600 × 400), então o palete não muda.
2. **A aba cresce para dentro** da família: `aba_pequeno = aba_grande + e_grande + folga − s`
   → G 11,6 → M 12,4 → P 12,9. É a aba maior no menor que paga a folga.

A altura é `X / φ`: 179 / 241 / 368. É onde φ mora na família, e é o que dá a torre.

#### O que `pendura()` confere (e quebra a build se falhar)

| | P em M | M em G |
|---|---|---|
| dois lado a lado no vão do grande | 384 em 390 | 590 em 596 |
| folga parede-parede, x / y | 1,5 / 1,5 mm | 1,5 / 1,5 mm |
| folga na fenda da ponte (lateral do grande) | 1,46 mm | 1,57 mm |
| apoio da saia na chapa da aba | 9,4 mm | 8,6 mm |
| aro do pequeno acima do aro do grande | 10,1 mm | 11,6 mm |
| base do pequeno acima do fundo do grande | 19,6 mm | 85,8 mm |

A fenda entre a ponte da coluna e a parede (por onde a parede da peça de cima passa no
ninho) é a mesma por onde passa a parede do pequeno pendurado: a margem da ponte subiu de
1,5 para 2,5 mm por isso.

**O que se perdeu.** O P encolheu 7 × 4 mm e 6 de altura (5,2 → 4,5 L); o M 6 × 1 e 4 de
altura (16,2 → 15,1 L). A aba maior come 2,5 mm de boca por lado no P. Fundo do P chapado,
M e G vazados, paredes 1,8 / 2,0 / 2,3 — como pedido.

**Grafismo.** A escala passou a ser arredondada para baixo no número de períodos, para a alma
nunca ficar abaixo do mínimo quando o padrão fecha a volta (o M tinha saído com 3,9 mm).

**Saídas em `out/` não foram regeneradas nesta revisão** — a pedido. `python3 exporta.py &&
python3 celular.py && python3 detalhes.py && python3 dossie_pdf.py` refaz tudo.

### rev.22 — acoplador lateral: dois P lado a lado

Pedido: as peças se acoplam uma ao lado da outra, com macho e fêmea nas laterais (exemplo:
a caixa preta com rasgos em T no aro). Por partes — primeiro o P.

**Onde pode haver relevo.** A parede é lisa por fora por causa do ninho. O único lugar da
peça onde um macho pode sair para fora é a **saia do aro**: no ninho ela fica um passo acima
da saia da peça de baixo e nunca entra em ninguém. No P a saia tem 11,7 mm — é essa a altura
útil do encaixe.

**O encaixe.** Macho em **T** saindo da saia (haste 2,6 × 4,5 mm, cabeça 2,8 × 10 mm, 5,4 mm
de saliência); fêmea em **ranhura** através da saia (5,1 mm), aberta embaixo e fechada em cima
pelo lintel, com o bolsão da cabeça dentro do oco da aba (10,8 mm de largura, 4,0 de fundo,
duas bochechas e parede de fundo de 1,8). A peça B desce sobre a A: a ranhura de B engole o
T de A. Passo entre as duas = X exato (289): as saias se tocam, a haste atravessa a saia da
vizinha e a cabeça fica no bolsão dela.

**Espelhado para qualquer P casar com qualquer P.** Lateral direita: macho em y = +0,29 b,
fêmea em −0,71 b. Lateral esquerda: o contrário. O macho direito de A entra na fêmea esquerda
de B e a fêmea direita de A recebe o macho esquerdo de B. As posições evitam as colunas do
encaixe e o rebaixo da frente.

**Limites conferidos por `assert`.** Saliência de 5,4 mm × 2 lados: 289 + 10,8 ≤ 300, ainda
dentro do módulo de palete. O bolsão (4,0 + 1,8) cabe no oco da aba de 12,9. Ninho e pilha
não mudam; na pendura o T fica em cima da aba do M (entre 141,5 e 147,5 mm do centro dele).

Massa do P: 280 → 281 g. `acoplador=True` só no P por enquanto; M e G recebem o mesmo
quando o P estiver aprovado.

### rev.23 — o P abre pelo lado curto

Correção de orientação: no P a **frente é o lado de 192 mm** e a profundidade é 289 — como
os cestos laranja da referência, e não como M e G, que abrem pelo lado longo. Consequências:

- **Acopladores nos lados longos** (289): uma fileira de P tem **passo 192**, todos de frente.
  O macho encolheu para caber no módulo: haste 2,2 + cabeça 1,8 = **4,0 mm** de saliência,
  192 + 8,0 = 200,0 = o módulo do palete. Bolsão da fêmea com 2,6 mm de fundo.
- **Colunas e copos** passam para os lados longos; b sobe de 70 para 118,5 mm e sobra espaço.
- **Pendura no M sem girar**: dois P de 192 lado a lado nos 390 do M (folga 3 por lado), a
  profundidade de 289 nos 295 (folga 3). `pendura()` agora testa as duas orientações e fica
  com a que cabe; para o M no G continua girado 90°. Folgas iguais às da rev.21.
- Massa do P 281 → 289 g (a frente rebaixada agora é o lado curto: sobra mais parede).

### rev.24 — a cadeia fecha: postes no aro, acoplador nos três, e o aro sai do mergulho

Pedido: encaixes no topo do M para travar o par de P, o mesmo no G para o par de M, e
macho/fêmea nas laterais de M e G. Antes de desenhar, duas medições mudaram o caminho.

**1. O aro da frente rebaixada atravessava a parede de baixo no ninho.** A peça de cima entra
girada 180°, então a frente rebaixada dela (aro a `hf` = 40% da altura) desce dentro da
traseira alta da peça de baixo. O aro em L ali sai 12,4 mm para fora de uma parede que está
0,26 mm dentro da parede de baixo: **10,1 mm de interferência, 22.488 vértices** no M. Está
assim desde a rev.01 — `confere_ninho()` só olhava a base. O mesmo acontecia com o M girado
dentro do G (rev.21): a frente do M cortava a lateral do G. Correção: **o aro (aba + saia)
só existe onde a borda está na altura cheia** — laterais, traseira e o começo dos cantos, até
a borda ter descido 3 mm. No mergulho a borda é a própria parede (2 mm), a arredondar no molde.
Novo teste `confere_aro_ninho()` em toda build: 0 vértices do aro dentro da parede de baixo.
Massa cai 9 / 20 / 36 g.

**2. Uma fenda no aro do M engataria 1 mm.** O P pousa pela saia no patamar do aro do M,
11,7 mm acima dele; o macho do P fica na saia, 0,6 mm acima da sola — ou seja, quase todo
ACIMA do aro do M. Qualquer fenda no M receberia 1 mm de macho. Dente pendurado sob a saia
não serve: no ninho a saia de cima passa 4 mm acima do aro de baixo. Solução invertida:
**postes em T que sobem do patamar do aro do grande** e entram, por baixo, na fêmea que o
pequeno já tem — a fêmea é aberta embaixo justamente para o macho da vizinha entrar.
Engate de **8,5 mm no P, 10,0 no M** (altura da ranhura menos 0,8). O poste tem os mesmos
7,5° da saia, então acompanha a fêmea inclinada sem folga variável.

**Por que ym_M = −yf_P e yf_M = −ym_P.** No ninho o poste do M de baixo cai onde está a
fêmea do M de cima, girado: poste em (lat_d, y) encontra a fêmea de lat_e em −y. Como os
postes ficam onde estão as fêmeas do P (lat_d em yf_P = −84,1; lat_e em ym_P = +34,4), a fêmea
do M tem de estar em ym_M = 84,1 (lat_e) e yf_M = −34,4 (lat_d). O bolsão do M fica com
**4,6 mm** para engolir a cabeça do poste (2,6 no P e no G); haste do poste a 0,58 mm da saia
da peça de cima; topo do poste 6,3 mm abaixo do lintel dela.

**Dois M no G, frente com frente.** Girados 90°, a lateral do M fica de frente para a frente
e para a traseira do G; só a traseira tem altura para receber poste. Entrando frente com
frente, as duas traseiras (com aro) pousam nas laterais do G e a lateral de trás de cada M
pousa na traseira do G, onde estão os dois postes (x = −181,9 e +63,4). Cada M apoia em
dois lados e trava num poste. A frente nua de cada M encosta na do outro no meio.

**Acopladores nos três.** Haste = e + 0,4 (2,2 / 2,4 / 2,7), cabeça 1,8, saliência 4,0 / 4,2 /
4,5. Módulo de palete conferido para a fileira de dois: 2X + uma cabeça livre ≤ dois módulos
(388, 784, 1.196,5). Correção de rev.22: o macho terminava 0,8 mm DENTRO do lintel da
vizinha; agora para 0,4 mm abaixo dele.

**Malha exata onde a folga é 0,3.** Macho, ranhura, bolsão, bochechas e postes passaram a
ser blocos com coordenada exata; por banda de amostra (1,3 mm) saíam até 1,3 mm fora do
lugar e a malha mostrava interferência que o projeto não tem. A saia por banda para uma
amostra antes da ranhura e o resto vai por bloco que acompanha a aresta inclinada da amostra.

**Sobre a proporção áurea.** Não foi preciso mexer nas larguras. Dobrar um lado e girar 90°
a cada degrau (P → M → G) é a aritmética da série A de papel (razão √2 preservaria a
proporção; com 3 : 2 do palete, P e G ficam em 1,5 e o M em 1,32). φ continua na altura
(H = X / 1,618) e não cabe na planta de três tamanhos ao mesmo tempo.

Conferências novas em toda build: aro fora da parede de baixo no ninho (3 tamanhos); poste
dentro do bolsão do filho; poste dentro do próprio bolsão girado (M); poste sob o lintel;
saia do pequeno pousa no patamar (não num degrau); haste do macho abaixo do lintel.

### rev.25 — em cima, não dentro: o P vira caixa

Pedido: o par de P não entra no M, **pousa em cima**; três P no G; o G encolhe para caber os três;
"uma peça uniforme", **clean, moderno e discreto** (B2C).

**O que impedia.** Os pés do P (os copos) ficavam 41,5 mm para dentro da linha do aro, por causa dos
7,5° de saída e da aba. Em cima de um M eles caíam 25 mm dentro da boca — e nada pode haver ali sem
quebrar o ninho do M (a peça de cima passa a 0,26 mm da parede). Duas tentativas de pés no contorno
do aro (colunas de canto com pino na sola; depois colunas ocas com pino subindo do aro do M) ficaram
feias: oito pés, colunas destacadas do corpo, boca estreita.

**A saída é a raiz.** O afunilamento de 7,5° só existe para o ninho, e o P não ninha mais. Tirando-o,
o P vira uma **caixa**: parede a **0,5°** (`saida` passou a ser por peça: `s["tan"]`), borda de
**7 mm** com saia de **12** para os acopladores (a saia deixa de vir do passo de ninho), **rodapé de
3 mm recuado 4 mm** em vez de perna de 50 com copos, fundo inteiro. 297 g, 8,1 L, 192 × 289 × 179.

**O encaixe.** Em cima do M e do G o rodapé do P cai dentro da boca e o ombro (o degrau de 4 mm entre
rodapé e parede) pousa no topo da parede do grande: folga de 1,2 mm no M e 0,9 no G entre rodapé e
face interna da parede; 2,0 / 2,3 mm de apoio no topo da parede. A boca segura o par em x e y.
**Nada de pé, coluna, pino ou furo.** O aro do M e do G é inteiro. Os P se acoplam entre si pelo
macho e fêmea da saia, como antes.

**P em cima de P.** O rodapé de cima cai na boca do de baixo e pousa no **degrau** das quatro colunas
internas (o antigo canal vira um degrau simples até 1 mm da parede, sem guia — com parede reta não
sobra espaço para canal + guia). Passo 176: os aros ficam rentes. Folga lateral 3,7 mm.

**O pilar.** Na frente do M e do G o mergulho tirava a parede onde o rodapé do P precisa ser segurado.
A frente ganhou pilares de altura cheia de **50 mm** entre os P e cantos altos nas pontas (25 mm de
rodapé de cada P apoiado em cada um); o mergulho virou **vãos de 142 mm, um sob cada P**. O perfil
da frente é função de x: zonas cheias (pontas e pilares), rampas suaves de 14 mm e o mergulho no
meio de cada vão. Só no M e no G; a frente do P é toda vão entre os cantos.

**As cotas.** X_g = n × 192 + 6, Y_g = 289 + 6 → M 390 × 295 (igual), **G 582 × 295 × 360**
(era 596 × 396 × 368; 35 L em vez de 54). Raio do canto 26 nos três. Aba do M e do G 12,4.
Módulo de palete mantido: 2 × 582 + 4,5 ≤ 1.200.

**O que se perdeu.** O **P não ninha** (parede reta). Dez P empilham rente: 179 + 9 × 176 mm.
**Dois M já não fazem um G** (2 × 390 > 582). M e G ninham como antes: pilar e canto alto são parede.

Conferências em toda build: fileira de n P dá o aro com 3 mm por lado; rodapé do P a ≥ 0,8 mm da
face interna da parede do grande; ombro apoiado ≥ 1,5 mm no topo da parede; canto alto alcança a
reta; ninho de M e G (base e aro) intacto. As conferências de ninho só rodam em quem ninha.

## Arquivos

| Arquivo | O que é |
|---|---|
| `geometria.py` | núcleo: contorno de cantos arredondados avaliável em qualquer altura, emissor de bandas da casca, casca perfurada, viga afunilada, prisma e normais suaves com crease |
| `modelo.py` | a peça — parâmetros dos 3 tamanhos, construção, `confere_ninho()`, `confere_aro_ninho()`, `pendura()`; `python3 modelo.py` imprime a ficha e quebra se algo colidir |
| `detalhes.py` | vistas de inspeção e cortes (`out/det-*.png`): copo, canal, ninho, pilha, encaixe do P na boca, pilha de P, P por baixo, frente |
| `dossie_pdf.py` | o dossiê em PDF (`out/modula-rev25.pdf`) |
| `render.py` | rasterizador próprio: z-buffer, sombreamento suave (Gouraud com crease), sombra de contato e base clara por luminância |
| `exporta.py` | gera o JSON do visualizador, as vistas e o STL (`python3 exporta.py stl` só o STL, `png` só as vistas) |
| `celular.py` | GLB (abre no celular), prancha de 6 vistas por tamanho e giro em GIF |
| `dossie.html` | o dossiê publicado |
| `out/0*.png`, `out/10-*.png` | vistas: família, isométrica, ninho, pilha, encaixe, torre, P em cima do M e do G, fileiras acopladas |
| `out/modula.json` | malha quantizada (int16 → base64) usada pelo visualizador |

Mudar `TAMANHOS` em `modelo.py` e rodar `python3 exporta.py` refaz tudo. O ritmo das ripas,
o raio dos cantos, a altura da boca e o perfil do aro são todos parâmetros.

## O que a fábrica precisa decidir

1. **Câmara quente no G.** Área projetada de 2.360 cm²: a 300 bar de pressão de cavidade
   dá 722 tf, a 400 bar dá 963 tf. O parque (`VW_MAQUINA_CAPACIDADE`) tem 38 injetoras
   até 260 t, **uma** de 398 t, **seis** de 600–800 t, uma de 1.100 t e 43 acima de
   1.200 t — e a faixa acima de 1.100 t é justamente a que o histórico mede com zero
   máquina livre. O G só é confortável com 3–4 pontos de injeção; com um ponto e canal
   frio, o comprimento de fluxo (250 + 300 mm) empurra a pressão para cima e a peça sai
   da faixa disponível. **É essa decisão, não o desenho, que define a máquina do G.**
2. **Qual PP.** O H 105 é homopolímero com clarificante — feito para transparência, não
   para caixa sob carga; caixa estruturada pede copolímero de impacto. Seja qual for,
   tem de continuar sendo PP: o ciclo de moído vale ~R$ 2,63 M/ano e só funciona porque
   o refugo é mono-resina.
3. **Cor entra por Coloratto.** Branco (farmácia) e chumbo (e-commerce), e só.
4. **Ensaio de compressão e fluência** antes do aço: o rodapé apoiado no canal das 4 colunas;
   5 andares a 15 kg = 750 N. PP deforma sob carga constante — é isso que faz torre de
   plástico "sentar" no estoque depois de meses. Com a parede vazada isso deixa de ser
   formalidade: é o ensaio que decide a espessura final.
5. **Vão do fundo em grelha** (9 mm no P, 18 no M, 22 no G) e os **quatro bolsões de canto**
   (o copo do pé, aberto para dentro da cesta): indiferentes para farmácia e e-commerce,
   decisivos para quarto infantil e cozinha. Alternativa sem mexer no molde: um tapete de
   fundo avulso, que também vira item de venda.
6. **As três cores**: branco (farmácia e casa), chumbo (e-commerce), terracota (linha).
   Nada além disso — cor divide demanda existente, produto novo cria demanda.
7. **A portinhola** da referência grande é uma **quarta peça**, fora dos 3 moldes.

## Verificação de catálogo (lição nº 10 do CLAUDE.md)

Busca no `TGFPRO`, grupo 1000000–1009999, faturamento 12 M (empresas 1/2/14, sem tabela
AVON 84 e sem exportação 3): **não existe organizador modular de frente aberta e
encaixável no catálogo.** Os vizinhos:

| Produto | Ref | 12 M | Observação |
|---|---|---|---|
| Gaveteiro 4 gavetas (P/B/rosa) | 004.006.* | R$ 1,36 M | gaveta, não caixa |
| Gaveteiro Modular Rattan 8,2 L | 254.006.* | R$ 1,14 M | **o vizinho comercial mais forte** |
| Caixa Organizadora Rattan 16 L | 069.006.* | R$ 1,11 M | fechada, com tampa |
| Prateleira Multiuso 4 andares | 053.004.* | R$ 321 k | é a estante, não o cesto |
| Cesto de Roupas Empilhável 43,8 L | 552.004.* | R$ 108 k | **empilha e tem 43,8 L; o G tem 46,8 L** |

O 552 é a pergunta que o curador vai fazer: já existe um empilhável de 43,8 L (1,19 kg,
R$ 108 k/12 M com 114 clientes) e o G tem 43,7 L. A resposta tem de ser funcional — o 552
abre por cima, não ninha e pesa 34% mais que o G — e tem de vir com número, não com
narrativa.

## Estado

Estudo de geometria e mecânica. **Não gravado em `pdp_lancamento`.** A borda nua do mergulho (2 mm) pede raio no molde e talvez reforço interno com saída — decidir com a ferramentaria. Falta o
`engenheiro-molde` (máquina, resina, ciclo) e o `curador-portfolio` (payback de 3 moldes,
canibalização do 254, resposta sobre o 552). Com 0,7% de acerto na safra 2025, três moldes
de uma vez é aposta de plataforma — e o viés padrão do projeto é não lançar.
