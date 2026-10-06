from api.database.connections import ConnectionDataBase
from api.models.caixa.caixa import Caixa, TotalCaixa, PagamentosCaixa
import sqlite3 as sql



class CaixaRepository:

    def connect_database(self):
        return ConnectionDataBase().connect_sql()

    def abertura_caixa(self, caixa: Caixa):
        try:
            if not isinstance(caixa, Caixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa"
                }

            resultado_caixa = self.buscar_caixa(caixa.caixa_id)

            if resultado_caixa is None:
                return None

            with self.connect_database() as conn:
                query = """
                    UPDATE
                        caixas
                    SET
                        valor_inicial = ?,
                        horario_aberto = ?,
                        data_aberto = ?,
                        status = ?
                    WHERE
                        caixa_id = ?
                """

                cur = conn.execute(query, (
                    caixa.valor_inicial,
                    caixa.horario_aberto,
                    caixa.data_aberto,
                    caixa.status,
                    caixa.caixa_id
                ))


                return {
                    "sucesso": True,
                    "dados": {
                        "caixa_id": caixa.caixa_id,
                        "valor_inicial": caixa.valor_inicial,
                        "horario_aberto": caixa.horario_aberto,
                        "data_aberto": caixa.data_aberto,
                        "status": caixa.status
                    },
                    "msg": f"Caixa {caixa.caixa_id} aberto com sucesso"
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def inserir_pagamentos_caixa(self, caixa: Caixa, pagamento_caixa: PagamentosCaixa):
        try:
            if not isinstance(caixa, Caixa) or not isinstance(pagamento_caixa, PagamentosCaixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa"
                }

            with self.connect_database() as conn:
                query = """
                    INSERT INTO pagamentos_caixa (
                        caixa_id,
                        forma_pagamento,
                        valor_pago
                    )VALUES(?,?,?)
                """

                cur = conn.execute(query, (
                    caixa.caixa_id,
                    pagamento_caixa.forma_pagamento,
                    pagamento_caixa.valor_pago
                ))

                pagamento_caixa_id = cur.lastrowid

                return {
                    "sucesso": True,
                    "dados": {
                        "pagamento_caixa_id": pagamento_caixa_id,
                        "caixa_id": caixa.caixa_id,
                        "forma_pagamento": pagamento_caixa.forma_pagamento,
                        "valor_pago": pagamento_caixa.valor_pago
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    # Em desenvolvimento é estudos
    def fechamento_caixa(self):
        pass 


    def cadastrar_caixa(self, caixa: Caixa) -> dict:
        try:
            if not isinstance(caixa, Caixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa"
                }
            
            with self.connect_database() as conn:
                query = """
                    INSERT INTO caixas (
                        valor_inicial,
                        horario_aberto,
                        data_aberto,
                        status
                    ) VALUES(?,?,?,?)
                """

                cur = conn.execute(query, (
                    caixa.valor_inicial,
                    caixa.horario_aberto,
                    caixa.data_aberto,
                    caixa.status
                ))

                caixa_id = cur.lastrowid

                return {
                    "sucesso": True,
                    "dados": {
                        "caixa_id": caixa_id,
                        "valor_inicial": caixa.valor_inicial,
                        "status": caixa.status
                    },
                    "msg": f"Caixa {caixa_id} cadastrado com sucesso"
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def buscar_caixa(self, caixa_id: int) -> dict | None:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT 
                        caixa_id,
                        valor_inicial,
                        horario_aberto,
                        data_aberto,
                        status
                    FROM
                        caixas
                    WHERE 
                        caixa_id = ?
                """

                cur = conn.execute(query, (caixa_id,))
                caixa = cur.fetchone()

                if caixa is not None:
                    return {
                        "caixa_id": caixa['caixa_id'],
                        "valor_inicial": caixa['valor_inicial'],
                        "horario_aberto": caixa['horario_aberto'],
                        "data_aberto": caixa['data_aberto'],
                        "status": caixa['status']
                    }
                else:
                    return None
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def listar_caixas_abertos(self) -> list[dict]:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT 
                        caixa_id,
                        valor_inicial,
                        horario_aberto,
                        data_aberto,
                        status
                    FROM
                        caixas
                    WHERE
                        status = 'aberto'
                """

                cur = conn.execute(query)
                caixas_abertos = cur.fetchall()
                return [dict(caixas) for caixas in caixas_abertos]
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }