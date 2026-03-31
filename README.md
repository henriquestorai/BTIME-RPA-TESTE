# 🤖 BTime RPA Test — Cotação de Moedas

Dois scripts Python para coleta automatizada de cotações de moedas estrangeiras em BRL, desenvolvidos como parte do processo seletivo BTime.

---

## 📁 Estrutura do Projeto
```
btime-rpa-test/
├── config/
│   └── settings.py         # Parâmetros e configurações centralizadas
├── core/
│   ├── models.py            # Entidade Cotacao (domínio puro)
│   └── use_cases.py         # Regras de negócio e validações
├── infrastructure/
│   ├── scraper.py           # Coleta via Web Scraping (Google Finance)
│   ├── api_client.py        # Coleta via API (open.er-api.com)
│   └── csv_writer.py        # Salvamento dos dados em CSV
├── utils/
│   ├── logger.py            # Log em arquivo TXT + console
│   ├── retry.py             # Re-execução automática em caso de falha
│   └── emailer.py           # Notificação por e-mail (sucesso/erro)
├── logs/                    # Logs gerados automaticamente por execução
├── output/                  # CSVs gerados automaticamente por execução
├── main_scraper.py          # Ponto de entrada — Script 1 (Scraping)
├── main_api.py              # Ponto de entrada — Script 2 (API)
├── requirements.txt         # Dependências do projeto
└── .env                     # Variáveis de ambiente (não versionado)
```

---

## 🏗️ Arquitetura

O projeto adota **Clean Architecture**, separando o código em camadas independentes:

- **`core/`** — domínio puro, sem dependências externas. Define os modelos de dados e as regras de negócio.
- **`infrastructure/`** — implementações concretas de acesso externo (web, API, CSV).
- **`config/`** — centraliza todos os parâmetros e lê variáveis sensíveis do `.env`.
- **`utils/`** — utilitários reutilizáveis nos dois scripts (log, retry, e-mail).

---

## ⚙️ Pré-requisitos

- Python 3.10 ou superior
- Conta Gmail com [Senha de App](https://myaccount.google.com/apppasswords) configurada

---

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/btime-rpa-test.git
cd btime-rpa-test
```

### 2. Crie e ative o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```env
EMAIL_REMETENTE=seu_email@gmail.com
EMAIL_SENHA=sua_senha_de_app_16_caracteres
EMAIL_DESTINATARIO=seu_email@gmail.com
MAX_TENTATIVAS=3
TIMEOUT=10
```

> ⚠️ A `EMAIL_SENHA` deve ser uma **Senha de App** gerada em [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords), não a senha normal da conta Gmail.

---

## ▶️ Execução

### Script 1 — Web Scraping
```bash
python3 main_scraper.py
```
Coleta cotações do **Google Finance** via BeautifulSoup.

### Script 2 — API
```bash
python3 main_api.py
```
Coleta cotações da API pública **open.er-api.com** via requests.

---

## 📊 Moedas Coletadas

| Código | Moeda |
|--------|-------|
| USD | Dólar Americano |
| EUR | Euro |
| GBP | Libra Esterlina |
| ARS | Peso Argentino |

---

## 📂 Saídas Geradas

Cada execução gera automaticamente:

- **`output/`** — arquivo CSV com as cotações coletadas
```
moeda,valor_brl,fonte,coletado_em
USD,5.2655,scraping,30/03/2026 20:39:52
EUR,6.0314,scraping,30/03/2026 20:39:52
```

- **`logs/`** — arquivo TXT com o log completo da execução
```
[2026-03-30 20:39:48] [INFO] INICIANDO SCRIPT 1 — WEB SCRAPING
[2026-03-30 20:39:52] [INFO] EXECUÇÃO FINALIZADA COM SUCESSO ✅
```

- **E-mail automático** com status de sucesso ou detalhes do erro

---

## 🛡️ Boas Práticas de RPA Aplicadas

- **Retry automático** — até 3 tentativas com espera entre elas
- **Log estruturado** — arquivo TXT por execução com timestamp
- **Notificação por e-mail** — sucesso ou erro com motivo detalhado
- **Diretórios organizados** — `/output` para CSVs, `/logs` para logs
- **Variáveis de ambiente** — credenciais isoladas no `.env`
- **Tratamento de exceções** — falhas pontuais não derrubam o processo

---

## 📦 Dependências

attrs-26.1.0 
beautifulsoup4-4.14.3 
certifi-2026.2.25 
charset_normalizer-3.4.6 
h11-0.16.0 
idna-3.11 
outcome-1.3.0.post0 
packaging-26.0 
pysocks-1.7.1 
python-dotenv-1.2.2 
requests-2.33.1 
selenium-4.41.0 
sniffio-1.3.1 
sortedcontainers-2.4.0 
soupsieve-2.8.3 
trio-0.33.0 
trio-websocket-0.12.2 
typing-extensions-4.15.0 
urllib3-2.6.3 
webdriver-manager-4.0.2 
websocket-client-1.9.0 
wsproto-1.3.2