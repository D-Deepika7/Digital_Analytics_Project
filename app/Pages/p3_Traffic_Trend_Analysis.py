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

st.set_page_config(page_title="Traffic Source & Segment Trends")


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access this page.")
    st.stop()

from filters import show_user_info  
show_user_info()



st.title("📊 Traffic Source & Segment Trends")

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
    line_chart_total_sessions_over_time,
    clustered_bar_sessions_by_source_device,
    stacked_bar_sessions_by_source_campaign,
    stacked_bar_sessions_by_source_content
)




# Line Chart – Total Sessions by Year and Month
st.plotly_chart(line_chart_total_sessions_over_time(filtered_sessions), use_container_width=True)

# Clustered Bar – Total Sessions by utm_source and device_type
st.plotly_chart(clustered_bar_sessions_by_source_device(filtered_sessions), use_container_width=True)

# Stacked Bar – Sessions by utm_source and utm_campaign
st.plotly_chart(stacked_bar_sessions_by_source_campaign(filtered_sessions), use_container_width=True)

# Stacked Bar – Sessions by utm_source and utm_content
st.plotly_chart(stacked_bar_sessions_by_source_content(filtered_sessions), use_container_width=True)




