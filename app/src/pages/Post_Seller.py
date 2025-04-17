import streamlit as st
import requests
import datetime
import random
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.header('Create New Listing')
api_url = "http://localhost:4000/seller/listings"


category_map = {
    "Tops": 1,
    "Bottoms": 2,
    "Dresses": 3,
    "Outerwear": 4,
    "Accessories": 5
}

with st.form("new_listing_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price ($)", min_value=0.0, step=0.01)

    col1, col2 = st.columns(2)
    with col1:
        color = st.text_input("Color")
        material = st.text_input("Material")
        brand = st.text_input("Brand")

    with col2:
        condition = st.selectbox("Condition",
                                 ["New with tags", "Like new", "Good", "Fair", "Poor"])
    size = st.selectbox("Size",
                        ["XS", "S", "M", "L", "XL", "XXL", "Other"])
    category = st.selectbox("Category",
                            ["Tops", "Bottoms", "Dresses", "Outerwear", "Accessories"])


    seller_id = st.session_state.get('user_id', 1)


    submit_button = st.form_submit_button("Create Listing")


if submit_button:

    timestamp = datetime.datetime.now().isoformat()

    listing_id = random.randint(1000, 9999)

    group_id = category_map[category]


    listing_data = {
        "listing_id": listing_id,
        "title": title,
        "description": description,
        "price": price,
        "color": color,
        "material": material,
        "brand": brand,
        "condition": condition,
        "size": size,
        "group_id": group_id,
        "seller_id": seller_id,
        "timestamp": timestamp
    }

    try:
        response = requests.post(api_url, json=listing_data)


        if response.status_code == 201:
            st.markdown("### 🎉 Listing Created Successfully! 👕 👗 👖 👢") #clothes for the theme

        else:
            st.error(f"Failed to create listing: {response.status_code}")
            st.error(response.text)

    except Exception as e:
        st.error(f"Error connecting to API: {e}")