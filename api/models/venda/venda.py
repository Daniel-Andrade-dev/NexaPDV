from dataclasses import dataclass
from api.enums.forma_pagamento import FormaPagamentos
from api.enums.status_venda import StatusVenda
from datetime import datetime

@dataclass
class VendaInicializada:
    venda_id: int 
    venda_quantidade: int
    horario_inicializada: datetime
    data_inicializada: datetime
    status: StatusVenda = StatusVenda.ABERTA

@dataclass
class VendaFinalizada:
    id_venda: int 
    forma_pagamento: FormaPagamentos
    valor_total: float 
    valor_pago: float
    status: StatusVenda = StatusVenda.CONCLUIDA