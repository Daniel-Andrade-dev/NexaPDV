import sqlite3 as sql

DB_NAME = "NexaPDV.db"



class Tabelas:

    @staticmethod
    def tabela_produtos():
        return """
            CREATE TABLE IF NOT EXISTS produtos (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto TEXT UNIQUE NOT NULL,
                preco_unitario NUMERIC(10,2) NOT NULL,
                estoque INTEGER NOT NULL,
                categoria TEXT,
                status TEXT DEFAULT "ativo" NOT NULL,
                FOREIGN KEY (categoria) REFERENCES categorias(nome_categoria)
            )
        """


    @staticmethod
    def tabela_categoria():
        return """
            CREATE TABLE IF NOT EXISTS categorias (
                categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT DEFAULT "diversos" UNIQUE,
                status TEXT DEFAULT "ativo" NOT NULL
            )
        """
    
    @staticmethod
    def tabela_vendas_inicializadas():
        return """
            CREATE TABLE IF NOT EXISTS vendas_inicializadas (
                venda_id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor_total NUMERIC(10,2) NOT NULL,
                venda_quantidade INTEGER NOT NULL,
                horario_inicializada TEXT NOT NULL,
                data_inicializada DATE NOT NULL,
                status TEXT DEFAULT "aberta" NOT NULL
            )
        """

    @staticmethod
    def tabela_itens_venda_inicializada():
        return """
            CREATE TABLE IF NOT EXISTS itens_venda_inicializada (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                codigo_produto INTEGER NOT NULL,
                venda_quantidade INTEGER NOT NULL,
                preco_unitario NUMERIC(10,2) NOT NULL,
                valor_total_produto NUMERIC(10,2) NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas_inicializadas(venda_id),
                FOREIGN KEY (codigo_produto) REFERENCES produtos(codigo)
            )
        """
    
    @staticmethod
    def tabela_vendas_finalizadas():
        return """
            CREATE TABLE IF NOT EXISTS vendas_finalizadas (
                id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                forma_pagamento TEXT NOT NULL,
                valor_total NUMERIC(10,2) NOT NULL,
                valor_pago NUMERIC(10,2) NOT NULL,
                status TEXT DEFAULT "concluida" NOT NULL,
                horario_finalizada TEXT NOT NULL,
                data_finalizada DATE NOT NULL
            )
        """




class ConnectionDataBase:

    def connect_sql(self):
        try:
            conn = sql.connect(DB_NAME)
            conn.row_factory = sql.Row
            return conn 
        except sql.InternalError as e:
            raise ValueError(f"Ocorreu um erro para realizar a conexão com o banco de dados >> {e}")

    def inicializar_tabelas(self):
        try:
            with self.connect_sql() as conn:
                conn.execute(Tabelas.tabela_produtos())
                conn.execute(Tabelas.tabela_vendas_inicializadas())
                conn.execute(Tabelas.tabela_vendas_finalizadas())
                conn.execute(Tabelas.tabela_categoria())
                conn.execute(Tabelas.tabela_itens_venda_inicializada())
            print("Tabelas inicializadas com sucesso !!!")
        except sql.Error as e:
            raise ValueError(f"Ocorreu um erro para inicializar as tabelas do banco >> {e}")

          
if __name__ == "__main__":
    conn = ConnectionDataBase()
    conn.inicializar_tabelas()