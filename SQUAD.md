# Como rodar a squad no Claude

Este repositório é a squad. Ele tem três partes:

| Arquivo | O que é |
|---|---|
| `CLAUDE.md` | **A memória do projeto.** Carrega automaticamente em toda sessão aberta nesta pasta. Contém as armadilhas de query, as conclusões já estabelecidas e os erros já cometidos. |
| `.claude/agents/*.md` | Os quatro agentes. O Claude os detecta sozinho e chama por nome. |
| `SQUAD.md` (este) | Como conectar, como pedir e o que não fazer. |

---

## 1. Antes de tudo: as duas conexões

A squad **não funciona sem Sankhya e Supabase**. Sem elas os agentes só têm o que está
escrito no `CLAUDE.md` — e vão responder de memória, que é exatamente o que este projeto
não quer.

### Sankhya (ERP — leitura)
Já existe como conector na conta `marketing@nitron.com.br`. Ele é um MCP remoto, então:

- **Claude na web / app / Cowork**: o conector já vem junto. Confira em
  **Settings → Connectors** que "Sankhya" está com status conectado.
- **Claude Code no terminal**: os conectores da conta não entram automaticamente. Rode
  `claude mcp list` para ver o que está ativo. Se Sankhya não aparecer, pegue a URL do
  servidor em Settings → Connectors e adicione:
  ```bash
  claude mcp add --transport http sankhya <URL-DO-SERVIDOR-MCP>
  ```
  (a URL é da instalação da Nitron — não está neste repositório de propósito, não commite ela)

Ferramentas esperadas: `sankhya_query`, `sankhya_describe_view`, `sankhya_list_views`,
`sankhya_dicionario_tabela`, `sankhya_dicionario_join`.
`sankhya_query` é **somente SELECT** — bloqueia escrita. Isso é proposital: nenhum agente
desta squad tem permissão de alterar o ERP.

### Supabase (onde as conclusões são gravadas — leitura e escrita)
```bash
claude mcp add supabase -- npx -y @supabase/mcp-server-supabase@latest \
  --project-ref=bwbeieumxcuomtrvlqxs
```
O token de acesso vai na variável de ambiente `SUPABASE_ACCESS_TOKEN` (Personal Access
Token, gerado em Supabase → Account → Access Tokens). **Não coloque o token em arquivo
deste repositório.**

Projeto correto: **`bwbeieumxcuomtrvlqxs`** (`integracao-crm-sankhya`).
Existe outro projeto chamado `afiliados` na mesma organização — **não é esse**.

### Teste de 30 segundos, antes de pedir qualquer análise
Peça ao Claude:

> Confirme que os MCPs de Sankhya e Supabase estão respondendo: traga a contagem de linhas
> de `pdp_linha` no Supabase e o `SELECT COUNT(*) FROM TGFPRO WHERE CODGRUPOPROD BETWEEN
> 1000000 AND 1009999` no Sankhya.

Resposta esperada: **17 linhas** em `pdp_linha` e **~4.252 produtos** no Sankhya.
Se algum dos dois falhar, pare e conserte a conexão. Não siga.

---

## 2. Os quatro agentes

```
analista-sankhya    → o dado interno: curva, margem, família, quantos clientes, o que já existe
        ↓
radar-concorrencia  → o dado externo: preço, marcas, avaliações (API oficial do ML primeiro, Apify depois)
        ↓
engenheiro-molde    → é fabricável? em que injetora? qual material? o claim se sustenta?
        ↓
curador-portfolio   → o crítico, com VETO. Já existe? É proliferação? O payback fecha?
        ↓
grava em pdp_lancamento (status = 'proposto')
```

**Regra dura: nada entra em `pdp_lancamento` sem passar pelo `curador-portfolio`.**
Com 0,7% de acerto na última safra (2 de 278 SKUs), o viés padrão da squad é **não lançar**.

Cada linha gravada precisa de `evidencia` preenchida com o dado que a sustenta —
CODPROD, referência, valor, variação, contagem de clientes ou preço de concorrente.
**Proposta sem evidência não entra.**

