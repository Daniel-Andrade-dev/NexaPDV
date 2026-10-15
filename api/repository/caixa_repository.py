from api.database.connections import ConnectionDataBase
from api.models.caixa.caixa import Caixa, FechamentosCaixa, PagamentosCaixa
from api.models.caixa.caixa import Sangrias
from api.repository.venda_repository import VendaRepository
from api.enums.status_caixa import StatusCaixa
import sqlite3 as sql



class CaixaRepository:

    def __init__(self):
        self.venda_repository = VendaRepository()

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

                conn.execute(query, (
                    caixa.valor_inicial,
                    caixa.horario_aberto,
                    caixa.data_aberto,
                    caixa.status,
                    caixa.caixa_id
                ))


                return {
                    "sucesso": True,
                    "msg": f"Caixa {caixa.caixa_id} aberto com sucesso",
                    "dados": {
                        "caixa_id": caixa.caixa_id,
                        "valor_inicial": caixa.valor_inicial,
                        "horario_aberto": caixa.horario_aberto,
                        "data_aberto": caixa.data_aberto,
                        "status": caixa.status
                    },
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def inserir_pagamentos_caixa(
            self, 
            caixa: Caixa,
            pagamentos_caixa: PagamentosCaixa,
            troco: int
        ) -> dict:
        try:
            if not isinstance(caixa, Caixa) or not isinstance(pagamentos_caixa, PagamentosCaixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa ou PagamentosCaixa"
                }
            
            with self.connect_database() as conn:
                query = """
                    INSERT INTO pagamentos_caixa (
                        caixa_id,
                        forma_pagamento,
                        valor_total_venda,
                        valor_pago,
                        troco
                    )VALUES(?,?,?,?,?)
                """

                cur = conn.execute(query, (
                    caixa.caixa_id,
                    pagamentos_caixa.forma_pagamento,
                    pagamentos_caixa.valor_total_venda,
                    pagamentos_caixa.valor_pago,
                    troco
                ))

                pagamento_id = cur.lastrowid

                return {
                    "sucesso": True,
                    "msg": f"Pagamento registrado no caixa {caixa.caixa_id}",
                    "dados": {
                        "pagamento_id": pagamento_id,
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def listar_pagamentos_caixa(self) -> dict:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        pagamento_id,
                        caixa_id,
                        forma_pagamento,
                        valor_total_venda,
                        valor_pago,
                        troco
                    FROM
                        pagamentos_caixa
                """

                cur = conn.execute(query)
                pagamentos = cur.fetchall()

                return {
                    "sucesso": True,
                    "dados": [dict(pagamento) for pagamento in pagamentos]
                }                
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }
    
    def fechamento_de_caixa(self, fechamento: FechamentosCaixa, caixa: Caixa):
        try:
            if not isinstance(fechamento, FechamentosCaixa) or not isinstance(caixa, Caixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa ou FechamentosCaixa"
                }

            with self.connect_database() as conn:
                query = """
                    INSERT INTO fechamentos_caixa (
                        caixa_id,
                        valor_esperado,
                        valor_contado,
                        diferenca,
                        data_fechamento,
                        horario_fechamento
                    ) VALUES(?,?,?,?,?,?)
                """

                cur = conn.execute(query, (
                    caixa.caixa_id,
                    fechamento.valor_esperado,
                    fechamento.valor_contado,
                    fechamento.diferenca,
                    fechamento.data_fechamento,
                    fechamento.horario_fechamento
                ))

                query_caixa_att = """
                    UPDATE 
                        caixas
                    SET
                        status = ?
                    WHERE
                        caixa_id = ?
                """

                conn.execute(query_caixa_att, (StatusCaixa.FECHADO, caixa.caixa_id))

                fechamento_id = cur.lastrowid

                return {
                    "sucesso": True,
                    "msg": f"Fechamento do caixa {caixa.caixa_id} realizado com sucesso",
                    "dados": {
                        "fechamento_id": fechamento_id,
                        "valor_esperado": fechamento.valor_esperado,
                        "valor_contado": fechamento.valor_contado,
                        "diferenca": fechamento.diferenca,
                        "data_fechamento": fechamento.data_fechamento,
                        "horario_fechamento": fechamento.horario_fechamento
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }
        
    def total_pagamentos_dinheiro(self, caixa_id: int) -> dict:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT 
                        SUM(p.valor_total_venda) AS total
                    FROM
                        pagamentos_caixa p
                    INNER JOIN
                        caixas c ON c.caixa_id = p.caixa_id
                    WHERE
                        c.caixa_id = ? AND p.forma_pagamento = 'dinheiro'
                """

            cur = conn.execute(query, (caixa_id,))
            pagamento = cur.fetchone()

            if pagamento['total'] is None:
                return {
                    "valor_total_dinheiro": 0.0
                }
            else:
                return {
                    "valor_total_dinheiro": pagamento['total']
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }
        
    def buscar_pagamentos_dinheiro(self, pagamento_id: float) -> dict:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        caixa_id,
                        pagamento_id,
                        forma_pagamento,
                        valor_pago,
                        troco
                    FROM
                        pagamentos_caixa
                    WHERE
                        pagamento_id = ? AND forma_pagamento = 'dinheiro'
                """

                cur = conn.execute(query, (pagamento_id,))
                pagamentos = cur.fetchone()

                if pagamentos is not None:
                    return {
                        "sucesso": True,
                        "dados": {
                            "caixa_id": pagamentos['caixa_id'],
                            "pagamento_id": pagamento_id,
                            "forma_pagamento": pagamentos['forma_pagamento'],
                            "valor_pago": pagamentos['valor_pago'],
                            "troco": pagamentos['troco']
                        }
                    }
                else:
                    return {"erro": "Não há pagamentos em dinheiro"}
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def inserir_sangria_caixa(self, sangria: Sangrias) -> dict:
        try:
            if not isinstance(sangria, Sangrias):
               return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Sangrias"
                }

            with self.connect_database() as conn:
                query = """
                    INSERT INTO sangrias (
                        caixa_id,
                        valor_retirado,
                        data_sangria,
                        horario_sangria
                    ) VALUES(?,?,?,?)
                """

                cur = conn.execute(query, (
                    sangria.caixa_id,
                    sangria.valor_retirado,
                    sangria.data_sangria,
                    sangria.horario_sangria
                ))

                return {
                    "sucesso": True,
                    "msg": "Sangria inserida com sucesso",
                    "dados": {
                        "sangria_id": cur.lastrowid,
                        "caixa_id": sangria.caixa_id,
                        "valor_retirado": sangria.valor_retirado,
                        "data_sangria": sangria.data_sangria,
                        "horario_sangria": sangria.horario_sangria
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def buscar_sangria_id(self, sangria_id: int) -> dict | None:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        caixa_id,
                        sangria_id,
                        valor_retirado,
                        data_sangria,
                        horario_sangria
                    FROM
                        sangrias
                    WHERE
                        sangria_id = ?
                """

                cur = conn.execute(query, (sangria_id,))
                sangria = cur.fetchone()
                return dict(sangria) if sangria is not None else None
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def valor_total_sangria(self, caixa_id: int) -> dict:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        SUM(s.valor_retirado) AS valor_total_sangria
                    FROM
                        sangrias s
                    INNER JOIN
                        caixas c ON c.caixa_id = s.caixa_id
                    WHERE 
                        c.caixa_id = ?
                """

                cur = conn.execute(query, (caixa_id,))
                valor_total = cur.fetchone()

                if valor_total['valor_total_sangria'] is None:
                    return {"valor_total_sangria": 0.0}
                else:
                    return {
                        "sucesso": True,
                        "valor_total_sangria": valor_total['valor_total_sangria']
                    }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def realizar_sangria_caixa(self, sangria: Sangrias, caixa: Caixa) -> dict:
        try:
            if not isinstance(caixa, Caixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa"
                }
            
            busca_caixa = self.buscar_caixa(caixa.caixa_id)
            busca_sangria = self.buscar_sangria_id(sangria.sangria_id)

            sangria = busca_caixa['valor_inicial'] - busca_sangria['valor_retirado']

            with self.connect_database() as conn:
                query = """
                    UPDATE
                        caixas
                    SET
                        valor_inicial = ?
                    WHERE
                        caixa_id = ?
                """

                conn.execute(query, (sangria, busca_caixa['caixa_id']))

                return {
                    "sucesso": True,
                    "msg": "Sangria realizada com sucesso",
                    "dados": {
                        "caixa_id": busca_caixa['caixa_id'],
                        "valor_retirado": busca_sangria['valor_retirado']
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

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

    def listar_caixas(self) -> list[dict]:
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
                """

                cur = conn.execute(query)
                caixas_abertos = cur.fetchall()
                return [dict(caixa) for caixa in caixas_abertos]
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }
