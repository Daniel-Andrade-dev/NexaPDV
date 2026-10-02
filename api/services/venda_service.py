from api.models.venda.venda import VendaFinalizada, VendaInicializada
from api.models.produto.produto import Produto
from api.enums.forma_pagamento import FormaPagamentos
from api.enums.status_produto import StatusProduto
from api.enums.status_venda import StatusVenda
from api.repository.venda_repository import VendaRepository
from api.services.produto_service import ProdutoService
from api.validator.validator import Validator
from datetime import datetime
import qrcode
import base64
import io

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
            "codigo_produto": produto.codigo,
            "nome_produto": produto.nome_produto,
            "preco_unitario": produto.preco_unitario,
            "quantidade_venda": venda.venda_quantidade,
            "horario_inicializada": venda.horario_inicializada,
            "data_inicializada": venda.data_inicializada,
            "valor_total_produto": round(produto.preco_unitario * venda.venda_quantidade, 2),
            "status": venda.status
        })
        return self.carrinho

    # A função e responsável por retorna apenas o que precisa do carrinho para API
    def carrinho_api(self, carrinho_atual: list[dict]) -> list:
        response = []
        for item in carrinho_atual:
            response.append({
                "codigo_produto": item['codigo_produto'],
                "nome_produto": item['nome_produto'],
                "preco_unitario": item['preco_unitario'],
                "quantidade_venda": item['quantidade_venda'],
                "valor_total_produto": item['valor_total_produto']
            })

        return response
    
    # A função e responsável por retorna apenas os dados que precisa para API
    def response_api(self, _response: list[dict]):
        response = []
        for item in _response:
            response.append({
                "sucesso": item['sucesso'],
                "carrinho": item['carrinho_atual'],
                "msg": item['msg'],
                "venda": item['venda']
            })

        return response

    def calcular_valor_total_venda(self) -> float:
        return round(sum(item['preco_unitario'] * item['quantidade_venda'] for item in self.carrinho), 2)

    def calcular_troco_e_verificar(self, valor_total, valor_dinheiro: float) -> dict | float:
        if valor_dinheiro < valor_total:
            return {"erro": f"Valor insuficiente. Faltam R${valor_total - valor_dinheiro:.2f}"}
        
        if valor_dinheiro == valor_total: return 0.0

        return round(valor_dinheiro - valor_total, 2)

    def buscar_venda_iniciada(self, venda_id) -> dict:
        return self.venda_repository.buscar_venda_inicializada(venda_id)

    def inicializar_venda(self, itens_vendas: list[dict]):

        carrinho_atual = self.carrinho
        valor_total = 0.0
        baixa_estoque = None
        response = []

        for item in itens_vendas:

            baixa_estoque = self.produto_service.baixa_estoque(
                item['produto_obj'],
                item['venda_obj']
            )

            if isinstance(baixa_estoque, dict) and "erro" in baixa_estoque:
                return baixa_estoque

            carrinho_atual = self.adicionar_ao_carrinho(
                item['venda_obj'],
                item['produto_obj']
            )

            if isinstance(carrinho_atual, dict) and "erro" in carrinho_atual:
                return carrinho_atual

            valor_total = self.calcular_valor_total_venda()

        response_carrinho = self.carrinho_api(carrinho_atual)

        resultado_repository = self.venda_repository.inicializar_vendas(
            carrinho_atual.copy(),
            valor_total
        )

        if isinstance(resultado_repository, dict) and "erro" in resultado_repository:
            return resultado_repository

        self.carrinho.clear()
        response.append({
            "sucesso": True,
            "msg": "Venda iniciada com sucesso",
            "carrinho_atual": response_carrinho,
            "venda": resultado_repository,
            "estoque": baixa_estoque['sucesso'],
        })

        return self.response_api(response)
            
    def cancelar_venda(self, venda_iniciada: VendaInicializada):
        if not isinstance(venda_iniciada, VendaInicializada):
            return {"erro": "Objeto inválido"}

        buscar_venda = self.buscar_venda_iniciada(venda_iniciada.venda_id)

        if buscar_venda['status'] == StatusVenda.CONCLUIDA:
            return {"erro": "Não e possível cancelar vendas concluídas"}

        if buscar_venda['status'] == StatusVenda.CANCELADA:
            return {"erro": "A venda já está cancelada. Tente novamente"}

        resultado_repository = self.venda_repository.cancelar_venda(venda_iniciada)

        return resultado_repository

    def finalizar_venda(self, venda_finalizada: VendaFinalizada, venda_iniciada: VendaInicializada, valor_dinheiro=None):

        if not isinstance(venda_finalizada, VendaFinalizada) or not isinstance(venda_iniciada, VendaInicializada):
            return {"erro": "Objeto inválido. Esperado tipo Venda"}

        buscar_venda = self.buscar_venda_iniciada(venda_iniciada.venda_id)

        if not buscar_venda: 
            return {"erro": "Venda não encontrada"}

        if buscar_venda['status'] == StatusVenda.CONCLUIDA:
            return {"erro": "Venda já está concluída. Tente novamente"}

        if buscar_venda['status'] == StatusVenda.CANCELADA:
            return {"erro": "Não e possível finalizar vendas canceladas"}

        troco = 0.0
        if venda_finalizada.forma_pagamento == FormaPagamentos.DINHEIRO:
            if not Validator.validar_negativos([valor_dinheiro]):
                return {"erro": "Informe valores acima de 0 para finalizar"}
            
            troco = self.calcular_troco_e_verificar(buscar_venda['valor_total'], valor_dinheiro)

            if isinstance(troco, dict) and "erro" in troco:
                return troco


        # Se a forma de pagamento não for dinheiro automaticamente será inserida no banco
        # Sendo débito ou crédito
        resultado_repository = self.venda_repository.finalizar_venda(
            venda_finalizada,
            buscar_venda['valor_total'],
            troco,
            horario_mock=datetime.now().strftime("%H:%M"),
            data_mock=datetime.now().strftime("%d/%m/%Y")
        )

        atualizar_status = self.venda_repository.atualizar_status_venda(venda_finalizada, venda_iniciada)

        if isinstance(atualizar_status, dict) and "erro" in atualizar_status:
            return atualizar_status
        
        return {
            "sucesso": True,
            "venda": resultado_repository,
            "status_venda_iniciada": atualizar_status
        }

    # def ler_imagem(self, path='qrcode.png'):
    #     with open(path, 'rb') as arq:
    #         img = arq.read()
    #     return img 

    def gerar_qrcode(self):
        img = qrcode.make("Pagamento feito com sucesso")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return img_base64

    def finalizar_venda_pix(self, venda_finalizada: VendaFinalizada, venda_iniciada: VendaInicializada):

        buscar_venda = self.buscar_venda_iniciada(venda_iniciada.venda_id)

        if buscar_venda['status'] == StatusVenda.CONCLUIDA:
            return {"erro": "Venda já está concluída. Tente novamente"}
        
        if buscar_venda['status'] == StatusVenda.CANCELADA:
            return {"erro": "Não e possível finalizar vendas canceladas"}

        if venda_finalizada.forma_pagamento != FormaPagamentos.PIX:
            return {"erro": "Apenas pagamentos em PIX são permitidos"}
        
        resultado_repository = self.venda_repository.finalizar_venda(
            venda_finalizada,
            buscar_venda['valor_total'],
            troco=0.0,
            horario_mock=datetime.now().strftime("%H:%M"),
            data_mock=datetime.now().strftime("%d/%m/%Y")
        )

        atualizar_status = self.venda_repository.atualizar_status_venda(venda_finalizada, venda_iniciada)

        if isinstance(atualizar_status, dict) and "erro" in atualizar_status:
            return atualizar_status

        return {
            "sucesso": True,
            "venda": resultado_repository,
            "qrcode": self.gerar_qrcode(),
            "status_venda": atualizar_status
        }
    
