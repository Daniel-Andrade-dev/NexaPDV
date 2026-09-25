from enum import Enum

class StatusVenda(str, Enum):
    ABERTA = "aberta"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluida"