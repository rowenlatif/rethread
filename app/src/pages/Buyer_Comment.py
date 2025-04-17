import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

logger = logging.getLogger(__name__)

SideBarLinks()

st.session_state['user'] = "sally"
user_id = st.session_state['user']

st.title("Marketplace Communications")

# Message section
st.subheader("Message to Seller")
message = st.text_area("Message to seller", key="message_input")

# Send button
if st.button("Send Message"):
    if message:
        # Simplified data with fixed values
        data = {
            "message_id": "msg123",
            "sender_id": user_id,
            "recipient_id": "user456",
            "listing_id": "1",
            "content": message
        }
        
        try:
            response = requests.post("http://localhost:4000/shopper/message", json=data)
            if response.status_code == 200:
                st.success("Message sent!")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
    else:
        st.warning("Please enter a message")


