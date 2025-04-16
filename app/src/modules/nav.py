# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Shopper ------------------------
def ShopperNav():
    st.sidebar.page_link(
        "pages/Buyer_Home.py", label = "Buyer Home", icon = "🛍️"
    )
    st.sidebar.page_link(
        "pages/comment.py", label = "Users Comments", icon = "💬"
    )
    st.sidebar.page_link(
        "pages/listing.py", label = "Listings", icon = "📄"
    )
    st.sidebar.page_link(
    "pages/saving.py", label = "Savings", icon = "⏳"
    )


#### ------------------------ Trend Analyst ------------------------
def TrendAnalystNav():
    st.sidebar.page_link(
        "pages/Trend_Analyst_Home.py", label="Analyst Home", icon="📈"
    )
    st.sidebar.page_link(
        "pages/Search_Trends.py", label="Search Trends", icon="🔍"
    )
    st.sidebar.page_link(
        "pages/Price_Trends.py", label="Price Trends", icon="💲"
    )
    st.sidebar.page_link(
        "pages/Reports.py", label="Reports", icon="📄"
    )



# ------------------------ Admin ------------------------
def AdminNav():
    st.sidebar.page_link(
        "pages/20_Admin_Home.py", label="Admin Home", icon="🛠️"
    )
    st.sidebar.page_link(
        "pages/25_Users.py", label="Users", icon="🧍"
    )
    st.sidebar.page_link(
        "pages/26_Listings.py", label="Listings", icon="🏷️"
    )
    st.sidebar.page_link(
        "pages/27_Groups.py", label="Groups", icon="👥"
    )
    st.sidebar.page_link(
        "pages/21_Flagged_Content.py", label="Reports", icon="📄"
    )

## ------------------------ Seller ------------------------
def SellerNav():
    st.sidebar.page_link(
        "pages/Seller_Home.py", label="Analyst Home", icon="📈"
    )
    st.sidebar.page_link(
        "pages/Post_Seller.py", label="Postings", icon="🔍"
    )
    st.sidebar.page_link(
        "pages/Listing_Analytics.py", label="Listing Analytics", icon="💲"
    )
    st.sidebar.page_link(
        "pages/Profile_Analytics.py", label="Profile Analytics", icon="📄"
    )

def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """
    
    # Add a logo to the sidebar always
    st.sidebar.image("app/src/assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    
    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        if st.session_state["role"] == "shopper":
            ShopperNav()
        elif st.session_state["role"] == "seller":
            SellerNav()
        elif st.session_state["role"] == "administrator":
            AdminNav()
        elif st.session_state["role"] == "trend_analyst":
            TrendAnalystNav()
    
    # Always show the About page at the bottom of the list of links
    # AboutPageNav()
       
    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")