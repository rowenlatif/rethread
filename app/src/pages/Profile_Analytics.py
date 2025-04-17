import logging
logger = logging.getLogger(__name__)
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from modules.nav import SideBarLinks

SideBarLinks()

st.header('Profile Analytics')

st.write(f"### Hi, {st.session_state['first_name']}.")

seller_id = 5
api_url = f"http://localhost:4000/seller/analytics/{seller_id}"

response = requests.get(api_url)
data = response.json()
graph_data = pd.DataFrame(data)

st.subheader("Seller Performance Overview")


total_views = graph_data['views'].sum()
total_saves = graph_data['saves'].sum()
total_shares = graph_data['shares'].sum()
engagement_rate = (total_saves + total_shares) / total_views * 100 if total_views > 0 else 0
listings_count = len(graph_data)


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Listings", listings_count)
with col2:
    st.metric("Total Views", total_views)
with col3:
    st.metric("Engagement Rate", f"{engagement_rate:.1f}%")
with col4:
    st.metric("Avg Views/Listing", f"{total_views/listings_count:.1f}" if listings_count > 0 else 0)


st.subheader("Performance Trends")

import numpy as np
dates = pd.date_range(end=pd.Timestamp.now(), periods=7, freq='D')
trend_data = pd.DataFrame({
    'date': dates,
    'profile_views': np.random.randint(10, 50, 7),
    'follower_gain': np.random.randint(0, 5, 7)
})
st.line_chart(trend_data.set_index('date'))


st.subheader("Listings Data")
st.dataframe(graph_data)