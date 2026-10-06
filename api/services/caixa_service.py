from api.models.caixa.caixa import Caixa
from api.repository.caixa_repository import CaixaRepository
from api.enums.status_caixa import StatusCaixa


class CaixaService:
    def __init__(self):
        self.caixa_repository = CaixaRepository()

    def cadastrar_caixa(self, caixa: Caixa,) -> dict:
        return self.caixa_repository.cadastrar_caixa(caixa)

    def abertura_caixa(self, caixa: Caixa) -> dict | None:
        busca_caixa = self.buscar_caixa_id(caixa.caixa_id)

        if caixa.valor_inicial < 0:
            return {"erro": "Informe valores acima de 0 ou igual a 0"}

        if busca_caixa['status'] == StatusCaixa.ABERTO:
            return {"erro": f"Caixa {caixa.caixa_id} já está aberto. Tente novamente"}
        
        return self.caixa_repository.abertura_caixa(caixa)

    def buscar_caixa_id(self, caixa_id: int) -> dict | None:
        return self.caixa_repository.buscar_caixa(caixa_id)

    def listar_caixas_abertos(self) -> list[dict]:
        return self.caixa_repository.listar_caixas_abertos()