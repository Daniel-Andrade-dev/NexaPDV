from api.repository.relatorios_repository.relatorio_caixa_repository import RelatoriosCaixasRepository
from api.classes.convert_precos import ConvertPrecos


class RelatoriosCaixasService:

    def __init__(self):
        self.relatorios_caixas_repository = RelatoriosCaixasRepository()

    def tratar_dados_caixas(self, dados_retornados: list):
        return self.relatorios_caixas_repository.qtd_caixas_fechados(), {
            "qtd_caixas_cadastrados": len(dados_retornados),
        }, [{
            "caixa_id": dados['caixa_id'],
            "valor_inicial": ConvertPrecos().convert_centavos(dados['valor_inicial_centavos']),
            "aberto_em": (
                f"{dados['data_aberto']}T{dados['horario_aberto']}" 
                if dados['data_aberto'] and dados['horario_aberto'] != None
                else "O caixa não foi aberto ainda"
            ),
            "status": dados['status']
        } for dados in dados_retornados]

    def tratar_dados_pagamentos_caixas(self, dados_retornados: list):
        return [{
            "caixa_id": dados['caixa_id'],
            "pagamento_id": dados['pagamento_id'],
            "forma_pagamento": dados['forma_pagamento'],
            "valor_pago": ConvertPrecos().convert_centavos(dados['valor_pago_centavos']),
            "valor_total_venda": ConvertPrecos().convert_centavos(dados['valor_total_centavos']),
            "troco": ConvertPrecos().convert_centavos(dados['troco_centavos'])
        } for dados in dados_retornados]

    def caixas_cadastrados(self):
        dados = self.relatorios_caixas_repository.caixas_cadastrados()

        if dados != []:
            return self.tratar_dados_caixas(dados)
        return {"msg": "Não há caixas cadastrados no momento"}
    
    def pagamentos_caixas(self):
        dados = self.relatorios_caixas_repository.pagamentos_caixas()

        if dados != []:
            return self.tratar_dados_pagamentos_caixas(dados)
        return {"msg": "Não há pagamentos registrados no momento"}

    def buscar_caixa_id(self, caixa_id: int) -> dict | None:
        dados = self.relatorios_caixas_repository.buscar_caixas_id(caixa_id)

        if dados is None: return {
            "status": 404,
            "erro": f"Caixa {caixa_id} não encontrado"
        }
        return dados

    def buscar_pagamentos_id(self, pagamento_id: int):
        dados = self.relatorios_caixas_repository.buscar_pagamentos_id(pagamento_id)
        if dados is None: return {
            "status": 404,
            "erro": "Pagamento ID não encontrado"
        }
        return dados