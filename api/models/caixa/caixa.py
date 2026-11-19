from dataclasses import dataclass
from api.enums.status_caixa import StatusCaixa
from datetime import datetime
from api.enums.forma_pagamento import FormaPagamentos


@dataclass
class Caixa:
    caixa_id: int
    valor_inicial_centavos: int
    horario_aberto: datetime
    data_aberto: datetime
    status: StatusCaixa = StatusCaixa.FECHADO


@dataclass
class PagamentosCaixa:
    pagamento_id: int 
    caixa_id: int
    forma_pagamento: FormaPagamentos
    valor_total_venda_centavos: int
    valor_pago_centavos: int


@dataclass
class FechamentosCaixa:
    fechamento_id: int
    caixa_id: int
    valor_esperado_centavos: int
    valor_contado_centavos: int 
    diferenca_centavos: int 
    data_fechamento: datetime
    horario_fechamento: datetime


@dataclass
class Sangrias:
    sangria_id: int
    caixa_id: int 
    valor_retirado_centavos: int
    data_sangria: datetime
    horario_sangria: datetime
