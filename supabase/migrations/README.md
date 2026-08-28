# Migrations aplicadas

| Nome | Projeto | O que faz |
|---|---|---|
| `pdp_desenvolvimento_produtos` | `bwbeieumxcuomtrvlqxs` (integracao-crm-sankhya) | Cria as 8 tabelas `pdp_*` do projeto de desenvolvimento de produtos, com RLS ligado e política de leitura para `anon`/`authenticated`. Prefixo `pdp_` para não colidir com as ~130 tabelas do CRM. |

Aplicada via MCP do Supabase. Os dados foram carregados por `INSERT ... ON CONFLICT DO NOTHING`,
então reaplicar é idempotente.

## Verificação feita

```sql
SET LOCAL ROLE anon;
SELECT count(*) FROM pdp_linha;              -- 17
SELECT count(*) FROM pdp_linha_concorrente;  -- 86
```
O papel `anon` lê as 8 tabelas e não escreve (só existe política de SELECT).

## Propostas ainda não aplicadas

| Arquivo | O que faz | Estado |
|---|---|---|
| `social_media_squad.sql` | Cria `social_post` e `social_qa` — o estado do fluxo de social media (Claude → n8n → OpenAI → Canva). RLS ligado, só política de SELECT, igual às `pdp_*`. | **não aplicada** — aguarda decisão sobre o caminho do n8n (ver `SOCIAL.md` §2) |
