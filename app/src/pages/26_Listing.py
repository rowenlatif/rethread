import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All in-progress listings')

listings = requests.get('http://api:4000/l/listings').json() ## need to update with actual api requests

try:
    if listings:
        st.dataframe(listings)
    st.write('#### Click to expand listing details')
    for listing in listings:
        with st.expander(f"Listing ID: {listing.get('listing_id')}"):
            st.write(f"**Title:** {listing.get('title')}")
    st.write(f"**Description:** {listing.get('description')}")
    st.write(f"**Price:** ${listing.get('price')}")
    st.write(f"**Condition:** {listing.get('condition')}")
    st.write(f"**Brand:** {listing.get('brand')}")
    st.write(f"**Size:** {listing.get('size')}")
    st.write(f"**Material:** {listing.get('material')}")
    st.write(f"**Color:** {listing.get('color')}")
    st.write(f"**Timestamp:** {listing.get('timestamp')}")
    st.write(f"**Seller ID:** {listing.get('seller_id')}")
    st.write(f"**Group ID:** {listing.get('group_id')}")
    else:
    st.write("no listings at the time")
except:
    st.write("could not conenct to database to retrieve listings")