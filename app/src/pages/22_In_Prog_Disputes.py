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

all_disputes = requests.get('http://api:4000/d/disputes').json() ## need to update with actual api requests
inprogress_disputes = [d for d in all_disputes if d.get("status", "").lower() != "resolved"]

# add a button to resolve disputes

try:
    st.dataframe(inprogress_disputes)
except:
    st.write("could not conenct to database to retreive disputes")