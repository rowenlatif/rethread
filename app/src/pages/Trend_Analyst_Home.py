import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Trend Analyst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Search Trends', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Search_Trends.py')

if st.button('View Price Trends', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Price_Trends.py')

if st.button('View Reports', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Reports.py')