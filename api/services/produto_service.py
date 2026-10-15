from api.repository.produto_repository import ProdutoRepository
from api.models.produto.produto import Produto
from api.models.categoria.categoria import Categoria
from api.models.venda.venda import VendaInicializada
from api.validator.validator import Validator
from api.enums.status_produto import StatusProduto
from api.repository.categoria_repository import CategoriaRepository

class ProdutoService:

    def __init__(self, produto_repository=None):
        self.produto_repository = produto_repository or ProdutoRepository()
        self.categoria_repository = CategoriaRepository()

    def cadastrar_produto(self, categoria: Categoria, produto: Produto) -> dict:

        if not Validator.validar_campos([
            produto.nome_produto,
            produto.preco_unitario,
            produto.estoque,
            produto.status
        ]):
            return {"erro": "Preeche os campos para cadastrar o produto."}

        if not Validator.validar_negativos([produto.preco_unitario, produto.estoque]):
            return {"erro": "Informe valores acima de 0."}

        if produto.status not in [status.value for status in StatusProduto]:
            return {"erro": "Status inválido. Apenas (ATIVO OU INATIVO)."}

        resultado_produto = self.produto_repository.inserir_produto(categoria, produto)
        
        return resultado_produto
        
    def produtos_cadastrados(self) -> dict | list[dict]:
        return self.produto_repository.listar_produtos()

    def buscar_produto(self, codigo: int) -> dict:
        return self.produto_repository.buscar_produto(codigo)

    def atualizar_produto(self, categoria: Categoria, produto: Produto) -> dict:

        if not Validator.validar_campos([
            produto.nome_produto,
            produto.preco_unitario,
            produto.estoque,
            produto.status
        ]):
            return {"erro": "Preeche os campos para atualizar  o produto."}
        
        if not Validator.validar_negativos([produto.preco_unitario, produto.estoque]):
            return {"erro": "Informe valores acima de 0."}
        
        if produto.status not in [status.value for status in StatusProduto]:
            return {"erro": "Status inválido. Apenas (ATIVO OU INATIVO)"}
        
        return self.produto_repository.atualizar_produto(categoria, produto)

    def deletar_produto(self, produto: Produto) -> dict | bool:
        return self.produto_repository.deletar_produto(produto)

    def baixa_estoque(self, produto: Produto, venda: VendaInicializada) -> dict:
        return self.produto_repository.baixa_estoque(produto, venda)