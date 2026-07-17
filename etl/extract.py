"""Extract: busca as cotacoes na AwesomeAPI.

API publica e de graca (nao precisa de chave), retorna o valor atual de
varios pares de moeda. Ex: https://economia.awesomeapi.com.br/json/last/USD-BRL
"""
import json

import requests

URL = "https://economia.awesomeapi.com.br/json/last/{pares}"
PARES = ["USD-BRL", "EUR-BRL", "BTC-BRL"]


def extrair():
    pares = ",".join(PARES)
    r = requests.get(URL.format(pares=pares), timeout=10)
    r.raise_for_status()
    dados = r.json()
    print(f"extract: {len(dados)} cotacoes da API")
    return dados


if __name__ == "__main__":
    print(json.dumps(extrair(), indent=2, ensure_ascii=False))
