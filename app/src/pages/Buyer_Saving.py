import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Set up navigation
SideBarLinks()

logger = logging.getLogger(__name__)

# Set user for this page
## Used for shopper Kim
user_id = "kim"

st.title("Search Listings by Tag")
st.write("Find items that match your interests")

# Get tag from user input
tag_name = st.text_input("Enter a tag to search for (e.g., vintage, furniture, electronics):")

# Store search results in session state if not already there
if "search_results" not in st.session_state:
    st.session_state.search_results = []

# Function to search listings by tag
def search_listings_by_tag(tag):
    try:
        api_url = f"http://localhost:4000/shopper/listings/search/{tag}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # Limit to only 5 results
            st.session_state.search_results = response.json()[:5]
            return True
        else:
            logger.error(f"Error searching listings: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Request error: {e}")
        return False

if st.button("Submit") and tag_name:
    with st.spinner(f"Searching for listings tagged '{tag_name}'..."):
        success = search_listings_by_tag(tag_name)
        
        if not success:
            st.error("There was an error connecting to the server. Please try again later.")

if st.session_state.search_results:
    st.subheader(f"Found {len(st.session_state.search_results)} listings tagged '{tag_name}'")
    
    for listing in st.session_state.search_results:
        with st.container():
            st.markdown(f"### {listing.get('brand', 'Unknown Brand')}")
            st.markdown("---")

else:
    if tag_name:
        st.info("No results found. Try another tag.")
    else:
        st.info("Enter a tag above and click 'Submit' to find listings.")