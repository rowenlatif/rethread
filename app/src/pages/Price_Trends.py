import logging
logger = logging.getLogger(__name__)

import pandas as pd
import streamlit as st
from datetime import datetime, date
import plotly.express as px
import requests
from modules.nav import SideBarLinks

# Sidebar and layout
SideBarLinks()
st.header("Price Trends Analytics")
st.caption("Analyze how item prices shift over time by style, location, and more.")
st.write(f"### Hi, {st.session_state['first_name']}.")

# --- Filter Form ---
st.subheader("Filter Price Trends")

with st.form("price_trends_filters"):
    tag = st.text_input("Item Tag (e.g. mesh top, slip dress)", placeholder="e.g. slip dress")
    location = st.selectbox("Location", ["All", "New York", "Los Angeles", "Chicago", "Online"])
    timeframe = st.selectbox("Timeframe", ["Today", "This Week", "This Month", "Custom Range"])

    custom_range = None
    if timeframe == "Custom Range":
        custom_range = st.date_input("Select Date Range", [date(2025, 1, 1), date(2025, 3, 30)])

    submitted = st.form_submit_button("Apply Filters")

# --- If form submitted, fetch and visualize ---
if submitted:
    if not tag.strip():
        st.warning("Please enter an item tag.")
        st.stop()

    st.subheader("💲 Price Trend Over Time")

    try:
        params = {
            "tag": tag.strip(),
            "location": location if location != "All" else None,
            "timeframe": timeframe.lower().replace(" ", "_")
        }

        if custom_range:
            params["start_date"] = custom_range[0].isoformat()
            params["end_date"] = custom_range[1].isoformat()

        # API call (replace with real endpoint)
        response = requests.get("http://web-api:4000/analytics/price-trends", params=params)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)

        if df.empty:
            st.info("No price trend data available for the selected filters.")
        else:
            fig = px.line(
                df,
                x="date",
                y="average_price",
                markers=True,
                labels={"date": "Date", "average_price": "Avg Price ($)"},
                title=f"Average Price Trend for '{tag.strip()}'"
            )
            fig.update_layout(xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)

    except requests.RequestException as e:
        logger.error(f"Error fetching price trend data: {e}")
        st.error("Failed to fetch price trend data from the API.")
    except ValueError as e:
        logger.error(f"Error parsing price trend data: {e}")
        st.error("Received malformed data from the API.")
