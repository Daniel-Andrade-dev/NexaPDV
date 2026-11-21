from api.enums.status_caixa import StatusCaixa
from api.enums.status_venda import StatusVenda


class Validator:

    @staticmethod
    def validar_negativos(valores: list) -> bool:
        return all(v > 0 for v in valores)

    @staticmethod
    def validar_campos(valores: list) -> bool:
        return all(
            valor is not None and str(valor).strip() != ""
            for valor in valores
        )


class ValidatorVenda:

    def __init__(self):
        from api.services.relatorios_service.relatorio_venda_service import RelatorioVendasService

        self.relatorio_venda_iniciada = RelatorioVendasService()

    def validar_status(self, venda_iniciada_id: int):
        buscar_venda_iniciada = self.relatorio_venda_iniciada.buscar_vendas_iniciadas(venda_iniciada_id)

        if buscar_venda_iniciada['status'] == StatusVenda.CONCLUIDA: return {
            "status": 400,
            "erro": "Venda já está concluída, faça outra venda que esteja aberta"
        }
            
        if buscar_venda_iniciada['status'] == StatusVenda.CANCELADA: return {
            "status": 400,
            "erro": "Venda está cancelada, faça outra venda que esteja aberta"
        }

        return {"venda_iniciada": buscar_venda_iniciada}

    def validar_status_venda_cancelada(self, venda_iniciada_id: int):
        buscar_venda_iniciada = self.relatorio_venda_iniciada.buscar_vendas_iniciadas(venda_iniciada_id)

        if buscar_venda_iniciada['status'] == StatusVenda.CONCLUIDA: return {
            "status": 400,
            "erro": "Não é possível cancelar vendas concluídas"
        }

        if buscar_venda_iniciada['status'] == StatusVenda.CANCELADA: return {
            "status": 400,
            "erro": "A venda iniciada já está cancelada"
        }

        return {"venda_iniciada": buscar_venda_iniciada}

class ValidatorCaixa:

    def __init__(self):
        from api.services.caixa_service import CaixaService

        self.caixa_service = CaixaService()

    def validar_status(self, caixa_id: int):
        buscar_caixa = self.caixa_service.buscar_caixa_id(caixa_id)

        if buscar_caixa['status'] != StatusCaixa.ABERTO:
            return {
                "status": 400,
                "erro": f"Caixa {buscar_caixa['caixa_id']} está fechado"
            }

        return {"caixa": buscar_caixa}