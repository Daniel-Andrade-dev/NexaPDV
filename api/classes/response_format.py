from datetime import datetime



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


class ComprovanteResponseFormat:

    @staticmethod
    def response_api_comprovante(response_api: dict[list, str]):
        MSG_FIXA = "Obrigado pela preferência! Volte sempre"

        if 'erro' in response_api: return response_api
        
        pagamento, venda, itens = response_api['pagamento'], response_api['venda'], response_api['itens']

        return {
            "comprovante": {
                "venda_id": venda['venda_iniciada_id'],
                "emitido_em": datetime.now().strftime("%d/%m/%Y às %H:%M"),
                "itens": [
                    {
                        "produto": item['nome_produto'],
                        "preco_unitario_centavos": item['preco_unitario_centavos'],
                        "quantidade_venda": item['quantidade_venda'],
                        "valor_total_produto_centavos": item['valor_total_produto_centavos']
                    } 
                    for item in itens
                ],
                "pagamento": {
                    "forma_pagamento": pagamento['forma_pagamento'], 
                    "subtotal_centavos": venda['subtotal_centavos'],
                    "desconto_centavos": venda['desconto_centavos'],
                    "valor_total_centavos": venda['valor_total_centavos'],
                    "valor_pago_centavos": pagamento['valor_pago_centavos']      
                },
                "troco_centavos": pagamento['troco_centavos'],
                "msg": MSG_FIXA
            }
        }

