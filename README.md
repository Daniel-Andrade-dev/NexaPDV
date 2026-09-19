# Null PDV

API de um sistema de **Ponto de Venda (PDV)** desenvolvido com o objetivo de estudar e simular o funcionamento básico de um sistema de supermercado.

## 🎯 Objetivo do projeto

O **Null PDV** foi desenvolvido como um projeto de estudo para compreender, na prática, como funciona o fluxo de uma venda em um sistema de supermercado.

A ideia principal é simular desde o **cadastro dos produtos** até a **finalização e pagamento de uma venda**, permitindo estudar conceitos como:

* Cadastro e organização de produtos;
* Controle de estoque;
* Criação e gerenciamento de categorias;
* Abertura de uma venda;
* Adição de produtos ao carrinho;
* Cálculo do valor total da venda;
* Baixa automática do estoque;
* Finalização da venda;
* Registro da forma de pagamento;
* Cálculo de troco para pagamentos em dinheiro.

> **Importante:** o Null PDV é um projeto desenvolvido para fins de estudo e aprendizado, tendo como foco a compreensão da lógica e do fluxo de funcionamento de um sistema de PDV.

---

# 🛠️ Tecnologias utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

* **Python** — linguagem principal utilizada no desenvolvimento da aplicação;
* **Flask** — framework utilizado para criação e disponibilização da API;
* **SQLite3** — banco de dados utilizado para armazenamento das informações do sistema;
* **QRCode** — biblioteca utilizada para geração de QR Codes relacionados às funcionalidades do sistema.

---

# 🚀 Funcionalidades

Atualmente, o sistema possui as seguintes funcionalidades:

### 📁 Categorias

* CRUD de categorias;
* Cadastro de categorias;
* Atualização de categorias;
* Consulta de categorias;
* Exclusão de categorias.

### 📦 Produtos

* CRUD de produtos;
* Cadastro de produtos;
* Atualização de produtos;
* Consulta de produtos;
* Exclusão de produtos;
* Vinculação de produtos a categorias;
* Controle de estoque;
* Definição de status do produto.

### 🛒 Vendas

* Iniciar uma venda;
* Adicionar produtos à venda;
* Calcular o valor total da venda;
* Baixar automaticamente os produtos do estoque;
* Listar vendas abertas;
* Finalizar uma venda;
* Registrar a forma de pagamento;
* Registrar o valor pago;
* Calcular o troco em pagamentos em dinheiro;
* Listar vendas finalizadas.

---

# 🚧 Funcionalidades em desenvolvimento

Algumas funcionalidades do projeto ainda estão em desenvolvimento:

### PIX

O pagamento via **PIX** ainda está em desenvolvimento e será implementado posteriormente.

### Itens da venda

O gerenciamento dos **itens individuais de uma venda** também está em desenvolvimento.

> **OBS:** As funcionalidades acima podem sofrer alterações conforme o desenvolvimento e evolução do projeto.

---

# 🧪 Como testar a API

Para realizar os testes das requisições, você pode utilizar qualquer uma das ferramentas abaixo:

1. **Bruno**
2. **Postman**
3. **Insomnia**

Após instalar uma dessas ferramentas, siga os passos abaixo.



## 1. Instalar as dependências

Dentro da pasta do projeto, execute:

```bash
pip install -r requirements.txt
```

Esse comando instala todas as bibliotecas necessárias para executar a API.

---

## 2. Executar a API

A forma principal de iniciar a aplicação é:

```bash
flask run
```

Caso esse comando não funcione, você também pode tentar:

### Windows

```bash
python app.py
```

### Linux

```bash
python3 app.py
```

Após iniciar a aplicação, a API estará disponível para receber as requisições.

---

# 📁 CRUD de Categorias

As categorias são utilizadas para **organizar e separar os produtos cadastrados no sistema**.

Um produto pode ser associado a uma categoria, facilitando a organização dos produtos dentro do PDV.

### Exemplo de cadastro

```json
{
    "categoria": "doce",
    "status": "ativo"
}
```

Nesse exemplo, está sendo criada a categoria **doce** com o status **ativo**.

---

# 📦 CRUD de Produtos

O CRUD de produtos é responsável pelo gerenciamento dos produtos utilizados nas vendas.

Cada produto possui informações como:

* Nome;
* Preço unitário;
* Estoque;
* Categoria;
* Status.

### Exemplo de cadastro

```json
{
    "nome_produto": "Arroz 1kg",
    "preco_unitario": 32.99,
    "estoque": 999,
    "categoria": "",
    "status": "ativo"
}
```

### Categoria automática

É possível informar a categoria diretamente no corpo da requisição.

Caso o campo `categoria` seja enviado vazio:

```json
"categoria": ""
```

a API automaticamente vinculará o produto à categoria:

```text
DIVERSOS
```

Isso permite cadastrar um produto mesmo quando nenhuma categoria específica foi informada.

---

# 🛒 Como iniciar uma venda

O processo de venda começa através da criação de uma venda com os produtos desejados.

Para iniciar uma venda, é necessário informar:

