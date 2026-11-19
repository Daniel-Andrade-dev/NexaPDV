
from functools import wraps
import time
from api.classes.log_time_funcs import LogTimeFuncs


def resultados_tempo(tempo_execucao: float, nome_funcao: str) -> any:
    
    resultado = []
    resultado.append({"nome_funcao": nome_funcao, "tempo_execucao": tempo_execucao})

    modelo_arquivo = LogTimeFuncs.modelo_arquivo(resultado)
    resultado_geracao_arquivo = LogTimeFuncs.criar_arquivo(modelo_arquivo)

    return resultado_geracao_arquivo

def medir_tempo_execucao(func):
    @wraps(func)
    def wrappers(*args, **kwargs):

        tempo_inicial = time.perf_counter()
        resultado = func(*args, **kwargs)
        tempo_final = time.perf_counter()

        tempo_execucao = tempo_final - tempo_inicial

        resultados_tempo(
            tempo_execucao=tempo_execucao,
            nome_funcao=func.__name__
        )
        return resultado

    return wrappers