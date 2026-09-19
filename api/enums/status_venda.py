from enum import Enum

class StatusVenda(str, Enum):
    ABERTA = "aberta"
    CONCLUIDA = "concluida"