from enum import Enum

class StatusCaixa(str, Enum):
    ABERTO = "aberto"
    FECHADO = "fechado"