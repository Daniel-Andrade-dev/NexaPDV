from api.repository.relatorios_repository.relatorio_produtos_repository import RelatorioProdutosRepository
from api.classes.convert_precos import ConvertPrecos

class RelatorioProdutosService:

    def __init__(self):
        self.relatorio_produto_repository = RelatorioProdutosRepository()

    def tratar_dados_produtos(self, dados_retornados: list[dict]) -> tuple[dict] | list[dict]:
        return {
            "qtd_produtos": len(dados_retornados)
        },[{
            "codigo_produto": dados['codigo_produto'],
            "categoria": dados['categoria'] if dados['categoria'] is not None else "Sem categoria",
            "produto": dados['nome_produto'],
            "preco_unitario": ConvertPrecos().convert_centavos(dados['preco_unitario_centavos']),
            "estoque": dados['estoque'],
            "status": dados['status']
        } for dados in dados_retornados]

    def produtos_cadastrados(self):
        dados = self.relatorio_produto_repository.produtos_cadastrados()
        if dados != []:
            return self.tratar_dados_produtos(dados) 
        else:
            return {"msg": "Não há produtos cadastrados no momento"}