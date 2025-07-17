import numpy as np
import pandas as pd
import pyodbc  
from datetime import datetime
import streamlit as st
import os


@st.cache_data  # Caches the result (until input changes)

def load_data():
    # # Connect Database

    # # Connection settings
    # server = 'LAPTOP-3IH234A8\SQLEXPRESS01'
    # database = 'Digital_Product_Analytics_Project'        

    # # Connection string (Windows Authentication)
    # conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    # # Connect and read a table
    # conn = pyodbc.connect(conn_str)

    # # Extract Tables
    # order_items = pd.read_sql("SELECT * FROM order_items", conn)
    # orders = pd.read_sql("SELECT * FROM orders", conn)
    # products = pd.read_sql("SELECT * FROM products", conn)
    # order_item_refunds = pd.read_sql("SELECT * FROM order_item_refunds", conn)
    # website_sessions = pd.read_sql("SELECT * FROM website_sessions", conn)
    # website_pageviews = pd.read_sql("SELECT * FROM website_pageviews", conn)


    data_path = "data"  # folder where your CSVs are saved

    order_items = pd.read_csv(os.path.join(data_path, "order_items.csv"))
    orders = pd.read_csv(os.path.join(data_path, "orders.csv"))
    products = pd.read_csv(os.path.join(data_path, "products.csv"))
    order_item_refunds = pd.read_csv(os.path.join(data_path, "order_item_refunds.csv"))
    website_sessions = pd.read_csv(os.path.join(data_path, "website_sessions.csv"))
    website_pageviews = pd.read_csv(os.path.join(data_path, "website_pageviews.csv"))


    # Merge to prepare order_data
    order_data = order_items.merge(orders, on='order_id', suffixes=('_item', '_order'))
    order_data = order_data.merge(products, on='product_id', how='left')
    order_data = order_data.merge(order_item_refunds, on='order_item_id', how='left', suffixes=('', '_refund'))
    order_data = order_data.merge(website_sessions, on='website_session_id', how='left', suffixes=('', '_session'))

    return order_data, website_sessions, website_pageviews






@st.cache_data(show_spinner=False)
def preprocess_session_path_data(website_pageviews):
    website_pageviews['created_at'] = pd.to_datetime(website_pageviews['created_at'])

    # Session paths
    session_paths = (
        website_pageviews.sort_values(['website_session_id', 'created_at'])
        .groupby('website_session_id')['pageview_url']
        .apply(lambda x: ' → '.join(x))
        .reset_index()
    )

    # Session durations
    session_duration = (
        website_pageviews.groupby('website_session_id')['created_at']
        .agg(session_start='min', session_end='max')
        .reset_index()
    )
    session_duration['session_duration_min'] = (
        (session_duration['session_end'] - session_duration['session_start']).dt.total_seconds() / 60
    )

    # Combine both
    combined = session_paths.merge(session_duration, on='website_session_id')
   
    return combined


















