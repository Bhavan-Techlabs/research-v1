"""
Semantic Scholar Service
Handles interactions with Semantic Scholar API
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from langchain import hub
from langchain_openai import ChatOpenAI
from config.settings import Settings


class SemanticScholarService:
    """Service for Semantic Scholar operations"""

    def __init__(self, model_name: str = None):
        """
        Initialize Semantic Scholar service

        Args:
            model_name: Model for agent operations
        """
        self.model_name = model_name or Settings.DEFAULT_MODEL
        self.llm = ChatOpenAI(model=self.model_name)

    def search(self, query: str) -> str:
        """
        Search using Semantic Scholar

        Args:
            query: Search query

        Returns:
            Search results
        """
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
