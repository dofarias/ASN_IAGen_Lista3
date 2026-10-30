# Regras de negócio — Garden Shop analytics

Definições acordadas para os cálculos. Aplique-as de forma consistente e informe
ao usuário qual regra foi usada quando houver mais de uma interpretação possível.

## 1. "Pedido entregue"
Um pedido é considerado **entregue** quando `orders.status == 'shipped'`.
Não existe um status "delivered" nos dados; `shipped` é o estado que representa
pedido enviado/concluído ao cliente.

## 2. Mês de referência
- **Pedidos realizados por mês** → agrupar pelo mês de `order_date`, considerando
  **todos os status**.
- **Pedidos entregues por mês** → agrupar pelo mês de `shipped_date`, filtrando
  **apenas `status == 'shipped'`**.
- Formato do mês na saída: `AAAA-MM`.
- Pedidos entregues sem `shipped_date` não devem ocorrer (todo `shipped` tem data),
  mas se ocorrer, trate como data ausente e relate.

## 3. UF do cliente
A UF de um pedido vem de `customers.state`, associada por `orders.customer_id`.
Não confundir com `suppliers.state`.

## 4. Valor e ticket médio
- Não há coluna de frete; "sem frete" é o comportamento padrão.
- **Valor de um item** = `quantity * unit_price` (usar `unit_price` de
  `order_items`, que é o preço registrado no momento da compra, não `products.price`).
- **Valor de um pedido** = soma dos valores dos itens daquele pedido.
- **Ticket médio por pedido** = média, entre os pedidos considerados, do valor
  total de cada pedido. Ou seja: `soma(valor de cada pedido) / nº de pedidos`.
  Calcule o valor por pedido primeiro e só então tire a média; não é a média
  simples das linhas de `order_items`.

## 5. Evitar duplicação em junções
- Ao juntar `orders` com `order_items`, uma linha de pedido vira várias linhas
  (uma por item). Para **contar pedidos** ou usar atributos do pedido/cliente,
  faça a contagem/agrupamento no nível de `order_id` (ex.: `drop_duplicates` ou
  agregue os itens antes de juntar com o cliente).
- Ao somar valores de itens, mantenha o nível de item; só agregue por pedido
  depois de calcular `quantity * unit_price`.

## 6. Filtros suportados (v1)
- **Por UF**: `customers.state == <UF>` (comparação exata, maiúsculas).
- **Por período**: intervalo de datas aplicado ao campo de data relevante da
  pergunta (`order_date` para pedidos realizados, `shipped_date` para entregues).
  Aceite "ano = 2024", "entre AAAA-MM-DD e AAAA-MM-DD" ou "mês = AAAA-MM".
- Filtros podem ser combinados (UF + período).

## 7. Dados ausentes e resultados vazios
- Se um filtro não retornar nenhuma linha, informe explicitamente "nenhum
  registro para os filtros aplicados" em vez de apresentar uma tabela vazia sem
  explicação.
- Informe quando campos relevantes estiverem ausentes (ex.: pedido sem
  `shipped_date`).
