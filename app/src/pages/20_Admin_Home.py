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

if st.button('🚩 Flagged Content Inbox'):
    st.switch_page('pages/21_Flagged_Content')
if st.button('🗂️View all disputes in progress'):
    st.switch_page('pages/22_In_Prog_Disputes')
if st.button('🗂️Notes and resolution history'):
    st.switch_page('pages/23_Res_History')
if st.button('📝 View platform reviews'):
    st.switch_page('pages/24_Ratings')