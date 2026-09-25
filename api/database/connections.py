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


            
    def inserir_produtos(self):
        produtos = [
            ("Arroz 5kg", 28.90, 50, "Alimentos", "ativo"),
            ("Feijão 1kg", 8.50, 80, "Alimentos", "ativo"),
            ("Macarrão 500g", 4.99, 100, "Alimentos", "ativo"),
            ("Açúcar 1kg", 4.79, 70, "Alimentos", "ativo"),
            ("Café 500g", 16.90, 60, "Alimentos", "ativo"),
            ("Leite Integral 1L", 5.49, 90, "Bebidas", "ativo"),
            ("Leite em Pó 400g", 18.90, 40, "Alimentos", "ativo"),
            ("Óleo de Soja 900ml", 7.99, 75, "Alimentos", "ativo"),
            ("Farinha de Trigo 1kg", 5.99, 65, "Alimentos", "ativo"),
            ("Farofa 250g", 6.50, 45, "Alimentos", "ativo"),

            ("Refrigerante Cola 2L", 9.99, 50, "Bebidas", "ativo"),
            ("Refrigerante Guaraná 2L", 8.99, 55, "Bebidas", "ativo"),
            ("Água Mineral 500ml", 2.50, 120, "Bebidas", "ativo"),
            ("Suco de Laranja 1L", 7.90, 40, "Bebidas", "ativo"),
            ("Energético 473ml", 10.90, 35, "Bebidas", "ativo"),

            ("Chocolate ao Leite 90g", 6.99, 80, "Doces", "ativo"),
            ("Chocolate Branco 90g", 7.49, 70, "Doces", "ativo"),
            ("Bala de Morango 100g", 4.50, 100, "Doces", "ativo"),
            ("Biscoito Recheado", 3.99, 90, "Alimentos", "ativo"),
            ("Biscoito Cream Cracker", 5.49, 65, "Alimentos", "ativo"),

            ("Sabonete", 2.99, 100, "Higiene", "ativo"),
            ("Shampoo 350ml", 14.90, 50, "Higiene", "ativo"),
            ("Condicionador 350ml", 15.90, 45, "Higiene", "ativo"),
            ("Creme Dental 90g", 6.49, 80, "Higiene", "ativo"),
            ("Escova de Dentes", 8.90, 60, "Higiene", "ativo"),

            ("Papel Higiênico 4un", 7.99, 70, "Limpeza", "ativo"),
            ("Detergente 500ml", 2.49, 100, "Limpeza", "ativo"),
            ("Sabão em Pó 1kg", 12.90, 50, "Limpeza", "ativo"),
            ("Amaciante 2L", 11.90, 45, "Limpeza", "ativo"),
            ("Desinfetante 500ml", 5.90, 80, "Limpeza", "ativo"),

            ("Caderno 100 folhas", 12.90, 40, "Papelaria", "ativo"),
            ("Caneta Azul", 1.99, 200, "Papelaria", "ativo"),
            ("Caneta Preta", 1.99, 180, "Papelaria", "ativo"),
            ("Lápis HB", 1.50, 150, "Papelaria", "ativo"),
            ("Borracha Branca", 1.99, 120, "Papelaria", "ativo"),

            ("Camiseta Básica", 39.90, 30, "Vestuário", "ativo"),
            ("Calça Jeans", 89.90, 20, "Vestuário", "ativo"),
            ("Meia Esportiva", 9.90, 60, "Vestuário", "ativo"),
            ("Boné", 29.90, 35, "Vestuário", "ativo"),
            ("Chinelo", 24.90, 40, "Vestuário", "ativo"),

            ("Mouse USB", 29.90, 30, "Eletrônicos", "ativo"),
            ("Teclado USB", 49.90, 25, "Eletrônicos", "ativo"),
            ("Fone de Ouvido", 39.90, 35, "Eletrônicos", "ativo"),
            ("Cabo USB-C", 19.90, 50, "Eletrônicos", "ativo"),
            ("Carregador USB", 34.90, 40, "Eletrônicos", "ativo"),

            ("Prato de Cerâmica", 14.90, 30, "Casa", "ativo"),
            ("Copo de Vidro", 6.90, 80, "Casa", "ativo"),
            ("Caneca", 12.90, 50, "Casa", "ativo"),
            ("Panela 2L", 49.90, 20, "Casa", "ativo"),
            ("Frigideira", 39.90, 25, "Casa", "ativo"),
        ]

        try:
            with self.connect_sql() as conn:
                conn.executemany("""
                    INSERT INTO produtos
                    (nome_produto, preco_unitario, estoque, categoria, status)
                    VALUES (?, ?, ?, ?, ?)
                """, produtos)

            print(f"{len(produtos)} produtos cadastrados com sucesso!")

        except sql.IntegrityError as e:
            raise ValueError(
                f"Erro de integridade ao inserir produtos >> {e}"
            )

        except sql.Error as e:
            raise ValueError(
                f"Erro ao inserir produtos >> {e}"
            )


    def inserir_categorias(self):
        categorias = [
            ("Alimentos", "ativo"),
            ("Bebidas", "ativo"),
            ("Doces", "ativo"),
            ("Higiene", "ativo"),
            ("Limpeza", "ativo"),
            ("Papelaria", "ativo"),
            ("Vestuário", "ativo"),
            ("Eletrônicos", "ativo"),
            ("Casa", "ativo"),
        ]

        try:
            with self.connect_sql() as conn:
                conn.executemany("""
                    INSERT INTO categorias
                    (nome, status)
                    VALUES (?, ?)
                """, categorias)

            print(f"{len(categorias)} categorias cadastradas com sucesso!")

        except sql.IntegrityError as e:
            raise ValueError(
                f"Erro de integridade ao inserir categorias >> {e}"
            )

        except sql.Error as e:
            raise ValueError(
                f"Erro ao inserir categorias >> {e}"
            )
    
if __name__ == "__main__":
    conn = ConnectionDataBase()
    conn.inicializar_tabelas()
    conn.inserir_produtos()
    conn.inserir_categorias()