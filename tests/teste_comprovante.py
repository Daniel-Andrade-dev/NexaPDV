from datetime import datetime

itens = [
    {
        "nome_produto": "Arroz 5kg",
        "quantidade_venda": 2,
        "valor_total_produto": 30.00
    },
    {
        "nome_produto": "Feijão 1kg",
        "quantidade_venda": 3,
        "valor_total_produto": 21.00
    },
    {
        "nome_produto": "Leite 1L",
        "quantidade_venda": 4,
        "valor_total_produto": 20.00
    },
    {
        "nome_produto": "Café 500g",
        "quantidade_venda": 1,
        "valor_total_produto": 15.50
    }
]

def modelo_comprovante(itens):

    emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")

    produtos = ""

    for item in itens:
        produtos += (
            f"{item['nome_produto']:<20}"
            f"{item['quantidade_venda']:>4}   "
            f"R$ {item['valor_total_produto']:>8.2f}\n"
        )

    modelo = f"""
========================================
              NexaPDV
         COMPROVANTE DE VENDA
========================================

Venda Nº: {1}

Produto              Qtd       Valor
----------------------------------------
{produtos}----------------------------------------

Valor total:               R$ "teste"
Valor pago:                R$ "teste"
Troco:                     R$ "teste"

Forma de pagamento:
"teste"

----------------------------------------
Emissão do comprovante:
{emissao}

========================================
       Obrigado pela preferência!
             Volte sempre!
========================================
"""

    return modelo

import os


def criar_arquivo_comprovante(venda_id: int, comprovante: str):

    path = "comprovantes"

    os.makedirs(path, exist_ok=True)

    arquivo = f"{path}/comprovante_{venda_id}_teste.txt"

    with open(arquivo, "w", encoding="utf-8") as arq:
        arq.write(comprovante)

    return {
        "sucesso": True,
        "arquivo": arquivo
    }


comprovante = modelo_comprovante(itens)

resultado = criar_arquivo_comprovante(
    venda_id=1,
    comprovante=comprovante
)

print(resultado)