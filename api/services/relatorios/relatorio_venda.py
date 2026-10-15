from api.repository.venda_repository import VendaRepository

class RelatorioVendas:

    def __init__(self):
        self.venda_repository = VendaRepository()

    def listar_vendas_iniciadas(self) -> list[dict]:
        return self.venda_repository.listar_vendas_iniciadas()

    def listar_vendas_finalizadas(self) -> list[dict] | dict:
        return self.venda_repository.listar_vendas_finalizadas()

    def vendas_canceladas(self) -> list[dict]:
        return self.venda_repository.listar_vendas_canceladas()

    def ticket_medio_vendas_finalizadas(self) -> dict:
        return self.venda_repository.ticket_medio_vendas_finalizadas()

    def total_vendas_canceladas(self) -> dict:
        return self.venda_repository.total_vendas_canceladas()

    def total_vendas_finalizadas(self) -> dict:
        return self.venda_repository.total_vendas_finalizadas()

    def total_vendas_iniciadas(self) -> dict: 
        return self.venda_repository.total_vendas_iniciadas()