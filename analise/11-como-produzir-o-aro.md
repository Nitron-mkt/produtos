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
