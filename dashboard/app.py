import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Funil de Recrutamento", layout="wide")

DB_PATH = "../data/warehouse.duckdb"

@st.cache_data
def load_data():
    con = duckdb.connect(DB_PATH, read_only=True)
    conversao = con.execute("SELECT * FROM main.mart_conversao_por_etapa").fetchdf()
    tth_area = con.execute("SELECT * FROM main.mart_time_to_hire_por_area").fetchdf()
    motivos = con.execute("SELECT * FROM main.mart_motivo_reprovacao").fetchdf()
    pivot = con.execute("SELECT * FROM main.int_funil_pivot").fetchdf()
    con.close()
    return conversao, tth_area, motivos, pivot

conversao, tth_area, motivos, pivot = load_data()

st.title("📊 Funil de Recrutamento")

# --- Filtros na sidebar ---
st.sidebar.header("Filtros")
areas_disponiveis = sorted(pivot["area"].unique())
area_selecionada = st.sidebar.multiselect("Área", areas_disponiveis, default=areas_disponiveis)

pivot_filtrado = pivot[pivot["area"].isin(area_selecionada)]

# --- KPIs no topo ---
col1, col2, col3, col4 = st.columns(4)

total_candidatos = len(pivot_filtrado)
total_contratados = pivot_filtrado["foi_contratado"].sum()
taxa_conversao_geral = round(100 * total_contratados / total_candidatos, 1) if total_candidatos else 0
tth_medio = round(pivot_filtrado[pivot_filtrado["foi_contratado"]]["time_to_hire_dias"].mean(), 1)

col1.metric("Total de Candidatos", f"{total_candidatos:,}")
col2.metric("Total Contratado", f"{total_contratados:,}")
col3.metric("Taxa de Conversão Geral", f"{taxa_conversao_geral}%")
col4.metric("Time-to-Hire Médio", f"{tth_medio} dias")

st.divider()

# --- Funil de conversão ---
st.subheader("Funil de Conversão por Etapa")

fig_funil = go.Figure(go.Funnel(
    y=conversao["etapa"],
    x=conversao["total_aprovados"],
    textinfo="value+percent initial"
))
st.plotly_chart(fig_funil, use_container_width=True)

# --- Gargalos por etapa ---
st.subheader("Taxa de Conversão por Etapa (Gargalos)")

fig_gargalos = px.bar(
    conversao,
    x="etapa",
    y="taxa_conversao_pct",
    text="taxa_conversao_pct",
    color="taxa_conversao_pct",
    color_continuous_scale="RdYlGn"
)
fig_gargalos.update_traces(texttemplate="%{text}%", textposition="outside")
st.plotly_chart(fig_gargalos, use_container_width=True)

# --- Comparação entre áreas ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Time-to-Hire por Área")
    fig_tth = px.bar(
        tth_area.sort_values("time_to_hire_medio_dias"),
        x="time_to_hire_medio_dias",
        y="area",
        orientation="h",
        text="time_to_hire_medio_dias"
    )
    st.plotly_chart(fig_tth, use_container_width=True)

with col_b:
    st.subheader("Volume de Contratações por Área")
    fig_vol = px.pie(
        tth_area,
        values="total_contratados",
        names="area",
        hole=0.4
    )
    st.plotly_chart(fig_vol, use_container_width=True)

# --- Motivos de reprovação ---
st.subheader("Motivo de Reprovação Mais Comum por Etapa")

fig_motivos = px.bar(
    motivos,
    x="etapa",
    y="total_ocorrencias",
    color="motivo_reprovacao",
    barmode="stack"
)
st.plotly_chart(fig_motivos, use_container_width=True)

st.divider()
st.caption("Dados 100% sintéticos, gerados com Faker. Projeto de portfólio — pipeline Airflow + dbt + DuckDB + Streamlit.")
