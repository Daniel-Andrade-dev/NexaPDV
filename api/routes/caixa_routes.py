from flask import jsonify, request, Blueprint
from api.models.caixa.caixa import Caixa
from api.services.caixa_service import CaixaService
from api.enums.status_caixa import StatusCaixa
from datetime import datetime

caixa_bp= Blueprint("caixa", __name__)
caixa_service = CaixaService()

@caixa_bp.route("/caixas", methods=['POST'])
def cadastrar_caixa():
    try:
        caixa = Caixa(
            caixa_id=None,
            valor_inicial=0,
            horario_aberto=None,
            data_aberto=None,
            status=StatusCaixa.FECHADO
        )

        resultado_service = caixa_service.cadastrar_caixa(caixa)
        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@caixa_bp.route("/caixas/<int:caixa_id>", methods=['GET'])
def buscar_caixa(caixa_id: int):
    try:
        caixa = caixa_service.buscar_caixa_id(caixa_id)

        if caixa is None:
            return jsonify({"erro": "Caixa não encontrado"}), 404
        return jsonify(caixa), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500  

@caixa_bp.route("/caixas/<int:caixa_id>", methods=['POST'])
def abertura_de_caixa(caixa_id: int):
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"erro": "Corpo da requisição inválido"}), 400

        buscar_caixa = caixa_service.buscar_caixa_id(caixa_id)

        if buscar_caixa is None:
            return jsonify({"erro": "Caixa não encontrado"}), 404

        caixa = Caixa(
            caixa_id=buscar_caixa['caixa_id'],
            valor_inicial=payload['valor_inicial'],
            horario_aberto=datetime.now().strftime("%H:%M"),
            data_aberto=datetime.now().strftime("%d/%m/%Y"),
            status=StatusCaixa.ABERTO
        )

        resultado_service = caixa_service.abertura_caixa(caixa)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500  

@caixa_bp.route("/caixas", methods=['GET'])
def listar_caixas_abertos():
    try:
        return jsonify(caixa_service.listar_caixas_abertos()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500  
