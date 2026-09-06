# Família MODULA — organizador modular encaixável/empilhável

**rev.06** — o pé achatado vira uma **saia de 50 mm** recortada em arcos: ninha junto com o corpo e abre 5 cm entre os andares.

Estudo 3D paramétrico de **3 moldes** (P, M, G) para uma linha de organizadores de
frente aberta que **encaixam quase colado no transporte** e **plugam um sobre o outro
no uso**, formando andares. Dez peças ninhadas ocupam menos altura que três plugadas.

> Sem STL nesta revisão, por decisão de projeto: a forma ainda está em ajuste.

Dossiê interativo (visualizador 3D, mecânica, ficha, riscos):
https://claude.ai/code/artifact/a7b943a0-a481-40ef-9798-b0c76dc870f0

## Os três tamanhos

| | Externo (mm) | Cesta + saia | Parede | Massa PP | Resina/peça | Capacidade | Passo pilha | Passo ninho | Cubagem (10) | Fechamento |
|---|---|---|---|---|---|---|---|---|---|---|
| **P** | 300 × 200 × 200 | 150 + 50 | 1,8 mm | 271 g | R$ 2,71 | 5,4 L | 200 mm | 16 mm | 5,9× | 184–245 tf |
| **M** | 400 × 300 × 250 | 200 + 50 | 2,0 mm | 472 g | R$ 4,71 | 15,9 L | 250 mm | 17 mm | 6,2× | 367–490 tf |
| **G** | 600 × 400 × 300 | 250 + 50 | 2,3 mm | 912 g | R$ 9,10 | 42,7 L | 300 mm | 20 mm | 6,3× | 734–979 tf |

Grade **1 : 2 : 4** — dois P dão exatamente um M, dois M dão exatamente um G.
No palete 1200 × 800: 16 P, 8 M ou 4 G por camada, sem sobra.
Dez M plugadas = 2.500 mm de altura; ninhadas = 403 mm.

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

O P é o mais fechado de propósito — é a peça que vai à vista em casa e a que guarda coisa
pequena; o G é o mais aberto, porque é caixa de estoque. `TAMANHOS` em `modelo.py` carrega
`ripa` (material), `vao` (furo), `fileiras`, `barra` e `vao_fundo` para cada um.

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

### rev.10 — o vazado vira o grafismo da marca

O logo foi medido no PNG da marca, não estimado a olho. O traço é uma **lente
de duas arestas curvas**: razão comprimento/largura **2,22** no traço curto e
**4,07** no longo, preenchimento **0,60** da caixa (retângulo seria 1,00, elipse
0,785), eixo maior a **63° da horizontal**, com uma curvatura de centro de ±9%
da largura (sutil; não reproduzida).

O furo é esse traço **girado 90°** — o mesmo grão, deitado. É isso que troca o
vazado vertical pelo horizontal sem perder a marca: o ângulo passa a 22° e a
malha alternada refaz a trama do logo.

| | P | M | G |
|---|---|---|---|
| grão | 38 × 9,2 mm | 56 × 13,8 mm | 72 × 17,7 mm |
| ponta (raio) | 2,2 mm | 2,2 mm | 2,2 mm |
| malha | 25 × 5 | 25 × 5 | 29 × 5 |
| passo (volta × altura) | 28,2 × 21,1 | 41,2 × 30,0 | 53,6 × 38,9 |
| vazado | 38,9% | 42,1% | 41,3% |
| **alma mínima** | **5,4 mm** | **7,5 mm** | **10,0 mm** |
| massa | 226 g | 440 g | 883 g |

O P continua o mais fechado da família de propósito: é a peça que vai à vista em
casa e a que guarda coisa pequena — furo de 9,2 mm de largura contra 17,7 do G.

**A geometria do furo.** Interseção de dois discos (é isso que dá a aresta curva
do logo) com as pontas arredondadas por um *max suave* de raio 2,2 mm — ponta
viva seria concentrador de tensão na peça e gume de aço fino no molde.

**Como a casca é emitida.** `perfurada()` em `geometria.py`: para cada tira do
contorno, acha os trechos sólidos no meio da tira e refina as bordas por
bisseção **nas duas colunas**. É isso que faz a borda do furo sair curva em vez
de escadinha, sem precisar de malha fina.

**O que não mudou.** O vazado continua **coplanar** — nenhum relevo por fora,
senão o ninho trava a meio caminho. Coluna e painel de etiqueta ficam cheios: a
coluna é poste de carga da pilha, não pode ser furada.

**Alma mínima** é a menor distância entre dois furos vizinhos, medida por
amostragem do contorno do grão contra os oito vizinhos, e é verificada por
`assert` nos três tamanhos (mínimo 4 mm).

## Arquivos

| Arquivo | O que é |
|---|---|
| `geometria.py` | núcleo: contorno de cantos arredondados avaliável em qualquer altura, emissor de bandas da casca, normais suaves com crease e o pé de planta arredondada |
| `modelo.py` | a peça — parâmetros dos 3 tamanhos e construção; `python3 modelo.py` imprime a ficha |
| `render.py` | rasterizador próprio: z-buffer, sombreamento suave (Gouraud com crease), sombra de contato e base clara por luminância |
| `exporta.py` | gera o JSON do visualizador e as vistas (sem STL nesta revisão) |
| `dossie.html` | o dossiê publicado |
| `out/0*.png` | vistas: família nas três cores, isométrica, ninho, pilha, encaixe, torre branca |
| `out/modula.json` | malha quantizada (int16 → base64) usada pelo visualizador |

Mudar `TAMANHOS` em `modelo.py` e rodar `python3 exporta.py` refaz tudo. O ritmo das ripas,
o raio dos cantos, a altura da boca e o perfil do aro são todos parâmetros.

## O que a fábrica precisa decidir

1. **Câmara quente no G.** Área projetada de 2.400 cm²: a 300 bar de pressão de cavidade
   dá 734 tf, a 400 bar dá 979 tf. O parque (`VW_MAQUINA_CAPACIDADE`) tem 38 injetoras
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
4. **Ensaio de compressão e fluência** antes do aço: 4 pés por peça apoiados nas cristas;
   5 andares a 15 kg = 750 N. PP deforma sob carga constante — é isso que faz torre de
   plástico "sentar" no estoque depois de meses. Com a parede vazada isso deixa de ser
   formalidade: é o ensaio que decide a espessura final.
5. **Vão do fundo em grelha** (15 a 22 mm conforme o tamanho): indiferente para farmácia e
   e-commerce, decisivo para quarto infantil e cozinha. Alternativa sem mexer no molde: um
   tapete de fundo avulso, que também vira item de venda.
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

Estudo de geometria e mecânica. **Não gravado em `pdp_lancamento`.** Falta o
`engenheiro-molde` (máquina, resina, ciclo) e o `curador-portfolio` (payback de 3 moldes,
canibalização do 254, resposta sobre o 552). Com 0,7% de acerto na safra 2025, três moldes
de uma vez é aposta de plataforma — e o viés padrão do projeto é não lançar.
