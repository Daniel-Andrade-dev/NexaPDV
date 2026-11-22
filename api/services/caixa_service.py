from api.models.caixa.caixa import Caixa, PagamentosCaixa, FechamentosCaixa, Sangrias
from api.repository.caixa_repository import CaixaRepository
from api.enums.status_caixa import StatusCaixa
from api.validator.validator import Validator
from api.validator.validator import ValidatorCaixa
from datetime import datetime

class CaixaService:
    
    def __init__(self):
        self.caixa_repository = CaixaRepository()
        self.validator_caixa = ValidatorCaixa()

    def calcular_valor_esperado(self, caixa: Caixa) -> int:
        valor_inicial = self.buscar_caixa_id(caixa.caixa_id)
        total_sangria = self.caixa_repository.valor_total_sangria(caixa.caixa_id)
        total_pagamentos = self.caixa_repository.total_pagamentos_dinheiro(caixa.caixa_id)

        return (
            valor_inicial['valor_inicial_centavos']
            + total_pagamentos['valor_total_dinheiro_centavos']
            - total_sangria['valor_total_sangria_centavos']
        )

    def calcular_diferenca_caixa(self, valor_contado_centavos: int, valor_esperado_centavos: int) -> int:
        return valor_contado_centavos - valor_esperado_centavos
    
    def cadastrar_caixa(self, caixa: Caixa) -> dict:
        return self.caixa_repository.cadastrar_caixa(caixa)

    def abertura_caixa(self, caixa_id: int, valor_inicial_centavos: int) -> dict | None:
        status_caixa = self.validator_caixa.validar_status_abertura_caixa(caixa_id)

        if "erro" in status_caixa: return status_caixa

        if valor_inicial_centavos < 0: return {
            "status": 400,
            "erro": "Informe valores acima de 0 ou igual a 0"
        }

        caixa = Caixa(
            caixa_id=status_caixa['caixa']['caixa_id'],
            valor_inicial_centavos=valor_inicial_centavos,
            horario_aberto=datetime.now().strftime("%H:%M"),
            data_aberto=datetime.now().strftime("%Y-%m-%d"),
            status=StatusCaixa.ABERTO
        )

        return self.caixa_repository.abertura_caixa(caixa)

    def fechamento_caixa(self, caixa_id: int, fechamento_caixa: FechamentosCaixa) -> dict | None:
        status_caixa = self.validator_caixa.validar_status_fechamento_caixa(caixa_id)

        if "erro" in status_caixa:  return status_caixa
        
        if not Validator.validar_campos([fechamento_caixa.valor_contado_centavos]):
            return {
                "status": 400,
                "erro": "Digite o valor para realizar o fechamento do caixa"
            }

        caixa = Caixa(
            caixa_id=status_caixa['caixa']['caixa_id'],
            valor_inicial_centavos=status_caixa['caixa']['valor_inicial_centavos'],
            horario_aberto=status_caixa['caixa']['horario_aberto'],
            data_aberto=status_caixa['caixa']['data_aberto'],
            status=StatusCaixa.FECHADO
        )

        valor_esperado_centavos = self.calcular_valor_esperado(caixa)

        diferenca_centavos = self.calcular_diferenca_caixa(
            fechamento_caixa.valor_contado_centavos,
            valor_esperado_centavos
        )

        fechamento_caixa_obj = FechamentosCaixa(
            fechamento_id=fechamento_caixa.fechamento_id,
            caixa_id=status_caixa['caixa']['caixa_id'],
            valor_esperado_centavos=valor_esperado_centavos,
            valor_contado_centavos=fechamento_caixa.valor_contado_centavos,
            diferenca_centavos=diferenca_centavos,
            data_fechamento=fechamento_caixa.data_fechamento,
            horario_fechamento=fechamento_caixa.horario_fechamento
        )

        return self.caixa_repository.fechamento_de_caixa(fechamento_caixa_obj, caixa)

    def inserir_pagamentos_caixa(self, caixa: Caixa, pagamentos_caixa: PagamentosCaixa, troco_centavos) -> dict:
        return self.caixa_repository.inserir_pagamentos_caixa(caixa, pagamentos_caixa, troco_centavos)
    
    def sangria_caixa(self, sangria_id: int, caixa_id: int) -> dict:

        busca_caixa = self.buscar_caixa_id(caixa_id)
        busca_sangria = self.buscar_sangria_id(sangria_id)
        
        if busca_caixa['status'] != StatusCaixa.ABERTO:
            return {
                "status": 400,
                "erro": "Não é possível realizar a sangria com caixa fechado"
            }

        if busca_sangria['valor_retirado_centavos'] > busca_caixa['valor_inicial_centavos']:
            return {
                "status": 400,
                "erro": "Não dinheiro suficiente para realizar a sangria. Verifique qual valor foi inserido"
            }

        sangria = Sangrias(
            sangria_id=busca_sangria['sangria_id'],
            caixa_id=busca_caixa['caixa_id'],
            valor_retirado_centavos=busca_sangria['valor_retirado_centavos'],
            data_sangria=busca_sangria['data_sangria'],
            horario_sangria=busca_sangria['horario_sangria']
        )

        caixa = Caixa(
            caixa_id=busca_caixa['caixa_id'],
            valor_inicial_centavos=busca_caixa['valor_inicial_centavos'],
            horario_aberto=busca_caixa['horario_aberto'],
            data_aberto=busca_caixa['data_aberto'],
            status=StatusCaixa.ABERTO
        )

        return self.caixa_repository.realizar_sangria_caixa(sangria, caixa)
    
    def inserir_sangria(self, caixa_id: int, sangria: Sangrias) -> dict:

        busca_caixa = self.buscar_caixa_id(caixa_id)

        if "erro" in busca_caixa:
            return busca_caixa

        if busca_caixa['status'] != StatusCaixa.ABERTO:
            return {
                "status": 400,
                "erro": "Não é possível inserir a sangria com caixa fechado"
            }
        
        if not Validator.validar_campos([sangria.valor_retirado_centavos]):
            return {"erro": "Digite o valor para realizar a sangria do caixa"}
        
        if not Validator.validar_negativos([sangria.valor_retirado_centavos]):
            return {"erro": "Informe valores acima de 0"}

        return self.caixa_repository.inserir_sangria_caixa(caixa_id, sangria)

    def buscar_caixa_id(self, caixa_id: int) -> dict | None:
        resultado_repository = self.caixa_repository.buscar_caixa_id(caixa_id)
        return resultado_repository

    def buscar_sangria_id(self, sangria_id: int):
        return self.caixa_repository.buscar_sangria_id(sangria_id)