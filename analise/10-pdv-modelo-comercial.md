# Como o PDV chega ao lojista — quatro rotas

Todas as contas saem do custo estimado por módulo (`dados/17-pdv-12-modulos.csv`).
⚠️ Custo **estimado por escala de massa, não apurado** — depende de reconciliar o custo da
madeira, que hoje está corrompido no ERP.

---

## A base da conta

A tabela padrão da Nitron tem **piso em 2,00 × `CUSGER`**, ou seja **margem bruta de 50%**.
Então, para uma compra de valor `V`, a margem gerada é `0,50 × V`.

O teto usual de investimento em material de PDV é **10% da margem que a compra gera**.
Logo, para um módulo de custo `C`:

```
C ≤ 0,10 × 0,50 × V     →     V ≥ 20 × C
```

**A compra qualificadora é 20 × o custo do móvel**, arredondada para cima na escada comercial
de R$ 10 k · 15 k · 25 k · 40 k · 65 k · 100 k · 150 k.

---

## As quatro rotas

| Rota | O que o lojista faz | O que a Nitron entrega | Prova preço? |
|---|---|---|---|
| **1 · Compra** | paga 2 × custo | nota de venda, ativo do lojista | **sim** |
| **2 · Coparticipação 50/50** | paga 50% do móvel **e** compra metade da faixa | nota de venda parcial | **sim** |
| **3 · Bonificação por volume** | compra a faixa cheia no período | móvel sem custo, `CODTIPOPER` 3220 | **não** |
| **4 · Comodato** | assina contrato de exposição | móvel cedido, ativo fica da Nitron | **não** |

### 1 · Compra
Preço = **2,00 × custo**, o piso da tabela. Para quem quer o móvel independente de volume, ou
para não-cliente. Faixa: **R$ 759 a R$ 6.270** conforme o módulo.

### 2 · Coparticipação 50/50 — a que costuma converter mais
O lojista paga metade do móvel e compra metade da faixa qualificadora. Menos atrito que a
compra pura, e **ainda gera nota de venda** — então conta para o teste de preço.

### 3 · Bonificação por volume — o "ganhando"
Comprou a faixa no período, o móvel vai sem custo. O ERP já tem a operação:
**`CODTIPOPER` 3220 Bonificação Especial**, que apareceu no histórico da própria Nitron Mob.

### 4 · Comodato
O móvel continua da Nitron, cedido por contrato de exposição: mix mínimo, ocupação combinada
e prazo. Indicado para **paredão e ponta de gôndola** — os módulos caros, que a Nitron
recupera se o cliente sair. Exige contrato e o ativo permanece no balanço.

---

## A escada, módulo por módulo

| Módulo | Custo est. | Compra (2×) | 20 × custo | **Faixa qualificadora** |
|---|---|---|---|---|
| Ilha P | R$ 380 | R$ 759 | R$ 7.594 | **R$ 10.000** |
| Checkout P | R$ 482 | R$ 965 | R$ 9.648 | **R$ 10.000** |
| Ponta P | R$ 545 | R$ 1.090 | R$ 10.903 | **R$ 15.000** |
| Checkout M | R$ 711 | R$ 1.423 | R$ 14.227 | **R$ 15.000** |
| Ilha M | R$ 737 | R$ 1.475 | R$ 14.746 | **R$ 15.000** |
| Checkout G | R$ 940 | R$ 1.881 | R$ 18.806 | **R$ 25.000** |
| Ponta M | R$ 1.057 | R$ 2.114 | R$ 21.142 | **R$ 25.000** |
| Ilha G | R$ 1.095 | R$ 2.190 | R$ 21.898 | **R$ 25.000** |
| Ponta G | R$ 1.569 | R$ 3.138 | R$ 31.382 | **R$ 40.000** |
| Paredão P | R$ 1.893 | R$ 3.787 | R$ 37.867 | **R$ 40.000** |
| Paredão M | R$ 2.514 | R$ 5.028 | R$ 50.282 | **R$ 65.000** |
| Paredão G | R$ 3.135 | R$ 6.270 | R$ 62.697 | **R$ 65.000** |

Para converter em caixas: divida a faixa pelo preço médio de caixa. A **R$ 250 por caixa**,
a faixa de R$ 10 k são **40 caixas** e a de R$ 65 k são **260 caixas**. O portal faz essa
conversão ao vivo com o preço que você informar.

---

## A armadilha que precisa estar na mesa

O curador de portfólio pôs uma condição para a linha seguir: **uma venda a ≥ 2,00 × `CUSGER`
para ≥ 3 clientes distintos, sem `CODTIPOPER` 3211 (amostra) nem 3220 (bonificação)**.

**Se todo PDV sair como bonificação ou comodato, a linha nunca prova preço** — e continua
travada no mesmo lugar onde está hoje (R$ 4.146,90 na vida, 2 parceiros, margem realizada de
−49,3%).

Daí a recomendação de desenho do programa:

1. **A rota de compra e a de coparticipação têm de existir e ser oferecidas primeiro.** São as
   duas que geram nota de venda.
2. **Bonificação como aceleradora, não como padrão** — para o cliente que já compra volume,
   não como forma de entrar.
3. **Comodato reservado ao paredão e à ponta de gôndola**, onde o valor do ativo justifica o
   contrato e a Nitron quer o móvel de volta se o cliente sair.
4. **Meta explícita: os 3 primeiros PDVs saem pela rota 1 ou 2.** É o que destrava o veredito
   do portfólio.

---

## Nota de escopo do portal

O portal (`frontend/monte-seu-pdv.html`) grava as solicitações no banco do artefato, e um
artefato que declara `db` é **interno à organização** — não pode ser compartilhado
publicamente. Na prática:

- **Funciona hoje** como ferramenta do representante: ele configura junto com o lojista, e o
  time comercial lê a fila de solicitações.
- **Não serve** como portal público de autoatendimento para o lojista final. Para isso seria
  preciso uma aplicação web de verdade, com domínio, autenticação e integração ao Sankhya.

O portal é o protótipo do fluxo e a especificação viva do configurador — a matemática dele é
a mesma do caderno de especificação.
