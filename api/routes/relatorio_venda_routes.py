from flask import jsonify, Blueprint
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
        return jsonify(vendas_relatorios.listar_vendas_finalizadas()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@relatorio_bp.route("/vendas_canceladas", methods=['GET'])
def logs_vendas_canceladas():
    try:
        return jsonify(vendas_relatorios.vendas_canceladas()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@relatorio_bp.route("/vendas_finalizadas/ticket_medio", methods=['GET'])
def log_ticket_medio_vendas_finalizadas():
    try:
        return jsonify(vendas_relatorios.ticket_medio_vendas_finalizadas()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@relatorio_bp.route("/total_vendas_canceladas", methods=['GET'])
def log_total_vendas_canceladas():
    try:
        return jsonify(vendas_relatorios.total_vendas_canceladas())
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@relatorio_bp.route("/total_vendas_iniciadas", methods=['GET'])
def log_total_vendas_iniciadas():
    try:
        return jsonify(vendas_relatorios.total_vendas_iniciadas())
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@relatorio_bp.route("/total_vendas_finalizadas", methods=['GET'])
def log_total_vendas_finalizadas():
    try:
        return jsonify(vendas_relatorios.total_vendas_finalizadas())
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500
