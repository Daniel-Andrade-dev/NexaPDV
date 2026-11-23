


class ValidatorTypes:

    def validar_valores_int(self, valor) -> int | dict:
        return {
            "status": 400,
            "erro": f"O valor {valor} precisa ser um inteiro"
        } if not isinstance(valor, int) else valor