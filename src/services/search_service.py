"""
Search Service
Handles Google Search and DuckDuckGo search operations
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from src.services.llm_manager import get_llm_manager
from src.utils.credentials_manager import CredentialsManager
import os


class SearchService:
    """Service for general web search operations"""

    def __init__(self, provider: str, model_name: str):
        """
        Initialize Search service

        Args:
            provider: LLM provider (e.g., 'openai', 'anthropic')
            model_name: Model for agent operations
        """
        if not provider or not model_name:
            raise ValueError("Both provider and model_name are required")

        self.provider = provider
        self.model_name = model_name

        # Initialize LLM using LLM Manager
        llm_manager = get_llm_manager()
        creds = CredentialsManager.get_credential(provider)

        if not creds:
            raise ValueError(f"No credentials found for provider '{provider}'")

        llm_manager.set_credentials(provider, **creds)
        self.llm = llm_manager.initialize_model(
            provider=provider, model=model_name, temperature=0.0
        )

        # Initialize Google Search if API key and CSE ID are in environment
        # Note: Google Search is optional and uses environment variables
        if os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID"):
            self.search_api = GoogleSearchAPIWrapper()
        else:
            self.search_api = None

    def google_search(self, query: str) -> str:
        """
        Search Google for recent results

        Args:
            query: Search query

        Returns:
            Search results

        Raises:
            ValueError: If Google API not configured
        """
        if not self.search_api:
            raise ValueError(
                "Google API not configured. Please set GOOGLE_API_KEY and GOOGLE_CSE_ID."
            )

        tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=self.search_api.run,
        )
        return tool.run(query)

    def duckduckgo_search(self, query: str) -> str:
        """
        Search using DuckDuckGo

        Args:
            query: Search query

        Returns:
            Search results
        """
        tools = load_tools(["ddg-search"])
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=False, handle_parsing_errors=True
        )
        response = agent_executor.invoke({"input": query})
        return response["output"]
