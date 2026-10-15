


"""
Apenas um regra de negócio básica para o PDV
"""

class Desconto:

    # Desconto fixo de 15% para vendas acima de R$199.00
    @staticmethod
    def aplicar_desconto(valor_total: float) -> float:
        return round(valor_total * 0.15, 2) if valor_total >= 199.00 else 0.0