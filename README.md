# NexaPDV

API de um sistema de **Ponto de Venda (PDV)** desenvolvido com o objetivo de estudar e simular o funcionamento básico de um sistema de supermercado.

---

# 🎯 Objetivo do projeto

O **NexaPDV** foi desenvolvido como um projeto de estudo para compreender, na prática, como funciona o fluxo de uma venda em um sistema de supermercado.

A ideia principal é simular desde o **cadastro de categorias e produtos** até a **finalização da venda**, passando pelo controle de estoque, gerenciamento dos itens da venda e simulação dos pagamentos.

Entre os principais conceitos implementados estão:

* Cadastro e organização de produtos;
* Controle de estoque;
* Criação e gerenciamento de categorias;
* Vinculação de produtos às categorias através do ID;
* Abertura de uma venda;
* Inserção dos itens da venda;
* Cálculo do valor total da venda;
* Baixa automática do estoque;
* Finalização da venda;
* Registro da forma de pagamento;
* Cálculo de troco para pagamentos em dinheiro;
* Simulação de pagamentos em débito e crédito;
* Simulação de pagamento via PIX;
* Geração de QR Code;
* Geração de comprovante em arquivo `.txt`;
* Geração de relatórios relacionados aos produtos e estoque.

> **Importante:** o NexaPDV é um projeto desenvolvido para fins de estudo e aprendizado, tendo como foco a compreensão da lógica e do fluxo de funcionamento de um sistema de PDV.

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
* Vinculação obrigatória do produto a uma categoria através do `categoria_id`;
* Controle de estoque;
* Definição de status do produto.

### 🛒 Vendas

* Iniciar uma venda;
* Adicionar produtos à venda;
* Inserir os itens da venda;
* Calcular o valor total da venda;
* Baixar automaticamente os produtos do estoque;
* Listar vendas abertas;
* Finalizar uma venda;
* Registrar a forma de pagamento;
* Registrar o valor pago;
* Calcular o troco em pagamentos em dinheiro;
* Listar vendas finalizadas;
* Gerar comprovante da venda em formato `.txt`.

### 💳 Pagamentos

* Simulação de pagamento em dinheiro;
* Simulação de pagamento em débito;
* Simulação de pagamento em crédito;
* Simulação de pagamento via PIX;
* Geração de QR Code para o fluxo simulado de pagamento via PIX;
* Retorno do QR Code em formato Base64;
* Rota específica para geração do QR Code;
* Registro das informações do pagamento.

> **Observação:** os pagamentos do NexaPDV são **simulados**. O projeto não utiliza APIs ou gateways de pagamento prontos, como Mercado Pago, Stripe ou outros serviços externos. A lógica de pagamento é implementada diretamente na aplicação com fins de estudo.

### 📄 Comprovante

O NexaPDV possui uma funcionalidade de **geração de comprovante da venda em formato `.txt`**.

O comprovante é gerado durante o processo de finalização da venda. A resposta da API informa o caminho do arquivo gerado.

Exemplo:

```json
{
    "msg_comprovante": {
        "arquivo": "comprovantes/comprovante_1.txt",
        "msg": "comprovante gerado com sucesso",
        "sucesso": true
    }
}
```

Dessa forma, o sistema simula a geração de um comprovante simples após a conclusão da venda.

### 📊 Relatórios

* Relatórios relacionados aos produtos e estoque;
* Consulta do valor total do estoque.

---

# 🗄️ Inicialização do banco de dados

O NexaPDV utiliza **SQLite3** para armazenamento dos dados.

Para iniciar o banco de dados, execute o seguinte comando na raiz do projeto:

```bash
python api/database/connections.py
```

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

Os produtos não recebem mais uma categoria padrão automaticamente. Para cadastrar um produto, é necessário informar uma categoria existente através do seu **ID**.

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

A categoria do produto é informada através do campo `categoria_id`:

```json
{
    "nome_produto": "Arroz 5g",
    "categoria_id": 1,
    "preco_unitario": 36.76,
    "estoque": 199,
    "status": "ativo"
}
```

Nesse exemplo:

* `nome_produto` define o nome do produto;
* `categoria_id` informa o ID da categoria vinculada ao produto;
* `preco_unitario` define o preço unitário;
* `estoque` define a quantidade disponível;
* `status` define o estado do produto.

### 🔗 Categoria obrigatória

O produto precisa possuir uma categoria vinculada.

A categoria deve ser informada através do campo:

```json
"categoria_id": 1
```

O valor informado deve corresponder ao ID de uma categoria existente no banco de dados.

Não existe mais a regra de atribuir automaticamente a categoria **DIVERSOS** quando nenhuma categoria é informada.

Portanto, o cadastro do produto depende da existência de uma categoria válida para realizar a vinculação.

---

# 🛒 Como iniciar uma venda

O processo de venda começa através da criação de uma venda com os produtos desejados.

