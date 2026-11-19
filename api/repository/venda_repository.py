from api.models.venda.venda import VendaIniciada, VendaFinalizada
from api.database.connections import ConnectionDataBase
from api.enums.status_venda import StatusVenda
from api.decorators.time_func import medir_tempo_execucao
from api.decorators.errors import verificar_erros_banco

class VendaRepository:

    @verificar_erros_banco
    def inserir_venda_iniciada(
        self, 
        itens: list[dict], 
        desconto_centavos: int, 
        subtotal_centavos: int, 
        valor_total_centavos: int
    )-> dict:
        sql = """
            INSERT INTO vendas_iniciadas (
                subtotal_centavos,
                desconto_centavos,
                valor_total_centavos,
                quantidade_venda,
                horario_iniciada,
                data_iniciada,
                status
            ) VALUES(?,?,?,?,?,?,?)
        """

        for item in itens:
            with ConnectionDataBase().connect_sql() as conn:
                cur = conn.execute(sql, (
                    subtotal_centavos,
                    desconto_centavos,
                    valor_total_centavos,
                    item.get('quantidade_venda', {}),
                    item.get('horario_iniciada', {}),
                    item.get('data_iniciada', {}),
                    item.get('status_venda', {})
                ))

                venda_iniciada_id = cur.lastrowid

                return {    
                    "venda_iniciada_id": venda_iniciada_id,
                    "iniciada_em": f"{item['data_iniciada']}T{item['horario_iniciada']}",
                    "status": item['status_venda'],
                    "desconto_centavos": desconto_centavos,
                    "subtotal_centavos": subtotal_centavos,
                    "valor_total_centavos": valor_total_centavos
                }

    @verificar_erros_banco
    def inserir_itens_venda(self, itens: list[dict], venda_iniciada_id: int) -> None:

        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                INSERT INTO itens_venda_iniciada (
                    venda_iniciada_id,
                    codigo_produto,
                    quantidade_venda,
                    preco_unitario_centavos,
                    valor_total_produto_centavos
                ) VALUES(?,?,?,?,?)
            """
            dados_itens = [
                (
                    venda_iniciada_id,
                    item['codigo_produto'],
                    item['quantidade_venda'],
                    item['preco_unitario_centavos'],
                    item['valor_total_produto']
                )
                for item in itens
            ]

            conn.executemany(sql, dados_itens)

    @verificar_erros_banco
    def finalizar_venda(
        self, 
        venda: VendaFinalizada, 
        valor_total_centavos: int, 
        troco_centavos: int, 
        horario, 
        data
    ) -> dict:
        
        sql = """
            INSERT INTO vendas_finalizadas (
                forma_pagamento,
                valor_total_centavos,
                valor_pago_centavos,
                status,
                horario_finalizada,
                data_finalizada
            ) VALUES(?,?,?,?,?,?)
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql, (
                venda.forma_pagamento,
                valor_total_centavos,
                venda.valor_pago_centavos,
                venda.status,
                horario,
                data
            ))

            venda_finalizada_id = cur.lastrowid

            return {
                "venda_finalizada_id": venda_finalizada_id,
                "finalizada_em": f"{data}T{horario}",
                "pagamento": {
                    "forma": venda.forma_pagamento,
                    "valor_pago_centavos": venda.valor_pago_centavos,
                    "troco_centavos": troco_centavos
                },
                "status_venda_finalizada": venda.status,
            }

    # A função e usada para exibir os produtos comprados no comprovante
    @verificar_erros_banco
    def buscar_itens_venda(self, venda_iniciada_id: int) -> dict | list[dict]:
        sql = """
            SELECT
                it.item_id,
                p.codigo_produto,
                p.nome_produto,
                p.preco_unitario_centavos,
                it.quantidade_venda,
                it.valor_total_produto_centavos
            FROM
                itens_venda_iniciada it
            LEFT JOIN 
                produtos p ON p.codigo_produto = it.codigo_produto
            INNER JOIN 
                vendas_iniciadas v ON v.venda_iniciada_id = it.venda_iniciada_id
            WHERE
                v.venda_iniciada_id = ?
        """

        with ConnectionDataBase().connect_sql() as conn:

            cur = conn.execute(sql, (venda_iniciada_id,))
            return [dict(item) for item in cur.fetchall()]

    @verificar_erros_banco
    def atualizar_status_venda(self, venda_iniciada_id: int) -> dict | bool:
        sql = """
            UPDATE
                vendas_iniciadas
            SET
                status = ?
            WHERE
                venda_iniciada_id = ?
        """
        
        with ConnectionDataBase().connect_sql() as conn:
            
            cur = conn.execute(sql,(
                StatusVenda.CONCLUIDA,
                venda_iniciada_id
            ))

            return {
                "sucesso": cur.rowcount > 0,
                "msg": "Status atualizado"
            }

    @verificar_erros_banco
    def cancelar_venda(self, venda_iniciada_id: int) -> dict:
        sql = """
            UPDATE
                vendas_iniciadas
            SET
                status = ?
            WHERE
                venda_iniciada_id = ?
        """

        with ConnectionDataBase().connect_sql() as conn:

            cur = conn.execute(sql, (
                StatusVenda.CANCELADA,
                venda_iniciada_id
            ))

            return {
                "sucesso": cur.rowcount > 0,
                "msg": "Venda cancelada com sucesso",
                "venda_iniciada_id": venda_iniciada_id,
                "status_venda": StatusVenda.CANCELADA,
            }