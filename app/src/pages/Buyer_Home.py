import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Hi, welcome to reThread, Sally.")
st.write('')
st.write('')
st.write('### What would you purchase today?')

if st.button('Listings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Buyer_Listing.py')

if st.button('Saving', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Buyer_Saving.py')

if st.button('Comments', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Buyer_Comment.py')