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

## Squad de social media

| Arquivo | O que faz | Estado |
|---|---|---|
| `social_media_squad.sql` | Cria `social_post` e `social_qa` — o estado do fluxo de social media (Claude → OpenAI → Canva). RLS ligado, só política de SELECT, igual às `pdp_*`. | **aplicada** 28/08/2026 |
| `social_cron.sql` | Agenda `social-imagem` (*/5) e `social-qa` (2-59/5). Reaproveita o header de um job existente, então não carrega chave. | **aplicada** 28/08/2026 |

Também criado: bucket **`social`** (público, 10 MB, `image/png|jpeg|webp`) e as Edge Functions
`social-imagem` e `social-qa` (v1, ACTIVE, `verify_jwt = true`).

### Verificação feita

```sql
select c.relname, c.relrowsecurity, string_agg(p.polname || ':' || p.polcmd::text, ', ')
from pg_class c left join pg_policy p on p.polrelid = c.oid
where c.relname in ('social_post','social_qa') group by 1,2;
-- social_post | t | social_post_sel:r
-- social_qa   | t | social_qa_sel:r
```
RLS ligado nas duas, só política de SELECT — nenhuma escrita pela `anon`.