* Código do produto;
* Quantidade que será vendida.

### Exemplo

```json
{
    "itens": [
        {
            "codigo_produto": 1,
            "quantidade_venda": 2
        },
        {
            "codigo_produto": 46,
            "quantidade_venda": 4
        }
    ]
}
```

Nesse exemplo:

* O produto `1` será vendido em uma quantidade de `2` unidades;
* O produto `46` será vendido em uma quantidade de `4` unidades.

---

## 📋 Resposta da API

Após iniciar a venda, a API retorna informações sobre o carrinho, os valores, o estoque e a própria venda.

```json
{
    "carrinho_atual": [
        {
            "nome_produto": "Arroz 5kg",
            "preco_unitario": 28.9,
            "quantidade_venda": 2,
            "valor_total_produto": 57.8
        },
        {
            "nome_produto": "Prato de Cerâmica",
            "preco_unitario": 14.9,
            "quantidade_venda": 4,
            "valor_total_produto": 59.6
        }
    ],
    "data": {
        "venda": {
            "iniciada_em": "18/09/2026T22:39",
            "status": "aberta",
            "valor_total_venda": 117.4,
            "venda_id": 2
        }
    },
    "estoque": true,
    "message": "Venda inicializada com sucesso.",
    "success": true
}
```

### O que significa `estoque: true`?

O campo:

```json
"estoque": true
```

indica que a operação de estoque foi realizada com sucesso.

Ao iniciar uma venda, a API **automaticamente realiza a baixa da quantidade vendida no estoque**.

Por exemplo:

```text
Estoque antes da venda: 999
Quantidade vendida:       2
Estoque após a venda:   997
```

Dessa forma, o estoque é atualizado de acordo com os produtos adicionados à venda.

---

# 💰 Como finalizar uma venda

Depois que a venda foi iniciada, ela permanece com o status:

```text
aberta
```

Para finalizar a venda, é necessário informar:

* A forma de pagamento;
* O valor pago, quando a forma de pagamento for dinheiro.

### Exemplo

```json
{
    "forma_pagamento": "dinheiro",
    "valor_dinheiro": 150
}
```

A API utiliza o `venda_id` da venda iniciada para identificar qual venda será finalizada.

---

## 💵 Pagamento em dinheiro

Quando a forma de pagamento for `dinheiro`, a API utiliza o valor informado em `valor_dinheiro` para calcular o troco.

Por exemplo:

```text
Total da venda: R$ 117,40
Valor recebido: R$ 150,00
Troco:          R$ 32,60
```

---

## 💳 Outras formas de pagamento

Quando a forma de pagamento **não for dinheiro**, o campo:

```json
"valor_dinheiro"
```

será ignorado pela API.

Isso acontece porque o valor recebido em dinheiro só é necessário para calcular o troco quando o pagamento é realizado em espécie.

> **OBS:** O pagamento via **PIX ainda está em desenvolvimento** e não está totalmente implementado no sistema.

---

## 📋 Resposta da finalização

Exemplo de resposta:

```json
{
    "status_venda": true,
    "sucesso": true,
    "troco": 32.6,
    "venda": {
        "finalizada_em": "18/09/2026T22:43",
        "pagamento": {
            "forma": "dinheiro",
            "valor_pago": 150
        },
        "status": "concluida",
        "venda_id": 2
    }
}
```

Após a finalização, a venda passa de:

```text
aberta
```

para:

```text
concluida
```

A API também registra informações como:

* ID da venda;
* Forma de pagamento;
* Valor pago;
* Horário de finalização;
* Status da venda;
* Troco, quando aplicável.



# 🔄 Fluxo básico do sistema

De forma simplificada, o funcionamento do **Null PDV** pode ser representado da seguinte maneira:

```text
        CADASTRAR CATEGORIA
                │
                ▼
         CADASTRAR PRODUTO
                │
                ▼
          DEFINIR ESTOQUE
                │
                ▼
          INICIAR VENDA
                │
                ▼
       ADICIONAR PRODUTOS
                │
                ▼
       BAIXAR DO ESTOQUE
                │
                ▼
        CALCULAR TOTAL
                │
                ▼
       ESCOLHER PAGAMENTO
                │
                ▼
        FINALIZAR VENDA
                │
                ▼
       REGISTRAR PAGAMENTO
                │
                ▼
        VENDA CONCLUÍDA
```

---

# 📌 Resumo

O **Null PDV** busca reproduzir, de forma simplificada, o fluxo básico encontrado em um sistema de supermercado.

O projeto começa pelo **cadastro e organização dos produtos**, passa pelo **controle de estoque**, permite **iniciar uma venda** e termina com o **processamento do pagamento e conclusão da venda**.

O principal objetivo não é apenas criar um CRUD, mas compreender como diferentes partes de um sistema de PDV se relacionam durante uma operação de venda.

```text
Produto → Estoque → Venda → Pagamento → Venda concluída
```

O projeto continuará sendo evoluído com a implementação de novas funcionalidades, incluindo o **pagamento via PIX** e o gerenciamento completo dos **itens das vendas**.
