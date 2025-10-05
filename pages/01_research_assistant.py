"""
Research Assistant Page - Multi-source Research Paper Search
Clean and modular version with improved error handling
"""

import streamlit as st
from src.core.research_search import ResearchSearcher
from src.utils.session_manager import SessionStateManager
from config.settings import Settings
from config.constants import UI_MESSAGES, EXAMPLE_QUERIES

# Initialize session state
SessionStateManager.initialize()

# Check OpenAI API key
if not Settings.is_openai_configured():
    st.error(UI_MESSAGES["NO_OPENAI_KEY"])
    st.stop()

# Header
st.markdown("Search for research papers across multiple academic databases")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Search Configuration")

    # Model selection
    model = st.selectbox(
        "AI Model",
        Settings.get_model_options(),
        index=0,
        help="Choose the AI model for search operations",
    )

    # Search source selection
    st.subheader("📚 Search Sources")
    use_arxiv = st.checkbox("ArXiv", value=True, help="Search ArXiv preprint server")
    use_semantic = st.checkbox(
        "Semantic Scholar", value=True, help="Search Semantic Scholar database"
    )
    use_google = st.checkbox(
        "Google Scholar",
        value=False,
        help="Requires Google API key (configure in Settings)",
        disabled=not Settings.is_google_configured(),
    )
    use_ddg = st.checkbox(
        "DuckDuckGo", value=False, help="General web search for research"
    )

    # Advanced options
    with st.expander("🔧 Advanced Options"):
        max_results = st.slider("Max Results per Source", 5, 50, 10)
        include_abstracts = st.checkbox("Include Abstracts", value=True)
        filter_year = st.number_input(
            "Min Publication Year", min_value=2000, max_value=2025, value=2020, step=1
        )

    # Statistics
    if st.session_state.get(SessionStateManager.SEARCH_HISTORY):
        st.markdown("---")
        st.metric("Total Searches", len(SessionStateManager.get_search_history()))

# Main content area
tab1, tab2 = st.tabs(["🔍 New Search", "📜 Search History"])

# Tab 1: New Search
with tab1:
    st.subheader("Enter Your Research Query")

    # Search input
    search_query = st.text_input(
        "Research query",
        placeholder="e.g., machine learning bias detection in healthcare",
        help="Enter keywords, research topics, or specific paper titles",
        label_visibility="collapsed",
    )

    # Quick search examples
    st.markdown("**💡 Quick Examples:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 AI & ML", use_container_width=True):
            search_query = EXAMPLE_QUERIES["AI_ML"]
            st.rerun()

    with col2:
        if st.button("🏥 Healthcare", use_container_width=True):
            search_query = EXAMPLE_QUERIES["HEALTHCARE"]
            st.rerun()

    with col3:
        if st.button("🔬 Data Science", use_container_width=True):
            search_query = EXAMPLE_QUERIES["DATA_SCIENCE"]
            st.rerun()

    # Search button
    if st.button(
        "🚀 Search Papers",
        type="primary",
        use_container_width=True,
        disabled=not search_query,
    ):
        if not search_query:
            st.warning("Please enter a search query")
        elif not any([use_arxiv, use_semantic, use_google, use_ddg]):
            st.warning("Please select at least one search source")
        else:
            try:
                # Initialize searcher
                searcher = ResearchSearcher(model_name=model)

                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()

                def update_progress(current, total, message):
                    progress = current / total
                    progress_bar.progress(progress)
                    status_text.text(message)

                # Perform search
                with st.spinner("Searching..."):
                    results = searcher.search_all_sources(
                        query=search_query,
                        use_arxiv=use_arxiv,
                        use_semantic=use_semantic,
                        use_google=use_google,
                        use_ddg=use_ddg,
                        progress_callback=update_progress,
                    )

                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()

                # Store results
                SessionStateManager.set(
                    SessionStateManager.RESEARCH_RESULTS,
                    {
                        "query": search_query,
                        "results": results,
                    },
                )

                # Add to search history
                sources = []
                if use_arxiv:
                    sources.append("ArXiv")
                if use_semantic:
                    sources.append("Semantic Scholar")
                if use_google:
                    sources.append("Google Scholar")
                if use_ddg:
                    sources.append("DuckDuckGo")

                SessionStateManager.add_search_to_history(search_query, sources)

                st.success("✅ Search completed!")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Search failed: {str(e)}")
                st.info("Please check your API keys and internet connection.")

