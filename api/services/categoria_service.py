from api.models.categoria.categoria import Categoria
from api.repository.categoria_repository import CategoriaRepository
from api.validator.validator import Validator
from api.enums.status_categoria import StatusCategoria

class CategoriaService:

    def __init__(self):
        self.categoria_repository = CategoriaRepository()

    def adicionar_categoria(self, categoria: Categoria) -> dict:

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido"}

        if not Validator.validar_campos([categoria.status]):
            return {"erro": "Há campos vazios que precisam ser preenchidos."}
        
        if categoria.status not in [status.value for status in StatusCategoria]:
            return {"erro": "Status inválido. Apenas (ATIVO OU INATIVO)"}

        return self.categoria_repository.adicionar_categoria(categoria)

        
    def atualizar_categoria(self, categoria: Categoria):
        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido"}

        if not Validator.validar_campos([categoria.status]):
            return {"erro": "Há campos vazios que precisam ser preenchidos."}
        
        if categoria.status not in [status.value for status in StatusCategoria]:
            return {"erro": "Status inválido. Apenas (ATIVO OU INATIVO)"}

        return self.categoria_repository.atualizar_categoria(categoria)

    def categorias_cadastradas(self):
        return self.categoria_repository.listar_categorias()

    def buscar_categoria_id(self, categoria_id: int):
        return self.categoria_repository.buscar_categoria_id(categoria_id)

    def buscar_categoria_nome(self, nome: str):
        return self.categoria_repository.buscar_categoria_nome(nome)
    
    def deletar_categoria(self, categoria: Categoria):

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo categoria"}

        return self.categoria_repository.deletar_categoria(categoria)

