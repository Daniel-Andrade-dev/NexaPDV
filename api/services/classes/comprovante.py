from __future__ import annotations
from api.models.venda.venda import VendaFinalizada, VendaInicializada
import os
import textwrap
from datetime import datetime


LARGURA = 48       
COL_DESC = 22      
COL_QTD = 4        
COL_UNIT = 9       
COL_TOTAL = 10     
COL_VALOR = 16    

def _moeda(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Comprovante:

    def criar_arquivo_comprovante(self, venda_iniciada: VendaInicializada, comprovante: str) -> dict:
        path = "comprovantes"
        os.makedirs(path, exist_ok=True)

        arquivo = f"{path}/comprovante_{venda_iniciada.venda_id}.txt"

        with open(arquivo, "w", encoding="utf-8") as arq:
            arq.write(comprovante)

        return {
            "sucesso": True,
            "msg": "comprovante gerado com sucesso",
            "arquivo": arquivo,
        }

    @staticmethod
    def _linhas_item(item: dict) -> list[str]:
        nome = str(item["nome_produto"])
        qtd = item["venda_quantidade"]
        total = item["valor_total_produto"]
        unitario = total / qtd if qtd else 0.0 

        partes = textwrap.wrap(nome, width=COL_DESC, break_long_words=True) or [""]

        primeira = (
            f"{partes[0]:<{COL_DESC}} "
            f"{qtd:>{COL_QTD}g} "
            f"{_moeda(unitario):>{COL_UNIT}} "
            f"{_moeda(total):>{COL_TOTAL}}"
        )
        return [primeira, *partes[1:]]

    @staticmethod
    def _linha_valor(rotulo: str, valor: float) -> str:
        return f"{rotulo:<{LARGURA - COL_VALOR}}{'R$ ' + _moeda(valor):>{COL_VALOR}}"

    def modelo_comprovante(self, itens: list[dict], troco: float, venda_iniciada: VendaInicializada, venda_finalizada: VendaFinalizada) -> str:
        emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        dupla = "=" * LARGURA
        simples = "-" * LARGURA

        linhas = [
            dupla,
            "NexaPDV".center(LARGURA),
            "COMPROVANTE DE VENDA".center(LARGURA),
            dupla,
            f"Venda Nº: {venda_iniciada.venda_id}",
            f"Emissão:  {emissao}",
            "",
            f"{'Produto':<{COL_DESC}} {'Qtd':>{COL_QTD}} {'Unit.':>{COL_UNIT}} {'Total':>{COL_TOTAL}}",
            simples,
        ]

        for item in itens:
            linhas.extend(self._linhas_item(item))

        linhas += [
            simples,
            self._linha_valor("Valor total:", venda_finalizada.valor_total),
            self._linha_valor("Valor pago:", venda_finalizada.valor_pago),
            self._linha_valor("Troco:", troco),
            "",
            f"Forma de pagamento: {venda_finalizada.forma_pagamento}",
            "",
            dupla,
            "Obrigado pela preferência! Volte sempre!".center(LARGURA),
            dupla,
        ]

        return "\n".join(linhas) + "\n"