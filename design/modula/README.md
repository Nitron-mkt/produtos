# Família MODULA — organizador modular encaixável/empilhável

Estudo 3D paramétrico de **3 moldes** (P, M, G) para uma linha de organizadores de
frente aberta que **encaixam um dentro do outro no transporte** e **empilham um sobre
o outro no uso**, formando andares.

Dossiê interativo (visualizador 3D, mecânica, ficha, riscos):
https://claude.ai/code/artifact/a7b943a0-a481-40ef-9798-b0c76dc870f0

## Os três tamanhos

| | Externo (mm) | Painel no topo | Base | Parede | Massa PP | Capacidade | Passo pilha | Passo ninho | Fechamento |
|---|---|---|---|---|---|---|---|---|---|
| **P** | 300 × 200 × 150 | 240 × 200 | 219 × 179 | 2,0 mm | 467 g | 6,2 L | 150 mm | 31 mm | 184–245 tf |
| **M** | 400 × 300 × 200 | 332 × 300 | 304 × 272 | 2,2 mm | 886 g | 17,4 L | 200 mm | 33 mm | 367–490 tf |
| **G** | 600 × 400 × 250 | 524 × 400 | 489 × 365 | 2,6 mm | 1.514 g | 46,8 L | 250 mm | 39 mm | 734–979 tf |

Grade **1 : 2 : 4** — dois P dão exatamente um M, dois M dão exatamente um G.
No palete 1200 × 800: 16 P, 8 M ou 4 G por camada, sem sobra.

Ganho de transporte (6 unidades ninhadas contra 6 empilhadas): **3,5× (P) · 3,3× (M) · 3,2× (G)**.
Seis M empilhadas = 1.200 mm de altura; ninhadas = 368 mm.

## A mecânica (o núcleo da patente de uso)

Cada lateral tem **4 canais verticais** (8 por peça), que são vincos da própria parede.
Dois canais por lateral têm o **topo fechado** — viram assento, com bolsão que captura
a talisca. Dois têm o **topo aberto** — viram guia. As posições fechadas e abertas são
espelhadas entre si:

```
fechado (assento)   y = +0,42·Y   e   y = -0,12·Y
aberto  (guia)      y = -0,42·Y   e   y = +0,12·Y
```

Na base nascem **4 taliscas** alinhadas com os assentos, com saliência
`H·tan(4°) + 12 mm` — os 12 mm são o apoio efetivo sobre o assento.

- **Alinhada (0°)** → talisca cai no assento → **empilha**, passo = altura da peça.
- **Girada (180°)** → talisca encontra o canal aberto e desce por dentro dele até a
  parede de cima encostar na de baixo → **ninho**, passo = `e / tan(4°)`.

Girar 180° é o seletor porque ele mantém a peça alinhada. O deslocamento
frente/verso (que é o que as referências do mercado usam) só tem a folga da
conicidade e depende de o operador acertar a posição.

### A regra de projeto que sai disso

Numa peça que encaixa em ninho, **nervura maciça é proibida**. Todo reforço tem de ser
vinco — parede deslocada para fora, vazio por dentro — e o conjunto de vincos tem de ser
**simétrico frente/verso**, senão a peça de cima trava a meio caminho. Uma única nervura
sólida numa parede interna mata o ninho.

Consequência boa: **nenhum recurso exige gaveta no molde**. Talisca, canal, assento,
rasgo de ventilação e furo do rebordo saem todos na direção de abertura.

## Arquivos

| Arquivo | O que é |
|---|---|
| `geometria.py` | núcleo: prismas, lei de conicidade, decomposição de painel com furos |
| `modelo.py` | a peça — parâmetros dos 3 tamanhos e construção; `python3 modelo.py` imprime a ficha |
| `render.py` | rasterizador próprio (painter + z-buffer + sombreamento plano) |
| `exporta.py` | gera STL, JSON do visualizador e as vistas |
| `dossie.html` | o dossiê publicado |
| `out/modula-{P,M,G}.stl` | **malha para impressão 3D** — imprimir a 1:2 para validar ninho e trava |
| `out/0*.png` | vistas: família, isométrica, ninho, pilha, mecanismo |

Mudar `TAMANHOS` ou `CANAIS` em `modelo.py` e rodar `python3 exporta.py` refaz tudo.

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
4. **Ensaio de compressão e fluência** antes do aço: 4 assentos por peça, ~12 mm de apoio
   cada; 5 andares a 15 kg = 750 N. PP deforma sob carga constante — é isso que faz torre
   de plástico "sentar" no estoque depois de meses.
5. **A portinhola** da referência grande é uma **quarta peça**, fora dos 3 moldes. Os
   canais dianteiros já saem com a calha que a receberia.

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
R$ 108 k/12 M com 114 clientes). A resposta tem de ser funcional — o 552 abre por cima e
não ninha — e tem de vir com número, não com narrativa.

## Estado

Estudo de geometria e mecânica. **Não gravado em `pdp_lancamento`.** Falta o
`engenheiro-molde` (máquina, resina, ciclo) e o `curador-portfolio` (payback de 3 moldes,
canibalização do 254, resposta sobre o 552). Com 0,7% de acerto na safra 2025, três moldes
de uma vez é aposta de plataforma — e o viés padrão do projeto é não lançar.
