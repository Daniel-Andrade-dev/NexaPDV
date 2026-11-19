from api.models.categoria.categoria import Categoria
from api.models.produto.produto import Produto
from api.repository.categoria_repository import CategoriaRepository
from api.validator.validator import Validator
from api.enums.status_categoria import StatusCategoria

class CategoriaService:

    def __init__(self):
        self.categoria_repository = CategoriaRepository()

    def adicionar_categoria(self, categoria: Categoria) -> dict:

        if not Validator.validar_campos([categoria.status]):
            return {
                "status": 400,
                "erro": "Há campos vazios para serem preenchidos"
            } 
               
        if categoria.status not in [status.value for status in StatusCategoria]:
            return {
                "status": 400,
                "erro": "Status inválido. Apenas (ativa ou inativa)"
            }

        return self.categoria_repository.adicionar_categoria(categoria)

    def atualizar_categoria(self, categoria: Categoria) -> dict:    
        resultado_busca = self.buscar_categoria_id(categoria.categoria_id)

        if "erro" in resultado_busca:
            return resultado_busca
        
        if not Validator.validar_campos([categoria.status]):
            return {
                "status": 400,
                "erro": "Há campos vazios para serem preenchidos"
            } 
                
        if categoria.status not in [status.value for status in StatusCategoria]:
            return {
                "status": 400,
                "erro": "Status inválido. Apenas (ativa ou inativa)"
            }
        return self.categoria_repository.atualizar_categoria(categoria)

    def categorias_cadastradas(self) -> list[dict] | dict:
        return self.categoria_repository.listar_categorias()

    def buscar_categoria_id(self, categoria_id: int) -> dict | None:
        return self.categoria_repository.buscar_categoria_id(categoria_id)
 
    def deletar_categoria(self, categoria_id: int) -> dict | bool:
        resultado_busca = self.buscar_categoria_id(categoria_id)

        if "erro" in resultado_busca:
            return resultado_busca

        categoria = Categoria(
            categoria_id=resultado_busca['categoria_id'],
            nome=resultado_busca['nome'],
            status=resultado_busca['status']
        )

        return self.categoria_repository.deletar_categoria(categoria)

