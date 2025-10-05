import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
import streamlit_authenticator as stauth


import yaml
from yaml.loader import SafeLoader

with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

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
    authenticator.logout()
    st.set_page_config(layout="wide")
    # If you want to use the no-sections version, this
    # defaults to looking in .streamlit/pages.toml, so you can
    # just call `get_nav_from_toml()`
    nav = get_nav_from_toml(".streamlit/pages_sections.toml")

    pg = st.navigation(nav)

    add_page_title(pg)

    pg.run()
elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')




