from api.database.connections import ConnectionDataBase
from api.decorators.errors import verificar_erros_banco



class RelatorioProdutosRepository:

    @verificar_erros_banco
    def produtos_cadastrados(self) -> list[dict]:

        sql = """
            SELECT
                p.codigo_produto,
                p.nome_produto,
                c.nome AS categoria,
                p.preco_unitario_centavos,
                p.estoque,
                p.status
            FROM
                produtos p 
            LEFT JOIN 
                categorias c ON p.categoria_id = c.categoria_id
            ORDER BY
                p.codigo_produto ASC;
        """

        with ConnectionDataBase().connect_sql() as conn:
            cur = conn.execute(sql)
            return [
                dict(row)
                for row in cur.fetchall()
            ]