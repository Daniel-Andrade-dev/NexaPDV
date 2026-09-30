from api.repository.produto_repository import ProdutoRepository


class RelatorioProdutos:

    def __init__(self):
        self.produto_repository = ProdutoRepository()

    def total_estoque_produtos(self) -> dict | float:
        return self.produto_repository.total_estoque()

    def total_produtos_ativos(self) -> dict:
        return self.produto_repository.total_produtos_ativos()