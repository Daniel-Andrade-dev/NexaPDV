from flask import jsonify, request, Blueprint
from api.models.caixa.caixa import Caixa, Sangrias, FechamentosCaixa
from api.services.caixa_service import CaixaService
from api.enums.status_caixa import StatusCaixa
from datetime import datetime

caixa_bp = Blueprint("caixa", __name__)
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

@caixa_bp.route("/pagamentos/dinheiro/<int:pagamento_id>", methods=['GET'])
def buscar_pagamentos_dinheiro(pagamento_id: int):
    try:
        pagamentos = caixa_service.buscar_pagamentos_dinheiro(pagamento_id)
        
        if isinstance(pagamentos, dict) and "erro" in pagamentos:
            return jsonify(pagamentos), 404        
        return jsonify(pagamentos), 200
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
     
@caixa_bp.route("/caixas/fechamento/<int:caixa_id>", methods=['POST'])
def fechamento_caixa(caixa_id: int):
    try:
        payload = request.get_json()

        buscar_caixa = caixa_service.buscar_caixa_id(caixa_id)

        if buscar_caixa is None:
            return jsonify({"erro": "Caixa não encontrado"}), 404

        caixa = Caixa(
            caixa_id=buscar_caixa['caixa_id'],
            valor_inicial=buscar_caixa['valor_inicial'],
            horario_aberto=buscar_caixa['horario_aberto'],
            data_aberto=buscar_caixa['data_aberto'],
            status=buscar_caixa['status']
        )
        
        fechamentos_caixa = FechamentosCaixa(
            fechamento_id=None,
            caixa_id=buscar_caixa['caixa_id'],
            valor_esperado=None,
            valor_contado=payload['valor_contado'],
            diferenca=None,
            data_fechamento=datetime.now().strftime("%d/%m/%Y"),
            horario_fechamento=datetime.now().strftime("%H:%M")
        )

        resultado_service = caixa_service.fechamento_caixa(caixa, fechamentos_caixa)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500  
    
@caixa_bp.route("/caixas/pagamentos", methods=['GET'])
def listar_pagamento_caixa():
    try:
        return jsonify(caixa_service.listar_pagamentos_caixa()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500  


@caixa_bp.route("/caixas", methods=['GET'])
def listar_caixas():
    try:
        return jsonify(caixa_service.listar_caixas()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500  
    

@caixa_bp.route("/caixas/sangrias/<int:caixa_id>", methods=['POST'])
def inserir_sangria(caixa_id: int):
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"erro": "Requisição inválida"}), 400

        caixa_buscado = caixa_service.buscar_caixa_id(caixa_id)

        if caixa_buscado is None:
            return jsonify({"erro": "Caixa não encontrado"}), 404

        sangria = Sangrias(
            sangria_id=None,
            caixa_id=caixa_buscado['caixa_id'],
            valor_retirado=payload['valor_retirado'],
            data_sangria=datetime.now().strftime("%d/%m/%Y"),
            horario_sangria=datetime.now().strftime("%H:%M")
        )

        resultado_service = caixa_service.inserir_sangria(sangria)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500 

    
@caixa_bp.route("/caixas/sangria/<int:caixa_id>", methods=['PUT'])
def realizar_sangria_caixa(caixa_id: int):
    try:
        payload = request.get_json()

        caixa_buscado = caixa_service.buscar_caixa_id(caixa_id)
        sangria_buscado = caixa_service.buscar_sangria_id(payload['sangria_id'])

        if caixa_buscado is None:
            return jsonify({"erro": "Caixa não encontrado"}), 404

        caixa = Caixa(
            caixa_id=caixa_buscado['caixa_id'],
            valor_inicial=caixa_buscado['valor_inicial'],
            horario_aberto=caixa_buscado['horario_aberto'],
            data_aberto=caixa_buscado['data_aberto'],
            status=caixa_buscado['status']
        )

        sangria = Sangrias(
            sangria_id=sangria_buscado['sangria_id'],
            caixa_id=caixa_buscado['caixa_id'],
            valor_retirado=sangria_buscado['valor_retirado'],
            data_sangria=sangria_buscado['data_sangria'],
            horario_sangria=sangria_buscado['horario_sangria']
        )

        resultado_service = caixa_service.sangria_caixa(sangria, caixa)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service)
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500   

@caixa_bp.route("/sangria/<int:sangria_id>", methods=['GET'])
def buscar_sangria_id(sangria_id: int):
    try:
        sangria = caixa_service.buscar_sangria_id(sangria_id)

        if sangria is None:
            return jsonify({"erro": "Sangria não encontrada"}), 404
        return jsonify(sangria), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500     

@caixa_bp.route("/sangria/valor_total/<int:caixa_id>", methods=['GET'])
def valor_total_sangria(caixa_id: int):
    try:
        return jsonify(caixa_service.total_valor_sangria(caixa_id)), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500 
