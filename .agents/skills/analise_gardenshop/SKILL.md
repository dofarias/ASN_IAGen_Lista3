---
name: analise_gardenshop
description: "Compreende perguntas sobre a base de dados do Garden Shop, identifica tabelas e campos, esclarece ambiguidades, escreve ou reutiliza código Python, executa a consulta e apresenta a resposta."
---

# Garden Shop analytics

## 1. Tarefa e resultado esperado

Responder perguntas de análise sobre a base **Garden Shop** executando código
Python+pandas e devolvendo uma resposta verificável (tabela + código + saída real).

- **Objetivo:** apoiar o estudo de dados da loja, transformando perguntas em
  análises executadas sem reescrever código do zero a cada pedido.
- **Incluído:** pedidos entregues por mês, pedidos entregues por mês e UF, top UFs
  por pedidos entregues, ticket médio por pedido entregue, ticket médio por mês,
  pedidos por situação (`status`); filtros por UF e por período; gráficos opcionais.
- **Fora do escopo:** previsões/modelagem, dados fora dos 6 CSVs, edição dos CSVs
  originais.

## 2. Quando usar

Use quando o pedido for sobre os dados da Garden Shop (pedidos, itens, clientes,
produtos, categorias, fornecedores) e puder ser respondido por contagem,
agregação ou média sobre esses CSVs.

Não use para perguntas que exijam dados não presentes na base (ex.: frete,
margem por canal de venda, dados de outra loja) — nesses casos, explique que a
fonte disponível não responde.

## 3. Entradas

| Entrada | Formato ou origem | Obrigatória | Como usar ou validar |
| --- | --- | --- | --- |
| Pergunta | Texto em linguagem natural | Sim | Mapear para uma das análises (ou combinação de filtros) |
| Pasta de dados | Caminho para a pasta com os 6 CSVs | Sim | Validar que os 6 arquivos existem (`load_data`) |
| UF | Sigla de estado (ex.: PA) | Não | Filtra `customers.state`; comparação exata em maiúsculas |
| Período | Datas AAAA-MM-DD (início/fim), ano ou mês | Não | Aplicado ao campo de data da pergunta |

Quando faltar a pasta de dados, peça o caminho antes de executar. Quando um
filtro (UF/período) for ambíguo, confirme o valor antes de calcular. Para uma UF
inexistente ou período sem registros, execute e informe resultado vazio (ver §7).

## 4. Saída

- **Entrega:** resposta no chat com a tabela do resultado, o código/comando
  executado e a saída real; opcionalmente um CSV em `output/`.
- **Formato:** tabela (meses em `AAAA-MM`; valores em USD com 2 casas).
- **Destino:** CSVs de saída apenas se o usuário pedir, em `output/` (ou pasta
  informada), nunca sobrescrevendo os CSVs originais.
- **Evidências:** o comando/código executado e sua saída; para contagens pequenas,
  os valores conferem com contagem manual (ver §10 e §11).

## 5. Regras específicas da tarefa

As definições completas estão em [references/business_rules.md](references/business_rules.md).
Pontos que mudam o cálculo:

1. **Pedido entregue = `status == 'shipped'`** (não existe "delivered" nos dados).
2. **Mês de referência:** pedidos *realizados* → `order_date` (todos os status);
   pedidos *entregues* → `shipped_date` (só `shipped`).
3. **UF** vem de `customers.state` via `orders.customer_id` (não é a UF do fornecedor).
4. **Ticket médio por pedido:** some `quantity * unit_price` por pedido e só então
   tire a média entre pedidos (não é a média das linhas de itens). Sem frete.
5. **Junções sem duplicação:** conte pedidos no nível `order_id` (`nunique`); some
   itens no nível de item antes de agregar por pedido.
6. **Datas** nos CSVs são `AAAA-MM-DD` (o dicionário diz DD/MM/AAAA — ignore o
   dicionário neste ponto). Formato inesperado interrompe a execução.
7. **Contagem por situação (`status`):** perguntas sobre "pedidos por situação"
   consideram **todos os status** (`shipped`, `pending`, `processing`, `cancelled`),
   sem o filtro de "entregue". Nesse caso, o filtro de período (se usado) recai
   sobre `order_date`, não `shipped_date`. A saída lista apenas os status
   presentes; um status com zero pedidos não aparece na tabela.

## 6. Procedimento

### Compreender o pedido
1. Identifique a métrica (contagem, top UFs, ticket médio) e os filtros (UF, período).
2. Confirme a pasta de dados; consulte [references/data_dictionary.md](references/data_dictionary.md)
   e [references/business_rules.md](references/business_rules.md) quando houver dúvida de campo ou regra.
3. Resolva ambiguidades que mudem o resultado (ex.: "por mês" = `order_date` ou
   `shipped_date`?). Aplique a regra da §5 e informe qual foi usada.

