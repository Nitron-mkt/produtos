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

`planejado` → `copy_pronta` → `briefing_pronto` → `gerando_imagem` → `imagem_hospedada` →
`imagem_aprovada` → `arte_montada` → `aprovado_maquina` → `publicado`

`gerando_imagem` é a **trava**, não um estado de trabalho: só existe entre pegar o post e
gravar o resultado.

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
| montagem no Canva de ponta a ponta | ✅ **fechado no Modelo 04**: `social_post` id 2, teaser de setembro da Nitron-Mob. GPT gerou a cena, QA automático aprovou, Canva montou, PNG 1080×1350 exportado, design na pasta `Setembro 2026`. |
| montagem nos Modelos 01/02/03 | ⚠️ mecânica funciona; o QA reprovou o post id 1 por fundo branco da foto (§6) |
| fotos de produto recortadas (PNG sem fundo) | ⬜ **o bloqueio dos modelos de produto** — ver §6 |
| trava de concorrência e resgate de órfão | ✅ na `social-imagem` |

**Desligar sem apagar**, se precisar:
`update cron.job set active = false where jobname like 'social-%';`

Teste de fumaça (as duas devolveram 200 com fila vazia em 28/08/2026):
```
{"processados":0,"resultados":[]}
{"avaliados":0,"resultados":[]}
```

---

## 6. Os modelos do Canva — e por que o mapa expira

Cadastrados em `social_modelo`, com o mapa `papel → locator_id`. Todos **1080 × 1350 (4:5)**,
brand kit `NITRON`. Leia sempre pela view `social_modelo_pronto`, que separa os adornos.

| Modelo | Template | Para que serve | Fotos de produto | Cenários GPT | Pessoa |
|---|---|---|---|---|---|
| **01** | `EAHTlFA83HE` | produto único em destaque | 1 | **0** | não |
| **02** | `EAHTlKR9Mek` | família ou cor: 4 SKUs empilhados | 4 | **0** | não |
| **03 teal** | `EAHTlO_M85U` p.1 | produto em uso, fundo teal | 1 | **0** | não |
| **03 rosa** | `EAHTlO_M85U` p.2 | mesmo layout, fundo rosa | 1 | **0** | não |
| **04** | `EAHTlIZUQbA` | institucional / lifestyle, squircle | 0 | 1 | **sim** |
| **05** | `EAHTlG7KBaQ` | listicle: 4 fotos de produto em ambiente | 4 | **0** | não |

### Template remontado troca `locator_id` — o mapa tem validade

Em 31/08/2026 a squad remontou os cinco. Mesmos IDs de template, `updated_at` novo, e:

| Modelo | O que mudou |
|---|---|
| **01** | título 73.9pt → **100pt** e cor coral → **teal `#0aa9b1`**; `logo` mudou de id; 3 adornos de marca novos |
| **02** | título → 100pt, subtítulo → 46.7pt; `logo` mudou de id; adorno de frutas removido |
| **03** | passou a ter **2 páginas** (teal e rosa), com `locator_id` **diferentes em cada** |
| **04** | slot deixou de ser **círculo** e virou **squircle**; `subtitulo`, `cenario_1` e `logo` mudaram de id — **só `titulo` e `page_id` sobreviveram** |
| **05** | título deixou de ser **bicolor** (a armadilha antiga acabou); `logo` mudou de id |

Meu teste anterior provou que `locator_id` é estável **entre cópias do mesmo template**. Um
template **remontado** é outra coisa: os ids trocam. As duas afirmações convivem, e confundir
uma com a outra é o que faz montar no elemento errado.

**Pré-voo obrigatório antes de montar:** `search-brand-templates` → compare `updated_at` com
`social_modelo.canva_updated_at`. Canva maior = mapa velho = remapeie primeiro.

### `isMediaReplaceable` deixou de significar "slot de produto"

Era uma heurística minha, e o remonte a matou: os modelos novos têm **adornos de marca
substituíveis** — os "O" do símbolo Nitron, folhas, texturas. Trocar um deles por foto de
produto gera post absurdo.

No `mapa`, papel que começa com `_` é adorno e **não se escreve nele**.
`social_modelo_pronto` entrega `mapa_editavel` e `adornos_nao_mexer` já separados.

### Modelo 05 foi reclassificado

As 4 fotos são **produto em ambiente** (o carrinho Nitron-Mob em banheiro, cozinha,
lavanderia e entrada), não cenário vazio. O GPT não desenha produto, então: `slots_produto =
4`, `slots_cenario = 0` — o oposto do que eu havia cadastrado lendo só a estrutura.

