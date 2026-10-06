from dataclasses import dataclass
from api.enums.status_caixa import StatusCaixa
from datetime import datetime
from api.enums.forma_pagamento import FormaPagamentos


@dataclass
class Caixa:
    caixa_id: int
    valor_inicial: float
    horario_aberto: datetime
    data_aberto: datetime
    status: StatusCaixa = StatusCaixa.FECHADO


@dataclass
class PagamentosCaixa:
    id: int 
    caixa_id: int
    forma_pagamento: FormaPagamentos
    valor_pago: float


@dataclass
class TotalCaixa:
    id: int
    caixa_id: int 
    valor_total_venda: float 
    valor_esperado: float
    valor_contado: float 
    diferenca: float 
    data_fechamento: datetime
    horario_fechamento: datetime
