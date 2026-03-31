# Responsável por registrar todos os eventos da execução em arquivo .txt e no console

import logging
import os
from datetime import datetime
from config.settings import LOG_DIR

def configurar_logger(nome_script: str) -> logging.Logger:
    """
    Cria e configura um logger com saída dupla:
    - Arquivo TXT com timestamp no nome (salvo em /logs)
    - Console (terminal) em tempo real
    """

    # Garante que a pasta /logs existe
    os.makedirs(LOG_DIR, exist_ok=True)

    # Nome do arquivo de log com data e hora ex: scraper_2026-01-31_23-59-00.txt
    timestamp    = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"{nome_script}_{timestamp}.txt"
    caminho_log  = os.path.join(LOG_DIR, nome_arquivo)

    # Cria o logger
    logger = logging.getLogger(nome_script)
    logger.setLevel(logging.DEBUG)

    # Formato da mensagem de log
    formato = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para salvar em arquivo TXT
    handler_arquivo = logging.FileHandler(caminho_log, encoding="utf-8")
    handler_arquivo.setLevel(logging.DEBUG)
    handler_arquivo.setFormatter(formato)

    # Handler para exibir no console/terminal
    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)
    handler_console.setFormatter(formato)

    # Evita duplicar handlers se o logger já existir
    if not logger.handlers:
        logger.addHandler(handler_arquivo)
        logger.addHandler(handler_console)

    logger.info(f"Logger iniciado — arquivo: {nome_arquivo}")
    return logger