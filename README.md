# Projeto de Desenvolvimento de Produtos — Nitron

Repositório do projeto de desenvolvimento de produtos: leitura das curvas de venda
por linha, seleção de candidatos a lançamento e validação de mercado.

## Estrutura

- `dados/` — extrações consolidadas do Sankhya (CSV, separador `;`)
  - `01-curva-por-linha.csv` — curva 36 meses por linha + margem e lucro bruto
  - `02-historico-lancamentos.csv` — taxa de acerto de lançamentos por safra (2021+)
  - `03-vetores-crescimento.csv` — SKUs em crescimento agrupados por vetor
- `analise/` — diagnóstico e recomendações
  - `01-diagnostico-e-recomendacoes.md` — Fase 1: curvas, vetores, 3+1 produtos por linha

## Metodologia da extração

- **Escopo:** Nitronplast (empresas 1 Matriz, 2 Filial, 14 Extrema), grupo Produto Acabado/Revenda
- **Receita:** `TGFCAB.TIPMOV` V/D, `STATUSNOTA='L'`, apenas TOPs com `ATUALFIN <> 0`
- **Devoluções** abatidas com sinal negativo
- **Excluídas** transferências intercompany (TOPs 3316, 3300, 3261, 3242, 3310, 3322)
- **Janelas móveis de 12 meses** para neutralizar sazonalidade e anos parciais
- **Custo:** `TGFCUS.CUSGER` (último registro de 2026, empresa 1, local 0)

## Fases

1. ✅ Diagnóstico das curvas e seleção de candidatos
2. ⏳ Raspagem de mercado para validar/matar cada candidato
3. ⏳ Business case e priorização por CAPEX/tonelagem
