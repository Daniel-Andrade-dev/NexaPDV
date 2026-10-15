from dataclasses import dataclass
from api.enums.status_produto import StatusProduto

@dataclass
class Produto:
    codigo: int 
    categoria_id: int
    nome_produto: str 
    preco_unitario: float 
    estoque: int 
    status: StatusProduto = StatusProduto.ATIVO