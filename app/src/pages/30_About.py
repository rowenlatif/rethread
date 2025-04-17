import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is a demo app for CS 3200 Course Project.  

    The goal of this demo is to provide information on the tech stack 
    being used as well as demo some of the features of the various platforms. 

    Our project is a new app called reThread. reThread is an app used for clothing.
    reThread allows for different types of users.

    One of the users are the shopper. These users are able to access the app to
    find the perfect clothes for them. They are able to find specific brands, location,
    style and so much more! They are able to message the people who posted the clothing
    and allows for them to write reviews about the seller.

    Another one of the users are the sellers. These users are allowed to use the app to
    post their clothes. They can interact with the shoppers by messaging them and giving
    them reviews.

    There are admins who help run the app in case an issue occurs. They can flag innapropriate
    content, verify a users account and monitor the messages to prevent hatefulness.

    There are also trend analysts that analyze what a shopper is interested in and gives clothes
    tailered to their interests. 

    Stay tuned for more information and features to come!
    """
        )