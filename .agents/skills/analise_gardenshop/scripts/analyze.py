"""Copiloto de analytics para a base Garden Shop.

Carrega os 6 CSVs, aplica as regras de negócio acordadas (ver
references/business_rules.md) e responde às perguntas da v1. Pode ser usado
via CLI ou importado como módulo.

Uso (CLI):
    python analyze.py --data-dir "<pasta com os CSVs>" --question <nome> [filtros]

Perguntas disponíveis (--question):
    delivered-by-month   Pedidos entregues por mês (status=shipped, por shipped_date)
    top-states           Top N UFs por nº de pedidos entregues
    avg-order-value      Ticket médio por pedido entregue (soma de itens, sem frete)

Filtros opcionais:
    --state PA           Filtra pela UF do cliente
    --start 2024-01-01   Data inicial (inclusive) do campo de data da pergunta
    --end   2024-06-30   Data final (inclusive)
    --top-n 5            Nº de linhas para top-states (padrão 5)
    --out-dir <pasta>    Se informado, salva o resultado em CSV nessa pasta

As regras (definições de "entregue", mês de referência, ticket médio, UF do
cliente e junções sem duplicação) estão em references/business_rules.md.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

CSV_FILES = {
    "categories": "categories.csv",
    "customers": "customers.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "products": "products.csv",
    "suppliers": "suppliers.csv",
}

DELIVERED_STATUS = "shipped"


def load_data(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Carrega os CSVs e valida que os arquivos esperados existem."""
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise FileNotFoundError(f"Pasta de dados não encontrada: {data_dir}")

    missing = [f for f in CSV_FILES.values() if not (data_dir / f).exists()]
    if missing:
        raise FileNotFoundError(
            "Arquivos ausentes na pasta de dados: " + ", ".join(missing)
        )

    data = {name: pd.read_csv(data_dir / fname) for name, fname in CSV_FILES.items()}

    # Parse de datas em ISO (AAAA-MM-DD). errors='coerce' transforma formatos
    # inesperados em NaT, que detectamos abaixo.
    for col in ("order_date", "shipped_date"):
        data["orders"][col] = pd.to_datetime(
            data["orders"][col], format="%Y-%m-%d", errors="coerce"
        )
    bad = data["orders"]["order_date"].isna().sum()
    if bad:
        raise ValueError(
            f"{bad} valor(es) de order_date não estão no formato AAAA-MM-DD. "
            "Verifique o arquivo orders.csv antes de prosseguir."
        )
    return data


def _apply_state_filter(df: pd.DataFrame, customers: pd.DataFrame, state: str | None) -> pd.DataFrame:
    """Filtra um DataFrame de pedidos pela UF do cliente."""
    if not state:
        return df
    cust_states = customers[["customer_id", "state"]]
    merged = df.merge(cust_states, on="customer_id", how="left")
    return merged[merged["state"] == state].drop(columns=["state"])


def _apply_period_filter(
    df: pd.DataFrame, date_col: str, start: str | None, end: str | None
) -> pd.DataFrame:
    if start:
        df = df[df[date_col] >= pd.Timestamp(start)]
    if end:
        df = df[df[date_col] <= pd.Timestamp(end)]
    return df


def delivered_orders(
    data: dict[str, pd.DataFrame], state: str | None = None,
    start: str | None = None, end: str | None = None,
) -> pd.DataFrame:
    """Pedidos entregues (status=shipped), com filtros de UF e período por shipped_date."""
    orders = data["orders"]
    delivered = orders[orders["status"] == DELIVERED_STATUS].copy()
    delivered = _apply_period_filter(delivered, "shipped_date", start, end)
    delivered = _apply_state_filter(delivered, data["customers"], state)
    return delivered


def q_delivered_by_month(data, state=None, start=None, end=None) -> pd.DataFrame:
    """Quantos pedidos entregues por mês (shipped_date)."""
    delivered = delivered_orders(data, state, start, end)
    if delivered.empty:
        return pd.DataFrame(columns=["month", "delivered_orders"])
    delivered = delivered.dropna(subset=["shipped_date"])
    out = (
        delivered.assign(month=delivered["shipped_date"].dt.strftime("%Y-%m"))
        .groupby("month", as_index=False)["order_id"].nunique()
        .rename(columns={"order_id": "delivered_orders"})
        .sort_values("month")
        .reset_index(drop=True)
    )
    return out


