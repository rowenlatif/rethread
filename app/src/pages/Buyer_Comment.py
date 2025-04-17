import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

logger = logging.getLogger(__name__)

st.session_state['user'] = "sally"

# Get the current values from session state
user_id = st.session_state['user']

# Create input fields for message and review
message = st.text_area("Message to seller", key="message_input")
review = st.text_area("Review for seller", key="review_input")

# Update session state based on input
st.session_state['message'] = message
st.session_state['review'] = review

# Determine which action to perform
if message:
    action = "Send Message"
elif review:
    action = "Submit Review"
else:
    action = "Submit"

# Create a button with the appropriate action text
if st.button(action):
    if user_id:
        if st.session_state['message']:
            response = requests.put(f"http://localhost:4000/message/message/{user_id}")
            if response.status_code == 200:
                st.success("Message sent")
            else:
                st.error("Failed to send message.")
        
        elif st.session_state['review']:
            response = requests.put(f"http://localhost:4000/message/review/{user_id}")
            if response.status_code == 200:
                st.success("Review submitted successfully!")
            else:
                st.error("Failed to send review.")
    else:
        st.error("User not logged in. Please log in to continue.")