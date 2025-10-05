# Migration Guide: v1 to v2 (Multi-LLM Support)

This guide explains how to migrate from the original research application to the refactored v2 with multi-LLM support.

## Overview of Changes

### ✅ What's New in v2

1. **Multi-LLM Support**
   - Support for OpenAI, Anthropic, Google Gemini, Azure OpenAI, Cohere, Together AI, Groq
   - Dynamic provider and model selection
   - Per-provider API key management

2. **Modular Architecture**
   - Clean separation: Pages → Core → Services → Utils → Config
   - Service layer for all external APIs
   - Centralized configuration and state management

3. **Complete Feature Set**
   - All 6 pages fully implemented (Home, Research Assistant, Paper Analyzer, RAG Chat, Prompt Manager, Settings)
   - 15+ default research prompts with CRUD operations
   - Comprehensive settings management

4. **Enhanced User Experience**
   - Unified UI across all pages
   - Better error handling
   - Progress indicators
   - Export functionality

## Migration Steps

### Step 1: Backup Your Data

```bash
# Backup old files
mkdir old_version
mv streamlit_app.py research_assistant.py paper_analyzer_page.py old_version/
mv rag_chat_page.py prompt_manager_page.py settings_page.py old_version/
mv home_page.py old_version/
```

### Step 2: Install New Dependencies

```bash
# Install v2 requirements
pip install -r requirements-v2-multi-llm.txt

# Or upgrade specific packages
pip install --upgrade langchain langchain-core langchain-community
pip install langchain-anthropic langchain-google-genai langchain-cohere
```

### Step 3: Update Environment Variables

Update your `.env` file to include credentials for multiple providers:

```bash
# Old format (v1)
OPENAI_API_KEY=your_key_here

# New format (v2) - Add keys for providers you want to use
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
COHERE_API_KEY=your_cohere_key
GROQ_API_KEY=your_groq_key
TOGETHER_API_KEY=your_together_key

# Optional features
GOOGLE_API_KEY=your_google_search_key  # For Google Search
GOOGLE_CSE_ID=your_cse_id
MONGODB_URI=your_mongodb_uri  # Optional: for prompt storage
```

### Step 4: Code Migration

#### Old Code (v1)
```python
# Old: Direct OpenAI usage
from src.services.openai_service import OpenAIService

openai_service = OpenAIService()
result = openai_service.simple_query("Analyze this paper...")
```

#### New Code (v2)
```python
# New: Multi-LLM support
from src.services.llm_manager import get_llm_manager
from src.utils.credentials_manager import CredentialsManager

# Set credentials
CredentialsManager.set_credential("openai", "your_api_key")

# Or use Anthropic
CredentialsManager.set_credential("anthropic", "your_api_key")

# Initialize LLM manager
llm_manager = get_llm_manager()
llm = llm_manager.initialize_model(
    provider="anthropic",
    model="claude-3-5-sonnet-20241022",
    temperature=0.0
)

# Use the model
from langchain_core.messages import HumanMessage
response = llm.invoke([HumanMessage(content="Analyze this paper...")])
print(response.content)
```

### Step 5: Update Page Imports

#### Old Page Structure (v1)
```
research_assistant.py
paper_analyzer_page.py
rag_chat_page.py
prompt_manager_page.py
settings_page.py
home_page.py
```

#### New Page Structure (v2)
```
pages/
├── 00_home.py
├── 01_research_assistant.py
├── 02_paper_analyzer.py
├── 03_rag_chat.py
├── 04_prompt_manager.py
└── 05_settings.py
```

### Step 6: Update Navigation

The new version uses `.streamlit/pages_sections.toml` for navigation:

```toml
[Home]
title = "🏠 Home"
icon = ":material/home:"
path = "pages/00_home.py"

[Research]
title = "Research Tools"
icon = ":material/science:"

[Research.assistant]
title = "🔍 Research Assistant"
icon = ":material/search:"
path = "pages/01_research_assistant.py"

[Research.analyzer]
title = "📄 Paper Analyzer"
icon = ":material/description:"
path = "pages/02_paper_analyzer.py"

[Research.chat]
title = "💬 RAG Chat"
icon = ":material/chat:"
path = "pages/03_rag_chat.py"

[Management]
title = "Management"
icon = ":material/settings:"

[Management.prompts]
title = "📝 Prompt Manager"
icon = ":material/edit_note:"
path = "pages/04_prompt_manager.py"

[Management.settings]
title = "⚙️ Settings"
icon = ":material/settings:"
path = "pages/05_settings.py"
```

### Step 7: Configure LLM Providers

1. Run the application: `streamlit run app.py`
2. Go to **Settings** page (⚙️)
3. Configure API keys for your preferred providers
4. Test connection using the "Test Configuration" feature
5. Set default preferences (temperature, chunk size, etc.)

## Feature Mapping

### Research Assistant
- **Old**: Basic multi-source search
- **New**: Enhanced with progress tracking, export, and search history

### Paper Analyzer
- **Old**: Single PDF analysis with OpenAI only
- **New**: Multi-LLM support, batch processing, downloadable results

### RAG Chat
- **Old**: Basic document Q&A
- **New**: Multi-document support, chat history, export functionality

### Prompt Manager
- **Old**: Limited prompt templates
- **New**: Full CRUD, 15+ default prompts, categories, search, import/export

### Settings
- **Old**: Basic configuration
- **New**: Complete LLM provider management, preferences, usage stats

## Breaking Changes

1. **API Changes**
   - `OpenAIService.simple_query()` → Use `LLMManager.initialize_model()` with LangChain
   - `OpenAIService.analyze_paper()` → Use `PaperAnalyzer` with provider parameter

2. **Import Paths**
   - Old: `from research_assistant import *`
   - New: `from src.services.llm_manager import get_llm_manager`

3. **Session State**
   - Use `SessionStateManager` for all state operations
   - Centralized state management

4. **Configuration**
   - Use `CredentialsManager` for API keys
   - Dynamic provider selection at runtime

## Advanced Features from research.py

The following features from the original research.py notebook are planned for future releases:

- ✅ **Implemented**: 60+ research prompts (available in Prompt Manager)
- 🔄 **In Progress**: CSV idea analyzer
- 🔄 **In Progress**: Zotero integration
- 🔄 **In Progress**: Structured output with Pydantic models
- 🔄 **In Progress**: Batch document processing with advanced prompts

## Troubleshooting

### Issue: "Provider not configured"
**Solution**: Go to Settings → LLM Providers and configure API key

### Issue: Import errors
**Solution**: Run `pip install -r requirements-v2-multi-llm.txt`

### Issue: Page not found
**Solution**: Ensure `.streamlit/pages_sections.toml` exists and pages are in `pages/` folder

### Issue: "Model not found"
**Solution**: Check provider documentation for correct model names or use custom model input

## Rollback

To rollback to v1:

```bash
# Restore old files
cp old_version/* .

# Reinstall old requirements
pip install -r requirements.txt  # old requirements

# Restore old .env
# Remove new provider keys, keep only OPENAI_API_KEY
```

## Support

- 📚 Documentation: See `README-v2.md`
- 🏗️ Architecture: See `ARCHITECTURE.md`
- ✅ Implementation: See `IMPLEMENTATION_GUIDE.md`
- 📋 Checklist: See `CHECKLIST.md`

## Next Steps

1. Test all pages with your preferred LLM provider
2. Import/export your custom prompts
3. Configure default preferences
4. Explore multi-LLM comparison features
5. Report issues or request features

---

**Welcome to Research Assistant v2.0! 🎉**
