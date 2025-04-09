"""
WebUi
"""

import importlib
import logging

import streamlit as st

from firestone_lib import utils as futils
from addressbook.webui import pages

_LOGGER = logging.getLogger(__name__)


PAGE_MAP = {}
for col in pages.RESOURCE_TYPES:
    page_name = col.capitalize()
    _LOGGER.debug(f"col: {col}")
    PAGE_MAP[page_name] = getattr(pages, f"{page_name}Page")

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
st.sidebar.title("Addressbook Picker")

current_resource_type = st.sidebar.selectbox(
    "Select a Resource Type",
    [futils.split_capitalize(_) for _ in PAGE_MAP.keys()],
)
if not current_resource_type:
    st.write("Select an addressbook resource type to view resources")

PAGE_MAP[current_resource_type](st).show()
