class Desconto:

    def aplicar_desconto(self, valor_total: float) -> float:
        if valor_total >= 199.00:
            return valor_total * 0.15

        return 0.0


venda = {"valor_total_venda": 1000}

valor_total = venda["valor_total_venda"]

desconto = Desconto()
valor_desconto = desconto.aplicar_desconto(valor_total)

response = {
    "subtotal": valor_total,
    "desconto": round(valor_desconto, 2),
    "total": round(valor_total - valor_desconto, 2)
}

print(response)