from api.repository.venda_repository import VendaRepository

class RelatorioVendas:

    def __init__(self):
        self.venda_repository = VendaRepository()

    def listar_vendas_iniciadas(self) -> list[dict]:
        return self.venda_repository.listar_vendas_iniciadas()

    def listar_vendas_finalizas(self):
        return self.venda_repository.listar_vendas_finalizas()

