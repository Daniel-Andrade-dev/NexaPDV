from flask import jsonify, Blueprint

from api.services.relatorios_service.relatorios_caixas_service import (
    RelatoriosCaixasService
)
from api.decorators.errors import verificar_erros_servidor



relatorio_caixas_bp = Blueprint("relatorio_caixas", __name__)
relatorio_caixas_service = RelatoriosCaixasService()


@relatorio_caixas_bp.route("/relatorios/caixas_cadastrados", methods=['GET'])
@verificar_erros_servidor
def caixas_cadastrados():
    resultado_service = relatorio_caixas_service.caixas_cadastrados()
    return jsonify(resultado_service), 200


@relatorio_caixas_bp.route("/relatorios/caixas/pagamentos", methods=['GET'])
@verificar_erros_servidor
def pagamentos_caixas():
    resultado_service = relatorio_caixas_service.pagamentos_caixas()
    return jsonify(resultado_service), 200

@relatorio_caixas_bp.route("/relatorios/caixas/buscar_pagamento/<int:pagamento_id>", methods=['GET'])
@verificar_erros_servidor
def buscar_pagamento(pagamento_id: int):
    return jsonify(relatorio_caixas_service.buscar_pagamentos_id(pagamento_id))