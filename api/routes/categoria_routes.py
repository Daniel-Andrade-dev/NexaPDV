from flask import jsonify, request, Blueprint
from api.services.categoria_service import CategoriaService
from api.models.categoria.categoria import Categoria
from api.enums.status_categoria import CategoriaDefault

categoria_bp = Blueprint("categoria", __name__)
categoria_service = CategoriaService()

@categoria_bp.route("/categorias", methods=["POST"])
def adicionar_categoria():
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"erro": "Corpo da requisição inválido"}), 400
        
        categoria = Categoria(
            categoria_id=None,
            nome=CategoriaDefault.DIVERSOS if payload['categoria'] == "" else payload['categoria'],
            status=payload['status']
        )

        resultado_service = categoria_service.adicionar_categoria(categoria=categoria)

        if "erro" not in resultado_service:
            return jsonify(resultado_service), 201
        return jsonify(resultado_service), 400
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@categoria_bp.route("/categorias/<int:categoria_id>", methods=["GET"])
def buscar_categoria(categoria_id):
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"erro": "Corpo da requisição inválido"}), 400

        resultado_service = categoria_service.buscar_categoria(
            payload['categoria'],
            categoria_id
        )

        if resultado_service is None:
            return jsonify({"erro": "Categoria não encontrada"}), 404
        return jsonify(resultado_service), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@categoria_bp.route("/categoria", methods=["GET"])
def listar_categorias():
    try:
        categorias = categoria_service.categorias_cadastradas()
        return jsonify(categorias), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500


@categoria_bp.route("/categorias/<int:categoria_id>", methods=["DELETE"])
def deletar_categoria(categoria_id: int):
    try:
        categoria_buscada = categoria_service.buscar_categoria(categoria_id=categoria_id)

        categoria = Categoria(
            categoria_id=categoria_id,
            nome=categoria_buscada['nome_categoria'],
            status=categoria_buscada['status']
        )

        resultado_service = categoria_service.deletar_categoria(categoria=categoria)

        return jsonify({
            "sucesso": True,
            "deletado": resultado_service
        }), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

