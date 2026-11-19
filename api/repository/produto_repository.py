from api.database.connections import ConnectionDataBase
from api.models.produto.produto import Produto
from api.models.venda.venda import VendaIniciada
from api.decorators.errors import verificar_erros_banco
import sqlite3

class ProdutoRepository:

    @verificar_erros_banco
    def inserir_produto(self, categoria_id: int, produto: Produto) -> dict:

        if not isinstance(produto, Produto):
            return {
                "sucesso": False,
                "dados": None,
                "erro": "Objeto inválido. Esperado tipo Produto."
            }

        try:
            with ConnectionDataBase().connect_sql() as conn:
                sql = """
                    INSERT INTO produtos (
                        categoria_id,
                        nome_produto,
                        preco_unitario_centavos,
                        estoque,
                        status
                    )
                    VALUES(?,?,?,?,?)
                """

                cur = conn.execute(sql,(
                    categoria_id,
                    produto.nome_produto,
                    produto.preco_unitario_centavos,
                    produto.estoque,
                    produto.status
                ))

            return {
                "sucesso": True,
                "msg": f"Produto {produto.nome_produto} cadastrado com sucesso",
                "dados": {
                    "codigo_produto": cur.lastrowid,
                    "categoria_id": categoria_id,
                    "nome": produto.nome_produto,
                    "preco_unitario_centavos": produto.preco_unitario_centavos,
                    "estoque": produto.estoque,
                    "status": produto.status
                },
            }
        except sqlite3.IntegrityError:
            return {
                "status": 409,
                "erro": f"Produto {produto.nome_produto} já está cadastrado. Tente novamente."
            }

    @verificar_erros_banco
    def buscar_produto(self, codigo_produto: int) -> dict:
        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                SELECT
                    p.codigo_produto,
                    c.nome AS categoria,
                    c.categoria_id,
                    p.nome_produto,
                    p.preco_unitario_centavos,
                    p.estoque,
                    p.status
                FROM
                    produtos p
                LEFT JOIN
                    categorias c ON p.categoria_id = c.categoria_id
                WHERE
                    p.codigo_produto = ?
            """
            cur = conn.execute(sql, (codigo_produto,))
            produto = cur.fetchone()

            return dict(produto) if produto is not None else None

    @verificar_erros_banco
    def baixa_estoque(self, codigo_produto: int, novo_estoque: int) -> dict:
        sql = """
            UPDATE
                produtos
            SET
                estoque = ?
            WHERE
                codigo_produto = ?
        """

        with ConnectionDataBase().connect_sql() as conn:
            
            cur = conn.execute(sql,(novo_estoque, codigo_produto))

            return {
                "sucesso": cur.rowcount > 0,
                "novo_estoque": novo_estoque
            }

    @verificar_erros_banco
    def retorno_estoque(self, codigo_produto: int, quantidade_retornada: int) -> dict:

        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                UPDATE 
                    produtos
                SET 
                    estoque = ?
                WHERE 
                    codigo_produto = ?
            """
            cur = conn.execute(sql, (quantidade_retornada, codigo_produto))

            return {
                "sucesso": cur.rowcount > 0,
                "msg": "Estoque do produto retornado com sucesso"
            }

    @verificar_erros_banco
    def deletar_produto(self, codigo_produto: int) -> dict:
        with ConnectionDataBase().connect_sql() as conn:
            sql = """
            DELETE
                FROM
                    produtos
                WHERE
                    codigo_produto = ?
            """

            cur = conn.execute(sql, (codigo_produto,))

            return {
                "sucesso": cur.rowcount > 0,
                "msg": "Produto deletado com sucesso"
            }

    @verificar_erros_banco
    def atualizar_produto(self, categoria_id: int, produto: Produto) -> dict:

        if not isinstance(produto, Produto):
            return {
                "sucesso": False,
                "dados": None,
                "erro": "Objeto inválido. Esperado tipo Produto."
            }

        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                UPDATE 
                    produtos
                SET 
                    nome_produto = ?,
                    categoria_id = ?,
                    preco_unitario_centavos = ?,
                    estoque = ?,
                    status = ?
                WHERE 
                    codigo_produto = ?
            """
            conn.execute(sql,(
                produto.nome_produto,
                categoria_id,
                produto.preco_unitario_centavos,
                produto.estoque,
                produto.status,
                produto.codigo_produto
            ))

            return {
                "msg": f"Produto {produto.nome_produto} atualizado com sucesso",
                "dados": {
                    "codigo_produto": produto.codigo_produto,
                    "categoria_id": categoria_id,
                    "nome": produto.nome_produto,
                    "preco_unitario_centavos": produto.preco_unitario_centavos,
                    "estoque": produto.estoque,
                    "status": produto.status
                }
            }