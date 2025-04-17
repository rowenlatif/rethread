##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('CS 3200 reThread Project')
st.write('\n\n')
st.write('### Hi! As which user would you like to log in?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Samatha, reThread Seller", 
        type = 'primary', 
        use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'Seller' 
        st.session_state['first_name'] = 'Samantha'
        logger.info("Logging in Samantha")
        st.switch_page('pages/Seller_Home.py')


if st.button('Act as Sally, reThread Shopper', 
        type = 'primary', 
        use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'Shopper'
        st.session_state['first_name'] = 'Sally'
        st.switch_page('pages/Buyer_Home.py')

if st.button('Act as Ashley, reThread App Administrator', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Ashley'
    st.switch_page('pages/20_Admin_Home.py')

if st.button('Act as Fark, reThread Trend Analyst',
             type = 'primary',
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'trend_analyst'
    st.session_state['first_name'] = 'Fark'
    st.switch_page('pages/Trend_Analyst_Home.py')