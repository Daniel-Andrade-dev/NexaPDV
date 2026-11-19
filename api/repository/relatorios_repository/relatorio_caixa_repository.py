from api.database.connections import ConnectionDataBase
from api.decorators.errors import verificar_erros_banco


class RelatoriosCaixasRepository:

    @verificar_erros_banco
    def caixas_cadastrados(self) -> list[dict]:

        sql = """
            SELECT
                caixa_id,
                valor_inicial_centavos,
                data_aberto,
                horario_aberto,
                status
            FROM
                caixas
            ORDER BY caixa_id ASC
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql)
            return [
                dict(row)
                for row in cur.fetchall()
            ]

    @verificar_erros_banco
    def pagamentos_caixas(self) -> list[dict]:

        sql = """
            SELECT
                c.caixa_id,
                p.pagamento_id,
                p.forma_pagamento,
                p.valor_total_venda_centavos AS valor_total_centavos,
                p.valor_pago_centavos,
                p.troco_centavos
            FROM
                pagamentos_caixa p 
            INNER JOIN
                caixas c ON p.caixa_id = c.caixa_id
            ORDER BY p.pagamento_id ASC
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql)
            return [
                dict(row)
                for row in cur.fetchall()
            ]

    @verificar_erros_banco
    def qtd_caixas_fechados(self):

        sql = """
            SELECT
                COUNT(caixa_id) AS qtd_caixas_fechados
            FROM 
                caixas
            WHERE
                status = 'fechado'
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql)
            caixas = cur.fetchone()

            return dict(caixas) if caixas is not None else {"qtd_caixas_fechados": 0}

    @verificar_erros_banco
    def buscar_caixas_id(self, caixa_id: int) -> dict | None:

        sql = """
            SELECT
                caixa_id,
                valor_inicial_centavos,
                data_aberto,
                horario_aberto,
                status
            FROM
                caixas
            WHERE
                caixa_id = ?
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql, (caixa_id,))
            caixa = cur.fetchone()
            return dict(caixa) if caixa is not None else None