def q_top_states(data, top_n=5, start=None, end=None) -> pd.DataFrame:
    """Top N UFs por nº de pedidos entregues."""
    delivered = delivered_orders(data, state=None, start=start, end=end)
    if delivered.empty:
        return pd.DataFrame(columns=["state", "delivered_orders"])
    merged = delivered.merge(
        data["customers"][["customer_id", "state"]], on="customer_id", how="left"
    )
    out = (
        merged.groupby("state", as_index=False)["order_id"].nunique()
        .rename(columns={"order_id": "delivered_orders"})
        .sort_values(["delivered_orders", "state"], ascending=[False, True])
        .head(top_n)
        .reset_index(drop=True)
    )
    return out


def q_delivered_by_month_state(data, state=None, start=None, end=None) -> pd.DataFrame:
    """Pedidos entregues detalhados por mês (shipped_date) e UF do cliente."""
    delivered = delivered_orders(data, state, start, end)
    if delivered.empty:
        return pd.DataFrame(columns=["month", "state", "delivered_orders"])
    delivered = delivered.dropna(subset=["shipped_date"])
    merged = delivered.merge(
        data["customers"][["customer_id", "state"]], on="customer_id", how="left"
    )
    out = (
        merged.assign(month=merged["shipped_date"].dt.strftime("%Y-%m"))
        .groupby(["month", "state"], as_index=False)["order_id"].nunique()
        .rename(columns={"order_id": "delivered_orders"})
        .sort_values(["month", "delivered_orders", "state"], ascending=[True, False, True])
        .reset_index(drop=True)
    )
    return out


def q_avg_order_value(data, state=None, start=None, end=None) -> pd.DataFrame:
    """Ticket médio por pedido entregue: soma de (quantity*unit_price) por pedido, depois a média."""
    delivered = delivered_orders(data, state, start, end)
    if delivered.empty:
        return pd.DataFrame(
            [{"delivered_orders": 0, "total_value": 0.0, "avg_order_value": None}]
        )
    items = data["order_items"].copy()
    items["line_value"] = items["quantity"] * items["unit_price"]
    # Valor por pedido (nível order_id), só dos pedidos entregues filtrados.
    per_order = (
        items[items["order_id"].isin(delivered["order_id"])]
        .groupby("order_id", as_index=False)["line_value"].sum()
        .rename(columns={"line_value": "order_value"})
    )
    n = len(per_order)
    total = per_order["order_value"].sum()
    avg = total / n if n else None
    return pd.DataFrame(
        [{
            "delivered_orders": n,
            "total_value": round(total, 2),
            "avg_order_value": round(avg, 2) if avg is not None else None,
        }]
    )


def q_orders_by_status(data, state=None, start=None, end=None) -> pd.DataFrame:
    """Quantidade de pedidos por situação (status), considerando todos os status.

    Diferente das demais análises, NÃO filtra por 'entregue'. O filtro de período,
    quando usado, é aplicado a order_date (data em que o pedido foi realizado),
    pois a pergunta abrange todos os status, inclusive os que não têm shipped_date.
    """
    orders = _apply_period_filter(data["orders"].copy(), "order_date", start, end)
    orders = _apply_state_filter(orders, data["customers"], state)
    if orders.empty:
        return pd.DataFrame(columns=["status", "orders"])
    out = (
        orders.groupby("status", as_index=False)["order_id"].nunique()
        .rename(columns={"order_id": "orders"})
        .sort_values(["orders", "status"], ascending=[False, True])
        .reset_index(drop=True)
    )
    return out


def q_avg_order_value_by_month(data, state=None, start=None, end=None) -> pd.DataFrame:
    """Ticket médio por pedido entregue, mês a mês (por shipped_date).

    Para cada pedido entregue, valor = soma de (quantity*unit_price); o pedido é
    atribuído ao mês de shipped_date; o ticket médio do mês é a média dos valores
    dos pedidos daquele mês.
    """
    delivered = delivered_orders(data, state, start, end)
    if delivered.empty:
        return pd.DataFrame(columns=["month", "delivered_orders", "total_value", "avg_order_value"])
    delivered = delivered.dropna(subset=["shipped_date"]).copy()
    delivered["month"] = delivered["shipped_date"].dt.strftime("%Y-%m")

    items = data["order_items"].copy()
    items["line_value"] = items["quantity"] * items["unit_price"]
    per_order = (
        items[items["order_id"].isin(delivered["order_id"])]
        .groupby("order_id", as_index=False)["line_value"].sum()
        .rename(columns={"line_value": "order_value"})
    )
    # Associa cada pedido ao seu mês de envio.
    per_order = per_order.merge(
        delivered[["order_id", "month"]], on="order_id", how="left"
    )
    out = (
        per_order.groupby("month", as_index=False)
        .agg(delivered_orders=("order_id", "nunique"),
             total_value=("order_value", "sum"),
             avg_order_value=("order_value", "mean"))
        .sort_values("month")
        .reset_index(drop=True)
    )
    out["total_value"] = out["total_value"].round(2)
    out["avg_order_value"] = out["avg_order_value"].round(2)
    return out


