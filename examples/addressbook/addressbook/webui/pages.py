"""
Addressbook CLI Streamlit module.
"""

import logging
import pandas as pd
import typing

import dictdiffer
import requests

RESOURCE_TYPES = [
    "addressbook",
    "persons",
    "postal_codes",
]

TIMEOUT = 5  # Default timeout for requests

_LOGGER = logging.getLogger(__name__)


class PageBase:
    """Base class for a Streamlit Page."""

    DEFAULT_BASEURL = "http://localhost:8080"

    def __init__(self, st: typing.Any, baseurl: str, resource_type: str):
        self.st = st
        self.baseurl = baseurl
        self.resource_type = resource_type
        self.api_url = self.DEFAULT_BASEURL
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


class AddressbookPage(PageBase):
    """Streamlit Page for ."""

    def __init__(self, st: typing.Any):
        super().__init__(st, "/addressbook", "addressbook")

    def column_config(self):
        """Get the column config for addressbook."""
        return {
            "addrtype": self.st.column_config.SelectboxColumn(
                label="Addrtype",
                help="The address type, e.g. work or home",
                required=True,
                options=["work", "home"],
            ),
            "city": self.st.column_config.TextColumn(
                label="City",
                help="The city of this address",
                required=True,
            ),
            "country": self.st.column_config.TextColumn(
                label="Country",
                help="The country of this address",
                required=True,
            ),
            "is_valid": self.st.column_config.CheckboxColumn(
                label="Is Valid",
                help="Address is valid or not",
            ),
            "people": self.st.column_config.ListColumn(
                label="People",
                help="A list of people's names living there",
            ),
            "person": self.st.column_config.JsonColumn(
                label="Person",
                help="This is a person object that lives at this address.",
            ),
            "state": self.st.column_config.TextColumn(
                label="State",
                help="The state of this address",
                required=True,
            ),
            "street": self.st.column_config.TextColumn(
                label="Street",
                help="The street and civic number of this address",
                required=True,
            ),
        }

    def show(self):
        """Show the page data."""
        # self.st.set_page_config(
        #    page_title="Addressbook",
        #    page_icon="📋",
        #    layout="wide",
        #    initial_sidebar_state="collapsed",
        # )
        self.st.subheader("Addressbook")
        self.st.markdown(
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

        resources = self.get_resources()
        if not resources:
            return

        df = pd.DataFrame(resources)

        edited_df = self.st.data_editor(
            df,
            column_config=self.column_config(),
            key="editor",
            num_rows="dynamic",
        )

        # Detect changes in the table and update via PUT request
        if df is not None and edited_df is not None:
            backend_len = len(df.index)
            grid_len = len(list(edited_df.iterrows()))

            print(f"edited_df.iterrows: {edited_df.iterrows()}")
            print(f"edited_df.size: {edited_df.size}")
            print(f"list(edited_df.iterrows): {list(edited_df.iterrows())}")
            print(f"len(list(edited_df.iterrows)): {len(list(edited_df.iterrows()))}")

            # This means we are adding/creaating a new record
            if backend_len < grid_len:
                index = grid_len - 1
                new_resource = edited_df.loc[index].to_dict()
                self.create_resource(new_resource)
                resources = self.get_resources()
                df = pd.DataFrame(resources)
                return

            # Delete resource
            if backend_len > grid_len:
                # handle delete
                # delete_id = self.st.text_input("Enter Resource ID to delete")
                # self.delete_resource(delete_id)
                self.st.write()
                return

            for index, row in edited_df.iterrows():
                print(f"df.size: {df.size}")
                original_row = df.iloc[index].to_dict()
                edited_row = row.to_dict()
                print(f"original_row: {original_row}")
                print(f"edited_row: {edited_row}")
                diffs = list(dictdiffer.diff(original_row, edited_row))
                print(f"diffs: {diffs}")
                if diffs:
                    key = "foo"
                    self.update_resource(key, edited_row)

        self.st.write()


class PersonsPage(PageBase):
    """Streamlit Page for ."""

    def __init__(self, st: typing.Any):
        super().__init__(st, "/persons", "persons")

    def column_config(self):
        """Get the column config for persons."""
        return {
            "age": self.st.column_config.NumberColumn(
                label="Age",
                help="The person's age",
            ),
            "first_name": self.st.column_config.TextColumn(
                label="First Name",
                help="The person's first name",
            ),
            "hobbies": self.st.column_config.ListColumn(
                label="Hobbies",
                help="The person's hobbies",
            ),
            "last_name": self.st.column_config.TextColumn(
                label="Last Name",
                help="The person's last name",
            ),
        }

    def show(self):
        """Show the page data."""
        # self.st.set_page_config(
        #    page_title="Persons",
        #    page_icon="📋",
        #    layout="wide",
        #    initial_sidebar_state="collapsed",
        # )
        self.st.subheader("Persons")
        self.st.markdown(
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

        resources = self.get_resources()
        if not resources:
            return

        df = pd.DataFrame(resources)

        edited_df = self.st.data_editor(
            df,
            column_config=self.column_config(),
            key="editor",
            num_rows="dynamic",
        )

        # Detect changes in the table and update via PUT request
        if df is not None and edited_df is not None:
            backend_len = len(df.index)
            grid_len = len(list(edited_df.iterrows()))

            print(f"edited_df.iterrows: {edited_df.iterrows()}")
            print(f"edited_df.size: {edited_df.size}")
            print(f"list(edited_df.iterrows): {list(edited_df.iterrows())}")
            print(f"len(list(edited_df.iterrows)): {len(list(edited_df.iterrows()))}")

            # This means we are adding/creaating a new record
            if backend_len < grid_len:
                index = grid_len - 1
                new_resource = edited_df.loc[index].to_dict()
                self.create_resource(new_resource)
                resources = self.get_resources()
                df = pd.DataFrame(resources)
                return

            # Delete resource
            if backend_len > grid_len:
                # handle delete
                # delete_id = self.st.text_input("Enter Resource ID to delete")
                # self.delete_resource(delete_id)
                self.st.write()
                return

            for index, row in edited_df.iterrows():
                print(f"df.size: {df.size}")
                original_row = df.iloc[index].to_dict()
                edited_row = row.to_dict()
                print(f"original_row: {original_row}")
                print(f"edited_row: {edited_row}")
                diffs = list(dictdiffer.diff(original_row, edited_row))
                print(f"diffs: {diffs}")
                if diffs:
                    key = "foo"
                    self.update_resource(key, edited_row)

        self.st.write()


class Postal_codesPage(PageBase):
    """Streamlit Page for ."""

    def __init__(self, st: typing.Any):
        super().__init__(st, "/postal_codes", "postal_codes")

    def column_config(self):
        """Get the column config for postal_codes."""
        return {
            "name": self.st.column_config.TextColumn(
                label="Name",
                help="The postal code's name/id",
            ),
        }

    def show(self):
        """Show the page data."""
        # self.st.set_page_config(
        #    page_title="Postal_codes",
        #    page_icon="📋",
        #    layout="wide",
        #    initial_sidebar_state="collapsed",
        # )
        self.st.subheader("Postal_codes")
        self.st.markdown(
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

        resources = self.get_resources()
        if not resources:
            return

        df = pd.DataFrame(resources)

        edited_df = self.st.data_editor(
            df,
            column_config=self.column_config(),
            key="editor",
            num_rows="dynamic",
        )

        # Detect changes in the table and update via PUT request
        if df is not None and edited_df is not None:
            backend_len = len(df.index)
            grid_len = len(list(edited_df.iterrows()))

            print(f"edited_df.iterrows: {edited_df.iterrows()}")
            print(f"edited_df.size: {edited_df.size}")
            print(f"list(edited_df.iterrows): {list(edited_df.iterrows())}")
            print(f"len(list(edited_df.iterrows)): {len(list(edited_df.iterrows()))}")

            # This means we are adding/creaating a new record
            if backend_len < grid_len:
                index = grid_len - 1
                new_resource = edited_df.loc[index].to_dict()
                self.create_resource(new_resource)
                resources = self.get_resources()
                df = pd.DataFrame(resources)
                return

            # Delete resource
            if backend_len > grid_len:
                # handle delete
                # delete_id = self.st.text_input("Enter Resource ID to delete")
                # self.delete_resource(delete_id)
                self.st.write()
                return

            for index, row in edited_df.iterrows():
                print(f"df.size: {df.size}")
                original_row = df.iloc[index].to_dict()
                edited_row = row.to_dict()
                print(f"original_row: {original_row}")
                print(f"edited_row: {edited_row}")
                diffs = list(dictdiffer.diff(original_row, edited_row))
                print(f"diffs: {diffs}")
                if diffs:
                    key = "foo"
                    self.update_resource(key, edited_row)

        self.st.write()
