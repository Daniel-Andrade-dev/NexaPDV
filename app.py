from flask import Flask
from flask_cors import CORS

from api.routes.caixa_routes import caixa_bp
from api.routes.categoria_routes import categoria_bp
from api.routes.produto_routes import produto_bp
from api.routes.venda_routes import venda_bp
from api.routes.relatorio_venda_routes import relatorio_venda_bp
from api.routes.relatorio_produto_routes import relatorio_produto_bp
from api.routes.relatorio_caixas_routes import relatorio_caixas_bp

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(produto_bp)
    app.register_blueprint(caixa_bp)
    app.register_blueprint(venda_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(relatorio_venda_bp)
    app.register_blueprint(relatorio_produto_bp)
    app.register_blueprint(relatorio_caixas_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True
    )
