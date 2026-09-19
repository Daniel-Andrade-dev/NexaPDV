from flask import jsonify, request, Blueprint
from api.services.produto_service import ProdutoService
from api.models.produto.produto import Produto
from api.enums.status_categoria import CategoriaDefault
from api.services.categoria_service import CategoriaService

produto_bp = Blueprint("produto", __name__)
produto_service = ProdutoService()
categoria_service = CategoriaService()

@produto_bp.route("/produtos", methods=["POST"])
def cadastrar_produto():
    try:
        payload = request.get_json()

        if not payload:
            return jsonify({"erro": "Corpo da requisição inválido"}), 400

        categoria_buscada = categoria_service.buscar_categoria(payload['categoria'])

        if categoria_buscada is None or "erro" in categoria_buscada:
            return jsonify(categoria_buscada), 404

        produto = Produto(
            codigo=None,
            nome_produto=payload['nome_produto'],
            preco_unitario=payload['preco_unitario'],
            estoque=payload['estoque'],
            categoria=payload['categoria'],
            status=payload['status'] 
        )

        cadastrado = produto_service.cadastrar_produto(produto=produto)

        if "erro" in cadastrado:
            return jsonify(cadastrado), 400
        return jsonify(cadastrado), 201
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@produto_bp.route("/produtos", methods=["GET"])
def produtos_cadastrados():
    try:
        produtos = produto_service.produtos_cadastrados()

        if produtos:
            return jsonify(produtos), 200
        return jsonify({"erro": "Não há produtos no momento"}), 404
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500
    
@produto_bp.route("/produtos/<int:codigo>", methods=["GET"])
def buscar_produto(codigo: int):
    try:
        produto = produto_service.buscar_produto(codigo)

        if "erro" in produto:
            return jsonify(produto), 404
        return jsonify(produto), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500


@produto_bp.route("/produtos/<int:codigo>", methods=["DELETE"])
def deletar_produto(codigo: int):
    try:
        produto_buscado = produto_service.buscar_produto(codigo)

        if produto_buscado is None:
            return jsonify({"erro": "Produto não encontrado para exclusão."}), 404

        produto = Produto(
            produto_buscado['codigo'],
            produto_buscado['nome_produto'],
            produto_buscado['preco_unitario'],
            produto_buscado['estoque'],
            produto_buscado['categoria'],
            produto_buscado['status']
        )

        return jsonify({
            "sucesso": True,
            "deletado": produto_service.deletar_produto(produto)
        }), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500

@produto_bp.route("/produtos/<int:codigo>", methods=["PUT"])
def atualizar_produto(codigo: int):
    try:
        payload = request.get_json()

        produto_buscado = produto_service.buscar_produto(codigo)

        if produto_buscado is None:
            return jsonify({"erro": "Produto não encontrado para exclusão."}), 404

        produto = Produto(
            produto_buscado['codigo'],
            payload['nome_produto'],
            payload['preco_unitario'],
            payload['estoque'],
            payload['categoria'],
            payload['status']
        )

        resultado_service = produto_service.atualizar_produto(produto)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500
        