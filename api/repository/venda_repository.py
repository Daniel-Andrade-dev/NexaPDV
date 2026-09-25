from api.models.venda.venda import VendaInicializada, VendaFinalizada
from api.models.produto.produto import Produto
from api.database.connections import ConnectionDataBase
import sqlite3 as sql


class VendaRepository:

    def connect_database(self):
        return ConnectionDataBase().connect_sql()

    def inicializar_vendas(self, items: list[dict], valor_total_mock: float) -> dict:

        if not items or len(items) == 0:
            return {"erro": "O carrinho precisa de um item para inicia a venda"}

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
                        valor_total_mock,
                        item['quantidade_venda'],
                        item['horario_inicializada'],
                        item['data_inicializada'],
                        item['status']
                    ))


                    venda_id = cur.lastrowid


                return {
                    "venda": {
                        "venda_id": venda_id,
                        "iniciada_em": f"{item['data_inicializada']}T{item['horario_inicializada']}",
                        "status": item['status'],
                        "valor_total_venda": valor_total_mock
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }


        
    def finalizar_venda(self, venda: VendaFinalizada, valor_total, horario_mock, data_mock):
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
                "pagamento": {
                    "forma": venda.forma_pagamento,
                    "valor_pago": venda.valor_pago
                },
                "status": venda.status,
                "finalizada_em": f"{data_mock}T{horario_mock}"
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

    def listar_vendas_finalizas(self):
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

                return cur.rowcount > 0 
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def cancelar_venda(self, venda_iniciada: VendaInicializada) -> dict:
        try:

            if not isinstance(venda_iniciada, VendaInicializada):
                return {"erro": "Objeto inválida"}
            
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
                    "msg": "Venda cancelada com sucesso"
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