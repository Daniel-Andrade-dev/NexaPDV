from dataclasses import dataclass
from api.enums.status_categoria import StatusCategoria


@dataclass
class Categoria:
    categoria_id: int 
    nome: str 
    status: StatusCategoria = StatusCategoria.ATIVO