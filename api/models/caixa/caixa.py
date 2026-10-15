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
    pagamento_id: int 
    caixa_id: int
    forma_pagamento: FormaPagamentos
    valor_total_venda: float
    valor_pago: float


@dataclass
class FechamentosCaixa:
    fechamento_id: int
    caixa_id: int
    valor_esperado: float
    valor_contado: float 
    diferenca: float 
    data_fechamento: datetime
    horario_fechamento: datetime


@dataclass
class Sangrias:
    sangria_id: int
    caixa_id: int 
    valor_retirado: float
    data_sangria: datetime
    horario_sangria: datetime
