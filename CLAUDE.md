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

### Vedação, tampa de madeira e material do corpo (conferido em 31/08/2026)

Levantado a partir do conceito "Linha Quadra" (pote quadrado, corpo transparente, tampa de teca,
anel de vedação). Nota técnica em `analise/06-quadra-material-montagem.html`.

- **Não existe uma única vedação de elastômero em estrutura de produto.** Todos os o-rings do ERP
  (`ANEL ORING ... NBR 70SH/90SH`, cordão NBR/silicone Ø 1,5 a 4,0 mm, anéis de molde Ø 12,7 a 22)
  estão no grupo **6000000 = manutenção** — ferramentaria e hidráulica, não grau alimentício, sem
  BOM. Os itens "ANEL" em PI (`205-A`, `122-A`, `546-A`) são **anéis injetados**, não vedações.
  Anel de silicone = fornecedor novo + laudo de contato + inspeção + PI + posto de montagem.
- **A casa já veda sem borracha:** `POTE VEDA MAIS` (083/086/087/089, 700 ml a 4,5 L, R$ 50,8 k/12 M)
  e a família de travas fazem vedação com geometria de PP.
- **Cadastro tem zero Tritan, PETG e copoliéster** (produto e MP). `PP H 105` (CODPROD 991) é
  homopolímero **com clarificante** — é dele que sai o quadrado transparente atual. `PS CRISTAL`
  (CODPROD 8788) custa **R$ 11,31/kg** em `TGFCUS` e é frágil/trinca sob gordura. O `TPE 997`
  segue **sem registro de custo** — nunca comprado.
- **A cota de vedação não pode morar na madeira.** Contração tangencial da teca ~5,3% sobre ~30
  pontos de umidade = **0,18% por ponto**. Numa tampa de 116 mm, oscilação de 3 a 5 pontos move
  **0,31 a 1,04 mm** — de 3 a 10× a faixa útil de aperto de um anel (0,4 a 0,6 mm, a manter em
  ±0,1 mm). Uma cota injetada em PP fica em ±0,05 mm. Tampa **quadrada** ainda sai de esquadro,
  porque se move diferente em cada eixo. Corolário: vedação vai em peça injetada; teca vira capa.
- **Vedação radial não serve a seção quadrada.** No redondo a parede responde em tração de aro e
  fecha; na face de 112 mm o meio cede. Em quadrado a vedação vai **na face**, e face exige força
  de fechamento — ou seja, **trava**. O corpo `3770` já tem trava.
- **Montagem madeira-em-plástico já é rotina:** 7 tampas de madeira cadastradas como PI
  (`501-TM`, `502-TM`, `503-TM`, `552-TM`, `268-TM`, `269-TM`, `270-TM`, com versões FSC).
  Fixação correta é parafuso central justo + laterais em rasgo; **não colar a face inteira**
  (placa de 116 mm colada em PP rígido empena). Bitolas compradas: 12, 15 e 18 mm — especificar 16
  obriga a desengrossar. Densidade da teca ~0,65 g/cm³: capa de 116×116×15 mm pesa **~131 g**,
  não 195 g.
- **O quadrado já existe em 4 litragens** (12 M, marca própria): `3770.012.001` 1,8 L R$ 263.619 /
  729 clientes · `240.024.001` **quadrado com válvula 3 L** R$ 190.421 / 283 · `3760.012.001` 3,7 L
  R$ 179.535 / 413 · `3780.012.001` 860 ml R$ 157.420 / 809 · `3790.012.001` 360 ml R$ 74.665 / 697.
  Conceito de "3 alturas novas" é molde novo para geometria que já vende — a rota barata é lançar
  **só a tampa** sobre o 1,8 L.

### Tritan e o teto de preço (conferido em 31/08/2026)

- **A injetora aceita copoliéster; a fábrica não está pronta.** Rosca de PP serve (uso geral, L/D
  20:1). O que falta: **secador dessecante** (<200 ppm, 66–71 °C, orvalho −29 °C) — não existe no
  cadastro, e não se compra nenhum consumível de secador; massa a 260–290 °C **a confirmar com a
  manutenção** (`VW_MAQUINA_CAPACIDADE` só tem tonelagem e ciclo, sem campo de temperatura);
  molde cortado para 0,2–0,5% de contração (ferramenta de PP entrega peça ~1,3 mm maior em
  112 mm); saída de 1,5–2° (a ficha pedia 1°); injetada em 30–70% do canhão; refugo segregado.
- **A escada de preço é o que trava, não a máquina.** `3770.012.001` sai a **R$ 4,92** com custo
  **R$ 2,77** e MB 43,7% — quase todo custo é resina (~198 g de PP a ~R$ 9,95/kg com moído).
  Em copoliéster a peça pesa ~258 g, a resina é importada e o refugo não volta: custo de
  **R$ 10 a 16** entre R$ 35 e 60/kg, preço de R$ 17 a 29 para manter a margem = **+250% a +490%**.
  Rota tampa de teca (corpo em PP) exige **+91% a +146%**.
