"""
OpenAI Service
Handles all interactions with OpenAI API using dynamic LLM Manager
"""

from typing import List, Dict, Optional
from openai import OpenAI
from src.services.llm_manager import get_llm_manager
from src.utils.credentials_manager import CredentialsManager
from config.settings import Settings


class OpenAIService:
    """Service for OpenAI API operations with multi-LLM support"""

    def __init__(self, provider: str, model_name: str, temperature: float = None):
        """
        Initialize OpenAI service with dynamic LLM support

        Args:
            provider: LLM provider name (e.g., 'openai', 'anthropic')
            model_name: Model to use
            temperature: Temperature for generation (defaults to Settings.DEFAULT_TEMPERATURE)
        """
        if not provider or not model_name:
            raise ValueError("Both provider and model_name are required parameters")

        self.provider = provider
        self.model_name = model_name
        self.temperature = (
            temperature if temperature is not None else Settings.DEFAULT_TEMPERATURE
        )

        # Get credentials and initialize LLM via LLM Manager
        llm_manager = get_llm_manager()
        creds = CredentialsManager.get_credential(provider)
        llm_manager.set_credentials(provider, **creds)

        # Initialize LLM with specified temperature
        self.llm = llm_manager.initialize_model(
            provider=provider, model_name=model_name, temperature=self.temperature
        )

        # Initialize OpenAI client for direct API calls (if provider is OpenAI)
        if provider.lower() == "openai":
            api_key = creds.get("api_key")
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                self.client = None
        else:
            self.client = None

    def chat_completion(
        self,
        messages: List[Dict],
        response_type: str = "text",
        temperature: float = None,
        max_tokens: int = None,
    ) -> str:
        """
        Call OpenAI chat completion API

        Args:
            messages: List of message dictionaries
            response_type: "text" or "json_object"
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            Response content string
        """
        if not self.client:
            raise ValueError(
                "OpenAI client not available. This method only works with OpenAI provider."
            )

        temperature = temperature if temperature is not None else self.temperature
        max_tokens = (
            max_tokens if max_tokens is not None else Settings.DEFAULT_MAX_TOKENS
        )

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": response_type},
        )
        return response.choices[0].message.content

    def simple_query(self, query: str) -> str:
        """
        Simple GPT query

        Args:
            query: The question or prompt

        Returns:
            AI response
        """
        ai_msg = self.llm.invoke(query)
        return ai_msg.content

    def structured_query(self, query: str, structure):
        """
        Query with structured output

        Args:
            query: The question or prompt
            structure: Output structure definition

        Returns:
            Structured response
        """
        structured_llm = self.llm.with_structured_output(structure, method="json_mode")
        return structured_llm.invoke(query)

    def analyze_paper(self, prompt: str) -> str:
        """
        Analyze a research paper with structured output

        Args:
            prompt: Analysis prompt with paper content

        Returns:
            JSON string with analysis results
        """
        return self.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
            response_type="json_object",
        )
