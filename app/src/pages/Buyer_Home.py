import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Hi, welcome to reThread, {st.session_state['name']}.")
st.write('')
st.write('')
st.write('### What would you purchase today?')

if st.button('Listings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/listing.py')

if st.button('Saving', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/saving.py')

if st.button('Comments', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/comment.py')