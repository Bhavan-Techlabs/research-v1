"""
LLM Manager Service
Supports multiple LLM providers using langchain's init_chat_model
Handles dynamic API key management and provider selection
Loads provider configurations from MongoDB
"""

import os
from typing import Optional, Dict, Any, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models import init_chat_model
from config.settings import Settings
from src.utils.model_manager import ModelManager


class LLMManager:
    """
    Manages multiple LLM providers with dynamic configuration
    Supports: OpenAI, Anthropic, Google, Azure, Cohere, and more
    Loads provider configurations from MongoDB
    """

    # Fallback providers in case MongoDB is not available
    FALLBACK_PROVIDERS = {
        "openai": {
            "name": "OpenAI",
            "api_key_env": "OPENAI_API_KEY",
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "requires_api_key": True,
        },
    }

    def __init__(self, use_mongodb: bool = True):
        """
        Initialize LLM Manager

        Args:
            use_mongodb: Whether to load providers from MongoDB (default: True)
        """
        self.credentials = {}
        self.use_mongodb = use_mongodb
        self._providers_cache = None  # Cache for MongoDB providers
        self._model_manager = None

        # Initialize ModelManager if MongoDB is enabled
        if self.use_mongodb:
            try:
                self._model_manager = ModelManager()
                print("✅ LLM Manager connected to MongoDB for provider data")
            except Exception as e:
                print(f"⚠️ MongoDB connection failed, using fallback providers: {e}")
                self.use_mongodb = False

        self._load_credentials_from_env()

    @property
    def SUPPORTED_PROVIDERS(self) -> Dict[str, Dict[str, Any]]:
        """
        Get supported providers, either from MongoDB or fallback
        Uses caching to avoid repeated database queries
        """
        if self.use_mongodb and self._model_manager:
            # Return cached providers if available
            if self._providers_cache is not None:
                return self._providers_cache

            try:
                # Load providers from MongoDB
                providers_list = self._model_manager.get_all_providers()

                # Convert list to dictionary format keyed by provider ID
                providers_dict = {}
                for provider_doc in providers_list:
                    provider_id = provider_doc.get("provider")
                    if provider_id:
                        # Remove MongoDB _id field and use provider as key
                        provider_data = {
                            k: v
                            for k, v in provider_doc.items()
                            if k not in ["_id", "provider"]
                        }
                        providers_dict[provider_id] = provider_data

                # Cache the result
                self._providers_cache = providers_dict

                if providers_dict:
                    print(f"✅ Loaded {len(providers_dict)} providers from MongoDB")
                    return providers_dict
                else:
                    print("⚠️ No providers found in MongoDB, using fallback")
                    return self.FALLBACK_PROVIDERS

            except Exception as e:
                print(f"⚠️ Error loading providers from MongoDB: {e}")
                return self.FALLBACK_PROVIDERS
        else:
            # Use fallback providers
            return self.FALLBACK_PROVIDERS

    def refresh_providers(self):
        """
        Refresh providers cache from MongoDB
        Call this after adding/updating providers in the database
        """
        self._providers_cache = None
        # Trigger reload
        _ = self.SUPPORTED_PROVIDERS

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

    def get_all_providers(self) -> List[Dict[str, Any]]:
        """Get information about all supported providers"""
        return [
            {"id": provider_id, **provider_info}
            for provider_id, provider_info in self.SUPPORTED_PROVIDERS.items()
        ]

    def get_model_manager(self) -> Optional[ModelManager]:
        """Get the ModelManager instance if MongoDB is enabled"""
        return self._model_manager


# Singleton instance
_llm_manager = None


def get_llm_manager() -> LLMManager:
    """Get singleton instance of LLM Manager"""
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager
