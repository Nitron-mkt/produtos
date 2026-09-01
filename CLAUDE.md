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

### Família liso — decisão de 31/08/2026 e o suprimento do anel

Direção definida pelo usuário: **família nova, molde novo**. Os corpos atuais têm abas e ondulações
de pegada e reaproveitá-los entrega produto com cara de adaptado. Brief em
`analise/07-familia-liso-brief.html`.

- **Geometria:** corpo cilíndrico liso, **Ø 140 mm externo** fixo, quatro alturas —
  **1,2 L (91 mm) · 1,8 L (132) · 2,6 L (187) · 3,5 L (249)** — cobrindo só as faixas que crescem
  (1,1–2 L +28,9% e 2,1–3,5 L +56,5%), nada abaixo de 1 L. Uma tampa serve as quatro.
- **Cilindro resolve o que o quadrado travava:** parede redonda responde em tração de aro, então
  vedação volta a ser problema com solução conhecida.
- **Pé de diâmetro constante (134 mm) em todas as alturas.** Com saída de 0,5° a base do 3,5 L sai
  4,3 mm mais estreita que a boca, e um rebaixo único de tampa não assentaria nos quatro. O pé
  constante, formado no fundo da cavidade, dá registro de empilhamento igual para todos.
- **Vedação: canal entre dois frisos, não sulco de anel radial.** Sulco radial exigiria saia de
  4,5 mm (rechupe). Canal de **3,8 mm** entre frisos de **2,4 mm**, cordão **Ø 3,0 shore A 60**;
  o anel sobra 0,6 mm além do friso, então o fechamento esmaga **20%** e **o friso vira batente** —
  impede sobrecompressão, que é a causa nº 1 de vedação que morre em 6 meses. Anel entra com
  circunferência interna 2–3% menor (tração, sem garra: tem que sair para lavar).
- **Força de fechamento:** baioneta de ¼ de volta (recomendada) · encaixe por pressão (mais barato,
  força varia com o lote) · rosca de 140 mm (molde mais caro: desrosqueamento ou macho colapsável).
- ⚠️ **Correção: TPE injeta em máquina convencional** (170–230 °C), silicone não. `CODPROD 997`
  (TPE Karinprene shore 45) está cadastrado e nunca foi comprado — há rota interna real. O número
  que decide é **compression set**: silicone recupera, TPE-S tende a deformação permanente e o pote
  fica fechado por meses. Exigir o ensaio antes de desenhar molde de anel.
- **Suprimento do anel, 3 rotas:** (1) tryout com cordão emendado — ferramenta zero, a manutenção
  já compra cordão Ø 1,5 a 4,0 mm; (2) produção em anel moldado por compressão em VMQ; (3) anel
  injetado em TPE no próprio parque. Sobreinjeção 2K exige injetora bi-material — não existe.
- ⚠️ **`RDC ANVISA nº 1.020, de 02/04/2026`** (vigor desde 07/04) trata especificamente de
  **silicones em contato com alimentos** e revogou as seções de elastômero de silicone da
  RDC 123/2001. Limites: matéria orgânica volátil ≤0,5%, extraíveis ≤0,5%, **peróxidos negativo**,
  aminas aromáticas primárias <0,01 mg/kg. Por isso especificar **cura por adição (platina)**, não
  por peróxido. Fornecedor que cota laudo só contra a 123/2001 está cotando contra regra superada.
- **Fornecedores de vedação já no cadastro** (compra ativa, sem onboarding): **ECOBOR BORRACHAS**
  (07.265.660/0001-43, maior volume, 21/07/2026) · **VF VEDAÇÃO E FIXAÇÃO** (19/08/2026) ·
  **VEDALL** (28/07/2026) · QUALIVED · ALLVED · VEDABRAS. São distribuidores de vedação industrial:
  porta de entrada, não necessariamente fornecedor final.
- **Parque (`VW_MAQUINA_CAPACIDADE`, centro NITRON):** 60 t ×2 · 80 ×3 · 120 ×8 · 130 ×4 · 150 ×2 ·
  160 ×12 · 200 ×13 · 210 ×1 · 250 ×10 · 280 ×1 · 300 ×1 · 380 ×3 · 398 ×1 · 600 ×2 · 650 ×2 ·
  1.100 ×1. Área projetada de 154 cm² pede 80–120 t — sobra. **O que decide é o curso de abertura,
  não a tonelagem:** 249 mm de profundidade pede ~550 mm de abertura, e o ERP não guarda curso.
  Pergunta aberta para a manutenção.

