# Dynamic Runtime Configuration Migration

## Overview

The application has been refactored to use **fully dynamic runtime configuration** instead of environment-based API keys and hardcoded models. All LLM providers, models, and embedding models are now managed through MongoDB and configured at runtime by users through the Settings UI.

## What Changed

### Removed from Settings
- ❌ `OPENAI_API_KEY` - No longer in environment
- ❌ `GOOGLE_API_KEY` - No longer in environment  
- ❌ `GOOGLE_CSE_ID` - No longer in environment
- ❌ `DEFAULT_MODEL` - No longer hardcoded
- ❌ `DEFAULT_EMBEDDING_MODEL` - No longer hardcoded
- ❌ `Settings.get_model_options()` - Removed method
- ❌ `Settings.get_embedding_options()` - Removed method
- ❌ `Settings.is_openai_configured()` - Removed method
- ❌ `Settings.is_google_configured()` - Removed method

### What Remains in Settings (Environment-Based)
- ✅ `MONGODB_URI` - Required for application to load providers/models
- ✅ `DEFAULT_TEMPERATURE` - UI default value
- ✅ `DEFAULT_MAX_TOKENS` - UI default value
- ✅ `DEFAULT_CHUNK_SIZE` - Document processing default
- ✅ `MAX_FILE_SIZE_MB` - File upload limit
- ✅ Directory paths and system configuration

## New Architecture

### 1. Model Management Collections

#### `models` Collection (LLM Providers)
```json
{
  "provider": "openai",
  "name": "OpenAI",
  "api_key_env": "OPENAI_API_KEY",
  "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
  "requires_api_key": true
}
```

#### `embedding_models` Collection (NEW)
```json
{
  "model_id": "text-embedding-3-large",
  "provider": "openai",
  "name": "OpenAI Text Embedding 3 Large",
  "dimensions": 3072,
  "max_input": 8191
}
```

### 2. New Utility Classes

#### `EmbeddingModelManager` (`src/utils/embedding_model_manager.py`)
- Manages embedding models from MongoDB
- CRUD operations for embedding configurations
- Similar pattern to `ModelManager` and `PromptManager`

#### `DynamicModelSelector` (`src/utils/dynamic_selector.py`)
- Runtime provider/model selection
- UI components for model selection
- Validates configured providers
- Helper functions for common operations

### 3. Updated LLM Manager

**Changes:**
- Removed `_load_credentials_from_env()` method
- Credentials now ONLY set at runtime via `CredentialsManager`
- No environment variable scanning for API keys
- All API keys entered through Settings UI

### 4. Updated Core Services

Services that need providers/models must now receive them as parameters:

**Before:**
```python
searcher = ResearchSearcher()  # Used Settings.DEFAULT_MODEL
```

**After:**
```python
searcher = ResearchSearcher(
    provider="openai",
    model_name="gpt-4o-mini"
)
```

## Usage Guide

### For Users

1. **Configure Providers** (Settings Page)
   - Go to Settings → LLM Providers
   - Enter API keys for desired providers (OpenAI, Anthropic, etc.)
   - Keys stored in session state (not environment)

2. **Select Models** (Any Page)
   - Each feature page shows provider/model selector
   - Only configured providers appear
   - Models loaded dynamically from MongoDB

3. **Runtime Only**
   - No need to restart application
   - Changes take effect immediately
   - Session-based security

### For Developers

#### Check if Providers Configured

```python
from src.utils.dynamic_selector import has_any_provider_configured

if not has_any_provider_configured():
    st.error("Please configure a provider in Settings")
    st.stop()
```

#### Render Model Selector

```python
from src.utils.dynamic_selector import render_model_selector

provider, model, embedding = render_model_selector(
    key_prefix="my_feature",
    show_embedding=True  # Optional
)

if not provider or not model:
    st.error("Please select provider and model")
    st.stop()
```

#### Initialize LLM with Runtime Credentials

```python
from src.services.llm_manager import get_llm_manager
from src.utils.credentials_manager import CredentialsManager

llm_manager = get_llm_manager()

# Get runtime credentials
creds = CredentialsManager.get_credential(provider)
llm_manager.set_credentials(provider, **creds)

# Initialize model
llm = llm_manager.initialize_model(
    provider=provider,
    model=model,
    temperature=0.0
)
```

#### Get Available Models/Embeddings

```python
from src.utils.dynamic_selector import DynamicModelSelector

# Get all configured providers
providers = DynamicModelSelector.get_configured_providers()

# Get models for a provider
models = DynamicModelSelector.get_available_models("openai")

# Get embedding models
embeddings = DynamicModelSelector.get_available_embedding_models("openai")
```

## MongoDB Setup

### Required Collections

1. **`models`** - LLM provider configurations (already exists)
2. **`embedding_models`** - Embedding model configurations (NEW)
3. **`prompts`** - Prompt templates (already exists)

### Seed Embedding Models

Example embedding models to add to MongoDB:

