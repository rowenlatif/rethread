import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## Create New Group')

post_group = requests.post('http://api:4000/groups').json() 

with st.form("Create a new group"):
    group_id = st.text_input("Input New Groups ID")
    group_name = st.text_input("Input New Groups Name")
    group_type = st.text_input("Input New Groups Type")
    group_creator = st.text_input("Input New Group Creator")

    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {}
        data['group_id'] = group_id
        data['name'] = group_name
        data['type'] = group_type
        data['created_by'] = group_creator
        st.write(data)

        requests.post('http://api:4000/groups', json=data)

st.write('\n\n')
st.write('## All Groups')

groups = requests.get('http://api:4000/groups/all').json() 

try:
    if groups:
        st.dataframe(groups)
    else:
        st.write("no groups at the time")
except:
    st.write("could not conenct to database to retrieve groups")