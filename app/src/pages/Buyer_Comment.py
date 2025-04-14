import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

logger = logging.getLogger(__name__)

## has the user, message user can send to seller or review user can make to seller
user_id = st.session_state['user']
message = st.session_state.put("message")
review = st.session_state.put("review")


## allows the user to either send a message or review and then submit said action or review
if message: action = "message"
elif review: action = "review"
else: action = "Submit"

## uses the button to let the user click a button to send a message or send a review
if st.button(action): 
    if user_id:
        if st.session_state.message:
            response = requests.put(f"http://localhost:4000/message/message/{user_id}")
            if response.status_code == 200:
                st.success("Message sent")
            else:
                st.error("Failed to send message.")
            
        elif review:
            response = requests.put(f"http://localhost:4000/message/review/{user_id}")
        if response.status_code == 200:
            st.success("Item unsaved successfully!")
        else:
            st.error("Failed to send review.")