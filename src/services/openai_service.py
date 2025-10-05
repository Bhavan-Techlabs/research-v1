"""
OpenAI Service
Handles all interactions with OpenAI API
"""

from typing import List, Dict, Optional
from openai import OpenAI
from langchain_openai import ChatOpenAI
from config.settings import Settings


class OpenAIService:
    """Service for OpenAI API operations"""

    def __init__(self, model_name: str = None):
        """
        Initialize OpenAI service

        Args:
            model_name: Model to use (defaults to Settings.DEFAULT_MODEL)
        """
        self.model_name = model_name or Settings.DEFAULT_MODEL
        self.client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        self.llm = ChatOpenAI(model=self.model_name)

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
        temperature = (
            temperature if temperature is not None else Settings.DEFAULT_TEMPERATURE
        )
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
