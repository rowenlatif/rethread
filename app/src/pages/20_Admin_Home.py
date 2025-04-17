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

if st.button('Flagged Content Inbox',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Flagged_Content.py')

if st.button('View & Create Groups',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/27_Groups.py')

if st.button('View Platform Reviews',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/24_Ratings.py')