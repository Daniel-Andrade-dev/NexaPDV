def calcular_valor_esperado(caixa_id):
        return list(caixa_id)
        buscar_caixa = self.buscar_caixa_id(id)
        total_sangria = self.total_valor_sangria(id)
        total_pagamentos = self.caixa_repository.total_pagamentos_dinheiro(d)

        valor_esperado = (
            buscar_caixa['valor_inicial']
            + total_pagamentos['valor_total_dinheiro']
            - total_sangria['valor_total_sangria']
        )

        return valor_esperado






print(calcular_valor_esperado(caixa_id=1))