### A resina do premium: SAN, não Tritan (31/08/2026)

Modelo 3D em `analise/08-linha-coluna-3d.html` (nome de trabalho **Linha Coluna**).

| Resina | Clareza | Impacto | Lava-louças | Secagem | Custo vs PP |
|---|---|---|---|---|---|
| PP H 105 clarificado | alta, com névoa (20–30%) | excelente | ok | não precisa | 1× |
| **SAN** | vidro (névoa 2–3%) | **frágil** | limítrofe | leve, 80 °C ar quente | ~2–3× |
| PETG | vidro | bom | **não** — amolece ~70 °C | dessecante | ~2–3× |
| PMMA | vidro+ | frágil | não — trinca com detergente | leve | ~3–4× |
| Tritan | vidro | bom | sim | dessecante rígida | ~5–8× |

**A tampa de teca já obriga lavagem à mão** — com isso a única fraqueza séria do SAN contra o
Tritan deixa de valer para este produto. Sobra a clareza, que é o que o cliente vê, e a rigidez,
que lê como premium. O projeto compensa a fragilidade com parede de 2,5 mm, raios generosos, zero
canto vivo interno e ponto de injeção central no fundo (linha de solda na parede vira trinca em
material frágil). Refugo de SAN moído e ensacado separado do PP.

**Exceção dentro da peça:** a **tampa interna sai em PP**, não em SAN — carrega as rampas da
baioneta, que querem tenacidade, e fica escondida sob a capa de teca.

### Geometria congelada da Linha Coluna

- Ø 140 externo · parede 2,5 · saída 0,5°/lado · pé Ø 134 **constante** nas quatro alturas.
- 1,2 L (h 91) · 1,8 L (h 132) · 2,6 L (h 187) · 3,5 L (h 249). Uma tampa serve as quatro.
- **A saia da tampa passa por fora do bocal** → tampa Ø 145 contra corpo Ø 140. Não é descuido:
  rebaixo no bocal seria contra-saída para o macho e obrigaria gaveta. Os 2,5 mm de aba por lado
  ainda protegem o anel.
- **A saia faz de friso externo** — economiza uma parede. Canal 3,8 entre a saia e o friso interno
  de 2,4; cordão Ø 3,0 shore A 60; esmagamento 0,6 = 20%, com o friso de batente.
- Fecho: baioneta de ¼ de volta, 3 orelhas no bocal. ⚠️ Orelha rasa sai por arranque em PP; em SAN,
  que é rígido, provavelmente **não** — e as orelhas estão no corpo, então é o molde do corpo que
  paga gaveta. Pergunta aberta para a ferramentaria.
- Pendências que o 3D não decide: cotação do SAN posto (acima de 4× o PP, reabrir o PP clarificado);
  **ensaio de queda com o pote cheio** (é o que o SAN pode reprovar — se reprovar, parede vai a
  3,0 mm antes de trocar de resina); compression set do TPE; curso de abertura para o 3,5 L.

### Emenda de anel: a rota do cordão (01/09/2026)

Procedimento em `analise/09-emenda-do-anel.html`.

- ⚠️ **A família já tem molde único de anel.** Uma tampa para as quatro alturas = **um** diâmetro
  (137,4 mm médio). Não há família de tamanhos para diluir ferramenta — a ideia de "um molde e
  depois eu junto" resolve um problema que este projeto foi desenhado para não ter.
- ⚠️ **Cordão não se injeta, se extruda.** Tira injetada sai com **linha de partição no sentido do
  comprimento** — numa vedação isso é caminho de vazamento de ponta a ponta. E não há linha de
  perfil na casa: os itens `PP - EXTRUSAO + LAVAGEM` e `PP - SEPARAÇÃO + MOAGEM + EXTRUSÃO` são
  **serviço de recuperação de PP** (MP comprada), não extrusora.
- **Parque por centro de trabalho (`VW_MAQUINA_CAPACIDADE`):** NITRON 62 (injetora + montagem) ·
  **WOOD 14** · Tanamu 10 · HYAK 2 · Nitron-MG 1.
