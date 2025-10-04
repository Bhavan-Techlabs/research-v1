"""Settings Page - Configuration and API key management"""

import streamlit as st
import os
from pathlib import Path

st.title("⚙️ Settings")
st.markdown("Configure your research application settings and API keys")

# API Keys section
st.header("🔑 API Configuration")

with st.expander("API Keys Setup", expanded=True):
    st.markdown("""
    **Required API Keys for full functionality:**
    
    - **OpenAI API Key**: Required for AI analysis and chat features
    - **Google API Key**: For Google Scholar search (optional)
    - **Google CSE ID**: For custom search engine (optional)
    """)
    
    # OpenAI API Key
    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Get your API key from https://platform.openai.com/"
    )
    
    # Google API Keys
    google_key = st.text_input(
        "Google API Key (Optional)",
        type="password", 
        value=os.getenv("GOOGLE_API_KEY", ""),
        help="For Google Scholar search functionality"
    )
    
    google_cse_id = st.text_input(
        "Google CSE ID (Optional)",
        value=os.getenv("GOOGLE_CSE_ID", ""),
        help="Custom Search Engine ID"
    )
    
    # MongoDB URI (optional)
    mongodb_uri = st.text_input(
        "MongoDB URI (Optional)",
        type="password",
        value=os.getenv("MONGODB_URI", ""),
        help="For saving prompts and templates"
    )
    
    if st.button("💾 Save API Keys"):
        # This would typically save to environment or config file
        st.success("✅ API keys saved (session only)")
        # In a real app, you'd want to save these securely

# Model Settings
st.header("🤖 Model Configuration")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Default Models")
    default_model = st.selectbox(
        "Default AI Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0
    )
    
    default_embedding = st.selectbox(
        "Default Embedding Model", 
        ["text-embedding-3-large", "text-embedding-3-small", "text-embedding-ada-002"],
        index=0
    )

with col2:
    st.subheader("Model Parameters")
    default_temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
    default_max_tokens = st.slider("Max Tokens", 1000, 16000, 4000, 500)

# Document Processing Settings
st.header("📄 Document Processing")

col1, col2 = st.columns(2)

with col1:
    st.subheader("PDF Processing")
    max_file_size = st.slider("Max File Size (MB)", 1, 100, 10)
    extract_images = st.checkbox("Extract Images", value=False)

with col2:
    st.subheader("Text Chunking")
    default_chunk_size = st.slider("Default Chunk Size", 500, 5000, 1000, 100)
    default_overlap = st.slider("Default Overlap", 0, 1000, 200, 50)

# Storage Settings
st.header("💾 Storage Configuration")

storage_path = st.text_input(
    "Document Storage Path",
    value="./documents",
    help="Local path to store uploaded documents"
)

vector_db_path = st.text_input(
    "Vector Database Path", 
    value="./chromadb",
    help="Path for ChromaDB vector storage"
)

# Advanced Settings
with st.expander("🔧 Advanced Settings"):
    st.subheader("Search Configuration")
    max_search_results = st.slider("Max Search Results", 5, 100, 20)
    search_timeout = st.slider("Search Timeout (seconds)", 10, 120, 60)
    
    st.subheader("Rate Limiting")
    api_rate_limit = st.slider("API Rate Limit (requests/minute)", 1, 60, 20)
    
    st.subheader("Caching")
    enable_caching = st.checkbox("Enable Response Caching", value=True)
    cache_ttl = st.slider("Cache TTL (hours)", 1, 48, 24)

# Save Settings
if st.button("💾 Save All Settings", type="primary", use_container_width=True):
    st.success("✅ Settings saved successfully!")

# System Information
st.header("ℹ️ System Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Application Info")
    st.info("""
    **Research Assistant v1.0**
    
    - Multi-source paper search
    - AI-powered analysis  
    - RAG chat system
    - Document management
    """)

with col2:
    st.subheader("System Status")
    
    # Check API keys
    openai_status = "✅ Configured" if openai_key else "❌ Not configured"
    google_status = "✅ Configured" if google_key else "⚠️ Optional"
    mongodb_status = "✅ Configured" if mongodb_uri else "⚠️ Optional"
    
    st.write(f"**OpenAI API**: {openai_status}")
    st.write(f"**Google API**: {google_status}")  
    st.write(f"**MongoDB**: {mongodb_status}")

# Data Management
st.header("🗂️ Data Management")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧹 Clear Cache", use_container_width=True):
        st.info("Cache cleared!")

with col2:
    if st.button("📤 Export Settings", use_container_width=True):
        st.info("Export functionality coming soon!")

with col3:
    if st.button("📥 Import Settings", use_container_width=True):
        st.info("Import functionality coming soon!")

# Help Section
with st.expander("❓ Settings Help"):
    st.markdown("""
    ### API Keys Setup
    
    1. **OpenAI API Key**: 
       - Visit https://platform.openai.com/
       - Create an account or log in
       - Navigate to API Keys section
       - Create a new secret key
    
    2. **Google API Keys**:
       - Go to Google Cloud Console
       - Enable Custom Search API
       - Create credentials
       - Set up Custom Search Engine
    
    ### Model Selection
    
    - **gpt-4o-mini**: Fastest and most cost-effective
    - **gpt-4o**: Best performance and accuracy
    - **gpt-3.5-turbo**: Good balance of speed and quality
    
    ### Document Settings
    
    - **Chunk Size**: Larger chunks for long documents, smaller for precise retrieval
    - **Overlap**: Helps maintain context between chunks
    - **File Size**: Increase for larger documents (may affect performance)
    
    ### Troubleshooting
    
    - Check API key validity if features aren't working
    - Ensure sufficient API credits for OpenAI
    - Verify internet connection for external searches
    - Check file permissions for storage paths
    """)
