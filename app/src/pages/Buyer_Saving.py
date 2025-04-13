import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

logger = logging.getLogger(__name__)

## has the user, listing and saves the item a user wants
user_id = st.session_state.get("user")
listing_id = st.session_state.get("listing")
saved = st.session_state.get("saved", True)


## will save item unless user wants to unsave the item
action = "Save" if saved else "Unsave"

## action that allows the user to either save their item or unsave their item
if st.button(action):
    if user_id and listing_id:
        if st.session_state.saved:
            response = requests.post(f"http://web-api:4000/save/save/{user_id}/{listing_id}")
            if response.status_code == 200:
                st.success("Item saved successfully!")
                st.session_state.saved = True
            else:
                st.error(f"Failed to save item. Server says: {response.text}")
        else:
            response = requests.delete(f"http://web-api:4000/save/unsave/{user_id}/{listing_id}")
            if response.status_code == 200:
                st.success("Item unsaved successfully!")
                st.session_state.saved = False
            else:
                st.error(f"Failed to unsave item. Server says: {response.text}")