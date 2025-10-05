"""
ArXiv Service
Handles all interactions with ArXiv API for paper search and retrieval
"""

from typing import List
from langchain_community.document_loaders import ArxivLoader
from langchain_community.retrievers import ArxivRetriever
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain_openai import ChatOpenAI
from config.settings import Settings


class ArxivService:
    """Service for ArXiv operations"""

    def __init__(self, model_name: str = None):
        """
        Initialize ArXiv service

        Args:
            model_name: Model for agent operations
        """
        self.model_name = model_name or Settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(model=self.model_name)

    def search_with_agent(self, query: str) -> str:
        """
        Search ArXiv using an agent

        Args:
            query: Search query

        Returns:
            Formatted search results
        """
        tools = load_tools(["arxiv"])
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=False, handle_parsing_errors=True
        )
        result = agent_executor.invoke({"input": query})
        return str(result["output"])

    def load_documents_from_query(
        self, query: str, max_docs: int = 10, load_all_meta: bool = True
    ) -> str:
        """
        Load documents from ArXiv based on query

        Args:
            query: Search query
            max_docs: Maximum documents to load
            load_all_meta: Whether to load all available metadata

        Returns:
            Formatted document information
        """
        loader = ArxivLoader(
            query=query,
            load_max_docs=max_docs,
            load_all_available_meta=load_all_meta,
        )
        docs = loader.load()

        text = ""
        for doc in docs:
            title = doc.metadata.get("Title", "No Title")
            entry_id = doc.metadata.get("entry_id", "No ID")
            text += f"{title} | {entry_id}\n\n"
        return text

    def load_document_by_id(self, paper_id: str, max_docs: int = 2) -> str:
        """
        Load specific ArXiv document by ID

        Args:
            paper_id: ArXiv paper ID
            max_docs: Maximum documents to load

        Returns:
            Document content
        """
        retriever = ArxivRetriever(load_max_docs=max_docs)
        docs = retriever.invoke(paper_id)

        text = ""
        for doc in docs:
            text += f"{doc.page_content}\n\n"
        return text
