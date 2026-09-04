# Família MODULA — organizador modular encaixável/empilhável

**rev.02** — parede inteira vazada, cantos arredondados, encaixe por pé + pino.

Estudo 3D paramétrico de **3 moldes** (P, M, G) para uma linha de organizadores de
frente aberta que **encaixam um dentro do outro no transporte** e **plugam um sobre
o outro no uso**, formando andares.

> Sem STL nesta revisão, por decisão de projeto: a forma ainda está em ajuste.

Dossiê interativo (visualizador 3D, mecânica, ficha, riscos):
https://claude.ai/code/artifact/a7b943a0-a481-40ef-9798-b0c76dc870f0

## Os três tamanhos

| | Externo (mm) | Canto | Parede | Massa PP | Resina/peça | Capacidade | Passo pilha | Passo ninho | Ganho transp. | Fechamento |
|---|---|---|---|---|---|---|---|---|---|---|
| **P** | 300 × 200 × 150 | R 22 | 2,0 mm | 215 g | R$ 2,15 | 5,9 L | 150 mm | 25 mm | 3,3× | 184–245 tf |
| **M** | 400 × 300 × 200 | R 30 | 2,2 mm | 414 g | R$ 4,13 | 17,2 L | 200 mm | 27 mm | 3,6× | 367–490 tf |
| **G** | 600 × 400 × 250 | R 40 | 2,5 mm | 840 g | R$ 8,38 | 45,6 L | 250 mm | 31 mm | 3,7× | 734–979 tf |

Grade **1 : 2 : 4** — dois P dão exatamente um M, dois M dão exatamente um G.
No palete 1200 × 800: 16 P, 8 M ou 4 G por camada, sem sobra.
Seis M plugadas = 1.200 mm de altura; ninhadas = 335 mm.

Resina a R$ 9,98/kg (80% virgem clarificado a R$ 10,96 + 20% moído a R$ 6,07).

### rev.01 → rev.02

| | massa rev.01 | massa rev.02 | capacidade | ninho |
|---|---|---|---|---|
| P | 467 g | **215 g** (−54%) | 6,2 → 5,9 L | 31 → 25 mm |
| M | 886 g | **414 g** (−53%) | 17,4 → 17,2 L | 33 → 27 mm |
| G | 1.514 g | **840 g** (−44%) | 46,8 → 45,6 L | 39 → 31 mm |

Vazar a lateral inteira e trocar os oito canais grossos pelo par pé-pino tirou metade
da resina sem tirar capacidade. O ninho ficou mais fundo porque a saída subiu de 4° para 5°.

## A mecânica — pé + pino

As ripas de cada lateral são distribuídas **simetricamente em torno do meio**, então a
posição espelhada de uma ripa é sempre outra ripa. Duas dessas ripas recebem um **pino**
oco no aro; as duas espelhadas correspondentes são **removidas** — e é por elas que o
**pé** desce. A janela do encaixe é uma ripa que falta, não um rasgo aberto.

```
MODULA M:  pinos em y = +105 e -75      janelas em y = +75 e -105
           abertura da janela 50 mm  >  largura do pé 34 mm
```

- **Alinhada (0°)** → o pé pousa na aba do aro (12 mm de apoio, contínua em toda a volta)
  e o pino entra no soquete: **pluga**. Passo = altura da peça.
- **Girada (180°)** → cada pé cai sobre uma janela e desce por dentro: **ninho**.
  Passo = `e / tan(5°)`.

O pino **não sustenta carga** — quem sustenta é a aba. O pino impede a pilha de escorregar
e de destravar de lado.

Como o contorno cresce por **offset** (e não por escala), o trecho reto da lateral tem o
mesmo comprimento em qualquer altura: o pé da peça de cima cai exatamente sobre o pino da
de baixo, sem correção.

### A regra que governa a peça inteira

**Saliência para fora só é permitida na faixa do topo**, mais baixa que o passo do ninho,
porque essa faixa nunca precisa entrar dentro de outra peça. Abaixo dela a parede é lisa
por fora e todo o vazado é coplanar.

É por isso que a MODULA **não tem friso horizontal e nenhuma nervura maciça**: os dois
matariam o ninho. Esse é o erro que aparece na maioria das caixas que "quase" encaixam —
a peça de cima trava a meio caminho num relevo que ninguém projetou para ser obstáculo.

Consequência boa: **nenhum recurso exige gaveta no molde**. Pé, pino, janela, rasgo de
ventilação e aro saem todos na direção de abertura.

## Arquivos

| Arquivo | O que é |
|---|---|
| `geometria.py` | núcleo: contorno de cantos arredondados avaliável em qualquer altura, e o emissor de bandas da casca |
| `modelo.py` | a peça — parâmetros dos 3 tamanhos e construção; `python3 modelo.py` imprime a ficha |
| `render.py` | rasterizador próprio (painter + z-buffer + sombreamento plano) |
| `exporta.py` | gera o JSON do visualizador e as vistas (sem STL nesta revisão) |
| `dossie.html` | o dossiê publicado |
| `out/0*.png` | vistas: família, isométrica, ninho, pilha, encaixe |
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
4. **Ensaio de compressão e fluência** antes do aço: 4 pés por peça, ~12 mm de apoio cada;
   5 andares a 15 kg = 750 N. PP deforma sob carga constante — é isso que faz torre de
   plástico "sentar" no estoque depois de meses. Com a parede vazada isso deixa de ser
   formalidade: é o ensaio que decide a espessura final.
5. **Vão do fundo em grelha** (15 a 22 mm conforme o tamanho): indiferente para farmácia e
   e-commerce, decisivo para quarto infantil e cozinha. Alternativa sem mexer no molde: um
   tapete de fundo avulso, que também vira item de venda.
6. **A portinhola** da referência grande é uma **quarta peça**, fora dos 3 moldes.

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
R$ 108 k/12 M com 114 clientes) e o G tem 45,6 L. A resposta tem de ser funcional — o 552
abre por cima, não ninha e pesa 42% mais que o G — e tem de vir com número, não com
narrativa.

## Estado

Estudo de geometria e mecânica. **Não gravado em `pdp_lancamento`.** Falta o
`engenheiro-molde` (máquina, resina, ciclo) e o `curador-portfolio` (payback de 3 moldes,
canibalização do 254, resposta sobre o 552). Com 0,7% de acerto na safra 2025, três moldes
de uma vez é aposta de plataforma — e o viés padrão do projeto é não lançar.
