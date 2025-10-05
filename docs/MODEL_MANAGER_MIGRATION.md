# MongoDB-Based LLM Provider Management

## Overview

The LLM provider system has been migrated from hardcoded configurations to a MongoDB-based system, similar to how prompts are managed. This provides greater flexibility and allows for dynamic provider management without code changes.

## Architecture

### Key Components

1. **ModelManager** (`src/utils/model_manager.py`)
   - Inherits from `MongoDBManager`
   - Handles CRUD operations for LLM provider configurations
   - Manages provider metadata, models, and requirements

2. **LLMManager** (`src/services/llm_manager.py`)
   - Loads providers from MongoDB with caching
   - Falls back to minimal hardcoded providers if MongoDB is unavailable
   - Maintains backward compatibility with existing code

3. **Seeding Script** (`scripts/seed_providers.py`)
   - Utility to populate MongoDB with default providers
   - Can list, seed, or force-update providers

## MongoDB Schema

### Collection: `models`

Each provider document follows this structure:

```json
{
  "_id": ObjectId("..."),
  "provider": "openai",
  "name": "OpenAI",
  "api_key_env": "OPENAI_API_KEY",
  "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
  "requires_api_key": true,
  "requires_endpoint": false,
  "requires_project": false,
  "extra_env": [],
  "default_base_url": ""
}
```

### Field Descriptions

- **provider** (string): Unique identifier for the provider (e.g., "openai", "anthropic")
- **name** (string): Display name of the provider
- **api_key_env** (string): Environment variable name for the API key
- **models** (array): List of available model names/IDs
- **requires_api_key** (boolean): Whether the provider requires an API key
- **requires_endpoint** (boolean): Whether the provider requires an endpoint URL (e.g., Azure)
- **requires_project** (boolean): Whether the provider requires a project ID (e.g., Google Vertex AI)
- **extra_env** (array): Additional environment variables needed
- **default_base_url** (string): Default base URL for self-hosted providers (e.g., Ollama)

## Setup Instructions

### 1. Ensure MongoDB is Running

Make sure you have MongoDB connection configured:

```bash
export MONGODB_URI="mongodb://localhost:27017/"
# or
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
```

### 2. Seed Provider Data

If you've already uploaded provider data to MongoDB, you can verify it:

```bash
python scripts/seed_providers.py list
```

If you need to add missing providers or update existing ones:

```bash
# Add missing providers (won't overwrite existing)
python scripts/seed_providers.py seed

# Force update all providers (overwrites existing)
python scripts/seed_providers.py force-seed
```

### 3. Run the Application

The application will automatically load providers from MongoDB:

```bash
streamlit run streamlit_app.py
```

## Features

### Dynamic Provider Loading

- Providers are loaded from MongoDB on startup
- Results are cached for performance
- Cache can be refreshed without restarting the application

### Fallback Mechanism

If MongoDB is unavailable, the system falls back to a minimal set of hardcoded providers:
- OpenAI (basic models only)

This ensures the application remains functional even without database connectivity.

### Provider Management Operations

The `ModelManager` class provides methods for:

```python
from src.utils.model_manager import ModelManager

model_manager = ModelManager()

# Get all providers
providers = model_manager.get_all_providers()

# Get specific provider
provider = model_manager.get_provider_by_id("openai")

# Add new provider
result = model_manager.add_provider(
    provider="custom_provider",
    name="Custom Provider",
    api_key_env="CUSTOM_API_KEY",
    models=["model-1", "model-2"],
    requires_api_key=True
)

# Update provider
result = model_manager.update_provider(
    "openai",
    {"models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "o1"]}
)

# Add model to provider
result = model_manager.add_model_to_provider("openai", "o1-preview")

# Delete provider
result = model_manager.delete_provider("custom_provider")
```

### Refresh Cache

After modifying providers in MongoDB, refresh the cache:

```python
from src.services.llm_manager import get_llm_manager

llm_manager = get_llm_manager()
llm_manager.refresh_providers()
```

## Migration from Hardcoded Providers

The original `SUPPORTED_PROVIDERS` dictionary has been converted to a property that:
1. Checks if MongoDB is enabled
2. Loads providers from MongoDB (with caching)
3. Falls back to minimal hardcoded providers if needed

All existing code continues to work without modification.

## Benefits

1. **Dynamic Management**: Add/update/remove providers without code changes
2. **Centralized Configuration**: Single source of truth for provider data
3. **Easy Updates**: Update model lists as providers release new models
4. **Scalability**: Supports large numbers of providers efficiently
5. **Consistency**: Same pattern as prompt management system

## Usage in Application

### Settings Page

The Settings page (`pages/05_settings.py`) automatically displays all providers from MongoDB:

```python
from src.utils.credentials_manager import LLMConfigWidget

# Renders all providers dynamically
LLMConfigWidget.render_all_providers()
```

### Using LLM Manager

Initialize models as before:

```python
from src.services.llm_manager import get_llm_manager
from src.utils.credentials_manager import CredentialsManager

llm_manager = get_llm_manager()

# Set credentials
CredentialsManager.set_credential("openai", "sk-...")

# Get credentials and initialize
creds = CredentialsManager.get_credential("openai")
llm_manager.set_credentials("openai", **creds)

# Initialize model
llm = llm_manager.initialize_model(
    provider="openai",
    model="gpt-4o",
    temperature=0.0
)
```

## Troubleshooting

### MongoDB Connection Issues

If you see warnings about MongoDB connection:

```
⚠️ MongoDB connection failed, using fallback providers
```

Check:
1. MongoDB URI is correctly set in environment variables
2. MongoDB service is running
3. Network connectivity to MongoDB instance

### No Providers Loaded

If no providers are loaded from MongoDB:

```bash
# Check if providers exist
python scripts/seed_providers.py list

# Seed providers if needed
python scripts/seed_providers.py seed
```

### Cache Issues

If changes to providers don't appear:

```python
# Refresh the cache
llm_manager.refresh_providers()
```

Or restart the Streamlit application.

## Example Provider Data

Here's an example of what you should see in MongoDB:

```json
[
  {
    "_id": {"$oid": "68e275ada9474f7b7f94f803"},
    "provider": "openai",
    "name": "OpenAI",
    "api_key_env": "OPENAI_API_KEY",
    "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
    "requires_api_key": true
  },
  {
    "_id": {"$oid": "68e275ada9474f7b7f94f804"},
    "provider": "anthropic",
    "name": "Anthropic",
    "api_key_env": "ANTHROPIC_API_KEY",
    "models": [
      "claude-3-5-sonnet-20241022",
      "claude-3-opus-20240229",
      "claude-3-sonnet-20240229",
      "claude-3-haiku-20240307"
    ],
    "requires_api_key": true
  }
]
```

## Future Enhancements

Potential future improvements:

1. **Admin UI**: Web interface for managing providers
2. **Provider Categories**: Group providers by type (cloud, local, etc.)
3. **Model Metadata**: Add cost, context window, capabilities for each model
4. **Usage Tracking**: Track which providers/models are most used
5. **Version History**: Track changes to provider configurations

## See Also

- [Prompt Manager Documentation](PROMPT_MANAGER_MIGRATION.md)
- [Multi-LLM Implementation](MULTI_LLM_IMPLEMENTATION.md)
- [MongoDB Manager](../src/utils/mongo_manager.py)
