# Squad de Social Media — fluxo e contrato com o n8n

Cinco agentes em `.claude/agents/`, uma tabela de estado no Supabase e três passos no n8n.

| Agente | Papel | Entra quando |
|---|---|---|
| `estrategista-conteudo` | pauta com evidência no dado | início |
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

## 2. Três coisas que não funcionam (verificado em 28/08/2026)

### O n8n não chama o Claude Code
Claude Code não tem endpoint de entrada. Um agente `.md` só roda quando alguém abre uma
sessão. Um fluxo que "volta pro Claude" no meio **para e espera um humano**.

O gate de QA automático é **chamada à API da Anthropic com visão** — nó HTTP no n8n ou Edge
Function. Modelo sugerido: `claude-sonnet-5` (visão boa, custo baixo; não precisa de Opus
para dizer que o texto estourou o box).

### O n8n não chama o MCP do Canva
Mesmo motivo. Duas saídas:

- **Caminho A (hoje)** — montagem na sessão do Claude via MCP, com o `montador-canva`.
  Funciona já, sem configurar nada. Precisa de alguém abrindo a sessão.
- **Caminho B (escala)** — n8n fala com a **Canva Connect API** direto (app OAuth próprio).
  Automatiza de ponta a ponta. Exige registrar o app e conferir o plano do Canva.

Comece no A. Migre para o B quando o volume doer.

### Autofill do Canva não está disponível
Zero brand templates com dataset na conta, e a tool `autofill-design` não existe no MCP.
O caminho é `copy-design` → `read-design(open_transaction)` → `edit-design(update_fill +
replace_text)` → `commit` → `export-design`. Está detalhado no `montador-canva`.

---

## 3. O fluxo

```
estrategista-conteudo  → planejado
redator-legenda        → copy_pronta          (claim_check preenchido)
diretor-arte           → briefing_pronto      ← daqui o n8n assume
─────────────────────────────────────────────────────────────────
n8n passo 1: OpenAI gpt-image-1 gera o cenário → imagem_gerada
n8n passo 2: salva PNG no bucket social/       → imagem_hospedada
n8n passo 3: Anthropic API (visão) avalia      → imagem_aprovada
                                               ou imagem_reprovada → volta ao passo 1
                                                  (tentativas_imagem + 1, máx 2)
─────────────────────────────────────────────────────────────────
montador-canva         → arte_montada
revisor-social         → aprovado_maquina  |  *_reprovado
humano                 → publicado
```

O estado vive **todo no Supabase**. Cada passo é idempotente: se o n8n cair no passo 2,
ninguém perde o briefing, e o retry pega de onde parou. É o mesmo padrão do `fila-processar`
que já roda de minuto em minuto neste projeto.

**Não crie um segundo agendador.** O projeto já tem ~70 crons em `pg_cron` disparando 54 Edge
Functions. Ou o n8n agenda, ou o `pg_cron` chama o webhook do n8n. Escolha um.

---

## 4. Contrato com o n8n

### Ler o que está pronto para gerar imagem

```http
GET {SUPABASE_URL}/rest/v1/social_post
    ?status=eq.briefing_pronto
    &tentativas_imagem=lt.2
    &select=id,marca,canal,formato,prompt_imagem,foto_produto_url,template_ref,referencia
    &order=data_prevista.asc
    &limit=5
```

### Devolver o resultado

```http
PATCH {SUPABASE_URL}/rest/v1/social_post?id=eq.123
{
  "imagem_gpt_url": "https://…/storage/v1/object/public/social/123-v1.png",
  "status": "imagem_hospedada"
}
```

### Chaves — onde cada uma mora

| Chave | Onde | Regra |
|---|---|---|
| `service_role` do Supabase | **só** no n8n, server-side | dá escrita em tudo. Nunca em front-end, nunca em log, nunca em nó com output visível. |
| `anon` do Supabase | front-end apenas | ⚠️ **89 tabelas deste projeto estão com RLS desligado**, incluindo `contato_enriquecido` (21 k) e `ghl_cliente` (10 k). A `anon` dá **leitura e escrita** nelas. |
| OpenAI | secret do n8n | não replique no banco |
| Anthropic | secret do n8n | não replique no banco |
| Canva | OAuth do app (caminho B) | não replique no banco |

As tabelas `social_*` nascem com RLS ligado e só política de SELECT, igual às `pdp_*`.

### Bucket

Crie `social` **público** (o `upload-asset-from-url` do Canva só aceita URL HTTPS já
pública). Convenção de nome: `{social_post.id}-v{tentativa}.png`.

Nunca use pastebin, Imgur ou WeTransfer para conseguir uma URL pública. Os buckets do
projeto resolvem, e material de marca não vai para hospedagem de terceiro.

---

## 5. Custo e teto

- **Máximo 2 regerações por post.** Na terceira, `status = 'parado_revisao_humana'`.
  Loop automático de reprovação queima crédito sem convergir — e três reprovações no mesmo
  item normalmente significam briefing errado, não execução errada.
- Meça o custo real por imagem no primeiro lote de 10 e registre aqui. Sem número medido,
  não estime.
- O QA por visão é ordens de grandeza mais barato que a geração de imagem. Rodar QA duas
  vezes (imagem crua + arte montada) é mais barato que uma regeração evitada.

---

## 6. Aprovação humana não é opcional

`aprovado_maquina` não é publicação. O `revisor-social` reduz o volume que chega ao humano;
não substitui o humano. Duas razões:

1. Claim em produto físico tem consequência jurídica sob o CDC — art. 36 exige que a Nitron
   **mantenha em seu poder** o dado técnico que sustenta cada alegação publicada.
2. A taxa de acerto de lançamento deste portfólio caiu para 0,7% na última safra. Este é um
   projeto onde o viés institucional correto é **desconfiar da própria proposta**.
