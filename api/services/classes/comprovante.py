from api.models.venda.venda import VendaFinalizada, VendaInicializada
from datetime import datetime
import os

class Comprovante:

    def criar_arquivo_comprovante(self,venda_iniciada: VendaInicializada,comprovante: str) -> dict:
        path = "comprovantes"

        os.makedirs(path, exist_ok=True)

        arquivo = f"{path}/comprovante_{venda_iniciada.venda_id}.txt"

        with open(arquivo, "w", encoding="utf-8") as arq:
            arq.write(comprovante)

        return {
            "sucesso": True,
            "msg": "comprovante gerado com sucesso",
            "arquivo": arquivo
        }

    def modelo_comprovante(self, itens: list[dict], troco: float, venda_iniciada: VendaInicializada, venda_finalizada: VendaFinalizada) -> str:
        emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")

        produtos = ""

        for item in itens:
            produtos += (
                f"{item['nome_produto']:<20}"
                f"{item['venda_quantidade']:>4}   "
                f"R$ {item['valor_total_produto']:>8.2f}\n"
            )

        modelo = f"""
========================================
              NexaPDV
         COMPROVANTE DE VENDA
========================================

Venda Nº: {venda_iniciada.venda_id}

Produto              Qtd       Valor
----------------------------------------
{produtos}----------------------------------------

Valor total:               R$ {venda_finalizada.valor_total:.2f}
Valor pago:                R$ {venda_finalizada.valor_pago:.2f}
Troco:                     R$ {troco:.2f}

Forma de pagamento: {venda_finalizada.forma_pagamento}

----------------------------------------
Emissão do comprovante:
{emissao}

========================================
       Obrigado pela preferência!
             Volte sempre!
========================================
"""

        return modelo