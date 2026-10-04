from flask import jsonify, request, Blueprint
from api.services.produto_service import ProdutoService
from api.models.produto.produto import Produto
from api.models.categoria.categoria import Categoria
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

        categoria_buscada = categoria_service.buscar_categoria_id(payload['categoria_id'])

        if categoria_buscada is None:
            return jsonify({"erro": "Categoria não encontrada"}), 404

        produto = Produto(
            codigo=None,
            categoria_id=categoria_buscada['categoria_id'],
            nome_produto=payload['nome_produto'],
            preco_unitario=payload['preco_unitario'],
            estoque=payload['estoque'],
            status=payload['status'] 
        )

        categoria = Categoria(
            categoria_id=categoria_buscada['categoria_id'],
            nome=categoria_buscada['nome'],
            status=categoria_buscada['status']
        )

        cadastrado = produto_service.cadastrar_produto(categoria,produto)

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
        return jsonify(produto_service.produtos_cadastrados()), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500
    
@produto_bp.route("/produtos/<int:codigo>", methods=["GET"])
def buscar_produto(codigo: int):
    try:
        produto = produto_service.buscar_produto(codigo)

        if not produto:
            return jsonify({"erro": "Produto não encontrado"}), 404
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
        categoria_buscada = categoria_service.buscar_categoria_id(payload['categoria_id'])

        if produto_buscado is None or categoria_buscada is None:
            return jsonify({"erro": "Produto ou categoria não encontrado para atualização."}), 404

        produto = Produto(
            codigo=produto_buscado['codigo'],
            categoria_id=categoria_buscada['categoria_id'],
            nome_produto=payload['nome_produto'],
            preco_unitario=payload['preco_unitario'],
            estoque=payload['estoque'],
            status=payload['status']
        )

        categoria = Categoria(
            categoria_id=categoria_buscada['categoria_id'],
            nome=categoria_buscada['nome'],
            status=categoria_buscada['status']    
        )

        resultado_service = produto_service.atualizar_produto(categoria, produto)

        if "erro" in resultado_service:
            return jsonify(resultado_service), 400
        return jsonify(resultado_service), 200
    except Exception as e:
        return jsonify({
            "msg": "Ocorreu um erro no servidor",
            "erro": str(e)
        }), 500
        