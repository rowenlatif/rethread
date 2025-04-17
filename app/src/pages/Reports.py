import logging
import requests
import pandas as pd
import streamlit as st
from datetime import date, datetime
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
SideBarLinks()

st.header("Reports")
st.caption("Build, view, and export trend reports.")

st.write(f"### Hi, {st.session_state['first_name']}.")

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

        submitted = st.form_submit_button("Generate Report")

        if submitted:
            payload = {
                "title": title,
                "summary": summary,
                "created_by": st.session_state["user_id"],
                "filters": {
                    "timeframe": timeframe.lower().replace(" ", "_"),
                    "start_date": custom_range[0].isoformat() if custom_range else None,
                    "end_date": custom_range[1].isoformat() if custom_range else None,
                    "include_keywords": include_keywords,
                    "include_prices": include_prices,
                    "include_descriptors": include_descriptors
                }
            }

            try:
                response = requests.post("http://web-api:4000/trendreport", json=payload)
                response.raise_for_status()
                st.success("Report created successfully!")
                st.rerun()
            except requests.RequestException as e:
                logger.error(f"Error creating report: {e}")
                st.error("Failed to create report.")


# --- List of Reports ---
st.subheader("📁 Existing Reports")

try:
    reports_response = requests.get("http://web-api:4000/trendreport")
    reports_response.raise_for_status()
    reports_data = reports_response.json()
    df = pd.DataFrame(reports_data)

    if df.empty:
        st.info("No reports found.")
    else:
        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"**{row['title']}**  \n{row['summary']}")
                st.caption(f"Created {row['created_at']} • Report ID: {row['report_id']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("View", key=f"view_{row['report_id']}"):
                        st.info("Viewing is not implemented yet.")
                with col2:
                    if st.button("Edit", key=f"edit_{row['report_id']}"):
                        st.warning("Edit flow not yet supported.")
                with col3:
                    export_format = st.selectbox("Export Format", ["PDF", "CSV"], key=f"export_format_{row['report_id']}")
                    if st.button("Export", key=f"export_{row['report_id']}"):
                        try:
                            export_url = f"http://web-api:4000/trendreport/{row['report_id']}/export?format={export_format.lower()}"
                            export_resp = requests.get(export_url)
                            export_resp.raise_for_status()

                            st.download_button(
                                label=f"Download {export_format}",
                                data=export_resp.content,
                                file_name=f"{row['title'].replace(' ', '_')}.{export_format.lower()}",
                                mime="application/octet-stream"
                            )
                        except requests.RequestException:
                            st.error("Export failed.")

except requests.RequestException as e:
    logger.error(f"Error fetching reports: {e}")
    st.error("Failed to fetch reports from the API.")