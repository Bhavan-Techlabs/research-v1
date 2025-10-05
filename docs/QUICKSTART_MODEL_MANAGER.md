# Quick Start: MongoDB Provider System

## What Changed?

LLM providers are now stored in MongoDB instead of being hardcoded in `llm_manager.py`. This follows the same pattern as the prompt management system.

## Quick Setup

### 1. Verify MongoDB Connection
```bash
export MONGODB_URI="your_mongodb_connection_string"
```

### 2. Check Existing Providers
Since you mentioned you've already uploaded provider data to MongoDB:
```bash
python scripts/seed_providers.py list
```

### 3. Run the Application
```bash
streamlit run streamlit_app.py
```

## Files Modified

1. **New Files**:
   - `src/utils/model_manager.py` - MongoDB manager for providers
   - `scripts/seed_providers.py` - Utility for managing provider data
   - `docs/MODEL_MANAGER_MIGRATION.md` - Full documentation

2. **Modified Files**:
   - `src/services/llm_manager.py` - Now loads from MongoDB
   - `src/utils/credentials_manager.py` - Updated to use instance method
   - `src/utils/__init__.py` - Added ModelManager export

## Key Features

✅ **Dynamic Loading**: Providers loaded from MongoDB on startup  
✅ **Caching**: Results cached for performance  
✅ **Fallback**: Falls back to OpenAI if MongoDB unavailable  
✅ **Backward Compatible**: All existing code works without changes  

## Common Operations

### List Providers
```bash
python scripts/seed_providers.py list
```

### Add Missing Providers
```bash
python scripts/seed_providers.py seed
```

### Update All Providers
```bash
python scripts/seed_providers.py force-seed
```

### Programmatic Access
```python
from src.utils.model_manager import ModelManager

model_manager = ModelManager()

# Get all providers
providers = model_manager.get_all_providers()

# Get specific provider
provider = model_manager.get_provider_by_id("openai")

# Add new model to provider
model_manager.add_model_to_provider("openai", "o1-preview")

# Close connection
model_manager.close()
```

## MongoDB Schema

```json
{
  "provider": "openai",
  "name": "OpenAI",
  "api_key_env": "OPENAI_API_KEY",
  "models": ["gpt-4o", "gpt-4o-mini"],
  "requires_api_key": true
}
```

## Troubleshooting

**No providers showing up?**
- Check MongoDB connection
- Verify data exists: `python scripts/seed_providers.py list`
- Check logs for connection errors

**Changes not appearing?**
- Restart Streamlit application
- Or refresh cache programmatically:
  ```python
  from src.services.llm_manager import get_llm_manager
  get_llm_manager().refresh_providers()
  ```

## Benefits

1. **Easy Updates**: Add new models without code changes
2. **Centralized**: Single source of truth in database
3. **Scalable**: Supports many providers efficiently
4. **Consistent**: Same pattern as prompt management

## Next Steps

1. Verify your MongoDB data is loaded correctly
2. Test the Settings page to configure providers
3. Add new providers/models as needed through MongoDB or the script

For full documentation, see `docs/MODEL_MANAGER_MIGRATION.md`
