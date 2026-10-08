from api.models.caixa.caixa import Caixa, PagamentosCaixa, TotalCaixa
from api.repository.caixa_repository import CaixaRepository
from api.enums.status_caixa import StatusCaixa

class CaixaService:
    def __init__(self):
        self.caixa_repository = CaixaRepository()

    def calcular_fechamento_caixa(self):
        pass 

    def calcular_diferenca_caixa(self):
        pass 
    
    def cadastrar_caixa(self, caixa: Caixa,) -> dict:
        return self.caixa_repository.cadastrar_caixa(caixa)

    def abertura_caixa(self, caixa: Caixa) -> dict | None:
        busca_caixa = self.buscar_caixa_id(caixa.caixa_id)

        if caixa.valor_inicial < 0:
            return {"erro": "Informe valores acima de 0 ou igual a 0"}

        if busca_caixa['status'] == StatusCaixa.ABERTO:
            return {"erro": f"Caixa {caixa.caixa_id} já está aberto. Tente novamente"}
        
        return self.caixa_repository.abertura_caixa(caixa)

    def fechamento_caixa(self, caixa: Caixa, total_caixa: TotalCaixa):
        pass

    def inserir_pagamentos_caixa(self, caixa: Caixa, pagamentos_caixa: PagamentosCaixa, troco) -> dict:
        buscar_caixa = self.buscar_caixa_id(caixa.caixa_id)

        if not buscar_caixa:
            return {"erro": "Caixa não encontrado para finalizar a venda"}
        
        if buscar_caixa['status'] != StatusCaixa.ABERTO:
            return {"erro": "Não foi possível finalizar a venda caixa está fechado"}

        return self.caixa_repository.inserir_pagamentos_caixa(caixa, pagamentos_caixa, troco)

    def buscar_caixa_id(self, caixa_id: int) -> dict | None:
        return self.caixa_repository.buscar_caixa(caixa_id)

    def listar_caixas_abertos(self) -> list[dict]:
        return self.caixa_repository.listar_caixas_abertos()

    def listar_caixas_fechados(self) -> list[dict]:
        return self.caixa_repository.listar_caixas_fechados()

    def listar_pagamentos_caixa(self) -> dict:
        return self.caixa_repository.listar_pagamentos_caixa()

    def sangria_caixa(self, valor_retirado, caixa: Caixa) -> dict:

        busca_caixa = self.buscar_caixa_id(caixa.caixa_id)

        if valor_retirado > busca_caixa['valor_inicial']:
            return {"erro": f"Não a dinheiro suficiente no caixa {busca_caixa['caixa_id']}"}

        if busca_caixa['status'] != StatusCaixa.ABERTO:
            return {"erro": "Não é possível realizar sangria com caixa fechado"}

        return self.caixa_repository.realizar_sangria_caixa(valor_retirado, caixa)