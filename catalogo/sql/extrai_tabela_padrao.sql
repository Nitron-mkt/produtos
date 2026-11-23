-- Extração da tabela padrão (CODTAB 0 = "PV0003 - TABELA PADRÃO") para o catálogo.
-- Atenção: CODTAB 3 é EXPORTAÇÃO, não é a padrão.
-- Só produtos ativos e não suspensos. Saída: uma linha por produto, campos separados por |
-- Conferência (23/11/2026): 620 itens, soma CODPROD 4.247.642, soma preço R$ 15.766,71, soma caixa 7.096.
SELECT P.CODPROD||'|'||C.REFERENCIA||'|'||C.PRODUTO||'|'||C.GRUPO||'|'||C.EAN13||'|'||C.EAN13_SITUACAO
       ||'|'||C.QTD_CAIXA||'|'||C.MULTIPLO_VENDA||'|'||TO_CHAR(P.PRECO,'FM99990.00') AS L
FROM AD_VW_COM_PRECOS P
JOIN AD_VW_COM_CADPRODUTOS C ON C.CODPROD = P.CODPROD
WHERE P.CODTAB = 0
  AND C.ATIVO = 'S'
  AND NVL(C.SUSPENSO,'N') <> 'S'
ORDER BY P.CODPROD;

-- Conferência (rode junto e compare com o arquivo gerado):
-- SELECT COUNT(*), SUM(P.CODPROD), SUM(ROUND(P.PRECO*100)), SUM(NVL(C.QTD_CAIXA,0))
-- FROM AD_VW_COM_PRECOS P JOIN AD_VW_COM_CADPRODUTOS C ON C.CODPROD=P.CODPROD
-- WHERE P.CODTAB=0 AND C.ATIVO='S' AND NVL(C.SUSPENSO,'N')<>'S';