- **A marcenaria já emenda topo a topo:** o centro WOOD tem `LINHA SEMI-AUTOMATICA DE FINGER JOINT`
  e `PRENSA SEMI-AUTOMATICA FINGER JOINT`, além de prensa de alta frequência e coladeira de
  cilindro. É a mesma discussão (emenda × peça inteira) em outro material — boa analogia com a
  fábrica.
- **Dispositivo de solda dá para construir na casa:** duas castanhas de alumínio com meia-cana
  Ø 3,0 (uma no carro, com batente) + lâmina de alumínio revestida de PTFE. A **resistência
  cartucho** (estoque em 6 · 7,8 · 9,3 · 9,7 · 9,8 · 10 · 11,8 · 16 mm), o **termopar tipo J** e o
  `CONTROLADOR DE TEMPERATURA DO MOLDE` **já estão no cadastro**. Só a chapa revestida é compra.
- **Procedimento (TPE-S):** corte **422 mm** (circunferência livre 431,6 − 2,5% de tração + ~1 mm
  que a solda consome), sobra de **1,2 mm por lado**, lâmina a **190–210 °C** por 5–10 s,
  **retirar a lâmina em menos de 2 s**, recalcar até o batente e segurar 20–30 s. Rebarbar rente —
  ressalto na face de vedação é vazamento. Silicone usa o mesmo dispositivo, mas **vulcaniza**
  (filme de RTV de adição, castanhas aquecidas a 150–180 °C por 3–5 min), não solda.
- **O que mata a emenda na produção é o relógio, não a resistência:** 60 a 120 s por anel →
  **833 a 1.667 h/ano** a 50 mil anéis. Não escala. Equilíbrio =
  `custo do molde ÷ (mão de obra por anel − preço do anel moldado)`.
- **Molde de compressão de borracha é placa usinada com sulcos:** um segundo diâmetro depois é
  *mais um sulco*, não ferramenta nova. A intuição de "um molde que serve para vários" se realiza
  melhor na compressão do que na emenda.
- Ensaio obrigatório da junta: esticar 25% e soltar, **50 ciclos** — o cliente estica o anel para
  lavar, e é ali que a emenda rompe. Adesivo na junta não é rota aceitável para contato alimentar.

### TPE atóxico: depende do grade, não do "TPE" (01/09/2026)

- **TPE é família e é composto, não polímero puro.** O provável aqui é TPE-S (SEBS), cuja base é
  inerte — mas o composto é SEBS + **óleo plastificante** + PP + cargas + aditivos. **O que migra é
  o óleo.** Exigir óleo mineral **branco, grau alimentício/USP**, sem ftalatos, e grade
  **natural sem pigmento** (pigmento muda o laudo). `CODPROD 997` diz "NATURAL", o que ajuda.
- **Enquadramento regulatório é uma bifurcação:** TPE não é vulcanizado, então o caminho usual é o
  de **plásticos** — `RDC 56/2012` (lista positiva de monômeros/polímeros) + `RDC 326/2019`
  (aditivos, alterada pela **`RDC 963/2025`**), com migração pela **`RDC 51/2010`** (global
  60 mg/kg ou 10 mg/dm²). Alguns fornecedores enquadram como elastômero (`RDC 123/2001`).
  **Exigir que o laudo declare o enquadramento e seja feito no composto acabado**, não na resina
  base. ⚠️ A `RDC 1.020/2026` é de **silicones** — não cobre TPE.
- **Risco prático deste produto, além do legal:** óleo migra para **gordura** (café, castanha,
  granola) e TPE pode transferir **odor e sabor**. Café absorve cheiro de qualquer coisa. Somar
  **ensaio sensorial/organoléptico** à lista — é barato e pega o que a migração não pega.
- **Estar cadastrado não é laudo.** `CODPROD 997` nunca foi comprado e não há laudo no sistema. A
  maioria dos fabricantes de TPE tem linha industrial e linha food/medical separadas, com preços
  diferentes — perguntar pelo grade alimentício explicitamente.
- **Comparação para a decisão:** silicone curado por adição é o default de menor risco (sem óleo
  extraível, praticamente inerte, melhor compression set); TPE é a opção barata e injetável na casa
  e exige especificação mais apertada. As duas são legítimas com o grade certo.

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
