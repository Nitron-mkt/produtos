# Projeto de Desenvolvimento de Produtos — Nitron

Repositório do projeto de desenvolvimento de produtos: leitura das curvas de venda
por linha, seleção de candidatos a lançamento e validação de mercado.

## Estrutura

- `dados/` — extrações consolidadas do Sankhya (CSV, separador `;`)
  - `01-curva-por-linha.csv` — **corte B** (mercado limpo): curva 36 meses + margem e lucro bruto
  - `01b-curva-tabela-padrao.csv` — **corte A** (PV0003 padrão): teto de preço e margem
  - `02-historico-lancamentos.csv` — taxa de acerto de lançamentos por safra (2021+)
  - `03-vetores-crescimento.csv` — SKUs em crescimento agrupados por vetor
  - `04-migracao-tabelas.csv` — prova de que a queda da padrão é migração, não demanda
  - `05-teto-preco-margem-padrao.csv` — preço e MB na tabela cheia por produto
- `analise/` — diagnóstico e recomendações
  - `01-diagnostico-e-recomendacoes.md` — Fase 1: curvas, vetores, 3+1 produtos por linha

## Metodologia da extração

- **Escopo:** Nitronplast (empresas 1 Matriz, 2 Filial, 14 Extrema), grupo Produto Acabado/Revenda
- **Receita:** `TGFCAB.TIPMOV` V/D, `STATUSNOTA='L'`, apenas TOPs com `ATUALFIN <> 0`
- **Devoluções** abatidas com sinal negativo
- **Excluídas** transferências intercompany (TOPs 3316, 3300, 3261, 3242, 3310, 3322)
- **Janelas móveis de 12 meses** para neutralizar sazonalidade e anos parciais
- **Custo:** `TGFCUS.CUSGER` (último registro de 2026, empresa 1, local 0)
- **Tabela de preço:** `TGFITE.NUTAB → TGFTAB.NUTAB → CODTAB`, nome em `TGFNTA`

### Os dois cortes

A "003 – tabela padrão" é `CODTAB = 0` (`PV0003 - TABELA PADRÃO`). Atenção: `CODTAB = 3` é
`TABELA EXPORTAÇÃO NITRON`.

| Corte | Filtro | Serve para | Não serve para |
|---|---|---|---|
| **A — Tabela padrão** | `CODTAB = 0` | Teto de preço e de margem (MB 60–80%) | Tendência: contaminado por migração de tabela |
| **B — Mercado limpo** | exceto `CODTAB` 84 (Avon/Natura) e 3 (exportação) | Curva, tendência, vetores, lançamentos | Precificação de tabela cheia |

A tabela padrão caiu 73% em 2 anos, mas isso é **migração**: Extrema (2025) e o programa Clube Nitron
criaram tabelas próprias que absorveram ~R$ 37 M — quase exatamente o que a padrão perdeu.
Ver `dados/04-migracao-tabelas.csv`.

## Fases

1. ✅ Diagnóstico das curvas e seleção de candidatos
2. ⏳ Raspagem de mercado para validar/matar cada candidato
3. ⏳ Business case e priorização por CAPEX/tonelagem
