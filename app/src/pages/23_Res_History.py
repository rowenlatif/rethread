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

all_disputes = requests.get('http://localhost:4000/admin/messages').json() ## need to update with actual api requests
resolved_disputes = [d for d in all_disputes if d.get("status", "").lower() == "resolved"]

try:
    if resolved_disputes:
        st.dataframe(resolved_disputes)
    else:
        st.write("no resolved disputes at the time")
except:
    st.write("could not conenct to database to retreive disputes")