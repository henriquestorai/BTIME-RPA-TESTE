# main_scraper.py
# Ponto de entrada do Script 1 — Web Scraping
# Orquestra todo o fluxo: coleta → processamento → salvamento → log → e-mail

from utils.logger import configurar_logger
from utils.retry import executar_com_retry
from utils.emailer import enviar_email
from core.use_cases import ProcessarCotacoes, ResumoExecucao
from infrastructure.scraper import coletar_via_scraping
from infrastructure.csv_writer import salvar_csv

def main():
    # ─── Inicialização ────────────────────────────────────────────────────
    logger = configurar_logger("scraper")
    logger.info("=" * 50)
    logger.info("  INICIANDO SCRIPT 1 — WEB SCRAPING")
    logger.info("=" * 50)

    caminho_csv = None

    try:
        # ─── Etapa 1: Coleta via Scraping com Retry ───────────────────────
        logger.info("Etapa 1/3 — Coletando cotações via Web Scraping...")
        dados_brutos = executar_com_retry(
            coletar_via_scraping,
            logger
        )
        logger.info(f"{len(dados_brutos)} moeda(s) coletada(s) com sucesso.")

        # ─── Etapa 2: Processamento e Validação ───────────────────────────
        logger.info("Etapa 2/3 — Processando e validando os dados...")
        use_case = ProcessarCotacoes()
        cotacoes = use_case.executar(dados_brutos, fonte="scraping")
        logger.info(f"{len(cotacoes)} cotação(ões) validada(s).")

        # ─── Etapa 3: Salvamento em CSV ───────────────────────────────────
        logger.info("Etapa 3/3 — Salvando dados em CSV...")
        caminho_csv = salvar_csv(cotacoes, nome_script="scraper")
        logger.info(f"CSV salvo em: {caminho_csv}")

        # ─── Resumo Final ─────────────────────────────────────────────────
        resumo = ResumoExecucao.gerar(cotacoes, fonte="scraping")
        logger.info("\n" + resumo)
        logger.info("=" * 50)
        logger.info("  EXECUÇÃO FINALIZADA COM SUCESSO ✅")
        logger.info("=" * 50)

        # ─── Notificação de Sucesso ───────────────────────────────────────
        enviar_email(
            assunto="Script Scraping — Cotações BTime",
            corpo=f"{resumo}\n\nCSV salvo em: {caminho_csv}",
            logger=logger,
            sucesso=True
        )

    except Exception as e:
        logger.error(f"ERRO CRÍTICO NA EXECUÇÃO: {e}")
        logger.info("=" * 50)
        logger.info("  EXECUÇÃO FINALIZADA COM ERRO ❌")
        logger.info("=" * 50)

        # ─── Notificação de Erro ──────────────────────────────────────────
        enviar_email(
            assunto="Script Scraping — Cotações BTime",
            corpo=(
                f"O script falhou após todas as tentativas.\n\n"
                f"Motivo do erro:\n{str(e)}\n\n"
                f"Verifique o arquivo de log para mais detalhes."
            ),
            logger=logger,
            sucesso=False
        )

if __name__ == "__main__":
    main()