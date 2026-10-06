from flask import jsonify, request, Blueprint
from api.models.venda.venda import VendaInicializada, VendaFinalizada
from api.models.produto.produto import Produto
from api.models.caixa.caixa import Caixa, PagamentosCaixa
from api.services.venda_service import VendaService
from api.services.produto_service import ProdutoService
from api.services.caixa_service import CaixaService
from api.enums.status_venda import StatusVenda
from datetime import datetime


venda_bp = Blueprint("venda", __name__)
venda_service = VendaService()
produto_service = ProdutoService()
caixa_service = CaixaService()

@venda_bp.route("/iniciar_venda/<int:caixa_id>", methods=["POST"])
def inicializar_venda(caixa_id: int):
    try:
        payload = request.get_json()

        if not payload or not payload['itens']:
            return jsonify({"erro": "Corpo da requisição inválida"}), 400

        resultado_caixa = caixa_service.buscar_caixa_id(caixa_id)

        if resultado_caixa is None:
            return jsonify({"erro": f"Caixa {caixa_id} não encontrado"}), 404
        
        itens_vendas = []

        for item in payload['itens']:
            produto_buscado = produto_service.buscar_produto(item['codigo_produto'])
            
            if not produto_buscado:
                return jsonify({"erro": "Produto não encontrado"}), 404

            venda = VendaInicializada(
                venda_id=None,
                horario_inicializada=datetime.now().strftime("%H:%M"),
                data_inicializada=datetime.now().strftime("%d/%m/%Y"),
                venda_quantidade=item['quantidade_venda'],
                status=StatusVenda.ABERTA
            )

            produto = Produto(
                produto_buscado['codigo'],
                produto_buscado['categoria'],
                produto_buscado['nome_produto'],
                produto_buscado['preco_unitario'],
                produto_buscado['estoque'],
                produto_buscado['status']
            )

            itens_vendas.append({
                "venda_obj": venda,
                "produto_obj": produto
            })

        caixa = Caixa(
            caixa_id=resultado_caixa['caixa_id'],
            valor_inicial=resultado_caixa['valor_inicial'],
            horario_aberto=resultado_caixa['horario_aberto'],
            data_aberto=resultado_caixa['data_aberto'],
            status=resultado_caixa['status']
        )
        
        resultado_service = venda_service.inicializar_venda(itens_vendas, caixa)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@venda_bp.route("/finalizar_venda/<int:venda_id>", methods=["POST"])
def finalizar_venda(venda_id: int):
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"erro": "Corpo da requisição inválida"}), 400

        busca_venda_iniciada = venda_service.buscar_venda_iniciada(venda_id)
        busca_caixa = caixa_service.buscar_caixa_id(payload['caixa_id'])

        if not busca_venda_iniciada:
            return jsonify({"erro": "Venda não encontrada"}), 404

        venda_finalizada = VendaFinalizada(
            id_venda=None,
            forma_pagamento=payload['forma_pagamento'],
            valor_total=busca_venda_iniciada['valor_total'],
            valor_pago=payload['valor_dinheiro'] if payload['forma_pagamento'] == 'dinheiro' else busca_venda_iniciada['valor_total'],
            status=StatusVenda.CONCLUIDA
        )

        venda_iniciada = VendaInicializada(
            venda_id=busca_venda_iniciada['venda_id'],
            venda_quantidade=busca_venda_iniciada['venda_quantidade'],
            horario_inicializada=busca_venda_iniciada['horario_inicializada'],
            data_inicializada=busca_venda_iniciada['data_inicializada'],
            status=busca_venda_iniciada['status']
        )

        caixa = Caixa(
            caixa_id=busca_caixa['caixa_id'],
            valor_inicial=busca_caixa['valor_inicial'],
            horario_aberto=busca_caixa['horario_aberto'],
            data_aberto=busca_caixa['data_aberto'],
            status=busca_caixa['status']
        )

        pagamentos_caixa = PagamentosCaixa(
            id=None,
            caixa_id=busca_caixa['caixa_id'],
            forma_pagamento=payload['forma_pagamento'],
            valor_pago=payload['valor_dinheiro'] if payload['forma_pagamento'] == 'dinheiro' else busca_venda_iniciada['valor_total'],
        )
        
        resultado_service = venda_service.finalizar_venda(
            caixa,
            pagamentos_caixa,
            venda_finalizada,
            venda_iniciada,
            payload['valor_dinheiro']
        )

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500
        

@venda_bp.route("/finalizar_venda/pix/<int:venda_id>", methods=["POST"])
def finalizar_venda_pix(venda_id: int):
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"erro": "Corpo da requisição inválida"}), 400

        busca_venda = venda_service.buscar_venda_iniciada(venda_id)

        if busca_venda is None:
            return jsonify({"erro": "Venda não encontrada"}), 404
        
        venda_finalizada = VendaFinalizada(
            id_venda=None,
            forma_pagamento=payload['forma_pagamento'],
            valor_total=busca_venda['valor_total'],
            valor_pago=busca_venda['valor_total'],
            status=StatusVenda.CONCLUIDA
        )

        venda_iniciada = VendaInicializada(
            venda_id=busca_venda['venda_id'],
            venda_quantidade=busca_venda['venda_quantidade'],
            horario_inicializada=busca_venda['horario_inicializada'],
            data_inicializada=busca_venda['data_inicializada'],
            status=busca_venda['status']
        )

        resultado_service = venda_service.finalizar_venda_pix(venda_finalizada, venda_iniciada)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500   

@venda_bp.route("/qrcode/pix", methods=['GET'])
def qrcode():
    return jsonify(venda_service.gerar_qrcode()), 200

@venda_bp.route("/cancelar_venda/<int:venda_id>", methods=["PUT"])
def cancelar_venda(venda_id: int):
    try:
        resultado_busca = venda_service.buscar_venda_iniciada(venda_id)

        if resultado_busca is None:
            return jsonify({"erro": "Venda não encontrada"}), 404

        venda_iniciada = VendaInicializada(
            resultado_busca['venda_id'],
            resultado_busca['venda_quantidade'],
            resultado_busca['horario_inicializada'],
            resultado_busca['data_inicializada'],
            StatusVenda.CANCELADA
        )

        resultado_service = venda_service.cancelar_venda(venda_iniciada)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500   
