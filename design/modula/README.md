# Família MODULA — organizador modular encaixável/empilhável

**rev.05** — medidas conferidas contra as referências, saída de 7,5° e vazado calibrado por tamanho.

Estudo 3D paramétrico de **3 moldes** (P, M, G) para uma linha de organizadores de
frente aberta que **encaixam quase colado no transporte** e **plugam um sobre o outro
no uso**, formando andares. Dez peças ninhadas ocupam menos altura que três plugadas.

> Sem STL nesta revisão, por decisão de projeto: a forma ainda está em ajuste.

Dossiê interativo (visualizador 3D, mecânica, ficha, riscos):
https://claude.ai/code/artifact/a7b943a0-a481-40ef-9798-b0c76dc870f0

## Os três tamanhos

| | Externo (mm) | Canto | Parede | Massa PP | Resina/peça | Capacidade | Passo pilha | Passo ninho | Avanço do pé | Cubagem (10) | Fechamento |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **P** | 300 × 200 × 150 | R 26 | 1,8 mm | 245 g | R$ 2,45 | 5,4 L | 150 mm | 16 mm | 32 mm | 5,2× | 184–245 tf |
| **M** | 400 × 300 × 200 | R 36 | 2,0 mm | 423 g | R$ 4,22 | 15,9 L | 200 mm | 17 mm | 40 mm | 5,6× | 367–490 tf |
| **G** | 600 × 400 × 250 | R 46 | 2,3 mm | 820 g | R$ 8,18 | 42,7 L | 250 mm | 20 mm | 48 mm | 5,9× | 734–979 tf |

Grade **1 : 2 : 4** — dois P dão exatamente um M, dois M dão exatamente um G.
No palete 1200 × 800: 16 P, 8 M ou 4 G por camada, sem sobra.
Dez M plugadas = 2.000 mm de altura; ninhadas = 355 mm.

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
