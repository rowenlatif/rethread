import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome Admin, Ashley.")
st.write('')
st.write('')
st.header('What would you like to do today?')

if st.button('Flagged Content Indox',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Flagged_Content.py')

if st.button('View all verified users',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_In_Prog_Disputes.py')

if st.button('View platform reviews',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/24_Ratings.py')