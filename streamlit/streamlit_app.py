import streamlit as st
import pandas as pd
import pathlib
from datetime import datetime, timedelta, time as dtime
import altair as alt
import sys
import os

# Adiciona o diretório coffee_sales_pipeline/src ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../coffee_sales_pipeline/src')))
from pipeline_runner import run_pipeline

# --- Configurações iniciais ---
st.set_page_config(page_title="Coffee Sales Dashboard", layout="wide")
st.title("Coffee Sales Healthcheck Dashboard ☕📊")

# --- Seletor de data e hora ---
st.sidebar.header("Selecione data e hora de referência")

default_date = datetime(year=2024, month=3, day=1)
default_time = dtime(hour=13, minute=0, second=0)

sel_date = st.sidebar.date_input("Data", value=default_date)
sel_time = st.sidebar.time_input("Hora", value=default_time)

# Combina data e hora selecionadas
selected_dt = datetime.combine(sel_date, sel_time)
start_dt = selected_dt - timedelta(hours=3)

# --- Função para carregar dados ---
@st.cache_data
def load_data(start_time, end_time):
    df = run_pipeline(
        start_datetime=start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_datetime=end_time.strftime("%Y-%m-%d %H:%M:%S")
    )
    if isinstance(df,pd.DataFrame) and df.empty:
        return pd.DataFrame()
    else:
        DATA_DIR = pathlib.Path(__file__).parent.parent / "coffee_sales_pipeline" / "src" / "data"
        processed_path = DATA_DIR / "processed" / "coffee_sales_summary.csv"
        df = pd.read_csv(processed_path)
        return df

# --- Botão para executar ---
st.sidebar.markdown("---")
load_button = st.sidebar.button("🔄 Carregar dados")

if load_button:
    with st.spinner("Executando pipeline e carregando dados..."):
        df = load_data(start_dt, selected_dt)

    st.subheader(f"Quantidade de vendas total: {start_dt} até {selected_dt} (últimas 3 horas)")

    if df.empty:
        st.warning("Nenhum registro encontrado nas últimas 3 horas para a data/hora selecionada.")
    else:
        # garantir que eixo temporal esteja como datetime
        # df["event_timestamp"] = pd.to_datetime(df["event_timestamp"],utc=True)

        # --- Gráfico de quantidade de vendas ---
        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("event_timestamp:T", title="Horário"),
                y=alt.Y("total_vendas:Q", title="Quantidade de vendas"),
                tooltip=["event_timestamp", "total_vendas"],
            )
            .properties(width=900, height=400)
        )
        st.altair_chart(chart, use_container_width=True)

        st.metric("Vendas (últimas 3h)", f"{df['total_vendas'].sum()}")
        st.dataframe(df[["event_timestamp", "total_vendas"]].reset_index(drop=True))

        # --- Gráfico de valor médio de vendas ---
        st.subheader(f"Valor médio de vendas: {start_dt} até {selected_dt} (últimas 3 horas)")
        chart_amt = (
            alt.Chart(df)
            .mark_line(point=True, color="#1f77b4")
            .encode(
                x=alt.X("event_timestamp:T", title="Horário"),
                y=alt.Y("valor_medio:Q", title="Média de vendas por hora"),
                tooltip=["event_timestamp", "valor_medio"],
            )
            .properties(width=900, height=400)
        )
        st.altair_chart(chart_amt, use_container_width=True)

        avg_val = float(df["valor_medio"].mean())
        st.metric("Total em $ (últimas 3h)", f"{avg_val:.2f}")
        st.dataframe(df[["event_timestamp", "valor_medio"]].reset_index(drop=True))

        ## -- Gráfico de vendas por tipo de café ---
        st.subheader(f"Quantidade total de vendas por tipo de café: {start_dt} até {selected_dt} (últimas 3 horas)")
        agg_type = {}
        for index, row in df.iterrows():
            sales_by_type = row["vendas_por_tipo"]
            for item in eval(sales_by_type):
                coffee_type = item["coffee_name"]
                quantity = item["qtd_vendas"]
                if coffee_type in agg_type:
                    agg_type[coffee_type] += quantity
                else:
                    agg_type[coffee_type] = quantity
        df_agg_type = pd.DataFrame.from_dict(agg_type, orient='index', columns=['qtd_vendas']).reset_index().rename(columns={'index': 'coffee_name'})
        df_agg_type_sorted = df_agg_type.sort_values(by="qtd_vendas", ascending=False).reset_index(drop=True)
        chart_type = (
            alt.Chart(df_agg_type_sorted)
            .mark_bar()
            .encode(
                x=alt.X("coffee_name", title="Tipo de café"),
                y=alt.Y("qtd_vendas", type="quantitative", title="Quantidade de vendas"),
                tooltip=["coffee_name", "qtd_vendas"],
                color=alt.Color("coffee_name", legend=None)
            )
            .properties(width=900, height=400)
        )
        st.altair_chart(chart_type, use_container_width=True)

        st.markdown("Total de vendas por tipo no período (ordenado):")
        st.dataframe(df_agg_type_sorted)
else:
    st.info("👈 Selecione uma data e hora, depois clique em **'Carregar dados'** para gerar os gráficos.")

