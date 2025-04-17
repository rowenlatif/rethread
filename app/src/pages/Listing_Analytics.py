import logging
logger = logging.getLogger(__name__)
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from modules.nav import SideBarLinks

SideBarLinks()

st.header('Listing Analytics')

st.write(f"### Hi, Samantha.")

seller_id = 5
api_url = f"http://localhost:4000/seller/analytics/{seller_id}"

response = requests.get(api_url)
data = response.json()
graph_data = pd.DataFrame(data)


selected_listing = st.selectbox("Select a Listing to Analyze", graph_data['title'].tolist())
filtered_data = graph_data[graph_data['title'] == selected_listing]


st.subheader(f"Analytics for: {selected_listing}")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Views", filtered_data['views'].values[0])
with col2:
    st.metric("Saves", filtered_data['saves'].values[0])
with col3:
    st.metric("Shares", filtered_data['shares'].values[0])


st.subheader("How this listing compares to others")
fig, ax = plt.subplots(figsize=(10, 5))

sorted_data = graph_data.sort_values('views', ascending=False)

colors = ['red' if title != selected_listing else 'blue' for title in sorted_data['title']]
sns.barplot(x='title', y='views', data=sorted_data, palette=colors, ax=ax)
plt.xticks(rotation=45, ha='right')
plt.title('Views Comparison Across Listings')
st.pyplot(fig)


st.subheader("Engagement Analysis")
graph_data['save_rate'] = graph_data['saves'] / graph_data['views'] * 100
graph_data['share_rate'] = graph_data['shares'] / graph_data['views'] * 100

fig2, ax2 = plt.subplots(figsize=(10, 5))
metrics_data = pd.melt(graph_data,
                      id_vars=['title'],
                      value_vars=['save_rate', 'share_rate'],
                      var_name='Metric',
                      value_name='Percentage')
sns.barplot(x='title', y='Percentage', hue='Metric', data=metrics_data, ax=ax2)
plt.xticks(rotation=45, ha='right')
plt.title('Save and Share Rates by Listing')
st.pyplot(fig2)

st.subheader("All Listings Data")
st.dataframe(graph_data)