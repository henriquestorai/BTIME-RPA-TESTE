# Implementa tentativas de re-execução automática em caso de falha

import time
from typing import Callable, Any
from config.settings import MAX_TENTATIVAS

def executar_com_retry(
    funcao: Callable,
    logger,
    *args,
    tentativas: int = MAX_TENTATIVAS,
    espera_segundos: int = 5,
    **kwargs
) -> Any:
    """
    Executa uma função com N tentativas em caso de falha.
    
    Parâmetros:
        funcao          → função a ser executada
        logger          → logger para registrar tentativas
        *args           → argumentos posicionais da função
        tentativas      → número máximo de tentativas (padrão: settings)
        espera_segundos → tempo de espera entre tentativas
        **kwargs        → argumentos nomeados da função
    
    Retorna o resultado da função ou lança exceção após esgotar tentativas.
    """

    for tentativa in range(1, tentativas + 1):
        try:
            logger.info(f"Tentativa {tentativa}/{tentativas} — executando '{funcao.__name__}'")
            resultado = funcao(*args, **kwargs)
            logger.info(f"Tentativa {tentativa}/{tentativas} — SUCESSO")
            return resultado

        except Exception as e:
            logger.warning(f"Tentativa {tentativa}/{tentativas} — FALHA: {e}")

            if tentativa < tentativas:
                logger.info(f"Aguardando {espera_segundos}s antes da próxima tentativa...")
                time.sleep(espera_segundos)
            else:
                logger.error(f"Todas as {tentativas} tentativas falharam para '{funcao.__name__}'")
                raise