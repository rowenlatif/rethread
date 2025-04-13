import logging
import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

logger = logging.getLogger(__name__)

## has the listing information posted on the website or listing is no longer posted
if 'listing' not in st.session_state:
    st.error('This listing is not available or found.')
else:
    listing_id = st.session_state['listing']
    st.title("Listing Information")

    url = f"http://localhost:4000/listing/listing/{listing_id}"
    response = requests.get(url)


    if response.status_code == 200:
        try:
            listing_data = response.json()
            ## created a dataframe for the different aspects a user can see with the listing
            df = pd.DataFrame(listing_data)

            listing_info = df.iloc[0].to_dict() if not df.empty else {}

            tag = listing_info.get('tag' 'N/A')
            information = listing_info.get('information', 'N/A')
            location = listing_info.get('location', 'N/A')

            st.subheader(' Listing:')
            st.write(f'**Tag**: {tag}')
            st.write(f'**Information**: {information}')
            st.write(f'**Location**: {location}')

        ## throws an error is the listing doesn't work
        except requests.exceptions.JSONDecodeError:
            st.error(f"Error. Listing not available: {response.text}")