Para iniciar uma venda, são informados:

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

* O produto `1` será adicionado à venda com quantidade `2`;
* O produto `46` será adicionado à venda com quantidade `4`.

---

# 🧾 Itens da venda

Os **itens da venda agora são inseridos durante a inicialização da venda**.

Cada item está relacionado a um produto e registra informações como:

* Código do produto;
* Nome do produto;
* Preço unitário;
* Quantidade vendida;
* Valor total do produto.

Essas informações são utilizadas para compor o carrinho e calcular o valor total da venda.

Exemplo:

```text
Produto: Arroz 5g
Preço unitário: R$ 36,76
Quantidade: 10
Valor total do produto: R$ 367,60
```

---

# 📋 Resposta da API

Após iniciar a venda, a API retorna os itens inseridos no carrinho e as informações da venda.

Exemplo da estrutura atual:

```json
[
    {
        "carrinho": [
            {
                "codigo_produto": 1,
                "nome_produto": "Arroz 5g",
                "preco_unitario": 36.76,
                "quantidade_venda": 10,
                "valor_total_produto": 367.6
            },
            {
                "codigo_produto": 1,
                "nome_produto": "Arroz 5g",
                "preco_unitario": 36.76,
                "quantidade_venda": 10,
                "valor_total_produto": 367.6
            }
        ],
        "msg": "Venda iniciada com sucesso",
        "sucesso": true,
        "venda": {
            "iniciada_em": "04/10/2026T20:36",
            "status": "aberta",
            "valor_total_venda": 735.2,
            "venda_id": 1
        }
    }
]
```

O retorno apresenta:

* `carrinho` — itens adicionados à venda;
* `codigo_produto` — código do produto;
* `nome_produto` — nome do produto;
* `preco_unitario` — preço de uma unidade;
* `quantidade_venda` — quantidade adicionada à venda;
* `valor_total_produto` — valor total daquele item;
* `msg` — mensagem referente à operação;
* `sucesso` — indica se a operação foi realizada com sucesso;
* `venda` — informações gerais da venda;
* `venda_id` — identificador da venda;
* `status` — situação atual da venda;
* `valor_total_venda` — valor total calculado para a venda.

No exemplo, existem dois registros de item e, por isso, o valor total da venda é:

```text
R$ 367,60 + R$ 367,60 = R$ 735,20
```

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

### 📋 Resposta da finalização em dinheiro

Além de finalizar a venda, a operação também gera o comprovante.

Exemplo da resposta atual:

```json
{
    "msg_comprovante": {
        "arquivo": "comprovantes/comprovante_1.txt",
        "msg": "comprovante gerado com sucesso",
        "sucesso": true
    },
    "status_venda_iniciada": {
        "msg": "Status atualizado",
        "sucesso": true
    },
    "sucesso": true,
    "venda": {
        "finalizada_em": "04/10/2026T20:38",
        "pagamento": {
            "forma": "dinheiro",
            "troco": 64.8,
            "valor_pago": 800
        },
        "status_venda_finalizada": "concluida",
        "venda_id": 1
    }
}
```

A resposta informa três partes importantes:

### `msg_comprovante`

Indica que o comprovante foi gerado e informa o caminho do arquivo:

```text
comprovantes/comprovante_1.txt
```

### `status_venda_iniciada`

Indica que o status da venda iniciada foi atualizado com sucesso.

```json
{
    "msg": "Status atualizado",
    "sucesso": true
}
```

### `venda`

Contém as informações da venda finalizada, incluindo:

* Horário de finalização;
* Forma de pagamento;
* Valor pago;
* Troco;
* Status final;
* ID da venda.

Após a finalização, a venda passa de:

```text
aberta
```

para:

```text
concluida
```

---

# 💳 Pagamentos em débito e crédito

O NexaPDV também possui suporte à **simulação de pagamentos em débito e crédito**.

Essas formas de pagamento fazem parte da lógica de finalização da venda, assim como o pagamento em dinheiro e o PIX.

Os pagamentos continuam sendo apenas **simulados**, não existindo integração com máquinas de cartão, adquirentes ou gateways externos.

---

# 💠 Pagamento via PIX

O pagamento via **PIX possui rotas específicas** para separar a finalização da venda da geração do QR Code.

Essa separação permite que a geração do QR Code seja realizada de forma independente da operação de finalização da venda.

## Finalização da venda via PIX

A venda pode ser finalizada através da rota:

```http
POST /finalizar_venda/pix/<venda_id>
```

### Exemplo de requisição

```json
{
    "forma_pagamento": "pix"
}
```

Essa rota realiza a lógica de finalização da venda utilizando a forma de pagamento PIX.

---

# 🔲 Geração do QR Code PIX

A geração do QR Code possui uma rota própria:

```http
GET /qrcode/pix
```

Com a API executando localmente:

```http
GET http://127.0.0.1:5000/qrcode/pix
```

