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


QUESTIONS = {
    "delivered-by-month": q_delivered_by_month,
    "delivered-by-month-state": q_delivered_by_month_state,
    "top-states": q_top_states,
    "avg-order-value": q_avg_order_value,
}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Garden Shop analytics copiloto")
    parser.add_argument("--data-dir", required=True, help="Pasta com os 6 CSVs")
    parser.add_argument("--question", required=True, choices=sorted(QUESTIONS))
    parser.add_argument("--state", default=None, help="UF do cliente (ex.: PA)")
    parser.add_argument("--start", default=None, help="Data inicial AAAA-MM-DD")
    parser.add_argument("--end", default=None, help="Data final AAAA-MM-DD")
    parser.add_argument("--top-n", type=int, default=5)
    parser.add_argument("--out-dir", default=None, help="Pasta para salvar o CSV do resultado")
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
