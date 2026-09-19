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
* Cálculo de troco para pagamentos em dinheiro;
* Pagamento via PIX;
* Geração de relatórios relacionados aos produtos e estoque.

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

### 💳 Pagamentos

* Pagamento em dinheiro;
* Pagamento via PIX;
* Geração de QR Code para o fluxo de pagamento via PIX;
* Retorno do QR Code em formato Base64.

### 📊 Relatórios

* Relatórios relacionados aos produtos e estoque;
* Consulta do valor total do estoque.

---

# 🚧 Funcionalidades em desenvolvimento

Algumas funcionalidades do projeto ainda estão em desenvolvimento:

### Itens da venda

O gerenciamento dos **itens individuais de uma venda** ainda está em desenvolvimento.

> **OBS:** As funcionalidades podem sofrer alterações conforme o desenvolvimento e evolução do projeto.

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

Quantidade vendida: 2

Estoque após a venda: 997
```

Dessa forma, o estoque é atualizado de acordo com os produtos adicionados à venda.

---

# 💰 Como finalizar uma venda

Depois que a venda foi iniciada, ela permanece com o status:

```text
aberta
```

A finalização da venda possui **rotas específicas de acordo com a forma de pagamento**.

---

## 💵 Pagamento em dinheiro

Para pagamentos em dinheiro, a venda pode ser finalizada pela rota:

```http
POST /finalizar_venda/<venda_id>
```

É necessário informar:

* A forma de pagamento;
* O valor pago.

### Exemplo

```json
{
    "forma_pagamento": "dinheiro",
    "valor_dinheiro": 150
}
```

A API utiliza o `venda_id` da venda iniciada para identificar qual venda será finalizada.

### Cálculo do troco

Quando a forma de pagamento for `dinheiro`, a API utiliza o valor informado em `valor_dinheiro` para calcular o troco.

Por exemplo:

```text
Total da venda: R$ 117,40

Valor recebido: R$ 150,00

Troco: R$ 32,60
```

---

## 💳 Pagamento via PIX

O pagamento via **PIX possui uma rota separada** da finalização convencional.

Essa separação foi realizada para evitar que o QR Code seja incluído nas respostas das outras formas de pagamento, mantendo as respostas da API menores e evitando conflitos relacionados ao conteúdo do QR Code.

A rota utilizada é:

```http
POST /finalizar_venda/pix/<venda_id>
```

### Exemplo de requisição

```json
{
    "forma_pagamento": "pix"
}
```

A rota específica do PIX realiza o fluxo de finalização da venda e retorna o QR Code juntamente com as informações necessárias da operação.

### QR Code em Base64

O campo `qrcode` retornado pela API contém a imagem do QR Code representada em **Base64**.

Exemplo:

```json
{
    "qrcode": "iVBORw0KGgoAAAANSUhEUgAAAXIAAAFyAQAAAADAX2yk...",
    "status_venda": true,
    "sucesso": true,
    "venda": {
        "finalizada_em": "19/09/2026T18:55",
        "pagamento": {
            "forma": "pix",
            "valor_pago": 117.4
        },
        "status": "concluida",
        "venda_id": 3
    }
}
```

O Base64 permite transportar os dados da imagem diretamente dentro da resposta JSON.

No futuro, o **front-end** poderá utilizar esse conteúdo para converter e exibir o QR Code visualmente para o usuário.

> **OBS:** O QR Code em Base64 é retornado especificamente pelo endpoint de PIX. Dessa forma, as respostas das demais formas de pagamento não precisam carregar esse conteúdo, mantendo o retorno da API mais enxuto.

---

## 📋 Resposta da finalização em dinheiro

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

---

# 📊 Relatórios

O sistema também possui funcionalidades relacionadas a **relatórios de produtos e estoque**.

Uma das informações disponíveis é o **valor total do estoque**, permitindo visualizar o valor financeiro correspondente aos produtos atualmente armazenados.

Exemplo conceitual:

```text
Relatório de Estoque
────────────────────────────
Valor total do estoque: R$ 12.450,00
```

Essas informações podem futuramente ser apresentadas de forma visual através do front-end.

---

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
        ┌───────┴────────┐
        ▼                ▼
     DINHEIRO           PIX
        │                │
        ▼                ▼
     TROCO          GERAR QR CODE
        │                │
        └───────┬────────┘
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

# 🖥️ Futuro Front-end

Como próxima etapa do projeto, será desenvolvido um **front-end integrado à API**.

A interface deverá permitir utilizar visualmente as funcionalidades já disponibilizadas pelo backend, incluindo:

* Cadastro e gerenciamento de produtos;
* Gerenciamento de categorias;
* Controle de estoque;
* Criação e finalização de vendas;
* Pagamento em dinheiro;
* Pagamento via PIX;
* Exibição do QR Code;
* Consulta de relatórios;
* Visualização do valor total do estoque.

A ideia é manter o **backend responsável pela lógica e regras do sistema**, enquanto o front-end será responsável pela interação visual com o usuário.

---

# 📌 Resumo

O **Null PDV** busca reproduzir, de forma simplificada, o fluxo básico encontrado em um sistema de supermercado.

O projeto começa pelo **cadastro e organização dos produtos**, passa pelo **controle de estoque**, permite **iniciar uma venda** e termina com o **processamento do pagamento e conclusão da venda**.

Atualmente, o sistema também possui suporte ao **pagamento via PIX através de uma rota específica**, com retorno do QR Code em **Base64**, além de funcionalidades de **relatórios de produtos e estoque**.

O principal objetivo não é apenas criar um CRUD, mas compreender como diferentes partes de um sistema de PDV se relacionam durante uma operação de venda.

```text
Produto → Estoque → Venda → Pagamento → Venda concluída
                         │
                         ├── Dinheiro → Troco
                         │
                         └── PIX → QR Code (Base64)
```

O projeto continuará sendo evoluído, tendo como uma das próximas etapas a implementação de um **front-end integrado à API**.
