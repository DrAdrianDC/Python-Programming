# Streamlit - Dashboard de Ventas Interactivo

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración general
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.title("📊 Dashboard de Ventas en Tiempo Real")

# Sidebar con controles
with st.sidebar:
    st.header("Filtros")
    fecha = st.date_input("Selecciona fecha")
    categoria = st.selectbox("Categoría", ["Todas", "Tecnologia", "Ropa"])

# Carga de datos
data = pd.read_csv("ventas.csv")
data["fecha"] = pd.to_datetime(data["fecha"])

# Filtrado por fecha
if fecha:
    data = data[data["fecha"] == pd.to_datetime(fecha)]

# Filtrado por categoría
if categoria != "Todas":
    data = data[data["categoria"] == categoria]

# Si no hay datos tras filtrar
if data.empty:
    st.warning("⚠️ No hay datos disponibles para los filtros seleccionados.")
    st.stop()

# Visualización interactiva
fig = px.bar(
    data,
    x="producto",
    y="ventas",
    color="categoria",
    title="Ventas por Producto",
    text_auto=True
)
st.plotly_chart(fig, use_container_width=True)

# Métricas calculadas dinámicamente
total_ventas = data["ventas"].sum()
total_clientes = data["clientes"].sum()
conversion = (total_clientes / (len(data) * 10)) * 100  # Ejemplo simple de cálculo

col1, col2, col3 = st.columns(3)
col1.metric("Ventas Totales", f"${total_ventas:,.0f}")
col2.metric("Clientes Totales", f"{total_clientes:,}")
col3.metric("Conversión", f"{conversion:.1f}%")

# Tabla interactiva
st.subheader("📋 Detalle de Ventas")
st.dataframe(data, use_container_width=True)
