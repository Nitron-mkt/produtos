# Tampa Portinhola — modelo 3D paramétrico

Conceito de tampa com **porta articulada** e **trava de correr** para a plataforma **Aro Comum**
(aro 105 × 206 mm, R14 — a base do Porta Sabão 008).

Substitui a *Tampa B · cursor deslizante* do estudo anterior, que tinha um defeito de
topologia: para o cursor sair, a canaleta era interrompida em 67 mm dos 622 mm de
perímetro. Onde a canaleta some, a tampa só encosta no aro — e nenhuma alegação de
estanqueidade se sustenta. A portinhola devolve o perímetro inteiro e move a abertura
para dentro da mesa da tampa.

> **Status: conceito.** Nada aqui foi validado em molde, ensaio ou tryout, e nada foi
> gravado em `pdp_lancamento`. Ver *Pendências* no fim.

---

## Como regenerar

```bash
cd molde
python3 pecas.py       # STL binário das 3 peças + web/geo.js (blob do visualizador)
python3 secao.py       # web/secao.svg — corte A-A cotado
python3 build_html.py  # ../analise/06-tampa-portinhola.html (artefato completo)
python3 preview.py     # PNGs de conferência (rasterizador próprio, sem dependência)
```

Sem dependência externa — Python 3 puro. **`pecas.py` é a fonte única das cotas**: o STL,
o render 3D do artefato, o corte cotado e a tabela de cotas saem todos do mesmo dicionário
`P`. Não existe cota digitada duas vezes.

| Arquivo | Papel |
|---|---|
| `geo.py` | kernel: contorno retangular arredondado, varredura de perfil, prismas, STL |
| `pecas.py` | **as cotas** + as três peças + métricas |
| `secao.py` | corte longitudinal A-A a 12 mm do eixo |
| `preview.py` | rasterizador z-buffer para conferir a malha sem abrir CAD |
| `build_html.py` | monta o artefato |
| `stl/` | `corpo.stl`, `tampa.stl`, `portinhola.stl`, `trava.stl` — binário, mm, Z para cima |

---

## Arquitetura de vedação — três barreiras, nenhuma de borracha

Material não cria vedação; **geometria e força de fechamento criam**. As três barreiras são
PP, no mesmo material do resto da peça.

**1 · Lábio flexível no aro — 0,35 mm de interferência em 592 mm contínuos.**
Aba em balanço de 1,00 × 7,40 mm que desce da mesa por dentro do aro e encosta na banda de
saída zero do corpo. É flexível de propósito: um cordão rígido esmagado dá muita força no
primeiro dia e perde quase tudo em semanas, porque o PP relaxa; um lábio longo trabalha com
deformação pequena e mantém pressão de contato. A perna externa do canal apoia o aro por
fora com 0,35 mm de folga — a interferência vira **pressão de contato** em vez de abrir a
boca do pote.

**2 · Batente, não aperto.** A mesa da tampa apoia no topo do aro (0,90 mm de largura,
592 mm de perímetro). É o encosto — não a força da trava — que define a compressão do lábio.
Isso endereça diretamente a hipótese aberta do projeto sobre `176.024.001` e `210.024.001`
(trava + válvula, MB 65,7% e 60,6%, caindo 57% e 39%): se a causa for fluência sob tensão
permanente de trava, esta tampa não herda o problema. **Isso precisa ser medido, não
assumido.**

**3 · Selo radial da portinhola — 0,30 mm em 267 mm.** A saia entra num gargalo cônico de
3° e sela pela lateral, não pela face: não depende de força de fechamento, depende de
encaixe, e o cone centra a peça sozinho. Retenção por ressalto de 0,90 mm na parede do
rebaixo, em duas zonas de 16 mm ao lado da concha do dedo. O eixo da dobradiça fica **acima
do plano da porta** — é o que faz a saia sair na vertical ao abrir, em vez de raspar o
gargalo.

**Por que não silicone:** LSR não roda nesta fábrica (canal frio, molde a 150–200 °C, bomba
bicomponente). E o motivo mais caro: o ciclo de moído vale **R$ 2,63 M/ano** e só funciona
porque o refugo é mono-resina. Guarnição de outro material contamina esse ativo.

