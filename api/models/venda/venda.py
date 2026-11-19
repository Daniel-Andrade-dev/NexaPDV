from dataclasses import dataclass
from api.enums.forma_pagamento import FormaPagamentos
from api.enums.status_venda import StatusVenda
from datetime import datetime

@dataclass
class VendaIniciada:
    venda_iniciada_id: int 
    quantidade_venda: int
    horario_iniciada: datetime
    data_iniciada: datetime
    status: StatusVenda = StatusVenda.ABERTA

@dataclass
class VendaFinalizada:
    venda_finalizada_id: int 
    forma_pagamento: FormaPagamentos
    valor_total_centavos: int 
    valor_pago_centavos: int
    status: StatusVenda = StatusVenda.CONCLUIDA