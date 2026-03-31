# Responsável por coletar cotações via API pública (open.er-api.com)
# API gratuita, sem necessidade de cadastro ou chave de acesso

import requests
from typing import List
from config.settings import URL_API, MOEDAS_ALVO, TIMEOUT

def coletar_via_api() -> List[dict]:
    """
    Acessa a API de câmbio e retorna as cotações das moedas alvo em BRL.

    A API retorna taxas com BRL como base, então invertemos o valor
    para obter quanto cada moeda estrangeira vale em reais.

    Retorna:
        Lista de dicionários com 'moeda' e 'valor'

    Lança:
        Exception em caso de falha na requisição ou resposta inválida
    """

    response = requests.get(URL_API, timeout=TIMEOUT)

    # Valida se a requisição foi bem sucedida
    if response.status_code != 200:
        raise Exception(f"API retornou status inesperado: {response.status_code}")

    dados = response.json()

    # Valida se a API retornou resultado positivo
    if dados.get("result") != "success":
        raise Exception(f"API retornou resultado inválido: {dados.get('result')}")

    taxas = dados.get("rates", {})

    if not taxas:
        raise Exception("API retornou taxas vazias.")

    cotacoes = []

    for moeda in MOEDAS_ALVO:
        if moeda in taxas:
            # A API retorna quantos BRL equivalem a 1 unidade de cada moeda
            # Como a base é BRL, invertemos: 1 moeda estrangeira = 1 / taxa BRL
            taxa_brl = taxas.get("BRL", 1)
            taxa_moeda = taxas.get(moeda, None)

            if taxa_moeda and taxa_moeda != 0:
                valor_em_brl = taxa_brl / taxa_moeda
                cotacoes.append({
                    "moeda": moeda,
                    "valor": round(valor_em_brl, 4)
                })

    if not cotacoes:
        raise Exception("Nenhuma moeda alvo encontrada na resposta da API.")

    return cotacoes