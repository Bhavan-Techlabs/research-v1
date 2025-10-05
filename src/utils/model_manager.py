"""
MongoDB Utility for Model/Provider Management
Handles storage and retrieval of LLM provider configurations from MongoDB
Also provides convenience methods for generating completions using configured LLMs
"""

from typing import List, Dict, Optional
from pymongo.errors import DuplicateKeyError
from .mongo_manager import MongoDBManager


class ModelManager(MongoDBManager):
    """
    MongoDB-based model/provider management system for LLM providers.
    Inherits from generic MongoDBManager.
    """

    def __init__(
        self, mongodb_uri: str = None, database_name: str = "research_assistant"
    ):
        super().__init__(
            collection_name="models",
            mongodb_uri=mongodb_uri,
            database_name=database_name,
        )

    def add_provider(
        self,
        provider: str,
        name: str,
        api_key_env: str,
        models: List[str],
        requires_api_key: bool = True,
        **kwargs,
    ) -> dict:
        """
        Add a new LLM provider to the database

        Args:
            provider: Provider identifier (e.g., 'openai', 'anthropic')
            name: Display name of the provider
            api_key_env: Environment variable name for API key
            models: List of available models for this provider
            requires_api_key: Whether provider requires an API key
            **kwargs: Additional provider-specific configuration
                     (e.g., requires_endpoint, requires_project, extra_env, etc.)

        Returns:
            Dictionary with insertion result
        """
        provider_doc = {
            "provider": provider,
            "name": name,
            "api_key_env": api_key_env,
            "models": models,
            "requires_api_key": requires_api_key,
            **kwargs,
        }

        try:
            result = self.insert_one(provider_doc)
            return {
                "success": True,
                "id": str(result.inserted_id),
                "message": f"Provider '{name}' added successfully",
            }
        except DuplicateKeyError:
            return {
                "success": False,
                "message": f"Provider '{provider}' already exists",
            }
        except Exception as e:
            return {"success": False, "message": f"Error adding provider: {str(e)}"}

    def get_provider_by_id(self, provider: str) -> Optional[dict]:
        """
        Retrieve a provider by its identifier

        Args:
            provider: Provider identifier (e.g., 'openai')

        Returns:
            Provider document or None if not found
        """
        return self.find_one({"provider": provider})

    def get_all_providers(self) -> List[dict]:
        """
        Retrieve all providers

        Returns:
            List of all provider documents
        """
        return self.find()

    def get_providers_by_requirement(
        self, requirement: str, value: bool = True
    ) -> List[dict]:
        """
        Get providers based on a specific requirement

        Args:
            requirement: Requirement field name (e.g., 'requires_api_key', 'requires_endpoint')
            value: Boolean value to filter by

        Returns:
            List of matching provider documents
        """
        return self.find({requirement: value})

    def update_provider(self, provider: str, updates: dict) -> dict:
        """
        Update an existing provider

        Args:
            provider: Provider identifier to update
            updates: Dictionary of fields to update

        Returns:
            Dictionary with update result
        """
        result = self.update_one({"provider": provider}, updates)
        if result.modified_count > 0:
            return {
                "success": True,
                "message": f"Provider '{provider}' updated successfully",
            }
        elif result.matched_count > 0:
            return {
                "success": True,
                "message": f"Provider '{provider}' exists but no changes were made",
            }
        else:
            return {"success": False, "message": f"Provider '{provider}' not found"}

    def delete_provider(self, provider: str) -> dict:
        """
        Delete a provider

        Args:
            provider: Provider identifier to delete

        Returns:
            Dictionary with deletion result
        """
        result = self.delete_one({"provider": provider})
        if result.deleted_count > 0:
            return {
                "success": True,
                "message": f"Provider '{provider}' deleted successfully",
            }
        else:
            return {"success": False, "message": f"Provider '{provider}' not found"}

    def search_providers(self, search_term: str) -> List[dict]:
        """
        Search providers by text in name or provider ID

        Args:
            search_term: Term to search for

        Returns:
            List of matching provider documents
        """
        query = {
            "$or": [
                {"provider": {"$regex": search_term, "$options": "i"}},
                {"name": {"$regex": search_term, "$options": "i"}},
            ]
        }
        return self.find(query)

    def bulk_add_providers(self, providers: List[dict]) -> dict:
        """
        Add multiple providers at once

        Args:
            providers: List of provider dictionaries

        Returns:
            Dictionary with insertion results
        """
        try:
            result = self.insert_many(providers)
            return {
                "success": True,
                "inserted_count": len(result.inserted_ids),
                "message": f"Successfully added {len(result.inserted_ids)} providers",
            }
        except Exception as e:
            return {"success": False, "message": f"Error during bulk insert: {str(e)}"}

    def get_provider_models(self, provider: str) -> List[str]:
        """
        Get list of models for a specific provider

        Args:
            provider: Provider identifier

        Returns:
            List of model names or empty list if provider not found
        """
        provider_doc = self.get_provider_by_id(provider)
        return provider_doc.get("models", []) if provider_doc else []

    def add_model_to_provider(self, provider: str, model: str) -> dict:
        """
        Add a new model to an existing provider

        Args:
            provider: Provider identifier
            model: Model name to add

        Returns:
            Dictionary with update result
        """
        provider_doc = self.get_provider_by_id(provider)
        if not provider_doc:
            return {"success": False, "message": f"Provider '{provider}' not found"}

        current_models = provider_doc.get("models", [])
        if model in current_models:
            return {
                "success": False,
                "message": f"Model '{model}' already exists for provider '{provider}'",
            }

        current_models.append(model)
        return self.update_provider(provider, {"models": current_models})

    def remove_model_from_provider(self, provider: str, model: str) -> dict:
        """
        Remove a model from an existing provider

        Args:
            provider: Provider identifier
            model: Model name to remove

        Returns:
            Dictionary with update result
        """
        provider_doc = self.get_provider_by_id(provider)
        if not provider_doc:
            return {"success": False, "message": f"Provider '{provider}' not found"}

        current_models = provider_doc.get("models", [])
        if model not in current_models:
            return {
                "success": False,
                "message": f"Model '{model}' not found for provider '{provider}'",
            }

        current_models.remove(model)
        return self.update_provider(provider, {"models": current_models})

    # ============================================================
    # LLM COMPLETION METHODS
    # ============================================================

    def generate_completion(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        """
        Generate a completion using the configured LLM

        This method provides a convenient way to generate completions without
        manually managing LLMManager instances. It automatically:
        1. Gets credentials from CredentialsManager
        2. Initializes the appropriate LLM
        3. Generates the completion
        4. Returns the text response

        Args:
            prompt: The prompt text to send to the LLM
            provider: Provider to use (if None, uses first configured provider)
            model: Model to use (if None, uses first available model for provider)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters to pass to the model

        Returns:
            The generated text response

        Raises:
            ValueError: If no providers are configured or initialization fails
            Exception: For other errors during generation

        Example:
            >>> manager = ModelManager()
            >>> response = manager.generate_completion(
            ...     prompt="What is the capital of France?",
            ...     temperature=0.5
            ... )
            >>> print(response)
        """
        from src.services.llm_manager import get_llm_manager
        from src.utils.credentials_manager import CredentialsManager
        from langchain_core.messages import HumanMessage

        # Get LLM manager
        llm_manager = get_llm_manager()

        # Get configured providers
        configured_providers = CredentialsManager.get_configured_providers()
        if not configured_providers:
            raise ValueError(
                "No LLM providers configured. Please configure at least one provider in Settings."
            )

        # Determine provider to use
        if provider is None:
            provider = configured_providers[0]
        elif provider not in configured_providers:
            raise ValueError(
                f"Provider '{provider}' is not configured. Configured providers: {', '.join(configured_providers)}"
            )

        # Get credentials and set them
        creds = CredentialsManager.get_credential(provider)
        llm_manager.set_credentials(provider, **creds)

        # Determine model to use
        if model is None:
            available_models = llm_manager.get_available_models(provider)
            if not available_models:
                raise ValueError(f"No models available for provider '{provider}'")
            model = available_models[0]

        # Initialize the model
        llm = llm_manager.initialize_model(
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        # Generate completion
        response = llm.invoke([HumanMessage(content=prompt)])

        # Return the text content
        return response.content

    def generate_streaming_completion(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ):
        """
        Generate a streaming completion using the configured LLM

        Similar to generate_completion but returns a generator that yields
        chunks of the response as they are generated.

        Args:
            prompt: The prompt text to send to the LLM
            provider: Provider to use (if None, uses first configured provider)
            model: Model to use (if None, uses first available model for provider)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters to pass to the model

        Yields:
            Chunks of the generated response

        Raises:
            ValueError: If no providers are configured or initialization fails
            Exception: For other errors during generation

        Example:
            >>> manager = ModelManager()
            >>> for chunk in manager.generate_streaming_completion("Hello"):
            ...     print(chunk, end="", flush=True)
        """
        from src.services.llm_manager import get_llm_manager
        from src.utils.credentials_manager import CredentialsManager
        from langchain_core.messages import HumanMessage

        # Get LLM manager
        llm_manager = get_llm_manager()

        # Get configured providers
        configured_providers = CredentialsManager.get_configured_providers()
        if not configured_providers:
            raise ValueError(
                "No LLM providers configured. Please configure at least one provider in Settings."
            )

        # Determine provider to use
        if provider is None:
            provider = configured_providers[0]
        elif provider not in configured_providers:
            raise ValueError(
                f"Provider '{provider}' is not configured. Configured providers: {', '.join(configured_providers)}"
            )

        # Get credentials and set them
        creds = CredentialsManager.get_credential(provider)
        llm_manager.set_credentials(provider, **creds)

        # Determine model to use
        if model is None:
            available_models = llm_manager.get_available_models(provider)
            if not available_models:
                raise ValueError(f"No models available for provider '{provider}'")
            model = available_models[0]

        # Initialize the model
        llm = llm_manager.initialize_model(
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        # Stream the completion
        for chunk in llm.stream([HumanMessage(content=prompt)]):
            if hasattr(chunk, "content"):
                yield chunk.content

    # close() is inherited from MongoDBManager
