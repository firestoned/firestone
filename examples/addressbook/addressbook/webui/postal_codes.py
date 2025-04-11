"""
Addressbook CLI Streamlit module.
"""

import logging
import pandas as pd
import typing

import dictdiffer
import requests
import streamlit as st

DEFAULT_BASEURL = "http://localhost:8080"

TIMEOUT = 5  # Default timeout for requests

_LOGGER = logging.getLogger(__name__)


class PageBase:
    """Base class for a Streamlit Page."""

    def __init__(self, st: typing.Any, baseurl: str, resource_type: str):
        self.st = st
        self.baseurl = baseurl
        self.resource_type = resource_type
        self.api_url = DEFAULT_BASEURL
        if self.baseurl:
            self.api_url += f"{self.baseurl}"

    def show(self, column_layout: dict):
        """Base method for writing to streamlit."""
        pass

    def add_custom_css(css: str):
        """Add some custom CSS to this page."""
        st.markdown(
            f"""
            <style>
                {css}
            </style>
            """,
            unsafe_allow_html=True,
        )

    def get_resources(self):
        try:
            response = requests.get(f"{self.api_url}", timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.st.error(f"Error fetching resources: {e}")
            return []

    def update_resource(self, resource_id: str, updated_data):
        """Update an existing resource for this resource type."""
        try:
            print(f"updated_data: {updated_data}")
            response = requests.put(
                f"{self.api_url}/{resource_id}", json=updated_data, timeout=TIMEOUT
            )
            response.raise_for_status()
            self.st.toast(f"{self.resource_type.capitalize()} updated successfully", icon="✅")
        except requests.RequestException as e:
            self.st.error(f"Error updating resource: {e}")

    def create_resource(self, new_data):
        """Create a new resource for this resource type."""
        try:
            print(f"new_data: {new_data}")
            response = requests.post(f"{self.api_url}", json=new_data, timeout=TIMEOUT)
            response.raise_for_status()
            self.st.toast(f"{self.resource_type.capitalize()} created successfully: {new_data}")
        except requests.RequestException as e:
            self.st.error(f"Error creating resource: {e}")

    def delete_resource(self, resource_id):
        """Create a new resource for this resource type."""
        try:
            response = requests.delete(f"{self.api_url}/{resource_id}", timeout=TIMEOUT)
            response.raise_for_status()
            self.st.toast(f"{self.resource_type} deleted successfully")
        except requests.RequestException as e:
            self.st.error(f"Error deleting resource {resource_id}: {e}")


page = PageBase(st, "/postal_codes", "postal_codes")

column_config = {
    "name": st.column_config.TextColumn(
        label="Name",
        help="The postal code's name/id",
    ),
    "uuid": st.column_config.TextColumn(
        label="Uuid",
        help="A UUID associated to this postal code",
    ),
}

st.subheader("Postal_codes")
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""",
    unsafe_allow_html=True,
)


@st.dialog("Create Postal Codes")
def create():
    with st.form("Create"):

        st.text_input("Name")

        st.text_input("Uuid")

        submit = st.form_submit_button("Create")

    if st.button("Submit"):
        # st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()


if st.button("Create"):
    create()

resources = page.get_resources()

df = pd.DataFrame(resources)

edited_df = st.data_editor(
    df,
    column_config=column_config,
    key="editor",
    num_rows="fixed",
    hide_index=True,
)

# Detect changes in the table and update via PUT request
if df is not None and edited_df is not None:
    backend_len = len(df.index)
    grid_len = len(list(edited_df.iterrows()))

    print(f"edited_df.iterrows: {edited_df.iterrows()}")
    print(f"edited_df.size: {edited_df.size}")
    print(f"list(edited_df.iterrows): {list(edited_df.iterrows())}")
    print(f"len(list(edited_df.iterrows)): {len(list(edited_df.iterrows()))}")

    for index, row in edited_df.iterrows():
        print(f"df.size: {df.size}")
        original_row = df.iloc[index].to_dict()
        edited_row = row.to_dict()
        print(f"original_row: {original_row}")
        print(f"edited_row: {edited_row}")
        diffs = list(dictdiffer.diff(original_row, edited_row))
        print(f"diffs: {diffs}")
        if diffs:
            key = edited_row["uuid"]
            page.update_resource(key, edited_row)

st.write()
