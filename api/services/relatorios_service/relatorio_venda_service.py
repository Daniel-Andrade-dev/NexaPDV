from api.repository.relatorios_repository.relatorio_venda_repository import RelatorioVendasRepository
from api.classes.convert_precos import ConvertPrecos

class RelatorioVendasService:

    def __init__(self):
        self.relatorio_vendas = RelatorioVendasRepository()

    #Objetivo ser exibido para o front-end
    def tratar_dados_vendas_iniciadas(self, dados_retornados: list[dict]) -> list[dict]:
        return {
            "qtd_vendas_iniciadas": len(dados_retornados),
        }, [{
            "venda_iniciada_id": dados['venda_iniciada_id'],
            "desconto": ConvertPrecos().convert_centavos(dados['desconto_centavos']),
            "subtotal":  ConvertPrecos().convert_centavos(dados['subtotal_centavos']),
            "valor_total": ConvertPrecos().convert_centavos(dados['valor_total_centavos']),
            "quantidade_venda": dados['quantidade_venda'],
            "status": dados['status'],
            "iniciada_em": f"{dados['data_iniciada']}T{dados['horario_iniciada']}"
        } for dados in dados_retornados]
    
    #Objetivo ser exibido para o front-end
    def tratar_dados_vendas_finalizadas(self, dados_retornados: list[dict]) -> list[dict]:
        return {
            "qtd_vendas_finalizadas": len(dados_retornados),
        }, [{
            "venda_finalizada_id": dados['venda_finalizada_id'],
            "forma_pagamento": dados['forma_pagamento'],
            "valor_total": ConvertPrecos().convert_centavos(dados['valor_total_centavos']),
            "valor_pago": ConvertPrecos().convert_centavos(dados['valor_pago_centavos']),
            "status": dados['status'],
            "finalizada_em": f"{dados['data_finalizada']}T{dados['horario_finalizada']}"
        } for dados in dados_retornados]

    def vendas_iniciadas(self) -> list[dict]:
        dados = self.relatorio_vendas.vendas_iniciadas()
        if dados != []:
            return self.tratar_dados_vendas_iniciadas(dados)
        else:
            return {"msg": "Não há vendas iniciadas no momento"}

    def vendas_finalizadas(self) -> list[dict]:
        dados = self.relatorio_vendas.vendas_finalizadas()
        if dados != []:
            return self.tratar_dados_vendas_finalizadas(dados)
        else:
            return {"msg": "Não há vendas finalizadas no momento"}

    def buscar_vendas_iniciadas(self, venda_iniciada_id: int) -> dict | None:
        resultado_busca = self.relatorio_vendas.buscar_vendas_iniciadas(venda_iniciada_id)

        if resultado_busca is None: return {
            "status": 404,
            "erro": "Venda não encontrada"
        }
        else:
            return resultado_busca

    def buscar_vendas_finalizadas(self, venda_finalizada_id: int) -> dict | None:
        resultado_busca = self.relatorio_vendas.buscar_vendas_finalizadas(venda_finalizada_id)

        if resultado_busca is None: return {
            "status": 404,
            "erro": "Venda não encontrada"
        }
        else:
            return resultado_busca