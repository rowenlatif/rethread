import logging
import requests
import json
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
SideBarLinks()

if "report_created" not in st.session_state:
    st.session_state.report_created = False

st.header("Reports")
st.caption("Build and view trend reports.")

# --- Create Report Form ---
st.subheader("📄 Create New Report")

timeframe_options = {
    "This Week": "this_week",
    "This Month": "this_month", 
    "Last Quarter": "last_quarter",
    "Custom Range": "custom_range"
}

with st.form("create_report_form"):
    report_id = st.number_input("Report ID", min_value=1, max_value=9999, value=101)
    created_by = st.number_input("Created By (Analyst ID)", min_value=1, max_value=40, value=9)
    
    timeframe_display = st.selectbox(
        "Timeframe",
        options=list(timeframe_options.keys())
    )
    
    title = st.text_input("Report Title", placeholder="e.g. Spring 2025 Trend Forecast")
    summary = st.text_area("Summary / Executive Insight")
    exported_format = st.selectbox("Format", ["pdf", "csv"])
    
    timeframe_value = timeframe_options[timeframe_display]
    
    filters_json = json.dumps({"timeframe": timeframe_value})

    submitted = st.form_submit_button("Generate Report")

if st.session_state.report_created:
    st.success("Report created successfully!")
    st.session_state.report_created = False

if submitted:
    if not title or not summary:
        st.warning("Please fill in all required fields.")
        st.stop()

    payload = {
        "report_id": int(report_id),
        "exported_format": exported_format,
        "title": title,
        "summary": summary,
        "filters": filters_json,
        "created_by": int(created_by)
    }
    
    try:
        response = requests.post("http://localhost:4000/analyst/trend-reports", json=payload)
        
        if response.status_code == 201:
            st.session_state.report_created = True
            st.rerun()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error creating report: {e}")
        st.error(f"Failed to create report: {str(e)}")

# --- View Existing Reports ---
st.subheader("📁 Existing Reports")

try:
    response = requests.get("http://localhost:4000/analyst/trend-reports")
    
    if response.status_code == 200:
        reports = response.json()
        
        if not reports:
            st.info("No reports available.")
        else:
            for report in reports:
                with st.container():
                    st.markdown(f"### {report.get('title', 'Untitled Report')}")
                    st.markdown(f"{report.get('summary', 'No summary provided')}")
                    
                    created_at = report.get('created_at', '')
                    if created_at and isinstance(created_at, str):
                        if 'T' in created_at:
                            created_at = created_at.split('T')[0]
                    
                    analyst_names = {
                        9: "Ashley Dyer",
                        16: "Tammy Sellers",
                        21: "Kim Martinez",
                        24: "Nicole Vaughn",
                        31: "John Ryan",
                        40: "Robert Chase"
                    }
                    
                    created_by = report.get('created_by', '')
                    analyst_name = analyst_names.get(created_by, f"Analyst #{created_by}")
                    
                    st.caption(f"Report #{report.get('report_id', 'N/A')} | Created on {created_at} by {analyst_name}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"Format: {report.get('exported_format', 'PDF').upper()}")
                    
                    with col2:
                        if 'filters' in report and report['filters']:
                            try:
                                filters_data = report['filters']
                                if isinstance(filters_data, str):
                                    filters_data = json.loads(filters_data)
                                timeframe_value = filters_data.get('timeframe', '')
                                
                                timeframe_display = timeframe_value.replace('_', ' ').title()
                                for display, value in timeframe_options.items():
                                    if value == timeframe_value:
                                        timeframe_display = display
                                        break
                                        
                                if timeframe_value:
                                    st.caption(f"Timeframe: {timeframe_display}")
                            except:
                                pass
                    
                    st.markdown("---")
    else:
        st.error(f"Error fetching reports: {response.status_code}")
                
except Exception as e:
    logger.error(f"Error fetching reports: {e}")
    st.error(f"Failed to fetch reports: {str(e)}")