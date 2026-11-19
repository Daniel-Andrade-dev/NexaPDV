
class ConvertPrecos:

    @staticmethod
    def convert_centavos(valor_centavos: int) -> float:
        return round(valor_centavos / 100, ndigits=2)

    @staticmethod
    def convert_format_reais(valor_centavos: int) -> str:
        convert = ConvertPrecos.convert_centavos(valor_centavos)
        return f"{convert:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")