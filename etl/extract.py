"""Extract: busca as cotacoes na AwesomeAPI.

API publica e de graca (nao precisa de chave), retorna o valor atual de
varios pares de moeda. Ex: https://economia.awesomeapi.com.br/json/last/USD-BRL

Se a API estiver fora do ar, cai pro arquivo de exemplo em dados/exemplo.json
pra nao quebrar (e pra dar pra rodar offline).
"""
import json
from pathlib import Path

import requests

URL = "https://economia.awesomeapi.com.br/json/last/{pares}"
PARES = ["USD-BRL", "EUR-BRL", "BTC-BRL"]
EXEMPLO = Path(__file__).resolve().parent.parent / "dados" / "exemplo.json"


def extrair():
    pares = ",".join(PARES)
    try:
        r = requests.get(URL.format(pares=pares), timeout=10)
        r.raise_for_status()
        dados = r.json()
        print(f"extract: {len(dados)} cotacoes da API")
        return dados
    except requests.RequestException as e:
        # nao quero que o pipeline quebre so pq a API oscilou
        print(f"extract: API falhou ({e}), usando exemplo offline")
        return json.loads(EXEMPLO.read_text(encoding="utf-8"))


if __name__ == "__main__":
    print(json.dumps(extrair(), indent=2, ensure_ascii=False))
