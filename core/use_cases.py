# Contém as regras de negócio e orquestra o fluxo de execução
# Na Clean Architecture, os use_cases coordenam as ações sem conhecer
# detalhes de implementação (não sabe se é scraping ou API, não sabe como salva o CSV — só coordena o fluxo)

from typing import List
from core.models import Cotacao

class ProcessarCotacoes:
    """
    Caso de uso responsável por processar e validar as cotações coletadas.
    Recebe dados brutos e retorna objetos Cotacao validados e prontos para uso.
    """

    def executar(self, dados_brutos: List[dict], fonte: str) -> List[Cotacao]:
        """
        Processa uma lista de dados brutos e retorna cotações validadas.

        Parâmetros:
            dados_brutos → lista de dicionários com 'moeda' e 'valor'
            fonte        → origem dos dados ('scraping' ou 'api')

        Retorna:
            Lista de objetos Cotacao validados
        """
        cotacoes = []

        for dado in dados_brutos:
            try:
                cotacao = self._validar_e_criar(dado, fonte)
                if cotacao:
                    cotacoes.append(cotacao)
            except Exception as e:
                # Ignora registros inválidos sem derrubar o processo inteiro
                print(f"[AVISO] Registro ignorado — dado inválido: {dado} | Erro: {e}")

        return cotacoes

    def _validar_e_criar(self, dado: dict, fonte: str) -> Cotacao:
        """
        Valida um dado bruto e cria um objeto Cotacao.
        Lança exceção se o dado for inválido.
        """

        moeda = str(dado.get("moeda", "")).strip().upper()
        valor = dado.get("valor")

        # Validações de negócio
        if not moeda:
            raise ValueError("Campo 'moeda' está vazio ou ausente.")

        if valor is None:
            raise ValueError(f"Campo 'valor' ausente para moeda {moeda}.")

        valor_float = float(valor)

        if valor_float <= 0:
            raise ValueError(f"Valor inválido para {moeda}: {valor_float}")

        return Cotacao(moeda=moeda, valor=valor_float, fonte=fonte)


class ResumoExecucao:
    """
    Gera um resumo da execução para ser usado no log e no e-mail.
    """

    @staticmethod
    def gerar(cotacoes: List[Cotacao], fonte: str) -> str:
        """
        Monta um texto de resumo com os resultados da coleta.

        Parâmetros:
            cotacoes → lista de cotações coletadas
            fonte    → origem dos dados

        Retorna:
            String formatada com o resumo
        """
        if not cotacoes:
            return f"Nenhuma cotação coletada via {fonte}."

        linhas = [
            f"Fonte       : {fonte.upper()}",
            f"Total       : {len(cotacoes)} moeda(s) coletada(s)",
            f"─" * 40,
        ]

        for c in cotacoes:
            linhas.append(f"  {c.moeda:<6} → R$ {c.valor:.4f}  ({c.coletado_em})")

        return "\n".join(linhas)