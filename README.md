# NexaPDV

Sistema de **Ponto de Venda (PDV)** com uma API para gerenciamento de
produtos, categorias, caixas, vendas e relatórios. O projeto está sendo
desenvolvido com foco nas regras de negócio e na organização do
back-end.

> **Status:** em desenvolvimento. A interface web está planejada para
> uma etapa futura, utilizando Vue.js.

## Objetivos

-   Gerenciar produtos e categorias.
-   Controlar a abertura, movimentação e o fechamento de caixas.
-   Registrar vendas e seus itens.
-   Finalizar vendas com diferentes formas de pagamento, incluindo PIX.
-   Consultar relatórios de vendas, produtos e caixas.

## Tecnologias e arquitetura

-   **Back-end:** Python com Flask.
-   **Banco de dados:** SQLite3.
-   **Front-end planejado:** Vue.js.

O Vue.js será utilizado futuramente para construir a interface do PDV e
consumir os endpoints disponibilizados pela API. Atualmente, a coleção
de requisições permite testar os endpoints localmente, por exemplo, pelo
Postman.

## Regras de negócio

### Valores monetários em centavos

O sistema utiliza **números inteiros em centavos** para representar
valores monetários. Essa decisão evita problemas de precisão que podem
ocorrer em operações com números de ponto flutuante.

Exemplos:

    Valor em reais   Valor enviado à API
  ---------------- ---------------------
          R\$ 1,00                 `100`
         R\$ 15,50                `1550`
        R\$ 150,00               `15000`
        R\$ 500,00               `50000`

Portanto, campos como `preco_unitario_centavos`,
`valor_inicial_centavos` e `valor_contado_centavos` devem receber
valores inteiros em centavos.

### Desconto nas vendas

O sistema aplica **15% de desconto quando o valor da venda ultrapassa
R\$ 150,00**, ou seja, quando o total é superior a `15000` centavos.

Exemplo:

  Descrição                                      Valor
  -------------------- -------------------------------
  Subtotal               R\$ 200,00 (`20000` centavos)
  Desconto de 15%          R\$ 30,00 (`3000` centavos)
  Total com desconto     R\$ 170,00 (`17000` centavos)

O limite é avaliado em centavos: uma venda de exatamente `15000`
centavos não ultrapassa o limite.

## Executando localmente

A coleção de requisições fornecida utiliza a URL base:

``` text
http://127.0.0.1:5000
```

Com a API em execução localmente, configure essa URL no cliente HTTP
utilizado para testar as rotas.

> Este README não define comandos de instalação ou inicialização porque
> eles não estão descritos na coleção de endpoints. Adicione aqui os
> comandos específicos do ambiente do projeto quando estiverem
> definidos.

## Endpoints da API

Abaixo estão as rotas presentes na coleção `API NexaPDV`. Os exemplos de
corpo seguem os formatos registrados nessa coleção.

### 1. PDV e vendas

  ----------------------------------------------------------------------------------------------------
  Método                  Rota                                                 Finalidade
  ----------------------- ---------------------------------------------------- -----------------------
  `POST`                  `/vendas/iniciar_vendas/{caixa_id}`                  Inicia uma venda
                                                                               vinculada a um caixa e
                                                                               recebe os itens da
                                                                               venda.

  `POST`                  `/vendas/finalizar_vendas/{venda_id}`                Finaliza uma venda
                                                                               informando a forma de
                                                                               pagamento, o valor em
                                                                               dinheiro em centavos e
                                                                               o caixa.

  `GET`                   `/vendas/qrcode/pix`                                 Solicita a geração de
                                                                               um QR Code para PIX.

  `PUT`                   `/vendas/cancelar_vendas/{venda_iniciada_id}`        Cancela uma venda
                                                                               iniciada.

  `POST`                  `/vendas/finalizar_vendas/pix/{venda_iniciada_id}`   Finaliza uma venda
                                                                               iniciada com pagamento
                                                                               via PIX.
  ----------------------------------------------------------------------------------------------------

#### Iniciar uma venda

`POST /vendas/iniciar_vendas/{caixa_id}`

Exemplo de corpo:

``` json
{
  "itens": [
    {
      "codigo_produto": 1,
      "quantidade_venda": 1
    }
  ]
}
```

#### Finalizar uma venda

`POST /vendas/finalizar_vendas/{venda_id}`

Exemplo de corpo:

``` json
{
  "forma_pagamento": "credito",
  "valor_dinheiro_centavos": 50000,
  "caixa_id": 1
}
```

#### Finalizar uma venda com PIX

`POST /vendas/finalizar_vendas/pix/{venda_iniciada_id}`

Exemplo de corpo:

``` json
{
  "forma_pagamento": "pix",
  "caixa_id": 1
}
```

### 2. Produtos

  ------------------------------------------------------------------------------
  Método                  Rota                           Finalidade
  ----------------------- ------------------------------ -----------------------
  `POST`                  `/produtos`                    Cadastra um produto.

  `GET`                   `/produtos/{codigo_produto}`   Busca um produto pelo
                                                         código.

  `PUT`                   `/produtos/{codigo_produto}`   Atualiza os dados de um
                                                         produto.

  `DELETE`                `/produtos/{codigo_produto}`   Exclui um produto.

  `GET`                   `/relatorios/produtos`         Consulta o relatório de
                                                         produtos cadastrados.
  ------------------------------------------------------------------------------

