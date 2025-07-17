# Streamlit app structure
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pyodbc
from datetime import datetime
import plotly.graph_objects as go
from PIL import Image
import base64


from filters import apply_filters
from data_loader import load_data
from base_kpi import calculate_kpis
from data_loader import preprocess_session_path_data

from filters import show_user_info 
show_user_info()

# Load data once at app start
order_data, website_sessions, website_pageviews = load_data()

# kpis = calculate_kpis(order_data, website_sessions, website_pageviews)
filters = apply_filters(order_data, website_pageviews, website_sessions)

# Access values explicitly:
filtered_order_data = filters["order_data"]
filtered_sessions = filters["sessions"]
filtered_pageviews = filters["pageviews"]

if filtered_order_data.empty or filtered_sessions.empty or filtered_pageviews.empty:
    st.warning("⚠️ No data available for the selected filter combination.")


kpis = calculate_kpis(filtered_order_data, filtered_sessions, filtered_pageviews)






def set_bg_color(color="#f5f5dc"):  
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
    """, unsafe_allow_html=True)

set_bg_color("#f5fff5")  





# def set_bg_image(image_path):
#     with open(image_path, "rb") as file:
#         encoded = base64.b64encode(file.read()).decode()
#     bg_img_style = f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/png;base64,{encoded}");
#         background-size: cover;
#         background-position: center;
#         background-attachment: fixed;
#     }}
#     </style>
#     """
#     st.markdown(bg_img_style, unsafe_allow_html=True)

# set_bg_image("background.png")  






# st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# === Title and Header ===
st.title("🧸 Stuffed Animal E-Commerce Dashboard")
st.markdown("## 📊 Business Overview")

# === Business Context ===
st.markdown("""
<div style="font-size: 18px; line-height: 1.6">
🚀 <b>Business Context</b>:<br>
An <b>e-commerce startup</b> specializing in <i>stuffed animal toys</i>. Operating for <b>3 years</b>, the company is now preparing for the next round of funding.<br><br>
<b>Cindy Sharp (CEO)</b> seeks <b>data-driven insights</b> for her investor pitch. The analytics team is tasked with developing dashboards tailored for different stakeholders.
</div>
""", unsafe_allow_html=True)

# === Stakeholders ===
st.markdown("### 👥 Stakeholders")
st.markdown("""
- 👩‍💼 **Cindy Sharp** – CEO  
- 👨‍💻 **Morgan Rockwell** – Website Manager  
- 📣 **Tom Parmesan** – Marketing Director  
""")


# st.title("E-Commerce Product Analytics")

st.write("---")
st.subheader("Overall Business key values ")

# Layout KPI cards in 3 columns
col1, col2, col3 = st.columns(3)

col1.metric("🧾 Total Orders", f"{kpis['total_orders']:,}")
col2.metric("💰 Gross Revenue", f"${kpis['gross_revenue']:,.0f}")
col3.metric("📈 Gross Profit %", f"{kpis['gross_profit_pct']:.2f}%")

col4, col5, col6 = st.columns(3)
col4.metric("🎯 Conversion Rate", f"{kpis['conversion_rate_pct']:.2f}%")
col5.metric("🔁 Average Session Duration for Users (min)", f"{kpis['avg_user_session_duration_min']:.2f}%")
col6.metric("❌ Bounce Rate", f"{kpis['bounce_rate_pct']:.2f}%")


# Credentials
USER_CREDENTIALS = {
    "ceo": "ceo123",
    "web": "web123",
    "mkt": "mkt123"
}

def login():
    st.title("🔐 Login to continue to app: ")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success(f"✅ Welcome, **{username.capitalize()}**!")
                st.balloons()

                # Add dashboard access message
                st.markdown("🎉 You are now logged in. Welcome to our app :)")
                st.markdown("[📊 Visit our Dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTIwM2EwMmEtZjliMi00YjRjLTk1ODMtN2YxNzQyNDZjMDFiIiwidCI6IjgxMjEwNDM2LTRmZGMtNDMwZC1iYjU5LTI3NThjNzBjYTk1YyJ9&pageName=de47d37aba0e3207b502)")

                st.stop()
            else:
                st.error("❌ Invalid username or password.")
    else:
        st.success(f"Logged in as **{st.session_state.user.capitalize()}**")
        st.markdown("[📊 Visit our Dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTIwM2EwMmEtZjliMi00YjRjLTk1ODMtN2YxNzQyNDZjMDFiIiwidCI6IjgxMjEwNDM2LTRmZGMtNDMwZC1iYjU5LTI3NThjNzBjYTk1YyJ9&pageName=de47d37aba0e3207b502)")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

login()



# # Footer
# st.markdown("---")
# st.markdown("Welcome to our app :)")
# st.write("[Visit our Dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTIwM2EwMmEtZjliMi00YjRjLTk1ODMtN2YxNzQyNDZjMDFiIiwidCI6IjgxMjEwNDM2LTRmZGMtNDMwZC1iYjU5LTI3NThjNzBjYTk1YyJ9&pageName=de47d37aba0e3207b502)")





# st.snow()

# # Load data generated 
# revenue_by_source = kpis["revenue_per_channel"]

# # Show the table
# st.subheader("Revenue by UTM Source")
# st.dataframe(revenue_by_source)

# # Bar chart
# st.subheader("Bar Chart: Gross Revenue by Source")
# fig, ax = plt.subplots(figsize=(10, 6))
# bars = ax.bar(revenue_by_source['utm_source'], revenue_by_source['gross_revenue'], color='skyblue')

# # Add data labels
# for bar in bars:
#     height = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width() / 2, height, f"${height:,.0f}", ha='center', va='bottom', fontsize=10)

# ax.set_xlabel("UTM Source")
# ax.set_ylabel("Gross Revenue (USD)")
# ax.set_title("Gross Revenue by UTM Source")
# st.pyplot(fig)


# from visuals import line_chart_conversion_rate_by_product

# line_chart_conversion_rate_by_product(filtered_order_data, filtered_sessions)


# st.balloons()




