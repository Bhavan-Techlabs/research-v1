"""
Home Page - Research Assistant Platform Dashboard
"""

import streamlit as st
from src.utils.session_manager import SessionStateManager
from src.utils.dynamic_selector import get_configured_providers
from config.settings import Settings

# Initialize session state
SessionStateManager.initialize()

# Header
st.markdown("### Your AI-Powered Research Companion")

st.markdown(
    """
Welcome to the Research Assistant Platform! This comprehensive tool helps researchers:
- 🔍 Search for papers across multiple academic databases
- 📄 Analyze research papers with AI
- 💬 Chat with your documents using RAG
- 📝 Manage research prompts
- ⚙️ Configure settings and API keys
"""
)

st.markdown("---")

# Dashboard metrics
st.subheader("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    search_history = SessionStateManager.get_search_history()
    st.metric(
        "Search History", len(search_history), help="Total number of searches performed"
    )

with col2:
    analysis_results = SessionStateManager.get(SessionStateManager.ANALYSIS_RESULTS)
    analysis_count = len(analysis_results) if analysis_results else 0
    st.metric("Papers Analyzed", analysis_count, help="Number of papers analyzed")

with col3:
    chat_history = SessionStateManager.get_chat_history()
    st.metric("Chat Messages", len(chat_history), help="Total chat messages")

with col4:
    docs_loaded = SessionStateManager.get(SessionStateManager.DOCUMENTS_LOADED, [])
    st.metric("Documents Loaded", len(docs_loaded), help="Documents in RAG system")

st.markdown("---")

# Quick Links
st.subheader("🚀 Quick Access")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Research Tools")
    st.page_link(
        "pages/01_research_assistant.py",
        label="🔍 Research Assistant",
        help="Search for papers",
    )
    st.page_link(
        "pages/02_paper_analyzer.py",
        label="📄 Paper Analyzer",
        help="Analyze PDF papers",
    )
    st.page_link(
        "pages/03_rag_chat.py", label="💬 RAG Chat System", help="Chat with documents"
    )
    st.page_link(
        "pages/04_prompt_manager.py", label="📝 Prompt Manager", help="Manage prompts"
    )

with col2:
    st.markdown("#### Configuration")
    st.page_link(
        "pages/05_settings.py",
        label="⚙️ Settings",
        help="Configure API keys and settings",
    )

    st.markdown("#### System Status")

    # Get configured LLM providers
    configured_providers = get_configured_providers()
    llm_status = (
        f"✅ {len(configured_providers)} provider(s) configured"
        if configured_providers
        else "❌ No providers configured"
    )

    mongodb_status = (
        "✅ Connected" if Settings.is_mongodb_configured() else "❌ Not configured"
    )

    st.markdown(
        f"""
    - **LLM Providers**: {llm_status}
    - **MongoDB**: {mongodb_status}
    """
    )

st.markdown("---")

# Getting Started Guide
with st.expander("📚 Getting Started Guide", expanded=False):
    st.markdown(
        """
    ### First Time Setup
    
    1. **Configure API Keys** (Settings page)
       - Add your OpenAI API key (required)
       - Optionally add Google API key for Google Scholar search
       - Optionally add MongoDB URI for prompt management
    
    2. **Search for Papers** (Research Assistant)
       - Enter research keywords
       - Select databases to search
       - View and export results
    
    3. **Analyze Papers** (Paper Analyzer)
       - Upload PDF files
       - Choose analysis type
       - Get AI-powered insights
    
    4. **Chat with Documents** (RAG Chat)
       - Upload research papers
       - Ask questions about the content
       - Get context-aware answers
    
    5. **Manage Prompts** (Prompt Manager)
       - Create reusable research prompts
       - Organize by category
       - Search and edit existing prompts
    
    ### Tips for Best Results
    
    - Use specific keywords for better search results
    - Upload high-quality PDF files for analysis
    - Try different analysis types for different insights
    - Use RAG chat for deep document exploration
    - Save frequently used prompts for quick access
    """
    )

# Help & Resources
with st.expander("❓ Help & Resources", expanded=False):
    st.markdown(
        """
    ### Need Help?
    
    - **Documentation**: Check the README.md for detailed information
    - **API Keys**: Visit the Settings page for configuration guides
    - **Issues**: Report bugs or request features on GitHub
    
    ### Useful Links
    
    - [OpenAI Platform](https://platform.openai.com/)
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [ArXiv](https://arxiv.org/)
    - [Semantic Scholar](https://www.semanticscholar.org/)
    """
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Research Assistant Platform v2.0 | Built with Streamlit & OpenAI</p>
        <p>Use the navigation sidebar to access different tools →</p>
    </div>
    """,
    unsafe_allow_html=True,
)
