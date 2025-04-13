import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All Groups')

groups = requests.get('http://api:4000/g/groups').json() ## need to update with actual api requests

try:
    if groups:
        st.dataframe(groups)
    st.write('#### Click to expand listing details')
    or listing in listings:
    with st.expander(f"Group ID: {group.get('group_id')}"):
        st.write(f"**Group Name:** {group.get('name')}")
    st.write(f"**Created By (User ID):** {group.get('created_by')}")
    st.write(f"**Type:** {group.get('type')}")
    else:
    st.write("no groups at the time")
except:
    st.write("could not conenct to database to retrieve groups")