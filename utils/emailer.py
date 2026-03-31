# Envia e-mail de notificação ao final da execução

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config.settings import EMAIL_REMETENTE, EMAIL_SENHA, EMAIL_DESTINATARIO

def enviar_email(
    assunto: str,
    corpo: str,
    logger,
    sucesso: bool = True
) -> None:
    """
    Envia um e-mail de notificação via Gmail SMTP.

    Parâmetros:
        assunto  → assunto do e-mail
        corpo    → corpo do e-mail com detalhes da execução
        logger   → logger para registrar o envio
        sucesso  → define o prefixo do assunto [SUCESSO] ou [ERRO]
    """

    # Valida se as credenciais estão configuradas
    if not all([EMAIL_REMETENTE, EMAIL_SENHA, EMAIL_DESTINATARIO]):
        logger.warning("E-mail não configurado no .env — notificação ignorada.")
        return

    try:
        prefixo  = "✅ [SUCESSO]" if sucesso else "❌ [ERRO]"
        assunto_final = f"{prefixo} {assunto}"

        # Monta o e-mail
        mensagem = MIMEMultipart("alternative")
        mensagem["Subject"] = assunto_final
        mensagem["From"]    = EMAIL_REMETENTE
        mensagem["To"]      = EMAIL_DESTINATARIO

        # Corpo em texto puro
        corpo_completo = (
            f"{'='*50}\n"
            f"  NOTIFICAÇÃO DE EXECUÇÃO RPA\n"
            f"{'='*50}\n\n"
            f"Status   : {'SUCESSO ✅' if sucesso else 'ERRO ❌'}\n"
            f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
            f"Detalhes:\n{corpo}\n\n"
            f"{'='*50}\n"
            f"Mensagem gerada automaticamente pelo RPA BTime\n"
        )

        mensagem.attach(MIMEText(corpo_completo, "plain", "utf-8"))

        # Envia via Gmail SMTP com SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
            servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, mensagem.as_string())

        logger.info(f"E-mail enviado com sucesso para {EMAIL_DESTINATARIO}")

    except Exception as e:
        logger.error(f"Falha ao enviar e-mail: {e}")