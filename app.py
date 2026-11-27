from flask import Flask
from flask_cors import CORS

from api.routes.caixa_routes import caixa_bp
from api.routes.categoria_routes import categoria_bp
from api.routes.produto_routes import produto_bp
from api.routes.venda_routes import venda_bp
from api.routes.relatorio_venda_routes import relatorio_venda_bp
from api.routes.relatorio_produto_routes import relatorio_produto_bp
from api.routes.relatorio_caixas_routes import relatorio_caixas_bp

BLUEPRINTS = [
    caixa_bp,
    categoria_bp,
    produto_bp,
    venda_bp,
    relatorio_caixas_bp,
    relatorio_produto_bp,
    relatorio_venda_bp
]

def create_app() -> Flask:
    app = Flask(__name__)
    app.json.sort_keys = False
    CORS(app)
    
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True
    )
