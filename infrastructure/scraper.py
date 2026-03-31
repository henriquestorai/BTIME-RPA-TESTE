# Responsável por coletar cotações via Web Scraping
# Utiliza requests + BeautifulSoup no Google Finance
# Faz uma requisição por moeda consultando diretamente a URL de cada par

import requests
from bs4 import BeautifulSoup
from typing import List
from config.settings import TIMEOUT

# Headers para simular navegador real e evitar bloqueios
HEADERS = {
    "User-Agent"      : (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language" : "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Moedas alvo com suas URLs diretas no Google Finance
MOEDAS_SCRAPING = {
    "USD": "https://www.google.com/finance/quote/USD-BRL",
    "EUR": "https://www.google.com/finance/quote/EUR-BRL",
    "GBP": "https://www.google.com/finance/quote/GBP-BRL",
    "ARS": "https://www.google.com/finance/quote/ARS-BRL",
}

def coletar_via_scraping() -> List[dict]:
    """
    Acessa o Google Finance e coleta a cotação de cada moeda em BRL.
    Faz uma requisição por moeda e extrai o valor do HTML retornado.

    Retorna:
        Lista de dicionários com 'moeda' e 'valor'

    Lança:
        Exception se nenhuma cotação for coletada
    """

    cotacoes = []

    for moeda, url in MOEDAS_SCRAPING.items():
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)

            if response.status_code != 200:
                print(f"[AVISO] {moeda}: status {response.status_code} — ignorando.")
                continue

            soup  = BeautifulSoup(response.text, "html.parser")
            valor = _extrair_valor(soup, moeda)

            if valor:
                cotacoes.append({"moeda": moeda, "valor": valor})
                print(f"[OK] {moeda}: R$ {valor:.4f}")
            else:
                print(f"[AVISO] {moeda}: valor não encontrado na página.")

        except Exception as e:
            print(f"[AVISO] {moeda}: erro ao coletar — {e}")
            continue

    if not cotacoes:
        raise Exception("Nenhuma cotação foi coletada via scraping.")

    return cotacoes


def _extrair_valor(soup: BeautifulSoup, moeda: str) -> float:
    """
    Extrai o valor da cotação do HTML do Google Finance.
    Tenta múltiplos seletores para maior resiliência.

    Parâmetros:
        soup  → objeto BeautifulSoup com o HTML da página
        moeda → código da moeda para log

    Retorna:
        Valor float ou None se não encontrado
    """

    import re

    # Seletores conhecidos do Google Finance em ordem de prioridade
    seletores = [
        ("div",  {"class": "YMlKec fxKbKc"}),
        ("div",  {"class": "AHmHk"}),
        ("span", {"class": "IsqQVc NprOob XcVN5d"}),
        ("div",  {"data-last-price": True}),
    ]

    for tag, attrs in seletores:
        elemento = soup.find(tag, attrs)
        if elemento:
            texto = elemento.get_text(strip=True)
            valor = _limpar_valor(texto)
            if valor:
                return valor

    # Último recurso — busca por qualquer elemento com data-last-price
    elemento = soup.find(attrs={"data-last-price": True})
    if elemento:
        try:
            valor = float(elemento["data-last-price"])
            if valor > 0:
                return valor
        except (ValueError, KeyError):
            pass

    return None


def _limpar_valor(texto: str) -> float:
    """
    Converte string monetária para float.
    Lida com formatos como '5,42', '5.42', 'R$5,42'

    Parâmetros:
        texto → string bruta extraída do HTML

    Retorna:
        Valor float ou None se não for possível converter
    """

    import re

    numeros = re.findall(r'[\d.,]+', texto)

    for numero in numeros:
        try:
            limpo = numero.replace(".", "").replace(",", ".")
            valor = float(limpo)
            if 0.0001 < valor < 100000:
                return valor
        except ValueError:
            continue

    return None