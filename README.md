# ASN IA Gen - Lista 3 — Copiloto de analytics Garden Shop

Projeto da Lista 3: criação de uma **skill** que atua como copiloto de analytics
sobre a base de dados fictícia **Garden Shop** (uma loja de jardinagem). A skill
permite fazer perguntas em linguagem natural sobre pedidos, clientes, produtos e
fornecedores; o agente traduz a pergunta em uma análise, executa código
Python+pandas e apresenta a resposta com a tabela, o comando executado e a saída
real.

## Estrutura do repositório

```
.
├── .agents/skills/analise_gardenshop/   # a skill
│   ├── SKILL.md                         # definição da skill (quando usar, regras, procedimento)
│   ├── references/
│   │   ├── data_dictionary.md           # campos, relacionamentos e inconsistências
│   │   └── business_rules.md            # definições dos cálculos
│   └── scripts/
│       └── analyze.py                   # análises reutilizáveis (pandas) + gráficos
├── Garden Shop/                         # dados de origem (6 CSVs)
│   ├── categories.csv
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   └── suppliers.csv
├── garden_shop_dicionario_dados.xlsx    # dicionário de dados oficial
├── problema.md                          # enunciado do problema
├── templates/                           # materiais de autoria (modelo e roteiro)
├── verificacao/GardenShop.pbix          # verificação independente (Power BI)
└── IAGP_Lista3-Daniele_Farias.docx      # documento da lista
```

## A base Garden Shop

Seis tabelas relacionadas por IDs:

```
customers 1──* orders 1──* order_items *──1 products *──1 categories
                                                  │
                                                  *──1 suppliers
```

| Tabela | Conteúdo |
| --- | --- |
| customers | clientes, cidade, UF (`state`), ativo |
| orders | pedidos, cliente, datas, situação (`status`), cupom |
| order_items | itens de cada pedido (quantidade, preço unitário) |
| products | produtos, categoria, fornecedor, preço, custo, estoque |
| categories | categorias de produtos |
| suppliers | fornecedores |

Detalhes de campos e relacionamentos em
[`references/data_dictionary.md`](.agents/skills/analise_gardenshop/references/data_dictionary.md).

## Regras de negócio principais

As definições completas estão em
[`references/business_rules.md`](.agents/skills/analise_gardenshop/references/business_rules.md).
Resumo do que muda os cálculos:

- **Pedido entregue** = `orders.status == 'shipped'` (não existe status "delivered").
- **Mês de referência:** pedidos *realizados* usam `order_date`; pedidos
  *entregues* usam `shipped_date`.
- **UF** vem de `customers.state` (via `orders.customer_id`), não do fornecedor.
- **Ticket médio por pedido:** soma `quantity * unit_price` por pedido e depois a
  média entre pedidos (sem frete, que não existe na base).
- **Datas** nos CSVs estão em `AAAA-MM-DD` (o dicionário diz DD/MM/AAAA — os dados
  prevalecem).

## Como usar

### Pré-requisitos

- Python 3
- `pandas` (obrigatório): `pip install pandas`
- `matplotlib` (opcional, para gráficos `--chart`): `pip install matplotlib`

### Executar uma análise

```bash
python .agents/skills/analise_gardenshop/scripts/analyze.py --data-dir "Garden Shop" --question <pergunta> [filtros]
```

Análises disponíveis (`--question`):

| Pergunta | O que responde |
| --- | --- |
| `delivered-by-month` | Pedidos entregues por mês (`shipped_date`) |
| `delivered-by-month-state` | Pedidos entregues por mês e UF |
| `top-states` | Top N UFs por pedidos entregues (`--top-n`) |
| `avg-order-value` | Ticket médio por pedido entregue (sem frete) |
| `avg-order-value-by-month` | Ticket médio por pedido entregue, mês a mês |
| `orders-by-status` | Pedidos por situação (todos os status) |

Filtros opcionais:

| Filtro | Efeito |
| --- | --- |
| `--state PA` | Filtra pela UF do cliente |
| `--start 2024-01-01` | Data inicial (inclusive) |
| `--end 2024-03-31` | Data final (inclusive) |
| `--top-n 5` | Nº de linhas (apenas `top-states`) |
| `--out-dir output` | Salva o resultado em CSV |
| `--chart` | Gera um gráfico (requer matplotlib) |
| `--chart-out <png>` | Caminho do PNG (padrão `output/<pergunta>.png`) |
| `--title "..."` | Título do gráfico |

### Exemplos

```bash
# Pedidos entregues por mês
python .agents/skills/analise_gardenshop/scripts/analyze.py --data-dir "Garden Shop" --question delivered-by-month

# Top 5 UFs com mais pedidos entregues
python .agents/skills/analise_gardenshop/scripts/analyze.py --data-dir "Garden Shop" --question top-states --top-n 5

# Entregas no 1º trimestre por mês e UF, com gráfico
python .agents/skills/analise_gardenshop/scripts/analyze.py --data-dir "Garden Shop" --question delivered-by-month-state --start 2024-01-01 --end 2024-03-31 --chart

# Pedidos por situação de clientes de PA
python .agents/skills/analise_gardenshop/scripts/analyze.py --data-dir "Garden Shop" --question orders-by-status --state PA
```

### Usar via agente de IA

Em um ambiente que carrega skills a partir de `.agents/skills/`, o agente lê o
[`SKILL.md`](.agents/skills/analise_gardenshop/SKILL.md), aplica as regras de
negócio e responde a perguntas em linguagem natural, escolhendo a análise
adequada e mostrando o comando e a saída.

## Observações

- Os CSVs originais em `Garden Shop/` são preservados; a skill nunca os sobrescreve.
- Saídas geradas (CSVs e gráficos) vão para `output/`, que não é versionada
  (ver `.gitignore`).
- As contagens de exemplo foram conferidas manualmente (ex.: total de pedidos
  `shipped` = 17 na base atual).
