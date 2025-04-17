import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title('App Administration Page')

st.write('\n\n')
st.write('## Create New Group')

with st.form("create_group_form"):
    group_id = st.text_input("Group ID")
    group_name = st.text_input("Group Name")
    group_type = st.selectbox("Group Type", ["community", "school", "business", "organization"])
    group_creator = st.text_input("Creator ID")

    submitted = st.form_submit_button("Create Group")

    if submitted:
        if not group_id or not group_name or not group_creator:
            st.error("Please fill in all fields")
        else:
            data = {
                'group_id': group_id,
                'name': group_name,
                'type': group_type,
                'created_by': group_creator
            }
            
            try:
                response = requests.post('http://localhost:4000/admin/groups', json=data)
                if response.status_code == 201:
                    st.success(f"Group '{group_name}' created successfully!")
                else:
                    st.error("Failed to create group")
            except:
                st.error("Error connecting to server")




st.write('\n\n')
st.write('## All Groups')

try:
    response = requests.get('http://localhost:4000/admin/groups/all')
    groups = response.json()
    
    if groups:
        st.dataframe(groups)
        st.write(f"Total number of groups: {len(groups)}")
    else:
        st.info("No groups found")
except:
    st.error("Could not connect to database to retrieve groups")



st.write("## Update Existing Group")

try:
    response = requests.get('http://localhost:4000/admin/groups/all')
    response.raise_for_status()
    groups = response.json()

    if groups:
        group_options = {f"{g['group_id']} - {g['name']}": g for g in groups}
        selected_group_key = st.selectbox("Select a group to update", list(group_options.keys()))
        selected_group = group_options[selected_group_key]

        group_types = sorted({g['type'] for g in groups if 'type' in g and g['type']})
        selected_type = selected_group['type']
        type_index = group_types.index(selected_type) if selected_type in group_types else 0

        with st.form("update_group_form"):
            updated_name = st.text_input("New Group Name", value=selected_group['name'])
            updated_type = st.selectbox("New Group Type", group_types, index=type_index)
            update_submit = st.form_submit_button("Update Group")

            if update_submit:
                update_data = {
                    'name': updated_name,
                    'type': updated_type
                }

                try:
                    group_id = selected_group['group_id']
                    put_response = requests.put(
                        f'http://localhost:4000/admin/groups/{group_id}', json=update_data
                    )

                    if put_response.status_code == 200:
                        st.success(f"Group '{updated_name}' updated successfully!")
                    else:
                        st.error("Failed to update group.")
                except Exception as e:
                    st.error(f"Error connecting to server: {e}")
    else:
        st.info("No groups available to update.")
except Exception as e:
    st.error(f"Could not retrieve groups to update: {e}")