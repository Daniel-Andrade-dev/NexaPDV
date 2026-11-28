from api.database.connections import ConnectionDataBase
from api.models.caixa.caixa import Caixa, FechamentosCaixa, PagamentosCaixa
from api.models.caixa.caixa import Sangrias
from api.repository.venda_repository import VendaRepository
from api.enums.status_caixa import StatusCaixa
from api.decorators.errors import verificar_erros_banco

class CaixaRepository:

    def __init__(self):
        self.venda_repository = VendaRepository()

    @verificar_erros_banco
    def abertura_caixa(self, caixa: Caixa) -> dict:
        if not isinstance(caixa, Caixa):
            return {
                "sucesso": False,
                "dados": None,
                "msg": "Objeto inválido. Esperado tipo Caixa"
            }
        
        sql = """
            UPDATE
                caixas
            SET
                valor_inicial_centavos = ?,
                horario_aberto = ?,
                data_aberto = ?,
                status = ?
            WHERE
                caixa_id = ?
        """
        
        with ConnectionDataBase().connect_sql() as conn:
            conn.execute(sql, (
                caixa.valor_inicial_centavos,
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
                    "aberto_em": f"{caixa.data_aberto}T{caixa.horario_aberto}",
                    "valor_inicial_centavos": caixa.valor_inicial_centavos,
                    "status": caixa.status
                },
            }

    @verificar_erros_banco
    def inserir_pagamentos_caixa(
            self, 
            caixa: Caixa,
            pagamentos_caixa: PagamentosCaixa,
            troco_centavos: int
        ) -> dict:
        if not isinstance(caixa, Caixa) or not isinstance(pagamentos_caixa, PagamentosCaixa):
            return {
                "sucesso": False,
                "dados": None,
                "msg": "Objeto inválido. Esperado tipo Caixa ou PagamentosCaixa"
            }

        sql = """
            INSERT INTO pagamentos_caixa (
                caixa_id,
                forma_pagamento,
                valor_total_venda_centavos,
                valor_pago_centavos,
                troco_centavos
            )VALUES(?,?,?,?,?)
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql, (
                caixa.caixa_id,
                pagamentos_caixa.forma_pagamento,
                pagamentos_caixa.valor_total_venda_centavos,
                pagamentos_caixa.valor_pago_centavos,
                troco_centavos
            ))

            pagamento_id = cur.lastrowid

            return {
                "sucesso": True,
                "msg": f"Pagamento registrado no caixa {caixa.caixa_id}",
                "dados": {
                    "pagamento_id": pagamento_id,
                }
            }

    @verificar_erros_banco
    def fechamento_de_caixa(self, fechamento: FechamentosCaixa, caixa: Caixa):
        if not isinstance(fechamento, FechamentosCaixa) or not isinstance(caixa, Caixa):
            return {
                "sucesso": False,
                "dados": None,
                "msg": "Objeto inválido. Esperado tipo Caixa ou FechamentosCaixa"
            }
        
        sql = """
            INSERT INTO fechamentos_caixa (
                caixa_id,
                valor_esperado_centavos,
                valor_contado_centavos,
                diferenca_centavos,
                data_fechamento,
                horario_fechamento
            ) VALUES(?,?,?,?,?,?)
         """
        
        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql, (
                caixa.caixa_id,
                fechamento.valor_esperado_centavos,
                fechamento.valor_contado_centavos,
                fechamento.diferenca_centavos,
                fechamento.data_fechamento,
                fechamento.horario_fechamento
            ))

            sql_caixa_att = """
                UPDATE 
                    caixas
                SET
                    status = ?
                WHERE
                    caixa_id = ?
            """

            conn.execute(sql_caixa_att, (StatusCaixa.FECHADO, caixa.caixa_id))

            fechamento_id = cur.lastrowid

            return {
                "sucesso": True,
                "msg": f"Fechamento do caixa {caixa.caixa_id} realizado com sucesso",
                "dados": {
                    "fechamento_id": fechamento_id,
                    "valor_esperado_centavos": fechamento.valor_esperado_centavos,
                    "valor_contado_centavos": fechamento.valor_contado_centavos,
                    "diferenca_centavos": fechamento.diferenca_centavos,
                    "fechado_em": f"{fechamento.data_fechamento}T{fechamento.horario_fechamento}"
                }
            }

    @verificar_erros_banco
    def total_pagamentos_dinheiro(self, caixa_id: int) -> dict:
        sql = """
            SELECT 
                SUM(p.valor_total_venda_centavos) AS total_centavos
            FROM
                pagamentos_caixa p
            INNER JOIN
                caixas c ON c.caixa_id = p.caixa_id
            WHERE
                c.caixa_id = ? AND p.forma_pagamento = 'dinheiro'
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql, (caixa_id,))
            pagamento = cur.fetchone()

            if pagamento['total_centavos'] is None:
                return {
                    "valor_total_dinheiro_centavos": 0
                }
            else:
                return {
                    "valor_total_dinheiro_centavos": pagamento['total_centavos']
                }

    @verificar_erros_banco
    def inserir_sangria_caixa(self, caixa_id: int, sangria: Sangrias) -> dict:
        if not isinstance(sangria, Sangrias):
           return {
                "sucesso": False,
                "dados": None,
                "msg": "Objeto inválido. Esperado tipo Sangrias"
            }
        
        sql = """
            INSERT INTO sangrias (
                caixa_id,
                valor_retirado_centavos,
                data_sangria,
                horario_sangria
            ) VALUES(?,?,?,?)
         """
        with ConnectionDataBase().connect_sql() as conn:
 
            cur = conn.execute(sql, (
                caixa_id,
                sangria.valor_retirado_centavos,
                sangria.data_sangria,
                sangria.horario_sangria
            ))

            return {
                "sucesso": True,
                "msg": "Sangria inserida com sucesso",
                "dados": {
                    "sangria_id": cur.lastrowid,
                    "caixa_id": caixa_id,
                    "valor_retirado_centavos": sangria.valor_retirado_centavos,
                    "feita_em": f"{sangria.data_sangria}T{sangria.horario_sangria}"
                }
            }

    @verificar_erros_banco
    def buscar_sangria_id(self, sangria_id: int) -> dict | None:
        sql = """
            SELECT
                caixa_id,
                sangria_id,
                valor_retirado_centavos,
                data_sangria,
                horario_sangria
            FROM
                sangrias
            WHERE
                sangria_id = ?
        """
        
        with ConnectionDataBase().connect_sql() as conn:

            cur = conn.execute(sql, (sangria_id,))
            sangria = cur.fetchone()
            return dict(sangria) if sangria is not None else None

    @verificar_erros_banco
    def valor_total_sangria(self, caixa_id: int) -> dict:
        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                SELECT
                    SUM(s.valor_retirado_centavos) AS valor_total_sangria_centavos
                FROM
                    sangrias s
                INNER JOIN
                    caixas c ON c.caixa_id = s.caixa_id
                WHERE 
                    c.caixa_id = ?
            """

            cur = conn.execute(sql, (caixa_id,))
            valor_total = cur.fetchone()

            if valor_total['valor_total_sangria_centavos'] is None:
                return {"valor_total_sangria_centavos": 0}
            else:
                return {
                    "sucesso": True,
                    "valor_total_sangria_centavos": valor_total['valor_total_sangria_centavos']
                }

    @verificar_erros_banco
    def realizar_sangria_caixa(self, sangria: Sangrias, caixa: Caixa) -> dict:
        if not isinstance(caixa, Caixa):
            return {
                "sucesso": False,
                "dados": None,
                "msg": "Objeto inválido. Esperado tipo Caixa"
            }

        busca_caixa = self.buscar_caixa_id(caixa.caixa_id)
        busca_sangria = self.buscar_sangria_id(sangria.sangria_id)

        sangria = busca_caixa['valor_inicial_centavos'] - busca_sangria['valor_retirado_centavos']

        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                UPDATE
                    caixas
                SET
                    valor_inicial_centavos = ?
                WHERE
                    caixa_id = ?
            """

            conn.execute(sql, (sangria, caixa.caixa_id))

            return {
                "sucesso": True,
                "msg": "Sangria realizada com sucesso",
                "dados": {
                    "caixa_id": caixa.caixa_id,
                    "valor_retirado_centavos": busca_sangria['valor_retirado_centavos'],
                }
            }

    @verificar_erros_banco
    def cadastrar_caixa(self, caixa: Caixa) -> dict:
        if not isinstance(caixa, Caixa):
            return {
                "sucesso": False,
                "dados": None,
                "msg": "Objeto inválido. Esperado tipo Caixa"
            }

        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                INSERT INTO caixas (
                    valor_inicial_centavos,
                    horario_aberto,
                    data_aberto,
                    status
                ) VALUES(?,?,?,?)
            """

            cur = conn.execute(sql, (
                caixa.valor_inicial_centavos,
                caixa.horario_aberto,
                caixa.data_aberto,
                caixa.status
            ))

            caixa_id = cur.lastrowid

            return {
                "sucesso": True,
                "dados": {
                    "caixa_id": caixa_id,
                    "valor_inicial_centavos": caixa.valor_inicial_centavos,
                    "status": caixa.status
                },
                "msg": f"Caixa {caixa_id} cadastrado com sucesso"
            }

    @verificar_erros_banco
    def buscar_caixa_id(self, caixa_id: int) -> dict | None:
        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                SELECT 
                    caixa_id,
                    valor_inicial_centavos,
                    horario_aberto,
                    data_aberto,
                    status
                FROM
                    caixas
                WHERE 
                    caixa_id = ?
            """

            cur = conn.execute(sql, (caixa_id,))
            caixa = cur.fetchone()

            if caixa is not None:
                return {
                    "caixa_id": caixa['caixa_id'],
                    "valor_inicial_centavos": caixa['valor_inicial_centavos'],
                    "aberto_em": f"{caixa['data_aberto']}T{caixa['horario_aberto']}",
                    "data_aberto": caixa['data_aberto'],
                    "horario_aberto": caixa['horario_aberto'],
                    "status": caixa['status']
                }
            return None