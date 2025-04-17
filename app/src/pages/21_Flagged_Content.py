import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import json

st.set_page_config(layout='wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## 📬 Flagged Content Inbox')
st.write('### All Flagged Content')

content_type = st.selectbox("Filter by content type:", ["all", "message", "user", "listing", "review"])

flagged_content = []

try:
    response = requests.get('http://localhost:4000/admin/flags')
    flagged_content = response.json()
except:
    st.error("Could not connect to the database to retrieve flagged content.")

# filter content by type
if flagged_content:
    if content_type != "all":
        filtered_content = []
        for item in flagged_content:
            item_type = item.get("content_type", "")
            if item_type == content_type:
                filtered_content.append(item)
    else:
        filtered_content = flagged_content
else:
    filtered_content = []

if filtered_content:
    st.dataframe(filtered_content)
else:
    st.write("No flagged content found for this filter.")