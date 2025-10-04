"""Research Assistant Page - Multi-source research paper search and discovery"""

import streamlit as st
import sys
import os
from typing import List, Dict

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from core.research_app import ResearchApp
    from utils.mongo_utils import PromptManager
except ImportError:
    st.error("⚠️ Research app dependencies not installed. Please run: pip install -r requirements.txt")
    st.stop()

st.title("🔍 Research Assistant")
st.markdown("Search for research papers across multiple sources")

# Initialize session state
if "research_results" not in st.session_state:
    st.session_state.research_results = None
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# Sidebar configuration
with st.sidebar:
    st.header("Search Configuration")

    # Model selection
    model = st.selectbox(
        "AI Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0
    )

    # Search source selection
    st.subheader("Search Sources")
    use_arxiv = st.checkbox("ArXiv", value=True)
    use_semantic = st.checkbox("Semantic Scholar", value=True)
    use_google = st.checkbox(
        "Google Scholar", value=False, help="Requires Google API key"
    )
    use_ddg = st.checkbox("DuckDuckGo", value=False)

    # Advanced options
    with st.expander("Advanced Options"):
        max_results = st.slider("Max Results per Source", 5, 50, 10)
        include_abstracts = st.checkbox("Include Abstracts", value=True)
        filter_year = st.number_input(
            "Min Publication Year", min_value=2000, max_value=2025, value=2020
        )

# Main search interface
st.subheader("🔍 Search Research Papers")

# Search tabs
search_tab, history_tab = st.tabs(["New Search", "Search History"])

with search_tab:
    # Search input
    search_query = st.text_input(
        "Enter your research query",
        placeholder="e.g., machine learning bias detection in healthcare",
        help="Enter keywords, research topics, or specific paper titles"
    )

    # Quick search suggestions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🤖 AI & Machine Learning", use_container_width=True):
            search_query = "artificial intelligence machine learning"
    with col2:
        if st.button("🏥 Healthcare Research", use_container_width=True):
            search_query = "healthcare medical research"
    with col3:
        if st.button("🔬 Data Science", use_container_width=True):
            search_query = "data science analytics"

    # Search button
    if st.button("🚀 Search Papers", type="primary", use_container_width=True) and search_query:
        try:
            research_app = ResearchApp(model_name=model)
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_results = {}
            total_sources = sum([use_arxiv, use_semantic, use_google, use_ddg])
            current_source = 0

            # ArXiv search
            if use_arxiv:
                current_source += 1
                status_text.text("Searching ArXiv...")
                try:
                    arxiv_results = research_app.arxiv_search_agent(search_query)
                    all_results["ArXiv"] = arxiv_results
                except Exception as e:
                    all_results["ArXiv"] = f"Error: {str(e)}"
                progress_bar.progress(current_source / total_sources)

            # Semantic Scholar search
            if use_semantic:
                current_source += 1
                status_text.text("Searching Semantic Scholar...")
                try:
                    semantic_results = research_app.semantic_search_agent(search_query)
                    all_results["Semantic Scholar"] = semantic_results
                except Exception as e:
                    all_results["Semantic Scholar"] = f"Error: {str(e)}"
                progress_bar.progress(current_source / total_sources)

            # Google search
            if use_google:
                current_source += 1
                status_text.text("Searching Google Scholar...")
                try:
                    google_results = research_app.google_search(f"{search_query} site:scholar.google.com")
                    all_results["Google Scholar"] = google_results
                except Exception as e:
                    all_results["Google Scholar"] = f"Error: {str(e)}"
                progress_bar.progress(current_source / total_sources)

            # DuckDuckGo search
            if use_ddg:
                current_source += 1
                status_text.text("Searching DuckDuckGo...")
                try:
                    ddg_results = research_app.ddg_search(f"{search_query} research papers")
                    all_results["DuckDuckGo"] = ddg_results
                except Exception as e:
                    all_results["DuckDuckGo"] = f"Error: {str(e)}"
                progress_bar.progress(current_source / total_sources)

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Store results
            st.session_state.research_results = {
                "query": search_query,
                "results": all_results,
                "timestamp": st.session_state.get("timestamp", "")
            }

            # Add to search history
            st.session_state.search_history.append({
                "query": search_query,
                "sources": [s for s, use in [("ArXiv", use_arxiv), ("Semantic", use_semantic), 
                          ("Google", use_google), ("DDG", use_ddg)] if use],
                "timestamp": "now"
            })

            st.success("✅ Search completed!")

        except Exception as e:
            st.error(f"Search failed: {str(e)}")

with history_tab:
    if st.session_state.search_history:
        st.subheader("Previous Searches")
        for i, search in enumerate(reversed(st.session_state.search_history[-10:])):  # Show last 10
            with st.expander(f"🔍 {search['query']}", expanded=False):
                st.write(f"**Sources:** {', '.join(search['sources'])}")
                st.write(f"**Time:** {search['timestamp']}")
                if st.button(f"Repeat Search", key=f"repeat_{i}"):
                    search_query = search['query']
                    st.rerun()
    else:
        st.info("No search history yet. Perform a search to see results here.")

# Display results
if st.session_state.research_results:
    st.markdown("---")
    st.header("🔬 Search Results")
    
    results = st.session_state.research_results
    st.subheader(f"Results for: '{results['query']}'")
    
    # Results tabs by source
    if results["results"]:
        source_tabs = st.tabs(list(results["results"].keys()))
        
        for i, (source, content) in enumerate(results["results"].items()):
            with source_tabs[i]:
                st.subheader(f"{source} Results")
                if isinstance(content, str) and content.startswith("Error:"):
                    st.error(content)
                else:
                    st.markdown(content)
                    
                # Export options
                if st.button(f"📥 Export {source} Results", key=f"export_{source}"):
                    st.info("Export functionality coming soon!")

    # Global export options
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Export All as PDF", use_container_width=True):
            st.info("PDF export coming soon!")
    with col2:
        if st.button("📄 Export as Markdown", use_container_width=True):
            st.info("Markdown export coming soon!")
    with col3:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.research_results = None
            st.rerun()

# Help section
with st.expander("ℹ️ How to Use Research Assistant"):
    st.markdown(
        """
    ### Research Assistant Guide
    
    1. **Enter Query**: Type your research topic or keywords
    2. **Select Sources**: Choose which databases to search
    3. **Configure Options**: Adjust search parameters in the sidebar
    4. **Run Search**: Click "Search Papers" to start
    5. **Review Results**: Browse results by source
    6. **Export**: Save results in your preferred format
    
    ### Search Sources
    
    - **ArXiv**: Preprint server for physics, mathematics, computer science, etc.
    - **Semantic Scholar**: AI-powered academic search engine
    - **Google Scholar**: Google's academic search (requires API key)
    - **DuckDuckGo**: General web search for research papers
    
    ### Tips
    
    - Use specific keywords for better results
    - Combine multiple sources for comprehensive coverage
    - Check search history to avoid duplicates
    - Export results for further analysis
    """
    )
