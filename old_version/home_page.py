import streamlit as st


# Example dashboard metrics (replace with real data sources as needed)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Projects", 5)
    st.metric("Papers Analyzed", 12)

with col2:
    st.metric("Prompts Managed", 8)
    st.metric("RAG Chats", 3)

with col3:
    st.metric("Team Members", 4)
    st.metric("Settings Updated", 2)

st.markdown("---")

st.header("Useful Links")

st.markdown("""
- [Research Assistant](?page=Research%20Assistant)
- [Paper Analyzer](?page=Paper%20Analyzer)
- [RAG Chat System](?page=RAG%20Chat%20System)
- [Prompt Manager](?page=Prompt%20Manager)
- [Settings](?page=Settings)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Project README](./README.md)
""")

st.markdown("---")

st.info("Use the navigation sidebar to access different research tools and settings.")
