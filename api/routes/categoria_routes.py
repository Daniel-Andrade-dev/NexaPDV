from flask import jsonify, request, Blueprint
from api.services.categoria_service import CategoriaService
from api.models.categoria.categoria import Categoria
from api.decorators.errors import verificar_erros_servidor

categoria_bp = Blueprint("categoria", __name__)
categoria_service = CategoriaService()


@categoria_bp.route("/categorias", methods=["POST"])
@verificar_erros_servidor
def adicionar_categoria():
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    categoria = Categoria(
        categoria_id=None,
        nome=payload['categoria'],
        status=payload['status'],
    )

    resultado_service = categoria_service.adicionar_categoria(categoria)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 201

@categoria_bp.route("/categorias/<int:categoria_id>", methods=["GET"])
@verificar_erros_servidor
def buscar_categoria(categoria_id: int):
    resultado_service = categoria_service.buscar_categoria_id(categoria_id)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 404)
    return jsonify(resultado_service), 200

@categoria_bp.route("/categorias", methods=["GET"])
@verificar_erros_servidor
def listar_categorias():
    return jsonify(categoria_service.categorias_cadastradas()), 200


@categoria_bp.route("/categorias/<int:categoria_id>", methods=["DELETE"])
@verificar_erros_servidor
def deletar_categoria(categoria_id: int):
    resultado_service = categoria_service.deletar_categoria(categoria_id)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 404)
    return jsonify(resultado_service), 200

@categoria_bp.route("/categorias/<int:categoria_id>", methods=["PUT"])
@verificar_erros_servidor
def atualizar_categoria(categoria_id: int):
    payload = request.get_json()
    
    categoria = Categoria(
        categoria_id=categoria_id,
        nome=payload['nome'],
        status=payload['status']
    )

    resultado_service = categoria_service.atualizar_categoria(categoria)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 200
