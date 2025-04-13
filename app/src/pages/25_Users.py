import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All in-progress disputes')

users = requests.get('http://api:4000/u/users').json() ## need to update with actual api requests

try:
    if users:
        st.dataframe(users)
    st.write('#### Click to expand user details')
    for user in users:
        with st.expander(f"User ID: {user.get('user_id')}"):
            st.write(f"**Name:** {user.get('name')}")
    st.write(f"**Role:** {user.get('role')}")
    st.write(f"**Location ID:** {user.get('location_id')}")
    st.write(f"**Demographic ID:** {user.get('demographic_id')}")
    else:
    st.write("no users at the time")
except:
    st.write("could not conenct to database to retreive users")