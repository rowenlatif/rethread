import logging

logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All listings')

try:
    # Use the correct URL with /admin prefix
    response = requests.get('http://localhost:4000/admin/listings/all')

    # Display response details for debugging
    st.write(f"Status code: {response.status_code}")

    # Try to parse as JSON
    listings = response.json()

    # Display listings if available
    if listings:
        st.dataframe(listings)
    else:
        st.write("No listings found at this time")
except requests.exceptions.RequestException as e:
    st.error(f"Connection error: {e}")
except ValueError as e:  # JSON decode error
    st.error(f"Error parsing response: {e}")
    st.write(f"Response content: {response.text[:200]}...")  # Show first 200 chars
except Exception as e:
    st.error(f"Unexpected error: {e}")