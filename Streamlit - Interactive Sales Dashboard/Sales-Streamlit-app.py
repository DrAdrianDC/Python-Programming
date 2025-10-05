# ================================================
# 📊 Streamlit - Interactive Sales Dashboard
# ================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# 🔧 Page Configuration
# ------------------------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Real-Time Sales Dashboard")

# ------------------------------------------------
# 📥 Load Data with Cache
# ------------------------------------------------
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("sales.csv")
        data["date"] = pd.to_datetime(data["date"])
        data["sales"] = pd.to_numeric(data["sales"], errors="coerce")
        data["customers"] = pd.to_numeric(data["customers"], errors="coerce")
        data["visits"] = pd.to_numeric(data["visits"], errors="coerce")
        return data.dropna(subset=["date", "sales", "customers", "visits"])
    except FileNotFoundError:
        st.error("❌ The file 'sales.csv' was not found. Please upload the dataset.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ An error occurred while loading the data: {e}")
        st.stop()

data = load_data()

# ------------------------------------------------
# 🎚️ Sidebar Filters
# ------------------------------------------------
with st.sidebar:
    st.header("Filters")

    min_date = data["date"].min().date()
    max_date = data["date"].max().date()
    date_range = st.date_input("Select Date Range", [min_date, max_date])

    categories = ["All"] + sorted(data["category"].dropna().unique().tolist())
    category = st.selectbox("Category", categories)

# ------------------------------------------------
# 🔍 Data Filtering
# ------------------------------------------------
if len(date_range) == 2:
    start_date, end_date = date_range
    data = data[(data["date"].dt.date >= start_date) & (data["date"].dt.date <= end_date)]

if category != "All":
    data = data[data["category"] == category]

if data.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

# ------------------------------------------------
# 📈 Interactive Visualization
# ------------------------------------------------
st.subheader("📊 Sales by Product")

# Create bar chart
fig = px.bar(
    data,
    x="product",
    y="sales",
    color="category",
    title="Sales by Product and Category",
    text=data["sales"]  # exact values for each bar
)

# Format Y-axis and bar text
max_sales = data["sales"].max()
fig.update_yaxes(range=[0, max_sales*1.1], tickformat="$,.0f")  # Y-axis as dollars
fig.update_traces(texttemplate='$%{text:,.0f}', textposition='inside')  # text inside bars in dollars
fig.update_layout(xaxis_title="Product", yaxis_title="Sales ($)", title_x=0.5)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# 📉 Key Metrics
# ------------------------------------------------
total_sales = data["sales"].sum()
total_customers = data["customers"].sum()
total_visits = data["visits"].sum()

conversion_rate = (total_customers / total_visits) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Customers", f"{total_customers:,}")
col3.metric("Conversion Rate", f"{conversion_rate:.1f}%")

# ------------------------------------------------
# 📋 Data Table
# ------------------------------------------------
st.subheader("📋 Sales Details")
st.dataframe(data.sort_values("sales", ascending=False), use_container_width=True)

# ------------------------------------------------
# ✅ Footer
# ------------------------------------------------
st.markdown("---")
st.caption("Developed using Streamlit, Pandas, and Plotly.")
