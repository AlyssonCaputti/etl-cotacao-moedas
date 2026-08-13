# ETL de cotação de moedas

Pipeline ETL simples em Python que busca a cotação de moedas numa API pública,
trata os dados e grava num PostgreSQL. Fiz pra praticar o fluxo
**extract → transform → load** e mexer com banco em container.

## Como funciona

```
AwesomeAPI  ──(extract)──>  JSON cru  ──(transform)──>  linhas limpas  ──(load)──>  Postgres
```

- **extract** (`etl/extract.py`): busca USD, EUR e BTC contra o Real na
  [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas) (grátis, sem chave).
  Se a API estiver fora, usa um exemplo salvo em `dados/exemplo.json`.
- **transform** (`etl/transform.py`): a API manda tudo como texto, aqui eu
  converto pra número/data, monto o par (`USD/BRL`) e organizo as colunas.
- **load** (`etl/load.py`): cria a tabela `cotacoes` (se não existir) e insere.
  Tem um `UNIQUE (par, data_cotacao)` + `ON CONFLICT DO NOTHING` pra não
  duplicar quando rodo o pipeline mais de uma vez.

## Como rodar

```bash
docker compose up -d              # sobe o postgres na porta 5432
pip install -r requirements.txt
python main.py                    # roda o ETL
```

Depois dá pra consultar os dados:

```bash
docker exec -it cotacoes_db psql -U postgres -d cotacoes -f - < consultas_exemplo.sql
```

Ou conectar em `localhost:5432` (user/senha `postgres`) com qualquer cliente
SQL e rodar as queries de `consultas_exemplo.sql`.

## Rodar de tempos em tempos

A ideia é rodar o `main.py` periodicamente pra ir montando um histórico. Dá
pra agendar com o cron (Linux) ou o Agendador de Tarefas (Windows). Não coloquei
Airflow nem nada disso de propósito: pra um projeto desse tamanho seria demais.

## Estrutura

```
etl/
  config.py      # dados de conexão (lê de variável de ambiente)
  extract.py     # busca na API
  transform.py   # limpa e formata
  load.py        # grava no postgres
main.py          # roda os 3 passos em ordem
docker-compose.yml
consultas_exemplo.sql
dados/exemplo.json  # fallback offline
```
