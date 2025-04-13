import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome Admin, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.header('### What would you like to do today?')

big_col1, big_col2, big_col3 = st.columns(3)
    
with big_col1:
    if st.button('🚩 Flagged Content Inbox',
                type='primary',
                user_container_width=True):
        st.switch_page('pages/21_Flagged_Content')
    
with big_col2:
    st.header("🗂️ Open Cases & Disputes")

    cases_col1, cases_col2 = st.columns(2)
    with cases_col1:
        if st.button('View all disputes in progress',
                type='primary',
                user_container_width=True):
            st.switch_page('pages/22_In_Prog_Disputes')
    with cases_col2:
        if st.button('Notes and resolution history',
                type='primary',
                user_container_width=True):
            st.switch_page('pages/23_Res_History')

with big_col3:
     if st.button('📝 View platform reviews',
            type='primary',
            user_container_width=True):
        st.switch_page('pages/24_Ratings')