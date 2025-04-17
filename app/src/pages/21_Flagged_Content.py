import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()
st.title('Flagged Content Admin')

# Filters
content_type = st.selectbox("Filter by:", ["all", "message", "user", "listing", "review"])
status_filter = st.selectbox("Status:", ["all", "in progress", "resolved", "unresolved"])

# Get data
try:
    response = requests.get('http://localhost:4000/admin/flags')
    items = response.json()
except:
    st.error("Database connection error")
    items = []

# Filter items
filtered = []
for item in items:
    type_match = content_type == "all" or item.get("content_type", "") == content_type
    status_match = status_filter == "all" or item.get("status", "in progress") == status_filter
    if type_match and status_match:
        filtered.append(item)

# Status update
col1, col2, col3 = st.columns(3)
with col1:
    flag_id = st.number_input("ID:", min_value=1, step=1)
with col2:
    new_status = st.selectbox("Set status:", ["in progress", "resolved", "unresolved"])
with col3:
    if st.button("Update"):
        try:
            response = requests.put(
                f'http://localhost:4000/admin/flags/{flag_id}',
                json={"status": new_status}
            )
            if response.status_code == 200:
                st.success(f"Updated to '{new_status}'")
            else:
                st.error("Update failed")
        except:
            st.error("Connection error")

# Display items
if filtered:
    for item in filtered:
        status = item.get('status', 'in progress')
        status_icon = "🔄" if status == "in progress" else "✅" if status == "resolved" else "❌"
        
        st.write(f"**ID {item.get('flag_id')}** | {item.get('content_type')} | {status_icon} {status} | {item.get('reason')}")
        st.write("---")
else:
    st.info("No items found")

# Add refresh button
if st.button("Refresh"):
    pass  # Streamlit will naturally rerun