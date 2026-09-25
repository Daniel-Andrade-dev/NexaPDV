from enum import Enum

class StatusCategoria(str, Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"

class CategoriaDefault(str, Enum):
    DIVERSOS = "diversos"