from dataclasses import dataclass
from api.enums.status_produto import StatusProduto

@dataclass
class Produto:
    codigo: int 
    nome_produto: str 
    preco_unitario: float 
    estoque: int 
    categoria: str 
    status: StatusProduto = StatusProduto.ATIVO