import logging
logger = logging.getLogger(__name__)
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Listing Analytics')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

api_url = "https://web-api:4000/ListingAnalytics"

# Make GET request to the API
response = requests.get(api_url)

# Check if request was successful
# Parse JSON response into a pandas DataFrame
data = response.json()
graph_data = pd.DataFrame(data)

#steamlit dataframe
st.dataframe(graph_data)

# Show summary statistics
st.subheader("Summary Statistics")
st.write(graph_data.describe())

# Create visualizations
st.subheader("Engagement Metrics")
fig, ax = plt.subplots()
graph_data[['total_views', 'total_saves', 'total_ratings']].mean().plot(kind='bar', ax=ax)
st.pyplot(fig)