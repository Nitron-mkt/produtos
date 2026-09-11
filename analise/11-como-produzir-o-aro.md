# Como produzir o aro — as três rotas, e por que a injetora não faz bobina

**Pergunta que originou este documento:** *"dá para a injetora ir injetando uma carretilha do
arinho até virar uma bobina, e aí eu extruso de acordo com o tamanho da tampa?"*

**Resposta curta:** injetora não produz material contínuo — são processos diferentes. Mas a
pergunta por trás dela ("um perfil só, N comprimentos, sem molde por tamanho") tem resposta, e
tem **três** rotas, não uma.

---

## 1. Por que a injetora não faz bobina

| | Injeção | Extrusão |
|---|---|---|
| Como a rosca trabalha | **vai e volta** — dosa, avança, injeta, recua | **gira sem parar** |
| Produção | **por batelada** — uma peça (ou N) por ciclo | **contínua**, metro após metro |
| O que define a forma | o **molde fechado** | a **matriz aberta** + calibrador |
| Depois que sai | a peça já está pronta e fria | precisa de **calibrador, banho, puxador, bobinadeira** |

A injetora fecha o molde, injeta, espera resfriar, abre e extrai. **Não existe o estado
"injetando continuamente"** — o ciclo é a essência da máquina. Não é questão de ajuste ou de
programação: a rosca recíproca e o molde fechado são o que a torna injetora.

E mesmo que a rosca girasse sem parar, faltaria tudo o que vem depois: o perfil sai mole da
matriz e precisa ser **calibrado a vácuo, resfriado em banho, puxado com velocidade controlada e
bobinado com tensão constante**. Sem esse trem, sai um espaguete disforme.

**A parte boa da sua intuição está certa:** as suas injetoras **conseguem processar TPE** — TPE-S
e TPV rodam em injetora convencional de PP, sem secador e sem modificação. Só não conseguem
fazer bobina.

*(Registro: o ERP tem um único elastômero cadastrado, `CODPROD 997 TPE Karinprene shore 45`, e
**sem nenhuma compra em 24 meses**. A casa não compra TPE hoje.)*

---

## 2. As três rotas

### Rota 1 — Comprar a fita extrudada pronta

| | |
|---|---|
| Investimento | **R$ 8.000 – 20.000** (só a ferramenta de perfil, que fica sendo nossa) |
| Molde | nenhum |
| **Junta no aro** | **sim — uma emenda por aro, 346.572 emendas por ano** |
| Montagem | cortar + soldar a junta + calçar = 15–25 s |
| **Escalar para nova tampa** | **só mudar o comprimento de corte — R$ 0** ✅ |
| Custo | R$ 0,20/peça · **R$ 69.314/ano** |

### Rota 2 — Extrusora própria (a bobina feita em casa)

| Item | Custo |
|---|---|
| Extrusora 45 mm | R$ 120–250 mil |
| Matriz + calibrador | R$ 15–35 mil |
| Banho de resfriamento | R$ 25–60 mil |
| Puxador | R$ 30–70 mil |
| Bobinadeira | R$ 20–45 mil |
| Instalação, elétrica, área | R$ 20–50 mil |
| **Total** | **R$ 230.000 – 510.000** |

O consumo do projeto inteiro é **637 kg/ano**. A 15 m/min, a linha rodaria **283 horas por ano**
— **7% de dois turnos.** Ficaria parada 93% do tempo.

❌ **Não faz sentido.** Não é o processo que está errado — é a escala. Extrusão só paga com
tonelagem contínua, e aqui há meia tonelada por ano.

### Rota 3 — Injetar o anel em casa, com um molde de família ⭐

Esta é a rota que responde ao seu problema real ("não quero um molde por tamanho") **usando a
máquina que você já tem**.

Um **único molde**, com as quatro cavidades — uma de cada tamanho — e **bloqueio de cavidade**,
para injetar só o tamanho que a produção precisa naquele dia.

**A força de fechamento é ridícula:**

| Anel | Área projetada | Força necessária |
|---|---|---|
| 22×14 | 23,0 cm² | **8,2 tf** |
| 26×18 | 28,1 cm² | **10,0 tf** |

Contra injetoras de **150 a 200 tf** que já rodam essas tampas. Cabe com folga enorme — dá para
pôr múltiplas cavidades por tamanho.

| | |
|---|---|
| Investimento | R$ 70.000 – 140.000 (molde de família com bloqueio) |
| **Junta no aro** | **NENHUMA — o anel sai fechado da máquina** ✅ |
| Montagem | **só calçar = 7–10 s** ✅ |
| Ocupação de injetora | 4 cavidades → 602 h/ano = 15% de dois turnos |
| Escalar para nova tampa | **postiço novo, R$ 10–20 mil cada** ❌ |
| Custo | R$ 0,14/peça · **R$ 48.520/ano** |

