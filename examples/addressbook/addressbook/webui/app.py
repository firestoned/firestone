"""
WebUi
"""

import importlib
import logging

import streamlit as st

from firestone_lib import utils as futils

_LOGGER = logging.getLogger(__name__)


# st.title("Addressbook")
st.set_page_config(
    page_title="Addressbook App",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stAppToolbar {display: none;}
        .stDeployButton {display: none;}
        footer {visibility: hidden;}
        #stDecoration {display: none;}
    </style>
""",
    unsafe_allow_html=True,
)

pages = {
    "Addrebook": [
        st.Page("addressbook.py", title="Addressbook"),
        st.Page("persons.py", title="Persons"),
        st.Page("postal_codes.py", title="Postal Codes"),
    ]
}

pg = st.navigation(pages)

pg.run()
