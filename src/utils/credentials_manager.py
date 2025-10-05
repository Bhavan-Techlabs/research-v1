"""
Credentials Manager
Handles secure storage and retrieval of API keys for multiple providers
"""

import streamlit as st
from typing import Dict, Optional, List
import json
from pathlib import Path
from config.settings import Settings


class CredentialsManager:
    """
    Manages credentials for multiple LLM providers
    Stores in Streamlit session state for security
    """

    SESSION_KEY = "llm_credentials"

    @staticmethod
    def initialize():
        """Initialize credentials in session state"""
        if CredentialsManager.SESSION_KEY not in st.session_state:
            st.session_state[CredentialsManager.SESSION_KEY] = {}

    @staticmethod
    def set_credential(provider: str, api_key: str, **kwargs):
        """
        Set credentials for a provider

        Args:
            provider: Provider name
            api_key: API key
            **kwargs: Additional credentials (endpoint, api_version, etc.)
        """
        CredentialsManager.initialize()
        st.session_state[CredentialsManager.SESSION_KEY][provider] = {
            "api_key": api_key,
            **kwargs,
        }

    @staticmethod
    def get_credential(provider: str) -> Optional[Dict]:
        """Get credentials for a provider"""
        CredentialsManager.initialize()
        return st.session_state[CredentialsManager.SESSION_KEY].get(provider)

    @staticmethod
    def get_api_key(provider: str) -> Optional[str]:
        """Get API key for a provider"""
        cred = CredentialsManager.get_credential(provider)
        return cred.get("api_key") if cred else None

    @staticmethod
    def has_credential(provider: str) -> bool:
        """Check if provider has credentials"""
        cred = CredentialsManager.get_credential(provider)
        return bool(cred and cred.get("api_key"))

    @staticmethod
    def get_configured_providers() -> List[str]:
        """Get list of configured providers"""
        CredentialsManager.initialize()
        return [
            p
            for p, cred in st.session_state[CredentialsManager.SESSION_KEY].items()
            if cred.get("api_key")
        ]

    @staticmethod
    def clear_credential(provider: str):
        """Clear credentials for a provider"""
        CredentialsManager.initialize()
        if provider in st.session_state[CredentialsManager.SESSION_KEY]:
            del st.session_state[CredentialsManager.SESSION_KEY][provider]

    @staticmethod
    def clear_all():
        """Clear all credentials"""
        st.session_state[CredentialsManager.SESSION_KEY] = {}

    @staticmethod
    def export_config(exclude_keys: bool = True) -> Dict:
        """
        Export configuration (optionally excluding sensitive keys)

        Args:
            exclude_keys: If True, excludes API keys from export

        Returns:
            Configuration dictionary
        """
        CredentialsManager.initialize()
        config = st.session_state[CredentialsManager.SESSION_KEY].copy()

        if exclude_keys:
            for provider in config:
                if "api_key" in config[provider]:
                    config[provider]["api_key"] = "***REDACTED***"

        return config

    @staticmethod
    def import_config(config: Dict):
        """
        Import configuration

        Args:
            config: Configuration dictionary
        """
        CredentialsManager.initialize()
        for provider, creds in config.items():
            if creds.get("api_key") and creds["api_key"] != "***REDACTED***":
                CredentialsManager.set_credential(provider, **creds)