### Executar a tarefa
4. Use `scripts/analyze.py` para as perguntas padrão (`delivered-by-month`,
   `delivered-by-month-state`, `top-states`, `avg-order-value`); para variações
   novas, importe as funções do script (`delivered_orders`, `q_*`) ou escreva
   código curto reaproveitando as mesmas regras.
5. Execute no ambiente autorizado (ver §8) e capture a saída real.

### Conferir o resultado
6. Confira contra um valor conhecido quando possível (ex.: total de pedidos
   `shipped` = 17; ver §10). Cheque que contagens de pedidos usam `nunique` sobre
   `order_id` e que o ticket médio agrega por pedido antes da média.
7. Verifique dados ausentes/resultado vazio e relate (ver §7 das regras).
8. Se houver divergência, identifique a causa, corrija e repita a verificação.

### Entregar
9. Apresente a tabela, o comando/código executado e a saída real, indicando os
   filtros e as definições usadas.
10. Informe limitações (ex.: "período sem registros", "frete não existe na base").

## 7. Recursos de apoio

- **Referências:** [references/data_dictionary.md](references/data_dictionary.md) — campos, relacionamentos e inconsistências;
  [references/business_rules.md](references/business_rules.md) — definições dos cálculos.
- **Scripts:** [scripts/analyze.py](scripts/analyze.py) — carregamento, filtros e as análises
  (`delivered-by-month`, `delivered-by-month-state`, `top-states`, `avg-order-value`);
  executar conforme §8.

Resolva os caminhos de `references/` e `scripts/` a partir da pasta da skill. A
pasta de dados e a pasta de saída são informadas pelo usuário (caminhos absolutos
ou relativos ao diretório atual), não presuma a máquina do autor.

## 8. Ambiente e ferramentas

- **Ferramentas necessárias:** execução de Python e leitura dos CSVs.
- **Dependências:** Python 3 e `pandas` (`pip install pandas`).
- **Execução (exemplos):**
  ```
  python scripts/analyze.py --data-dir "<pasta>" --question delivered-by-month
  python scripts/analyze.py --data-dir "<pasta>" --question delivered-by-month-state --start 2024-01-01 --end 2024-03-31
  python scripts/analyze.py --data-dir "<pasta>" --question top-states --top-n 5
  python scripts/analyze.py --data-dir "<pasta>" --question avg-order-value --state PA --start 2024-01-01 --end 2024-06-30
  ```
- **Se o recurso não estiver disponível:** se `pandas` não estiver instalado,
  informe e instale com `pip install pandas` antes de executar; se a pasta de
  dados não existir, peça o caminho correto.

Não relate um número como calculado sem ter executado o código que o produz;
mostre sempre o comando e a saída real.

## 9. Limites de atuação

- **Preservar:** os 6 CSVs originais e os arquivos de autoria da pasta `templates/`.
- **Alterações previstas:** criar apenas arquivos de saída em `output/` quando
  solicitado.
- **Decisões a esclarecer:** valor de UF/período ambíguo; se "por mês" se refere a
  pedidos realizados ou entregues quando a pergunta não deixar claro.

## 10. Critérios de conclusão

- A resposta traz a tabela, o comando/código executado e a saída real.
- As definições e filtros usados estão explícitos.
- Os valores conferem com a verificação possível (ex.: soma dos meses de pedidos
  entregues = total de pedidos `shipped` no período).
- Resultado vazio ou pergunta não respondível pela base é comunicado como tal.

## 11. Exemplos de uso

### Pedido pertinente
> "Quantos pedidos entregues foram realizados em cada mês?"

**Resultado esperado:** tabela com `month` (AAAA-MM) e `delivered_orders`; a soma
da coluna é igual ao total de pedidos `shipped` (17 na base atual, sem filtros).

### Pedido com duas dimensões e filtro
> "Pedidos entregues no 1º trimestre por mês e UF."

**Resultado esperado:** tabela com `month`, `state` e `delivered_orders`
(`delivered-by-month-state` com `--start 2024-01-01 --end 2024-03-31`); os totais
por mês coincidem com os de `delivered-by-month` no mesmo período.

### Pedido que abrange todos os status
> "Qual a quantidade de pedidos da UF = PA por situação?"

**Resultado esperado:** tabela com `status` e `orders` (`orders-by-status --state PA`),
considerando todos os status (não só `shipped`); status com zero pedidos não
aparecem na tabela.

### Entrada ausente ou inválida
> "Ticket médio por pedido entregue na UF ZZ."

**Comportamento esperado:** executa o filtro, não encontra pedidos para `state=ZZ`
e informa "nenhum registro para os filtros aplicados" em vez de um número.

### Pedido fora do escopo
> "Qual foi o custo de frete médio por pedido?"

**Comportamento esperado:** explicar que a base Garden Shop não contém dados de
frete, portanto a pergunta não pode ser respondida com esta fonte.
