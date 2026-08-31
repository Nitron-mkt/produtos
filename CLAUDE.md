# Projeto de Desenvolvimento de Produtos — Nitron

Squad de agentes para decidir **o que lançar e o que não lançar** no portfólio de
utilidades domésticas da Nitron, com base em dados do ERP, do mercado e da fábrica.

Leia este arquivo inteiro antes de agir. Ele contém armadilhas que já custaram
retrabalho — inclusive conclusões erradas que foram publicadas e depois corrigidas.

---

## 1. Conexões obrigatórias

O squad **não funciona** sem os dois MCPs abaixo. Se algum estiver desconectado,
diga isso ao usuário em vez de responder de memória.

| MCP | Uso | Modo |
|---|---|---|
| **Sankhya** | ERP: faturamento, custo, cadastro, apontamento de produção | somente leitura (`sankhya_query` bloqueia escrita) |
| **Supabase** | Onde as conclusões são gravadas (tabelas `pdp_*`) e onde vivem os tokens de ML/Apify | leitura e escrita |

Projeto Supabase: **`bwbeieumxcuomtrvlqxs`** (nome: `integracao-crm-sankhya`).
Não use o projeto `afiliados`.

**Teste de fumaça antes de qualquer análise** (confirmado em 24/08/2026):
`SELECT COUNT(*) FROM pdp_linha` → **17** · `SELECT COUNT(*) FROM TGFPRO WHERE
CODGRUPOPROD BETWEEN 1000000 AND 1009999` → **4.252**. Se algum falhar, conserte a
conexão antes de seguir — não responda de memória.

### ⚠️ Segurança — leia antes de qualquer front-end
Esse projeto Supabase tem **89 tabelas com RLS desligado**, incluindo dado de cliente
(`contato_enriquecido` 21 k linhas, `ghl_cliente` 10 k, `parc_matriz` 3,7 k,
`cobranca_cliente`). A chave anon dá leitura **e escrita** nelas.

- As tabelas `pdp_*` nascem com RLS ligado e só política de SELECT — essas estão certas.
- **Nunca** publique front-end com a chave anon em URL pública antes de resolver o RLS.
- **Nunca** imprima `ml_oauth_token.access_token` nem `ml_oauth_app.apify_token` na
  conversa. Use-os dentro do SQL (`net.http_get(headers := ... (SELECT ...))`).

---

## 2. Sankhya — como consultar sem errar

### O recorte correto de faturamento

```sql
-- Empresas da Nitronplast: 1 (Matriz), 2 (Filial), 14 (Extrema, abriu em 2025)
-- Grupo Produto Acabado/Revenda: CODGRUPOPROD entre 1000000 e 1009999
CAB.CODEMP IN (1,2,14)
AND CAB.STATUSNOTA = 'L'
AND CAB.TIPMOV IN ('V','D')          -- devolução entra com sinal -1
AND TOP.ATUALFIN <> 0                 -- só o que atualiza financeiro
AND CAB.CODTIPOPER NOT IN (3316,3300,3261,3242,3310,3322)  -- transferências intercompany
```

Join do TOP exige as duas colunas:
`JOIN TGFTOP TOP ON TOP.CODTIPOPER=CAB.CODTIPOPER AND TOP.DHALTER=CAB.DHTIPOPER`

### Tabela de preço — a armadilha nº 1

A **"003 tabela padrão"** é **`CODTAB = 0`** (`PV0003 - TABELA PADRÃO`).
**`CODTAB = 3` é `TABELA EXPORTAÇÃO NITRON`** — assumir o número 3 traz a curva errada.

Caminho: `TGFITE.NUTAB → TGFTAB.NUTAB → TGFTAB.CODTAB`, nome em `TGFNTA.NOMETAB`.

**Sempre exclua** para ter a curva de marca própria:
- `CODTAB = 84` → `PV0134 - AVON` (é Natura/Avon). Fez R$ 8,97 M em **580 itens** nos
  últimos 12 M. Distorce tudo: infla linhas inteiras e conta SKU OEM como "acerto de lançamento".
