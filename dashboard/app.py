import os
from datetime import datetime, timedelta, date
import pandas as pd
import plotly.express as px
import streamlit as st
import requests

# ----------------------------
# Config
# ----------------------------
API_URL = os.getenv("API_URL", "http://localhost:8000/api")  # your FastAPI backend
st.set_page_config(page_title="Telegram Medical Analytics", page_icon="🧪", layout="wide")
st.title("Telegram Medical Analytics Dashboard")
st.caption("Explore channel activity, products, and detections")

# ----------------------------
# Sidebar Filters
# ----------------------------
with st.sidebar:
    st.header("Filters")
    today = date.today()
    default_start = today - timedelta(days=30)
    date_range = st.date_input("Date range", (default_start, today))
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = default_start, today

    # -------------------------------
    # Channels fetched from API
    # -------------------------------
    try:
        resp = requests.get(f"{API_URL}/channels")
        resp.raise_for_status()
        channels = resp.json()  # list of all channels from backend
    except Exception:
        channels = []
    
    selected_channels = st.multiselect("Channels", channels)

    st.markdown("---")
    search_q = st.text_input("Search messages", "")

start_dt = datetime.combine(start_date, datetime.min.time())
end_dt = datetime.combine(end_date, datetime.min.time())

# ----------------------------
# Helper Functions
# ----------------------------
def fetch_top_products(limit=10, strategy="combined"):
    resp = requests.get(f"{API_URL}/reports/top-products", params={"limit": limit, "strategy": strategy})
    if resp.status_code == 200:
        return pd.DataFrame(resp.json())
    return pd.DataFrame(columns=["product_name", "count"])

def fetch_channel_activity(channel_name):
    resp = requests.get(f"{API_URL}/channels/{channel_name}/activity")
    if resp.status_code == 200:
        data = resp.json()
        return pd.DataFrame(data)
    return pd.DataFrame(columns=["date", "count"])

def search_messages(query):
    resp = requests.get(f"{API_URL}/search/messages", params={"query": query})
    if resp.status_code == 200:
        return pd.DataFrame(resp.json())
    return pd.DataFrame(columns=["message_id", "channel_name", "message_date", "message_text", "message_length", "has_image", "product_name"])

def fetch_kpis(channel_name):
    df = fetch_channel_activity(channel_name)
    total_messages = df['count'].sum() if not df.empty else 0
    # For demo, we fetch images count and avg length as placeholders
    # Ideally your API should provide `/overview` endpoint for KPIs
    images = int(total_messages * 0.3)  # placeholder
    avg_len = 120.0  # placeholder
    return {"total_messages": total_messages, "images": images, "avg_len": avg_len}

# ----------------------------
# Main Dashboard
# ----------------------------
if selected_channels:
    # For simplicity, use first channel
    channel = selected_channels[0]

    kpis = fetch_kpis(channel)

    # KPIs
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.metric("Total messages", f"{int(kpis['total_messages']):,}")
    with kpi_cols[1]:
        images = kpis['images']
        total = kpis['total_messages']
        pct = (images / total * 100) if total else 0
        st.metric("Messages with images", f"{images:,}", f"{pct:.1f}%")
    with kpi_cols[2]:
        st.metric("Avg. message length", f"{float(kpis['avg_len']):.1f}")

    # Activity by day
    left, right = st.columns((2,1), gap="large")
    with left:
        st.subheader(f"Activity by day ({channel})")
        df_activity = fetch_channel_activity(channel)
        if not df_activity.empty:
            df_activity['date'] = pd.to_datetime(df_activity['date'])
            fig = px.area(df_activity, x="date", y="count", template="plotly_white")
            fig.update_traces(line_color="#2E86AB")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity for the selected filters.")

    # Top products
    with right:
        st.subheader("Top products")
        df_products = fetch_top_products(limit=10)
        if not df_products.empty:
            fig2 = px.bar(df_products.head(10), x="count", y="product_name", orientation="h", template="plotly_white")
            fig2.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No products found.")

# ----------------------------
# Search Messages Tab
# ----------------------------
st.markdown("---")
tab1, tab2 = st.tabs(["Search", "Detections"])

with tab1:
    st.subheader("Search messages")
    if search_q.strip():
        df_search = search_messages(search_q.strip())
        st.caption(f"{len(df_search)} results")
        st.dataframe(df_search, use_container_width=True, hide_index=True)
    else:
        st.info("Enter a keyword above to search across messages.")

# ----------------------------
# Detections Tab (YOLO)
# ----------------------------
with tab2:
    st.subheader("Detected objects (YOLO)")
    # Placeholder: API endpoint for detections not provided in your CRUD
    st.info("YOLO detections not implemented yet. Add an endpoint to fetch detections.")
