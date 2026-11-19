from flask import jsonify, request, Blueprint

from api.services.relatorios_service.relatorio_venda_service import (
    RelatorioVendasService
)
from api.decorators.errors import verificar_erros_servidor

relatorio_venda_bp = Blueprint("relatorio_venda", __name__)
relatorio_venda_service = RelatorioVendasService()

@relatorio_venda_bp.route("/relatorios/vendas_iniciadas", methods=['GET'])
@verificar_erros_servidor
def vendas_iniciadas():
    resultado_service = relatorio_venda_service.vendas_iniciadas()
    return jsonify(resultado_service), 200

@relatorio_venda_bp.route("/relatorios/vendas_finalizadas", methods=['GET'])
@verificar_erros_servidor
def vendas_finalizadas():
    resultado_service = relatorio_venda_service.vendas_finalizadas()
    return jsonify(resultado_service), 200

@relatorio_venda_bp.route("/relatorios/buscar/vendas_iniciadas/<int:venda_iniciada_id>", methods=['GET'])
@verificar_erros_servidor
def buscar_vendas_iniciadas(venda_iniciada_id: int):
    resultado_service = relatorio_venda_service.buscar_vendas_iniciadas(venda_iniciada_id)
    if "erro" in resultado_service: return jsonify(
        resultado_service
    ), resultado_service.get("status", 404)
    else:
        return jsonify(resultado_service), 200

@relatorio_venda_bp.route("/relatorios/buscar/vendas_finalizadas/<int:venda_finalizada_id>", methods=['GET'])
@verificar_erros_servidor
def buscar_vendas_finalizadas(venda_finalizada_id: int):
    resultado_service = relatorio_venda_service.buscar_vendas_finalizadas(venda_finalizada_id)
    if "erro" in resultado_service: return jsonify(
        resultado_service
    ), resultado_service.get("status", 404)
    else:
        return jsonify(resultado_service), 200