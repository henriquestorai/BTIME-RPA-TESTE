# config/settings.py
# Centraliza todos os parâmetros e configurações do projeto
# Lê as variáveis sensíveis do arquivo .env

import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# ─── Configurações de E-mail ───────────────────────────────────────────────
EMAIL_REMETENTE     = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA         = os.getenv("EMAIL_SENHA")
EMAIL_DESTINATARIO  = os.getenv("EMAIL_DESTINATARIO")

# ─── Configurações de Execução ────────────────────────────────────────────
MAX_TENTATIVAS = int(os.getenv("MAX_TENTATIVAS", 3))
TIMEOUT        = int(os.getenv("TIMEOUT", 10))

# ─── Moedas que serão coletadas ───────────────────────────────────────────
MOEDAS_ALVO = ["USD", "EUR", "GBP", "ARS", "BTC"]

# ─── Caminhos de Saída ────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
LOG_DIR     = os.path.join(BASE_DIR, "logs")

# ─── URLs ─────────────────────────────────────────────────────────────────
URL_SCRAPING = "https://wise.com/br/currency-converter/usd-to-brl-rate"
URL_API      = "https://open.er-api.com/v6/latest/BRL"