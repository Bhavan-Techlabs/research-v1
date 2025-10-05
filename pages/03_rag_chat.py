"""
RAG Chat Page
Chat with your research documents using multi-LLM support
"""

import streamlit as st
from pathlib import Path
import tempfile
from src.core.rag_system import RAGSystem
from src.utils.credentials_manager import CredentialsManager, LLMConfigWidget
from src.utils.session_manager import SessionStateManager
from src.utils.document_utils import DocumentProcessor

# Page configuration
st.set_page_config(page_title="RAG Chat", page_icon="💬", layout="wide")

st.title("💬 Chat with Research Documents")
st.markdown(
    "Upload documents and ask questions using RAG (Retrieval-Augmented Generation)"
)

# Initialize
CredentialsManager.initialize()
SessionStateManager.initialize()

# Check if any LLM is configured
configured_providers = CredentialsManager.get_configured_providers()
if not configured_providers:
    st.warning(
        "⚠️ No LLM providers configured. Please configure at least one provider in Settings."
    )
    if st.button("Go to Settings"):
        st.switch_page("pages/05_settings.py")
    st.stop()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # LLM Selection
    provider, model = LLMConfigWidget.render_model_selector(default_provider="openai")

    if not provider or not model:
        st.error("Please select a valid provider and model")
        st.stop()

    st.divider()

    # RAG settings
    st.subheader("🔧 RAG Settings")

    chunk_size = st.slider(
        "Chunk Size",
        min_value=500,
        max_value=2000,
        value=1000,
        step=100,
        help="Size of text chunks for retrieval",
    )

    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=0,
        max_value=500,
        value=200,
        step=50,
        help="Overlap between chunks",
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Higher values make responses more creative",
    )

    st.divider()

    # Document management
    st.subheader("📄 Documents")

    if SessionStateManager.get("rag_documents"):
        docs = SessionStateManager.get("rag_documents", [])
        st.success(f"✅ {len(docs)} document(s) loaded")

        if st.button("🗑️ Clear Documents", use_container_width=True):
            SessionStateManager.set("rag_documents", [])
            SessionStateManager.set("rag_retriever", None)
            SessionStateManager.set("rag_chat_history", [])
            st.rerun()
    else:
        st.info("No documents loaded")

# Main content
tab1, tab2 = st.tabs(["📤 Upload & Chat", "📜 Chat History"])

with tab1:
    # Document upload
    st.subheader("Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF or Text files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        help="Upload research papers, articles, or notes",
    )

    if uploaded_files:
        if st.button("📚 Process Documents", type="primary"):
            with st.spinner("Processing documents..."):
                try:
                    # Save files temporarily
                    temp_dir = Path(tempfile.mkdtemp())
                    doc_paths = []

                    for uploaded_file in uploaded_files:
                        temp_path = temp_dir / uploaded_file.name
                        temp_path.write_bytes(uploaded_file.getvalue())
                        doc_paths.append(str(temp_path))

                    # Get credentials
                    api_key = CredentialsManager.get_api_key(provider)
                    creds = CredentialsManager.get_credential(provider)

                    # Create RAG system
                    rag = RAGSystem(
                        provider=provider,
                        model=model,
                        api_key=api_key,
                        **{k: v for k, v in creds.items() if k != "api_key"},
                    )

                    # Create retriever from multiple documents
                    retriever = rag.create_retriever_from_paths(
                        doc_paths, chunk_size=chunk_size, chunk_overlap=chunk_overlap
                    )

                    # Store in session
                    SessionStateManager.set(
                        "rag_documents", [f.name for f in uploaded_files]
                    )
                    SessionStateManager.set("rag_retriever", retriever)
                    SessionStateManager.set("rag_chat_history", [])

                    st.success(f"✅ Processed {len(uploaded_files)} documents!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")

    st.divider()

    # Chat interface
    st.subheader("💬 Ask Questions")

    # Check if documents are loaded
    if not SessionStateManager.get("rag_retriever"):
        st.info("👆 Please upload and process documents first")
    else:
        # Display chat history
        chat_history = SessionStateManager.get("rag_chat_history", [])

        for message in chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message
            chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Get retriever
                        retriever = SessionStateManager.get("rag_retriever")

                        # Get credentials
                        api_key = CredentialsManager.get_api_key(provider)
                        creds = CredentialsManager.get_credential(provider)

                        # Create RAG system
                        rag = RAGSystem(
                            provider=provider,
                            model=model,
                            api_key=api_key,
                            temperature=temperature,
                            **{k: v for k, v in creds.items() if k != "api_key"},
                        )

                        # Query
                        response = rag.query(retriever, prompt)

                        st.markdown(response)

                        # Add to history
                        chat_history.append({"role": "assistant", "content": response})
                        SessionStateManager.set("rag_chat_history", chat_history)

                        # Update counter
                        SessionStateManager.increment_counter("chat_messages")

                    except Exception as e:
                        error_msg = f"Error generating response: {str(e)}"
                        st.error(error_msg)
                        chat_history.append({"role": "assistant", "content": error_msg})
                        SessionStateManager.set("rag_chat_history", chat_history)

with tab2:
    st.subheader("📜 Chat History")

    chat_history = SessionStateManager.get("rag_chat_history", [])

    if not chat_history:
        st.info("No chat history yet. Start chatting to see messages here.")
    else:
        # Export button
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear History"):
                SessionStateManager.set("rag_chat_history", [])
                st.rerun()

        # Display history
        for idx, message in enumerate(chat_history):
            with st.expander(
                f"{'👤 You' if message['role'] == 'user' else '🤖 Assistant'} - Message {idx + 1}",
                expanded=False,
            ):
                st.markdown(message["content"])

        # Export chat
        chat_text = "\n\n".join(
            [
                f"{'USER' if m['role'] == 'user' else 'ASSISTANT'}: {m['content']}"
                for m in chat_history
            ]
        )

        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name="rag_chat_history.txt",
            mime="text/plain",
            use_container_width=True,
        )

# Footer
st.divider()
st.markdown(
    """
### 💡 Tips
- **Upload Multiple Documents**: Combine papers, articles, and notes for comprehensive answers
- **Ask Specific Questions**: Get better results with clear, focused questions
- **Chunk Size**: Larger chunks preserve context, smaller chunks improve retrieval precision
- **Temperature**: Lower values (0-0.3) for factual answers, higher (0.7-1.0) for creative responses
"""
)