---

## 3. Comparação

| | Rota 1 — fita comprada | Rota 2 — extrusora própria | **Rota 3 — anel injetado** |
|---|---|---|---|
| Investimento | **R$ 8–20 k** ✅ | R$ 230–510 k ❌ | R$ 70–140 k |
| Custo/peça | R$ 0,20 | R$ 0,16 | **R$ 0,14** ✅ |
| Custo/ano | R$ 69.314 | R$ 55.452 | **R$ 48.520** ✅ |
| **Junta (risco de vazar)** | uma por aro ❌ | uma por aro ❌ | **nenhuma** ✅ |
| Tempo de montagem | 15–25 s | 15–25 s | **7–10 s** ✅ |
| Depende de fornecedor externo | sim ❌ | não | **não** ✅ |
| **Escalar para a 5ª tampa** | **R$ 0** ✅ | **R$ 0** ✅ | R$ 10–20 k ❌ |
| Reversível se falhar | sim | não | sim (o molde é só do aro) |

---

## 4. A recomendação, e ela é em duas etapas

### Agora: Rota 1, para provar o conceito

Comprar a fita e cortar. **R$ 8–20 mil**, sem molde nenhum. Isso responde as perguntas que ainda
não têm resposta — o aro veda? fica no lugar? a tampa continua fácil de abrir? — **com o menor
dinheiro possível em risco.**

Não faz sentido comprar molde de R$ 70–140 mil para descobrir a cota de interferência.

### Depois que funcionar: Rota 3, se o volume justificar

A Rota 3 é melhor em quase tudo — sem junta, montagem 2× mais rápida, R$ 20.794/ano mais barata,
sem depender de fornecedor. **Ela se paga em 3 a 7 anos só pela diferença de custo**, o que
sozinho não justifica.

**O que justifica é a junta.** 346 mil emendas por ano, cada uma um ponto de vazamento potencial
num produto cujo apelo é justamente não vazar. Se o piloto da Rota 1 mostrar falha de junta em
campo, a Rota 3 deixa de ser otimização de custo e vira necessidade de qualidade.

### E a Rota 2 está descartada

Meia tonelada por ano não paga uma linha de extrusão. Se um dia a aplicação for para as 18 tampas
da linha inteira, ainda assim seria 1,4 t/ano e 15% de um turno. **Comprar sempre será mais
barato que extrudar em casa nessa escala.**

---

## 5. O que muda no projeto do aro

Nada da geometria muda. O perfil em U calçado na saia (documento 10) serve tanto para fita cortada
quanto para anel injetado — **é a mesma seção, produzida de dois jeitos diferentes.**

Só um detalhe muda se a Rota 3 for adiante: um anel injetado pode ter **variação de seção ao longo
do perímetro** (mais reforço nos cantos, por exemplo), coisa que fita extrudada não permite. Isso é
uma carta na manga para depois, não uma decisão de agora.

---

## Resumo

1. **Injetora não faz bobina** — o ciclo é a essência da máquina, e falta todo o trem de
   calibração, resfriamento, puxamento e bobinamento.
2. **Mas suas injetoras rodam TPE sem modificação.** Isso abre a Rota 3.
3. **Extrusora própria está descartada:** R$ 230–510 mil para rodar 7% de dois turnos.
4. **Comece comprando fita** (R$ 8–20 mil) para provar o conceito.
5. **Se funcionar, avalie injetar o anel** num molde de família de 4 cavidades — sem junta,
   montagem 2× mais rápida, R$ 48,5 mil/ano contra R$ 69,3 mil.

---

# ADENDO — Molde de família balanceado por demanda

**Pergunta:** *"no mesmo molde eu tenho o aro G, aí de repente eu coloco dois M e três P."*

**Sim, é exatamente assim que se faz** — chama-se molde de família balanceado por demanda. Com os
seus números, funciona ainda melhor do que a proporção que você imaginou. Três ajustes.

## 1. A proporção não é 1G : 2M : 3P — e o motivo é estrutural

O maior volume **não é o pote menor.** É o A1 (22×14), e por uma razão que vale entender:

| Aro | Demanda/ano | Serve | |
|---|---:|---|---|
| **A1 22×14** | **155.949** | Raso 1,1 L + Alto 2,2 L | **dois produtos** |
| A2 26×18 | 80.346 | Raso 2,3 L + Alto 4,3 L | **dois produtos** |
| A3 20×19 | 68.257 | Quadrado 1,8 L | um |
| A4 25×16,5 | 42.020 | Ultraforte 2,1 L | um |

