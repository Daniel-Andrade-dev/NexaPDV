from api.repository.produto_repository import ProdutoRepository


class RelatorioProdutos:

    def __init__(self):
        self.produto_repository = ProdutoRepository()

    def total_estoque_produtos(self):
        return self.produto_repository.total_estoque()