- `CODTAB = 3` → exportação.

```sql
LEFT JOIN TGFTAB TAB ON TAB.NUTAB = ITE.NUTAB
WHERE NVL(TAB.CODTAB,-1) NOT IN (84,3)
```

**Não use a tabela padrão sozinha para medir tendência.** Ela caiu 73% em 2 anos, mas
isso é **migração de tabela**, não demanda: Extrema abriu em 2025 e o programa Clube
Nitron nasceu no último ciclo; as tabelas novas absorveram ~R$ 37 M, quase o que a
padrão perdeu. Use a padrão para **teto de preço e margem** (MB de 60–80% lá, contra
45–55% na média — o desconto de canal come 15 a 25 pontos).

### Custo e margem

```sql
-- TGFCUS, último registro do ano corrente, empresa 1, local 0
SELECT CODPROD, CUSGER FROM (
  SELECT CODPROD, CUSGER, ROW_NUMBER() OVER (PARTITION BY CODPROD ORDER BY DTATUAL DESC) RN
  FROM TGFCUS WHERE CODEMP=1 AND CODLOCAL=0 AND CUSGER>0 AND DTATUAL >= DATE '2026-01-01'
) WHERE RN=1
```

**`VW_CUSTO_PRODUTO_FINAL` dá timeout (60 s). Não use.**

### Referência de produto — a armadilha nº 2

`TGFPRO.REFERENCIA` tem formato **`NNN.012.001`** (ex.: `233.012.001`).
**Nunca trunque para `233`.** Existem produtos homônimos com referência curta que são
private label de 2 a 4 clientes, enquanto o `.012.001` é o de canal com ~1.000 clientes.
Esse erro já produziu uma recomendação publicada e errada.

### Campos de cadastro que estão VAZIOS (não confie neles)

| Campo | Preenchido |
|---|---|
| `AD_TONELAGEMMIN` / `AD_TONELAGEMMAX` | 10 de 4.252 |
| `AD_QTDCAVIDADE` | 52 de 4.252 |
| `AD_CODCORPROD` | **0** — cor tem que sair da descrição |
| `AD_FICHATECNICA` (tabela) | 4 linhas |
| `TPRCPR` (roteiro) | 0 linhas |

### Capacidade de máquina

- Parque: `VW_MAQUINA_CAPACIDADE` — `QTDCAPACIDADEPAD` é a tonelagem. 56 injetoras na
  Nitron-Fábrica, 10 na Tanamu.
- Apontamento real: `AD_APONTACICLO` (CODPROD, CODWCP, DHPRODUCAO, DHTERMINOPRODUCAO, COR).
- **99,7% dos apontamentos são em Produto Intermediário (PI), não PA.** A injetora produz
  peça PI e a montagem vira PA. Não achamos a estrutura PA→PI numa view direta — se
  encontrar, documente aqui.
- Ocupação medida (12 M): **≤260 t = 56,9% com 7 de 15 máquinas paradas** ·
  261–1.100 t = 76,4% com **5 de 6 paradas** · 1.101–2.000 t = 73,5%, **zero livre** ·
  >2.000 t = 72,7%, **zero livre**.
- Ressalva: horas = `DHTERMINOPRODUCAO − DHPRODUCAO`, pode incluir tempo morto, então
  a ocupação real tende a ser **menor**.

---

## 3. Supabase — as tabelas do projeto

Prefixo `pdp_` (projeto de desenvolvimento de produtos), para não colidir com as ~130
tabelas do CRM que já vivem nesse banco.

