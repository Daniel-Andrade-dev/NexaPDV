from api.models.venda.venda import VendaInicializada, VendaFinalizada
from api.database.connections import ConnectionDataBase
import sqlite3 as sql


class VendaRepository:

    def connect_database(self):
        return ConnectionDataBase().connect_sql()

    def inicializar_vendas(self, items: list[dict], valor_total: float) -> dict:

        try:
            for item in items:
                with self.connect_database() as conn:
                    query = """
                        INSERT INTO vendas_inicializadas (
                            valor_total,
                            venda_quantidade,
                            horario_inicializada,
                            data_inicializada,
                            status
                        ) VALUES(?,?,?,?,?)
                    """

                    cur = conn.execute(query, (
                        valor_total,
                        item['quantidade_venda'],
                        item['horario_inicializada'],
                        item['data_inicializada'],
                        item['status']
                    ))

                    venda_id = cur.lastrowid

                    dados_itens = [
                        (
                            venda_id,
                            item["codigo_produto"],
                            item["quantidade_venda"],
                            item["preco_unitario"],
                            item['valor_total_produto']
                        )
                        for item in items
                    ]

                    query_itens_venda = """
                        INSERT INTO itens_venda_inicializada (
                            venda_id,
                            codigo_produto,
                            venda_quantidade,
                            preco_unitario,
                            valor_total_produto
                        ) VALUES(?,?,?,?,?)
                    """

                    conn.executemany(query_itens_venda, dados_itens)

                    return {    
                        "venda_id": venda_id,
                        "iniciada_em": f"{item['data_inicializada']}T{item['horario_inicializada']}",
                        "status": item['status'],
                        "valor_total_venda": valor_total
                    }
        except sql.Error as e:
            return {
                "erro": f"Erro de banco de dados: {str(e)}"
            }


        
    def finalizar_venda(self, venda: VendaFinalizada, valor_total, troco, horario_mock, data_mock):
        try:
            if not isinstance(venda, VendaFinalizada):
                return {'erro': 'Objeto inválido'}

            with self.connect_database() as conn:
                query = """
                    INSERT INTO vendas_finalizadas (
                        forma_pagamento,
                        valor_total,
                        valor_pago,
                        status,
                        horario_finalizada,
                        data_finalizada
                    ) VALUES(?,?,?,?,?,?)
                """

                cur = conn.execute(query, (
                    venda.forma_pagamento,
                    valor_total,
                    venda.valor_pago,
                    venda.status,
                    horario_mock,
                    data_mock
                ))

                venda_id = cur.lastrowid

            return {
                "venda_id": venda_id,
                "finalizada_em": f"{data_mock}T{horario_mock}",
                "pagamento": {
                    "forma": venda.forma_pagamento,
                    "valor_pago": venda.valor_pago,
                    "troco": troco
                },
                "status_venda_finalizada": venda.status,
            }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            } 

    def listar_vendas_iniciadas(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        venda_id,
                        valor_total,
                        venda_quantidade,
                        horario_inicializada AS horario,
                        data_inicializada AS data,
                        status
                    FROM
                        vendas_inicializadas
                """
                cur = conn.execute(query)
                vendas_atuais = cur.fetchall()
                return [dict(venda) for venda in vendas_atuais]
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }   

    def listar_vendas_finalizadas(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        id_venda AS venda_id,
                        forma_pagamento,
                        valor_total,
                        valor_pago,
                        status,
                        horario_finalizada AS horario,
                        data_finalizada AS data
                    FROM
                        vendas_finalizadas
                    ORDER BY valor_total ASC
                """

                cur = conn.execute(query)
                vendas_atuais = cur.fetchall()
                return [dict(venda) for venda in vendas_atuais]
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            } 
    def buscar_venda_inicializada(self, venda_id: int):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT 
                        venda_id,
                        valor_total,
                        venda_quantidade,
                        horario_inicializada,
                        data_inicializada,
                        status
                    FROM
                        vendas_inicializadas
                    WHERE 
                        venda_id = ?
                """

                cur = conn.execute(query, (venda_id,))
                venda = cur.fetchone()

                return dict(venda) if venda is not None else None
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def atualizar_status_venda(self, venda_finalizada: VendaFinalizada, venda_iniciada: VendaInicializada) -> dict | bool:
        try:
            buscar_venda = self.buscar_venda_inicializada(venda_iniciada.venda_id)

            if buscar_venda is None:
                return {"erro": "Venda não encontrada"}

            with self.connect_database() as conn:
                query = """
                    UPDATE
                        vendas_inicializadas
                    SET
                        status = ?
                    WHERE
                        venda_id = ?
                """
                cur = conn.execute(query,(
                    venda_finalizada.status,
                    buscar_venda["venda_id"]
                ))

                return {
                    "sucesso": cur.rowcount > 0,
                    "msg": "Status atualizado"
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def cancelar_venda(self, venda_iniciada: VendaInicializada) -> dict:
        try:

            if not isinstance(venda_iniciada, VendaInicializada):
                return {"erro": "Objeto inválido"}
            
            buscar_venda = self.buscar_venda_inicializada(venda_iniciada.venda_id)

            if buscar_venda is None:
                return {"erro": "Venda não encontrada"}
            
            with self.connect_database() as conn:
                query = """
                    UPDATE
                        vendas_inicializadas
                    SET
                        status = ?
                    WHERE
                        venda_id = ?
                """

                cur = conn.execute(query, (
                    venda_iniciada.status,
                    buscar_venda['venda_id']
                ))

                return {
                    "sucesso": cur.rowcount > 0,
                    "msg": "Venda cancelada com sucesso",
                    "venda": {
                        "venda_id": buscar_venda['venda_id'],
                        "status_venda": venda_iniciada.status,
                        "valor_total": buscar_venda['valor_total']
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def listar_vendas_canceladas(self) -> list[dict]:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        venda_id,
                        valor_total,
                        venda_quantidade,
                        horario_inicializada AS horario,
                        data_inicializada AS data,
                        status
                    FROM
                        vendas_inicializadas
                    WHERE
                        status = 'cancelada'
                """
                cur = conn.execute(query)
                vendas_canceladas = cur.fetchall()
                return [dict(venda) for venda in vendas_canceladas]
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def total_vendas_iniciadas(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        COUNT(venda_id) AS total_vendas
                    FROM
                        vendas_inicializadas
                """

                cur = conn.execute(query)
                total_vendas = cur.fetchone()

                return {"total_vendas_iniciadas": total_vendas['total_vendas']}
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def total_vendas_canceladas(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        COUNT(venda_id) AS vendas_canceladas
                    FROM
                        vendas_inicializadas
                    WHERE 
                        status = 'cancelada'
                """
                cur = conn.execute(query)
                vendas = cur.fetchone()

                return {"vendas_canceladas": vendas['vendas_canceladas']}
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def total_vendas_finalizadas(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        COUNT(id_venda) AS total_vendas_finalizadas
                    FROM
                        vendas_finalizadas
                """
                cur = conn.execute(query)
                vendas = cur.fetchone()

                return {"total_vendas": vendas['total_vendas_finalizadas']}
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def ticket_medio_vendas_finalizadas(self):
        try:

            with self.connect_database() as conn:
                query = """
                    SELECT
                        SUM(valor_total) / COUNT(id_venda) AS ticket_medio
                    FROM
                        vendas_finalizadas
                """

                cur = conn.execute(query)
                ticket = cur.fetchone()

                # Se o ticket retorna None ou null significa que é = 0
                if ticket['ticket_medio'] is None:
                    return {
                        "ticket_medio": 0.0
                    }
                else:
                    return {
                        "ticket_medio": round(ticket['ticket_medio'], 2)
                    }
                    
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

