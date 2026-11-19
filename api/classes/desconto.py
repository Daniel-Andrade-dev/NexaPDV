


"""
Apenas um regra de negócio básica para o PDV
"""

class Desconto:

    # Desconto fixo de 15% para vendas acima de R$150.00 (15000 centavos)
    @staticmethod
    def aplicar_desconto(subtotal_centavos: int) -> int:
        return subtotal_centavos * 15 // 100 if subtotal_centavos >= 15000 else 0