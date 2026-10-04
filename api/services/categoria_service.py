from api.models.categoria.categoria import Categoria
from api.models.produto.produto import Produto
from api.repository.categoria_repository import CategoriaRepository
from api.validator.validator import Validator
from api.enums.status_categoria import StatusCategoria

class CategoriaService:

    def __init__(self):
        self.categoria_repository = CategoriaRepository()

    def adicionar_categoria(self, categoria: Categoria) -> dict:

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo Categoria"}

        if not Validator.validar_campos([categoria.status]):
            return {"erro": "Há campos vazios que precisam ser preenchidos."}
        
        if categoria.status not in [status.value for status in StatusCategoria]:
            return {"erro": "Status inválido. Apenas (ATIVO OU INATIVO)"}

        return self.categoria_repository.adicionar_categoria(categoria)

    def atualizar_categoria(self, categoria: Categoria) -> dict:
        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo Categoria"}

        if not Validator.validar_campos([categoria.status]):
            return {"erro": "Há campos vazios que precisam ser preenchidos."}
        
        if categoria.status not in [status.value for status in StatusCategoria]:
            return {"erro": "Status inválido. Apenas (ATIVO OU INATIVO)"}

        return self.categoria_repository.atualizar_categoria(categoria)

    def categorias_cadastradas(self) -> list[dict] | dict:
        return self.categoria_repository.listar_categorias()

    def buscar_categoria_id(self, categoria_id: int) -> dict | None:
        return self.categoria_repository.buscar_categoria_id(categoria_id)
 
    def deletar_categoria(self, categoria: Categoria) -> dict | bool:

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo Categoria"}

        return self.categoria_repository.deletar_categoria(categoria)

