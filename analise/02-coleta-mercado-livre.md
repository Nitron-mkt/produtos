# Fase 2 — Rota de coleta no Mercado Livre

Testado em 24/08/2026, com o token OAuth e o token Apify já guardados em
`ml_oauth_app` / `ml_oauth_token` (projeto `integracao-crm-sankhya`).

## O que funciona e o que não

| Rota | Status | Serve para |
|---|---|---|
| `GET /products/search?site_id=MLB&status=active&q=…` | **200** | Descobrir catálogos por termo. Retornou `paging.total: 10000` para "lixeira pedal 6l" |
| `GET /products/{catalog_product_id}` | **200** | **Nome, `attributes.BRAND` estruturado, MODEL, `buy_box_winner`** |
| `GET /products/{id}/items` | 404 | Não usar |
| `GET /sites/MLB/search` | **403** | Restringido pelo ML. Era o que eu tentei primeiro |
| `GET /users/me` | 200 | Conta: "VIDA CASA" / NITRONPLAST, id 768797214 |
| `https://api.apify.com/v2/users/me` | **200** | Token válido, plano **SCALE** |
| Raspagem direta do site, deste container | **bloqueada** | `ERR_CONNECTION_RESET`, mesmo com Chromium real |

## O achado que decide a arquitetura

O `/products/{id}` devolve a **marca em campo estruturado**:

```
name:  "Kit2 Lixeira Pedal 6l Cesto Lixo Banheiro Cozinha Ou - Azul"
BRAND: "Ou"          <- Tier A, casado automaticamente
MODEL: "Pedal 6L Azul"
```

Casar SKU da Nitron com produto de concorrente é a parte difícil do cruzamento
item × Tier A. Com `BRAND` estruturado, isso deixa de ser heurística de string.
E o primeiro resultado de um termo aleatório já era um concorrente Tier A.

## Recomendação: híbrido, começando pela API oficial

**API oficial faz o cruzamento (custo zero, já pago no token):**
1. Para cada termo das linhas priorizadas → `/products/search` → lista de catálogos
2. Para cada catálogo → `/products/{id}` → marca, modelo, `buy_box_winner` (preço + seller)
3. Filtrar `BRAND` contra `pdp_concorrente` → cruzamento item × Tier A pronto

**Apify entra onde a API não vai:**
- **Avaliações** (`sourabhbgp/mercadolibre-scraper`, 15.254 runs, cobre Products +
  Reviews + Q&A + Sellers). É a lacuna que importa: o diferencial de projeto de
  cada certeiro sai do que o consumidor reclama do concorrente.
- **Preço e quantidade vendida quando o `buy_box_winner` vem nulo** — aconteceu no
  primeiro teste. Aí só lendo o anúncio.

Ordem importa: rodar a API oficial primeiro reduz o volume que vai para o Apify
ao conjunto que realmente interessa, em vez de raspar categoria inteira.

## Onde o pipeline deve morar

Ao lado das funções que já existem (`ml-catalogo-ean`, `ml-catalogos`,
`ml-item-ean`, `ml-osint`), usando `pg_net` ou uma Edge Function nova. O token
nunca sai do banco — foi assim que testei.

Atenção: a fila do `pg_net` deste projeto tem um cron rodando a cada minuto.
Meus 3 requests de teste levaram alguns minutos para sair. Coleta em lote precisa
de throttle, ou vai competir com o pipeline de produção.

## Decisões que faltam

1. **Por qual concorrente e categoria começar.** Sugiro Ou em Lixeiras e Banheiro
   (aparece nas duas frentes que recomendo mexer, e já apareceu no teste), mais
   Plastutti e Rainha em Potes (declaram "herméticos" e "com trava", que é o vetor
   válvula).
2. **Autorização de gasto no Apify.** Os actors são PAY_PER_EVENT; o preço só
   aparece autenticado no seu console. Não rodei nada que gere custo.
3. **Volume por rodada** — quantos catálogos por linha, para dimensionar.
