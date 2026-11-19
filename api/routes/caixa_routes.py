from flask import jsonify, request, Blueprint

from api.models.caixa.caixa import Caixa, Sangrias, FechamentosCaixa
from api.services.caixa_service import CaixaService
from api.enums.status_caixa import StatusCaixa
from api.decorators.errors  import verificar_erros_servidor
from datetime import datetime

caixa_bp = Blueprint("caixa", __name__)
caixa_service = CaixaService()

@caixa_bp.route("/caixas", methods=['POST'])
@verificar_erros_servidor
def cadastrar_caixa():
    caixa = Caixa(
        caixa_id=None,
        valor_inicial_centavos=0,
        horario_aberto=None,
        data_aberto=None,
        status=StatusCaixa.FECHADO
    )

    resultado_service = caixa_service.cadastrar_caixa(caixa)
    if "erro" in resultado_service:
        return jsonify(resultado_service), 400
    return jsonify(resultado_service), 201

@caixa_bp.route("/caixas/<int:caixa_id>", methods=['GET'])
@verificar_erros_servidor
def buscar_caixa(caixa_id: int):
    resultado_service = caixa_service.buscar_caixa_id(caixa_id)
    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 404)
    return jsonify(resultado_service), resultado_service.get("status", 200)


@caixa_bp.route("/caixas/<int:caixa_id>", methods=['POST'])
@verificar_erros_servidor
def abertura_de_caixa(caixa_id: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    resultado_service = caixa_service.abertura_caixa(caixa_id, payload['valor_inicial_centavos'])

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 201

@caixa_bp.route("/caixas/fechamento/<int:caixa_id>", methods=['POST'])
@verificar_erros_servidor
def fechamento_caixa(caixa_id: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400
    
    fechamento_caixa = FechamentosCaixa(
        fechamento_id=None,
        caixa_id=caixa_id,
        valor_esperado_centavos=None,
        valor_contado_centavos=payload['valor_contado_centavos'],
        diferenca_centavos=None,
        data_fechamento=datetime.now().strftime("%Y-%m-%d"),
        horario_fechamento=datetime.now().strftime("%H:%M")
    )

    resultado_service = caixa_service.fechamento_caixa(caixa_id, fechamento_caixa)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 201

@caixa_bp.route("/caixas/sangrias/<int:caixa_id>", methods=['POST'])
@verificar_erros_servidor
def inserir_sangria(caixa_id: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    sangria = Sangrias(
        sangria_id=None,
        caixa_id=caixa_id,
        valor_retirado_centavos=payload['valor_retirado_centavos'],
        data_sangria=datetime.now().strftime("%Y-%m-%d"),
        horario_sangria=datetime.now().strftime("%H:%M")
    )

    resultado_service = caixa_service.inserir_sangria(caixa_id, sangria)

    if "erro" in resultado_service:
        return jsonify(resultado_service), 400
    return jsonify(resultado_service), 201


@caixa_bp.route("/caixas/sangria/<int:caixa_id>", methods=['PUT'])
@verificar_erros_servidor
def realizar_sangria_caixa(caixa_id: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400
    
    resultado_service = caixa_service.sangria_caixa(payload['sangria_id'], caixa_id)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service)

@caixa_bp.route("/caixas/sangria/<int:sangria_id>", methods=['GET'])
@verificar_erros_servidor
def buscar_sangria_id(sangria_id: int):
    sangria = caixa_service.buscar_sangria_id(sangria_id)

    if sangria is None:
        return jsonify({"erro": "Sangria não encontrada"}), 404
    return jsonify(sangria), 200