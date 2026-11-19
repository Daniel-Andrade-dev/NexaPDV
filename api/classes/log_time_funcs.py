from pathlib import Path
from datetime import datetime

class LogTimeFuncs:

    @staticmethod
    def criar_arquivo(modelo_arquivo) -> Path:
        pasta = Path("monitoramento_funcoes") #Nome da pasta
        pasta.mkdir(exist_ok=True)

        arquivo = pasta / "monitoramento_funcoes.txt"
        with open(arquivo, "a", encoding="utf-8") as arq:
            arq.write(modelo_arquivo)

        return arquivo  

    @staticmethod
    def modelo_arquivo(dados_retornados: list) -> str:

        if not dados_retornados:
            raise ValueError("Não a dados retornados para criar o arquivo")

        linhas = [
            "==================================================\n",
            "        MONITORAMENTO DE FUNÇÕES NEXAPDV\n",
            "==================================================\n"
        ]

        for dados in dados_retornados:
            linhas.append(
                f"Monitoramento feito em: {datetime.now().strftime("%d/%m/%Y")} as {datetime.now().strftime("%H:%M")}\n"
                "\n"
                "--------------------------------------------------\n"
                f"Função: {dados['nome_funcao']}()\n"
                f"Tempo de execução: {dados['tempo_execucao']:.3f} segundos\n"
                f"Camada: Em desenvolvimento\n"
                f"Arquivo: Em desenvolvimento\n"
                "\n"
                "==================================================\n"
            )

        return "".join(linhas)



