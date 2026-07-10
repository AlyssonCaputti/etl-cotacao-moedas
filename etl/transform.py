"""Transform: pega o JSON cru da API e deixa num formato limpo pra carregar.

O que faz:
- transforma o dict {"USDBRL": {...}} numa lista de linhas;
- converte os campos de texto pra numero (a API manda tudo como string);
- monta o par tipo "USD/BRL";
- usa o create_date da API como a data da cotacao.
"""
from datetime import datetime


def transformar(dados_brutos):
    linhas = []
    for chave, info in dados_brutos.items():
        try:
            linha = {
                "par": f"{info['code']}/{info['codein']}",
                "moeda_origem": info["code"],
                "moeda_destino": info["codein"],
                "compra": float(info["bid"]),
                "venda": float(info["ask"]),
                "maxima": float(info["high"]),
                "minima": float(info["low"]),
                "variacao_pct": float(info["pctChange"]),
                "data_cotacao": datetime.strptime(
                    info["create_date"], "%Y-%m-%d %H:%M:%S"
                ),
            }
            linhas.append(linha)
        except (KeyError, ValueError) as e:
            # se vier um registro estranho, pula ele mas avisa
            print(f"transform: pulei {chave} por erro: {e}")

    print(f"transform: {len(linhas)} linhas prontas")
    return linhas


if __name__ == "__main__":
    from extract import extrair
    for l in transformar(extrair()):
        print(l)
