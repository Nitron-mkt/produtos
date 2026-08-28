# Squad de Social Media — fluxo Claude → OpenAI → Canva

Cinco agentes em `.claude/agents/`, duas tabelas de estado no Supabase e duas Edge Functions.

| Agente | Papel | Entra quando o status é |
|---|---|---|
| `estrategista-conteudo` | pauta com evidência no dado | *(início)* |
| `redator-legenda` | legenda + gate de claim (CDC) | `planejado` |
| `diretor-arte` | prompt do GPT + foto real + template | `copy_pronta` |
| `montador-canva` | executa a montagem no Canva | `imagem_aprovada` |
| `revisor-social` | **o crítico, com veto** | `arte_montada` |

---

## 1. A divisão de camadas — a decisão central

```
camada 3 — MARCA    → Canva   (logo, fonte, cor, selo)
camada 2 — PRODUTO  → foto real de produto_foto.link_principal  (749 SKUs disponíveis)
camada 1 — CENÁRIO  → imagem gerada pelo GPT
```

**O GPT nunca gera o produto.** Ele gera cenário, luz e ambiente — que é exatamente o que o
Canva faz mal. O Canva aplica a identidade da marca com precisão — que é exatamente o que o
GPT faz mal. Cada um no que é bom.

Se o GPT desenhar o produto, sai um pote que não existe: tampa errada, proporção errada, cor
que a fábrica não produz. Além de ficar ruim, é publicidade enganosa (CDC art. 37).

---

## 2. Por que não tem n8n aqui

Decidido em 28/08/2026. O n8n não existia ainda neste stack, e três fatos derrubaram a
necessidade dele:

**O n8n não chamaria o Claude Code.** Claude Code não tem endpoint de entrada. Um agente
`.md` só roda quando alguém abre uma sessão. Um fluxo que "volta pro Claude" no meio **para
e espera um humano** — não é automação.

**O n8n não chamaria o MCP do Canva.** Mesmo motivo. Para o n8n mexer no Canva seria preciso
a Canva Connect API com app OAuth próprio.

**O projeto já é um orquestrador.** ~70 jobs em `pg_cron` disparando 54 Edge Functions, com
fila (`fila-processar`, de minuto em minuto), trava e config em tabela. Instalar n8n seria um
**segundo agendador** — duas fontes de verdade sobre quem disparou o quê.

Então os dois passos automáticos viraram Edge Function, no padrão que o projeto já usa.
Se um dia o n8n entrar, ele entra pelo mesmo contrato REST da §4 — nada aqui precisa mudar.

---

## 3. O fluxo

```
┌─ CLAUDE (sessão interativa) ─────────────────────────────────────────┐
│ estrategista-conteudo  → planejado                                   │
│ redator-legenda        → copy_pronta        (claim_check preenchido)  │
│ diretor-arte           → briefing_pronto                             │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─ EDGE FUNCTION social-imagem  (cron */5) ────────────────────────────┐
│ gpt-image-1 gera o cenário → PNG no bucket público social/           │
│                        → imagem_hospedada                            │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─ EDGE FUNCTION social-qa  (cron 2-59/5) ─────────────────────────────┐
│ claude-sonnet-5 com visão avalia o cenário cru                       │
│   aprovou  → imagem_aprovada                                         │
│   reprovou → briefing_pronto (regera)  ·  máx 2 → parado_revisao_...  │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─ CLAUDE (sessão interativa) ─────────────────────────────────────────┐
│ montador-canva  → arte_montada                                       │
│ revisor-social  → aprovado_maquina  |  *_reprovado                   │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
                        humano aprova → publicado
```

O estado vive **todo no Supabase**. Cada passo é idempotente: se a função cair no meio,
ninguém perde o briefing e o próximo tick pega de onde parou.

### Os dois QA são diferentes, e o segundo é o que importa

| | `social-qa` (automático) | `revisor-social` (sessão) |
|---|---|---|
| Olha | a imagem **crua** do GPT | a arte **montada**, pelo thumbnail do Canva |
| Pega | produto na cena, texto, pessoa, área sem espaço livre | texto estourando box, logo tampado, contraste, brand kit errado |
| Custa | centavos | uma passada de agente |

