from dataclasses import dataclass
from api.enums.status_caixa import StatusCaixa
from datetime import datetime

@dataclass
class Caixa:
    caixa_id: int
    valor_inicial: float
    horario_aberto: datetime
    data_aberto: datetime
    status: StatusCaixa = StatusCaixa.FECHADO

