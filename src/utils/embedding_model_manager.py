"""
MongoDB Utility for Embedding Provider Management
Handles storage and retrieval of embedding provider configurations from MongoDB
"""

from typing import List, Dict, Optional
from pymongo.errors import DuplicateKeyError
from config.settings import Settings
from .mongo_manager import MongoDBManager


class EmbeddingModelManager(MongoDBManager):
    """
    MongoDB-based embedding provider management system.
    Inherits from generic MongoDBManager.
    """

    def __init__(self, mongodb_uri: str = None, database_name: str = None):
        super().__init__(
            collection_name=Settings.MONGODB_COLLECTION_EMBEDDINGS,
            mongodb_uri=mongodb_uri,
            database_name=database_name,
        )

    def add_provider(
        self,
        provider: str,
        name: str,
        api_key_env: str,
        models: List[Dict],
        requires_api_key: bool = True,
        **kwargs,
    ) -> dict:
        """
        Add a new embedding provider to the database

        Args:
            provider: Provider identifier (e.g., 'openai', 'cohere')
            name: Display name of the provider
            api_key_env: Environment variable name for API key
            models: List of model configurations for this provider
            requires_api_key: Whether provider requires an API key
            **kwargs: Additional provider-specific configuration

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
                "message": f"Embedding provider '{name}' added successfully",
            }
        except DuplicateKeyError:
            return {
                "success": False,
                "message": f"Embedding provider '{provider}' already exists",
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error adding embedding provider: {str(e)}",
            }

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
        Retrieve all embedding providers

        Returns:
            List of all embedding provider documents
        """
        return self.find()

    def get_models_by_provider(self, provider: str) -> List[Dict]:
        """
        Get embedding models for a specific provider

        Args:
            provider: Provider identifier (e.g., 'openai')

        Returns:
            List of model dictionaries for the provider
        """
        provider_doc = self.find_one({"provider": provider})
        if provider_doc:
            return provider_doc.get("models", [])
        return []

    def get_all_models(self) -> List[Dict]:
        """
        Get all embedding models from all providers

        Returns:
            List of all model dictionaries with provider info added
        """
        providers = self.find()
        all_models = []

        for provider_doc in providers:
            provider_id = provider_doc.get("provider")
            provider_name = provider_doc.get("name")
            for model in provider_doc.get("models", []):
                model_with_provider = model.copy()
                model_with_provider["provider"] = provider_id
                model_with_provider["provider_name"] = provider_name
                all_models.append(model_with_provider)

        return all_models

    def update_provider(self, provider: str, updates: dict) -> dict:
        """
        Update an existing embedding provider

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
                "message": f"Embedding provider '{provider}' updated successfully",
            }
        elif result.matched_count > 0:
            return {
                "success": True,
                "message": f"Embedding provider '{provider}' exists but no changes were made",
            }
        else:
            return {
                "success": False,
                "message": f"Embedding provider '{provider}' not found",
            }

    def delete_provider(self, provider: str) -> dict:
        """
        Delete an embedding provider

        Args:
            provider: Provider identifier to delete

        Returns:
            Dictionary with deletion result
        """
        result = self.delete_one({"provider": provider})
        if result.deleted_count > 0:
            return {
                "success": True,
                "message": f"Embedding provider '{provider}' deleted successfully",
            }
        else:
            return {
                "success": False,
                "message": f"Embedding provider '{provider}' not found",
            }

    def add_model_to_provider(self, provider: str, model: Dict) -> dict:
        """
        Add a model to an existing provider

        Args:
            provider: Provider identifier
            model: Model configuration dictionary

        Returns:
            Dictionary with result
        """
        try:
            result = self.collection.update_one(
                {"provider": provider}, {"$push": {"models": model}}
            )
            if result.modified_count > 0:
                return {
                    "success": True,
                    "message": f"Model added to provider '{provider}'",
                }
            else:
                return {
                    "success": False,
                    "message": f"Provider '{provider}' not found",
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error adding model: {str(e)}",
            }

    def search_models(self, search_term: str) -> List[Dict]:
        """
        Search embedding models by text

        Args:
            search_term: Term to search for

        Returns:
            List of matching model dictionaries
        """
        all_models = self.get_all_models()
        search_lower = search_term.lower()

        results = []
        for model in all_models:
            # Search in model_id, name, provider, and description
            if (
                search_lower in model.get("model_id", "").lower()
                or search_lower in model.get("name", "").lower()
                or search_lower in model.get("provider", "").lower()
                or search_lower in model.get("description", "").lower()
            ):
                results.append(model)

        return results

    # Backward compatibility methods (deprecated)
    def get_all_embedding_models(self) -> List[Dict]:
        """
        Legacy method - get all models (deprecated, use get_all_models)
        """
        return self.get_all_models()

    def get_embedding_models_by_provider(self, provider: str) -> List[Dict]:
        """
        Legacy method - get models by provider (deprecated, use get_models_by_provider)
        """
        return self.get_models_by_provider(provider)

    def search_embedding_models(self, search_term: str) -> List[Dict]:
        """
        Legacy method - search models (deprecated, use search_models)
        """
        return self.search_models(search_term)

    # close() is inherited from MongoDBManager
