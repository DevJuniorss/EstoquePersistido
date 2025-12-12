# Persistencia

## Alunos: 
> Leonardo Martins de Loiola - 553762
> Lucas Cavalcante Torres - 557156
> Roberto Alexandre da Silva Sousa Junior - 475223

## Instruções para Uso

- Seguir guia do UV([https://uv.pydevtools.com/])
- source .venv/bin/activate
- uv add [nome da lib]

## Relações

- Produto
- Venda
- Categoria
- Cliente
- Pedido
- Pagamento
- Fornecedor
- Compra
- Item Compra
- Item Pedido

##Diagramas Mermaid
```mermaid
erDiagram

    CLIENTE {
        string id_cliente
        string tipo_cliente "CPF | CNPJ"
        string email
        string telefone
        string endereco
    }

    VENDA {
        string id_venda
        date data_venda
    }

    PEDIDO {
        string id_pedido
        int quantidade_itens
        float valor_total
    }

    ITEM_PEDIDO {
        string id_item
        int quantidade
        float valor_unitario
    }

    PRODUTO {
        string id_produto
        date data_validade
        date data_entrada_estoque
        date data_alerta_vencimento
        date data_venda
    }

    PAGAMENTO {
        string id_pagamento
        date data_pagamento
        string tipo_pagamento "À vista | Parcelado"
        int numero_parcelas
        string forma_recebimento "Dinheiro | Cartão | Pix"
    }

    FORNECEDOR {
        string id_fornecedor
        string tipo_documento "CPF | CNPJ"
        string telefone
        string endereco
        string email
    }

    COMPRA {
        string id_compra
        date data_compra
        float valor_total
    }

    ITEM_COMPRA {
        string id_item_compra
        int quantidade
        float valor_unitario
    }

    %% RELACIONAMENTOS — SAÍDA (VENDA)
    CLIENTE ||--o{ VENDA : realiza
    VENDA ||--o{ PEDIDO : possui
    PEDIDO ||--o{ ITEM_PEDIDO : contem
    ITEM_PEDIDO }o--|| PRODUTO : refere_se
    VENDA ||--|| PAGAMENTO : paga_por

    %% RELACIONAMENTOS — ENTRADA (COMPRA / ESTOQUE)
    FORNECEDOR ||--o{ COMPRA : realiza
    COMPRA ||--o{ ITEM_COMPRA : contem
    ITEM_COMPRA }o--|| PRODUTO : abastece
```

# Querys
## Clientes
- CONSULTAR_CLIENTES
- CONSULTAR_CLIENTE_POR_ID
- CONSULTAR_CLIENTES_POR_TIPO

## Produtos
- CONSULTAR_PRODUTOS
- CONSULTAR_PRODUTO_POR_ID
- CONSULTAR_PRODUTOS_COM_ESTOQUE_BAIXO
- CONSULTAR_PRODUTOS_PROXIMOS_DO_VENCIMENTO 

## Fornecedores
- CONSULTAR_FORNECEDORES
- CONSULTAR_FORNECEDOR_POR_ID

## Vendas
- CONSULTAR_VENDAS
- CONSULTAR_VENDAS_POR_PERIODO
- CONSULTAR_VENDAS_POR_CLIENTE
- CONSULTAR_VENDAS_POR_FORMA_PAGAMENTO

## Pedidos
- CONSULTAR_PEDIDOS
- CONSULTAR_PEDIDOS_POR_VENDA

## Itens em Pedido
- CONSULTAR_ITENS_PEDIDO_POR_PEDIDO

## Pagamentos
- CONSULTAR_PAGAMENTOS
- CONSULTAR_PAGAMENTOS_PARCELADOS
- CONSULTAR_PAGAMENTOS_A_VISTA

## Compras
- CONSULTAR_COMPRAS
- CONSULTAR_COMPRAS_POR_FORNECEDOR
- CONSULTAR_COMPRAS_POR_PERIODO

## Itens em Compra
- CONSULTAR_ITENS_COMPRA_POR_COMPRA

## Estoque
- CONSULTAR_MOVIMENTACAO_ESTOQUE
