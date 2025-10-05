"""
Dynamic Model and Provider Selection Utilities
Provides runtime helper functions for selecting models, providers, and embeddings
"""

import streamlit as st
from typing import List, Tuple, Optional, Dict
from src.utils.credentials_manager import CredentialsManager
from src.services.llm_manager import get_llm_manager
from src.utils.embedding_model_manager import EmbeddingModelManager


class DynamicModelSelector:
    """Helper class for dynamic model and provider selection"""

    _embedding_manager = None
    _embedding_cache = None

    @staticmethod
    def get_embedding_manager() -> Optional[EmbeddingModelManager]:
        """Get or create embedding model manager singleton"""
        if DynamicModelSelector._embedding_manager is None:
            try:
                DynamicModelSelector._embedding_manager = EmbeddingModelManager()
            except Exception as e:
                print(f"⚠️ Failed to initialize EmbeddingModelManager: {e}")
                return None
        return DynamicModelSelector._embedding_manager

    @staticmethod
    def get_configured_providers() -> List[str]:
        """
        Get list of LLM providers that have credentials configured

        Returns:
            List of provider IDs that are configured
        """
        return CredentialsManager.get_configured_providers()

    @staticmethod
    def has_any_provider_configured() -> bool:
        """
        Check if at least one LLM provider is configured

        Returns:
            True if at least one provider has credentials
        """
        return len(DynamicModelSelector.get_configured_providers()) > 0

    @staticmethod
    def get_available_models(provider: str = None) -> List[str]:
        """
        Get available models for a provider or all configured providers

        Args:
            provider: Specific provider ID, or None for all configured providers

        Returns:
            List of available model names
        """
        llm_manager = get_llm_manager()

        if provider:
            return llm_manager.get_available_models(provider)

        # Get models from all configured providers
        configured = DynamicModelSelector.get_configured_providers()
        all_models = []

        for prov in configured:
            models = llm_manager.get_available_models(prov)
            # Prefix models with provider for clarity
            all_models.extend([f"{prov}/{model}" for model in models])

        return all_models

    @staticmethod
    def get_available_embedding_models(provider: str = None) -> List[Dict]:
        """
        Get available embedding models from MongoDB

        Args:
            provider: Specific provider ID, or None for all providers

        Returns:
            List of embedding model documents
        """
        embedding_manager = DynamicModelSelector.get_embedding_manager()
        if not embedding_manager:
            return []

        # Use cache if available
        if DynamicModelSelector._embedding_cache is not None:
            models = DynamicModelSelector._embedding_cache
        else:
            models = embedding_manager.get_all_embedding_models()
            DynamicModelSelector._embedding_cache = models

        if provider:
            return [m for m in models if m.get("provider") == provider]

        # Filter by configured providers only
        configured = DynamicModelSelector.get_configured_providers()
        return [m for m in models if m.get("provider") in configured]

    @staticmethod
    def refresh_embedding_cache():
        """Refresh the embedding models cache"""
        DynamicModelSelector._embedding_cache = None

    @staticmethod
    def render_provider_model_selector(
        key_prefix: str = "default",
        default_provider: str = None,
        show_embedding: bool = False,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Render a UI component for selecting provider and model

        Args:
            key_prefix: Unique prefix for widget keys
            default_provider: Default provider to select
            show_embedding: Whether to show embedding model selector

        Returns:
            Tuple of (provider, model, embedding_model)
        """
        configured_providers = DynamicModelSelector.get_configured_providers()

        if not configured_providers:
            st.warning(
                "⚠️ No LLM providers configured. Please configure at least one provider in Settings."
            )
            return None, None, None

        # Get provider info for display names
        llm_manager = get_llm_manager()
        provider_names = {
            p: llm_manager.get_provider_info(p).get("name", p)
            for p in configured_providers
        }

        # Provider selection
        default_index = 0
        if default_provider and default_provider in configured_providers:
            default_index = configured_providers.index(default_provider)

        provider = st.selectbox(
            "LLM Provider",
            options=configured_providers,
            format_func=lambda x: provider_names.get(x, x),
            index=default_index,
            key=f"{key_prefix}_provider",
            help="Select the LLM provider to use",
        )

        if not provider:
            return None, None, None

        # Model selection
        available_models = llm_manager.get_available_models(provider)

        if available_models and available_models != ["custom"]:
            model = st.selectbox(
                "Model",
                options=available_models,
                key=f"{key_prefix}_model",
                help=f"Select a model from {provider_names.get(provider)}",
            )
        else:
            model = st.text_input(
                "Model Name",
                placeholder="Enter model name or deployment name",
                key=f"{key_prefix}_model",
                help="Enter the model name (for Azure, use deployment name)",
            )

        # Embedding model selection (optional)
        embedding_model = None
        if show_embedding:
            embedding_models = DynamicModelSelector.get_available_embedding_models(
                provider
            )

            if embedding_models:
                st.markdown("**Embedding Model**")
                embedding_options = {
                    m["model_id"]: f"{m['name']} ({m['dimensions']} dims)"
                    for m in embedding_models
                }

                selected_embedding = st.selectbox(
                    "Embedding Model",
                    options=list(embedding_options.keys()),
                    format_func=lambda x: embedding_options[x],
                    key=f"{key_prefix}_embedding",
                    help="Select embedding model for document processing",
                    label_visibility="collapsed",
                )
                embedding_model = selected_embedding
            else:
                st.info(
                    f"ℹ️ No embedding models available for {provider_names.get(provider)}"
                )

        return provider, model, embedding_model

    @staticmethod
    def get_default_selection() -> Tuple[Optional[str], Optional[str]]:
        """
        Get a sensible default provider and model if available

        Returns:
            Tuple of (provider, model) or (None, None)
        """
        configured = DynamicModelSelector.get_configured_providers()

        if not configured:
            return None, None

        # Prefer OpenAI if configured
        if "openai" in configured:
            llm_manager = get_llm_manager()
            models = llm_manager.get_available_models("openai")
            if models:
                # Prefer gpt-4o-mini if available
                if "gpt-4o-mini" in models:
                    return "openai", "gpt-4o-mini"
                return "openai", models[0]

        # Otherwise, use first configured provider
        provider = configured[0]
        llm_manager = get_llm_manager()
        models = llm_manager.get_available_models(provider)

        if models and models != ["custom"]:
            return provider, models[0]

        return provider, None

    @staticmethod
    def validate_selection(
        provider: Optional[str], model: Optional[str]
    ) -> Tuple[bool, str]:
        """
        Validate provider and model selection

        Args:
            provider: Provider ID
            model: Model name

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not provider:
            return False, "No provider selected"

        if not model:
            return False, "No model selected"

        if not CredentialsManager.has_credential(provider):
            return False, f"Provider '{provider}' is not configured"

        return True, ""


def get_configured_providers() -> List[str]:
    """Shortcut function to get configured providers"""
    return DynamicModelSelector.get_configured_providers()


def has_any_provider_configured() -> bool:
    """Shortcut function to check if any provider is configured"""
    return DynamicModelSelector.has_any_provider_configured()


def render_model_selector(
    key_prefix: str = "default",
    default_provider: str = None,
    show_embedding: bool = False,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Shortcut function to render model selector"""
    return DynamicModelSelector.render_provider_model_selector(
        key_prefix, default_provider, show_embedding
    )
