import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Setup Authentication
with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get('authentication_status'):
    with st.sidebar:
        authenticator.logout("Logout", "sidebar")

    st.set_page_config(layout="wide")
    nav = get_nav_from_toml(".streamlit/pages_sections.toml")
    pg = st.navigation(nav)
    add_page_title(pg)
    pg.run()
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')