```json
[
  {
    "model_id": "text-embedding-3-large",
    "provider": "openai",
    "name": "OpenAI Text Embedding 3 Large",
    "dimensions": 3072,
    "max_input": 8191
  },
  {
    "model_id": "text-embedding-3-small",
    "provider": "openai",
    "name": "OpenAI Text Embedding 3 Small",
    "dimensions": 1536,
    "max_input": 8191
  },
  {
    "model_id": "embed-english-v3.0",
    "provider": "cohere",
    "name": "Cohere Embed English v3",
    "dimensions": 1024,
    "max_input": 512
  },
  {
    "model_id": "embed-multilingual-v3.0",
    "provider": "cohere",
    "name": "Cohere Embed Multilingual v3",
    "dimensions": 1024,
    "max_input": 512
  },
  {
    "model_id": "voyage-large-2",
    "provider": "voyageai",
    "name": "Voyage Large 2",
    "dimensions": 1536,
    "max_input": 16000
  }
]
```

## Migration Checklist

### Files Updated

- ✅ `config/settings.py` - Removed API keys and model options
- ✅ `src/services/llm_manager.py` - Removed env credential loading
- ✅ `src/utils/embedding_model_manager.py` - NEW file
- ✅ `src/utils/dynamic_selector.py` - NEW file
- ✅ `pages/00_home.py` - Updated status display
- ✅ `pages/01_research_assistant.py` - Dynamic model selection
- ✅ `pages/05_settings.py` - Updated environment display

### Files That Need Updates (TODO)

- ⏳ `pages/02_paper_analyzer.py` - Add dynamic model selection
- ⏳ `pages/03_rag_chat.py` - Add dynamic model + embedding selection
- ⏳ `pages/04_prompt_manager.py` - Add dynamic model selection
- ⏳ `src/core/research_search.py` - Accept provider/model params
- ⏳ `src/core/paper_analyzer.py` - Accept provider/model params
- ⏳ `src/core/rag_system.py` - Accept provider/model/embedding params
- ⏳ `src/services/arxiv_service.py` - Remove DEFAULT_MODEL usage
- ⏳ `src/services/openai_service.py` - Remove DEFAULT_MODEL usage
- ⏳ `src/services/search_service.py` - Remove DEFAULT_MODEL usage
- ⏳ `src/services/semantic_scholar_service.py` - Remove DEFAULT_MODEL usage

## Benefits

### 1. **No Environment Variables Required**
- Users don't need to set environment variables
- No `.env` file management
- Cleaner deployment

### 2. **Runtime Flexibility**
- Switch providers without restart
- Test multiple providers easily
- Session-based configuration

### 3. **Enhanced Security**
- API keys in session state only
- No keys in files or environment
- Temporary credential storage

### 4. **True Multi-Provider**
- Equal treatment of all providers
- No hardcoded preferences
- Easy to add new providers via MongoDB

### 5. **Centralized Management**
- All configurations in MongoDB
- Single source of truth
- Easy updates and maintenance

## Troubleshooting

### "No providers configured" Error

**Solution:** Go to Settings page and configure at least one LLM provider with API key.

### Embedding Models Not Showing

**Solution:** 
1. Ensure MongoDB is connected
2. Seed `embedding_models` collection
3. Refresh cache: `DynamicModelSelector.refresh_embedding_cache()`

### Old Code Still Using DEFAULT_MODEL

**Solution:** Update the code to accept provider/model as parameters:
```python
# OLD
def __init__(self, model_name=None):
    self.model = model_name or Settings.DEFAULT_MODEL

# NEW
def __init__(self, provider, model_name):
    if not provider or not model_name:
        raise ValueError("Provider and model must be specified")
    self.provider = provider
    self.model = model_name
```

## Testing

### Test Provider Configuration

```python
from src.utils.dynamic_selector import DynamicModelSelector

# Should return empty list initially
assert DynamicModelSelector.get_configured_providers() == []

# Configure via UI, then check
providers = DynamicModelSelector.get_configured_providers()
assert "openai" in providers
```

### Test Model Loading

```python
from src.services.llm_manager import get_llm_manager

manager = get_llm_manager()
models = manager.get_available_models("openai")
assert len(models) > 0
assert "gpt-4o-mini" in models
```

### Test Dynamic Selection

```python
provider, model, embedding = render_model_selector(
    key_prefix="test",
    show_embedding=True
)
assert provider is not None
assert model is not None
```

## Next Steps

1. ✅ Create `embedding_models` collection in MongoDB
2. ✅ Seed embedding models for configured providers
3. ⏳ Update remaining pages (paper analyzer, RAG chat, etc.)
4. ⏳ Update core services to require provider/model params
5. ⏳ Remove all `Settings.DEFAULT_MODEL` references
6. ⏳ Add embedding model selection to RAG features
7. ⏳ Test end-to-end with multiple providers

## See Also

- [Model Manager Migration](MODEL_MANAGER_MIGRATION.md)
- [Multi-LLM Implementation](MULTI_LLM_IMPLEMENTATION.md)
- [Prompt Manager](PROMPT_MANAGER_MIGRATION.md)
