from functools import wraps
from flask import jsonify
import sqlite3

# Decorador adicionado para não repetir as mesmas tratações de erros em cada rota.
def verificar_erros_servidor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({
                "msg": "Ocorreu um erro interno no servidor",
                "erro": str(e)
            }), 500

    return wrapper

# Decorador adicionado para não repetir as mesmas tratações de erros em cada função do repository.
def verificar_erros_banco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return jsonify({
                "msg": "Ocorreu um erro interno no banco de dados",
                "erro": str(e)
            }), 500
    return wrapper