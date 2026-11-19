from api.models.produto.produto import Produto
from api.models.venda.venda import VendaIniciada


class Carrinho:

    def __init__(self):
        self.itens = []

    def adicionar_ao_carrinho(self, venda_iniciada: VendaIniciada, produto: Produto) -> list:
        itens = {
            "codigo_produto": produto.codigo_produto,
            "produto": produto.nome_produto,
            "preco_unitario_centavos": produto.preco_unitario_centavos,
            "quantidade_venda": venda_iniciada.quantidade_venda,
            "horario_iniciada": venda_iniciada.horario_iniciada,
            "data_iniciada": venda_iniciada.data_iniciada,
            "valor_total_produto": (
                venda_iniciada.quantidade_venda * produto.preco_unitario_centavos
            ),
            "status_venda": venda_iniciada.status
        }

        self.itens.append(itens) 
        return self.itens

    def limpar_carrinho(self) -> None:
        return self.itens.clear() 

    def obter_valor_total_carrinho(self) -> int:
        return sum(
            item['quantidade_venda'] * item['preco_unitario_centavos']
            for item in self.itens
        ) 