import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Listings")

user_id = "sally"

try:
    url = "http://localhost:4000/resources/listing"
    response = requests.get(url)
    
    if response.status_code == 200:
        all_listings = response.json()
        listings_df = pd.DataFrame(all_listings)
    else:
        st.error(f"Error fetching listings: Status code {response.status_code}")
        listings_df = pd.DataFrame()
except Exception as e:
    st.error(f"An error occurred: {e}")
    listings_df = pd.DataFrame()

if 'saved_listings' not in st.session_state:
    st.session_state.saved_listings = []

if not listings_df.empty:
    st.subheader(f"Available Listings ({len(listings_df)} items)")

    for index, row in listings_df.iterrows():
        listing_id = row['listing_id']
        is_saved = listing_id in st.session_state.saved_listings

        with st.expander(f"{row['title']} - ${row['price']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                for key, value in row.items():
                    if key not in ["listing_id", "title", "price"]:
                        st.write(f"**{key.capitalize()}**: {value}")
            
            with col2:
                action = "Unsave" if is_saved else "Save"
                if st.button(action, key=f"save_{listing_id}"):
                    try:
                        api_url = "http://localhost:4000/shopper/toggle-save"
                        payload = {
                            "user_id": user_id,
                            "listing_id": listing_id,
                            "action": "unsave" if is_saved else "save"
                        }
                        toggle_response = requests.post(api_url, json=payload)

                        if is_saved:
                            st.session_state.saved_listings.remove(listing_id)
                        else:
                            st.session_state.saved_listings.append(listing_id)
                        
                        message = "Item unsaved successfully!" if is_saved else "Item saved successfully!"
                        st.success(message)
                    except Exception as e:
                        st.error(f"API Error: {e}. Updating local state only.")

                        if is_saved:
                            st.session_state.saved_listings.remove(listing_id)
                        else:
                            st.session_state.saved_listings.append(listing_id)
                        
                    st.rerun()
else:
    st.info("No listings found.")

st.markdown("---")
st.subheader("Your Saved Listings")

if st.session_state.saved_listings and not listings_df.empty:
    saved_df = listings_df[listings_df["listing_id"].isin(st.session_state.saved_listings)]
    if not saved_df.empty:
        st.dataframe(saved_df[["listing_id", "title", "price"]])
    else:
        st.info("You haven't saved any listings yet.")
else:
    st.info("You haven't saved any listings yet.")