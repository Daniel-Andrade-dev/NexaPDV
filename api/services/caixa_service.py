from api.models.caixa.caixa import Caixa, PagamentosCaixa, FechamentosCaixa, Sangrias
from api.repository.caixa_repository import CaixaRepository
from api.enums.status_caixa import StatusCaixa
from api.validator.validator import Validator

class CaixaService:
    def __init__(self):
        self.caixa_repository = CaixaRepository()

    def calcular_valor_esperado(self, caixa: Caixa):
        buscar_caixa = self.buscar_caixa_id(caixa.caixa_id)
        total_sangria = self.total_valor_sangria(caixa.caixa_id)
        total_pagamentos = self.caixa_repository.total_pagamentos_dinheiro(caixa.caixa_id)

        valor_esperado = (
            buscar_caixa['valor_inicial']
            + total_pagamentos['valor_total_dinheiro']
            - total_sangria['valor_total_sangria']
        )

        return valor_esperado
    
    def calcular_diferenca_caixa(self, valor_contado: float, valor_esperado: float) -> float:
        return round(valor_contado - valor_esperado, 2)
    
    def cadastrar_caixa(self, caixa: Caixa,) -> dict:
        return self.caixa_repository.cadastrar_caixa(caixa)

    def abertura_caixa(self, caixa: Caixa) -> dict | None:
        busca_caixa = self.buscar_caixa_id(caixa.caixa_id)

        if caixa.valor_inicial < 0:
            return {"erro": "Informe valores acima de 0 ou igual a 0"}

        if busca_caixa['status'] == StatusCaixa.ABERTO:
            return {"erro": f"Caixa {caixa.caixa_id} já está aberto. Tente novamente"}
        
        return self.caixa_repository.abertura_caixa(caixa)

    def fechamento_caixa(self, caixa: Caixa, fechamento_caixa: FechamentosCaixa):
        buscar_caixa = self.buscar_caixa_id(caixa.caixa_id)

        if buscar_caixa['status'] == StatusCaixa.FECHADO:
            return {"erro": "O caixa já está fechado"}

        if not Validator.validar_campos([fechamento_caixa.valor_contado]):
            return {"erro": "Digite o valor para realizar o fechamento do caixa"}

        valor_esperado = self.calcular_valor_esperado(caixa)
        diferenca = self.calcular_diferenca_caixa(fechamento_caixa.valor_contado, valor_esperado)

        fechamento_caixa_obj = FechamentosCaixa(
            fechamento_id=fechamento_caixa.fechamento_id,
            caixa_id=caixa.caixa_id,
            valor_esperado=valor_esperado,
            valor_contado=fechamento_caixa.valor_contado,
            diferenca=diferenca,
            data_fechamento=fechamento_caixa.data_fechamento,
            horario_fechamento=fechamento_caixa.horario_fechamento
        )
        return self.caixa_repository.fechamento_de_caixa(fechamento_caixa_obj, caixa)

    def inserir_pagamentos_caixa(self, caixa: Caixa, pagamentos_caixa: PagamentosCaixa, troco) -> dict:
        buscar_caixa = self.buscar_caixa_id(caixa.caixa_id)

        if buscar_caixa['status'] != StatusCaixa.ABERTO:
            return {"erro": "Não foi possível finalizar a venda caixa está fechado"}

        return self.caixa_repository.inserir_pagamentos_caixa(caixa, pagamentos_caixa, troco)
    
    def sangria_caixa(self, sangria: Sangrias, caixa: Caixa) -> dict:

        busca_caixa = self.buscar_caixa_id(caixa.caixa_id)
        busca_sangria = self.buscar_sangria_id(sangria.sangria_id)

        if busca_caixa['status'] != StatusCaixa.ABERTO:
            return {"erro": "Não é possível realizar sangria com caixa fechado"}

        if busca_sangria['valor_retirado'] > busca_caixa['valor_inicial']:
            return {"erro": "Não dinheiro suficiente para realizar a sangria. Verifique qual valor foi inserido"}
        
        return self.caixa_repository.realizar_sangria_caixa(sangria, caixa)
    
    def inserir_sangria(self, sangria: Sangrias) -> dict:

        if not Validator.validar_campos([sangria.valor_retirado]):
            return {"erro": "Digite o valor para realizar a sangria do caixa"}
        
        if not Validator.validar_negativos([sangria.valor_retirado]):
            return {"erro": "Informe valores acima de 0"}

        return self.caixa_repository.inserir_sangria_caixa(sangria)

    def buscar_caixa_id(self, caixa_id: int) -> dict | None:
        return self.caixa_repository.buscar_caixa(caixa_id)

    def buscar_pagamentos_dinheiro(self, pagamento_id: int) -> dict:
        return self.caixa_repository.buscar_pagamentos_dinheiro(pagamento_id)

    def buscar_sangria_id(self, sangria_id: int):
        return self.caixa_repository.buscar_sangria_id(sangria_id)

    def total_pagamento_dinheiro(self, caixa_id: int):
        return self.caixa_repository.total_pagamentos_dinheiro(caixa_id)
    
    def total_valor_sangria(self, caixa_id: int):
        return self.caixa_repository.valor_total_sangria(caixa_id)

    def listar_caixas(self) -> list[dict]:
        return self.caixa_repository.listar_caixas()

    def listar_pagamentos_caixa(self) -> dict:
        return self.caixa_repository.listar_pagamentos_caixa()
