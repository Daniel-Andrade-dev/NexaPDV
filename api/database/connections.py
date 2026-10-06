import sqlite3 as sql

DB_NAME = "NexaPDV.db"



class Tabelas:

    @staticmethod
    def tabela_produtos():
        return """
            CREATE TABLE IF NOT EXISTS produtos (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria_id INTEGER NOT NULL,
                nome_produto TEXT UNIQUE NOT NULL,
                preco_unitario NUMERIC(10,2) NOT NULL,
                estoque INTEGER NOT NULL,
                status TEXT DEFAULT "ativo" NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
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
    def tabela_caixa():
        return """
            CREATE TABLE IF NOT EXISTS caixas (
                caixa_id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor_inicial NUMERIC(10,2) DEFAULT 0.0,
                data_aberto DATE,
                horario_aberto TEXT,
                status TEXT DEFAULT "fechado"
            )
        """

    @staticmethod
    def tabela_pagamentos_caixa():
        return """
            CREATE TABLE IF NOT EXISTS pagamentos_caixa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caixa_id INTEGER NOT NULL,
                forma_pagamento TEXT NOT NULL,
                valor_pago NUMERIC(10,2) NOT NULL,
                FOREIGN KEY (caixa_id) REFERENCES caixas(caixa_id)
            )
        """
    
    @staticmethod
    def tabela_total_caixa():
        return """
            CREATE TABLE IF NOT EXISTS total_caixa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caixa_id INTEGER NOT NULL,
                valor_total_venda NUMERIC(10,2) NOT NULL,
                valor_esperado NUMERIC(10,2) NOT NULL,
                valor_contado NUMERIC(10,2) NOT NULL,
                diferenca NUMERIC(10,2) NOT NULL,
                data_fechamento DATE NOT NULL,
                horario_fechamento TEXT NOT NULL,
                FOREIGN KEY (caixa_id) REFERENCES caixas(caixa_id)
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
        tabelas = {
            "tabela_produto": Tabelas.tabela_produtos(),
            "tabela_categoria": Tabelas.tabela_categoria(),
            "tabela_vendas_iniciada": Tabelas.tabela_vendas_inicializadas(),
            "tabela_vendas_finalizadas": Tabelas.tabela_vendas_finalizadas(),
            "tabela_itens_venda": Tabelas.tabela_itens_venda_inicializada(),
            "tabela_caixas": Tabelas.tabela_caixa(),
            "tabela_total_caixass": Tabelas.tabela_total_caixa(),
            "tabela_pagamentos_caixa": Tabelas.tabela_pagamentos_caixa()
        }
        try:
            with self.connect_sql() as conn:
                for tabela in tabelas.values():
                    conn.execute(tabela)
            print("Tabelas inicializadas com sucesso !!!")
        except sql.Error as e:
            raise ValueError(f"Ocorreu um erro para inicializar as tabelas do banco >> {e}")

          
if __name__ == "__main__":
    conn = ConnectionDataBase()
    conn.inicializar_tabelas()