**Depois do remonte, o Modelo 04 é o único que usa GPT.** Os outros cinco slots-de-produto
dependem de fotografia — e os Modelos 01, 02 e 03 dependem de **PNG recortado**, o bloqueio
de sempre.

### Limites de caractere caíram

Os títulos foram de 73.9pt para **100pt**, então cabe menos: Modelo 01 → 24, Modelo 02 → 27,
Modelo 04 → 32, Modelo 03 → 40, Modelo 05 → 38. Medidos na renderização, não estimados. O
remonte invalida essas medidas: reconfira depois de cada um.

### Convenção de nome no Canva

`Marca · DD-MM · Formato · Linha · assunto`
(ex.: `Nitron · 02-09 · Estático · Nitron-Mob · teaser de linha`)

---

## 6.1 Coerência entre copy e imagem — o furo que o post 2 revelou

O teaser de setembro da Nitron-Mob saiu tecnicamente correto e **comunicativamente errado**:
copy prometendo "cantos que a casa ainda não resolveu" e nomeando arara e prateleiras, sobre
uma cena de quarto arrumado sem nenhum dos dois. Os **dois QA aprovaram**.

### Por que os dois QA aprovaram

Porque ambos comparavam a imagem com o **prompt**, e o prompt estava sendo cumprido à risca.
Quem escreveu o prompt foi quem escreveu a copy, na mesma cabeça e no mesmo minuto — então
**um briefing incoerente passa no próprio teste**. Um gate que valida o executor contra as
instruções do executor não é um gate.

### A correção: `promessa_visual`

Novo campo em `social_post`, escrito pelo **`redator-legenda`** a partir da copy — nunca a
partir do prompt. É o contrato: *o que a imagem precisa mostrar para a copy não mentir.*

- O `diretor-arte` escolhe o modelo e escreve o prompt **para entregar a promessa**.
- O `social-qa` avalia a cena contra a **promessa** (item 8, bloqueante), com o prompt
  rebaixado a "briefing técnico secundário".
- O `revisor-social` lê a promessa **antes** da arte. Ler o prompt primeiro contamina o
  julgamento: você passa a avaliar se o prompt foi cumprido.

O banco recusa `briefing_pronto` sem `promessa_visual`. Isso é trigger, não convenção.

### As duas incoerências que o item 8 caça

| Falha | Como aparece |
|---|---|
| **Copy de problema, cena de solução** | O texto vende a dor ("o canto que ninguém resolveu") e a imagem mostra ordem. A cena comunica o oposto do texto. |
| **Copy nomeia objeto que a imagem não tem** | "arara de roupa e prateleiras" escrito, nada na foto. O leitor procura e não acha. |

### A correção estrutural: roteamento por promessa

`social_modelo.aceita_produto_na_copy`. O **Modelo 04 é `false`** — não tem slot de produto,
então não pode ilustrar copy que nomeia SKU. Um trigger recusa post com `codprod` ou
`referencia` nesse modelo.

Regra em uma linha: **a promessa escolhe o modelo, o modelo restringe a copy.** Não o
contrário.

### O gate foi testado contra o proprio caso que o motivou

Repus o post 2 em `imagem_hospedada` com a **mesma imagem** e a promessa preenchida.
O `social-qa` reprovou por **item 8** nas tres rodadas, e escreveu a correcao sozinho:

> *"Remover a acao de 'dobrar roupa sobre cama arrumada' pois isso comunica organizacao ja
> resolvida; substituir por uma cena de roupas acumuladas sem destino e parede/vao vazio."*

Isso e a mesma conclusao a que eu havia chegado lendo a arte. O gate nao esta apenas
bloqueando: ele esta produzindo o briefing corrigido.

### O que a cena certa seria, naquele post

A **dor**: cadeira com roupa acumulada, parede vazia sem uso, vão ocioso ao lado da máquina —
e nenhum móvel de organização na cena, porque é exatamente o que está faltando ali. A
ausência do produto deixa de ser um furo e passa a ser o argumento.

Isso vale como padrão: em copy de "antes", a ausência do produto é intencional e a cena
mostra o problema. Em copy de "depois", o produto tem que aparecer — e aí o modelo precisa
de slot de produto.

### Quando a copy exige produto E cenário ao mesmo tempo

Existe um caminho que ainda não está em uso: `edit-design` tem `insert_fill`, que **insere um
novo elemento de imagem** numa posição do design. Com um PNG recortado dá para pôr a foto
real do produto **por cima** do cenário do GPT, em qualquer modelo — inclusive no 04, que não
tem slot de produto.

Esbarra no mesmo bloqueio de §6: `produto_foto` é JPG com fundo branco, e um retângulo branco
sobre uma cena fotográfica fica pior do que sobre cor plana. O mecanismo está pronto e espera
o bucket de recorte.

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
