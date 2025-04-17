import logging
import requests
import pandas as pd
import streamlit as st
from datetime import date, datetime
from modules.nav import SideBarLinks
import uuid
import json
import random

logger = logging.getLogger(__name__)
SideBarLinks()

st.header("Reports")
st.caption("Build and view trend reports.")

# --- Create Report Form ---
st.subheader("📄 Create New Report")

with st.expander("Click to build a new trend report"):
    with st.form("create_report_form"):
        title = st.text_input("Report Title", placeholder="e.g. Spring 2025 Trend Forecast")
        summary = st.text_area("Summary / Executive Insight")

        timeframe = st.selectbox("Timeframe", ["This Week", "This Month", "Custom Range"])
        custom_range = None
        if timeframe == "Custom Range":
            custom_range = st.date_input("Select Date Range", [date(2025, 1, 1), date(2025, 3, 30)])

        include_keywords = st.checkbox("Include Keyword Trend Data")
        include_prices = st.checkbox("Include Price Trend Data")
        include_descriptors = st.checkbox("Include Item Descriptors")

        author = st.text_input("Created By (your name)")
        format_choice = st.selectbox("Exported Format", ["PDF", "CSV"])

        submitted = st.form_submit_button("Generate Report")

        if submitted:
            if not all([title, summary, author]):
                st.warning("Please fill in all required fields.")
                st.stop()

            report_id = random.randint(100000, 999999)

            payload = {
                "report_id": report_id,
                "exported_format": format_choice,
                "title": title,
                "summary": summary,
                "filters": json.dumps({
                    "timeframe": timeframe.lower().replace(" ", "_"),
                    "start_date": custom_range[0].isoformat() if custom_range else None,
                    "end_date": custom_range[1].isoformat() if custom_range else None,
                    "include_keywords": include_keywords,
                    "include_prices": include_prices,
                    "include_descriptors": include_descriptors
                }),
                "created_by": author
            }

            try:
                res = requests.post("http://localhost:4000/analyst/trend-reports", json=payload)
                res.raise_for_status()
                st.success("Report created successfully.")
                st.rerun()
            except requests.RequestException as e:
                logger.error(f"Error creating report: {e}")
                st.error("Failed to create report.")

# --- Existing Reports ---
st.subheader("📁 Existing Reports")

try:
    res = requests.get("http://localhost:4000/trend-reports")
    res.raise_for_status()
    reports = res.json()
    df = pd.DataFrame(reports)

    if df.empty:
        st.info("No reports created yet.")
    else:
        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"**{row['title']}**  \n{row['summary']}")
                st.caption(f"Created on {row['created_at']} by {row['created_by']}")

except requests.RequestException as e:
    logger.error(f"Error fetching reports: {e}")
    st.error("No reports yet.")