- **Prêmio que o mercado paga (1.001 ofertas no `pdp_ml_oferta`, potes de 200 a 5.000 ml):**
  plástico **R$ 23,00/L** · vidro **R$ 26,47/L** (+15%) · vidro + tampa de madeira/bambu
  **R$ 36,33/L** (+58%, **n=4** — teto indicativo). Nenhuma rota cabe no prêmio disponível.
- **Espaço vazio confirmado, mas com ressalva:** **Tritan = 0 de 1.001** anúncios. Pote de
  alimento em plástico com tampa de madeira = **0** (os 51 anúncios com madeira/bambu são cesto de
  roupa, caixa organizadora, porta-talher e gaveteiro). Só que a Nitron está do lado de quem
  **já tentou e não vendeu** — ver abaixo. Espaço vazio ≠ demanda.
- **Tritan é argumento de garantia, não de vitrine.** O consumidor não distingue copoliéster de
  PP clarificado na foto. A vantagem (não embaça na lava-louças, não trinca, sem BPA) só se paga
  em canal que vende durabilidade, não em marketplace de preço por peça.

### O experimento controlado da Caixa Flat 10,35 L (mesmo corpo, só a tampa muda)

| Versão | Preço/un | Custo/un | MB | Unidades 12 M | Clientes |
|---|---|---|---|---|---|
| `503.006.001` tampa plástica transparente | 12,04 | 5,53 | 54,1% | 14.399 | 305 |
| `503.006.003` tampa plástica preta | 15,75 | 5,39 | 65,8% | 10.202 | 220 |
| `503.006.002` tampa plástica branca | 15,58 | 5,39 | 65,4% | 9.606 | 156 |
| `503.006.086` tampa plástica chumbo | 14,23 | 5,39 | 62,1% | 4.872 | 110 |
| `503.006.M03` **tampa de teca** preta | 34,44 | 16,96 | 50,8% | **318** | 48 |
| `503.006.M02` **tampa de teca** branca | 33,10 | 16,96 | 48,8% | **264** | 39 |

Tampa de teca: preço **+119%**, custo **+215%**, MB **−15 pontos**, unidades **÷32**.
Corrige a leitura anterior de que teca dilui margem por natureza — **esta** teca dá 50,8% de MB,
acima da média de 36,8% da linha. O que ela não sustenta é volume. **Por que só 318 unidades é
pergunta aberta e vale mais que qualquer decisão de resina** — é a mesma que a Quadra enfrentaria.

Preço médio e MB (12 M, marca própria) dos quadrados: `3780` 860 ml R$ 3,88 / MB 53,9% ·
`3770` 1,8 L R$ 4,92 / 43,7% · `240` válvula 3 L R$ 6,31 / 43,0% · `3760` 3,7 L R$ 7,06 / 46,0%.

⚠️ `pdp_ml_oferta` tem **1.001 ofertas** agora, não 267.

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


### A lição de 2022 — por que cor não é lançamento

Em 2022 a empresa optou por **criar cores em vez de moldes**. O resultado foi
**saldo e ruptura ao mesmo tempo**, e a produção dobrou/triplicou em bateladas.
Hoje o portfólio foi enxugado e as cores vão pela linha **Coloratto**.

Não foi azar, foi aritmética. Estoque de segurança é proporcional ao **desvio**, não à
demanda. Partindo a mesma demanda em N cores:

- demanda por SKU cai para **1/N**
- desvio por SKU cai só para **1/√N**
- estoque de segurança **total** sobe para **√N**

Uma cor vira três → **+73% de estoque de segurança para vender o mesmo tanto**. E cada
cor fica com cobertura mais fina que o produto único tinha, então **a ruptura sobe junto**.
Saldo e ruptura simultâneos não são contradição — são o resultado previsto.

Somado: troca de cor na injetora exige **purga** (material perdido + hora-máquina).
Triplicar cores triplica bateladas, consumindo capacidade sem produzir peça a mais.

**Regra: cor divide demanda existente; produto novo cria demanda. Os dois somam SKU, só um
paga o SKU que somou.** Cor nova só via Coloratto.

### A janela de litragem — a regra de lançamento mais forte do projeto

Testada em **79 referências** de pote (nascidas antes de 2024, vendendo nas duas janelas,
≥50 clientes):

| Faixa | Refs | Δ 12 M | Subiram |
|---|---|---|---|
| até 600 ml | 22 | **−31,5%** | **2 de 22** |
| 601 ml – 1 L | 16 | +2,9% | 5 de 16 |
| **1,1 – 2 L** | 21 | **+28,9%** | 12 de 21 |
| **2,1 – 3,5 L** | 11 | **+56,5%** | 7 de 11 |
| acima de 3,5 L | 9 | −0,7% | 5 de 9 |

**88 pontos de amplitude**, contra 12 pontos da hipótese Alto/Raso (que não sobrevive a
teste controlado: na família redonda Alto +20,7% e Raso +20,6%). O mesmo padrão reaparece
em 5 famílias independentes (trava, válvula, quadrado, rosca, modular) e também em
micro-ondas (2,6 L +65%, 850 ml −48%).
**Nada novo abaixo de 1 L.**

### Materiais — o que a fábrica realmente roda

