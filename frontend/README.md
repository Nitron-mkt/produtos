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

---

# Portal do lojista — Monte seu PDV

`monte-seu-pdv.html` — documento único e autônomo, sem build e **sem chave de
API**. Sobe em qualquer host estático e funciona offline: nada nele lê o
Supabase, então a ressalva de RLS acima não se aplica a esse arquivo.

O lojista escolhe família, painel, corrida e altura; a página calcula a **cota
externa real** do módulo (a ripa entra 40,60 mm dentro de cada nó) e monta a
solicitação.

## Integrar com o backend

No topo do `<script>`:

```js
var ENDPOINT = "";                       // ex.: "https://api.nitron.com.br/pdv/solicitacoes"
var EMAIL_DESTINO = "trade@nitron.com.br";
```

Com `ENDPOINT` preenchido a página faz `POST` do JSON do pedido. Em branco, ela
cai nos três botões de saída: e-mail, download do JSON e imprimir/PDF.

## O que é fixo

| eixo | opções | fonte |
|---|---|---|
| largura (profundidade) | BLA-01-AC 200 · BLA-03-AC 287 · PSC-02 415 | PI de largura |
| comprimento | PSC-01 315 · PSC-02 415 · PSC-03 595 · PSC-04 717 | PI de comprimento |
| vertical | BAL-02-AC 270 · PSA-05 513 | PI de altura |
| painéis | **7**, pela regra `1,3 ≤ comprimento ÷ largura ≤ 2,6` | grade da Rev. 2 |

Painéis mantidos: `200×360 · 200×450 · 300×450 · 300×634 · 300×754 · 460×634 ·
460×754`. Cortados por proporção: 200×634, 200×754 (tira), 300×360, 460×360,
460×450 (quadrado).

A altura é uma **pilha de baias** — uma ripa vertical por baia, então o mesmo
módulo mistura passo curto e vão alto. No topo, a **peça L** (`850-L`) fecha o
poste e segura uma ripa atravessada sem somar prateleira: é a coroa, e ela passa
21,62 mm de cada lado do corpo.

A geometria, as fórmulas e a cobertura da curva estão em
`analise/11-nitron-mob-cota-final.md` e nos CSVs `dados/22` a `dados/27`.

## Versão do artefato

`_artifact-monte-seu-pdv.html` é **gerado**, não editado à mão:

```bash
python3 build-artifact.py
```

Ele tira o envelope `<!doctype>/<head>/<body>` do arquivo autônomo, porque o
visualizador de artefato injeta o próprio esqueleto. Fonte de verdade única:
edite só o `monte-seu-pdv.html`.