| Tabela | Conteúdo |
|---|---|
| `pdp_linha` | 17 linhas: curva, margem, lucro, score 0-20, veredito, o que lançar, por que sim/não |
| `pdp_lancamento` | **A lista.** O que lançar em ordem de prioridade, com status (proposto → aprovado → em_ferramentaria → lancado → descartado) |
| `pdp_linha_concorrente` | Cruzamento linha × concorrente Tier A/D |
| `pdp_concorrente` | 26 concorrentes do mapa competitivo |
| `pdp_vetor` + `pdp_vetor_evidencia` | 8 vetores de crescimento e as evidências |
| `pdp_cor` | Performance das 16 cores |
| `pdp_capacidade` | Ocupação das injetoras por faixa |
| `pdp_lancamento_safra` | Taxa de acerto de lançamento por safra |
| `pdp_ml_oferta` | Ofertas coletadas no ML (267 já carregadas) |
| `pdp_ml_review` | Avaliações dos anúncios de concorrente (vazia — a coletar) |

Função auxiliar: `pdp_carrega_ml(run_id, termo, json)` normaliza e insere o dataset do Apify.

### pg_net é assíncrono e a fila é lenta

Esse projeto tem cron rodando a cada minuto. Requisições `net.http_get`/`net.http_post`
podem levar **minutos** para aparecer em `net._http_response`. Dispare, faça outra coisa,
volte para ler. Não conclua "não funcionou" sem esperar.

---

## 4. Mercado Livre — o que funciona

Testado em 24/08/2026 com o token da conta (`VIDA CASA` / NITRONPLAST, id 768797214).

| Rota | Status |
|---|---|
| `GET /products/search?site_id=MLB&status=active&q=…` | **200** ✅ |
| `GET /products/{catalog_product_id}` | **200** ✅ — traz `attributes.BRAND` **estruturado** |
| `GET /sites/MLB/search` | **403** ❌ restringido pelo ML |
| `GET /products/{id}/items` | 404 — não usar |
| Raspagem direta do site | **bloqueada** — `ERR_CONNECTION_RESET`, IP de datacenter |

**`attributes.BRAND` vindo estruturado é o que viabiliza o cruzamento item × concorrente** —
casar SKU da Nitron com produto de concorrente deixa de ser heurística de string.

### Apify (plano SCALE, token em `ml_oauth_app.apify_token`)

Actor: **`sourabhbgp/mercadolibre-scraper`** — modes: `search`, `product`, `reviews`, `seller`.
Input: `{mode, country:'BR', searchQuery, maxItems, scrapeProductDetails, includeReviews, useResidentialProxy:true}`
Custo medido: **~US$ 0,15 por run de 50-80 itens**, ~65 s. PAY_PER_EVENT.

`maxItems` alto não garante volume — "pote mantimento" devolveu 49 itens com maxItems=250.
Para volume, use **vários termos**, não um termo com limite alto.

**Atenção:** `revenda_catalogo` e `revenda_oferta_api` (tabelas antigas do CRM) apontam para
o catálogo da **própria Nitron**, não de concorrentes. `revenda_oferta_api.titulo` está 100%
nulo. Não confunda com dado de concorrência.

---

## 5. Conclusões já estabelecidas (não refaça)

### A curva
Marca própria, janelas móveis de 12 M: **R$ 101,4 M → R$ 96,1 M → R$ 83,1 M (−18%)**.
Lucro bruto R$ 41,4 M. Só duas linhas crescem: **Frasqueiras (+8,6%)** e **Decor Util (+21%)**.

### O achado principal
Taxa de acerto de lançamento (SKU que acumula R$ 500 k na vida), só marca própria:
**2021: 28,0% → 2022: 12,2% → 2023: 7,8% → 2024: 3,4% → 2025: 0,7% (2 de 278)**.
304 dos 357 SKUs de 2024 não passaram de R$ 100 k em dois anos.
**A recomendação nº 1 do projeto é lançar menos e melhor.**

### Os 8 vetores de crescimento (com evidência no faturamento)
V1 Válvula (Pote Alto 2,9L **+1.297%**) · V2 Cor chumbo (Lixeira Rattan Pedal 6L +208%) ·
V3 Acoplado+rosca (+566%) · V4 Flat/slim (+420%, 364→811 clientes) · V5 Nitronfort (+111%) ·
V6 Gadget "Fácil" (Churros +117%, 342→842 clientes) · V7 Kit/multipack · V8 Frasqueira cor/formato.

