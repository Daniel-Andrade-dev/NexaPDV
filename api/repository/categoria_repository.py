from api.models.categoria.categoria import Categoria
from api.database.connections import ConnectionDataBase
from api.decorators.errors import verificar_erros_banco
import sqlite3

class CategoriaRepository:

    @verificar_erros_banco
    def adicionar_categoria(self, categoria: Categoria) -> dict:

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo categoria"}

        try:
            with ConnectionDataBase().connect_sql() as conn:
                sql = """
                    INSERT INTO categorias (
                        nome,
                        status
                    ) VALUES(?,?)
                """

                cur = conn.execute(sql, (
                    categoria.nome,
                    categoria.status,
                ))

                categoria_id = cur.lastrowid

                return {
                    "msg": "Categoria cadastrada com sucesso",
                    "dados": {
                        "categoria_id": categoria_id,
                        "categoria": categoria.nome,
                        "status": categoria.status,
                    }
                }
        except sqlite3.IntegrityError:
            return {
                "status": 409,
                "erro": f"Categoria {categoria.nome} já está cadastrada. Tente novamente"
            }

    @verificar_erros_banco
    def buscar_categoria_id(self, categoria_id: int) -> dict | None:
        with ConnectionDataBase().connect_sql() as conn:
            sql_buscar = """
                SELECT
                    categoria_id,
                    nome,
                    status
                FROM
                    categorias
                WHERE
                    categoria_id = ?
            """

            cur = conn.execute(sql_buscar,(categoria_id,))
            categoria = cur.fetchone()
            return dict(categoria) if categoria else {"status": 404, "erro": "Categoria não encontrado"}

    @verificar_erros_banco
    def deletar_categoria(self, categoria: Categoria) -> dict:

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo categoria"}

        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                DELETE
                    FROM
                    categorias
                WHERE
                    categoria_id = ?        

            """
            cur = conn.execute(sql, (categoria.categoria_id,))
            return {
                "sucesso": cur.rowcount > 0,
                "msg": "Categoria deletado com sucesso"
            }

    @verificar_erros_banco
    def atualizar_categoria(self, categoria: Categoria) -> dict:

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo categoria"}

        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                UPDATE
                    categorias
                SET
                    nome = ?,
                    status = ?
                WHERE
                    categoria_id = ?
            """

            cur = conn.execute(sql, (
                categoria.nome,
                categoria.status,
                categoria.categoria_id
            ))

            return {
                "sucesso": cur.rowcount > 0,
                "msg": f"Categoria ID {categoria.categoria_id} atualizada com sucesso"
            }

    @verificar_erros_banco
    def listar_categorias(self) -> list[dict]:
        with ConnectionDataBase().connect_sql() as conn:
            sql = """
                SELECT
                    categoria_id,
                    nome,
                    status
                FROM
                    categorias
            """

            cur = conn.execute(sql)
            return [
                dict(row) 
                for row in cur.fetchall()
            ]
        
