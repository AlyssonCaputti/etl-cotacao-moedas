"""Load: grava as cotacoes no Postgres.

Cria a tabela se nao existir e insere as linhas. Pra nao duplicar quando rodar
varias vezes no mesmo minuto, uso ON CONFLICT no par+data_cotacao (deixei um
UNIQUE nessas duas colunas).
"""
import psycopg2

from etl.config import DB_CONFIG

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS cotacoes (
    id            SERIAL PRIMARY KEY,
    par           TEXT NOT NULL,
    moeda_origem  TEXT,
    moeda_destino TEXT,
    compra        NUMERIC(18, 6),
    venda         NUMERIC(18, 6),
    maxima        NUMERIC(18, 6),
    minima        NUMERIC(18, 6),
    variacao_pct  NUMERIC(10, 4),
    data_cotacao  TIMESTAMP,
    carregado_em  TIMESTAMP DEFAULT NOW(),
    UNIQUE (par, data_cotacao)
);
"""

INSERT = """
INSERT INTO cotacoes
    (par, moeda_origem, moeda_destino, compra, venda, maxima, minima, variacao_pct, data_cotacao)
VALUES
    (%(par)s, %(moeda_origem)s, %(moeda_destino)s, %(compra)s, %(venda)s,
     %(maxima)s, %(minima)s, %(variacao_pct)s, %(data_cotacao)s)
ON CONFLICT (par, data_cotacao) DO NOTHING;
"""


def carregar(linhas):
    conn = psycopg2.connect(**DB_CONFIG)
    inseridas = 0
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE)
            for linha in linhas:
                cur.execute(INSERT, linha)
                inseridas += cur.rowcount  # 0 se ja existia
        conn.commit()
    finally:
        conn.close()
    print(f"load: {inseridas} linhas novas gravadas (as repetidas foram ignoradas)")
    return inseridas
