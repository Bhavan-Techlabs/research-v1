"""
Semantic Scholar Service
Handles interactions with Semantic Scholar API
"""

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.tools.semanticscholar.tool import SemanticScholarQueryRun
from langchain import hub
from src.services.llm_manager import get_llm_manager
from src.utils.credentials_manager import CredentialsManager


class SemanticScholarService:
    """Service for Semantic Scholar operations"""

    def __init__(self, provider: str, model_name: str):
        """
        Initialize Semantic Scholar service

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
