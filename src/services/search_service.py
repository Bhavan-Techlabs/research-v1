"""
Search Service
Handles Google Search and DuckDuckGo search operations
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain import hub
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_openai import ChatOpenAI
from config.settings import Settings


class SearchService:
    """Service for general web search operations"""

    def __init__(self, model_name: str = None):
        """
        Initialize Search service

        Args:
            model_name: Model for agent operations
        """
        self.model_name = model_name or Settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(model=self.model_name)

        # Initialize Google Search if configured
        if Settings.is_google_configured():
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
