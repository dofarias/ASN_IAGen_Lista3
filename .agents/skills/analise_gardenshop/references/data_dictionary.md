# Dicionário de dados — Garden Shop

Fonte: `garden_shop_dicionario_dados.xlsx`. Este arquivo resume os campos de cada
CSV e registra as inconsistências reais entre o dicionário e os dados.

Os 6 arquivos ficam na pasta de dados informada pelo usuário (ex.: `Garden Shop/`).
Todos usam vírgula como separador e cabeçalho na primeira linha.

## categories.csv
| Campo | Descrição | Valores válidos |
| --- | --- | --- |
| category_id | Identificador único da categoria | 1 a 8 |
| category_name | Nome da categoria | Houseplants, Seeds & Bulbs, Tools, Pots & Planters, Soil & Compost, Watering, Fertilizer, Outdoor Decor |

## customers.csv
| Campo | Descrição | Valores válidos |
| --- | --- | --- |
| customer_id | Identificador único do cliente | 1 a 20 |
| first_name | Primeiro nome | Texto não vazio |
| last_name | Sobrenome | Texto |
| email | E-mail do cliente | Formato de e-mail válido |
| phone | Telefone | Texto; pode estar ausente |
| city | Cidade | Nome de cidade |
| state | **UF (estado)** | Sigla de estado dos EUA (PA, CA, OH, OR, ...) |
| signup_date | Data de cadastro | AAAA-MM-DD |
| is_active | Cadastro ativo | true / false |

## orders.csv
| Campo | Descrição | Valores válidos |
| --- | --- | --- |
| order_id | Identificador único do pedido | 1 a 24 |
| customer_id | Cliente do pedido | existe em customers.customer_id |
| order_date | Data em que o pedido foi realizado | AAAA-MM-DD (ver nota 1) |
| shipped_date | Data de envio ao cliente | AAAA-MM-DD; ausente quando não enviado |
| status | Situação do pedido | shipped, pending, processing, cancelled (ver nota 2) |
| coupon_code | Cupom usado | texto; pode estar ausente |

## order_items.csv
| Campo | Descrição | Valores válidos |
| --- | --- | --- |
| order_item_id | Identificador único do item | 1 a 48 |
| order_id | Pedido ao qual o item pertence | existe em orders.order_id |
| product_id | Produto comprado | existe em products.product_id |
| quantity | Quantidade de unidades | inteiro positivo |
| unit_price | Preço unitário registrado no pedido | USD, não negativo |

## products.csv
| Campo | Descrição | Valores válidos |
| --- | --- | --- |
| product_id | Identificador único do produto | — |
| product_name | Nome comercial | texto |
| category_id | Categoria | existe em categories.category_id |
| supplier_id | Fornecedor | existe em suppliers.supplier_id |
| price | Preço atual de venda | USD |
| cost | Custo unitário | USD |
| quantity_on_hand | Estoque atual | inteiro não negativo |
| reorder_level | Nível de reposição | inteiro |
| discontinued | Descontinuado | true / false |

## suppliers.csv
| Campo | Descrição | Valores válidos |
| --- | --- | --- |
| supplier_id | Identificador único | 1 a 6 |
| supplier_name | Nome do fornecedor | texto |
| contact_email | E-mail de contato | formato válido; pode estar ausente |
| state | UF do fornecedor | sigla de estado dos EUA |

## Relacionamentos
```
customers 1───* orders 1───* order_items *───1 products *───1 categories
                                                     │
                                                     *───1 suppliers
```
- `orders.customer_id`  → `customers.customer_id`
- `order_items.order_id` → `orders.order_id`
- `order_items.product_id` → `products.product_id`
- `products.category_id` → `categories.category_id`
- `products.supplier_id` → `suppliers.supplier_id`

## Notas sobre inconsistências reais (confirmadas nos dados)
1. **Formato de datas**: o dicionário descreve `order_date`/`shipped_date` como
   `DD/MM/AAAA`, mas os CSVs reais usam `AAAA-MM-DD`. Faça o parse como ISO
   (`AAAA-MM-DD`). Se encontrar outro formato, pare e informe.
2. **Valores de status**: o dicionário cita `shipped, pending, processing, cancelled`.
   Nos dados atuais aparecem exatamente esses quatro. Não existe um status literal
   "delivered" / "entregue".
