"""Interface gráfica (tkinter) para o controle do banco do NexaPDV.

Reproduz o mesmo menu do terminal em api/database/connections.py:
  1 - Criar tabelas
  2 - Deletar banco
  0 - Sair
"""

import io
import tkinter as tk
from contextlib import redirect_stdout
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk

from api.database.connections import ConnectionDataBase


class Cores:
    FUNDO = "#EEF1F5"          
    CABECALHO = "#26364A"      
    CABECALHO_TEXTO = "#FFFFFF"
    CABECALHO_SUBTEXTO = "#A9B8CB"
    CARTAO = "#FFFFFF"
    BORDA = "#CBD3DD"
    TEXTO = "#2B3340"
    TEXTO_SUAVE = "#6B7686"
    PRIMARIO = "#3F6E9E"      
    PRIMARIO_HOVER = "#335B85"
    PERIGO = "#A94F4F"         
    PERIGO_HOVER = "#8F4141"
    NEUTRO = "#E3E8EE"
    NEUTRO_HOVER = "#D3DAE3"

    LOG_FUNDO = "#F8FAFC"
    LOG_COMANDO = "#3F6E9E"
    LOG_ERRO = "#A94F4F"
    LOG_HORA = "#8A94A3"


FONTE = "Segoe UI"
FONTE_MONO = "Consolas"


class App:
    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("NexaPDV - Controle do Banco de Dados")
        raiz.geometry("760x520")
        raiz.minsize(640, 420)
        raiz.configure(bg=Cores.FUNDO)

        self._configurar_estilos()
        self._montar_cabecalho()
        self._montar_corpo()
        self._montar_rodape()

    def _configurar_estilos(self):
        estilo = ttk.Style(self.raiz)
        estilo.theme_use("clam") 

        base = {"font": (FONTE, 10, "bold"), "padding": (16, 8),
                "borderwidth": 0, "focusthickness": 0}

        for nome, normal, hover, texto in (
            ("Primario.TButton", Cores.PRIMARIO, Cores.PRIMARIO_HOVER, "#FFFFFF"),
            ("Perigo.TButton", Cores.PERIGO, Cores.PERIGO_HOVER, "#FFFFFF"),
            ("Neutro.TButton", Cores.NEUTRO, Cores.NEUTRO_HOVER, Cores.TEXTO),
        ):
            estilo.configure(nome, background=normal, foreground=texto, **base)
            estilo.map(nome, background=[("active", hover)])

    def _montar_cabecalho(self):
        cabecalho = tk.Frame(self.raiz, bg=Cores.CABECALHO)
        cabecalho.pack(fill="x")

        tk.Label(cabecalho, text="NexaPDV", bg=Cores.CABECALHO,
                 fg=Cores.CABECALHO_TEXTO,
                 font=(FONTE, 16, "bold")).pack(anchor="w", padx=20, pady=(14, 0))
        tk.Label(cabecalho, text="Controle do Banco de Dados",
                 bg=Cores.CABECALHO, fg=Cores.CABECALHO_SUBTEXTO,
                 font=(FONTE, 10)).pack(anchor="w", padx=20, pady=(0, 14))

    def _montar_corpo(self):
        corpo = tk.Frame(self.raiz, bg=Cores.FUNDO)
        corpo.pack(fill="both", expand=True, padx=20, pady=16)

        acoes = tk.Frame(corpo, bg=Cores.FUNDO)
        acoes.pack(fill="x", pady=(0, 12))

        ttk.Button(acoes, text="Criar tabelas", style="Primario.TButton",
                   command=self.criar_tabelas).pack(side="left", padx=(0, 8))
        ttk.Button(acoes, text="Deletar banco", style="Perigo.TButton",
                   command=self.deletar_banco).pack(side="left", padx=(0, 8))

        ttk.Button(acoes, text="Sair", style="Neutro.TButton",
                   command=self.raiz.destroy).pack(side="right")
        ttk.Button(acoes, text="Limpar log", style="Neutro.TButton",
                   command=self.limpar_log).pack(side="right", padx=(0, 8))

        tk.Label(corpo, text="Registro de operações", bg=Cores.FUNDO,
                 fg=Cores.TEXTO, font=(FONTE, 10, "bold")).pack(anchor="w", pady=(0, 6))

        moldura = tk.Frame(corpo, bg=Cores.CARTAO, highlightthickness=1,
                           highlightbackground=Cores.BORDA)
        moldura.pack(fill="both", expand=True)

        self.saida = scrolledtext.ScrolledText(
            moldura, wrap="word", state="disabled", relief="flat",
            bg=Cores.LOG_FUNDO, fg=Cores.TEXTO, font=(FONTE_MONO, 10),
            padx=12, pady=10, borderwidth=0, highlightthickness=0,
        )
        self.saida.pack(fill="both", expand=True)

        self.saida.tag_configure("hora", foreground=Cores.LOG_HORA)
        self.saida.tag_configure("comando", foreground=Cores.LOG_COMANDO,
                                 font=(FONTE_MONO, 10, "bold"))
        self.saida.tag_configure("erro", foreground=Cores.LOG_ERRO)

    def _montar_rodape(self):
        rodape = tk.Frame(self.raiz, bg=Cores.NEUTRO)
        rodape.pack(fill="x", side="bottom")

        self.status = tk.StringVar(value="Pronto")
        tk.Label(rodape, textvariable=self.status, bg=Cores.NEUTRO,
                 fg=Cores.TEXTO_SUAVE, font=(FONTE, 9),
                 anchor="w").pack(fill="x", padx=20, pady=6)

    def _escrever(self, texto, tag=None):
        self.saida.configure(state="normal")
        self.saida.insert("end", texto, tag)
        self.saida.see("end")
        self.saida.configure(state="disabled")

    def limpar_log(self):
        self.saida.configure(state="normal")
        self.saida.delete("1.0", "end")
        self.saida.configure(state="disabled")
        self.status.set("Log limpo")

    def executar(self, rotulo, metodo):
        buffer = io.StringIO()
        erro = None

        try:
            conexao = ConnectionDataBase()
            with redirect_stdout(buffer):
                getattr(conexao, metodo)()
        except Exception as e: 
            erro = e

        agora = datetime.now().strftime("%H:%M:%S")
        self._escrever(f"[{agora}] ", "hora")
        self._escrever(f"{rotulo}\n", "comando")

        saida = buffer.getvalue()
        if saida:
            self._escrever(saida if saida.endswith("\n") else saida + "\n")

        if erro:
            self._escrever(f"Erro: {erro}\n", "erro")
            self.status.set(f"Falha em: {rotulo}")
        else:
            self.status.set(f"Concluído: {rotulo} ({agora})")

        self._escrever("\n")

    def criar_tabelas(self):
        self.executar("Criar tabelas", "inicializar_tabelas")

    def deletar_banco(self):
        confirmado = messagebox.askyesno(
            "Confirmar exclusão",
            "Isso apagará o banco de dados do NexaPDV.\n\nDeseja continuar?",
            icon="warning",
        )
        if confirmado:
            self.executar("Deletar banco", "deletar_banco")


if __name__ == "__main__":
    raiz = tk.Tk()
    App(raiz)
    raiz.mainloop()