import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All in-progress disputes')

all_disputes = requests.get('http://api:4000/d/disputes').json() ## need to update with actual api requests
inprogress_disputes = [d for d in all_disputes if d.get("status", "").lower() != "resolved"]

try:
    if inprogress_disputes:
        st.dataframe(inprogress_disputes)
        st.write('#### Click to expand dispute details')
    for dispute in inprogress_disputes:
        with st.expander(f"Dispute ID: {dispute.get('dispute_id')}"):
            st.write(f"**Status:** {dispute.get('status')}")
            st.write(f"**Seller ID:** {dispute.get('seller_id')}")
            st.write(f"**Buyer ID:** {dispute.get('buyer_id')}")
            st.write(f"**Listing ID:** {dispute.get('listing_id')}")
            st.write(f"**Created At:** {dispute.get('created_at')}")
            st.write(f"**Resolution:** {dispute.get('resolution') or 'N/A'}") 
        # add button to resolve disputes
    else:
        st.write("no in-progress disputes at the time")
except:
    st.write("could not conenct to database to retreive disputes")