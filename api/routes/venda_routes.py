from flask import jsonify, request, Blueprint
from api.models.venda.venda import VendaInicializada, ItensVendasIniciada, VendaFinalizada
from api.models.produto.produto import Produto
from api.services.venda_service import VendaService
from api.services.produto_service import ProdutoService
from api.enums.status_venda import StatusVenda
from datetime import datetime


venda_bp = Blueprint("venda", __name__)
venda_service = VendaService()
produto_service = ProdutoService()

@venda_bp.route("/iniciar_venda", methods=["POST"])
def inicializar_venda():
    try:
        payload = request.get_json()

        if not payload or not payload['itens']:
            return jsonify({"erro": "Corpo da requisição inválida"}), 400

        itens_vendas = []

        for item in payload['itens']:
            produto_buscado = produto_service.buscar_produto(item['codigo_produto'])
            if not produto_buscado or "erro" in produto_buscado:
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
                produto_buscado['nome_produto'],
                produto_buscado['preco_unitario'],
                produto_buscado['estoque'],
                produto_buscado['categoria'],
                produto_buscado['status']
            )

            itens_vendas.append({
                "venda_obj": venda,
                "produto_obj": produto
            })

        resultado_service = venda_service.inicializar_venda(itens_vendas)

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


        resultado_service = venda_service.finalizar_venda(venda_finalizada, venda_iniciada, payload['valor_dinheiro'])

        if isinstance(resultado_service, dict) and "erro" in resultado_service:
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