QUESTIONS = {
    "delivered-by-month": q_delivered_by_month,
    "delivered-by-month-state": q_delivered_by_month_state,
    "top-states": q_top_states,
    "avg-order-value": q_avg_order_value,
    "avg-order-value-by-month": q_avg_order_value_by_month,
    "orders-by-status": q_orders_by_status,
}


def make_chart(result: pd.DataFrame, question: str, out_path: Path, title: str | None = None) -> Path:
    """Gera um gráfico a partir do resultado de uma pergunta.

    - delivered-by-month: barras por mês.
    - top-states: barras por UF.
    - delivered-by-month-state: barras agrupadas (mês no eixo X, uma barra por UF).
    - avg-order-value-by-month: linha de tendência do ticket médio por mês.
    avg-order-value não é adequado a gráfico (valor único); nesse caso, levanta erro.
    """
    import matplotlib
    matplotlib.use("Agg")  # backend sem janela, salva em arquivo
    import matplotlib.pyplot as plt

    if result.empty:
        raise ValueError("Resultado vazio: não há dados para plotar.")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))

    if question == "delivered-by-month":
        ax.bar(result["month"], result["delivered_orders"], color="#4c9a2a")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Pedidos entregues")
    elif question == "top-states":
        ax.bar(result["state"], result["delivered_orders"], color="#4c9a2a")
        ax.set_xlabel("UF")
        ax.set_ylabel("Pedidos entregues")
    elif question == "delivered-by-month-state":
        pivot = result.pivot_table(
            index="month", columns="state", values="delivered_orders",
            aggfunc="sum", fill_value=0,
        )
        pivot.plot(kind="bar", ax=ax)
        ax.set_xlabel("Mês")
        ax.set_ylabel("Pedidos entregues")
        ax.legend(title="UF")
        plt.xticks(rotation=0)
    elif question == "avg-order-value-by-month":
        ax.plot(result["month"], result["avg_order_value"],
                marker="o", color="#4c9a2a")
        for x, y in zip(result["month"], result["avg_order_value"]):
            ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=8)
        ax.set_xlabel("Mês")
        ax.set_ylabel("Ticket médio (USD)")
        ax.set_ylim(bottom=0)
    else:
        raise ValueError(f"Pergunta '{question}' não tem gráfico padrão definido.")

    ax.set_title(title or question)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Garden Shop analytics copiloto")
    parser.add_argument("--data-dir", required=True, help="Pasta com os 6 CSVs")
    parser.add_argument("--question", required=True, choices=sorted(QUESTIONS))
    parser.add_argument("--state", default=None, help="UF do cliente (ex.: PA)")
    parser.add_argument("--start", default=None, help="Data inicial AAAA-MM-DD")
    parser.add_argument("--end", default=None, help="Data final AAAA-MM-DD")
    parser.add_argument("--top-n", type=int, default=5)
    parser.add_argument("--out-dir", default=None, help="Pasta para salvar o CSV do resultado")
    parser.add_argument("--chart", action="store_true", help="Gera um gráfico do resultado")
    parser.add_argument("--chart-out", default=None, help="Caminho do PNG (padrão: output/<pergunta>.png)")
    parser.add_argument("--title", default=None, help="Título do gráfico")
    args = parser.parse_args(argv)

    data = load_data(args.data_dir)

    if args.question == "top-states":
        result = q_top_states(data, top_n=args.top_n, start=args.start, end=args.end)
    else:
        result = QUESTIONS[args.question](
            data, state=args.state, start=args.start, end=args.end
        )

    print(result.to_string(index=False))

    if args.out_dir:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{args.question}.csv"
        result.to_csv(out_path, index=False)
        print(f"\nResultado salvo em: {out_path}")

    if args.chart:
        chart_out = Path(args.chart_out) if args.chart_out else Path("output") / f"{args.question}.png"
        saved = make_chart(result, args.question, chart_out, title=args.title)
        print(f"Gráfico salvo em: {saved}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
