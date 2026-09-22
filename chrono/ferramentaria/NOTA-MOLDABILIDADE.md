# Chrono datador — nota de moldabilidade

Para o projetista. Resposta ao apontamento: *"não tem ângulos de saída, pontos
para extração e etc."*

**Você está certo.** O modelo que foi enviado é um modelo de **protótipo**, feito
para impressão 3D — e nessa função ele já cumpriu o papel: as três peças foram
impressas, montadas sobre uma tampa real e o mecanismo gira, trava e lê certo. O
que ele não é, e nunca foi, é modelo de ferramenta.

Abaixo está o tamanho exato do problema, medido face a face no próprio STEP, e o
que eu preciso de você para fechar a revisão.

---

## 1. O tamanho do problema, medido

Varredura de todas as faces, ângulo medido contra o eixo de extração (Y):

| Peça | faces | parede vertical (saída < 0,5°) |
|---|---|---|
| M02 rodinha dos meses | 554 | 518 faces · 268,6 mm² · **25% da área** |
| M03 ponteira | 624 | 593 faces · 234,7 mm² · **29% da área** |
| M01 acréscimos na válvula | 1.991 | 1.911 faces · 417,4 mm² · **26% da área** |

Todos os cilindros saíram cilindros de verdade — **0,00° em todos**. Não há saída
em lugar nenhum, exceto os chanfros já desenhados (cones de 45° e o chanfro da
janela, 5,8°–18,5°).

## 2. Por que eu acho que é revisão e não redesenho

O modelo é **paramétrico**: cada perfil de revolução e cada extrusão sai de uma
cota nomeada em código. Colocar saída é trocar `r` constante por `r(y)` — não é
redesenhar, é revisar e regerar. O que me segura não é o trabalho, são as
decisões que são suas (seção 4).

E a conta boa: **saída quase não mexe nos ajustes.**

| saída | custa em 1,60 de parede | em 2,95 de parede |
|---|---|---|
| 0,5° | 0,014 mm | 0,026 mm |
| **1,0°** | **0,028 mm** | **0,051 mm** |
| 1,5° | 0,042 mm | 0,077 mm |
| 3,0° | 0,084 mm | 0,155 mm |

Contra as folgas de projeto:

| ajuste | folga radial |
|---|---|
| poste Ø13,20 × furo da rodinha Ø13,60 | 0,20 mm |
| pino Ø5,80 × furo Ø6,00 | 0,10 mm |

Ou seja: **1° cabe folgado no ajuste do poste**. No pino (0,10 de folga em 2,95 de
altura) 1° come metade — dá, mas é o único ponto onde a saída e o ajuste brigam, e
provavelmente vale conicar o furo e o pino com o **mesmo** ângulo para a folga
ficar constante na altura.

## 3. Alturas de parede que precisam de saída

| peça | feature | altura |
|---|---|---|
| M01 | furo passante Ø6,00 | 2,85 |
| M01 | poste Ø13,20 externo | 2,55 |
| M01 | parede do rebaixo | 0,60 |
| M01 | 31 numerais dos dias, **em relevo** | 0,25 |
| M02 | furo Ø13,60 e externo Ø26,80 | 1,60 |
| M02 | 12 numerais dos meses, **gravados** | 0,30 |
| M03 | lâmina e janela | 1,60 |
| M03 | pino Ø5,80 | 2,95 |
| M03 | ícone e marcas M/D, **gravados** | 0,25 |

## 4. O que eu preciso decidir com você

1. **Ângulo padrão da casa** — 1°? 1,5°? Muda com acabamento (polido × texturizado)?
2. **Linha de partição** de cada peça. Minha proposta: M02 e M03 partem na face de
   baixo (tudo sai para cima, extração em +Y); M01 herda a partição da válvula atual.
3. **Onde o extrator pode empurrar.** Área livre que eu vejo:
   - M02: face de baixo, anel entre Ø13,60 e Ø26,80, fora das 12 covinhas de detente.
   - M03: face de baixo da lâmina (gota), Y 38,35 — área grande e plana.
   - M01: a válvula já tem extração resolvida; os acréscimos podem ter mudado isso.
4. **Contração.** Material é **PP** (a casa roda 98,4% PP; PP H 105 clarificado é o
   item mais comprado). Qual fator você aplica?

## 5. Três coisas que preciso que você olhe com atenção

**a) A farpa do pino da M03 é undercut de projeto, não esquecimento.**
Farpa Ø6,80 sobre furo Ø6,00 = **0,40 mm de interferência radial**. É o que segura
a ponteira. As 4 fendas existem para as pernas flexarem na montagem. Na extração
isso vira decisão sua: extrai forçando (strip) ou muda o esquema de retenção? Se
achar que não sai, me diga — eu troco o conceito de retenção, não é sagrado.

**b) As 12 covinhas de detente da M02 são undercut, e as 2 molas da M01 não são.**
Medi as duas: as covinhas da rodinha são esféricas com o equador **abaixo** da face
(abertura 0,461 de raio, barriga 0,55) → **0,089 mm de undercut radial**, strippable
em PP mas precisa ser intencional. As molas da M01 são calotas que estreitam para
cima → saem limpas.

**c) Traço fino em aço.** O que é gravado na peça vira **nervura** no aço:

| gravação | traço mínimo | profundidade |
|---|---|---|
| numerais dos meses (M02) | 0,373 mm | 0,30 |
| marcas M e D (M03) | **0,240 mm** | 0,25 |
| ícone Nitron (M03) | 1,684 mm | 0,25 |

As marcas M/D ficam em nervura de 0,24 × 0,25 — proporção 1:1. Se para você é
frágil, eu engrosso a fonte ou aumento a altura da letra; é cosmético, não
funcional.

## 6. A única coisa que não pode mudar

**A metade de baixo da válvula.** Ela foi replicada bit a bit do STL da peça que já
é injetada, exatamente para não mexer no molde da tampa nem no balancim. O
movimento de gangorra foi conferido: varredura de −3,6° a +3,6° em torno do pivô,
curva **idêntica** à da válvula original; interferência com a tampa igual à
original até a quarta casa.

Os arquivos `M01a/M01b/M01c` foram entregues justamente nesse formato — *subtrair
rebaixo → somar acréscimo → subtrair furo* — para serem aplicados sobre o **CAD
original da válvula**, que está com vocês. Nada do que eu mandei redesenha a
válvula.

## 7. Proposta

Me devolva os 4 itens da seção 4 e os 3 da seção 5. Com isso eu regero as três
peças com saída, conicidade casada nos ajustes e as áreas de extração já planas e
livres, e mando STEP novo. Se preferir remodelar do zero no CAD de vocês, também
funciona — nesse caso o STEP atual serve como referência dimensional e o que vale
são as cotas e as folgas listadas aqui.

O que eu não quero é decidir ângulo de saída e ponto de extração por conta própria
e você descobrir no tryout.
