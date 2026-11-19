



class VendaResponseFormat:

    @staticmethod
    def response_api_venda_iniciada(response_api: list[dict]) -> list[dict]: 
        return [
            {
                "sucesso": response['sucesso'],
                "itens":response['carrinho'],
                "msg": response['msg'],
                "venda":response['venda']
            }
            for response in response_api
        ]

    @staticmethod
    def response_api_carrinho(response_api: list[dict]) -> list[dict]:
        return [
            {
                "codigo_produto": response['codigo_produto'],
                "nome_produto": response['nome_produto'],
                "preco_unitario_centavos": response['preco_unitario_centavos'],
                "quantidade_venda": response['quantidade_venda'],
                "valor_total_produto": response['valor_total_produto_centavos']
            }
            for response in response_api
        ]

    @staticmethod
    def response_api_venda_finalizada(response_api: list[dict]) -> list[dict]:
        return [
            {
                "sucesso": True,
                "venda": response['venda'],
                "comprovante": response['msg_comprovante']['msg'],
                "resgistro_caixa": response['resultado_pagamento_caixa']['msg']
            }
            for response in response_api
        ]
    
class CarrinhoResponseFormat:

    @staticmethod
    def response_api_carrinho(response_api: list[dict]) -> list[dict]:
        return [
            {
                "codigo_produto": response['codigo_produto'],
                "nome_produto": response['produto'],
                "preco_unitario_centavos": response['preco_unitario_centavos'],
                "quantidade_venda": response['quantidade_venda'],
                "valor_total_produto_centavos": response['valor_total_produto']
            }
            for response in response_api
        ]