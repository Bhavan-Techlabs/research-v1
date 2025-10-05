"""
Research Assistant Platform - Main Application Entry Point
Clean, modular version with improved error handling
"""

import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Research Assistant Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load authentication configuration
config_path = Path(".streamlit/config.yaml")
if not config_path.exists():
    st.error(
        "⚠️ Authentication configuration file not found. Please create .streamlit/config.yaml"
    )
    st.stop()

with open(config_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Authentication logic
try:
    authenticator.login()
except Exception as e:
    st.error(f"Authentication error: {e}")
    st.stop()

# Handle authentication status
if st.session_state.get("authentication_status"):
    # User is authenticated
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.get('name', 'User')}!")
        authenticator.logout("Logout", "sidebar")
        st.markdown("---")

    # Load navigation
    nav = get_nav_from_toml(".streamlit/pages_sections.toml")
    pg = st.navigation(nav)
    add_page_title(pg)
    pg.run()

elif st.session_state.get("authentication_status") is False:
    st.error("❌ Username/password is incorrect")
    st.info("Please check your credentials and try again.")

elif st.session_state.get("authentication_status") is None:
    st.warning("⚠️ Please enter your username and password")
    st.info("Use your credentials to access the Research Assistant Platform.")
