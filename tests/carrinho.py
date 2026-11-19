produtos = [
    {"codigo_produto": 1, "produto": "Camiseta Python", "preco": 34.45},
    {"codigo_produto": 2, "produto": "Caneca Dev", "preco": 50.00}
]

itens_api = [
    {
        "codigo_produto": 1,
        "quantidade_venda": 2
    },
    {
        "codigo_produto": 2,
        "quantidade_venda": 3
    }
]

def buscar_produto(codigo):
    for produto in produtos:
        if produto['codigo_produto'] == codigo:
            return produto 
    return None 

carrinho_atual_back = []

for item in itens_api:
    produto = buscar_produto(item['codigo_produto'])
    
    if produto:
        carrinho_atual_back.append({
            "codigo_produto": item['codigo_produto'],
            "produto": produto['produto'],
            "preco": produto['preco'],
            "quantidade_venda": item['quantidade_venda']
        })
    else:
        print(f"Aviso: Produto com código {item['codigo_produto']} não encontrado.")

print("=== CARRINHO ===")
total = 0
for item in carrinho_atual_back:
    subtotal = item['quantidade_venda'] * item['preco']
    total += subtotal

    print("Codigo produto:", item['codigo_produto'])
    print("Produto:", item['produto'])
    print("Preço:", item['preco'])
    print("Quantidade venda:", item['quantidade_venda'])
    print("Subtotal:", subtotal)
    print("-" * 20)

print("Valor total do carrinho:", total)