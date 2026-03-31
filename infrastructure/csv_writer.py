# Responsável por salvar as cotações coletadas em arquivo CSV
# Boa prática de RPA: organização dos arquivos de saída com timestamp no nome

import csv
import os
from datetime import datetime
from typing import List
from core.models import Cotacao
from config.settings import OUTPUT_DIR

def salvar_csv(cotacoes: List[Cotacao], nome_script: str) -> str:
    """
    Salva uma lista de cotações em arquivo CSV no diretório /output.

    Parâmetros:
        cotacoes    → lista de objetos Cotacao para salvar
        nome_script → prefixo do nome do arquivo (ex: 'scraper', 'api')

    Retorna:
        Caminho completo do arquivo CSV gerado
    """

    # Garante que a pasta /output existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Nome do arquivo com timestamp ex: scraper_2024-01-15_14-30-00.csv
    timestamp    = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"{nome_script}_{timestamp}.csv"
    caminho_csv  = os.path.join(OUTPUT_DIR, nome_arquivo)

    # Cabeçalhos do CSV baseados no modelo Cotacao
    cabecalhos = ["moeda", "valor_brl", "fonte", "coletado_em"]

    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=cabecalhos)
        writer.writeheader()

        for cotacao in cotacoes:
            writer.writerow(cotacao.to_dict())

    return caminho_csv