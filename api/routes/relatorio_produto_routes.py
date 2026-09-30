from flask import jsonify, Blueprint
from api.services.relatorios.relatorio_produto import RelatorioProdutos


produtos_relatorio = RelatorioProdutos()
relatorio_produto_bp = Blueprint("relatorio_produto", __name__)


@relatorio_produto_bp.route("/total_estoque", methods=['GET'])
def log_total_estoque():
    try:
        return jsonify(produtos_relatorio.total_estoque_produtos()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@relatorio_produto_bp.route("/produtos_ativos", methods=['GET'])
def log_total_produtos_ativos():
    try:
        return jsonify(produtos_relatorio.total_produtos_ativos()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500  