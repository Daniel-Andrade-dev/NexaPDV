import sqlite3 as sql
from api.database.connections import ConnectionDataBase
from api.models.produto.produto import Produto
from api.models.categoria.categoria import Categoria
from api.models.venda.venda import VendaInicializada


"""
CRUD CONTROLE DE ESTOQUE PARA O PDV
"""

class ProdutoRepository:

    def connect_database(self):
        return ConnectionDataBase().connect_sql()

    def inserir_produto(self, categoria: Categoria, produto: Produto) -> dict:
        if not isinstance(produto, Produto):
            return {"erro": "Objeto inválido. Esperado tipo Produto."}

        try:
            with self.connect_database() as conn:
                query = """
                    INSERT INTO produtos (
                        categoria_id,
                        nome_produto,
                        preco_unitario,
                        estoque,
                        status
                    )
                    VALUES(?,?,?,?,?)
                """

                cur = conn.execute(query,(
                    categoria.categoria_id,
                    produto.nome_produto,
                    produto.preco_unitario,
                    produto.estoque,
                    produto.status
                ))

            return {
                "sucesso": True,
                "dados": {
                    "codigo": cur.lastrowid,
                    "categoria_id": categoria.categoria_id,
                    "nome": produto.nome_produto,
                    "preco_unitario": produto.preco_unitario,
                    "estoque": produto.estoque,
                    "status": produto.status
                },
                "msg": f"Produto {produto.nome_produto} cadastrado com sucesso"
            }
            
        except sql.IntegrityError:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Produto {produto.nome_produto} já está cadastrado. Tente novamente."
            }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }

    def buscar_produto(self, codigo: int) -> dict:
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        p.codigo,
                        c.nome AS categoria,
                        p.nome_produto,
                        p.preco_unitario,
                        p.estoque,
                        p.status
                    FROM
                        produtos p
                    INNER JOIN
                        categorias c ON p.categoria_id = c.categoria_id
                    WHERE
                        p.codigo = ?
                """
                cur = conn.execute(query, (codigo,))
                produto = cur.fetchone()

                if produto is not None:
                    return {
                        "codigo": produto["codigo"],
                        "categoria": produto['categoria'],
                        "nome_produto": produto["nome_produto"],
                        "preco_unitario": produto["preco_unitario"],
                        "estoque": produto["estoque"],
                        "status": produto["status"]
                    }
                else:
                    return None
        except sql.Error as e:
            return {
                "erro": f"Erro de banco de dados: {str(e)}"
            }
    
    def baixa_estoque(self, produto: Produto, venda: VendaInicializada) -> dict | bool:
        if not isinstance(venda, VendaInicializada):
            return {"erro": "Objeto de venda inválido."}

        try:
            busca_produto = self.buscar_produto(produto.codigo)

            if not busca_produto:
                return {"erro": "Produto não foi encontrado"}
            
            novo_estoque = int(busca_produto['estoque']) - venda.venda_quantidade

            if venda.venda_quantidade > busca_produto['estoque']:
                return {"erro": f"Não há estoque suficiente do produto {produto.nome_produto} código {produto.codigo}."}

            with self.connect_database() as conn:
                query = """
                    UPDATE
                        produtos
                    SET
                        estoque = ?
                    WHERE
                        codigo = ?
                """
                cur = conn.execute(query,(novo_estoque, produto.codigo))

                return {
                    "sucesso": cur.rowcount > 0,
                    "estoque_atual": busca_produto['estoque'],
                    "novo_estoque": novo_estoque
                }
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }       

    def deletar_produto(self, produto: Produto) -> dict | bool:
        if not isinstance(produto, Produto):
            return {"erro": "Objeto inválido."}

        try:
            busca = self.buscar_produto(produto.codigo)

            with self.connect_database() as conn:
                query = """
                DELETE
                    FROM
                        produtos
                    WHERE
                        codigo = ?
                """

                cur = conn.execute(query, (produto.codigo,))

                if busca is not None:
                    return {
                        "sucesso": cur.rowcount > 0,
                        "msg": f"Produto {produto.nome_produto} deletado"
                    }
                else:
                    return None
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }
    
    def listar_produtos(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        p.codigo,
                        p.nome_produto,
                        c.nome AS categoria,
                        p.preco_unitario,
                        p.estoque,
                        p.status
                    FROM 
                        produtos p
                    INNER JOIN 
                        categorias c ON p.categoria_id = c.categoria_id;
                """
                cur = conn.execute(query)
                produtos = cur.fetchall()

                return {
                    "dados": [dict(produto) for produto in produtos]
                }
            
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Erro de banco de dados: {str(e)}"
            }
        
    def atualizar_produto(self, categoria: Categoria, produto: Produto) -> dict:
        if not isinstance(produto, Produto):
            return {"erro": "Objeto inválido."}

        try:
            busca = self.buscar_produto(produto.codigo)

            with self.connect_database() as conn:
                query = """
                    UPDATE 
                        produtos
                    SET 
                        nome_produto = ?,
                        categoria_id = ?,
                        preco_unitario = ?,
                        estoque = ?,
                        status = ?
                    WHERE 
                        codigo = ?
                """
                conn.execute(query,(
                    produto.nome_produto,
                    categoria.categoria_id,
                    produto.preco_unitario,
                    produto.estoque,
                    produto.status,
                    produto.codigo
                ))

                if busca is not None:
                    return {
                        "dados": {
                            "codigo": produto.codigo,
                            "categoria_id": categoria.categoria_id,
                            "nome": produto.nome_produto,
                            "preco_unitario": produto.preco_unitario,
                            "estoque": produto.estoque,
                            "status": produto.status
                        }
                    }
                else:
                    return None  
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Ocorreu um erro ao atualizar o produto: {str(e)}"
            }

    def total_estoque(self):
        try:
            with self.connect_database() as conn:
                query = """
                    SELECT
                        COUNT(codigo) AS produtos,
                        SUM(preco_unitario * estoque) AS valor_total_estoque
                    FROM
                        produtos
                """

                cur = conn.execute(query)
                valor_total = cur.fetchone()

                if valor_total['valor_total_estoque'] is None:
                    return {"valor_total_estoque": 0}
                else:
                    return {"valor_total_estoque": valor_total['valor_total_estoque']}

        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Ocorreu um erro ao atualizar o produto: {str(e)}"
            } 

    def total_produtos_ativos(self):
        try:
            with self.connect_database() as conn:
                query = """
                SELECT
                    COUNT(codigo) AS produtos_ativos
                FROM
                    produtos
                WHERE
                    status = 'ativo'
                """

                cur = conn.execute(query)
                produtos_ativos = cur.fetchone()
                return {"produto_ativos": produtos_ativos['produtos_ativos']}
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Ocorreu um erro ao atualizar o produto: {str(e)}"
            } 
