


class Validator:

    @staticmethod
    def validar_negativos(valores: list) -> bool:
        for valor in valores:
            if valor <= 0: 
                return False 
        return True 

    @staticmethod
    def validar_campos(valores: list) -> bool:
        for valor in valores: 
            if not valor or str(valor) == "":
                return False 
        return True
