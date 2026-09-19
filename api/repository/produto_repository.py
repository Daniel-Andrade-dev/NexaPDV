import sqlite3 as sql
from api.database.connections import ConnectionDataBase
from api.models.produto.produto import Produto
from api.models.venda.venda import VendaInicializada

"""
CRUD CONTROLE DE ESTOQUE PARA O PDV
"""

class ProdutoRepository:

    def connect_database(self):
        return ConnectionDataBase().connect_sql()

    def inserir_produto(self, produto: Produto) -> dict:
        if not isinstance(produto, Produto):
            return {"erro": "Objeto inválido. Esperado tipo Produto."}

        try:
            with self.connect_database() as conn:
                query = """
                    INSERT INTO produtos
                    (nome_produto, preco_unitario, estoque, categoria, status)
                    VALUES(?,?,?,?,?)
                """
                cur = conn.execute(query,(
                    produto.nome_produto,
                    produto.preco_unitario,
                    produto.estoque,
                    produto.categoria,
                    produto.status
                ))

            return {
                "sucesso": True,
                "dados": {
                    "codigo": cur.lastrowid,
                    "nome": produto.nome_produto,
                    "preco_unitario": produto.preco_unitario,
                    "estoque": produto.estoque,
                    "categoria": produto.categoria,
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
                        codigo,
                        nome_produto,
                        preco_unitario,
                        estoque,
                        categoria,
                        status
                    FROM
                        produtos
                    WHERE
                        codigo = ?
                """
                cur = conn.execute(query, (codigo,))
                produto = cur.fetchone()

                if produto is not None:
                    return {
                        "codigo": produto["codigo"],
                        "nome_produto": produto["nome_produto"],
                        "preco_unitario": produto["preco_unitario"],
                        "estoque": produto["estoque"],
                        "categoria": produto["categoria"],
                        "status": produto["status"]
                    }
                return {"erro": "Produto não encontrado"}
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

            if novo_estoque < 0:
                return {"erro": "Não há estoque suficiente do produto."}

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

                return cur.rowcount > 0
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

            if busca is None:
                return {"erro": "Produto não encontrado para exclusão."}

            with self.connect_database() as conn:
                query = """
                DELETE
                    FROM
                        produtos
                    WHERE
                        codigo = ?
                """

                cur = conn.execute(query, (produto.codigo,))

                return cur.rowcount > 0
                
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
                        codigo,                      
                        nome_produto,
                        preco_unitario,
                        estoque,
                        categoria,
                        status
                    FROM 
                        produtos
                    ORDER BY preco_unitario ASC
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
        
    def atualizar_produto(self, produto: Produto) -> dict:
        if not isinstance(produto, Produto):
            return {"sucesso": False, "dados": None, "erro": "Objeto inválido."}

        try:
            busca = self.buscar_produto(produto.codigo)

            if busca is None:
                return {"erro": "Produto não encontrado para atualização."}

            with self.connect_database() as conn:
                query = """
                    UPDATE 
                        produtos
                    SET 
                        nome_produto = ?,
                        preco_unitario = ?,
                        estoque = ?,
                        categoria = ?,
                        status = ?
                    WHERE 
                        codigo = ?
                """
                conn.execute(query,(
                    produto.nome_produto,
                    produto.preco_unitario,
                    produto.estoque,
                    produto.categoria,
                    produto.status,
                    produto.codigo
                ))

                return {
                    "dados": {
                        "codigo": produto.codigo,
                        "nome": produto.nome_produto,
                        "preco_unitario": produto.preco_unitario,
                        "estoque": produto.estoque,
                        "categoria": produto.categoria,
                        "status": produto.status
                    }
                }
                
        except sql.Error as e:
            return {
                "sucesso": False,
                "dados": None,
                "erro": f"Ocorreu um erro ao atualizar o produto: {str(e)}"
            }