Exemplo de corpo para cadastro:

``` json
{
  "categoria_id": 1,
  "nome_produto": "Produto exemplo",
  "preco_unitario_centavos": 60000,
  "estoque": 670,
  "status": "ativo"
}
```

O campo `preco_unitario_centavos` representa o preço unitário em
centavos. No exemplo, `60000` equivale a R\$ 600,00.

### 3. Categorias

  ------------------------------------------------------------------------------
  Método                  Rota                           Finalidade
  ----------------------- ------------------------------ -----------------------
  `POST`                  `/categorias`                  Cadastra uma categoria.

  `GET`                   `/categorias`                  Lista as categorias.

  `GET`                   `/categorias/{categoria_id}`   Busca uma categoria
                                                         pelo identificador.

  `PUT`                   `/categorias/{categoria_id}`   Atualiza uma categoria.

  `DELETE`                `/categorias/{categoria_id}`   Exclui uma categoria.
  ------------------------------------------------------------------------------

Exemplo de corpo para cadastro:

``` json
{
  "categoria": "Categoria Teste",
  "status": "ativa"
}
```

Exemplo de corpo para atualização:

``` json
{
  "nome": "frios",
  "status": "ativo"
}
```

### 4. Caixas

  ---------------------------------------------------------------------------------
  Método                  Rota                              Finalidade
  ----------------------- --------------------------------- -----------------------
  `POST`                  `/caixas`                         Cadastra um caixa.

  `POST`                  `/caixas/{caixa_id}`              Realiza a abertura do
                                                            caixa.

  `POST`                  `/caixas/fechamento/{caixa_id}`   Realiza o fechamento do
                                                            caixa.

  `POST`                  `/caixas/sangrias/{caixa_id}`     Registra uma sangria no
                                                            caixa.

  `PUT`                   `/caixas/sangria/{caixa_id}`      Realiza uma operação de
                                                            sangria usando o
                                                            identificador informado
                                                            no corpo.

  `GET`                   `/caixas/sangria/{sangria_id}`    Busca uma sangria pelo
                                                            identificador.
  ---------------------------------------------------------------------------------

#### Abrir um caixa

`POST /caixas/{caixa_id}`

``` json
{
  "valor_inicial_centavos": 1000
}
```

#### Fechar um caixa

`POST /caixas/fechamento/{caixa_id}`

``` json
{
  "valor_contado_centavos": 12000
}
```

#### Registrar uma sangria

`POST /caixas/sangrias/{caixa_id}`

``` json
{
  "valor_retirado_centavos": 3000
}
```

#### Realizar uma operação de sangria

`PUT /caixas/sangria/{caixa_id}`

``` json
{
  "sangria_id": 1
}
```

Os valores monetários desses exemplos também são expressos em centavos.

### 5. Relatórios de vendas

  ---------------------------------------------------------------------------------------------------------------
  Método                  Rota                                                            Finalidade
  ----------------------- --------------------------------------------------------------- -----------------------
  `GET`                   `/relatorios/vendas_iniciadas`                                  Consulta as vendas
                                                                                          iniciadas.

  `GET`                   `/relatorios/vendas_finalizadas`                                Consulta as vendas
                                                                                          finalizadas.

  `GET`                   `/relatorios/buscar/vendas_iniciadas/{venda_iniciada_id}`       Busca uma venda
                                                                                          iniciada pelo
                                                                                          identificador.

  `GET`                   `/relatorios/buscar/vendas_finalizadas/{venda_finalizada_id}`   Busca uma venda
                                                                                          finalizada pelo
                                                                                          identificador.
  ---------------------------------------------------------------------------------------------------------------

### 6. Relatórios de caixas

  ----------------------------------------------------------------------------------
  Método                  Rota                               Finalidade
  ----------------------- ---------------------------------- -----------------------
  `GET`                   `/relatorios/caixas/pagamentos`    Consulta os pagamentos
                                                             registrados nos caixas.

  `GET`                   `/relatorios/caixas_cadastrados`   Consulta os caixas
                                                             cadastrados.
  ----------------------------------------------------------------------------------

## Testando as rotas

A coleção JSON utilizada como referência contém as requisições
organizadas por área funcional e pode ser importada no Postman. Ela
utiliza variáveis para os identificadores, como:

-   `{{caixa_id}}`
-   `{{venda_id}}`
-   `{{venda_iniciada_id}}`
-   `{{codigo_produto}}`
-   `{{categoria_id}}`
-   `{{sangria_id}}`
-   `{{venda_finalizada_id}}`

Preencha essas variáveis com identificadores válidos do ambiente local
antes de executar as requisições.

## Integração futura com Vue.js

O front-end será desenvolvido futuramente com **Vue.js**. A aplicação
web consumirá a API para disponibilizar as operações do PDV, incluindo:

-   Cadastro e consulta de produtos e categorias.
-   Abertura e fechamento de caixas.
-   Registro, acompanhamento e finalização de vendas.
-   Operações de pagamento.
-   Visualização de relatórios.

A separação entre front-end e back-end permitirá que a interface seja
desenvolvida independentemente das regras de negócio implementadas na
API



**NexaPDV --- Sistema de Ponto de Venda.**
