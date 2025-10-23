import pandas as pd
from datetime import datetime

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma os dados brutos em métricas agregadas para o dashboard."""
    print("Transformando dados...")

    if df.empty:
        print("DataFrame vazio recebido para transformação.")
        return pd.DataFrame()

    df["event_timestamp"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],  # concatena data e hora
        errors="coerce"                 # valores inválidos viram NaT
    )

    # Trunca o event_Timestamp para o início da hora
    df["event_timestamp"] = df["event_timestamp"].dt.floor("H")

    # Total de vendas e valor por hora (como séries nomeadas)
    total_sales = df.groupby("event_timestamp")["money"].sum().rename("valor_total")
    total_transactions = df.groupby("event_timestamp")["money"].count().rename("total_vendas")

    # Vendas por tipo de café (mantendo valor agregado por tipo)
    coffee_sales = (
        df.groupby(by=["event_timestamp", "coffee_name"])["money"]
        .agg(["count", "sum"])
        .reset_index()
        .rename(columns={"count": "qtd_vendas", "sum": "valor_total_tipo"})
    )

    # Média por hora
    hourly_avg = (
        df.groupby("event_timestamp")
        .agg(qtd_vendas=("coffee_name", "count"), valor_medio=("money", "mean"))
        .reset_index()
    )

    # monta dataframe base com uma linha por event_timestamp
    print(total_sales)
    print(total_transactions)
    base = pd.concat([total_transactions, total_sales], axis=1).reset_index()

    # agrega vendas_por_tipo como lista de dicts por timestamp
    vendas_por_tipo = (
        coffee_sales
        .groupby("event_timestamp")
        .apply(lambda g: g[["coffee_name", "qtd_vendas", "valor_total_tipo"]].to_dict(orient="records"))
        .reset_index(name="vendas_por_tipo")
    )

    # junta tudo em um DataFrame com as keys como colunas e cada elemento das listas como rows
    final = (
        base
        .merge(hourly_avg, on="event_timestamp", how="left")
        .merge(vendas_por_tipo, on="event_timestamp", how="left")
    )

    print("Transformação concluída.")
    return final