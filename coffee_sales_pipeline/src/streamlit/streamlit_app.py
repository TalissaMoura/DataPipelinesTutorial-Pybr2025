import streamlit as st
import pandas as pd
import pathlib
from datetime import datetime, timedelta, time as dtime
import altair as alt

_file_path = pathlib.Path(__file__).resolve()
parents = _file_path.parents
if len(parents) > 1:
    base_dir = parents[1]
else:
    base_dir = _file_path.parent

DATA_PATH_COUNT = base_dir / "data" / "processed" / "dummy_coffee_sales_data_number_of_sales_per_hour.csv"
DATA_PATH_AVG = base_dir / "data" / "processed" / "dummy_coffee_sales_data_average_number_of_sales_per_hour.csv"
DATA_PATH_BY_TYPE = base_dir / "data" / "processed" / "dummy_coffee_sales_data_count_number_of_sales_per_hour_and_coffee.csv"

@st.cache_data
def load_count_data(path: pathlib.Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "event_timestamp" not in df.columns:
        raise ValueError("Coluna 'event_timestamp' não encontrada no dataset.")
    if "coffee_sales" not in df.columns:
        raise ValueError("Coluna 'coffee_sales' não encontrada no dataset.")
    
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
    dt_col = "event_timestamp"
    sales_col = "coffee_sales"

    return df, dt_col, sales_col

@st.cache_data
def load_avg_data(path: pathlib.Path):
    df = pd.read_csv(path)
    if "event_timestamp" not in df.columns:
        raise ValueError("Coluna 'event_timestamp' não encontrada no dataset de médias.")
    if "coffee_sales_avg_amount" not in df.columns:
        raise ValueError("Coluna 'coffee_sales_avg_amount' não encontrada no dataset de médias.")
    
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
    dt_col = "event_timestamp"
    avg_col = "coffee_sales_avg_amount"
    return df, dt_col, avg_col

@st.cache_data
def load_count_by_type(path: pathlib.Path):
    df = pd.read_csv(path)
    if "event_timestamp" not in df.columns:
        raise ValueError("Coluna 'event_timestamp' não encontrada no dataset por tipo.")
    if "coffee_type" not in df.columns:
        raise ValueError("Coluna 'coffee_type' não encontrada no dataset por tipo.")
    # aceitar variações no nome da coluna de quantidade
    qty_candidates = ["coffee_sales_quanity", "coffee_sales_quantity", "coffee_sales"]
    qty_col = next((c for c in qty_candidates if c in df.columns), None)
    if qty_col is None:
        raise ValueError("Coluna de quantidade de vendas não encontrada no dataset por tipo.")
    df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
    return df, "event_timestamp", "coffee_type", qty_col

st.set_page_config(page_title="coffee sales dashboard", layout="wide")
st.title("Coffee sales healthcheck Dashboard ☕📊")

# carregar dados
try:
    df, dt_col, sales_col = load_count_data(DATA_PATH_COUNT)
except FileNotFoundError:
    st.error(f"Arquivo não encontrado: {DATA_PATH_COUNT}")
    st.stop()

if sales_col is None:
    st.error("Não foi possível identificar a coluna de vendas no dataset.")
    st.stop()

# seletor de data e hora (sidebar)
st.sidebar.header("Selecione data e hora de referência")
max_dt = df[dt_col].max()
default_date = max_dt.date()
default_time = dtime(hour=max_dt.hour, minute=max_dt.minute, second=0)

sel_date = st.sidebar.date_input("Data", value=default_date)
sel_time = st.sidebar.time_input("Hora", value=default_time)

selected_dt = datetime.combine(sel_date, sel_time)
# garantir que a seleção não ultrapasse o máximo disponível
if selected_dt > max_dt:
    st.sidebar.info(f"Data selecionada maior que a última disponível ({max_dt}). Usando {max_dt}.")
    selected_dt = max_dt

start_dt = selected_dt - timedelta(hours=3)

# filtrar últimas 3 horas (exclusivo/inclusivo conforme solicitado)
mask = (df[dt_col] > start_dt) & (df[dt_col] <= selected_dt)
window = df.loc[mask].copy()

## --- grafico de quantidade de vendas nas ultimas 3 horas
st.subheader(f"Quantidade de vendas total: {start_dt}  até  {selected_dt}  (últimas 3 horas)")

if window.empty:
    st.warning("Nenhum registro encontrado nas últimas 3 horas para a data/hora selecionada.")
else:
    # garantir que eixo temporal esteja como datetime
    window[dt_col] = pd.to_datetime(window[dt_col])

    # gráfico de linha com Altair
    chart = (
        alt.Chart(window)
        .mark_line(point=True)
        .encode(
            x=alt.X(dt_col, type="temporal", title="Horário"),
            y=alt.Y(sales_col, type="quantitative", title="Quantidade de vendas"),
            tooltip=[dt_col, sales_col],
        )
        .properties(width=900, height=400)
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("Total de vendas no período:")
    st.metric("Vendas (últimas 3h)", f"{int(window[sales_col].sum())}")

    st.dataframe(window[[dt_col, sales_col]].reset_index(drop=True))

# --- gráfico de média por hora (mesma seleção de data/hora) ---
try:
    df_avg, dt_col_avg, avg_col = load_avg_data(DATA_PATH_AVG)
except FileNotFoundError:
    st.warning(f"Arquivo de médias não encontrado: {DATA_PATH_AVG}")
    df_avg = None
    dt_col_avg = None
    avg_col = None

if df_avg is not None:
    # garantir datetime
    df_avg[dt_col_avg] = pd.to_datetime(df_avg[dt_col_avg])

    mask_avg = (df_avg[dt_col_avg] > start_dt) & (df_avg[dt_col_avg] <= selected_dt)
    window_avg = df_avg.loc[mask_avg].copy()

    st.subheader(f"Média de vendas por hora: {start_dt} até {selected_dt} (últimas 3 horas)")

    if window_avg.empty:
        st.warning("Nenhum registro de média encontrado nas últimas 3 horas para a data/hora selecionada.")
    else:
        chart_avg = (
            alt.Chart(window_avg)
            .mark_line(point=True, color="#1f77b4")
            .encode(
                x=alt.X(dt_col_avg, type="temporal", title="Horário"),
                y=alt.Y(avg_col, type="quantitative", title="Média de vendas por hora"),
                tooltip=[dt_col_avg, avg_col],
            )
            .properties(width=900, height=400)
        )
        st.altair_chart(chart_avg, use_container_width=True)

        avg_val = float(window_avg[avg_col].mean())
        st.markdown("Média de vendas por hora no período:")
        st.metric("Média (últimas 3h)", f"{avg_val:.2f}")

        st.dataframe(window_avg[[dt_col_avg, avg_col]].reset_index(drop=True))

# --- gráfico de vendas por tipo de café ---
try:
    df_type, dt_col_type, type_col, qty_col = load_count_by_type(DATA_PATH_BY_TYPE)
except FileNotFoundError:
    st.warning(f"Arquivo de vendas por tipo não encontrado: {DATA_PATH_BY_TYPE}")
    df_type = None
except ValueError as e:
    st.warning(f"Problema ao carregar dados por tipo: {e}")
    df_type = None

if df_type is not None:
    df_type[dt_col_type] = pd.to_datetime(df_type[dt_col_type])

    # filtrar pela janela de 3 horas (sem filtro por tipo)
    mask_type = (
        (df_type[dt_col_type] > start_dt)
        & (df_type[dt_col_type] <= selected_dt)
    )
    window_type = df_type.loc[mask_type].copy()

    st.subheader(f"Quantidade total de vendas por tipo de café: {start_dt} até {selected_dt} (últimas 3 horas)")

    if window_type.empty:
        st.warning("Nenhum registro de vendas por tipo nas últimas 3 horas para a data/hora selecionada.")
    else:
        # agregar por tipo e ordenar do mais vendido para o menos vendido
        agg = (
            window_type
            .groupby(type_col)[qty_col]
            .sum()
            .reset_index()
            .sort_values(qty_col, ascending=False)
        )

        # gráfico de barras ordenado
        chart_type = (
            alt.Chart(agg)
            .mark_bar()
            .encode(
                x=alt.X(type_col, sort=agg[type_col].tolist(), title="Tipo de café"),
                y=alt.Y(qty_col, type="quantitative", title="Quantidade de vendas"),
                tooltip=[type_col, qty_col],
                color=alt.Color(type_col, legend=None)
            )
            .properties(width=900, height=400)
        )
        st.altair_chart(chart_type, use_container_width=True)

        st.markdown("Total de vendas por tipo no período (ordenado):")
        st.dataframe(agg.rename(columns={type_col: "coffee_type", qty_col: "quantity"}).reset_index(drop=True))

