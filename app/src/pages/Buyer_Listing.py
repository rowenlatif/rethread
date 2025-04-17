import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks


SideBarLinks()

st.title("Listings")


listing_id = st.session_state.get('listing', None)

# default listing
if listing_id is None:
    listing_id = st.number_input("Enter a listing ID:", min_value=1, step=1)

## allows shoppers to see listings 
if listing_id:
    url = f"http://localhost:4000/shopper/listing/{listing_id}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if data and len(data) > 0:
                listing_df = pd.DataFrame(data)
                st.subheader("Listing Info")
                st.dataframe(listing_df)

                # lets the shopper see the details of the listing
                st.markdown("### Listing Details")
                for key, value in listing_df.iloc[0].items():
                    st.write(f"**{key.capitalize()}**: {value}")
            else:
                st.warning("Listing not found.")
        else:
            st.error(f"Error fetching listing: Status code {response.status_code}")

    except Exception as e:
        st.error(f"An error occurred: {e}")