import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All user verifications')

verifications = requests.get('http://api:4000/verifications').json()

try:
    if verifications:
        st.dataframe(verifications)
    else:
        st.write("no verifications at the time")
except:
    st.write("could not conenct to database to retreive verifications")