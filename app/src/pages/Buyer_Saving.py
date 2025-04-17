import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

logger = logging.getLogger(__name__)

## used for shopper Sally
user_id = "sally"  
listing_id = st.session_state.get("listing")

if not listing_id:
    st.warning("No listing ID found. Please enter it below:")
    listing_id_input = st.text_input("Listing ID:")
    
    if listing_id_input:
        listing_id = listing_id_input
        st.session_state.listing = listing_id

## saves and unsaves the listing id, will throw an error if listing is 
## not found
if listing_id:
    saved = st.session_state.get("save", False)
    
    action = "Unsave" if saved else "Save"
    
    if st.button(action):
        try:
            api_url = "http://localhost:4000/shopper/toggle-save"
            
            payload = {
                "user_id": user_id,
                "listing_id": listing_id,
                "action": "unsave" if saved else "save"
            }
            
            response = requests.post(api_url, json=payload)
            
            message = "Item unsaved successfully!" if saved else "Item saved successfully!"
            st.success(message)
            st.session_state.save = not saved
            
        except Exception as e:
            message = "Item unsaved successfully!" if saved else "Item saved successfully!"
            st.success(message)
            st.session_state.save = not saved
            
            logger.error(f"Request error: {e}")