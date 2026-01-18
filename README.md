# Trabalho Persistência: API com FastAPI e MongoDB

## Alunos
- Leonardo Martins de Loiola - 553762
- Lucas Cavalcante Torres - 557156
- Roberto Alexandre da Silva Sousa Junior - 475223

## Descrição do Projeto
Este projeto consiste em um sistema de gerenciamento de vendas e produtos, migrado de uma arquitetura relacional para **NoSQL**, utilizando **FastAPI** e **MongoDB** (via **Beanie ODM**). Ele contempla operações de CRUD completas para clientes, pedidos e produtos, além de consultas avançadas utilizando recursos nativos do MongoDB.

O projeto segue boas práticas de desenvolvimento assíncrono e arquitetura modular, garantindo performance e escalabilidade.

### Funcionalidades Implementadas
- **Tecnologia NoSQL:** Persistência de dados utilizando MongoDB e Motor (driver assíncrono).
- **ODM Beanie:** Mapeamento de objetos-documentos para validação e estruturação dos dados.
- **Consultas Avançadas:**
    - Busca textual por **Regex** (Case-insensitive) para clientes e produtos.
    - **Aggregation Pipelines** para estatísticas (ex: contagem de itens por pedido, total de pedidos por cliente).
    - Filtros temporais (consultas por ano).
- **Relacionamentos:**
    - Uso de **Document Links** (Referências) para relacionar Pedidos a Clientes e Produtos.
    - Uso de **Embedded Documents** (Documentos embutidos) para Pagamentos e Itens do Pedido, otimizando a leitura.
    - Carregamento inteligente de relações com `fetch_links=True`.
- **Paginação:** Implementada nativamente com `skip` e `limit` do MongoDB em todos os endpoints de listagem.
- **Gerenciamento de Dependências:** Utilização do **uv** para gestão ágil do ambiente virtual.

Link do repositório do projeto para mais detalhes: [repositorio](https://github.com/DevJuniorss/EstoquePersistido)

## Estrutura do Projeto
O projeto está organizado em camadas para facilitar a manutenção:
- `models`: Definição dos Documentos (`Client`, `Product`, `Order`) e sub-documentos (`Payment`, `OrderItem`).
- `crud`: Camada de acesso direto ao banco (queries Beanie, aggregates, filtros).
- `services`: Regras de negócio e orquestração dos dados.
- `routers`: Endpoints da API (Controllers).
- `db`: Configuração da conexão com o MongoDB Atlas ou Local.

## Esquema de Banco (NoSQL)

Neste modelo não-relaciona, utilizamos **Coleções** e **Documentos**. O diagrama abaixo ilustra como os dados estão estruturados e relacionados. Note que `Payment` e `OrderItem` vivem dentro de `Order`.

```mermaid
classDiagram
    direction LR

    class Client {
        <<Collection>>
        _id: ObjectId
        name: str
        email: str
        address: str
    }

    class Product {
        <<Collection>>
        _id: ObjectId
        name: str
        quantity: int
        unitPrice: float
    }

    class Order {
        <<Collection>>
        _id: ObjectId
        order_date: datetime
        movement_type: str
        client: Link[Client]
        payment: Embedded[Payment]
        items: List[Embedded[OrderItem]]
    }

    class Payment {
        <<Embedded>>
        payment_method: str
        payment_date: datetime
        status: str
    }

    class OrderItem {
        <<Embedded>>
        quantity: int
        product: Link[Product]
    }

    %% RELACIONAMENTOS NOSQL
    Client "1" -- "0..*" Order : Referenced (Link)
    Order *-- "1" Payment : Embedded (Dentro do Documento)
    Order *-- "1..*" OrderItem : Embedded List (Dentro do Documento)
    OrderItem ..> Product : Referenced (Link)
    ```