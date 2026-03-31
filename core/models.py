# Define as entidades/modelos de dados do domínio
# Na Clean Architecture, o core não depende de nada externo
# É aqui que definimos como um dado de cotação deve se parecer

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cotacao:
    """
    Representa uma cotação de moeda estrangeira em relação ao BRL.
    
    Atributos:
        moeda       → código da moeda (ex: USD, EUR, GBP)
        valor       → valor da cotação em BRL
        fonte       → origem do dado (ex: 'scraping', 'api')
        coletado_em → data e hora da coleta
    """
    moeda       : str
    valor       : float
    fonte       : str
    coletado_em : str = ""

    def __post_init__(self):
        # Garante que a data/hora sempre seja preenchida automaticamente
        if not self.coletado_em:
            self.coletado_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self) -> dict:
        """Converte o objeto para dicionário — usado na geração do CSV"""
        return {
            "moeda"       : self.moeda,
            "valor_brl"   : f"{self.valor:.4f}",
            "fonte"       : self.fonte,
            "coletado_em" : self.coletado_em
        }