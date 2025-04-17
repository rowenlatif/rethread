import streamlit as st
import requests
import datetime


st.header('Create New Listing')
api_url = "http://localhost:4000/seller/listings"

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
    group_id = st.selectbox("Category",
    ["Tops", "Bottoms", "Dresses", "Outerwear", "Accessories"])


    # Default to 1 if not logged in
    seller_id = st.session_state.get('user_id', 1)

    # Submit button
    submit_button = st.form_submit_button("Create Listing")

# Handle form submission
if submit_button:
    # Create timestamp
    timestamp = datetime.datetime.now().isoformat()

    # Prepare data for API
    listing_data = {
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

    # Send data to API
    try:
        response = requests.post(api_url, json=listing_data)

    # Created
        if response.status_code == 201:
            st.success("Listing created successfully!")
        # Celebrate with some balloons!
            st.balloons()
        else:
            st.error(f"Failed to create listing: {response.status_code}")
            st.error(response.text)
        
    except Exception as e:
        st.error(f"Error connecting to API: {e}")