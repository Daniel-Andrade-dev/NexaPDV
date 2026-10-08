from api.enums.status_produto import StatusProduto
from api.enums.status_categoria import StatusCategoria
from api.enums.status_caixa import StatusCaixa
from api.enums.status_venda import StatusVenda


class ValidatorStatus:

    @staticmethod
    def status_produto(produto_status) -> bool:
        if produto_status == StatusProduto.INATIVO:
            return False
        return True
    
    @staticmethod
    def status_categoria(categoria_status) -> bool:
        if categoria_status == StatusCategoria.INATIVO:
            return False
        return True
    
    @staticmethod
    def status_caixa(caixa_status) -> bool:
        if caixa_status == StatusCaixa.FECHADO:
            return False
        return True
    
    @staticmethod
    def status_venda(venda_status) -> bool:
        if venda_status == StatusVenda.CANCELADA:
            return False
        if venda_status == StatusVenda.CONCLUIDA:
            return False
        return True
    