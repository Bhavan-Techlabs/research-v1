"""
Core Research Application Module
Consolidates all research-related functionality from the original research.py
"""

import os
from io import BytesIO
from typing import List, Optional
import json

import fitz
import requests
import tiktoken
from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
    create_react_agent,
)
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.document_loaders import ArxivLoader, PyMuPDFLoader
from langchain_community.retrievers import ArxivRetriever
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from scidownl import scihub_download


class ResearchPaperRetriever(BaseRetriever):
    """Custom retriever for loading research papers from a storage folder"""

    storage_folder_path: str

    def _load_research_paper(self, file_name: str) -> List[Document]:
        """Load a research paper using PyMuPDFLoader"""
        file_path = f"{self.storage_folder_path}/{file_name}"
        loader = PyMuPDFLoader(file_path)
        return loader.load()

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Get relevant documents based on the query (filename)"""
        return self._load_research_paper(query)


class ResearchApp:
    """
    Main Research Application Class
    Provides comprehensive research tools including:
    - Multi-source search (Google, ArXiv, Semantic Scholar, DuckDuckGo)
    - Document processing (PDF, Web, HTML)
    - AI-powered analysis
    - RAG system integration
    """

    def __init__(
        self, model_name: str = "gpt-4o-mini", storage_folder_path: str = None
    ):
        """
        Initialize the Research Application

        Args:
            model_name: OpenAI model to use (default: gpt-4o-mini)
            storage_folder_path: Path to store/retrieve research papers
        """
        self.model_name = model_name
        self.storage_folder_path = storage_folder_path

        # Initialize APIs and models
        self.search_api = GoogleSearchAPIWrapper()
        self.client = OpenAI()
        self.llm = ChatOpenAI(model=model_name)

        # Initialize retriever if storage path is provided
        if storage_folder_path:
            self.retriever = ResearchPaperRetriever(
                storage_folder_path=storage_folder_path
            )
        else:
            self.retriever = None

    # ============================================================================
    # AI SEARCH METHODS
    # ============================================================================

    def gpt_search(self, query: str) -> str:
        """Perform a simple GPT search"""
        ai_msg = self.llm.invoke(query)
        return ai_msg.content

    def gpt_search_with_structure(self, query: str, structure):
        """Perform GPT search with structured output"""
        structured_llm = self.llm.with_structured_output(structure, method="json_mode")
        ai_msg = structured_llm.invoke(query)
        return ai_msg

    def google_search(self, query: str) -> str:
        """Search Google for recent results"""
        tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=self.search_api.run,
        )
        return tool.run(query)

    def ddg_search(self, query: str) -> str:
        """Search using DuckDuckGo"""
        tools = load_tools(["ddg-search"])
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=False, handle_parsing_errors=True
        )
        response = agent_executor.invoke({"input": query})
        return response["output"]

    def semantic_search_agent(self, query: str) -> str:
        """Search using Semantic Scholar"""
        instructions = "You are an expert researcher."
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        prompt = base_prompt.partial(instructions=instructions)
        tools = [SemanticScholarQueryRun()]
        agent = create_openai_functions_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=False, handle_parsing_errors=True
        )
        result = agent_executor.invoke({"input": query})
        return str(result["output"])

    def arxiv_search_agent(self, query: str) -> str:
        """Search ArXiv using an agent"""
        tools = load_tools(["arxiv"])
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=False, handle_parsing_errors=True
        )
        result = agent_executor.invoke({"input": query})
        return str(result["output"])

    # ============================================================================
    # ARXIV METHODS
    # ============================================================================

    def arxiv_load_documents_from_query(
        self, query: str, load_max_docs: int = 10, load_all_available_meta: bool = True
    ) -> str:
        """Load documents from ArXiv based on query"""
        loader = ArxivLoader(
            query=query,
            load_max_docs=load_max_docs,
            load_all_available_meta=load_all_available_meta,
        )
        docs = loader.load()
        text = ""
        for doc in docs:
            text += f"{doc.metadata.get('Title', 'No Title')} | {doc.metadata.get('entry_id', 'No ID')}\n\n"
        return text

    def arxiv_load_document_from_id(self, paper_id: str, load_max_docs: int = 2) -> str:
        """Load specific ArXiv document by ID"""
        retriever = ArxivRetriever(load_max_docs=load_max_docs)
        docs = retriever.invoke(paper_id)
        text = ""
        for doc in docs:
            text += f"{doc.page_content}\n\n"
        return text

    # ============================================================================
    # DOCUMENT PROCESSING METHODS
    # ============================================================================

    def extract_text_from_pdf(self, pdf_file: BytesIO) -> str:
        """Extract text from PDF file"""
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text

    def extract_text_from_html(self, url: str) -> str:
        """Extract text from HTML webpage"""
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return " ".join([p.get_text() for p in soup.find_all("p")])

    def extract_text_from_url(self, url: str) -> str:
        """Extract text from URL (handles both PDF and HTML)"""
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").lower()

        if "application/pdf" in content_type:
            pdf_file = BytesIO(response.content)
            return self.extract_text_from_pdf(pdf_file)
        else:
            return self.extract_text_from_html(url)

    def get_full_content(self, selected_file: str) -> str:
        """Get full content from a stored research paper"""
        if not self.retriever:
            raise ValueError("Storage folder path not configured")

        documents = self.retriever._load_research_paper(selected_file)
        page_contents = [doc.page_content for doc in documents]
        full_content = " ".join(page_contents)
        return full_content

    def get_all_papers(self, pdf_file_path: str) -> List[str]:
        """Get list of all papers in a directory"""
        return os.listdir(pdf_file_path)

    # ============================================================================
    # AI ANALYSIS METHODS
    # ============================================================================

    def openai_chat_completion(
        self, messages: List[dict], response_type: str = "text"
    ) -> str:
        """Call OpenAI chat completion API"""
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0,
            max_tokens=16383,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": response_type},
        )
        return response.choices[0].message.content

    def extract_research_paper_info(self, prompt: str) -> str:
        """Extract research paper information using structured output"""
        return self.openai_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
            response_type="json_object",
        )

    # ============================================================================
    # TOKEN MANAGEMENT
    # ============================================================================

    def num_tokens_from_string(self, string: str, encoding_name: str = None) -> int:
        """Calculate number of tokens in a string"""
        if encoding_name is None:
            encoding_name = self.model_name
        encoding = tiktoken.encoding_for_model(encoding_name)
        return len(encoding.encode(string))

    def get_optimized_final_prompt(
        self, base_prompt: str, pdf_filename: str, max_token_limit: int = 100000
    ) -> str:
        """
        Get an optimized prompt by truncating content if needed

        Args:
            base_prompt: The base prompt template with {full_paper} placeholder
            pdf_filename: Name of the PDF file to analyze
            max_token_limit: Maximum tokens allowed

        Returns:
            Optimized prompt with paper content
        """
        full_text = self.get_full_content(pdf_filename)
        paper_token_count = self.num_tokens_from_string(full_text)

        if paper_token_count > max_token_limit:
            encoding = tiktoken.encoding_for_model(self.model_name)
            encoded_tokens = encoding.encode(full_text)[:max_token_limit]
            full_text = encoding.decode(encoded_tokens)

        final_prompt = base_prompt.replace("{full_paper}", full_text)
        return final_prompt

    # ============================================================================
    # RAG SYSTEM METHODS
    # ============================================================================

    def get_retriever(
        self,
        doc_path: str,
        embedding_model: str = "text-embedding-3-large",
        chunk_size: int = 10000,
        chunk_overlap: int = 200,
        separators: List[str] = None,
        collection_name: str = "rag_collection",
        persist_directory: str = "./chromadb",
    ):
        """
        Create a retriever from a document

        Args:
            doc_path: Path to the document
            embedding_model: OpenAI embedding model to use
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            separators: List of separators for text splitting
            collection_name: Name for the ChromaDB collection
            persist_directory: Directory to persist the vector store

        Returns:
            A retriever object
        """
        if separators is None:
            separators = ["\n---\n", "\n\n", "\n", " "]

        # Determine file type and load
        file_extension = os.path.splitext(doc_path)[1]

        if file_extension == ".pdf":
            loader = PyMuPDFLoader(doc_path)
        else:
            from langchain_community.document_loaders import TextLoader

            loader = TextLoader(doc_path)

        documents = loader.load()

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
        )

        # Create vector store
        vector_store = Chroma.from_documents(
            documents=text_splitter.split_documents(documents),
            embedding=OpenAIEmbeddings(model=embedding_model),
            collection_name=collection_name,
            persist_directory=persist_directory,
        )

        return vector_store.as_retriever()

    def create_rag_system(self, retriever, prompt: str, query: str) -> str:
        """
        Create and run a RAG system

        Args:
            retriever: The retriever object
            prompt: The prompt hub path (e.g., "rlm/rag-prompt")
            query: The user query

        Returns:
            The RAG system response
        """

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | hub.pull(prompt)
            | self.llm
            | StrOutputParser()
        )

        return rag_chain.invoke(query)

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def download_scihub_pdf(self, doi: str, base_directory: str = "./scihub/") -> str:
        """Download PDF from Sci-Hub"""
        paper_url = f"https://doi.org/{doi}"
        out_filename = f"paper_{doi.replace('/', '-')}.pdf"
        out_path = base_directory + out_filename

        try:
            scihub_download(
                paper_url,
                paper_type="doi",
                out=out_path,
                proxies={"http": "socks5://127.0.0.1:7890"},
            )
            return f"Downloaded: {doi} to {out_path}"
        except Exception as e:
            return f"Failed to download {doi}: {e}"