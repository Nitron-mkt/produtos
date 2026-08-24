# Fase 2 — Potes: a lista de lançamento

Raspagem executada em 24/08/2026 via Apify (actor `sourabhbgp/mercadolibre-scraper`,
proxy residencial, plano SCALE). **6 runs, 267 itens, custo total ~US$ 0,90.**

## Por que Potes e não Micro-ondas

O meu score dizia Potes 8/20 e Micro-ondas 15/20. Contrariei o score por dois
motivos que ele não mede:

1. **Pool de lucro.** Potes gera R$ 7,2 M de lucro bruto contra R$ 890 k de
   Micro-ondas — 8×. Um lançamento razoável em Potes move mais que um excelente
   em Micro-ondas.
2. **Equity de marca.** O score não tem entrada para "somos conhecidos por potes".
   Isso muda o custo de entrada de um lançamento.

O que o score de saturação dizia de verdade não era "não vá" — era **"não vá com
SKU avulso"**. Isso é forma, não veto. Toda a lista abaixo é kit ou cor.

Micro-ondas fica na lista, em quarto.

## O que a raspagem mostrou

| Medida | Resultado |
|---|---|
| Itens coletados | **267** (129 marcas) |
| Kits | **190 de 267 — 71%** |
| Tier A presentes | 6 marcas, 28 itens |
| Nitron | apenas 2 itens |
| Kit 5 peças | R$ 26,90 a R$ 185,95 · médio **R$ 55,14** |
| Kit **com válvula** | médio **R$ 99,07** |
| Kit **sem válvula** | médio **R$ 71,83** |

**Premium de válvula medido no mercado: +38%.** É a primeira confirmação externa
de que válvula é atributo que o consumidor paga — até agora eu só tinha o vetor
interno (+1.297% no 2,9L).

E o mercado desse espaço vende kit: 71% dos anúncios.

### Tier A no espaço de potes

| Marca | Itens | Preço médio | Faixa | Nota |
|---|---|---|---|---|
| Sanremo | 11 | R$ 37,82 | 25,14 – 72,90 | 4,81 |
| Paramount | 7 | R$ 69,19 | 29,90 – 149,90 | 4,91 |
| Ou | 4 | R$ 70,71 | 50,00 – 89,94 | 4,87 |
| Tramontina | 3 | R$ 84,55 | 61,67 – 95,99 | 4,80 |
| Uninjet | 2 | R$ 40,96 | 39,20 – 42,71 | 4,80 |
| Injetemp | 1 | R$ 33,00 | — | 4,50 |

**Sanremo é o concorrente de preço** (médio R$ 37,82, o mais baixo). E as notas
vão de 4,80 a 4,91: **não existe concorrente com produto ruim para atacar por
qualidade** nesse espaço. O ataque tem que ser por atributo ou por composição de
kit, não por "o deles é pior".

### Ressalva de leitura que importa

Os R$ 55 do ML são **varejo ao consumidor final**. O preço-alvo de R$ 24 é
**saída de fábrica para atacado**. Não são comparáveis direto. O que o dado mostra
é que existe cerca de 2× de margem de canal — espaço confortável — e não que o
preço-alvo esteja errado.

## Os três achados do Sankhya que nomeiam os itens

1. **A família válvula tem 9 tamanhos ativos e nenhum kit.** Os avulsos somam
   R$ 1,47 M em 12 meses e os três tamanhos novos fizeram +530%, +1.297% e +1.032%.
   O vetor mais forte do banco está sem a embalagem que multiplica ticket.
2. **Kit 5 peças tem ticket de R$ 22 a 28 contra R$ 5 do avulso**, com MB de 50,6%
   (preto) e 54,4% (branco).
3. **Os 5 SKUs "acoplado rosca 1L" da safra 2025/26 têm MB de 11,7% a 26,5%** e
   faturam R$ 16 k somados. Os equivalentes de 2L fazem R$ 113 k a R$ 240 k com MB
   de 48 a 52%. É a proliferação que diagnostiquei na Fase 1, acontecendo ao vivo.

## A lista — `pdp_lancamento` no Supabase

| # | Produto | Tipo | Molde | Preço alvo | MB alvo |
|---|---|---|---|---|---|
| 1 | **Kit Potes com Válvula 4 peças** (950ml + 1,9L + 2,9L + 4,6L) | kit | existente | R$ 24 | 50% |
| 2 | **Kit Mantimentos Acoplado Rosca 5 peças — CHUMBO** | extensão de cor | existente | R$ 26 | 52% |
| 3 | **Pote Ultraforte CHUMBO** — 2,1L, 4L, 6,9L | extensão de cor | existente | R$ 11,40 | 52% |
| 4 | **Kit Micro-ondas** — caçarola 2,6L + tampa + omeleteira | kit | existente | R$ 18 | 53% |
| 5 | **Descontinuar** os 5 SKUs Acoplado Rosca 1L | descontinuar | — | — | — |

**Nenhum item exige molde novo.** Os cinco são composição, pigmento ou embalagem.

O campo `status` é para o time mover: `proposto → aprovado → em_ferramentaria →
lancado`, ou `descartado` com o motivo em `risco`.

## O que ficou de fora e por quê

**Avaliações.** Pedi `includeReviews` nos 6 runs e os datasets têm as avaliações,
mas eu puxei só os campos de produto para as tabelas. Os 6 dataset IDs estão
registrados — dá para minerar o texto das avaliações sem rodar nada de novo,
sem custo adicional.

É o que falta para responder "que defeito do concorrente meu produto corrige",
e é o que transforma o Kit Válvula de "mesma coisa com feature" em projeto
diferenciado. Sugiro isso como próximo passo.

## Nota operacional

A fila do `pg_net` deste projeto tem cron de minuto e ficou lenta: cada request
levou de 1 a 4 minutos para sair. Funcionou, mas coleta recorrente precisa de
throttle próprio ou de uma Edge Function dedicada, para não competir com o
pipeline de produção do CRM.
