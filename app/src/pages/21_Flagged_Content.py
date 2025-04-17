import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## 📬 Flagged Content Inbox')
st.write('### All Flagged Content')

# this gives the admin the option to pick the kind of cotntent that is flagged
content_type = st.selectbox("Filter by content type:", ["all", "messages", "users", "listings"])

try:
    flagged_content = requests.get('http://localhost:4000/admin/flags').json()
except:
    st.error("could not connect to the database to retrieve flagged content.")

if content_type != "all":
    filtered_content = [item for item in flagged_content if item.get("content_type") == content_type]
else:
    filtered_content = flagged_content

if filtered_content:
    st.dataframe(filtered_content)
else:
    st.write("No flagged content found for this filter.")