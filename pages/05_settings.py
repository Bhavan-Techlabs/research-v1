"""
Settings Page
Configure LLM providers, API keys, and application settings
"""

import streamlit as st
from src.utils.credentials_manager import CredentialsManager, LLMConfigWidget
from src.services.llm_manager import get_llm_manager
from src.utils.session_manager import SessionStateManager
from config.settings import Settings

# Page configuration
st.markdown("Configure LLM providers, API keys, and other application settings")

# Initialize
CredentialsManager.initialize()
SessionStateManager.initialize()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔑 LLM Providers", "🎨 Preferences", "📊 Usage Stats", "ℹ️ About"]
)

with tab1:
    st.subheader("🔑 LLM Provider Configuration")
    st.markdown(
        """
    Configure API keys for different LLM providers. Your keys are stored securely in your browser session
    and are never sent to any third parties except the respective LLM providers.
    """
    )

    st.divider()

    # Render all provider configurations
    LLMConfigWidget.render_all_providers()

    st.divider()

    # Test connection section
    st.subheader("🧪 Test Configuration")
    st.markdown("Test your LLM configuration before using it in the app")

    configured_providers = CredentialsManager.get_configured_providers()

    if not configured_providers:
        st.info("No providers configured yet. Configure at least one provider above.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            test_provider, test_model = LLMConfigWidget.render_model_selector()

        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button(
                "🧪 Test Connection", type="primary", use_container_width=True
            ):
                if test_provider and test_model:
                    with st.spinner(f"Testing {test_provider} - {test_model}..."):
                        try:
                            llm_manager = get_llm_manager()

                            # Get credentials
                            creds = CredentialsManager.get_credential(test_provider)
                            llm_manager.set_credentials(test_provider, **creds)

                            # Initialize model
                            llm = llm_manager.initialize_model(
                                provider=test_provider,
                                model=test_model,
                                temperature=0.0,
                            )

                            # Test with a simple query
                            from langchain_core.messages import HumanMessage

                            response = llm.invoke(
                                [
                                    HumanMessage(
                                        content="Say 'Hello, I'm working!' in 5 words or less."
                                    )
                                ]
                            )

                            st.success("✅ Connection successful!")
                            st.info(f"**Response:** {response.content}")

                        except Exception as e:
                            st.error(f"❌ Connection failed: {str(e)}")
                else:
                    st.error("Please select a provider and model")

with tab2:
    st.subheader("🎨 Application Preferences")

    # Default LLM settings
    st.markdown("### Default LLM Settings")
    st.markdown("Set default values for LLM configuration across the app")

    col1, col2 = st.columns(2)

    with col1:
        default_temperature = st.slider(
            "Default Temperature",
            min_value=0.0,
            max_value=1.0,
            value=SessionStateManager.get("default_temperature", 0.0),
            step=0.1,
            help="Higher values make output more creative but less consistent",
        )

        default_max_tokens = st.number_input(
            "Default Max Tokens",
            min_value=100,
            max_value=8000,
            value=SessionStateManager.get("default_max_tokens", 2000),
            step=100,
            help="Maximum length of generated responses",
        )

    with col2:
        default_chunk_size = st.slider(
            "Default Chunk Size (RAG)",
            min_value=500,
            max_value=2000,
            value=SessionStateManager.get("default_chunk_size", 1000),
            step=100,
            help="Size of text chunks for RAG retrieval",
        )

        default_chunk_overlap = st.slider(
            "Default Chunk Overlap (RAG)",
            min_value=0,
            max_value=500,
            value=SessionStateManager.get("default_chunk_overlap", 200),
            step=50,
            help="Overlap between text chunks",
        )

    if st.button("💾 Save Preferences", type="primary"):
        SessionStateManager.set("default_temperature", default_temperature)
        SessionStateManager.set("default_max_tokens", default_max_tokens)
        SessionStateManager.set("default_chunk_size", default_chunk_size)
        SessionStateManager.set("default_chunk_overlap", default_chunk_overlap)
        st.success("✅ Preferences saved!")

    st.divider()

    # UI Preferences
    st.markdown("### UI Preferences")

    col1, col2 = st.columns(2)

    with col1:
        show_welcome = st.checkbox(
            "Show welcome message on home page",
            value=SessionStateManager.get("show_welcome", True),
        )

        show_tips = st.checkbox(
            "Show tips and help text", value=SessionStateManager.get("show_tips", True)
        )

    with col2:
        auto_scroll = st.checkbox(
            "Auto-scroll in chat", value=SessionStateManager.get("auto_scroll", True)
        )

        compact_mode = st.checkbox(
            "Compact mode (reduce spacing)",
            value=SessionStateManager.get("compact_mode", False),
        )

    if st.button("💾 Save UI Preferences"):
        SessionStateManager.set("show_welcome", show_welcome)
        SessionStateManager.set("show_tips", show_tips)
        SessionStateManager.set("auto_scroll", auto_scroll)
        SessionStateManager.set("compact_mode", compact_mode)
        st.success("✅ UI preferences saved!")

    st.divider()

    # Data Management
    st.markdown("### 🗄️ Data Management")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑️ Clear Search History", use_container_width=True):
            SessionStateManager.set("search_history", [])
            st.success("Search history cleared!")

    with col2:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            SessionStateManager.set("rag_chat_history", [])
            st.success("Chat history cleared!")

    with col3:
        if st.button("🗑️ Clear All Data", use_container_width=True, type="primary"):
            if st.session_state.get("confirm_clear_all"):
                # Clear everything
                SessionStateManager.set("search_history", [])
                SessionStateManager.set("rag_chat_history", [])
                SessionStateManager.set("rag_documents", [])
                SessionStateManager.set("rag_retriever", None)
                SessionStateManager.set("analysis_count", 0)
                SessionStateManager.set("search_count", 0)
                SessionStateManager.set("chat_messages", 0)
                st.session_state["confirm_clear_all"] = False
                st.success("All data cleared!")
                st.rerun()
            else:
                st.session_state["confirm_clear_all"] = True
                st.warning("⚠️ Click again to confirm")

with tab3:
    st.subheader("📊 Usage Statistics")

    # Get stats
    search_count = SessionStateManager.get("search_count", 0)
    analysis_count = SessionStateManager.get("analysis_count", 0)
    chat_messages = SessionStateManager.get("chat_messages", 0)
    search_history = SessionStateManager.get("search_history", [])

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🔍 Searches", search_count)

    with col2:
        st.metric("📄 Papers Analyzed", analysis_count)

    with col3:
        st.metric("💬 Chat Messages", chat_messages)

    with col4:
        st.metric(
            "📚 Documents Loaded", len(SessionStateManager.get("rag_documents", []))
        )

    st.divider()

    # Recent searches
    st.markdown("### 🕒 Recent Searches")

    if search_history:
        for idx, search in enumerate(reversed(search_history[-10:])):
            with st.expander(
                f"Search {len(search_history) - idx}: {search.get('query', 'N/A')}",
                expanded=False,
            ):
                st.markdown(f"**Query:** {search.get('query', 'N/A')}")
                st.markdown(f"**Sources:** {', '.join(search.get('sources', []))}")
                st.markdown(f"**Results:** {search.get('results', 0)}")
    else:
        st.info("No search history yet")

    st.divider()

    # Provider usage
    st.markdown("### 🤖 Configured Providers")

    configured = CredentialsManager.get_configured_providers()

    if configured:
        for provider in configured:
            llm_manager = get_llm_manager()
            provider_info = llm_manager.get_provider_info(provider)
            st.markdown(f"✅ **{provider_info.get('name', provider)}**")
    else:
        st.info("No providers configured")

with tab4:
    st.subheader("ℹ️ About Research Assistant")

    st.markdown(
        """
    ### 🎯 Features
    
    **Research Assistant** is a comprehensive tool for academic research powered by multiple LLM providers:
    
    - 🔍 **Multi-Source Search**: ArXiv, Semantic Scholar, Google, DuckDuckGo
    - 📄 **Paper Analysis**: AI-powered analysis with customizable prompts
    - 💬 **RAG Chat**: Chat with your research documents
    - 📝 **Prompt Manager**: Organize and reuse research prompts
    - 🤖 **Multi-LLM Support**: OpenAI, Anthropic, Google, Azure, Cohere, and more
    
    ### 🔒 Privacy & Security
    
    - API keys stored securely in browser session only
    - No data sent to third parties except chosen LLM providers
    - Local document processing
    - Optional MongoDB integration for prompt storage
    
    ### 🛠️ Technology Stack
    
    - **Framework**: Streamlit
    - **LLM Integration**: LangChain with multi-provider support
    - **Vector Store**: ChromaDB
    - **Document Processing**: PyMuPDF, BeautifulSoup
    - **Search APIs**: ArXiv, Semantic Scholar, Google, DuckDuckGo
    
    ### 📝 Version
    
    **Version**: 2.0.0  
    **Last Updated**: 2024
    
    ### 🔗 Resources
    
    - [Documentation](#)
    - [GitHub Repository](#)
    - [Report Issues](#)
    
    ### 👏 Credits
    
    Built with ❤️ using open-source tools and libraries.
    """
    )

    st.divider()

    # System info
    st.markdown("### 🖥️ System Information")

    import sys
    import platform

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Python Version**: {sys.version.split()[0]}")
        st.markdown(f"**Platform**: {platform.system()} {platform.release()}")

    with col2:
        st.markdown(f"**Streamlit Version**: {st.__version__}")
        settings = Settings()
        st.markdown(
            f"**Environment**: {'Production' if settings.is_openai_configured() else 'Development'}"
        )

# Footer
st.divider()
st.markdown(
    """
<div style='text-align: center; color: gray;'>
    Research Assistant v2.0 | Multi-LLM Support | Powered by LangChain
</div>
""",
    unsafe_allow_html=True,
)
