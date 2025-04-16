import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All listings')

listings = requests.get('http://api:4000/listings/all').json()

try:
    if listings:
        st.dataframe(listings)
    else:
        st.write("no listings at the time")
except:
    st.write("could not conenct to database to retrieve listings")