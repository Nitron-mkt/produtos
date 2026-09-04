# Como o PDV chega ao lojista — duas rotas

Rev. 2 · 04/09/2026 · substitui a versão de quatro rotas.
Saíram **coparticipação** e **comodato** por decisão do usuário: ficam
**venda direta** e **bonificação por volume**.

Custos por módulo em `dados/26-pdv-escada-comercial-rev3.csv`, na estrutura de
medida fixa (`analise/11-nitron-mob-cota-final.md`).
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

## As duas rotas

| Rota | O que o lojista faz | O que a Nitron entrega | Prova preço? |
|---|---|---|---|
| **1 · Venda direta** | paga 2 × o custo de material | nota de venda, ativo do lojista no ato | **sim** |
| **2 · Bonificação por volume** | compra a faixa cheia no período | móvel sem custo, `CODTIPOPER` 3220 | **não** |

### 1 · Venda direta
Preço = **2,00 × custo**, o piso da tabela. Não depende de meta de compra: serve para quem
quer o móvel independente de volume e para não-cliente. Faixa hoje: **R$ 333 a R$ 4.457**
conforme o módulo — o checkout P entra abaixo de R$ 350.

### 2 · Bonificação por volume — o "ganhando"
Comprou a faixa no período, o móvel vai sem custo e passa a ser do lojista. O ERP já tem a
operação: **`CODTIPOPER` 3220 Bonificação Especial**, que apareceu no histórico da própria
Nitron Mob.

---

## A escada, módulo por módulo

Doze módulos: quatro famílias × três versões (P/M/G por número de vãos).

| Módulo | Painel | Medida final (mm) | Custo est. | Venda direta (2×) | 20 × custo | **Faixa qualificadora** |
|---|---|---|---|---|---|---|
| Checkout P | 300 × 450 | 457 × 372 × 1.140 | R$ 167 | R$ 333 | R$ 3.331 | **R$ 10.000** |
| Ilha P | 460 × 634 | 637 × 500 × 878 | R$ 241 | R$ 482 | R$ 4.823 | **R$ 10.000** |
| Checkout M | 300 × 450 | 892 × 372 × 1.140 | R$ 314 | R$ 629 | R$ 6.286 | **R$ 10.000** |
| Checkout G | 300 × 450 | 1.327 × 372 × 1.140 | R$ 462 | R$ 924 | R$ 9.242 | **R$ 10.000** |
| Ilha M | 460 × 634 | 1.252 × 500 × 878 | R$ 465 | R$ 931 | R$ 9.308 | **R$ 10.000** |
| Ponta P | 300 × 634 | 637 × 372 × 1.664 | R$ 485 | R$ 971 | R$ 9.708 | **R$ 10.000** |
| Ilha G | 460 × 634 | 1.867 × 500 × 878 | R$ 690 | R$ 1.379 | R$ 13.794 | **R$ 15.000** |
| Ponta M | 300 × 634 | 1.252 × 372 × 1.664 | R$ 944 | R$ 1.888 | R$ 18.876 | **R$ 25.000** |
| Paredão P | 200 × 754 | 2.233 × 285 × 1.926 | R$ 1.348 | R$ 2.697 | R$ 26.965 | **R$ 40.000** |
| Ponta G | 300 × 634 | 1.867 × 372 × 1.664 | R$ 1.402 | R$ 2.804 | R$ 28.043 | **R$ 40.000** |
| Paredão M | 200 × 754 | 2.970 × 285 × 1.926 | R$ 1.788 | R$ 3.577 | R$ 35.766 | **R$ 40.000** |
| Paredão G | 200 × 754 | 3.707 × 285 × 1.926 | R$ 2.228 | R$ 4.457 | R$ 44.566 | **R$ 65.000** |

Para converter em caixas: divida a faixa pelo preço médio de caixa. A **R$ 250 por caixa**,
a faixa de R$ 10 k são **40 caixas** e a de R$ 65 k são **260 caixas**. O portal faz essa
conversão ao vivo com o preço que você informar.

**Seis dos doze módulos caem na primeira faixa (R$ 10 k).** É a consequência de a estrutura
nova ser mais barata que a Rev. 2 — o checkout M caiu de R$ 711 para R$ 314, porque o painel
passou de 435 × 431 mm para 300 × 450 e a altura de 6 para 5 prateleiras. Na prática,
**a escada só começa a discriminar de verdade a partir da ponta M**.

---

## A armadilha, e ela ficou mais apertada com duas rotas

O curador de portfólio pôs uma condição para a linha seguir: **uma venda a ≥ 2,00 × `CUSGER`
para ≥ 3 clientes distintos, sem `CODTIPOPER` 3211 (amostra) nem 3220 (bonificação)**.

Na versão de quatro rotas havia **duas** que geravam nota (compra e coparticipação). Agora há
**uma só**. Ou seja: **se o programa rodar predominantemente por bonificação, a linha nunca
prova preço** — e continua travada onde está hoje (R$ 4.146,90 na vida, 2 parceiros, margem
realizada de −49,3%).

Recomendação de desenho do programa, ajustada:

1. **Venda direta é a rota oferecida primeiro**, sempre. É a única que gera nota.
2. **Bonificação como aceleradora, não como porta de entrada** — para o cliente que já compra
   volume, não como forma de começar.
3. **Meta explícita: os 3 primeiros PDVs saem por venda direta.** É o que destrava o veredito
   do portfólio, e agora não há rota alternativa que também sirva.
4. O preço de venda direta ajuda: com o checkout P a **R$ 333** e o M a **R$ 629**, a venda
   direta virou uma proposta pequena o suficiente para ser aceita sem contrapartida — o que
   não era verdade quando o módulo de entrada custava R$ 965.

---

## Nota de escopo do portal

O portal (`frontend/monte-seu-pdv.html`) é um **documento único e autônomo, sem chave de
API** — sobe em qualquer host estático e funciona offline. Ele não lê o Supabase.

A versão de artefato (`frontend/_artifact-monte-seu-pdv.html`) declara `db` para gravar a
fila de solicitações, e um artefato que declara `db` é **interno à organização** — não pode
ser compartilhado publicamente. Na prática:

- **A versão de artefato funciona hoje** como ferramenta do representante: ele configura junto
  com o lojista, e o time comercial lê a fila.
- **Para autoatendimento público** use o arquivo autônomo em domínio próprio, apontando
  `ENDPOINT` para um backend seu. Sem `ENDPOINT`, ele cai em e-mail, download do JSON e
  impressão — o que já resolve o piloto.

O portal é o protótipo do fluxo e a especificação viva do configurador — a matemática dele é
a mesma do caderno de especificação e do documento de cota.