Verificar só a imagem crua deixa passar o erro mais comum em social — legenda estourando o
box só existe **depois** da montagem.

---

## 4. Contrato REST (vale para a Edge Function e para qualquer n8n futuro)

### Ler a fila

```http
GET {SUPABASE_URL}/rest/v1/social_post
    ?status=eq.briefing_pronto
    &tentativas_imagem=lt.2
    &prompt_imagem=not.is.null
    &select=id,marca,canal,formato,modelo,prompts_cenario,fotos_produto,referencia,social_modelo(slots_cenario,permite_pessoa)
    &order=data_prevista.asc.nullslast
    &limit=3
```

### Devolver o resultado

```http
PATCH {SUPABASE_URL}/rest/v1/social_post?id=eq.123
{ "imagem_gpt_url": "…/storage/v1/object/public/social/123-v1.png",
  "status": "imagem_hospedada" }
```

### Estados

`planejado` → `copy_pronta` → `briefing_pronto` → `imagem_hospedada` →
`imagem_aprovada` → `arte_montada` → `aprovado_maquina` → `publicado`

Desvios: `briefing_reprovado`, `copy_reprovada`, `arte_reprovada`, `imagem_reprovada`,
`parado_revisao_humana`, `descartado`. A constraint `social_post_status_ck` recusa qualquer
outro valor — se um status novo for preciso, altere a constraint, não contorne com texto livre.

### Chaves — onde cada uma mora

| Chave | Onde | Regra |
|---|---|---|
| `SUPABASE_SERVICE_ROLE_KEY` | injetada no runtime da Edge Function | dá escrita em tudo. Nunca em front-end, nunca em log. |
| `OPENAI_API_KEY` | secret do projeto Supabase | usada só por `social-imagem` |
| `ANTHROPIC_API_KEY` | secret do projeto Supabase | usada só por `social-qa` |
| chave `anon` | front-end apenas | ⚠️ **89 tabelas deste projeto estão com RLS desligado**, incluindo `contato_enriquecido` (21 k) e `ghl_cliente` (10 k). A `anon` dá **leitura e escrita** nelas. |

`social_post` e `social_qa` nascem com RLS **ligado** e só política de SELECT, igual às `pdp_*`.

### Bucket

`social` — **público**, 10 MB, só `image/png|jpeg|webp`. Criado em 28/08/2026.
Nome do arquivo: `{social_post.id}-v{tentativa}.png`.

O `upload-asset-from-url` do Canva só aceita **URL HTTPS já pública** — por isso o bucket é
público. **Nunca** use pastebin, Imgur ou WeTransfer para conseguir uma URL: material de
marca não vai para hospedagem de terceiro.

---

## 5. O que está montado e o que falta

| Item | Estado |
|---|---|
| 5 agentes `.md` | ✅ em `.claude/agents/` |
| `social_post` + `social_qa`, RLS ligado | ✅ aplicado em `bwbeieumxcuomtrvlqxs` |
| bucket público `social` | ✅ criado |
| Edge Function `social-imagem` | ✅ deployada, v1, ACTIVE |
| Edge Function `social-qa` | ✅ deployada, v1, ACTIVE |
| secrets `OPENAI_API_KEY` e `ANTHROPIC_API_KEY` | ✅ já existiam no projeto — as duas funções responderam 200 no teste, e o guard no topo devolveria 500 se faltassem |
| jobs `social-imagem-5min` (*/5) e `social-qa-5min` (2-59/5) | ✅ ativos |
| 5 modelos do Canva mapeados em `social_modelo` | ✅ Modelo 01 a 05, com mapa de `locator_id` por papel (§6) |
| primeiro post real na fila | ✅ `social_post` id 1 — Frasqueira Cristal 1,5L, Modelo 01 |
| caminho de custo zero (`slots_cenario = 0`) | ✅ o cron levou o post de `briefing_pronto` a `imagem_aprovada` sem chamar a OpenAI |
| montagem no Canva de ponta a ponta | ⚠️ mecânica **funciona**; o QA reprovou por fundo branco da foto (§6). Transação cancelada, 3 reprovas em `social_qa`. |
| fotos de produto recortadas (PNG sem fundo) | ⬜ **o bloqueio atual** — ver §6 |

