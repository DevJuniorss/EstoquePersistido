# Trabalho PErsistencia

## Alunos: 
- Leonardo Martins de Loiola - 553762
- Lucas Cavalcante Torres - 557156
- Roberto Alexandre da Silva Sousa Junior - 475223

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



## Diagramas Mermaid
```mermaid
classDiagram
direction LR

class Client {
    int: id
    str: name
    str: email
    str: address
}

class Order {
    int: id
    date: orderDate
    str: movementType
}

class Payment {
    int: id
    date: paymentDate
    str: paymentMethod
    bool: paymentStatus
}

class Product {
    int: id
    str: name
    int: quantity
    float: unitPrice
}

%% RELACIONAMENTOS
Client "1" -- "*" Order 
Order "1" -- "1" Payment
Order "*" --> "*" Product
```
