import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    layout="wide"
)

st.title("📊 Behavioral Customer Analytics Platform")
st.markdown("RFM Based Customer Segmentation Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("rfm_segments.csv")
    return df

df = load_data()

# --------------------------------------------------
# Cluster Mapping (Business Friendly Names)
# --------------------------------------------------
cluster_map = {
    0: "🏆 High Value",
    1: "💰 Regular",
    2: "😴 Inactive",
    3: "🚨 At Risk"
}

df["Cluster_Label"] = df["Cluster"].map(cluster_map)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------
total_revenue = df["Monetary"].sum()
total_customers = df["CustomerID"].nunique()
avg_revenue = df["Monetary"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💵 Total Revenue", f"{total_revenue:,.0f}")
col2.metric("👥 Total Customers", total_customers)
col3.metric("📈 Avg Revenue per Customer", f"{avg_revenue:,.0f}")

st.divider()

# --------------------------------------------------
# Cluster Explanation Section
# --------------------------------------------------
st.subheader("📌 Cluster Explanation")

st.info("""
🏆 **High Value Customers**
- High spending
- Frequent purchases
- Recently active

💰 **Regular Customers**
- Moderate spending
- Average frequency

😴 **Inactive Customers**
- Low frequency
- Not recent buyers

🚨 **At Risk Customers**
- Used to purchase
- Haven’t purchased recently
""")

st.divider()

# --------------------------------------------------
# Revenue by Cluster (Bar Chart)
# --------------------------------------------------
st.subheader("💰 Revenue Contribution by Cluster")

cluster_revenue = (
    df.groupby("Cluster_Label")["Monetary"]
    .sum()
    .reset_index()
    .sort_values(by="Monetary", ascending=False)
)

fig_revenue = px.bar(
    cluster_revenue,
    x="Cluster_Label",
    y="Monetary",
    color="Cluster_Label",
    text_auto=True
)

st.plotly_chart(fig_revenue, use_container_width=True)

st.divider()

# --------------------------------------------------
# Top 5 Customers by Cluster
# --------------------------------------------------
st.subheader("🏆 Top 5 Customers by Cluster")

selected_cluster = st.selectbox(
    "Select Cluster",
    df["Cluster_Label"].unique()
)

cluster_df = df[df["Cluster_Label"] == selected_cluster]

top5_cluster = (
    cluster_df.groupby("CustomerID")["Monetary"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig_top5 = px.bar(
    top5_cluster,
    x="CustomerID",
    y="Monetary",
    text_auto=True
)

st.plotly_chart(fig_top5, use_container_width=True)
st.dataframe(top5_cluster, use_container_width=True)

st.divider()

# --------------------------------------------------
# RFM Scatter Plot
# --------------------------------------------------
st.subheader("📊 RFM Segmentation View")

fig_scatter = px.scatter(
    df,
    x="Recency",
    y="Monetary",
    color="Cluster_Label",
    hover_data=["CustomerID", "Frequency"]
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# --------------------------------------------------
# Detailed Filtered View
# --------------------------------------------------
st.subheader("🔎 View Customers by Cluster")

filtered_df = df[df["Cluster_Label"] == selected_cluster]

st.dataframe(filtered_df, use_container_width=True)