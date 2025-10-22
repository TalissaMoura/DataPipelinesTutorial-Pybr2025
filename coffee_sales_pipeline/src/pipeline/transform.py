import pandas as pd
from datetime import datetime

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma os dados brutos em métricas agregadas para o dashboard."""
    print("Transformando dados...")

    df["event_timestamp"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],  # concatena data e hora
        errors="coerce"                 # valores inválidos viram NaT
    )

    # Total de vendas e valor
    total_sales = df["money"].sum()
    total_transactions = len(df)

    # Vendas por tipo de café
    coffee_sales = (
        df.groupby("coffee_name")["money"]
        .agg(["count", "sum"])
        .reset_index()
        .rename(columns={"count": "qtd_vendas", "sum": "valor_total"})
    )

    # Média por hora
    hourly_avg = (
        df.groupby("hour_of_day")
        .agg(qtd_vendas=("coffee_name", "count"), valor_medio=("money", "mean"))
        .reset_index()
    )

    summary = {
        "event_timestamp": datetime.now(),
        "total_vendas": total_transactions,
        "valor_total": total_sales,
        "vendas_por_tipo": coffee_sales.to_dict(orient="records"),
        "media_por_hora": hourly_avg.to_dict(orient="records"),
    }

    print("Transformação concluída.")
    return pd.DataFrame([summary])
