-- Consultas de exemplo pra ver os dados depois que o ETL rodou.

-- ultima cotacao de cada par
SELECT DISTINCT ON (par)
    par, compra, venda, variacao_pct, data_cotacao
FROM cotacoes
ORDER BY par, data_cotacao DESC;

-- quantas cotacoes ja foram coletadas por par
SELECT par, COUNT(*) AS total_coletas
FROM cotacoes
GROUP BY par
ORDER BY par;

-- historico do dolar (as ultimas 10 coletas)
SELECT data_cotacao, compra, venda
FROM cotacoes
WHERE par = 'USD/BRL'
ORDER BY data_cotacao DESC
LIMIT 10;
