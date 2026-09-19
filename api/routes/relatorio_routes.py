from flask import jsonify, request, Blueprint
from api.services.relatorios.relatorio_venda import RelatorioVendas



vendas_relatorios = RelatorioVendas()
relatorio_bp = Blueprint("relatorio", __name__)


@relatorio_bp.route("/vendas_iniciadas", methods=['GET'])
def logs_vendas_iniciadas():
    try:
        return jsonify(vendas_relatorios.listar_vendas_iniciadas()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@relatorio_bp.route("/vendas_finalizadas", methods=['GET'])
def logs_vendas_finalizadas():
    try:
        return jsonify(vendas_relatorios.listar_vendas_finalizas()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500