from api.models.categoria.categoria import Categoria
from api.database.connections import ConnectionDataBase
from api.enums.status_categoria import CategoriaDefault
from api.enums.status_categoria import StatusCategoria
import sqlite3 as sql



class CategoriaRepository:

    def connect_database(self):
        return ConnectionDataBase().connect_sql()

    def adicionar_categoria(self, categoria: Categoria):

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo categoria"}

        try:
            with self.connect_database() as conn:
                query = """
                    INSERT INTO categorias (
                        nome_categoria,
                        status
                    ) VALUES(?,?)
                """

                cur = conn.execute(query, (
                    categoria.nome,
                    categoria.status
                ))

                categoria_id = cur.lastrowid

                return {
                    "msg": "Categoria cadastrada com sucesso",
                    "dados": {
                        "categoria_id": categoria_id,
                        "categoria": categoria.nome,
                        "status": categoria.status
                    },
                }
        except sql.IntegrityError:
            return {
                "erro": "Categoria já está cadastrada. Tente novamente"
            }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }


    def buscar_categoria(self, nome_categoria=None, categoria_id=None) -> dict:
        try:
            with self.connect_database() as conn:
                query_buscar = """
                    SELECT
                        categoria_id,
                        nome_categoria,
                        status
                    FROM
                        categorias
                    WHERE
                        nome_categoria = ? OR categoria_id = ?
                """

                if nome_categoria == "":
                    query = """
                        INSERT INTO categorias (
                            nome_categoria,
                            status
                        ) VALUES(?,?)
                    """
                    cur = conn.execute(query, (CategoriaDefault.DIVERSOS, StatusCategoria.ATIVO))
                    return {
                        "categoria": CategoriaDefault.DIVERSOS
                    }
                else:
                    cur = conn.execute(query_buscar,(nome_categoria, categoria_id,))
                    categoria = cur.fetchone()
                    return dict(categoria) if categoria is not None else {"erro": "Categoria não encontrada"}
        except sql.Error as e:
            return {
                "erro": f"Erro de banco de dados: {str(e)}"
            }
   

    def deletar_categoria(self, categoria: Categoria):

        if not isinstance(categoria, Categoria):
            return {"erro": "Objeto inválido. Esperado tipo categoria"}

        try:
            resultado_busca = self.buscar_categoria(categoria.categoria_id)

            if resultado_busca is None:
                return {"erro": "Categoria não encontrada para exclusão"}
            
            with self.connect_database() as conn:
                query = """
                    DELETE
                        FROM
                        categorias
                    WHERE
                        categoria_id = ?        

                """
                cur = conn.execute(query, (categoria.categoria_id,))
                return cur.rowcount > 0
        except sql.Error as e:
            return {
                "erro": f"Erro de banco de dados: {str(e)}"
            }
   

    def atualizar_categoria(self, categoria: Categoria):
        pass 


    def listar_categorias(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        categoria_id,
                        nome_categoria,
                        status
                    FROM
                        categorias
                """

                cur = conn.execute(query)
                categorias = cur.fetchall()

                return [dict(categoria) for categoria in categorias]
        except sql.Error as e:
            return {
                "erro": f"Erro de banco de dados: {str(e)}"
            }
