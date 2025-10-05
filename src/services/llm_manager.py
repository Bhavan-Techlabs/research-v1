"""
LLM Manager Service
Supports multiple LLM providers using langchain's init_chat_model
Handles dynamic API key management and provider selection
"""

import os
from typing import Optional, Dict, Any, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models import init_chat_model
from config.settings import Settings


class LLMManager:
    """
    Manages multiple LLM providers with dynamic configuration
    Supports: OpenAI, Anthropic, Google, Azure, Cohere, and more
    """

    # Supported providers and their configuration
    SUPPORTED_PROVIDERS = {
        "openai": {
            "name": "OpenAI",
            "api_key_env": "OPENAI_API_KEY",
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "requires_api_key": True,
        },
        "anthropic": {
            "name": "Anthropic",
            "api_key_env": "ANTHROPIC_API_KEY",
            "models": [
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
            ],
            "requires_api_key": True,
        },
        "google-genai": {
            "name": "Google Gemini",
            "api_key_env": "GOOGLE_API_KEY",
            "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
            "requires_api_key": True,
        },
        "azure": {
            "name": "Azure OpenAI",
            "api_key_env": "AZURE_OPENAI_API_KEY",
            "models": ["custom"],  # User-defined deployment names
            "requires_api_key": True,
            "requires_endpoint": True,
        },
        "cohere": {
            "name": "Cohere",
            "api_key_env": "COHERE_API_KEY",
            "models": ["command-r-plus", "command-r", "command"],
            "requires_api_key": True,
        },
        "together": {
            "name": "Together AI",
            "api_key_env": "TOGETHER_API_KEY",
            "models": [
                "meta-llama/Llama-3-70b-chat-hf",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
            ],
            "requires_api_key": True,
        },
        "groq": {
            "name": "Groq",
            "api_key_env": "GROQ_API_KEY",
            "models": ["llama3-70b-8192", "mixtral-8x7b-32768"],
            "requires_api_key": True,
        },
    }

    def __init__(self):
        """Initialize LLM Manager"""
        self.credentials = {}
        self._load_credentials_from_env()

    def _load_credentials_from_env(self):
        """Load credentials from environment variables"""
        for provider, config in self.SUPPORTED_PROVIDERS.items():
            api_key_env = config.get("api_key_env")
            if api_key_env:
                api_key = os.getenv(api_key_env)
                if api_key:
                    self.credentials[provider] = {"api_key": api_key}

    def set_credentials(self, provider: str, api_key: str, **kwargs):
        """
        Set credentials for a provider

        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            api_key: API key for the provider
            **kwargs: Additional credentials (e.g., endpoint for Azure)
        """
        if provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")

        self.credentials[provider] = {"api_key": api_key, **kwargs}

    def get_credentials(self, provider: str) -> Dict[str, Any]:
        """Get credentials for a provider"""
        return self.credentials.get(provider, {})

    def is_provider_configured(self, provider: str) -> bool:
        """Check if a provider is configured"""
        creds = self.get_credentials(provider)
        return bool(creds.get("api_key"))

    def get_configured_providers(self) -> List[str]:
        """Get list of configured providers"""
        return [
            p for p in self.SUPPORTED_PROVIDERS.keys() if self.is_provider_configured(p)
        ]

    def get_available_models(self, provider: str) -> List[str]:
        """Get available models for a provider"""
        if provider not in self.SUPPORTED_PROVIDERS:
            return []
        return self.SUPPORTED_PROVIDERS[provider]["models"]

    def initialize_model(
        self,
        provider: str,
        model: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> BaseChatModel:
        """
        Initialize a chat model with specified provider and configuration

        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional model-specific parameters

        Returns:
            Initialized chat model

        Raises:
            ValueError: If provider is not configured or unsupported
        """
        if provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {provider}")

        if not self.is_provider_configured(provider):
            raise ValueError(
                f"Provider '{provider}' is not configured. Please set API key."
            )

        # Get credentials
        creds = self.get_credentials(provider)
        api_key = creds.get("api_key")

        # Prepare configuration
        config = {
            "temperature": temperature,
        }

        if max_tokens:
            config["max_tokens"] = max_tokens

        # Provider-specific configuration
        if provider == "azure":
            config["azure_endpoint"] = creds.get("endpoint")
            config["api_version"] = creds.get("api_version", "2024-02-15-preview")

        # Initialize model using init_chat_model
        try:
            llm = init_chat_model(
                model=model,
                model_provider=provider,
                api_key=api_key,
                **config,
                **kwargs,
            )
            return llm
        except Exception as e:
            raise ValueError(
                f"Failed to initialize {provider} model '{model}': {str(e)}"
            )

    def get_provider_info(self, provider: str) -> Dict[str, Any]:
        """Get information about a provider"""
        return self.SUPPORTED_PROVIDERS.get(provider, {})

    @staticmethod
    def get_all_providers() -> List[Dict[str, Any]]:
        """Get information about all supported providers"""
        return [
            {"id": provider_id, **provider_info}
            for provider_id, provider_info in LLMManager.SUPPORTED_PROVIDERS.items()
        ]


# Singleton instance
_llm_manager = None


def get_llm_manager() -> LLMManager:
    """Get singleton instance of LLM Manager"""
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager
