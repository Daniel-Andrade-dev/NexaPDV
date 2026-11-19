from api.models.venda.venda import VendaFinalizada, VendaIniciada
from api.models.produto.produto import Produto
from api.models.caixa.caixa import Caixa, PagamentosCaixa
from api.enums.forma_pagamento import FormaPagamentos
from api.enums.status_produto import StatusProduto
from api.enums.status_venda import StatusVenda
from api.enums.status_caixa import StatusCaixa
from api.services.produto_service import ProdutoService
from api.classes.comprovante import Comprovante
from api.services.caixa_service import CaixaService
from api.classes.desconto import Desconto
from api.classes.pagamento_invalido import PagamentoInvalido
from api.classes.response_format import VendaResponseFormat, CarrinhoResponseFormat
from api.services.relatorios_service.relatorio_venda_service import RelatorioVendasService
from api.repository.venda_repository import VendaRepository
from api.decorators.time_func import medir_tempo_execucao
from api.validator.validator import Validator, ValidatorVenda, ValidatorCaixa
from api.services.carrinho import Carrinho
from datetime import datetime
import qrcode
import base64
import io

class VendaService:
 
    def __init__(self) -> None:
        self.venda_repository = VendaRepository()
        self.relatorio_venda_service = RelatorioVendasService()
        self.produto_service = ProdutoService()
        self.caixa_service = CaixaService()
        self.comprovante = Comprovante()
        self.validar_status = ValidatorVenda()
        self.validar_caixa = ValidatorCaixa()

    def calcular_troco_e_verificar(self, valor_total_centavos: int, valor_dinheiro_centavos: int) -> dict | int:
        if valor_dinheiro_centavos < valor_total_centavos:
            return {
                "status": 400,
                "erro": f"Valor insuficiente. Faltam R${valor_total_centavos - valor_dinheiro_centavos / 100:.2f}"
            }
        
        if valor_dinheiro_centavos == valor_total_centavos: return 0

        return valor_dinheiro_centavos - valor_total_centavos

    @medir_tempo_execucao
    def iniciar_venda(self, itens_vendas: list[dict], caixa_id: int) -> dict | None | list:

        validator_caixa = self.validar_caixa.validar_status(caixa_id)
        carrinho_obj = Carrinho() # []
        response = []

        if "erro" in validator_caixa: return validator_caixa

        if not itens_vendas: return {
            "status": 400,
            "erro": "Informe pelo menos um item ao carrinho"
        }

        for item in itens_vendas:
            buscar_produto = self.produto_service.buscar_produto(
                item["codigo_produto"]
            )

            if "erro" in buscar_produto: return buscar_produto

            if buscar_produto['status'] == StatusProduto.INATIVO:
                return {
                    "status": 400,
                    "erro": f"Produto {buscar_produto['nome_produto']} está inativo no estoque"
                }
            
            baixa_estoque = self.produto_service.baixa_estoque(
                buscar_produto['codigo_produto'], 
                item['venda_obj']
            )

            if isinstance(baixa_estoque, dict) and "erro" in baixa_estoque: return baixa_estoque
            
            produto_obj = Produto(
                codigo_produto=buscar_produto['codigo_produto'],
                categoria_id=buscar_produto['categoria_id'],
                nome_produto=buscar_produto['nome_produto'],
                preco_unitario_centavos=buscar_produto['preco_unitario_centavos'],
                estoque=buscar_produto['estoque'],
                status=buscar_produto['status']
            )

            carrinho_obj.adicionar_ao_carrinho(item['venda_obj'], produto_obj)
        
        subtotal_centavos = carrinho_obj.obter_valor_total_carrinho()
        desconto_centavos = Desconto.aplicar_desconto(subtotal_centavos) 
        valor_total_centavos = subtotal_centavos - desconto_centavos

        resultado_repository = self.venda_repository.inserir_venda_iniciada(
            carrinho_obj.itens,
            desconto_centavos,
            subtotal_centavos,
            valor_total_centavos
        ) 

        if isinstance(resultado_repository, dict) and "erro" in resultado_repository: return resultado_repository
        
        response_carrinho = CarrinhoResponseFormat.response_api_carrinho(carrinho_obj.itens)
        inserir_itens = self.venda_repository.inserir_itens_venda(carrinho_obj.itens, resultado_repository['venda_iniciada_id'])

        if isinstance(inserir_itens, dict) and "erro" in inserir_itens: return inserir_itens

        carrinho_obj.limpar_carrinho()
        response.append({
            "sucesso": True,
            "msg": "Venda iniciada com sucesso",
            "carrinho": response_carrinho,
            "venda": resultado_repository,
        })

        return VendaResponseFormat.response_api_venda_iniciada(response)

    @medir_tempo_execucao
    def cancelar_venda(self, venda_iniciada_id: int) -> dict:

        validator_venda = self.validar_status.validar_status_venda_cancelada(venda_iniciada_id)
        itens = self.venda_repository.buscar_itens_venda(venda_iniciada_id)

        if "erro" in validator_venda: return validator_venda

        if not itens: return {
            "status": 404,
            "erro": f"Não há itens na venda ID {validator_venda['venda_iniciada']['venda_iniciada_id']}"
        }

        venda_iniciada = VendaIniciada(
            venda_iniciada_id=validator_venda['venda_iniciada']['venda_iniciada_id'],
            quantidade_venda=validator_venda['venda_iniciada']['quantidade_venda'],
            horario_iniciada=validator_venda['venda_iniciada']['horario_iniciada'],
            data_iniciada=validator_venda['venda_iniciada']['data_iniciada'],
            status=validator_venda['venda_iniciada']['status']
        )

        response_produto = []
        for item in itens:
            response = self.produto_service.retorno_estoque(
                item['codigo_produto'],
                venda_iniciada
            )

            response_produto.append(response)
            
        return {
            "resultado_venda_cancelada": self.venda_repository.cancelar_venda(validator_venda['venda_iniciada']['venda_iniciada_id']),
            "resultado_produto": response_produto
        }

    @medir_tempo_execucao
    def finalizar_venda(
            self,
            caixa_id: int,
            venda_finalizada: VendaFinalizada, 
            venda_iniciada_id: int, 
            valor_dinheiro=None
        ) -> dict | None:

        validator_venda = self.validar_status.validar_status(venda_iniciada_id)
        validator_caixa = self.validar_caixa.validar_status(caixa_id)
        buscar_itens_venda = self.venda_repository.buscar_itens_venda(venda_iniciada_id)
        forma_pagamento_invalido = PagamentoInvalido().verificar_pagamento_invalido(venda_finalizada.forma_pagamento)
        response = []

        if "erro" in validator_caixa: return validator_caixa

        if "erro" in validator_venda: return validator_venda

        if isinstance(forma_pagamento_invalido, dict) and "erro" in forma_pagamento_invalido:
            return forma_pagamento_invalido

        troco_centavos = 0
        if venda_finalizada.forma_pagamento == FormaPagamentos.DINHEIRO:
            if not Validator.validar_negativos([valor_dinheiro]):return {
                "status": 400,
                "erro": "Informe valores acima de 0 para finalizar a venda"
            }
                       
            troco_centavos = self.calcular_troco_e_verificar(
                validator_venda['venda_iniciada']['valor_total_centavos'],
                valor_dinheiro
            )

            if isinstance(troco_centavos, dict) and "erro" in troco_centavos:
                return troco_centavos

        caixa = Caixa(
            caixa_id=validator_caixa['caixa']['caixa_id'],
            valor_inicial_centavos=validator_caixa['caixa']['valor_inicial_centavos'],
            horario_aberto=validator_caixa['caixa']['horario_aberto'],
            data_aberto=validator_caixa['caixa']['data_aberto'],
            status=validator_caixa['caixa']['status']
        )

        venda_iniciada = VendaIniciada(
            venda_iniciada_id=venda_iniciada_id,
            quantidade_venda=validator_venda['venda_iniciada']['quantidade_venda'],
            horario_iniciada=validator_venda['venda_iniciada']['horario_iniciada'],
            data_iniciada=validator_venda['venda_iniciada']['data_iniciada'],
            status=validator_venda['venda_iniciada']['status']
        )

        resultado_repository = self.venda_repository.finalizar_venda(
            venda=venda_finalizada,
            valor_total_centavos=validator_venda['venda_iniciada']['valor_total_centavos'],
            troco_centavos=troco_centavos,
            horario=datetime.now().strftime("%H:%M"),
            data=datetime.now().strftime("%Y-%m-%d")
        )

        if "erro" in resultado_repository:
            return resultado_repository

        pagamentos_caixa = PagamentosCaixa(
            pagamento_id=None,
            caixa_id=validator_caixa['caixa']['caixa_id'],
            forma_pagamento=resultado_repository['pagamento']['forma'],
            valor_total_venda_centavos=validator_venda['venda_iniciada']['valor_total_centavos'],
            valor_pago_centavos=resultado_repository['pagamento']['valor_pago_centavos']
        )

        registro_caixa = self.caixa_service.inserir_pagamentos_caixa(caixa, pagamentos_caixa, troco_centavos)
        status_venda_iniciada = self.venda_repository.atualizar_status_venda(venda_iniciada_id)

        comprovante = self.comprovante.modelo_comprovante(
            itens=buscar_itens_venda,
            troco_centavos=troco_centavos,
            subtotal_centavos=validator_venda['venda_iniciada']['subtotal_centavos'],
            desconto_centavos=validator_venda['venda_iniciada']['desconto_centavos'],
            venda_iniciada=venda_iniciada,
            valor_total_centavos=validator_venda['venda_iniciada']['valor_total_centavos'],
            venda_finalizada=venda_finalizada
        )

        if isinstance(comprovante, dict) and "erro" in comprovante:
            return comprovante

        response.append({
            "sucesso": True,
            "venda": resultado_repository,
            "msg_comprovante": self.comprovante.criar_arquivo_comprovante(venda_iniciada, comprovante),
            "status_venda_iniciada": status_venda_iniciada,
            "resultado_pagamento_caixa": registro_caixa
        })

        return VendaResponseFormat.response_api_venda_finalizada(response)

    @medir_tempo_execucao
    def gerar_qrcode(self) -> dict:
        img = qrcode.make("Pagamento feito com sucesso")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return {"qrcode":img_base64}

    @medir_tempo_execucao
    def finalizar_venda_pix(self, caixa_id: int, venda_finalizada: VendaFinalizada, venda_iniciada_id: int) -> dict | None:

        validator_venda = self.validar_status.validar_status(venda_iniciada_id)
        validator_caixa = self.validar_caixa.validar_status(caixa_id)
        buscar_itens_venda = self.venda_repository.buscar_itens_venda(venda_iniciada_id)
        forma_pagamento_invalido_pix = PagamentoInvalido().verificar_pagamento_pix_invalido(venda_finalizada.forma_pagamento)
        response = []

        if "erro" in validator_caixa:
            return validator_caixa

        if "erro" in validator_venda:
            return validator_venda

        if isinstance(forma_pagamento_invalido_pix, dict) and "erro" in forma_pagamento_invalido_pix:
            return forma_pagamento_invalido_pix

        troco_centavos = 0

        caixa = Caixa(
            caixa_id=validator_caixa['caixa']['caixa_id'],
            valor_inicial_centavos=validator_caixa['caixa']['valor_inicial_centavos'],
            horario_aberto=validator_caixa['caixa']['horario_aberto'],
            data_aberto=validator_caixa['caixa']['data_aberto'],
            status=validator_caixa['caixa']['status']
        )

        venda_iniciada = VendaIniciada(
            venda_iniciada_id=venda_iniciada_id,
            quantidade_venda=validator_venda['venda_iniciada']['quantidade_venda'],
            horario_iniciada=validator_venda['venda_iniciada']['horario_iniciada'],
            data_iniciada=validator_venda['venda_iniciada']['data_iniciada'],
            status=validator_venda['venda_iniciada']['status']
        )

        resultado_repository = self.venda_repository.finalizar_venda(
            venda=venda_finalizada,
            valor_total_centavos=validator_venda['venda_iniciada']['valor_total_centavos'],
            troco_centavos=troco_centavos,
            horario=datetime.now().strftime("%H:%M"),
            data=datetime.now().strftime("%Y-%m-%d")
        )

        if "erro" in resultado_repository:
            return resultado_repository

        pagamentos_caixa = PagamentosCaixa(
            pagamento_id=None,
            caixa_id=validator_caixa['caixa']['caixa_id'],
            forma_pagamento=resultado_repository['pagamento']['forma'],
            valor_total_venda_centavos=validator_venda['venda_iniciada']['valor_total_centavos'],
            valor_pago_centavos=resultado_repository['pagamento']['valor_pago_centavos']
        )

        registro_caixa = self.caixa_service.inserir_pagamentos_caixa(caixa, pagamentos_caixa, troco_centavos)
        status_venda_iniciada = self.venda_repository.atualizar_status_venda(venda_iniciada_id)

        comprovante = self.comprovante.modelo_comprovante(
            itens=buscar_itens_venda,
            troco_centavos=troco_centavos,
            subtotal_centavos=validator_venda['venda_iniciada']['subtotal_centavos'],
            desconto_centavos=validator_venda['venda_iniciada']['desconto_centavos'],
            venda_iniciada=venda_iniciada,
            valor_total_centavos=validator_venda['venda_iniciada']['valor_total_centavos'],
            venda_finalizada=venda_finalizada
        )

        if isinstance(comprovante, dict) and "erro" in comprovante:
            return comprovante

        response.append({
            "sucesso": True,
            "venda": resultado_repository,
            "msg_comprovante": self.comprovante.criar_arquivo_comprovante(venda_iniciada, comprovante),
            "status_venda_iniciada": status_venda_iniciada,
            "resultado_pagamento_caixa": registro_caixa
        })

        return VendaResponseFormat.response_api_venda_finalizada(response)