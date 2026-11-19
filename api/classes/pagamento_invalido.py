from api.enums.forma_pagamento import FormaPagamentos


class PagamentoInvalido:

    @staticmethod
    def verificar_pagamento_invalido(forma_pagamento) -> dict | bool:

        if forma_pagamento == FormaPagamentos.PIX: return {
            "status": 400,
            "erro": "Apenas pagamentos crédito, débito e dinheiro são permitidos"
        }

        if forma_pagamento not in [forma.value for forma in FormaPagamentos]: return {
            "status": 400,
            "erro": "Forma de pagamento inválida"
        }

        return True
    
    
    @staticmethod
    def verificar_pagamento_pix_invalido(forma_pagamento_pix) -> dict | bool:

        if forma_pagamento_pix != FormaPagamentos.PIX:return {
            "status": 400,
            "erro": "Apenas pagamento em pix e permitido"
        }

        return True
  