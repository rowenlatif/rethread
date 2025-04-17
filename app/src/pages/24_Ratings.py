import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

if 'deleted_reviews' not in st.session_state:
    st.session_state.deleted_reviews = []
    
if 'show_success' not in st.session_state:
    st.session_state.show_success = None

def delete_review(review_id):
    try:
        response = requests.delete(f"http://localhost:4000/admin/reviews/{review_id}")
        if response.status_code == 200:
            st.session_state.deleted_reviews.append(review_id)
            st.session_state.show_success = f"Review {review_id} deleted successfully!"
        else:
            st.session_state.show_success = f"Failed to delete review: {response.json().get('message')}"
    except Exception as e:
        logger.error(f"Error deleting review: {e}")
        st.session_state.show_success = f"Error deleting review: {str(e)}"

st.write('\n\n')
st.write('## All Platform Reviews')

if st.session_state.show_success:
    st.success(st.session_state.show_success)
    import time
    time.sleep(0.1)
    st.session_state.show_success = None

try:
    reviews = requests.get('http://localhost:4000/admin/reviews/flagged').json()
except:
    st.error("could not connect to the database to retrieve reviews.")
    reviews = []

if reviews:
    reviews = [r for r in reviews if r.get('review_id') not in st.session_state.deleted_reviews]
    
    sort = st.selectbox("Sort by:", ["Highest to Lowest", "Lowest to Highest"])
    if sort == "Highest to Lowest":
        reviews_sorted = sorted(reviews, key=lambda x: x.get('rating', 0), reverse=True)
    else:
        reviews_sorted = sorted(reviews, key=lambda x: x.get('rating', 0))

    for review in reviews_sorted:
        review_id = review.get('review_id')
        with st.container():
            cols = st.columns([3, 1])
            
            with cols[0]:
                st.write(f"**Review #{review_id}** - Rating: {review.get('rating')}/5")
                st.write(f"Comment: {review.get('comment')}")
                st.write(f"From user {review.get('reviewer_id')} to user {review.get('reviewee_id')}")
                st.write(f"Created at: {review.get('created_at')}")
            
            with cols[1]:
                if st.button("Delete Review", key=f"delete_{review_id}"):
                    delete_review(review_id)
                    st.rerun()
            
            st.markdown("---")
    
    st.write("### Reviews Overview")
    st.dataframe(reviews_sorted)
else:
    st.write("No reviews found at this time")