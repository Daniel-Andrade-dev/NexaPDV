from flask import jsonify, Blueprint

from api.services.relatorios_service.relatorio_produto_service import (
    RelatorioProdutosService
)
from api.decorators.errors import verificar_erros_servidor


relatorio_produto_bp = Blueprint("relatorio_produto", __name__)
relatorio_produto_service = RelatorioProdutosService()

@relatorio_produto_bp.route("/relatorios/produtos", methods=['GET'])
@verificar_erros_servidor
def produtos_cadastrados():
    resultado_service = relatorio_produto_service.produtos_cadastrados()
    return jsonify(resultado_service), 200