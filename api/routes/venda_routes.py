from flask import jsonify, request, Blueprint

from api.models.venda.venda import VendaIniciada, VendaFinalizada
from api.services.venda_service import VendaService
from api.services.produto_service import ProdutoService
from api.services.caixa_service import CaixaService
from api.enums.status_venda import StatusVenda
from api.decorators.errors import verificar_erros_servidor
from api.services.relatorios_service.relatorio_venda_service import RelatorioVendasService
from datetime import datetime


venda_bp = Blueprint("venda", __name__)
venda_service = VendaService()
produto_service = ProdutoService()
caixa_service = CaixaService()
relatorio_venda_service = RelatorioVendasService()

@venda_bp.route("/vendas/iniciar_vendas/<int:caixa_id>", methods=["POST"])
@verificar_erros_servidor
def iniciar_vendas(caixa_id: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválida"}), 400

    itens_vendas = []

    for item in payload['itens']:
        venda = VendaIniciada(
            venda_iniciada_id=None,
            quantidade_venda=item['quantidade_venda'],
            horario_iniciada=datetime.now().strftime("%H:%M"),
            data_iniciada=datetime.now().strftime("%Y-%m-%d"),
            status=StatusVenda.ABERTA
        )

        itens_vendas.append({
            "venda_obj": venda,
            "codigo_produto": item['codigo_produto']
        })

    resultado_service = venda_service.iniciar_venda(itens_vendas, caixa_id)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 201

@venda_bp.route("/vendas/finalizar_vendas/<int:venda_iniciada_id>", methods=["POST"])
@verificar_erros_servidor
def finalizar_vendas(venda_iniciada_id: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválida"}), 400

    valor_total_centavos = relatorio_venda_service.buscar_vendas_iniciadas(venda_iniciada_id)

    if "erro" in valor_total_centavos:
        return jsonify(valor_total_centavos), valor_total_centavos.get("status", 400)

    venda_finalizada = VendaFinalizada(
        venda_finalizada_id=None,
        forma_pagamento=payload['forma_pagamento'],
        valor_total_centavos=valor_total_centavos['valor_total_centavos'],
        valor_pago_centavos=(
            payload['valor_dinheiro_centavos'] 
            if payload['forma_pagamento'] == "dinheiro"
            else valor_total_centavos['valor_total_centavos']
        ),
        status=StatusVenda.CONCLUIDA
    )

    resultado_service = venda_service.finalizar_venda(
        payload['caixa_id'],
        venda_finalizada,
        venda_iniciada_id,
        payload['valor_dinheiro_centavos']
    )

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 201


@venda_bp.route("/vendas/finalizar_vendas/pix/<int:venda_iniciada_id>", methods=["POST"])
@verificar_erros_servidor
def finalizar_vendas_pix(venda_iniciada_id: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválida"}), 400

    valor_total_centavos = relatorio_venda_service.buscar_vendas_iniciadas(venda_iniciada_id)

    if "erro" in valor_total_centavos:
        return jsonify(valor_total_centavos), valor_total_centavos.get("status", 400)
    
    venda_finalizada = VendaFinalizada(
        venda_finalizada_id=None,
        forma_pagamento=payload['forma_pagamento'],
        valor_total_centavos=valor_total_centavos['valor_total_centavos'],
        valor_pago_centavos=valor_total_centavos['valor_total_centavos'],
        status=StatusVenda.CONCLUIDA
    )

    resultado_service = venda_service.finalizar_venda_pix(payload['caixa_id'], venda_finalizada, venda_iniciada_id)

    if "erro" in resultado_service:
        return jsonify(resultado_service), 400
    return jsonify(resultado_service), 201

@venda_bp.route("/vendas/qrcode/pix", methods=['GET'])
@verificar_erros_servidor
def qrcode():
    return jsonify(venda_service.gerar_qrcode()), 200

@venda_bp.route("/vendas/cancelar_vendas/<int:venda_iniciada_id>", methods=["PUT"])
@verificar_erros_servidor
def cancelar_vendas(venda_iniciada_id: int):
    resultado_service = venda_service.cancelar_venda(venda_iniciada_id)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)

    return jsonify(resultado_service), 200