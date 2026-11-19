from dataclasses import dataclass
from api.enums.status_produto import StatusProduto

@dataclass
class Produto:
    codigo_produto: int 
    categoria_id: int
    nome_produto: str 
    preco_unitario_centavos: int 
    estoque: int 
    status: StatusProduto = StatusProduto.ATIVO

