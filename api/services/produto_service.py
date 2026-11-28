from api.repository.produto_repository import ProdutoRepository
from api.models.produto.produto import Produto
from api.models.venda.venda import VendaIniciada
from api.validator.validator import Validator
from api.enums.status_produto import StatusProduto
from api.repository.categoria_repository import CategoriaRepository
from api.decorators.time_func import medir_tempo_execucao
from api.validator.validator_types import ValidatorTypes

class ProdutoService:

    def __init__(self):
        self.produto_repository = ProdutoRepository()
        self.categoria_repository = CategoriaRepository()
        self.validor_type = ValidatorTypes()

    @medir_tempo_execucao
    def cadastrar_produto(self, categoria_id: int, produto: Produto) -> dict:
        validator = self.validor_type.validar_valores_int(produto.preco_unitario_centavos)

        if not Validator.validar_campos([
            produto.nome_produto,
            produto.preco_unitario_centavos,
            produto.estoque,
            produto.status
        ]):
            return {
                "status": 400,
                "erro": "A campos vazios para serem preenchidos"
            }

        if isinstance(validator, dict) and "erro" in validator: return validator

        if not Validator.validar_negativos([produto.preco_unitario_centavos, produto.estoque]):
            return {
                "status": 400,
                "erro": "Informe valores acima de 0."
            }
        
        if produto.status not in [status.value for status in StatusProduto]:
            return {
                "status": 400,
                "erro": "Status inválido. Apenas (ativo ou inativo)"
            }

        categoria = categoria_id if categoria_id != [0, ""] else None
        
        return self.produto_repository.inserir_produto(categoria, produto)
    
    def atualizar_produto(self, categoria_id: int, produto: Produto) -> dict:

        buscar_produto = self.produto_repository.buscar_produto(produto.codigo_produto)
        validator = self.validor_type.validar_valores_int(produto.preco_unitario_centavos)

        if "erro" in buscar_produto:
            return buscar_produto

        if not Validator.validar_campos([
            produto.nome_produto,
            produto.preco_unitario_centavos,
            produto.estoque,
            produto.status
        ]):
            return {
                "status": 400,
                "erro": "A campos vazios para serem preenchidos"
            }

        if isinstance(validator, dict) and "erro" in validator: return validator
        
        if not Validator.validar_negativos([produto.preco_unitario_centavos, produto.estoque]):
            return {
                "status": 400,
                "erro": "Informe valores acima de 0."
            }
        
        if produto.status not in [status.value for status in StatusProduto]: 
            return {
                "status": 400,
                "erro": "Status inválido. Apenas (ativo ou inativo)"
            }

        categoria = categoria_id if categoria_id != [0, ""] else None
        
        return self.produto_repository.atualizar_produto(categoria, produto)

    def deletar_produto(self, codigo_produto: int) -> dict | bool:
        buscar_produto = self.produto_repository.buscar_produto(codigo_produto)

        if "erro" in buscar_produto:
            return buscar_produto
        
        return self.produto_repository.deletar_produto(buscar_produto['codigo'])

    def retorno_estoque(self, codigo_produto: int, venda_inicida: VendaIniciada) -> dict:
        buscar_produto = self.produto_repository.buscar_produto(codigo_produto)
        quantidade_retornada = int(buscar_produto['estoque']) + venda_inicida.quantidade_venda
        
        return self.produto_repository.retorno_estoque(codigo_produto, quantidade_retornada)
    
    def baixa_estoque(self, codigo_produto: int, venda_iniciada: VendaIniciada) -> dict:
        buscar_produto = self.produto_repository.buscar_produto(codigo_produto)
        novo_estoque = int(buscar_produto['estoque']) - venda_iniciada.quantidade_venda

        if venda_iniciada.quantidade_venda > buscar_produto['estoque'] or buscar_produto['estoque'] <= 0:
            return {
                "status": 400,
                "erro": "Não a estoque do produto escolhido"
            }

        return self.produto_repository.baixa_estoque(buscar_produto['codigo_produto'], novo_estoque)

    @medir_tempo_execucao
    def buscar_produto(self, codigo_produto: int) -> dict:
        produto = self.produto_repository.buscar_produto(codigo_produto)

        if produto is None: return {
            "status": 404,
            "erro": "Produto não encontrado"
        }

        return produto