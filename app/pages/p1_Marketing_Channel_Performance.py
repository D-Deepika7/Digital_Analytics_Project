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

st.set_page_config(page_title="Marketing Channel Performance")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first to access this page.")
    st.stop()

from filters import show_user_info  
show_user_info()

st.title("📊 Marketing Channel Performance")

# Load data
order_data, website_sessions, website_pageviews = load_data()

# Get KPIs
kpis = calculate_kpis(order_data, website_sessions, website_pageviews)

st.write("---")
st.subheader("Overall Business key values (static)")

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
st.subheader("Key Values")

filters = apply_filters(order_data, website_pageviews, website_sessions)

# Access values explicitly:
filtered_order_data = filters["order_data"]
filtered_sessions = filters["sessions"]
filtered_pageviews = filters["pageviews"]


kpis = calculate_kpis(filtered_order_data, filtered_sessions, filtered_pageviews)

# 4. Display KPI cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{kpis['total_orders']:,}")
col2.metric("Gross Revenue", f"${kpis['gross_revenue']:,.0f}")
col3.metric("Conversion Rate", f"{kpis['conversion_rate_pct']:.2f}%")


# st.dataframe(kpis["revenue_per_channel"])

# st.subheader("Available KPI Keys")

# with st.expander("🔍 View Available KPI Keys"):
#     st.write(list(kpis.keys()))




# from visuals import (
#     line_chart_conversion_rate,
#     pie_chart_total_sessions,
#     bar_chart_gross_revenue
# )

# with st.expander("📊 Conversion Rate Over Time"):
#     line_chart_conversion_rate(filtered_order_data, filtered_sessions)

# with st.expander("📊 UTM Source Distribution"):
#     pie_chart_total_sessions(filtered_sessions)

# with st.expander("📊 Gross Revenue by UTM Source"):
#     bar_chart_gross_revenue(filtered_order_data)


from visuals import (
    line_chart_conversion_rate_1,
    pie_chart_total_sessions_1,
    bar_chart_gross_revenue_1
)

st.markdown("## 📈 Conversion Rate % by Year")

line_chart_conversion_rate_1(filtered_order_data, filtered_sessions)

st.markdown("## 📈 Total Session by UTM Source")
pie_chart_total_sessions_1(filtered_sessions)

st.markdown("## Gross Revenue by UTM Source")
bar_chart_gross_revenue_1(filtered_order_data)




# from visuals import channel_kpi_heatmap


# channel_kpi_heatmap(filtered_order_data, filtered_sessions, filtered_pageviews)
# # st.dataframe(matrix)



st.markdown("## 📈 Channel Sources Vs KPIs")
from visuals import channel_kpi_heatmap_plotly

channel_kpi_heatmap_plotly(filtered_order_data, filtered_sessions, filtered_pageviews)

# matrix, normalized_df = channel_kpi_heatmap_plotly(filtered_order_data, filtered_sessions, filtered_pageviews)


# with st.expander("📄 Normalized (for heatmap)"):
#     st.dataframe(normalized_df.round(2))

# with st.expander("📄 Original KPI Values"):
#     st.dataframe(matrix.round(2))


# st.dataframe(matrix.round(2))



# from visuals import line_column_avg_time_by_session_path

# fig = line_column_avg_time_by_session_path(filtered_pageviews)
# st.plotly_chart(fig, use_container_width=True)

# from visuals import line_column_avg_time_by_session_path

# # Precomputed once at app start
# combined_paths_data = preprocess_session_path_data(filtered_pageviews)
# st.dataframe(combined_paths_data)

# # Visual in page
# fig = line_column_avg_time_by_session_path(combined_paths_data)
# st.plotly_chart(fig, use_container_width=True)








st.balloons()




