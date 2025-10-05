"""
RAG System Module
Retrieval-Augmented Generation for document Q&A with multi-LLM support
"""

import os
from pathlib import Path
from typing import List, Optional
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.services.llm_manager import get_llm_manager
from src.utils.credentials_manager import CredentialsManager
from src.utils.document_utils import DocumentProcessor
from config.settings import Settings
from config.constants import DEFAULT_SEPARATORS


class RAGSystem:
    """
    Retrieval-Augmented Generation system for document Q&A with multi-LLM and embedding support
    """

    def __init__(
        self,
        provider: str,
        model: str,
        embedding_provider: str = None,
        embedding_model: str = None,
        temperature: float = 0,
        **kwargs
    ):
        """
        Initialize RAG System with multi-LLM support

        Args:
            provider: LLM provider (openai, anthropic, google-genai, etc.)
            model: Model name
            embedding_provider: Embedding provider (defaults to same as provider)
            embedding_model: Embedding model name (required if embeddings are needed)
            temperature: Temperature for generation
            **kwargs: Additional provider-specific parameters
        """
        if not provider or not model:
            raise ValueError("Both provider and model are required parameters")

        self.provider = provider
        self.model = model
        self.embedding_provider = embedding_provider or provider
        self.embedding_model = embedding_model
        self.temperature = temperature

        # Initialize LLM manager
        self.llm_manager = get_llm_manager()

        # Get credentials and set them
        creds = CredentialsManager.get_credential(provider)
        self.llm_manager.set_credentials(provider, **creds)

        # Initialize LLM
        self.llm = self.llm_manager.initialize_model(
            provider=provider, model_name=model, temperature=temperature
        )

        # Initialize embeddings if model specified
        self.embeddings = None
        if embedding_model:
            self._initialize_embeddings()

    def _initialize_embeddings(self):
        """Initialize embedding model based on provider"""
        embedding_creds = CredentialsManager.get_credential(self.embedding_provider)

        if self.embedding_provider.lower() == "openai":
            from langchain_openai import OpenAIEmbeddings

            api_key = embedding_creds.get("api_key")
            self.embeddings = OpenAIEmbeddings(
                model=self.embedding_model, openai_api_key=api_key
            )
        elif self.embedding_provider.lower() in ["cohere"]:
            from langchain_cohere import CohereEmbeddings

            api_key = embedding_creds.get("api_key")
            self.embeddings = CohereEmbeddings(
                model=self.embedding_model, cohere_api_key=api_key
            )
        elif self.embedding_provider.lower() in ["google-genai", "google"]:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings

            api_key = embedding_creds.get("api_key")
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=self.embedding_model, google_api_key=api_key
            )
        else:
            # Fallback to OpenAI for unknown providers
            from langchain_openai import OpenAIEmbeddings

            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)

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
        if not self.embeddings:
            raise ValueError(
                "Embedding model not initialized. Please provide embedding_model in constructor."
            )

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
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=persist_directory,
        )

        return vector_store.as_retriever()

    def create_retriever_from_paths(
        self,
        doc_paths: List[str],
        chunk_size: int = None,
        chunk_overlap: int = None,
        separators: List[str] = None,
        collection_name: str = "rag_collection",
        persist_directory: str = None,
    ):
        """
        Create a retriever from multiple document paths

        Args:
            doc_paths: List of document paths
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            separators: List of separators for text splitting
            collection_name: Name for the ChromaDB collection
            persist_directory: Directory to persist the vector store

        Returns:
            A retriever object
        """
        if not self.embeddings:
            raise ValueError(
                "Embedding model not initialized. Please provide embedding_model in constructor."
            )

        chunk_size = chunk_size or Settings.DEFAULT_CHUNK_SIZE
        chunk_overlap = chunk_overlap or Settings.DEFAULT_CHUNK_OVERLAP
        separators = separators or DEFAULT_SEPARATORS
        persist_directory = persist_directory or str(Settings.CHROMADB_DIR)

        # Load all documents
        all_documents = []
        for doc_path in doc_paths:
            documents = DocumentProcessor.load_documents_from_path(doc_path)
            all_documents.extend(documents)

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
        )

        # Create vector store
        vector_store = Chroma.from_documents(
            documents=text_splitter.split_documents(all_documents),
            embedding=self.embeddings,
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
