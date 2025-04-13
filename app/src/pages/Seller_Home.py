import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Hi, welcome to reThread, {st.session_state['Samantha']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Listings Analytics',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Listing_Analytics.py')

if st.button('Create Post',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Post_Seller.py')

if st.button('Profile Analytics',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Profile_Analytics.py')