Compras de resina, 12 M até 24/08/2026: **≈ 2.605 t, 98,4% PP**, 1,6% poliestireno
(PSAI + PS cristal 8 t), **PEHD 1.125 kg** (amostra, não abastecimento).
**Zero PET, zero Tritan, zero copoliéster, zero silicone como MP.** O único elastômero
cadastrado é **CODPROD 997, TPE Karinprene shore 45 — sem histórico de compra**.

- **Silicone (LSR): não roda.** Exige canal frio, molde aquecido 150–200 °C, bomba
  bicomponente A+B e vácuo. É conversão de máquina.
- **PET: inviável para pote.** Higroscópico (secagem a <50 ppm, equipamento que não existe)
  e **cristaliza em parede grossa** — sai leitoso, matando a transparência que motiva a escolha.
- **Tritan (copoliéster Eastman): roda em prensa convencional**, mas exige secador, **molde
  cortado para a resina** (contrai 0,2–0,5% contra 1,2–2% do PP), resina de fonte única e
  custo em outro patamar.
- **PP H 105 é "homopolímero com clarificante"** e é o item mais comprado da casa (896 t/ano).
  Antes de qualificar resina nova, esgotar ele.

⚠️ **O ciclo de moído vale ~R$ 2,63 M/ano.** 537 t (20,6% do volume) entram a R$ 6,07/kg
contra R$ 10,96 do virgem clarificado. Esse ciclo **só funciona porque o refugo é
mono-resina** — refugo de Tritan misturado com PP não vale nada, e vice-versa. Material novo
não adiciona custo de resina: **contamina um ativo de R$ 2,6 M/ano** que nenhum business
case de lançamento contabiliza.

### Mais lições de método

6. **Cor que vende por função não vira paleta.** Em Organização, laranja marca
   **R$ 211 k por SKU** (1,5× o preto) — mas é **um produto**: `170.006.028` Caixa de
   Ferramentas Nitronfort Laranja 16 L, R$ 421.810 e 500 clientes. É sinalização de
   ferramenta, não paleta. Não generaliza para organizador doméstico.
7. **Peça removível não carrega função de segurança.** Se o produto só é seguro com um
   componente dentro (base de silicone, disco), a segurança fica na memória do consumidor.
   Proteção essencial vai **na geometria do molde**.
8. **Tampa de madeira em corpo plástico: testado, falhou.** Mesmo corpo 10,35 L —
   tampa plástica em 4 cores fez **R$ 492.548** (309/223/158/111 clientes); **tampa teca**
   em 2 cores fez **R$ 16.192** com **57 e 40 clientes**, caindo 52% e 38%. 30× de diferença.
9. **Separe rampa de lançamento de curva orgânica.** `817/818/819` (Pote Alto com Válvula)
   nasceram em 2024-09 e 2025-02 — o "+1.272%" era base parcial. A plataforma válvula
   cresce **+49,9%** orgânico, não +95,6%. E `MIN(DTNEG)` por referência **conflita
   lançamento com re-cadastro** (as datas se agrupam em 2020-03, 2022-02, 2023-02, 2024-08,
   2025-02, 2026-02) — não leia cohort sem confirmar.
10. **Sete ideias "novas" já existiam no catálogo.** Caixa Organizadora Rattan chumbo ·
   Lixeira Basculante Rattan chumbo · trava+válvula (`176.024.001`, `210.024.001`) ·
   Caixa Flat com Tampa Teca · Balde Pipoca (`342.006.597`, <R$ 5 k/ano) · Kit Geladeira
   (4 refs) · Kit de potes com válvula (`241.006.P01`, R$ 2.919 e 13 clientes, em 460 ml).
   Nenhuma foi mal concebida — foram **executadas na litragem errada ou abandonadas**.
   A busca no `TGFPRO` com 3 palavras diferentes é obrigatória antes de propor.

### Achados abertos (valem mais que a maioria dos lançamentos)

- **Branco em Organização cai 17,0%** — R$ 5,95 M → R$ 4,94 M, ~R$ 1 M/ano. Causa não
  investigada: preço, ruptura, cliente grande ou migração para preto?
- **Café 2 L (`363.012.003`)** custa R$ 3,69 contra R$ 2,55 dos irmãos de mesma litragem —
  MB 25,9% contra 48–50%. **R$ 56.577/ano** de margem.
- **`176` e `210`** (válvula+trava) caem 56% e 49% — as duas **únicas** quedas numa
  plataforma que cresce 49,9%. Decide o Chrono e a rota barata do quadrado+válvula.
- **Kit modular `353.006.001`** caiu 83% (R$ 2,59 M → R$ 436 k) com os clientes
  **subindo** de 127 para 179 e o ticket caindo 88%. Queda difusa, não perda de contrato.
- **`TGFEST` não é legível sem mapa de local** — 120 combinações empresa/local para 3
  produtos, com o local 1080000 em negativo grande. Falta saber qual `CODLOCAL` é o
  armazém de PA para medir saldo e ruptura.
- **Perguntas para a fábrica:** os moldes de tampa aceitam inserto trocável? Os potes
  quadrados atuais são altos ou rasos?

---

## 7. Como o squad trabalha

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