### Sobre cor
Das 16 cores, **só chumbo (+93%) e laranja (+82%) cresceram**; 14 caíram.
**Chumbo já está em 44 SKUs** — Lixeiras 12, Organização 13, Cozinha 12, Banheiro 3, Limpeza 1,
e **zero** em Frasqueiras, Potes, Jarras, Micro-ondas, Decor Util, Geladeira.
Parte do "+93%" é recadastro de SKUs "CINZA" → "CHUMBO" e "LISO" → "FLAT", par a par.
Ganho líquido da família cinza+chumbo: **+R$ 1,70 M**, não +R$ 2,57 M.
Laranja é a cor mais produtiva por SKU (R$ 233 k vs R$ 58 k do chumbo) porque é
**sinalização funcional** (Nitronfort = ferramenta), não decoração.

### Saturação competitiva (do `mapa_concorrentes_nitron.md`, 15 Tier A)
Organização **15 de 15** · Cozinha 12 · Potes 9 · Teca 7 (Tier D, Tramontina e Stolf
prioridade máxima) · Limpeza 4 · Lixeiras 4 · Banheiro 3 · Geladeira 2 · ECO 2 · Infantil 1 ·
**Frasqueiras, Micro-ondas, Jarras e Decor Util: ZERO**.

### Padrões finos já detectados
- **Alto está crescendo, Raso está caindo** na família com travas (Alto: 3 de 4 subindo;
  Raso: 3 de 4 caindo, só o 1,1L cresce).
- Os **5 SKUs "acoplado rosca 1L"** (CODPROD 13992-13996, safra 2025/26) têm MB de
  **11,7% a 26,5%** e faturam R$ 16 k somados, contra R$ 113-240 k dos 2L com MB 48-52%.
  Candidatos a descontinuação.
- Trava+válvula **já existe** (ref `176.024.001` e `210.024.001`) com **MB de 65,7% e 60,6%**
  — as melhores da família válvula — mas **caiu 57% e 39%**. Causa não investigada.
  Hipótese aberta: conflito funcional (válvula é abertura projetada; quem compra por
  hermeticidade se decepciona) ou creep do PE sob tensão de trava.

### Sobre claim "hermético"
Não há norma ABNT específica para utilidades; é claim publicitário sob o CDC, e o art. 36
obriga o fornecedor a manter os dados técnicos que sustentam a alegação.
Dos 267 anúncios coletados, **só 8 dizem "hermético" (3%)** e **apenas 1 desses tem válvula**.
Os que dizem "hermético + válvula" são de **vidro** com guarnição de silicone.
**Sanremo**, em plástico com válvula, escreve *"válvula micro ondas"* — evita o claim.
Material não cria hermeticidade; geometria de vedação + força de fechamento criam.

---

## 6. Lições de método (erros já cometidos neste projeto)

1. **Verifique se o produto já existe antes de propor lançar.** Dois "certeiros" foram
   publicados e estavam errados: "Caixa Organizadora Rattan chumbo" e "Lixeira Basculante
   Rattan chumbo" já existiam no catálogo.
2. **Não trunque referência.** `233` ≠ `233.012.001`.
3. **Score de categoria não decide sozinho.** O modelo de 4 critérios não tem entrada para
   equity de marca nem pondera pool de lucro absoluto. Potes marcou 8/20 e ainda assim é a
   escolha certa: R$ 7,2 M de lucro bruto contra R$ 890 k de Micro-ondas.
4. **Capacidade ociosa não é o mesmo que oportunidade.** Molde é 30-40% do custo de um
   lançamento; cadastro, EAN, arte, foto, catálogo, amostra, estoque e gôndola não ficam
   mais baratos porque o CNC está parado. E CNC parado pode ser sintoma de gargalo na
   ferramentaria (projeto, bancada, tryout), não folga real.
