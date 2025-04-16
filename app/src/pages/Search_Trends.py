import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from datetime import datetime, date
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header and caption of the page
st.header('Search Trends Analytics')
st.caption("Analyze search query data by keyword, location, time, and/or style group")
st.write(f"### Hi, {st.session_state['first_name']}.")

# --- Filter Form ---
st.subheader("Filter Search Trends")

with st.form("filters_form"):
    term_1 = st.text_input("Search Term 1", placeholder="e.g. mesh top")
    term_2 = st.text_input("Search Term 2 (optional)", "")
    term_3 = st.text_input("Search Term 3 (optional)", "")

    location = st.selectbox("Location", ["All", "New York", "Los Angeles", "Chicago", "Online"])
    group = st.selectbox("Aesthetic Group", ["All", "Clean Girl", "Coquette", "Grunge Revival", "Y2K", "Office Siren"])
    timeframe = st.selectbox("Timeframe", ["Today", "This Week", "This Month", "Custom Range"])

    custom_range = None
    if timeframe == "Custom Range":
        custom_range = st.date_input("Select Date Range", [date(2025, 1, 1), date(2025, 3, 30)])

    submitted = st.form_submit_button("Apply Filters")

# --- If form submitted, fetch and visualize ---
if submitted:
    search_terms = [term.strip() for term in [term_1, term_2, term_3] if term.strip()]
    if not search_terms:
        st.warning("Please enter at least one search term.")
        st.stop()

    st.subheader("📈 Keyword Trend Graph")

    try:
        params = {
            "terms": search_terms,
            "location": location if location != "All" else None,
            "group": group if group != "All" else None,
            "timeframe": timeframe.lower().replace(" ", "_")
        }

        if custom_range:
            params["start_date"] = custom_range[0].isoformat()
            params["end_date"] = custom_range[1].isoformat()

        # API call (replace with real endpoint)
        response = requests.get("http://web-api:4000//analytics/search-trends", params=params)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)

        if df.empty:
            st.info("No trend data available for the selected filters.")
        else:
            fig = px.line(
                df,
                x="date",
                y="search_volume",
                color="term",
                markers=True,
                labels={"date": "Date", "search_volume": "Search Volume", "term": "Search Term"},
                title="Search Volume Over Time"
            )
            fig.update_layout(legend_title_text="Search Terms", xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)

    except requests.RequestException as e:
        logger.error(f"Error fetching trend data: {e}")
        st.error("Failed to fetch trend data from the API.")
    except ValueError as e:
        logger.error(f"Error parsing trend data: {e}")
        st.error("Received malformed data from the API.")