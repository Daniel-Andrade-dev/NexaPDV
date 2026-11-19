from api.database.connections import ConnectionDataBase
from api.decorators.errors import verificar_erros_banco
from datetime import datetime



class RelatorioVendasRepository:

    @verificar_erros_banco
    def vendas_iniciadas(self) -> list[dict]:

        sql = """
            SELECT
                venda_iniciada_id,
                subtotal_centavos,
                desconto_centavos,
                valor_total_centavos,
                quantidade_venda,
                horario_iniciada,
                data_iniciada,
                status
            FROM 
                vendas_iniciadas
            ORDER BY venda_iniciada_id ASC
        """


        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql)

            return [
                dict(row)
                for row in cur.fetchall()
            ]

    @verificar_erros_banco
    def vendas_finalizadas(self) -> list[dict]:

        sql = """
            SELECT
                venda_finalizada_id,
                forma_pagamento,
                valor_total_centavos,
                valor_pago_centavos,
                status,
                horario_finalizada,
                data_finalizada
            FROM
                vendas_finalizadas
            ORDER BY venda_finalizada_id ASC
        """
        
        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql)

            return [
                dict(row)
                for row in cur.fetchall()
            ]

    @verificar_erros_banco
    def buscar_vendas_iniciadas(self, venda_iniciada_id: int) -> dict | None:

        sql = """
            SELECT
                venda_iniciada_id,
                subtotal_centavos,
                desconto_centavos,
                valor_total_centavos,
                quantidade_venda,
                horario_iniciada,
                data_iniciada,
                status
            FROM 
                vendas_iniciadas
            WHERE
                venda_iniciada_id = ?
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql, (venda_iniciada_id,))
            venda = cur.fetchone()
            return dict(venda) if venda is not None else None 


    @verificar_erros_banco
    def buscar_vendas_finalizadas(self, venda_finalizada_id: int) -> dict | None:

        sql = """
            SELECT
                venda_finalizada_id,
                forma_pagamento,
                valor_total_centavos,
                valor_pago_centavos,
                status,
                horario_finalizada,
                data_finalizada
            FROM
                vendas_finalizadas
            WHERE
                venda_finalizada_id = ?
        """    

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql, (venda_finalizada_id,))
            venda = cur.fetchone()
            return dict(venda) if venda is not None else None 
