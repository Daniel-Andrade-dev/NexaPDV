from api.enums.status_caixa import StatusCaixa
from api.enums.status_venda import StatusVenda

# Melhorar validações genericas

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


class ValidatorVenda:

    def __init__(self):
        from api.services.caixa_service import CaixaService
        from api.services.relatorios_service.relatorio_venda_service import RelatorioVendasService

        self.caixa_service = CaixaService()
        self.relatorio_venda_iniciada = RelatorioVendasService()

    def validar_status(self, caixa_id: int, venda_iniciada_id: int):
        buscar_caixa = self.caixa_service.buscar_caixa_id(caixa_id)
        buscar_venda_iniciada = self.relatorio_venda_iniciada.buscar_vendas_iniciadas(venda_iniciada_id)

        if buscar_caixa['status'] != StatusCaixa.ABERTO:return {
            "status": 400,
            "erro": f"Caixa {caixa_id} está fechado, faça abertura para finalizar as vendas"
        }

        if buscar_venda_iniciada['status'] == StatusVenda.CONCLUIDA: return {
            "status": 409,
            "erro": "Venda já está concluída, faça outra venda que esteja aberta"
        }
            
        if buscar_venda_iniciada['status'] == StatusVenda.CANCELADA: return {
            "status": 409,
            "erro": "Venda está cancelada, faça outra venda que esteja aberta"
        }

        return {"caixa": buscar_caixa, "venda_iniciada": buscar_venda_iniciada}