"""
RAG System Module - Multi-LLM Support
Retrieval-Augmented Generation for document Q&A with multi-LLM support
"""

from pathlib import Path
from typing import List, Optional
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
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

    def create_retriever(
        self, doc_path: str, chunk_size: int = 1000, chunk_overlap: int = 200
    ):
        """
        Create a retriever from a document

        Args:
            doc_path: Path to document
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            Retriever object
        """
        # Load documents
        documents = DocumentProcessor.load_documents_from_path(doc_path)

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        splits = text_splitter.split_documents(documents)

        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )

        # Create retriever
        retriever = vectorstore.as_retriever()

        return retriever

    def create_retriever_from_paths(
        self, doc_paths: List[str], chunk_size: int = 1000, chunk_overlap: int = 200
    ):
        """
        Create a retriever from multiple documents

        Args:
            doc_paths: List of document paths
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            Retriever object
        """
        all_documents = []

        for doc_path in doc_paths:
            documents = DocumentProcessor.load_documents_from_path(doc_path)
            all_documents.extend(documents)

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        splits = text_splitter.split_documents(all_documents)

        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=splits, embedding=OpenAIEmbeddings()
        )

        # Create retriever
        retriever = vectorstore.as_retriever()

        return retriever

    def query(
        self, retriever, query: str, prompt_hub_path: str = "rlm/rag-prompt"
    ) -> str:
        """
        Query the RAG system

        Args:
            retriever: Retriever object
            query: Query string
            prompt_hub_path: LangChain hub prompt path

        Returns:
            Answer string
        """
        # Initialize LLM
        llm = self.llm_manager.initialize_model(
            provider=self.provider, model=self.model, temperature=self.temperature
        )

        # Get retrieval QA chain prompt
        retrieval_qa_chat_prompt = hub.pull(prompt_hub_path)

        # Create chain
        from langchain.chains import create_retrieval_chain
        from langchain.chains.combine_documents import create_stuff_documents_chain

        combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        # Query
        result = retrieval_chain.invoke({"input": query})

        return result["answer"]
