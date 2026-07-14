"""Roda o ETL de ponta a ponta: extract -> transform -> load.

Uso:
    python main.py
"""
from etl.extract import extrair
from etl.transform import transformar
from etl.load import carregar


def main():
    print("--- iniciando ETL de cotacoes ---")
    brutos = extrair()
    linhas = transformar(brutos)
    carregar(linhas)
    print("--- fim ---")


if __name__ == "__main__":
    main()