---

## 3. Como pedir

Chame o agente por nome quando quiser um passo só:

> Use o `analista-sankhya`: quais SKUs da família 231/232/233/234 (referência completa
> `.012.001`) cresceram nos últimos 12 meses, com contagem de clientes por SKU?

> Use o `curador-portfolio`: vale abrir molde de tampa trava+válvula para os potes
> pequenos? O investimento é nosso.

Ou peça o fluxo inteiro e deixe o Claude encadear:

> Rode a squad completa para avaliar uma tampa com trava e válvula na linha de potes.
> Quero o veredito do curador antes de qualquer coisa ir para o Supabase.

Em sessão longa, peça o dado **antes** da conclusão. A regra que mais economizou
retrabalho aqui: *"me traga a query e o número, depois a recomendação."*

---

## 4. As cinco coisas que já deram errado — evite repetir

1. **Tabela de preço.** A "003 tabela padrão" é **`CODTAB = 0`**.
   `CODTAB = 3` é **exportação**. E sempre exclua `CODTAB = 84` (Avon/Natura, R$ 8,97 M em
   580 itens) — esse cliente quebra a curva de marca própria.
2. **Referência truncada.** `233` ≠ `233.012.001`. Truncar traz uma família homônima de
   private label com 2-4 clientes em vez da família de canal com ~1.000. Esse erro já
   gerou recomendação publicada e errada.
3. **Produto que já existe.** Dois "certeiros" propostos já estavam no catálogo.
   O primeiro teste do curador é procurar no `TGFPRO`.
4. **Capacidade ociosa ≠ oportunidade.** Molde é 30-40% do custo de um lançamento. CNC
   parado pode ser gargalo de ferramentaria, não folga.
5. **`pg_net` é assíncrono.** Requisição HTTP disparada do Postgres pode levar minutos
   para aparecer em `net._http_response`. Três já foram declaradas como "403 / não
   funciona" quando estavam só na fila — uma delas era 200.

---

## 5. Segurança — o que nenhum agente deve fazer

- **Não imprimir** `ml_oauth_token.access_token` nem `ml_oauth_app.apify_token` na
  conversa. Use dentro do SQL:
  ```sql
  SELECT net.http_get(
    url := 'https://api.mercadolibre.com/products/search?site_id=MLB&status=active&q=pote',
    headers := jsonb_build_object('Authorization','Bearer '||
      (SELECT access_token FROM ml_oauth_token ORDER BY id LIMIT 1)));
  ```
- **89 tabelas desse projeto Supabase estão com RLS desligado**, incluindo dado de cliente
  (`contato_enriquecido` 21 k, `ghl_cliente` 10 k, `parc_matriz` 3,7 k, `cobranca_cliente`).
  A chave anon dá leitura **e escrita** nelas. **Não publique o front-end em URL pública
  antes de resolver isso.** As tabelas `pdp_*` já nascem com RLS e política de SELECT.
  E não ligue RLS nas outras sem definir política — isso derruba o CRM.
- `frontend/config.js` está no `.gitignore`. A chave não vai para o repositório.
- Os atores do **Apify são PAY_PER_EVENT** (~US$ 0,15 por run de 50-80 itens).
  Confirme o gasto com o usuário antes de rodar lote.
- `sankhya_query` é read-only. Nenhum agente altera cadastro, preço ou estoque no ERP.

---

## 6. Onde estão as coisas

| Caminho | Conteúdo |
|---|---|
| `analise/01-diagnostico-e-recomendacoes.md` | O diagnóstico completo da carteira |
| `analise/02-coleta-mercado-livre.md` | Quais rotas do ML funcionam e como coletar |
| `analise/carteira-lancamentos.html` | O relatório visual |
| `analise/painel-lancamento.html` | O painel de decisão por categoria |
| `frontend/` | Front-end que lê as tabelas `pdp_*` via PostgREST |
| `dados/` | CSVs das extrações e o `mapa_concorrentes_nitron.md` |
| `supabase/migrations/` | Histórico das migrations `pdp_*` |
