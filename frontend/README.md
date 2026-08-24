# Painel de Lançamento — front-end

Arquivo único, sem build. Lê as tabelas `pdp_*` do Supabase via REST.

## Rodar local

```bash
cp config.example.js config.js   # preencha SUPABASE_KEY
python3 -m http.server 8080
# abre http://localhost:8080
```

## Publicar

Qualquer host estático serve (Vercel, Netlify, Cloudflare Pages, GitHub Pages,
Supabase Storage). Suba `index.html` + `config.js`.

## Antes de publicar em URL pública — leia

Este projeto Supabase tem **89 tabelas com RLS desligado**, incluindo dados de
cliente (`ghl_cliente` 10.413 linhas, `contato_enriquecido` 21.015,
`parc_matriz` 3.735, `cobranca_cliente` 619). A chave anon/publishable que este
front-end usa dá **leitura e escrita** nessas tabelas para qualquer pessoa que
abrir o código-fonte da página.

As tabelas `pdp_*` que este painel usa já nascem com RLS ligado e política de
leitura pública — elas estão certas. O problema são as outras.

Duas saídas antes de expor a chave:
1. Ligar RLS nas 89 tabelas com políticas adequadas (o MCP do Supabase entrega o
   SQL de remediação; **não rode sem definir as políticas**, senão bloqueia o CRM).
2. Ou servir os dados por uma Edge Function com `service_role` no servidor, e o
   front-end chama a função em vez do PostgREST.

## Fonte dos dados

| Tabela | Conteúdo |
|---|---|
| `pdp_linha` | 17 linhas: curva, margem, score, veredito, o que lançar, por que sim/não |
| `pdp_linha_concorrente` | cruzamento linha × concorrente Tier A/D |
| `pdp_concorrente` | 26 concorrentes do mapa competitivo |
| `pdp_vetor` + `pdp_vetor_evidencia` | 8 vetores de crescimento e as evidências |
| `pdp_cor` | performance das 16 cores |
| `pdp_capacidade` | ocupação das injetoras por faixa de tonelagem |
| `pdp_lancamento_safra` | taxa de acerto de lançamento por safra |
