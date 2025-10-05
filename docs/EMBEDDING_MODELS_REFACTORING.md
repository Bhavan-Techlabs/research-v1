# Embedding Models Refactoring Summary

## Overview
Refactored the embedding models system to follow the same provider-based pattern as the LLM providers, simplifying management and improving consistency.

## Changes Made

### 1. `scripts/seed_embedding_models.py`
**Before:** Stored individual embedding models as separate documents in MongoDB
**After:** Groups embedding models by provider with models as an array within each provider document

#### Key Changes:
- Renamed function: `get_default_embedding_models()` → `get_embedding_providers()`
- Structure change: Each provider document now contains:
  - `provider`: Provider ID (e.g., "openai")
  - `name`: Display name (e.g., "OpenAI")
  - `api_key_env`: Environment variable for API key
  - `models`: Array of model configurations
  - `requires_api_key`: Boolean flag
  - Additional provider-specific configs (e.g., `requires_endpoint`, `extra_env`)

- Model structure within the array:
  ```python
  {
      "model_id": "text-embedding-3-large",
      "name": "Text Embedding 3 Large",
      "dimensions": 3072,
      "max_input": 8191,
      "description": "Most capable OpenAI embedding model"
  }
  ```

- Simplified CLI commands:
  - `python seed_embedding_models.py list` - List all providers
  - `python seed_embedding_models.py seed` - Seed providers
  - `python seed_embedding_models.py force-seed` - Force update providers

### 2. `src/utils/embedding_model_manager.py`
**Before:** Managed individual embedding model documents
**After:** Manages provider documents with embedded model arrays

#### Key Changes:
- Collection name changed: `embedding_models` → `embedding_providers`
- New core methods:
  - `add_provider()`: Add a provider with its models
  - `get_provider_by_id()`: Get provider by ID
  - `get_all_providers()`: Get all providers
  - `get_models_by_provider()`: Get models for a specific provider
  - `get_all_models()`: Get all models from all providers (flattened)
  - `update_provider()`: Update a provider
  - `delete_provider()`: Delete a provider
  - `add_model_to_provider()`: Add a model to an existing provider
  - `search_models()`: Search across all models

- Backward compatibility methods (deprecated but functional):
  - `get_all_embedding_models()` → calls `get_all_models()`
  - `get_embedding_models_by_provider()` → calls `get_models_by_provider()`
  - `search_embedding_models()` → calls `search_models()`

### 3. `src/utils/dynamic_selector.py`
**Status:** No changes needed
- Continues to work via backward compatibility methods in `EmbeddingModelManager`
- `get_available_embedding_models()` still functions correctly

### 4. Other Files
**Status:** No changes needed
- No direct usage of embedding model management in pages or core modules
- All existing code continues to work through backward compatibility layer

## Benefits

1. **Consistency**: Embedding providers now follow the same pattern as LLM providers
2. **Simplified Management**: Easier to add/update providers with multiple models
3. **Better Organization**: Models are grouped by provider in the database
4. **Backward Compatibility**: Existing code continues to work without modifications
5. **Cleaner Seeding**: Seed script is now simpler and follows the same pattern as `seed_providers.py`

## Database Migration

### Old Structure (embedding_models collection):
```json
{
    "_id": "...",
    "model_id": "text-embedding-3-large",
    "provider": "openai",
    "name": "OpenAI Text Embedding 3 Large",
    "dimensions": 3072,
    "max_input": 8191,
    "description": "..."
}
```

### New Structure (embedding_providers collection):
```json
{
    "_id": "...",
    "provider": "openai",
    "name": "OpenAI",
    "api_key_env": "OPENAI_API_KEY",
    "requires_api_key": true,
    "models": [
        {
            "model_id": "text-embedding-3-large",
            "name": "Text Embedding 3 Large",
            "dimensions": 3072,
            "max_input": 8191,
            "description": "..."
        },
        {
            "model_id": "text-embedding-3-small",
            "name": "Text Embedding 3 Small",
            "dimensions": 1536,
            "max_input": 8191,
            "description": "..."
        }
    ]
}
```

## Migration Steps (if needed)

If you have existing data in the `embedding_models` collection:

1. The new code uses `embedding_providers` collection, so old data won't conflict
2. Run the seed script to populate the new structure:
   ```bash
   python scripts/seed_embedding_models.py seed
   ```
3. Optionally, drop the old collection if no longer needed:
   ```python
   # In MongoDB shell or client
   db.embedding_models.drop()
   ```

## Providers Included

The seed script includes embedding models from:
- OpenAI
- Cohere
- Google Vertex AI
- Google Gemini
- AWS Bedrock
- Azure OpenAI
- Mistral AI
- Voyage AI
- HuggingFace
- Ollama (local)

Each provider includes multiple model variants optimized for different use cases.
