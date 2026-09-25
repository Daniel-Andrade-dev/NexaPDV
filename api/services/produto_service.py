from api.repository.produto_repository import ProdutoRepository
from api.models.produto.produto import Produto
from api.models.venda.venda import VendaInicializada
from api.validator.validator import Validator
from api.enums.status_produto import StatusProduto

class ProdutoService:

    def __init__(self, produto_repository=None):
        self.produto_repository = produto_repository or ProdutoRepository()

    def cadastrar_produto(self, produto: Produto) -> dict:

        if not isinstance(produto, Produto): 
            return {
                "erro": "Objeto inválido. Esperado tipo Produto."
            }

        if not Validator.validar_campos([
            produto.nome_produto,
            produto.preco_unitario,
            produto.estoque,
            produto.status
        ]):
            return {
                "erro": "Há campos vazios que precisam ser preenchidos."
            }

        if not Validator.validar_negativos([produto.preco_unitario, produto.estoque]):
            return {
                "erro": "Informe valores acima de 0 para preço e estoque."
            }

        if produto.status not in [status.value for status in StatusProduto]:
            return {
                "erro": "Status inválido. Apenas (ATIVO OU INATIVO)"
            }
        
        return self.produto_repository.inserir_produto(produto=produto)

    def produtos_cadastrados(self):
        return self.produto_repository.listar_produtos()

    def buscar_produto(self, codigo: int) -> dict:
        return self.produto_repository.buscar_produto(codigo)

    def atualizar_produto(self, produto: Produto) -> dict:

        if not isinstance(produto, Produto):
            return {
                "erro": "Objeto inválido. Esperado tipo Produto."
            }

        if not Validator.validar_campos([
            produto.nome_produto,
            produto.preco_unitario,
            produto.estoque,
            produto.status
        ]):
            return {
                "erro": "Há campos vazios que precisam ser preenchidos."
            }
        
        if not Validator.validar_negativos([produto.preco_unitario, produto.estoque]):
            return {
                "erro": "Informe valores acima de 0 para preço e estoque."
            }
        
        if produto.status not in [status.value for status in StatusProduto]:
            return {
                "erro": "Status inválido. Apenas (ATIVO OU INATIVO)"
            }
        

        return self.produto_repository.atualizar_produto(produto=produto)

    def deletar_produto(self, produto: Produto):
        
        if not isinstance(produto, Produto):
            return {
                "erro": "Objeto inválido. Esperado tipo Produto."
            }

        return self.produto_repository.deletar_produto(produto)

    def baixa_estoque(self, produto: Produto, venda: VendaInicializada) -> dict:
        return self.produto_repository.baixa_estoque(produto, venda)