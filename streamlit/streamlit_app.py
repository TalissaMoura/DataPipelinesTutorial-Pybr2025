import streamlit as st
import pandas as pd
import pathlib
from datetime import datetime, timedelta, time as dtime
import altair as alt
from coffee_sales_pipeline.src.pipeline_runner import run_pipeline



@st.cache_data
def load_data(start_time,end_time):
    run_pipeline(start_datetime=start_time.strftime("%Y-%m-%d %H:%M:%S"),
                 end_datetime=end_time.strftime("%Y-%m-%d %H:%M:%S"))
    DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
    processed_path = DATA_DIR / "processed" / "coffee_sales_summary.csv"
    df = pd.read_csv(processed_path)
    return df

st.set_page_config(page_title="coffee sales dashboard", layout="wide")
st.title("Coffee sales healthcheck Dashboard ☕📊")

# seletor de data e hora (sidebar)
st.sidebar.header("Selecione data e hora de referência")
# Define colunm names and default values
dt_col = "event_timestamp"
qty_sales_col = "total_vendas"
avg_sales_col = "media_por_hora"

default_date = dtime(year=2024, month=3, day=1)
default_time = dtime(hour=13, minute=00, second=0)

sel_date = st.sidebar.date_input("Data", value=default_date)
sel_time = st.sidebar.time_input("Hora", value=default_time)

selected_dt = datetime.combine(sel_date, sel_time)
start_dt = selected_dt - timedelta(hours=3)

# filtrar últimas 3 horas (exclusivo/inclusivo conforme solicitado)
df = load_data(start_dt, selected_dt)

## --- grafico de quantidade de vendas nas ultimas 3 horas
st.subheader(f"Quantidade de vendas total: {start_dt}  até  {selected_dt}  (últimas 3 horas)")

if df.empty:
    st.warning("Nenhum registro encontrado nas últimas 3 horas para a data/hora selecionada.")
else:
    # garantir que eixo temporal esteja como datetime
    df[dt_col] = pd.to_datetime(df[dt_col])

    # gráfico de linha com Altair
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X(dt_col, type="temporal", title="Horário"),
            y=alt.Y("total_vendas", type="quantitative", title="Quantidade de vendas"),
            tooltip=[dt_col, "total_vendas"],
        )
        .properties(width=900, height=400)
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("Total de vendas no período:")
    st.metric("Vendas (últimas 3h)", f"{int(df['total_vendas'].sum())}")

    st.dataframe(df[[dt_col, "total_vendas"]].reset_index(drop=True))

# --- gráfico de média por hora (mesma seleção de data/hora) ---

    chart_avg = (
        alt.Chart(df)
        .mark_line(point=True, color="#1f77b4")
        .encode(
            x=alt.X(dt_col, type="temporal", title="Horário"),
            y=alt.Y("media_por_hora", type="quantitative", title="Média de vendas por hora"),
            tooltip=[dt_col, "media_por_hora"],
        )
        .properties(width=900, height=400)
    )
    st.altair_chart(chart_avg, use_container_width=True)

    avg_val = float(df["media_por_hora"].mean())
    st.markdown("Média de vendas por hora no período:")
    st.metric("Média (últimas 3h)", f"{avg_val:.2f}")

    st.dataframe(df[[dt_col, "media_por_hora"]].reset_index(drop=True))

# --- gráfico de vendas por tipo de café ---
# try:
#     df_type, dt_col_type, type_col, qty_col = load_count_by_type(DATA_PATH_BY_TYPE)
# except FileNotFoundError:
#     st.warning(f"Arquivo de vendas por tipo não encontrado: {DATA_PATH_BY_TYPE}")
#     df_type = None
# except ValueError as e:
#     st.warning(f"Problema ao carregar dados por tipo: {e}")
#     df_type = None

# if df_type is not None:
#     df_type[dt_col_type] = pd.to_datetime(df_type[dt_col_type])

#     # filtrar pela janela de 3 horas (sem filtro por tipo)
#     mask_type = (
#         (df_type[dt_col_type] > start_dt)
#         & (df_type[dt_col_type] <= selected_dt)
#     )
#     window_type = df_type.loc[mask_type].copy()

#     st.subheader(f"Quantidade total de vendas por tipo de café: {start_dt} até {selected_dt} (últimas 3 horas)")

#     if window_type.empty:
#         st.warning("Nenhum registro de vendas por tipo nas últimas 3 horas para a data/hora selecionada.")
#     else:
#         # agregar por tipo e ordenar do mais vendido para o menos vendido
#         agg = (
#             window_type
#             .groupby(type_col)[qty_col]
#             .sum()
#             .reset_index()
#             .sort_values(qty_col, ascending=False)
#         )

#         # gráfico de barras ordenado
#         chart_type = (
#             alt.Chart(agg)
#             .mark_bar()
#             .encode(
#                 x=alt.X(type_col, sort=agg[type_col].tolist(), title="Tipo de café"),
#                 y=alt.Y(qty_col, type="quantitative", title="Quantidade de vendas"),
#                 tooltip=[type_col, qty_col],
#                 color=alt.Color(type_col, legend=None)
#             )
#             .properties(width=900, height=400)
#         )
#         st.altair_chart(chart_type, use_container_width=True)

#         st.markdown("Total de vendas por tipo no período (ordenado):")
#         st.dataframe(agg.rename(columns={type_col: "coffee_type", qty_col: "quantity"}).reset_index(drop=True))