A rota foi separada da finalização da venda para manter a geração do QR Code como uma operação independente.

### QR Code em Base64

O projeto utiliza a biblioteca **QRCode** para gerar o QR Code.

O conteúdo da imagem pode ser representado em **Base64**, permitindo que a imagem seja transportada através da API.

Exemplo conceitual:

```json
{
    "qrcode": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

O front-end poderá utilizar esse conteúdo para exibir visualmente o QR Code.

> **Importante:** o PIX implementado no NexaPDV é **simulado**. O projeto não realiza uma transação PIX real e não possui integração com gateways ou APIs externas de pagamento.

---

# 📄 Comprovante da venda

O NexaPDV possui uma funcionalidade de **geração de comprovante da venda em formato `.txt`**.

O comprovante é gerado durante a finalização da venda.

O sistema informa na resposta da API o arquivo gerado:

```text
comprovantes/comprovante_1.txt
```

A resposta também informa:

```json
{
    "msg": "comprovante gerado com sucesso",
    "sucesso": true
}
```

O comprovante possui finalidade de **simulação**, reproduzindo de forma simplificada as informações relacionadas à venda realizada.

> **Importante:** esse arquivo não representa um documento fiscal oficial. Ele é utilizado no projeto para simular a geração de um comprovante de venda.

---

# 📊 Relatórios

O sistema possui funcionalidades relacionadas a **relatórios de produtos e estoque**.

Uma das informações disponíveis é o **valor total do estoque**, permitindo visualizar o valor financeiro correspondente aos produtos atualmente armazenados.

Exemplo conceitual:

```text
Relatório de Estoque

────────────────────────────

Valor total do estoque: R$ 12.450,00
```

Essas informações poderão futuramente ser apresentadas de forma visual através do front-end.

---

# 🔄 Fluxo básico do sistema

De forma simplificada, o funcionamento do **NexaPDV** pode ser representado da seguinte maneira:

```text
        CADASTRAR CATEGORIA
                │
                ▼
         CADASTRAR PRODUTO
                │
                ▼
       VINCULAR CATEGORIA
          ATRAVÉS DO ID
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
        INSERIR ITENS DA VENDA
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
       ┌────────┼────────┐
       ▼        ▼        ▼
   DINHEIRO   DÉBITO   CRÉDITO
       │
       ▼
     TROCO

                │
                ▼
              PIX
                │
                ▼
        GERAR QR CODE
                │
                ▼
        PIX SIMULADO

                │
                ▼
         FINALIZAR VENDA
                │
                ▼
       REGISTRAR PAGAMENTO
                │
                ▼
       GERAR COMPROVANTE
             (.txt)
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
* Gerenciamento dos itens da venda;
* Simulação de pagamento em dinheiro;
* Simulação de pagamento em débito;
* Simulação de pagamento em crédito;
* Simulação de pagamento via PIX;
* Geração e exibição do QR Code;
* Geração do comprovante;
* Consulta de relatórios;
* Visualização do valor total do estoque.

A ideia é manter o **backend responsável pela lógica e regras do sistema**, enquanto o front-end será responsável pela interação visual com o usuário.

---

# 📌 Resumo

O **NexaPDV** busca reproduzir, de forma simplificada, o fluxo básico encontrado em um sistema de supermercado.

O projeto começa pelo **cadastro de categorias e produtos**, passa pela **vinculação obrigatória da categoria através do ID** e pelo **controle de estoque**, permite **iniciar uma venda e inserir seus itens**, calcula o valor total e realiza a baixa dos produtos no estoque.

Após isso, a venda pode ser finalizada utilizando as formas de pagamento disponíveis no sistema, incluindo **dinheiro, débito, crédito e PIX**.

Na finalização, o sistema registra as informações do pagamento, atualiza o status da venda para **concluída** e gera um **comprovante em formato `.txt`**.

O projeto também possui uma rota específica para geração do **QR Code PIX**, mantendo essa operação separada da finalização da venda.

A implementação dos pagamentos tem **finalidade exclusivamente educacional**. O NexaPDV não utiliza gateways ou APIs externas de pagamento, como Mercado Pago, Stripe ou outros serviços semelhantes. Toda a lógica foi desenvolvida dentro da própria aplicação para simular o comportamento de um sistema de PDV.

O principal objetivo não é apenas criar um CRUD, mas compreender como diferentes partes de um sistema de PDV se relacionam durante uma operação de venda.

```text
Produto
   ↓
Categoria
   ↓
Estoque
   ↓
Venda
   ↓
Itens da venda
   ↓
Cálculo do total
   ↓
Pagamento
   ├── Dinheiro → Troco
   ├── Débito
   ├── Crédito
   └── PIX → QR Code
            ↓
      Venda concluída
            ↓
    Comprovante (.txt)
```

O projeto continuará sendo evoluído, tendo como uma das próximas etapas a implementação de um **front-end integrado à API**.
