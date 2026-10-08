from api.database.connections import ConnectionDataBase
from api.models.caixa.caixa import Caixa, TotalCaixa, PagamentosCaixa
from api.models.venda.venda import VendaFinalizada
from api.repository.venda_repository import VendaRepository
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
                        valor_total_venda AS valor_total,
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
    
    # Em desenvolvimento é estudos
    def fechamento_caixa(self, total_caixa: TotalCaixa, caixa: Caixa):
        try:
            if not isinstance(total_caixa, TotalCaixa) or not isinstance(caixa, Caixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa ou TotalCaixa"
                }

            with self.connect_database() as conn:
                query = """
                    INSERT INTO total_caixa (
                        caixa_id,
                        valor_total_venda,
                        valor_esperado,
                        valor_contado,
                        diferenca,
                        data_fechamento,
                        horario_fechamento
                    ) VALUES(?,?,?,?,?,?,?)
                """

                cur = conn.execute(query, (
                    caixa.caixa_id,
                    total_caixa.valor_total_venda,
                    total_caixa.valor_esperado,
                    total_caixa.valor_contado,
                    total_caixa.diferenca,
                    total_caixa.data_fechamento,
                    total_caixa.horario_fechamento
                ))

                fechamento_id = cur.lastrowid

                return {
                    "sucesso": True,
                    "msg": f"Fechamento do caixa {caixa.caixa_id} realizado com sucesso",
                    "dados": {
                        "fechamento_id": fechamento_id,
                        "valor_total_venda": total_caixa.valor_total_venda,
                        "valor_esperado": total_caixa.valor_esperado,
                        "valor_contado": total_caixa.valor_contado,
                        "diferenca": total_caixa.diferenca,
                        "data_fechamento": total_caixa.data_fechamento,
                        "horario_fechamento": total_caixa.horario_fechamento
                    }
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }
        

    def realizar_sangria_caixa(self, valor_retirado, caixa: Caixa) -> dict:
        try:
            if not isinstance(caixa, Caixa):
                return {
                    "sucesso": False,
                    "dados": None,
                    "msg": "Objeto inválido. Esperado tipo Caixa"
                }
            
            resultado_busca = self.buscar_caixa(caixa.caixa_id)
            sangria = resultado_busca['valor_inicial'] - valor_retirado

            with self.connect_database() as conn:
                query = """
                    UPDATE
                        caixas
                    SET
                        valor_inicial = ?
                    WHERE
                        caixa_id = ?
                """

                conn.execute(query, (sangria, resultado_busca['caixa_id']))

                return {
                    "sucesso": True,
                    "msg": "Sangria realizada com sucesso",
                    "dados": {
                        "caixa_id": resultado_busca['caixa_id'],
                        "valor_retirado": valor_retirado,
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
                return {
                    "sucesso": True,
                    "dados": [dict(caixa) for caixa in caixas_abertos]
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def listar_caixas_fechados(self) -> list[dict]:
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
                        status = 'fechado'
                """

                cur = conn.execute(query)
                caixas_abertos = cur.fetchall()
                return {
                    "sucesso": True,
                    "dados": [dict(caixa) for caixa in caixas_abertos]
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }