from flask import jsonify, request, Blueprint

from api.services.produto_service import ProdutoService
from api.models.produto.produto import Produto
from api.services.categoria_service import CategoriaService
from api.decorators.errors import verificar_erros_servidor

produto_bp = Blueprint("produto", __name__)
produto_service = ProdutoService()
categoria_service = CategoriaService()

@produto_bp.route("/produtos", methods=["POST"])
@verificar_erros_servidor
def cadastrar_produto():
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    produto = Produto(
        codigo_produto=None,
        categoria_id=payload['categoria_id'],
        nome_produto=payload['nome_produto'],
        preco_unitario_centavos=payload['preco_unitario_centavos'],
        estoque=payload['estoque'],
        status=payload['status'] 
    )

    resultado_service = produto_service.cadastrar_produto(payload['categoria_id'],produto)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 201


@produto_bp.route("/produtos/<int:codigo_produto>", methods=["GET"])
@verificar_erros_servidor
def buscar_produto(codigo_produto: int):
    resultado_service = produto_service.buscar_produto(codigo_produto)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 404)
    return jsonify(resultado_service), 200


@produto_bp.route("/produtos/<int:codigo_produto>", methods=["DELETE"])
@verificar_erros_servidor
def deletar_produto(codigo_produto: int):
    resultado_service = produto_service.deletar_produto(codigo_produto)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 404)
    return jsonify(resultado_service), 200

@produto_bp.route("/produtos/<int:codigo_produto>", methods=["PUT"])
@verificar_erros_servidor
def atualizar_produto(codigo_produto: int):
    payload = request.get_json()

    if not payload:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400
    
    produto = Produto(
        codigo_produto=codigo_produto,
        categoria_id=payload['categoria_id'],
        nome_produto=payload['nome_produto'],
        preco_unitario_centavos=payload['preco_unitario_centavos'],
        estoque=payload['estoque'],
        status=payload['status']
    )

    resultado_service = produto_service.atualizar_produto(payload['categoria_id'], produto)

    if "erro" in resultado_service:
        return jsonify(resultado_service), resultado_service.get("status", 400)
    return jsonify(resultado_service), 200
