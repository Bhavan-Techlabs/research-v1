"""
RAG System Module
Retrieval-Augmented Generation for document Q&A with multi-LLM support
"""

from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.services.llm_manager import get_llm_manager
from src.utils.document_utils import DocumentProcessor
from config.settings import Settings


class RAGSystem:
    """
    Retrieval-Augmented Generation system for document Q&A with multi-LLM support
    """

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        temperature: float = 0,
        **kwargs
    ):
        """
        Initialize RAG System with multi-LLM support

        Args:
            provider: LLM provider (openai, anthropic, google-genai, etc.)
            model: Model name
            api_key: API key for the provider
            temperature: Temperature for generation
            **kwargs: Additional provider-specific parameters
        """
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.settings = Settings()

        # Initialize LLM manager
        self.llm_manager = get_llm_manager()

        # Set credentials if provided
        if api_key:
            self.llm_manager.set_credentials(provider, api_key, **kwargs)


import os
from typing import List
from pathlib import Path
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import Settings
from config.constants import DEFAULT_SEPARATORS
from src.utils.document_utils import DocumentProcessor


class RAGSystem:
    """Retrieval Augmented Generation system"""

    def __init__(self, model_name: str = None, embedding_model: str = None):
        """
        Initialize RAG System

        Args:
            model_name: LLM model name
            embedding_model: Embedding model name
        """
        self.model_name = model_name or Settings.DEFAULT_MODEL
        self.embedding_model = embedding_model or Settings.DEFAULT_EMBEDDING_MODEL
        self.llm = ChatOpenAI(model=self.model_name)

    def create_retriever(
        self,
        doc_path: str,
        chunk_size: int = None,
        chunk_overlap: int = None,
        separators: List[str] = None,
        collection_name: str = "rag_collection",
        persist_directory: str = None,
    ):
        """
        Create a retriever from a document

        Args:
            doc_path: Path to the document
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            separators: List of separators for text splitting
            collection_name: Name for the ChromaDB collection
            persist_directory: Directory to persist the vector store

        Returns:
            A retriever object
        """
        chunk_size = chunk_size or Settings.DEFAULT_CHUNK_SIZE
        chunk_overlap = chunk_overlap or Settings.DEFAULT_CHUNK_OVERLAP
        separators = separators or DEFAULT_SEPARATORS
        persist_directory = persist_directory or str(Settings.CHROMADB_DIR)

        # Load documents
        documents = DocumentProcessor.load_documents_from_path(doc_path)

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
        )

        # Create vector store
        vector_store = Chroma.from_documents(
            documents=text_splitter.split_documents(documents),
            embedding=OpenAIEmbeddings(model=self.embedding_model),
            collection_name=collection_name,
            persist_directory=persist_directory,
        )

        return vector_store.as_retriever()

    def query(
        self, retriever, query: str, prompt_hub_path: str = "rlm/rag-prompt"
    ) -> str:
        """
        Query the RAG system

        Args:
            retriever: The retriever object
            query: User query
            prompt_hub_path: LangChain hub prompt path

        Returns:
            Response from RAG system
        """

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | hub.pull(prompt_hub_path)
            | self.llm
            | StrOutputParser()
        )

        return rag_chain.invoke(query)
