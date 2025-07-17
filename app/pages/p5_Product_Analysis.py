import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

import plotly.graph_objects as go

from filters import apply_filters
from data_loader import load_data
from base_kpi import calculate_kpis
from data_loader import preprocess_session_path_data


st.set_page_config(page_title="Product Performance")


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access this page.")
    st.stop()

from filters import show_user_info  
show_user_info()




# ["utm_source"].str.upper() != 'NULL')

st.title("📊 Product Performance")

# Load data
order_data, website_sessions, website_pageviews = load_data()

# Get KPIs
kpis = calculate_kpis(order_data, website_sessions, website_pageviews)

st.write("---")
st.subheader("Overall Business key values ")

filters = apply_filters(order_data, website_pageviews, website_sessions)

# Access values explicitly:
filtered_order_data = filters["order_data"]
filtered_sessions = filters["sessions"]
filtered_pageviews = filters["pageviews"]


kpis = calculate_kpis(filtered_order_data, filtered_sessions, filtered_pageviews)

# Layout KPI cards in 3 columns
col1, col2, col3 = st.columns(3)

col1.metric("🧾 Total Orders", f"{kpis['total_orders']:,}")
col2.metric("💰 Gross Revenue", f"${kpis['gross_revenue']:,.0f}")
col3.metric("📈 Gross Profit %", f"{kpis['gross_profit_pct']:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("🎯 Conversion Rate", f"{kpis['conversion_rate_pct']:.2f}%")
col5.metric("🔁 Average Session Duration for Users (min)", f"{kpis['avg_user_session_duration_min']:.2f}%")
col6.metric("❌ Bounce Rate", f"{kpis['bounce_rate_pct']:.2f}%")

st.write("---")



from visuals import (
    line_column_revenue_orders_by_product,
    donut_units_sold_by_product,
    matrix_cross_selling,
    bar_refunds_by_product
)

st.title("📦 Product Performance Dashboard")

# Assume filtered_order_data is passed or available
fig1 = line_column_revenue_orders_by_product(filtered_order_data)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

fig2 = donut_units_sold_by_product(filtered_order_data)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

fig3 = matrix_cross_selling(filtered_order_data)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

fig4 = bar_refunds_by_product(filtered_order_data)
st.plotly_chart(fig4, use_container_width=True)