5. **Espere o `pg_net`.** Três requests foram declarados como "403 / não funciona" quando na
   verdade estavam na fila — e um deles era 200.

---

## 7. Squad de social media (fluxo Claude → OpenAI → Canva)

Cinco agentes próprios, documentados em **`SOCIAL.md`**: `estrategista-conteudo`,
`redator-legenda`, `diretor-arte`, `montador-canva`, `revisor-social` (tem veto).

**A decisão central — divisão de camadas:**
`camada 1 CENÁRIO` = GPT · `camada 2 PRODUTO` = foto real de `produto_foto` (749 SKUs) ·
`camada 3 MARCA` = Canva. **O GPT nunca gera o produto** — sai um SKU que não existe, e isso
é publicidade enganosa (CDC art. 37) além de ficar ruim.

### Não tem n8n — e isso foi decidido, não esquecido (28/08/2026)

1. **O n8n não chamaria o Claude Code.** Não há endpoint de entrada; agente `.md` só roda em
   sessão aberta. Fluxo que "volta pro Claude" no meio para e espera um humano.
2. **O n8n não chamaria o MCP do Canva.** Precisaria da Canva Connect API com app OAuth.
3. **O projeto já é orquestrador** — ~70 crons e 54 Edge Functions. n8n seria um segundo
   agendador e uma segunda fonte de verdade.

Então os dois passos automáticos são Edge Function: **`social-imagem`** (gpt-image-1 gera o
cenário → bucket público `social`) e **`social-qa`** (`claude-sonnet-5` com visão avalia).
O contrato é REST puro sobre `social_post`, então n8n ainda pode entrar depois sem mudar nada.

### Armadilhas verificadas

- **`gpt-image-1` não aceita 1080×1350.** Só 1024×1024, 1024×1536 e 1536×1024. Geramos em
  1024×1536 e o **Canva recorta**. Não escreva pixel dentro do prompt.
- **Autofill do Canva não está disponível** — zero brand templates com dataset, e a tool
  `autofill-design` não existe no MCP. O caminho é `copy-design` → `read-design(open_
  transaction)` → `edit-design(update_fill + replace_text)` → `commit` → `export-design`.
  `commit` é irreversível; `cancel` é grátis.
- `upload-asset-from-url` do Canva só aceita **URL HTTPS já pública** → buckets públicos
  (`social`, `produtos`, `app`, `catalogos`). Nunca pastebin/Imgur/WeTransfer.
- **Dois QA, e o segundo é o que importa.** `social-qa` olha a imagem crua (produto na cena,
  texto, pessoa). O `revisor-social` olha a **arte montada** pelo thumbnail — texto estourando
  box e logo tampado só existem depois da montagem.
- Teto de **2 regerações**; na terceira o post vira `parado_revisao_humana`. Falha de
  **upload** não consome tentativa (a imagem já foi paga); só recusa da OpenAI consome.
- **Gate de coerência: `promessa_visual`.** O QA comparava imagem × prompt, e quem escrevia o
  prompt escrevia a copy — briefing incoerente passava no próprio teste. O post 2 saiu com
  copy de "canto não resolvido" sobre cena de quarto arrumado, sem os produtos citados, e os
  **dois QA aprovaram**. Agora o `redator-legenda` escreve `promessa_visual` a partir da copy,
  o `social-qa` avalia contra ela (item 8, bloqueante) e o banco recusa `briefing_pronto` sem
  ela. Duas falhas caçadas: copy de problema com cena de solução, e copy que nomeia objeto
  ausente da foto.
- **A promessa escolhe o modelo, o modelo restringe a copy.** `aceita_produto_na_copy = false`
  no Modelo 04 (sem slot de produto): trigger recusa post com `codprod`/`referencia` nele.
