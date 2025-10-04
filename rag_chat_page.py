"""RAG Chat System Page - Question answering over research documents"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from core.research_app import ResearchApp
except ImportError:
    st.error("⚠️ Research app dependencies not installed. Please run: pip install -r requirements.txt")
    st.stop()

st.title("🤖 RAG Chat System")
st.markdown("Ask questions about your research documents using AI-powered retrieval")

# Initialize session state
if "rag_retriever" not in st.session_state:
    st.session_state.rag_retriever = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = []

# Sidebar configuration
with st.sidebar:
    st.header("RAG Configuration")

    # Model selection
    model = st.selectbox(
        "AI Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0
    )

    # Vector store settings
    with st.expander("Vector Store Settings"):
        chunk_size = st.slider("Chunk Size", 500, 2000, 1000)
        chunk_overlap = st.slider("Chunk Overlap", 50, 500, 200)

    # Document stats
    st.markdown("---")
    st.subheader("Document Stats")
    st.metric("Documents Loaded", len(st.session_state.documents_loaded))
    st.metric("Chat Messages", len(st.session_state.chat_history))

    # Clear buttons
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🗑️ Clear Documents", use_container_width=True):
        st.session_state.documents_loaded = []
        st.session_state.rag_retriever = None
        st.rerun()

# Document upload section
st.subheader("📚 Document Management")

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload research papers to add to the knowledge base",
)

if uploaded_files and st.button("📤 Process Documents"):
    try:
        research_app = ResearchApp(model_name=model)
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Save all files temporarily and create retriever
        temp_files = []
        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Save file temporarily
            temp_path = Path(f"./temp_{uploaded_file.name}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            temp_files.append(temp_path)
            
            progress_bar.progress((idx + 1) / len(uploaded_files))

        # Create retriever for the first document (you could combine multiple)
        if temp_files:
            st.session_state.rag_retriever = research_app.get_retriever(
                doc_path=str(temp_files[0]),
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                collection_name="research_collection",
            )
            
            # Store document names
            st.session_state.documents_loaded = [f.name for f in uploaded_files]

        # Clean up temp files
        for temp_path in temp_files:
            if temp_path.exists():
                temp_path.unlink()

        progress_bar.empty()
        status_text.empty()
        st.success(f"✅ Processed {len(uploaded_files)} documents!")
        st.rerun()

    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")

# Chat interface
if st.session_state.rag_retriever:
    st.markdown("---")
    st.subheader("💬 Chat with Documents")

    # Display loaded documents
    if st.session_state.documents_loaded:
        st.info(f"📚 Loaded documents: {', '.join(st.session_state.documents_loaded)}")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                try:
                    research_app = ResearchApp(model_name=model)
                    
                    # Create RAG response
                    response = research_app.create_rag_system(
                        retriever=st.session_state.rag_retriever,
                        prompt="rlm/rag-prompt",
                        query=prompt
                    )
                    
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": response
                    })

                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": error_msg
                    })

    # Example questions
    st.markdown("**💡 Try asking:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("What are the main findings?", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user", 
                "content": "What are the main findings of these papers?"
            })
            st.rerun()
    with col2:
        if st.button("What methodology was used?", use_container_width=True):
            st.session_state.chat_history.append({
                "role": "user", 
                "content": "What research methodology was used in these studies?"
            })
            st.rerun()

else:
    st.info("👆 Upload some documents first to start chatting!")

# Help section
with st.expander("ℹ️ How to Use RAG Chat"):
    st.markdown(
        """
    ### RAG Chat System Guide
    
    1. **Upload Documents**: Add PDF files to your knowledge base
    2. **Configure Settings**: Adjust chunk size and other parameters in sidebar
    3. **Start Chatting**: Ask questions about your uploaded documents
    4. **Review Responses**: Get AI-powered answers based on document content
    
    ### Features
    
    - **Intelligent Chunking**: Documents are split into optimal chunks for retrieval
    - **Semantic Search**: Find relevant information even with different wording
    - **Chat History**: Maintain conversation context across multiple queries
    - **Multi-Document Support**: Search across multiple uploaded documents
    
    ### Tips
    
    - Upload related documents to build a comprehensive knowledge base
    - Use specific questions for better results
    - Adjust chunk size based on your document types
    - Clear chat history to start fresh conversations
    """
    )