# Tab 2: Search History
with tab2:
    search_history = SessionStateManager.get_search_history()

    if search_history:
        st.subheader("📜 Previous Searches")

        # Display last 10 searches
        for i, search in enumerate(reversed(search_history[-10:])):
            with st.expander(f"🔍 {search['query']}", expanded=False):
                st.markdown(f"**Sources:** {', '.join(search['sources'])}")
                st.markdown(f"**Time:** {search['timestamp']}")

                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button(
                        "🔄 Repeat", key=f"repeat_{i}", use_container_width=True
                    ):
                        search_query = search["query"]
                        st.rerun()
    else:
        st.info(UI_MESSAGES["NO_SEARCH_HISTORY"])

# Display results
research_results = SessionStateManager.get(SessionStateManager.RESEARCH_RESULTS)

if research_results:
    st.markdown("---")
    st.header("📊 Search Results")

    st.subheader(f"Results for: '{research_results['query']}'")

    # Results tabs by source
    if research_results.get("results"):
        source_tabs = st.tabs(list(research_results["results"].keys()))

        for i, (source, content) in enumerate(research_results["results"].items()):
            with source_tabs[i]:
                st.subheader(f"{source} Results")

                if isinstance(content, str) and content.startswith("Error:"):
                    st.error(content)
                else:
                    st.markdown(content)

                    # Export button
                    if st.button(f"📥 Export {source} Results", key=f"export_{source}"):
                        st.download_button(
                            label="Download as Text",
                            data=content,
                            file_name=f"{source.replace(' ', '_').lower()}_results.txt",
                            mime="text/plain",
                            key=f"download_{source}",
                        )

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Export as Markdown", use_container_width=True):
            # Prepare markdown content
            md_content = f"# Search Results: {research_results['query']}\n\n"
            for source, content in research_results["results"].items():
                md_content += f"## {source}\n\n{content}\n\n"

            st.download_button(
                label="Download Markdown",
                data=md_content,
                file_name=f"search_results_{research_results['query'][:30]}.md",
                mime="text/markdown",
            )

    with col2:
        if st.button("📋 Copy All Results", use_container_width=True):
            st.info("Results copied! (Use browser's copy feature)")

    with col3:
        if st.button("🗑️ Clear Results", use_container_width=True):
            SessionStateManager.clear(SessionStateManager.RESEARCH_RESULTS)
            st.rerun()

# Help section
with st.expander("ℹ️ How to Use Research Assistant"):
    st.markdown(
        """
    ### Research Assistant Guide
    
    #### Getting Started
    1. **Enter Query**: Type your research topic or keywords
    2. **Select Sources**: Choose which databases to search
    3. **Configure Options**: Adjust search parameters in the sidebar
    4. **Run Search**: Click "Search Papers" to start
    5. **Review Results**: Browse results by source
    6. **Export**: Save results in your preferred format
    
    #### Search Sources
    - **ArXiv**: Preprint server for physics, math, CS, etc.
    - **Semantic Scholar**: AI-powered academic search engine
    - **Google Scholar**: Google's academic search (requires API key)
    - **DuckDuckGo**: General web search for research papers
    
    #### Tips for Better Results
    - Use specific keywords rather than general terms
    - Combine multiple sources for comprehensive coverage
    - Check search history to avoid duplicate searches
    - Export results for further analysis
    - Use filter year to focus on recent research
    """
    )
