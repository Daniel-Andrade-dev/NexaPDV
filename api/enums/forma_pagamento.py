from enum import Enum


class FormaPagamentos(str, Enum):
    CREDITO = "credito"
    DEBITO = "debito"
    DINHEIRO = "dinheiro"
    PIX = "pix"