---

## A trava de correr

A trava é um **cursor cativo** que corre num trilho em T moldado na saia da tampa e leva uma
lingueta que entra **por baixo de uma aba do corpo**.

Fechado o pote, a trava está sobre a **janela de entrada** — a região da aba deixada aberta de
propósito, por onde a lingueta desce junto com a tampa. Um empurrão de **22 mm** leva a lingueta
para debaixo da aba e tranca. A ponta que avança tem **rampa de 6 mm**; o resto é patamar. É a
rampa que faz o trabalho: ao correr, ela passa sob a aba e **puxa a tampa 0,08 mm contra o
batente**. Depois disso o contato é plano contra plano — não há mola tensionada para relaxar
com o tempo, e nada volta sozinho por vibração.

| | |
|---|---|
| Aba do corpo | 1,40 mm de projeção · 2 zonas de 22 mm nas faces curtas · face de encosto a 0° |
| Engate da lingueta | 1,06 mm |
| Curso | 22 mm |
| Aperto da rampa | 0,08 mm |
| Massa | 0,5 g por trava |

**Por que isto é melhor que a alavanca.** A versão anterior dependia de uma dobradiça viva de
0,45 mm em PP H 105 — homopolímero **com clarificante**, e nucleante deixa dobradiça frágil.
Era a maior incerteza técnica do conceito. A trava de correr não flexiona nada: trabalha em
**cisalhamento**. Em troca, vira uma quarta peça e um segundo clique de montagem.

A lingueta é **cativa** — presa no trilho, com batentes nas duas pontas. Não é componente solto
que o consumidor perde, como o copo dosador que o 008 embala junto.

O corpo também ganha uma **banda de vedação**: 6,2 mm de **saída zero** na face interna do aro
(z 112,4 → 118,6). Sem ela, a saída de 1,5° faria a interferência variar com a profundidade de
encaixe, e a vedação passaria a depender de quanto o consumidor apertou.

---

## Ferramentaria

| Peça | Área proj. | Fechamento | Massa | Saída negativa |
|---|---|---|---|---|
| Corpo AC-21 | 214,6 cm² | ≈ 75 t | 116,0 g | aba: **2 gavetas** nas faces curtas — ou extração forçada, a ensaiar |
| Tampa D | 214,6 cm² | ≈ 75 t | 36,3 g | trilho em T: **2 gavetas retas**, puxando em Y |
| Portinhola | 70,2 cm² | ≈ 25 t | 11,2 g | munhões na linha de partição |
| Trava de correr | 9,5 cm² | ≈ 4 t | 0,5 g (×2) | nenhuma — peça plana, 2 placas, 8 cavidades |

Conjunto: **164,5 g** em 5 peças · montagem de **3 cliques** (porta + 2 travas). A casa já monta:
99,7% dos apontamentos são em PI, e o PA sai da montagem.

**A regra que decide o ponto de injeção.** A mesa da tampa tem um furo de 62 × 82 mm no meio.
Todo furo gera linha de solda a jusante, e linha de solda é a região mais fraca e mais permeável
da peça. Se uma delas cair **sobre o gargalo**, vira caminho de vazamento na superfície que
precisa vedar. Os pontos têm de jogar as linhas de solda na mesa, longe do gargalo e do lábio
periférico. Isso é simulação de preenchimento antes de cortar aço.

**Faixa de tonelagem.** Os quatro moldes caem em ≤ 260 t, onde a ocupação medida neste projeto
é 56,9% com 7 de 15 injetoras paradas. Isso reduz risco de agenda, **não custo de ferramenta** —
molde é 30 a 40% do custo de um lançamento, e CNC parado também pode ser gargalo de
ferramentaria em vez de folga.

---

## Cotas principais

| Cota | Valor |
|---|---|
| Aro (referência) | 105 × 206 mm, R14 |
| Corpo | 120 mm de altura · parede 1,30 · fundo 2,00 · saída 1,5°/lado |
| Volume | 2,34 L até a borda · **2,18 L útil** |
| Mesa da tampa | 1,60 mm |
| Canal | 2,10 mm (recebe aro de 1,30) · folga externa 0,35 |
| Lábio de vedação | 1,00 × 7,40 mm · cone 2° · interferência **0,35 mm** |
| Perímetro de vedação | **591,8 mm contínuos** |
| Boca livre | 62 × 82 mm, R12 · **49,6 cm²** · perímetro 267,4 mm |
| Gargalo | 4,80 mm · cone 3° |
| Saia da portinhola | 3,80 mm · interferência **0,30 mm** |
| Rebaixo da porta | 1,60 mm — porta rente à mesa, tampa empilhável |
| Aba do corpo | 1,40 mm · 2 × 22 mm · engate 1,06 mm · curso 22 mm |
| Altura total | 120 + 5,6 mm (dobradiça) |

---

## Claim — o que dá para escrever

Não existe norma ABNT de estanqueidade para utilidade doméstica. "Hermético" é alegação
publicitária sob o CDC, e o **art. 36** obriga o fornecedor a manter os dados técnicos que a
sustentam. Dos 267 anúncios coletados no ML, só 8 dizem hermético (3%) — e os que dizem
"hermético + válvula" são de vidro com guarnição de silicone.

**Sustentável, com ensaio documentado:**
1. *Fecha contra umidade* — 200 g de sal refinado, 30 dias a 23 °C/50% UR, contra controle aberto.
2. *Não vaza deitado* — 1,5 L de água corada, 24 h apoiado em cada face, papel-toalha sob o pote.
3. *A trava não abre na queda* — 3 quedas de 1,0 m com 80% de carga: fundo, aresta, tampa.
4. *Continua vedando depois de guardado* — 30 dias fechado a 40 °C e repete o ensaio 2.
   **Este é o ensaio que ninguém faz** e é o que mede relaxação do PP sob tensão de trava.

**Não escrever:** "hermético" sozinho · "conserva a vácuo" (não há válvula) · "vai ao
micro-ondas fechado" · "mantém crocância por X dias".

---

## Pendências

1. **O aro tem de sair do desenho, não do cadastro.** A interferência é 0,35 mm. O cadastro
   do 008 diz 20,7 cm de profundidade; a plataforma foi desenhada em 20,6. Um milímetro é
   **três vezes a interferência** — engole a vedação ou trava o encaixe. Pré-requisito de
   tudo. *(engenheiro-molde)*
2. **O veredito vigente de Potes é "só kit"** (`pdp_linha`, score 8, 487 SKUs ativos,
   R$ 16,0 M caindo 15,5%). A versão compatível é a tampa entrar como peça da plataforma,
   servindo os quatro corpos do aro comum — não como SKU avulso. *(curador-portfolio · veto)*
3. **Quatro gavetas no total.** A aba do corpo e o trilho da tampa são saída negativa: duas
   gavetas em cada molde. No corpo, extração forçada pode substituir — a parede tem 1,3 mm e
   flexiona. No trilho, não: a seção é constante e a gaveta puxa reta em Y, o que é barato de
   fazer e caro de esquecer no orçamento. *(engenheiro-molde)*
4. **Esforço para correr a trava — inclusive com a mão molhada.** Falta medir força para
   travar, força para destravar, e o mesmo com sabão na mão: este pote é para mantimento **e
   para limpeza**. Se ficar duro, o consumidor deixa destravado e a vedação vira decoração.
   Ensaio de 5.000 ciclos com medição de força nas duas pontas. *(engenheiro-molde)*
5. **Por que `176` e `210` caíram** com a melhor margem da família. Se for fluência sob
   trava, o batente é a resposta. Se for conflito funcional, uma porta articulada corre o
   mesmo risco. *(analista-sankhya)*
6. **Payback do molde.** A taxa de acerto caiu de 28,0% (2021) para 0,7% (2025). O viés
   padrão é **não lançar**. Este modelo mostra que a peça funciona; não mostra que ela se
   paga. *(curador-portfolio · veto)*
