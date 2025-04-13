import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## All Platform Reviews')

try:
    # need to update path
    reviews = requests.get('http://api:4000/r/review').json()
except:
    st.error("could not connect to the database to retrieve reviews.")

if reviews:
    sort = st.selectbox("Sort by:", ["Highest to Lowest", "Lowest to Highest"])
    if sort_order == "Highest to Lowest":
        reviews_sorted = sorted(reviews, key=lambda x: x.get('rating', 0), reverse=True)
    else:
        reviews_sorted = sorted(reviews, key=lambda x: x.get('rating', 0))

st.dataframe(reviews_sorted)
else:
    st.write("No reviews found at this time")