import logging
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
SideBarLinks()

st.header("Price Trends")
st.caption("Analyze how item prices shift over time by listing.")

st.subheader("View Price Trend")
with st.form("price_trend_form"):
    listing_id = st.text_input("Listing ID", placeholder="e.g. 1")
    submitted = st.form_submit_button("View Trend")

if submitted:
    if not listing_id.strip().isdigit():
        st.warning("Please enter a valid numeric Listing ID.")
        st.stop()

    try:
        response = requests.get(
            f"http://localhost:4000/analyst/price-history/{listing_id.strip()}"
        )
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        if df.empty:
            st.info("No price trend data available for this listing.")
        else:
            df["date"] = pd.to_datetime(df["date"])
            fig = px.line(
                df,
                x="date",
                y="average_price",
                markers=True,
                labels={"date": "Date", "average_price": "Avg Price ($)"},
                title=f"Price Trend for Listing ID {listing_id.strip()}"
            )
            fig.update_layout(xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)

    except requests.RequestException as e:
        logger.error(f"API error: {e}")
        st.error("Failed to fetch price trend data.")