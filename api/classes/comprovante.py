
from datetime import datetime
from pathlib import Path

from api.models.venda.venda import VendaFinalizada, VendaIniciada
from api.classes.convert_precos import ConvertPrecos

LARGURA = 48


class Comprovante:

    def criar_arquivo_comprovante(
        self,
        venda_iniciada: VendaIniciada,
        comprovante: str,
    ) -> dict:
        pasta = Path("comprovantes")
        pasta.mkdir(exist_ok=True)

        arquivo = pasta / f"comprovante_{venda_iniciada.venda_iniciada_id}.txt"
        arquivo.write_text(comprovante, encoding="utf-8")

        return {
            "sucesso": True,
            "msg": "Comprovante gerado com sucesso.",
            "arquivo": str(arquivo),
        }

    def modelo_comprovante(
        self,
        itens: list[dict],
        troco_centavos: int,
        subtotal_centavos: int,
        desconto_centavos: int,
        valor_total_centavos: int,
        venda_iniciada: VendaIniciada,
        venda_finalizada: VendaFinalizada,
    ) -> str:

        def separador() -> str:
            return "-" * LARGURA

        def valor_linha(nome: str, centavos: int) -> str:
            return f"{nome:<32}{ConvertPrecos.convert_format_reais(centavos):>16}"

        linhas = [
            "=" * LARGURA,
            "NexaPDV".center(LARGURA),
            "COMPROVANTE DE VENDA".center(LARGURA),
            "=" * LARGURA,
            f"Venda Nº: {venda_iniciada.venda_iniciada_id}",
            f"Emissão: {datetime.now():%d/%m/%Y às %H:%M}",
            separador(),
            f"{'Itens':<22} {'Qtd':>4} {'Unit.':>8} {'Total':>11}",
            separador(),
        ]


        for item in itens:
            nome = str(item["nome_produto"])
            quantidade = item["quantidade_venda"]
            total_centavos = item["valor_total_produto_centavos"]
            preco_unitario_centavos = item['preco_unitario_centavos']

            linhas.append(
                f"{nome[:22]:<22} "
                f"{quantidade:>4} "
                f"{ConvertPrecos.convert_format_reais(preco_unitario_centavos):>8}"
                f"{ConvertPrecos.convert_format_reais(total_centavos):>11}"
            )

        if not itens:
            linhas.append("Nenhum produto foi registrado.")

        linhas.extend([
            separador(),
            valor_linha("Subtotal:", subtotal_centavos),
            valor_linha("Desconto:", desconto_centavos),
            separador(),
            valor_linha("VALOR TOTAL:", valor_total_centavos),
            valor_linha("VALOR PAGO:", venda_finalizada.valor_pago_centavos),
            valor_linha("Troco:", troco_centavos),
            separador(),
            f"Forma de pagamento: {venda_finalizada.forma_pagamento}",
            "=" * LARGURA,
            "Obrigado pela preferência!".center(LARGURA),
            "Volte sempre!".center(LARGURA),
            "=" * LARGURA,
        ])

        return "\n".join(linhas) + "\n"