class LLMConfigWidget:
    """
    Streamlit widget for LLM provider configuration
    Provides UI for setting up multiple LLM providers
    """

    @staticmethod
    def render_provider_config(provider_id: str, provider_info: Dict):
        """
        Render configuration UI for a provider

        Args:
            provider_id: Provider identifier
            provider_info: Provider information
        """
        CredentialsManager.initialize()

        provider_name = provider_info.get("name", provider_id)
        is_configured = CredentialsManager.has_credential(provider_id)

        with st.expander(
            f"{'✅' if is_configured else '⚠️'} {provider_name}",
            expanded=not is_configured,
        ):
            # API Key input
            requires_api_key = provider_info.get("requires_api_key", True)
            current_cred = CredentialsManager.get_credential(provider_id)
            current_key = current_cred.get("api_key") if current_cred else None

            api_key = None
            if requires_api_key:
                api_key_placeholder = "***" * 10 if current_key else "Enter API key"
                api_key = st.text_input(
                    f"{provider_name} API Key",
                    value="" if not current_key else current_key,
                    type="password",
                    key=f"{provider_id}_api_key",
                    placeholder=api_key_placeholder,
                    help=f"Get your API key from {provider_info.get('name')} platform",
                )

            # Additional fields for specific providers
            extra_fields = {}

            # Azure OpenAI / Azure AI
            if provider_id in ["azure_openai", "azure_ai"]:
                endpoint = st.text_input(
                    "Azure Endpoint",
                    value=(current_cred.get("endpoint", "") if current_cred else ""),
                    key=f"{provider_id}_endpoint",
                    placeholder="https://your-resource.openai.azure.com/",
                )
                api_version = st.text_input(
                    "API Version",
                    value=(
                        current_cred.get("api_version", "2024-02-15-preview")
                        if current_cred
                        else "2024-02-15-preview"
                    ),
                    key=f"{provider_id}_api_version",
                )
                extra_fields = {"endpoint": endpoint, "api_version": api_version}

            # Google Vertex AI / Anthropic Vertex
            elif provider_id in ["google_vertexai", "google_anthropic_vertex"]:
                project = st.text_input(
                    "Google Cloud Project ID",
                    value=(current_cred.get("project", "") if current_cred else ""),
                    key=f"{provider_id}_project",
                    placeholder="my-project-id",
                )
                location = st.text_input(
                    "Location",
                    value=(
                        current_cred.get("location", "us-central1")
                        if current_cred
                        else "us-central1"
                    ),
                    key=f"{provider_id}_location",
                    placeholder="us-central1",
                )
                creds_file = st.text_input(
                    "Credentials File Path (optional)",
                    value=(
                        current_cred.get("credentials_file", "") if current_cred else ""
                    ),
                    key=f"{provider_id}_creds_file",
                    placeholder="/path/to/credentials.json",
                    help="Path to Google Cloud credentials JSON file",
                )
                extra_fields = {"project": project, "location": location}
                if creds_file:
                    extra_fields["credentials_file"] = creds_file

            # AWS Bedrock
            elif provider_id in ["bedrock", "bedrock_converse"]:
                secret_key = st.text_input(
                    "AWS Secret Access Key",
                    value=(current_cred.get("secret_key", "") if current_cred else ""),
                    type="password",
                    key=f"{provider_id}_secret_key",
                    placeholder="Enter AWS secret key",
                )
                region = st.text_input(
                    "AWS Region",
                    value=(
                        current_cred.get("region", "us-east-1")
                        if current_cred
                        else "us-east-1"
                    ),
                    key=f"{provider_id}_region",
                    placeholder="us-east-1",
                )
                extra_fields = {"secret_key": secret_key, "region": region}

            # IBM watsonx
            elif provider_id == "ibm":
                url = st.text_input(
                    "IBM Cloud URL",
                    value=(current_cred.get("url", "") if current_cred else ""),
                    key=f"{provider_id}_url",
                    placeholder="https://us-south.ml.cloud.ibm.com",
                )
                project_id = st.text_input(
                    "Project ID",
                    value=(current_cred.get("project_id", "") if current_cred else ""),
                    key=f"{provider_id}_project_id",
                    placeholder="your-project-id",
                )
                extra_fields = {"url": url, "project_id": project_id}

            # Ollama
            elif provider_id == "ollama":
                base_url = st.text_input(
                    "Ollama Base URL",
                    value=(
                        current_cred.get("base_url", "http://localhost:11434")
                        if current_cred
                        else "http://localhost:11434"
                    ),
                    key=f"{provider_id}_base_url",
                    placeholder="http://localhost:11434",
                    help="URL where Ollama is running",
                )
                extra_fields = {"base_url": base_url}

            # Save button
            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button(
                    f"💾 Save {provider_name}",
                    key=f"{provider_id}_save",
                    use_container_width=True,
                ):
                    # Validate based on requirements
                    if requires_api_key and not api_key:
                        st.error("Please enter an API key")
                    elif provider_id in [
                        "google_vertexai",
                        "google_anthropic_vertex",
                    ] and not extra_fields.get("project"):
                        st.error("Please enter Google Cloud Project ID")
                    elif provider_id in [
                        "bedrock",
                        "bedrock_converse",
                    ] and not extra_fields.get("secret_key"):
                        st.error("Please enter AWS Secret Access Key")
                    elif provider_id == "ibm" and (
                        not extra_fields.get("url")
                        or not extra_fields.get("project_id")
                    ):
                        st.error("Please enter IBM Cloud URL and Project ID")
                    else:
                        # Save credentials
                        if api_key:
                            CredentialsManager.set_credential(
                                provider_id, api_key, **extra_fields
                            )
                        else:
                            # For providers without API key (like Ollama)
                            CredentialsManager.set_credential(
                                provider_id, "", **extra_fields
                            )
                        st.success(f"✅ {provider_name} configured!")
                        st.rerun()

            with col2:
                if is_configured and st.button(
                    f"🗑️ Clear", key=f"{provider_id}_clear", use_container_width=True
                ):
                    CredentialsManager.clear_credential(provider_id)
                    st.success(f"Cleared {provider_name} credentials")
                    st.rerun()

            # Model selection for this provider
            if is_configured:
                models = provider_info.get("models", [])
                if models and models != ["custom"]:
                    st.markdown("**Available Models:**")
                    st.markdown(", ".join([f"`{m}`" for m in models]))

    @staticmethod
    def render_all_providers():
        """Render configuration UI for all providers"""
        from src.services.llm_manager import get_llm_manager

        llm_manager = get_llm_manager()

        st.subheader("All LLM Providers")
        st.markdown("Configure your API keys for different LLM providers:")

        # Get all providers from the manager (now loaded from MongoDB)
        all_providers = llm_manager.get_all_providers()

        if not all_providers:
            st.warning("⚠️ No LLM providers available. Please check MongoDB connection.")
            return

        for provider_info in all_providers:
            provider_id = provider_info["id"]
            LLMConfigWidget.render_provider_config(provider_id, provider_info)

    @staticmethod
    def render_model_selector(default_provider: str = "openai") -> tuple:
        """
        Render provider and model selector

        Args:
            default_provider: Default provider to select

        Returns:
            Tuple of (provider, model)
        """
        from src.services.llm_manager import get_llm_manager

        llm_manager = get_llm_manager()
        configured_providers = CredentialsManager.get_configured_providers()

        if not configured_providers:
            st.warning(
                "⚠️ No LLM providers configured. Please configure at least one provider in Settings."
            )
            return None, None

        # Provider selection
        provider_names = {
            p: llm_manager.get_provider_info(p).get("name", p)
            for p in configured_providers
        }
        provider_display = st.selectbox(
            "LLM Provider",
            options=configured_providers,
            format_func=lambda x: provider_names.get(x, x),
            index=(
                configured_providers.index(default_provider)
                if default_provider in configured_providers
                else 0
            ),
        )

        if not provider_display:
            return None, None

        # Model selection
        available_models = llm_manager.get_available_models(provider_display)

        if available_models and available_models != ["custom"]:
            model = st.selectbox(
                "Model",
                options=available_models,
                help=f"Select a model from {provider_names.get(provider_display)}",
            )
        else:
            model = st.text_input(
                "Model Name",
                placeholder="Enter model name or deployment name",
                help="Enter the model name (for Azure, use deployment name)",
            )

        return provider_display, model
