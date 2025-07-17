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


st.set_page_config(page_title="User Engagement & Session Behavior")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access this page.")
    st.stop()

from filters import show_user_info  
show_user_info()



# ["utm_source"].str.upper() != 'NULL')

st.title("📊 User Engagement & Session Behavior")

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



st.markdown("## 📈 Line + Column Chart – Avg Session Time & Count of sessions by session_path")

from visuals import line_column_avg_time_by_session_path

# Precomputed once at app start
combined_paths_data = preprocess_session_path_data(filtered_pageviews)
# st.dataframe(combined_paths_data)

# Visual in page
fig = line_column_avg_time_by_session_path(combined_paths_data)
st.plotly_chart(fig, use_container_width=True)


st.markdown("## 📈 Stacked Column Chart – Bounce Rate % by utm_source and utm_campaign")

from visuals import bounce_rate_stacked_column

pageviews_per_session = filtered_pageviews.groupby("website_session_id").size().reset_index(name="pageview_count")
bounced = pageviews_per_session[pageviews_per_session["pageview_count"] == 1]["website_session_id"]

fig = bounce_rate_stacked_column(filtered_sessions, bounced)
st.plotly_chart(fig, use_container_width=True)



st.markdown("## 📈 Stacked Column Chart – Bounce Rate % by utm_source and utm_content")

from visuals import bounce_rate_stacked_column_by_content

pageviews_per_session = filtered_pageviews.groupby("website_session_id").size().reset_index(name="pageview_count")
bounced = pageviews_per_session[pageviews_per_session["pageview_count"] == 1]["website_session_id"]

fig = bounce_rate_stacked_column_by_content(filtered_sessions, bounced)
st.plotly_chart(fig, use_container_width=True)



