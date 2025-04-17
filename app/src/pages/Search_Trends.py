import logging
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, date, timedelta
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)
SideBarLinks()

st.header('Search Trends')
st.caption("Analyze search query data by keyword, demographic, and time period")

sample_keywords = ["vintage jeans", "lululemon", "y2k top", "nike shoes", "prada bag", 
                  "brandy melville", "urban outfitters", "zara blazer", "shein top", "adidas campus"]
age_groups = ["All Ages", "18-24", "25-30", "31-35"]
genders = ["All Genders", "male", "female", "nonbinary"]
locations = ["All Locations", "New York City", "Los Angeles", "Chicago", "Boston", "Miami"]
time_periods = ["Last 7 Days", "Last 30 Days", "Last 3 Months", "Custom Range"]

st.subheader("Filter Search Trends")

with st.form("search_trends_form"):
    keyword = st.selectbox("Search Keyword", ["All Keywords"] + sample_keywords)
    
    col1, col2 = st.columns(2)
    with col1:
        age_group = st.selectbox("Age Group", age_groups)
        gender = st.selectbox("Gender", genders)
    
    with col2:
        location = st.selectbox("Location", locations)
        time_period = st.selectbox("Time Period", time_periods)
    
    custom_range = None
    if time_period == "Custom Range":
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        custom_range = st.date_input("Select Date Range", [start_date, end_date])
    
    submitted = st.form_submit_button("Apply Filters")

if submitted:
    try:
        st.info(f"Showing search trends for: Keyword='{keyword}', Age='{age_group}', Gender='{gender}', Location='{location}', Time='{time_period}'")
        
        demo_response = requests.get("http://localhost:4000/analyst/search-trends")
        demo_response.raise_for_status()
        demo_data = demo_response.json()
        
        if not demo_data:
            st.info("No demographic trend data available.")
        else:
            df = pd.DataFrame(demo_data)
            st.subheader("👥 Search Activity Demographics")
            

            if 'search_month' in df.columns:
                df['month_name'] = pd.to_numeric(df['search_month']).apply(
                    lambda x: datetime(2025, int(x), 1).strftime('%B')
                )
            

            if 'gender' in df.columns and 'search_count' in df.columns:
                fig1 = px.bar(
                    df,
                    x='month_name' if 'month_name' in df.columns else 'search_month',
                    y='search_count',
                    color='gender',
                    barmode='group',
                    labels={
                        'month_name': 'Month',
                        'search_month': 'Month',
                        'search_count': 'Search Count',
                        'gender': 'Gender'
                    },
                    title=f"Search Activity by Gender {'for '+keyword if keyword != 'All Keywords' else ''}"
                )
                fig1.update_layout(xaxis_title=None, yaxis_title=None)
                st.plotly_chart(fig1, use_container_width=True)

            if 'age' in df.columns and 'search_count' in df.columns:
                fig2 = px.bar(
                    df,
                    x='month_name' if 'month_name' in df.columns else 'search_month',
                    y='search_count',
                    color='age',
                    barmode='group',
                    labels={
                        'month_name': 'Month',
                        'search_month': 'Month', 
                        'search_count': 'Search Count',
                        'age': 'Age Group'
                    },
                    title=f"Search Activity by Age Group {'for '+keyword if keyword != 'All Keywords' else ''}"
                )
                fig2.update_layout(xaxis_title=None, yaxis_title=None)
                st.plotly_chart(fig2, use_container_width=True)

            if 'location_id' in df.columns and 'search_count' in df.columns:
                fig3 = px.bar(
                    df,
                    x='month_name' if 'month_name' in df.columns else 'search_month',
                    y='search_count',
                    color='location_id',
                    barmode='group',
                    labels={
                        'month_name': 'Month',
                        'search_month': 'Month',
                        'search_count': 'Search Count',
                        'location_id': 'Location ID'
                    },
                    title=f"Search Activity by Location {'for '+keyword if keyword != 'All Keywords' else ''}"
                )
                fig3.update_layout(xaxis_title=None, yaxis_title=None)
                st.plotly_chart(fig3, use_container_width=True)

    except requests.RequestException as e:
        logger.error(f"API error: {e}")
        st.error("Failed to fetch search trend data.")
    except ValueError as e:
        logger.error(f"Data parsing error: {e}")
        st.error("Received malformed data from the API.")