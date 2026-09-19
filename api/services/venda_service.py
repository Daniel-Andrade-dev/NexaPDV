from api.models.venda.venda import ItensVendasIniciada, VendaFinalizada, VendaInicializada
from api.models.produto.produto import Produto
from api.enums.forma_pagamento import FormaPagamentos
from api.enums.status_produto import StatusProduto
from api.enums.status_venda import StatusVenda
from api.repository.venda_repository import VendaRepository
from api.services.produto_service import ProdutoService
from api.validator.validator import Validator
from datetime import datetime
# import qrcode
# from PIL import Image

class VendaService:
    
    def __init__(self, venda_repository=None):
        self.venda_repository = venda_repository or VendaRepository()
        self.produto_service = ProdutoService()
        self.carrinho = []

    
    def adicionar_ao_carrinho(self, venda: VendaInicializada, produto: Produto) -> list:
        if not Validator.validar_campos([produto.codigo, venda.venda_quantidade]):
            return {"erro": "Preenche os campos para iniciar a VENDA"}
        
        if not Validator.validar_negativos([venda.venda_quantidade]):
            return {"erro": "Informa valores acima de 0 para quantidade"}
        
        if produto.status == StatusProduto.INATIVO:
            return {"erro": f"Produto {produto.nome_produto} está inativo no estoque"}

        self.carrinho.append({
            "nome_produto": produto.nome_produto,
            "preco_unitario": produto.preco_unitario,
            "quantidade_venda": venda.venda_quantidade,
            "horario_inicializada": venda.horario_inicializada,
            "data_inicializada": venda.data_inicializada,
            "valor_total_produto": round(produto.preco_unitario * venda.venda_quantidade, 2),
            "status": venda.status
        })
        return self.carrinho
    
    def calcular_valor_total_venda(self) -> float:
        return round(sum(item['preco_unitario'] * item['quantidade_venda'] for item in self.carrinho), 2)

    def calcular_troco_e_verificar(self, valor_total, valor_dinheiro: float) -> dict | float:
        if valor_dinheiro < valor_total:
            return {"erro": f"Valor insuficiente. Faltam R${valor_total - valor_dinheiro:.2f}"}
        
        if valor_dinheiro == valor_total:
            return 0.0

        return round(valor_dinheiro - valor_total, 2)

    def buscar_venda_iniciada(self, venda_id) -> dict:
        return self.venda_repository.buscar_venda_inicializada(venda_id)

    def inicializar_venda(self, itens_vendas: list[dict]):

        carrinho_atual = self.carrinho
        valor_total = 0.0
        baixa_estoque = None

        for item in itens_vendas:
            carrinho_atual = self.adicionar_ao_carrinho(
                item['venda_obj'],
                item['produto_obj']
            )

            if isinstance(carrinho_atual, dict) and "erro" in carrinho_atual:
                return carrinho_atual

            valor_total = self.calcular_valor_total_venda()

            baixa_estoque = self.produto_service.baixa_estoque(
                item['produto_obj'],
                item['venda_obj']
            )

            if isinstance(baixa_estoque, dict) and "erro" in baixa_estoque:
                return baixa_estoque

        carrinho_api = []

        for item in carrinho_atual:
            carrinho_api.append({
                "nome_produto": item['nome_produto'],
                "preco_unitario": item['preco_unitario'],
                "quantidade_venda": item['quantidade_venda'],
                "valor_total_produto": item['valor_total_produto']
            })

        resultado_repository = self.venda_repository.inicializar_vendas(
            carrinho_atual.copy(),
            valor_total
        )

        if isinstance(resultado_repository, dict) and "erro" in resultado_repository:
            return resultado_repository

        self.carrinho.clear()
        return {
            "success": True,
            "message": "Venda inicializada com sucesso.",
            "carrinho_atual": carrinho_api,
            "data": resultado_repository,
            "estoque": baixa_estoque
        }
            

    def finalizar_venda(self, venda_finalizada: VendaFinalizada, venda_iniciada: VendaInicializada, valor_dinheiro=None):

        if not isinstance(venda_finalizada, VendaFinalizada) or not isinstance(venda_iniciada, VendaInicializada):
            return {"erro": "Objeto inválido. Esperado tipo Venda"}

        buscar_venda = self.buscar_venda_iniciada(venda_iniciada.venda_id)

        if not buscar_venda: 
            return {"erro": "Venda não encontrada"}

        if buscar_venda['status'] == StatusVenda.CONCLUIDA:
            return {"erro": "Venda já está concluída. Tente novamente"}

        troco = 0.0
        if venda_finalizada.forma_pagamento == FormaPagamentos.DINHEIRO:
            troco = self.calcular_troco_e_verificar(buscar_venda['valor_total'], valor_dinheiro)

            if isinstance(troco, dict) and "erro" in troco:
                return troco

        resultado_repository = self.venda_repository.finalizar_venda(
            venda_finalizada,
            buscar_venda['valor_total'],
            horario_mock=datetime.now().strftime("%H:%M"),
            data_mock=datetime.now().strftime("%d/%m/%Y")
        )

        atualizar_status = self.venda_repository.atualizar_status_venda(venda_finalizada, venda_iniciada)

        if isinstance(atualizar_status, dict) and "erro" in atualizar_status:
            return atualizar_status
        
        return {
            "sucesso": True,
            "venda": resultado_repository,
            "troco": troco,
            "status_venda": atualizar_status
        }

    # Em desenvolvimento
    def finalizar_venda_pix(self):
        pass
    
