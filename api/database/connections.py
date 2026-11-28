import sqlite3 as sql
import os

DB_NAME = "NexaPDV.db"

class Tabelas:

    # Categoria não e obrigatoria
    @staticmethod
    def tabela_produtos():
        return """
            CREATE TABLE IF NOT EXISTS produtos (
                codigo_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria_id INTEGER,
                nome_produto TEXT UNIQUE NOT NULL,
                preco_unitario_centavos INTEGER NOT NULL,
                estoque INTEGER NOT NULL,
                status TEXT DEFAULT "ativo" NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
            );
        """

    @staticmethod
    def tabela_categoria():
        return """
            CREATE TABLE IF NOT EXISTS categorias (
                categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT DEFAULT "diversos" UNIQUE,
                status TEXT DEFAULT "ativa" NOT NULL
            );
        """

    @staticmethod
    def tabela_caixa():
        return """
            CREATE TABLE IF NOT EXISTS caixas (
                caixa_id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor_inicial_centavos INTEGER DEFAULT 0,
                data_aberto DATE,
                horario_aberto TEXT,
                status TEXT DEFAULT "fechado"
            );
        """

    @staticmethod
    def tabela_sangria():
        return """
            CREATE TABLE IF NOT EXISTS sangrias (
                sangria_id INTEGER PRIMARY KEY AUTOINCREMENT,
                caixa_id INTEGER NOT NULL,
                valor_retirado_centavos INTEGER NOT NULL,
                data_sangria DATE NOT NULL,
                horario_sangria TEXT NOT NULL,
                FOREIGN KEY (caixa_id) REFERENCES caixas(caixa_id)
            );
        """
    
    @staticmethod
    def tabela_pagamentos_caixa():
        return """
            CREATE TABLE IF NOT EXISTS pagamentos_caixa (
                pagamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
                caixa_id INTEGER NOT NULL,
                forma_pagamento TEXT NOT NULL,
                valor_total_venda_centavos INTEGER NOT NULL,
                valor_pago_centavos INTEGER NOT NULL,
                troco_centavos INTEGER DEFAULT 0,
                FOREIGN KEY (caixa_id) REFERENCES caixas(caixa_id)
            );
        """
    
    @staticmethod
    def tabela_fechamentos_caixa():
        return """
            CREATE TABLE IF NOT EXISTS fechamentos_caixa (
                fechamento_id INTEGER PRIMARY KEY AUTOINCREMENT,
                caixa_id INTEGER NOT NULL,
                valor_esperado_centavos INTEGER NOT NULL,
                valor_contado_centavos INTEGER NOT NULL,
                diferenca_centavos INTEGER NOT NULL,
                data_fechamento DATE NOT NULL,
                horario_fechamento TEXT NOT NULL,
                FOREIGN KEY (caixa_id) REFERENCES caixas(caixa_id)
            );
        """
    
    @staticmethod
    def tabela_vendas_iniciadas():
        return """
            CREATE TABLE IF NOT EXISTS vendas_iniciadas (
                venda_iniciada_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subtotal_centavos INTEGER NOT NULL,
                desconto_centavos INTEGER NOT NULL,
                valor_total_centavos INTEGER NOT NULL,
                quantidade_venda INTEGER NOT NULL,
                horario_iniciada TEXT NOT NULL,
                data_iniciada DATE NOT NULL,
                status TEXT DEFAULT "aberta" NOT NULL
            );
        """

    @staticmethod
    def tabela_itens_venda_iniciada():
        return """
            CREATE TABLE IF NOT EXISTS itens_venda_iniciada (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_iniciada_id INTEGER NOT NULL,
                codigo_produto INTEGER NOT NULL,
                quantidade_venda INTEGER NOT NULL,
                preco_unitario_centavos INTEGER NOT NULL,
                valor_total_produto_centavos INTEGER NOT NULL,
                FOREIGN KEY (venda_iniciada_id) REFERENCES vendas_iniciadas(venda_iniciada_id),
                FOREIGN KEY (codigo_produto) REFERENCES produtos(codigo_produto)
            );
        """
    
    @staticmethod
    def tabela_vendas_finalizadas():
        return """
            CREATE TABLE IF NOT EXISTS vendas_finalizadas (
                venda_finalizada_id INTEGER PRIMARY KEY AUTOINCREMENT,
                forma_pagamento TEXT NOT NULL,
                valor_total_centavos INTEGER NOT NULL,
                valor_pago_centavos INTEGER NOT NULL,
                status TEXT DEFAULT "concluida" NOT NULL,
                horario_finalizada TEXT NOT NULL,
                data_finalizada DATE NOT NULL
            );
        """


"""
Como o SQLite3 não existe DROP DATABASE.
O uso da lib OS ajuda para remover o arquivo .db
"""

class ConnectionDataBase:

    def connect_sql(self):
        try:
            conn = sql.connect(DB_NAME)
            conn.row_factory = sql.Row
            conn.execute("PRAGMA foreign_key = ON;")
            return conn 
        except sql.InternalError as e:
            raise ValueError(f"Ocorreu um erro para realizar a conexão com o banco de dados >> {e}")
        
    def deletar_banco(self) -> None:
        if not os.path.exists(DB_NAME):
            print(f"[!] Banco '{DB_NAME}' não encontrado, nada para deletar.")
            return

        os.remove(DB_NAME)
        print(f"[OK] Banco '{DB_NAME}' deletado com sucesso.")

    def tabelas_dict(self) -> dict:
        return {
            "tabela_produto": Tabelas.tabela_produtos(),
            "tabela_categoria": Tabelas.tabela_categoria(),
            "tabela_vendas_iniciada": Tabelas.tabela_vendas_iniciadas(),
            "tabela_vendas_finalizadas": Tabelas.tabela_vendas_finalizadas(),
            "tabela_itens_venda": Tabelas.tabela_itens_venda_iniciada(),
            "tabela_caixas": Tabelas.tabela_caixa(),
            "tabela_fechamentos_caixa": Tabelas.tabela_fechamentos_caixa(),
            "tabela_pagamentos_caixa": Tabelas.tabela_pagamentos_caixa(),
            "tabela_sangrias": Tabelas.tabela_sangria()
        }
    
    def inicializar_tabelas(self) -> dict:
        tabelas = self.tabelas_dict()

        try:
            if os.path.exists(DB_NAME):
                print("[i] Tabelas já estão criadas.")
                return 
            
            with self.connect_sql() as conn:
                for tabela in tabelas.values():
                    conn.execute(tabela)
            print(f"[OK] {len(tabelas)} tabelas criadas com sucesso.")
        except sql.Error as e:
            raise ValueError(f"Ocorreu um erro para criar as tabelas do banco >> {e}")