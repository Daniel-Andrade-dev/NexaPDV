# 🛒 NexaPDV

**API para simular um Ponto de Venda (PDV)**

O NexaPDV é um projeto desenvolvido em Python com o objetivo de simular as principais operações de um sistema de ponto de venda de supermercado, incluindo gerenciamento de produtos, processamento de vendas, pagamentos e controle de caixa.

O projeto tem como foco o aprendizado e a aplicação de conceitos de desenvolvimento Back-End, organização de código, persistência de dados e testes de APIs REST.

## 🚀 Funcionalidades

### 📦 Gerenciamento de produtos e categorias
- Cadastro, consulta, atualização e exclusão de produtos e categorias.
- Controle de estoque.
- Validação de dados dos produtos.
- Identificação de produtos ativos e inativos.

### 🛍️ Gerenciamento de vendas
- Inicialização de vendas.
- Adição de produtos e definição de quantidades.
- Cálculo automático do valor total da venda.
- Finalização e cancelamento de vendas.
- Controle de status das vendas.
- Registro dos itens associados a cada venda.

### 🏷️ Regra de desconto

O NexaPDV possui uma regra de desconto aplicada de acordo com o valor total da venda:

- Vendas com valor total de até R$ 199,00 não recebem desconto por essa regra.
- Vendas com valor total superior a R$ 199,00 recebem **15% de desconto**.

**Exemplo:**

| Descrição | Valor |
|---|---:|
| Valor original | R$ 250,00 |
| Desconto de 15% | R$ 37,50 |
| **Total com desconto** | **R$ 212,50** |

Essa regra permite praticar cálculos comerciais e implementar regras de negócio no processamento das vendas.

### 💳 Formas de pagamento
- Dinheiro, com cálculo de troco.
- Cartão de crédito.
- Cartão de débito.
- PIX simulado, com geração de QR Code.

> Os pagamentos são simulados para fins de estudo. O projeto não utiliza uma integração real com instituições financeiras ou gateways de pagamento.

### 🧾 Comprovantes de venda
- Geração de comprovantes em arquivos `.txt`.
- Registro do número da venda, produtos, valores, forma de pagamento, troco e data de emissão.
- Organização dos comprovantes em diretório próprio.

### 🏦 Controle de caixa
- Cadastro e abertura de caixa.
- Registro de pagamentos associados ao caixa.
- Registro e consulta de sangrias.
- Cálculo do valor esperado em dinheiro.
- Fechamento de caixa com valor contado.
- Cálculo da diferença entre o valor esperado e o valor contado.
- Consulta de caixas abertos e fechados.

### 📊 Relatórios
- Consulta de vendas iniciadas e finalizadas.
- Consulta de informações de estoque.
- Cálculo de indicadores, como ticket médio e valor total do estoque, conforme os endpoints implementados.

## 🛠️ Tecnologias utilizadas

- **Python** — linguagem de programação.
- **Flask** — desenvolvimento da API REST.
- **SQLite3** — banco de dados relacional.
- **qrcode** — geração de QR Codes.
- **Base64** — representação do QR Code em respostas da API.
- **Bruno / Postman / Insomnia** — ferramentas para testar as requisições HTTP.

## 🏗️ Organização do projeto

O NexaPDV utiliza uma arquitetura inspirada no DDD, em uma abordagem simplificada (*DDD-lite*), separando as responsabilidades da aplicação.

- **Routes:** recebem e encaminham as requisições HTTP.
- **Services:** implementam as regras de negócio.
- **Repositories:** concentram as operações de acesso ao banco de dados.
- **Models:** representam as entidades e os dados utilizados pela aplicação.
- **Enums:** definem valores padronizados, como status de vendas e formas de pagamento.
- **Validators:** auxiliam na validação dos dados recebidos.
- **Comprovantes:** geram os arquivos de comprovante de venda.

Essa separação facilita a manutenção, os testes e a evolução do sistema.

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd NexaPDV
```

Substitua `URL_DO_REPOSITORIO` pelo endereço real do repositório.

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente virtual no Linux:

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicialize o banco de dados

Execute o script de inicialização do banco conforme a estrutura atual do projeto.
```bash
python api/database/connections.py
```
### 5. Execute a aplicação

```bash
flask run
```

Caso o projeto esteja configurado para execução direta pelo arquivo principal, também é possível utilizar:

```bash
python app.py
```

A API ficará disponível localmente no endereço padrão do Flask, geralmente `http://127.0.0.1:5000`.

## 🧪 Testes de API

As requisições podem ser executadas utilizando Bruno, Postman ou Insomnia.

Essas ferramentas permitem verificar os endpoints, os códigos HTTP, os payloads, as respostas e o comportamento das regras de negócio.

## 🎯 Objetivos do projeto

O NexaPDV foi desenvolvido para praticar:

- Desenvolvimento de APIs REST com Flask.
- Operações CRUD.
- Consultas SQL e relacionamentos entre tabelas.
- Organização de código e separação de responsabilidades.
- Implementação de regras de negócio.
- Controle de estoque e processamento de vendas.
- Transações e persistência de dados.
- Testes e validação de APIs.
- Controle de caixa e cálculos financeiros.


**NexaPDV — Projeto de estudo em desenvolvimento Back-End com Python.**