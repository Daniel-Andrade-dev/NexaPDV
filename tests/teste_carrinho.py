produtos = [
    {"codigo": 1, "produto": "Teste", "preco": 59.99},
    {"codigo": 2, "produto": "Teste2", "preco": 23.87}
]

itens_json = [
    {"codigo": 1, "quantidade": 5},
    {"codigo": 2, "quantidade": 4},
    {"codigo": 1, "quantidade": 9}
]

mapa_precos = {p["codigo"]: p["preco"] for p in produtos}

total = sum(item["quantidade"] * mapa_precos[item["codigo"]] for item in itens_json)

print(f"Total: R$ {total:.2f}")





