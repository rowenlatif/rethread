# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Shopper ------------------------
# def ShopperNav():


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


## ------------------------ Seller ------------------------
# def SellerNav():


# ------------------------ Admin ------------------------
# def AdminNav():






def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """
    
    # Add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    
    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        if role == "shopper":
            ShopperNav()
        elif role == "seller":
            SellerNav()
        elif role == "administrator":
            AdminNav()
        elif role == "trend_analyst":
            TrendAnalystNav()
    
    # Always show the About page at the bottom of the list of links
    # AboutPageNav()
       
        if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
            if st.sidebar.button("Logout"):
                del st.session_state["role"]
                del st.session_state["authenticated"]
                st.switch_page("Home.py")