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
        "azure_openai": {
            "name": "Azure OpenAI",
            "api_key_env": "AZURE_OPENAI_API_KEY",
            "models": ["custom"],  # User-defined deployment names
            "requires_api_key": True,
            "requires_endpoint": True,
            "extra_env": ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_VERSION"],
        },
        "azure_ai": {
            "name": "Azure AI",
            "api_key_env": "AZURE_AI_API_KEY",
            "models": ["custom"],
            "requires_api_key": True,
            "requires_endpoint": True,
        },
        "google_vertexai": {
            "name": "Google Vertex AI",
            "api_key_env": "GOOGLE_APPLICATION_CREDENTIALS",
            "models": ["gemini-1.5-pro", "gemini-1.5-flash", "text-bison@002"],
            "requires_api_key": False,
            "requires_project": True,
            "extra_env": ["GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION"],
        },
        "google_genai": {
            "name": "Google Gemini",
            "api_key_env": "GOOGLE_API_KEY",
            "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
            "requires_api_key": True,
        },
        "google_anthropic_vertex": {
            "name": "Anthropic via Google Vertex AI",
            "api_key_env": "GOOGLE_APPLICATION_CREDENTIALS",
            "models": [
                "claude-3-5-sonnet@20240620",
                "claude-3-opus@20240229",
                "claude-3-haiku@20240307",
            ],
            "requires_api_key": False,
            "requires_project": True,
        },
        "bedrock": {
            "name": "AWS Bedrock",
            "api_key_env": "AWS_ACCESS_KEY_ID",
            "models": [
                "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "anthropic.claude-3-sonnet-20240229-v1:0",
                "meta.llama3-70b-instruct-v1:0",
                "mistral.mistral-large-2402-v1:0",
            ],
            "requires_api_key": True,
            "extra_env": ["AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        },
        "bedrock_converse": {
            "name": "AWS Bedrock Converse",
            "api_key_env": "AWS_ACCESS_KEY_ID",
            "models": [
                "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "anthropic.claude-3-sonnet-20240229-v1:0",
            ],
            "requires_api_key": True,
            "extra_env": ["AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        },
        "cohere": {
            "name": "Cohere",
            "api_key_env": "COHERE_API_KEY",
            "models": ["command-r-plus", "command-r", "command"],
            "requires_api_key": True,
        },
        "fireworks": {
            "name": "Fireworks AI",
            "api_key_env": "FIREWORKS_API_KEY",
            "models": [
                "accounts/fireworks/models/llama-v3p1-70b-instruct",
                "accounts/fireworks/models/mixtral-8x7b-instruct",
            ],
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
        "mistralai": {
            "name": "Mistral AI",
            "api_key_env": "MISTRAL_API_KEY",
            "models": [
                "mistral-large-latest",
                "mistral-medium-latest",
                "mistral-small-latest",
            ],
            "requires_api_key": True,
        },
        "huggingface": {
            "name": "HuggingFace",
            "api_key_env": "HUGGINGFACEHUB_API_TOKEN",
            "models": [
                "HuggingFaceH4/zephyr-7b-beta",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
            ],
            "requires_api_key": True,
        },
        "groq": {
            "name": "Groq",
            "api_key_env": "GROQ_API_KEY",
            "models": [
                "llama-3.1-70b-versatile",
                "llama3-70b-8192",
                "mixtral-8x7b-32768",
            ],
            "requires_api_key": True,
        },
        "ollama": {
            "name": "Ollama",
            "api_key_env": None,
            "models": ["llama3", "mistral", "codellama", "phi3"],
            "requires_api_key": False,
            "requires_base_url": True,
            "default_base_url": "http://localhost:11434",
        },
        "deepseek": {
            "name": "DeepSeek",
            "api_key_env": "DEEPSEEK_API_KEY",
            "models": ["deepseek-chat", "deepseek-coder"],
            "requires_api_key": True,
        },
        "ibm": {
            "name": "IBM watsonx.ai",
            "api_key_env": "IBM_API_KEY",
            "models": [
                "ibm/granite-13b-chat-v2",
                "meta-llama/llama-3-70b-instruct",
            ],
            "requires_api_key": True,
            "extra_env": ["IBM_CLOUD_URL", "IBM_PROJECT_ID"],
        },
        "nvidia": {
            "name": "NVIDIA AI",
            "api_key_env": "NVIDIA_API_KEY",
            "models": [
                "meta/llama3-70b-instruct",
                "mistralai/mixtral-8x7b-instruct-v0.1",
            ],
            "requires_api_key": True,
        },
        "xai": {
            "name": "xAI (Grok)",
            "api_key_env": "XAI_API_KEY",
            "models": ["grok-beta", "grok-vision-beta"],
            "requires_api_key": True,
        },
        "perplexity": {
            "name": "Perplexity AI",
            "api_key_env": "PERPLEXITY_API_KEY",
            "models": [
                "llama-3.1-sonar-large-128k-online",
                "llama-3.1-sonar-small-128k-online",
            ],
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
            creds = {}

            # Load API key if required
            if api_key_env:
                api_key = os.getenv(api_key_env)
                if api_key:
                    creds["api_key"] = api_key

            # Load extra environment variables
            extra_env = config.get("extra_env", [])
            for env_var in extra_env:
                value = os.getenv(env_var)
                if value:
                    # Convert env var name to credential key (lowercase, remove prefixes)
                    key = env_var.lower().replace(f"{provider.upper()}_", "")
                    creds[key] = value

            # Set default base URL for Ollama
            if provider == "ollama" and "base_url" not in creds:
                creds["base_url"] = config.get(
                    "default_base_url", "http://localhost:11434"
                )

            if creds:
                self.credentials[provider] = creds

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
        if provider not in self.SUPPORTED_PROVIDERS:
            return False

        config = self.SUPPORTED_PROVIDERS[provider]
        creds = self.get_credentials(provider)

        # Providers that don't require API key (like Ollama)
        if not config.get("requires_api_key", True):
            # Check if other required fields are present
            if config.get("requires_project"):
                return bool(creds.get("google_cloud_project"))
            if config.get("requires_base_url"):
                return bool(creds.get("base_url"))
            return True  # No special requirements

        # Standard API key check
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
        if provider in ["azure_openai", "azure_ai"]:
            config["azure_endpoint"] = creds.get("azure_openai_endpoint") or creds.get(
                "endpoint"
            )
            config["api_version"] = creds.get(
                "azure_openai_api_version", "2024-02-15-preview"
            )

        elif provider in ["google_vertexai", "google_anthropic_vertex"]:
            config["project"] = creds.get("google_cloud_project")
            config["location"] = creds.get("google_cloud_location", "us-central1")

        elif provider in ["bedrock", "bedrock_converse"]:
            config["aws_access_key_id"] = creds.get("api_key")
            config["aws_secret_access_key"] = creds.get("aws_secret_access_key")
            config["region_name"] = creds.get("aws_region", "us-east-1")

        elif provider == "ibm":
            config["url"] = creds.get("ibm_cloud_url")
            config["project_id"] = creds.get("ibm_project_id")

        elif provider == "ollama":
            config["base_url"] = creds.get("base_url", "http://localhost:11434")

        # Initialize model using init_chat_model
        try:
            llm = init_chat_model(
                model=model,
                model_provider=provider,
                api_key=api_key if api_key else None,
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