**Desligar sem apagar**, se precisar:
`update cron.job set active = false where jobname like 'social-%';`

Teste de fumaça (as duas devolveram 200 com fila vazia em 28/08/2026):
```
{"processados":0,"resultados":[]}
{"avaliados":0,"resultados":[]}
```

---

## 6. Os 5 modelos do Canva

Cadastrados em `social_modelo` em 28/08/2026, com o mapa de `locator_id` por papel.
Todos são **1080 × 1350 (4:5)** nativos, brand kit `NITRON`.

| Modelo | Template | Para que serve | Fotos de produto | Cenários GPT | Pessoa |
|---|---|---|---|---|---|
| **01** | `EAHTlFA83HE` | produto único em destaque — o default de SKU | 1 | **0** | não |
| **02** | `EAHTlKR9Mek` | família ou cor: 4 SKUs empilhados | 4 | **0** | não |
| **03** | `EAHTlO_M85U` | produto em uso / benefício funcional | 1 | **0** | não |
| **04** | `EAHTlIZUQbA` | institucional / lifestyle, foto circular | 0 | 1 | **sim** |
| **05** | `EAHTlG7KBaQ` | listicle: 4 cantos da casa com rótulo | 0 | 4 | não |

### O achado que mudou o pipeline

**Em 3 dos 5 modelos o GPT não entra.** Os Modelos 01, 02 e 03 são layouts de cor plana da
marca com slots de **foto real de produto** — não têm fundo fotográfico. A `social-imagem`
detecta `slots_cenario = 0` e promove o post direto para `imagem_aprovada`, **sem chamar a
OpenAI e sem custo nenhum**.

Isso não enfraquece a divisão de camadas da §1 — confirma. Onde a marca resolve o layout,
não há cenário para gerar. O GPT entra só no Modelo 04 (uma cena lifestyle, o único que
aceita pessoa) e no Modelo 05 (quatro ambientes).

### O autofill não existe — e não faz falta

Zero brand templates com dataset, e a tool `autofill-design` não existe no MCP. Mas os
`locator_id` **são estáveis entre cópias** (verificado: duas cópias do Modelo 01 devolveram
os mesmos ids), então o mapa fixo em `social_modelo.mapa` substitui o autofill com
vantagem — ele controla o que pode ser trocado, e o autofill não controlaria.

```
create-design-from-brand-template → upload-asset-from-url →
read-design(open_transaction) → edit-design(update_fill + replace_text) →
[conferir thumbnail] → commit → export-design
```

Papéis no `mapa`: `titulo`, `subtitulo`, `produto_1..4`, `cenario_1..4`, `rotulo_1..4`,
`selo`, `adorno_topo`, `adorno_base`, `logo`. **O `logo` está lá para ser conferido, nunca
substituído.**

### O bloqueio real: foto de catálogo é JPG com fundo branco

Descoberto montando o primeiro post de verdade (28/08/2026, `social_post` id 1).

Os templates foram desenhados com **PNG recortado** — o produto flutua sobre a cor plana da
marca, com sombra suave. As 749 fotos de `produto_foto` são **JPG de catálogo com fundo
branco**. Colocar uma delas no slot produz um **retângulo branco visível** sobre o creme
`#fff7ea` do Modelo 01. Mecanicamente funciona; visualmente é inaceitável.

JPG não tem canal alfa, então não há truque de composição no Canva que resolva. As saídas,
em ordem de preferência:

1. **Bucket de recorte.** Marketing sobe PNG com fundo transparente num bucket público
   (`produtos-recorte`), e o `diretor-arte` puxa de lá quando existe. Trabalho pontual por
   SKU, custo zero de recorrência, e o resultado é o melhor.
2. **Remoção de fundo por API** numa Edge Function entre `produto_foto` e o Canva. Automático,
   mas custa por imagem e erra em produto transparente — e Frasqueira Cristal é transparente,
   justamente o caso difícil.
3. **Trocar o fundo do slot**, não do produto: os cinco modelos têm `background.isMediaReplaceable
   = true`. Dá para pôr uma cena atrás e deixar a foto branca por cima — mas aí o post deixa
   de ser o layout que a squad aprovou.

Isso bloqueia justamente os Modelos 01, 02 e 03 — os três que não gastam GPT. O Modelo 04 e
o 05 não sofrem: os slots deles recebem cenário gerado, que já vem sem fundo branco.

### O tamanho da imagem vem do slot, não do canal

O slot do Modelo 04 é um **círculo de 741×741**. Gerar retrato 2:3 para ele perde as
laterais no recorte circular. Por isso `social_modelo.cenario_size` manda no tamanho pedido
ao `gpt-image-1`, e o canal virou só fallback: Modelo 04 → `1024x1024`, Modelo 05 →
`1024x1536` (slots de ~313×507).

### A negativa da função cobre utilidades, não móvel

A `social-imagem` acrescenta ao prompt uma negativa fixa contra "pote, vasilha, recipiente,
caixa ou embalagem" — que é o catálogo histórico da Nitron. Para a linha **Nitron-Mob**
(móveis) o produto é arara e prateleira, e nada disso está na negativa fixa.

Quem escreve o prompt tem que proibir o produto **daquela** linha explicitamente. No post
de setembro da Nitron-Mob o prompt lista: sem arara, sem cabideiro, sem prateleira, sem
estante, sem nicho, sem sapateira, sem armário aberto, sem cômoda, sem estrutura de tubos
ou módulos. Sem isso o GPT desenha o móvel — e o móvel desenhado não é o móvel vendido.

### Limite de caractere: meça na arte, não no schema

O `titulo_max` do Modelo 01 estava em 46 por estimativa. Na renderização real, **33
caracteres quebraram em 3 linhas** e colidiram com a caixa do subtítulo. O box de 455px a
73.9pt cabe **~12 caracteres por linha**. Corrigido para 24.

Todo `titulo_max` e `subtitulo_max` da tabela deve ser confirmado montando um post real. Não
confie na largura do box dividida pelo corpo da fonte.

### O slot `selo` do Modelo 01 é claim, não ornamento

O que eu havia mapeado como `selo` é a **régua de ícones**: freezer, micro-ondas,
lava-louças e **BPA FREE**. São quatro alegações sobre o produto.

Para uma Frasqueira de organização, micro-ondas é falso e BPA exige especificação de
material. Um post que herda a régua do template sem checar **publica claim que a Nitron pode
não sustentar** (CDC art. 36). O `montador-canva` apaga o elemento quando o SKU não sustenta
os quatro — e apagar é a escolha segura por default.

### Duas armadilhas registradas

**Modelo 05 — título bicolor.** Tem duas `textRegions` de cores diferentes (`"5 cantos"` em
`#f28a7e`, o resto em `#dfa3a5`). `replace_text` achata as duas numa cor. Use
`find_and_replace_text` por região. E o layout tem **4 fotos** apesar de o título dizer
"5 cantos".

**Limite de caracteres.** `titulo_max` e `subtitulo_max` vêm da largura do box medida no
template. Estourar não dá erro — dá texto cortado, que só aparece depois da montagem.

### Convenção de nome no Canva

`Marca · DD-MM · Formato · Linha · assunto`
(ex.: `Nitron · 28-09 · Estático · Infantil · copo livre de BPA`)

---

## 7. Custo e teto

- **Máximo 2 regerações por post.** Na terceira, `status = 'parado_revisao_humana'`.
  Loop automático de reprovação queima crédito sem convergir — e três reprovações no mesmo
  item normalmente significam briefing errado, não execução errada.
- Meça o custo real por imagem no primeiro lote de 10 e registre aqui. Sem número medido,
  não estime.
- O QA por visão é ordens de grandeza mais barato que a geração de imagem. Rodar QA duas
  vezes (imagem crua + arte montada) sai mais barato que uma única regeração evitada.

---

## 8. Aprovação humana não é opcional

`aprovado_maquina` não é publicação. O `revisor-social` reduz o volume que chega ao humano;
não substitui o humano. Duas razões:

1. Claim em produto físico tem consequência jurídica sob o CDC — o art. 36 exige que a Nitron
   **mantenha em seu poder** o dado técnico que sustenta cada alegação publicada.
2. A taxa de acerto de lançamento deste portfólio caiu para 0,7% na última safra. Este é um
   projeto onde o viés institucional correto é **desconfiar da própria proposta**.