A proporção real é **3,71 : 1,91 : 1,62 : 1**, e ela vem da **demanda**, não do tamanho da peça.
O A1 domina porque é a única tampa que serve dois produtos de alto giro.

## 2. O limitante é a ÁREA do molde, não a tonelagem

Aqui está o que quase derruba a ideia de pôr os quatro no mesmo molde. Um anel é **vazado no
meio** — ocupa muita área de molde e quase nenhuma tonelagem:

| Arranjo | Excesso | Área | Lado aprox. | Força | Menor injetora que aceita |
|---|---:|---:|---:|---:|---|
| 4 : 2 : 2 : 1 (proporção ideal) | 8,4% | 4.476 cm² | ~84 cm | **92 tf** | **600 tf** ❌ |
| 2 : 1 : 1 : 1 | 13,7% | 2.511 cm² | ~63 cm | 52 tf | 380 tf ❌ |
| 1 : 1 : 1 : 1 | 44,4% | 2.086 cm² | ~57 cm | 42 tf | 250 tf |

**Precisaria de 92 tf de força e de uma máquina de 600 tf** — não pela força, mas porque o molde
não caberia entre as colunas de nada menor. Rodar 92 tf numa 600 tf é pagar hora-máquina de
máquina grande para fazer trabalho de máquina pequena.

*(Espaço entre colunas por tonelagem é estimativa de engenharia — **confirmar nas máquinas
reais** antes de fechar o projeto do molde.)*

## 3. A solução: dois moldes pequenos, não um grande

| Molde | Cavidades | Excesso | Área | Força | Injetora | Horas/ano |
|---|---|---:|---:|---:|---|---:|
| **1** | **2× A1 + 1× A2** | **2,0%** | 1.459 cm² (~48×48) | **30 tf** | **200 tf** ✅ | 558 h |
| **2** | **2× A3 + 1× A4** | 12,5% | 1.558 cm² (~49×49) | **31 tf** | **200 tf** ✅ | 292 h |

Os dois cabem nas injetoras de 200 tf que **já rodam essas tampas hoje**.

### E com bloqueio de cavidade o excesso vai a ZERO

É aqui que a sua ideia fica redonda. Roda o molde cheio até completar o item que satura primeiro,
depois **bloqueia as cavidades prontas** e roda só o que falta:

**Molde 1** — 77.974 ciclos com tudo aberto → A1 completo (155.949 ✓), A2 em 77.974.
Bloqueia o A1, roda 2.372 ciclos só de A2. **Total 80.346 ciclos, excesso zero.**

**Molde 2** — 34.128 ciclos com tudo aberto → A3 completo (68.257 ✓), A4 em 34.128.
Bloqueia o A3, roda 7.892 ciclos só de A4. **Total 42.020 ciclos, excesso zero.**

**850 horas de injetora por ano somando os dois** — 21% de dois turnos de uma máquina de 200 tf.

## 4. O que precisa de atenção no projeto do molde

⚠️ **Balanceamento de enchimento.** Cavidades de tamanhos diferentes enchem em tempos diferentes —
a maior demora mais. Desbalanceado, a menor superpacka (rebarba, tensão interna) e a maior sai
incompleta. **No caso do aro é mais fácil que o normal**, porque a seção é a mesma em todas: o que
muda é só o comprimento do caminho, e isso se corrige **dimensionando os canais** (canal escalonado,
mais estreito para a cavidade menor). Exigir do ferramenteiro o estudo de balanceamento — é o item
técnico nº 1 do molde.

⚠️ **O bloqueio precisa ser previsto no projeto**, não improvisado depois: obturador de canal por
cavidade, acessível sem desmontar o molde.

⚠️ **Confirmar o espaço entre colunas** das injetoras de 200 tf antes de fechar a área do molde.

## 5. Investimento revisado

| | |
|---|---|
| Molde 1 (2× A1 + 1× A2, com bloqueio) | R$ 40.000 – 70.000 |
| Molde 2 (2× A3 + 1× A4, com bloqueio) | R$ 40.000 – 70.000 |
| **Total** | **R$ 80.000 – 140.000** |

Mesma faixa do molde de família único de 4 cavidades — **mas rodando em máquina de 200 tf em vez
de 600 tf**, o que muda o custo por hora de produção, e com excesso zero em vez de 8 a 14%.

**A recomendação do corpo deste documento não muda:** comece comprando fita (R$ 8–20 mil) para
provar o conceito. O molde de família é o passo dois, quando a geometria estiver validada.