- **Trava de concorrência é obrigatória em passo pago.** O cron de 5 min e uma chamada
  manual pegaram o mesmo post e o QA rodou duas vezes; na geração seria pagar duas vezes.
  A trava é `UPDATE ... WHERE status='briefing_pronto'` → `gerando_imagem`, tomada depois
  das validações de graça e antes da primeira chamada paga, com resgate de órfão em 10 min.
- **Nome de arquivo único por geração.** `x-upsert` troca os bytes mas o CDN serve a versão
  antiga pela mesma URL — o QA avaliou a imagem velha e reprovou uma cena correta. O nome
  leva `Date.now()`; para revalidar uma URL já servida, use `?v=<epoch>`.
- **Storage deste projeto exige o header `apikey`**, não só `Authorization: Bearer` — senão
  403 `Invalid Compact JWS`. O PostgREST aceita só o Bearer, o Storage não. Verificado.
- **Os 5 modelos estão em `social_modelo`** (`mapa` = papel → `locator_id`, verificados como
  estáveis entre cópias). Em **3 dos 5 o GPT não entra**: Modelos 01, 02 e 03 são cor plana
  com slot de foto real, e a `social-imagem` os promove sem custo. GPT só no 04 (lifestyle,
  o único que aceita pessoa) e no 05 (4 ambientes).
- **O bloqueio atual:** `produto_foto` são **JPG com fundo branco** e os modelos pedem **PNG
  recortado** — JPG no slot vira retângulo branco sobre o creme. Bloqueia justamente os três
  modelos que não gastam GPT. Saída preferida: bucket de recorte alimentado pelo marketing.
- **`titulo_max` tem que ser medido montando arte real.** No Modelo 01 são 24 caracteres:
  33 quebram em 3 linhas e colidem com o subtítulo. Estimar pela largura do box erra.
- **O slot `selo` do Modelo 01 é a régua de ícones** (freezer, micro-ondas, lava-louças,
  BPA FREE) — são quatro claims. Se o SKU não sustenta, apague o elemento.

Tabelas: `social_post` (estado) e `social_qa` (log de avaliação), RLS ligado e só SELECT.

Claim é gate, não detalhe: **"hermético" está bloqueado sem laudo** (CDC art. 36 obriga a
manter o dado técnico em poder do fornecedor). "Livre de BPA" e "atóxico" exigem
especificação de material. A Sanremo escreve *"válvula micro ondas"* justamente para evitar
o claim — copie a Sanremo.

---

## 8. Como o squad de produto trabalha

Os quatro agentes vivem em `.claude/agents/`. O Claude os detecta sozinho e chama por nome.
O guia de conexão, de como pedir e o teste de fumaça estão em **`SQUAD.md`**.

| Agente | Papel | MCPs que usa |
|---|---|---|
| `analista-sankhya` | dado interno: curva, margem, família, clientes por SKU | Sankhya |
| `radar-concorrencia` | dado externo: preço, marcas, avaliações (API do ML antes do Apify) | Supabase |
| `engenheiro-molde` | viabilidade: injetora, material, montagem, claim | Sankhya + Supabase |
| `curador-portfolio` | **o crítico, com veto** | Sankhya + Supabase |

Ordem padrão de uma decisão de lançamento:

```
analista-sankhya   → o dado interno (curva, margem, família, o que já existe)
        ↓
radar-concorrencia → o dado externo (preço, marcas, avaliações)
        ↓
engenheiro-molde   → é fabricável? em que máquina? qual material? o claim se sustenta?
        ↓
curador-portfolio  → o crítico. Já existe? É proliferação? Qual o payback? Vale?
        ↓
grava em pdp_lancamento (status = 'proposto')
```

**O `curador-portfolio` tem poder de veto** e deve ser chamado sempre antes de gravar
qualquer proposta. Com 0,7% de acerto na última safra, o viés padrão é **não lançar**.

Toda proposta gravada em `pdp_lancamento` precisa de `evidencia` preenchida com o dado
que a sustenta. Proposta sem evidência não entra.
