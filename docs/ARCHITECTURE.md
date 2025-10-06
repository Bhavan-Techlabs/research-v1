# 🏗️ Architecture - Research Assistant Platform

## System Architecture Overview

The Research Assistant Platform is built with a **service-oriented architecture** featuring **runtime LLM configuration**, **multi-provider support**, and **MongoDB-backed provider registry**.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER (Streamlit)                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  streamlit_app.py (Entry Point)                                      │
│  ├── Authentication (streamlit-authenticator)                        │
│  ├── Navigation (st-pages)                                           │
│  └── Session State Initialization                                    │
│                                                                       │
│  pages/                                                              │
│  ├── 00_home.py               - Dashboard with metrics              │
│  ├── 01_research_assistant.py - Multi-source paper search           │
│  ├── 02_paper_analyzer.py     - AI-powered PDF analysis             │
│  ├── 03_rag_chat.py           - RAG document Q&A                    │
│  ├── 04_prompt_manager.py     - Prompt library CRUD                 │
│  └── 05_settings.py           - Runtime LLM configuration           │
│                                                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ uses
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   CORE BUSINESS LOGIC LAYER                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  src/core/                                                           │
│  ├── research_search.py                                             │
│  │   └── ResearchSearcher                                           │
│  │       ├── search_all_sources()      - Orchestrate multi-search  │
│  │       ├── search_arxiv()            - ArXiv search               │
│  │       ├── search_semantic_scholar() - Semantic Scholar search    │
│  │       └── search_google/duckduckgo() - Web search                │
│  │                                                                   │
│  ├── paper_analyzer.py                                              │
│  │   └── PaperAnalyzer                                              │
│  │       ├── analyze_pdf()             - Single paper analysis      │
│  │       ├── analyze_multiple_pdfs()   - Batch processing           │
│  │       └── _build_analysis_prompt()  - Dynamic prompt builder     │
│  │                                                                   │
│  └── rag_system.py                                                  │
│      └── RAGSystem                                                  │
│          ├── create_retriever()        - Vector DB initialization   │
│          ├── query()                   - RAG query execution        │
│          └── get_relevant_docs()       - Document retrieval         │
│                                                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ depends on
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  SERVICES LAYER (API Integrations)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  src/services/                                                       │
│  ├── llm_manager.py              ★ CORE SERVICE ★                   │
│  │   └── LLMManager                                                 │
│  │       ├── initialize_model()       - Dynamic LLM initialization  │
│  │       ├── set_credentials()        - Runtime API key setting     │
│  │       ├── SUPPORTED_PROVIDERS      - MongoDB-backed provider list│
│  │       ├── refresh_providers()      - Reload from database        │
│  │       └── get_available_models()   - Get models for provider     │
│  │                                                                   │
│  ├── arxiv_service.py                                               │
│  │   └── ArxivService                                               │
│  │       ├── search_with_agent()      - LLM-enhanced search         │
│  │       ├── load_documents_from_query()                            │
│  │       └── load_document_by_id()                                  │
│  │                                                                   │
│  ├── semantic_scholar_service.py                                    │
│  │   └── SemanticScholarService                                     │
│  │       └── search()                 - Semantic Scholar API        │
│  │                                                                   │
│  └── search_service.py                                              │
│      └── SearchService                                              │
│          ├── google_search()          - Google Custom Search        │
│          └── duckduckgo_search()      - DuckDuckGo search           │
│                                                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ uses
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         UTILITIES LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  src/utils/                                                          │
│  ├── credentials_manager.py     ★ RUNTIME SECURITY ★                │
│  │   └── CredentialsManager                                         │
│  │       ├── set_credential()         - Store API keys (session)    │
│  │       ├── get_credential()         - Retrieve credentials        │
│  │       ├── has_credential()         - Check if configured         │
│  │       ├── get_configured_providers() - List active providers     │
│  │       └── clear_credential()       - Remove credentials          │
│  │   └── LLMConfigWidget             - UI components for config     │
│  │       ├── render_provider_config() - Provider setup UI           │
│  │       ├── render_model_selector()  - Model dropdown              │
│  │       └── render_all_providers()   - Full config interface       │
│  │                                                                   │
│  ├── model_manager.py           ★ DATABASE LAYER ★                  │
│  │   └── ModelManager (extends MongoDBManager)                      │
│  │       ├── add_provider()           - Register LLM provider       │
│  │       ├── get_all_providers()      - List all providers          │
│  │       ├── get_provider_by_id()     - Fetch specific provider     │
│  │       ├── update_provider()        - Modify provider config      │
│  │       └── delete_provider()        - Remove provider             │
│  │                                                                   │
│  ├── embedding_model_manager.py ★ EMBEDDING DB ★                    │
│  │   └── EmbeddingModelManager (extends MongoDBManager)             │
│  │       ├── add_provider()           - Register embedding provider │
│  │       ├── get_all_providers()      - List embedding providers    │
│  │       ├── get_models_by_provider() - Get models for provider     │
│  │       └── get_all_models()         - List all embedding models   │
│  │                                                                   │
│  ├── prompt_manager.py          ★ PROMPT DB ★                       │
│  │   └── PromptManager (extends MongoDBManager)                     │
│  │       ├── add_prompt()             - Create new prompt           │
│  │       ├── get_all_prompts()        - List prompts                │
│  │       ├── search_prompts()         - Search by term/category     │
│  │       ├── update_prompt()          - Modify prompt               │
│  │       └── delete_prompt()          - Remove prompt               │
│  │                                                                   │
│  ├── document_utils.py                                              │
│  │   └── DocumentProcessor                                          │
│  │       ├── extract_text_from_pdf()  - PyMuPDF extraction          │
│  │       ├── extract_text_from_html() - BeautifulSoup parsing       │
│  │       ├── extract_text_from_url()  - URL content extraction      │
│  │       ├── load_documents_from_path() - LangChain doc loading     │
│  │       └── save_uploaded_file()     - File upload handling        │
│  │                                                                   │
│  ├── token_utils.py                                                 │
│  │   └── TokenManager                                               │
│  │       ├── count_tokens()           - tiktoken counting           │
│  │       ├── truncate_text()          - Limit by tokens             │
│  │       └── optimize_prompt()        - Reduce token usage          │
│  │                                                                   │
│  ├── session_manager.py                                             │
│  │   └── SessionStateManager                                        │
│  │       ├── initialize()             - Setup session state         │
│  │       ├── get() / set() / clear()  - State management            │
│  │       ├── add_search_to_history()  - Track searches              │
│  │       ├── add_message_to_chat()    - Chat history                │
│  │       └── get_search_history()     - Retrieve history            │
│  │                                                                   │
│  ├── dynamic_selector.py        ★ UI COMPONENTS ★                   │
│  │   └── DynamicModelSelector                                       │
│  │       ├── render_model_selector()  - Dynamic LLM dropdown        │
│  │       ├── render_embedding_selector() - Embedding dropdown       │
│  │       └── get_configured_providers() - Available providers       │
│  │                                                                   │
│  └── mongo_manager.py           ★ BASE CLASS ★                      │
│      └── MongoDBManager (Generic CRUD operations)                   │
│          ├── insert_one() / insert_many()                           │
│          ├── find() / find_one()                                    │
│          ├── update_one() / update_many()                           │
│          └── delete_one() / delete_many()                           │
│                                                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ uses
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  config/                                                             │
│  ├── settings.py                                                    │
│  │   └── Settings (class)                                           │
│  │       ├── MongoDB Configuration                                  │
│  │       │   ├── MONGODB_URI                                        │
│  │       │   ├── MONGODB_DATABASE                                   │
│  │       │   ├── MONGODB_COLLECTION_PROMPTS                         │
│  │       │   ├── MONGODB_COLLECTION_MODELS                          │
│  │       │   └── MONGODB_COLLECTION_EMBEDDINGS                      │
│  │       ├── Search APIs (Optional)                                 │
│  │       │   ├── GOOGLE_API_KEY                                     │
│  │       │   └── GOOGLE_CSE_ID                                      │
│  │       ├── Document Processing                                    │
│  │       │   ├── DEFAULT_CHUNK_SIZE                                 │
│  │       │   ├── DEFAULT_CHUNK_OVERLAP                              │
│  │       │   └── MAX_FILE_SIZE_MB                                   │
│  │       ├── Model Defaults                                         │
│  │       │   ├── DEFAULT_TEMPERATURE                                │
│  │       │   └── DEFAULT_MAX_TOKENS                                 │
│  │       └── Helper Methods                                         │
│  │           ├── is_mongodb_configured()                            │
│  │           └── ensure_directories()                               │
│  │                                                                   │
│  └── constants.py                                                   │
│      ├── ANALYSIS_TYPES                                             │
│      ├── OUTPUT_FORMATS                                             │
│      ├── SEARCH_SOURCES                                             │
│      ├── PROMPT_CATEGORIES                                          │
│      ├── UI_MESSAGES                                                │
│      ├── EXAMPLE_QUERIES                                            │
│      ├── RAG_EXAMPLE_QUESTIONS                                      │
│      └── MODEL_PARAMS                                               │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              │ reads from
                              │
┌─────────────────────────────────────────────────────────────────────┐
│                   EXTERNAL DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  .env (Environment Variables - MongoDB & Optional Settings Only)     │
│  ├── MONGODB_URI=mongodb://localhost:27017/                         │
│  ├── MONGODB_DATABASE=research_assistant                            │
│  ├── GOOGLE_API_KEY=...         (Optional)                          │
│  ├── GOOGLE_CSE_ID=...          (Optional)                          │
│  └── DEFAULT_CHUNK_SIZE=1000    (Optional)                          │
│                                                                       │
│  .streamlit/                                                         │
│  ├── config.toml                - Streamlit configuration           │
│  ├── config.yaml                - Authentication                    │
│  └── pages_sections.toml        - Navigation structure              │
│                                                                       │
│  MongoDB Collections                                                 │
│  ├── models                     - LLM provider configurations        │
│  │   ├── provider: "openai"                                         │
│  │   ├── name: "OpenAI"                                             │
│  │   ├── api_key_env: "OPENAI_API_KEY"                              │
│  │   ├── models: ["gpt-4o", "gpt-4o-mini", ...]                     │
│  │   └── requires_api_key: true                                     │
│  │                                                                   │
│  ├── embedding_models           - Embedding provider configurations  │
│  │   ├── provider: "openai"                                         │
│  │   ├── models: [                                                  │
│  │   │     {model_id, name, dimensions, max_input, description}     │
│  │   │   ]                                                           │
│  │   └── requires_api_key: true                                     │
│  │                                                                   │
│  └── prompts                    - User-created research prompts      │
│      ├── title: "Paper Analysis"                                    │
│      ├── category: "research"                                       │
│      ├── value: "Analyze this paper..."                             │
│      ├── variables: ["paper_title", "focus_area"]                   │
│      └── tags: ["analysis", "methodology"]                          │
│                                                                       │
│  Seeding Scripts (Initial Data Population)                          │
│  ├── scripts/seed_language_models.py    - Populate LLM providers    │
│  ├── scripts/seed_embedding_models.py   - Populate embeddings       │
│  └── scripts/seed_prompts.py            - Default prompts           │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Architectural Patterns

### 1. **Runtime Configuration Pattern**

**Traditional Approach** (Not Used):
```
Environment Variables → Application Startup → Fixed Configuration
```

**Our Approach**:
```
MongoDB → LLM Manager → Runtime Loading → User UI Configuration
                     ↓
              Session Storage → Per-User Credentials
```

**Benefits**:
- ✅ Multi-user support with different providers
- ✅ No restart needed for configuration changes
- ✅ Secure session-based credential storage
- ✅ Easy to add new providers without code changes

### 2. **Dynamic Provider Registry**

```python
# MongoDB stores provider metadata
{
  "provider": "openai",
  "name": "OpenAI",
  "models": ["gpt-4o", "gpt-4o-mini"],
  "requires_api_key": true
}

# LLMManager loads at runtime
providers = model_manager.get_all_providers()

# User configures via UI
CredentialsManager.set_credential("openai", api_key="sk-...")

# LLM initialized dynamically
llm = llm_manager.initialize_model(
    provider="openai",
    model="gpt-4o"
)
```

---

## Data Flow Diagram

### Example 1: Research Paper Search with Dynamic LLM

```
┌──────────┐
│   User   │ Enter query + select provider/model
└────┬─────┘
     │
     ▼
┌─────────────────────────────┐
│ 01_research_assistant.py    │ UI handles input
│ - Dynamic model selector    │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ DynamicModelSelector        │ Get available providers
│ - get_configured_providers()│
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ CredentialsManager          │ Check which providers have keys
│ - has_credential()          │
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ ResearchSearcher (core)     │ Orchestrate search
│ - search_all_sources()      │
└────┬────────────────────────┘
     │
     ├────────────────────┬─────────────────────┬──────────────────┐
     │                    │                     │                  │
     ▼                    ▼                     ▼                  ▼
┌──────────┐      ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
│ ArxivSrv │      │ SemanticSrv  │    │ SearchSrv    │   │ SearchSrv    │
│ search() │      │ search()     │    │ google_srch()│   │ ddg_search() │
└────┬─────┘      └──────┬───────┘    └──────┬───────┘   └──────┬───────┘
     │                   │                   │                  │
     └───────────────────┴───────────────────┴──────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Aggregate       │
                     │ Results         │
                     └────┬────────────┘
                          │
                          ▼
                   ┌──────────────────┐
                   │ SessionManager   │ Store results
                   │ .set(RESULTS)    │
                   └────┬─────────────┘
                        │
                        ▼
                   ┌──────────────────┐
                   │ Display Results  │ Show in UI
                   │ with AI Summary  │
                   └──────────────────┘
```

### Example 2: RAG Chat with Runtime LLM Configuration

```
User                Settings Page       RAGSystem        LLMManager      Embedding
 │                       │                   │                │              │
 │  Configure OpenAI     │                   │                │              │
 ├──────────────────────>│                   │                │              │
 │                       │  set_credential() │                │              │
 │                       ├──────────────────>│                │              │
 │                       │  (store in session)                │              │
 │                       │<──────────────────┤                │              │
 │                       │                   │                │              │
 │  Upload PDF           │                   │                │              │
 ├──────────────────────────────────────────>│                │              │
 │                       │  create_retriever()                │              │
 │                       │                   ├───────────────>│              │
 │                       │                   │  init_model()  │              │
 │                       │                   │<───────────────┤              │
 │                       │                   │                │  embed_docs  │
 │                       │                   ├───────────────────────────────>│
 │                       │                   │<───────────────────────────────┤
 │                       │<──────────────────┤                │              │
 │                       │                   │                │              │
 │  Ask Question         │                   │                │              │
 ├──────────────────────────────────────────>│                │              │
 │                       │  query(question)  │                │              │
 │                       │                   │  get_credentials()            │
 │                       │                   ├───────────────>│              │
 │                       │                   │<───────────────┤              │
 │                       │                   │  init_llm()    │              │
 │                       │                   ├───────────────>│              │
 │                       │                   │<───────────────┤              │
 │                       │                   │  retrieve_docs │              │
 │                       │                   ├───────────────────────────────>│
 │                       │                   │<───────────────────────────────┤
 │                       │                   │  generate()    │              │
 │                       │                   ├───────────────>│              │
 │                       │                   │<───────────────┤              │
 │                       │<──────────────────┤                │              │
 │<──────────────────────────────────────────┤                │              │
 │  Display Answer       │                   │                │              │
```

### Example 3: LLM Provider Initialization Flow

```
Application Startup
        │
        ▼
┌──────────────────┐
│ LLMManager.init()│
└────┬─────────────┘
     │
     ▼
┌────────────────────────┐
│ Check MongoDB          │
│ - MONGODB_URI set?     │
└────┬───────────────────┘
     │
     ├─── Yes ──────────────────────┐
     │                              │
     ▼                              │
┌────────────────────────┐          │
│ ModelManager           │          │
│ - get_all_providers()  │          │
└────┬───────────────────┘          │
     │                              │
     ▼                              │
┌────────────────────────┐          │
│ Load from MongoDB      │          │
│ - 15+ providers        │          │
│ - Provider metadata    │          │
│ - Model lists          │          │
└────┬───────────────────┘          │
     │                              │
     └──────────────────────────────┤
                                    │
     ├─── No ───────────────────────┘
     │
     ▼
┌────────────────────────┐
│ Use fallback providers │
│ - OpenAI only          │
└────┬───────────────────┘
     │
     ▼
┌────────────────────────┐
│ Cache providers list   │
│ - SUPPORTED_PROVIDERS  │
└────┬───────────────────┘
     │
     ▼
┌────────────────────────┐
│ Ready for runtime      │
│ configuration          │
└────────────────────────┘

User Runtime Flow:
        │
        ▼
┌──────────────────────────┐
│ User goes to Settings    │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Select provider from     │
│ SUPPORTED_PROVIDERS list │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Enter API key            │
│ (stored in session only) │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ LLMManager.initialize()  │
│ - Get credentials        │
│ - Create LLM instance    │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Test connection          │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│ Provider ready to use    │
│ across all pages         │
└──────────────────────────┘
```

## Module Dependency Graph

---

## Module Dependency Graph

```
streamlit_app.py
 │
 └─> pages/*
      ├─> src/core/*
      │    ├─> src/services/llm_manager.py ★ CENTRAL SERVICE ★
      │    │    ├─> src/utils/model_manager.py (MongoDB)
      │    │    ├─> src/utils/credentials_manager.py (Session)
      │    │    └─> langchain.chat_models.init_chat_model
      │    │         ├─> OpenAI API
      │    │         ├─> Anthropic API
      │    │         ├─> Google API
      │    │         ├─> AWS Bedrock
      │    │         ├─> Cohere API
      │    │         ├─> Groq API
      │    │         ├─> Together API
      │    │         ├─> Mistral API
      │    │         ├─> HuggingFace
      │    │         ├─> Ollama (Local)
      │    │         └─> 5+ more providers
      │    │
      │    ├─> src/services/arxiv_service.py
      │    │    └─> ArXiv API
      │    │
      │    ├─> src/services/semantic_scholar_service.py
      │    │    └─> Semantic Scholar API
      │    │
      │    └─> src/services/search_service.py
      │         ├─> Google Custom Search API
      │         └─> DuckDuckGo Search
      │
      ├─> src/utils/*
      │    ├─> credentials_manager.py (Session-based storage)
      │    ├─> model_manager.py (MongoDB interface)
      │    ├─> embedding_model_manager.py (MongoDB interface)
      │    ├─> prompt_manager.py (MongoDB interface)
      │    ├─> document_utils.py (PyMuPDF, BeautifulSoup)
      │    ├─> token_utils.py (tiktoken)
      │    ├─> session_manager.py (Streamlit state)
      │    ├─> dynamic_selector.py (UI components)
      │    └─> mongo_manager.py (Base CRUD)
      │
      └─> config/*
           ├─> settings.py (Environment Vars - MongoDB only)
           └─> constants.py (Application constants)
```

### Dependency Layers

**Layer 1: Configuration & Database**
- MongoDB (provider registry, embeddings, prompts)
- .env (MongoDB URI only)
- config/settings.py

**Layer 2: Data Access & Utilities**
- mongo_manager.py (Base CRUD)
- model_manager.py (LLM providers)
- embedding_model_manager.py (Embeddings)
- prompt_manager.py (Prompts)
- credentials_manager.py (Session storage)

**Layer 3: Services**
- llm_manager.py (Multi-provider LLM)
- arxiv_service.py
- semantic_scholar_service.py
- search_service.py

**Layer 4: Core Business Logic**
- research_search.py
- paper_analyzer.py
- rag_system.py

**Layer 5: UI**
- Streamlit pages
- dynamic_selector.py (UI widgets)
- LLMConfigWidget (Settings UI)

---

## Component Interaction Matrix

| Component | Uses | Used By | Purpose |
|-----------|------|---------|---------|
| **Pages** | Core, Utils, Config | streamlit_app.py | User interface |
| **Core (ResearchSearcher)** | Services, Utils | Pages | Search orchestration |
| **Core (PaperAnalyzer)** | LLMManager, Utils | Pages | Paper analysis |
| **Core (RAGSystem)** | LLMManager, Utils | Pages | RAG retrieval & generation |
| **LLMManager** | ModelManager, CredentialsManager, LangChain | Core, Pages | Dynamic LLM initialization |
| **ModelManager** | MongoDBManager | LLMManager | Provider registry |
| **CredentialsManager** | Session State | LLMManager, Pages | Runtime API key storage |
| **EmbeddingModelManager** | MongoDBManager | RAGSystem, Pages | Embedding registry |
| **PromptManager** | MongoDBManager | Pages | Prompt library |
| **DocumentProcessor** | PyMuPDF, BeautifulSoup | Core, Pages | PDF/HTML processing |
| **TokenManager** | tiktoken | Core, Services | Token counting |
| **SessionManager** | Streamlit State | Pages | State management |
| **DynamicSelector** | CredentialsManager, ModelManager | Pages | Model selection UI |
| **Settings** | Environment Vars | All Layers | Configuration |
| **Constants** | - | All Layers | Static values |

---

## Security Architecture

### API Key Management

**Session-Based Storage**:
```python
# Keys stored in browser session only
st.session_state["llm_credentials"] = {
    "openai": {"api_key": "sk-..."},
    "anthropic": {"api_key": "sk-ant-..."}
}

# Never persisted to disk or database
# Cleared on browser close
# Separate per user session
```

**Flow**:
```
User enters API key → CredentialsManager → Session State → LLMManager uses
                                                             ↓
                                                      Never saved to:
                                                      - .env
                                                      - MongoDB
                                                      - Disk
                                                      - Logs
```

### MongoDB Security

**What's Stored**:
- ✅ Provider metadata (name, models, requirements)
- ✅ Embedding model specifications
- ✅ User-created prompts
- ❌ API keys (NEVER stored)
- ❌ User credentials
- ❌ Sensitive data

**Connection Security**:
```python
# .env configuration
MONGODB_URI=mongodb://user:pass@host:27017/?authSource=admin&ssl=true

# Production recommendations:
# - Enable authentication
# - Use TLS/SSL
# - Restrict IP access
# - Use MongoDB Atlas with encryption
```

---

## Performance Optimization

### 1. Provider Caching

```python
# LLMManager caches provider list
_providers_cache = None  # Load once from MongoDB

def SUPPORTED_PROVIDERS():
    if _providers_cache is not None:
        return _providers_cache  # Return cached
    
    # Load from MongoDB only first time
    providers = model_manager.get_all_providers()
    _providers_cache = providers
    return providers
```

### 2. Session State Management

```python
# Centralized session management
SessionStateManager.initialize()  # Once per session

# Efficient state access
results = SessionStateManager.get("search_results")
SessionStateManager.set("search_results", new_results)
```

### 3. Document Processing

```python
# Chunking strategies
chunk_size = 1000  # Optimized for most models
chunk_overlap = 200  # Balance between context and redundancy

# Token limiting
TokenManager.truncate_text(text, max_tokens=100000)
```

### 4. Database Queries

```python
# Indexed fields
db.models.create_index({"provider": 1})
db.embedding_models.create_index({"provider": 1})
db.prompts.create_index({"category": 1, "tags": 1})

# Efficient queries
model_manager.get_provider_by_id("openai")  # Indexed lookup
prompt_manager.get_prompts_by_category("research")  # Indexed
```

---

## Sequence Diagram: RAG Chat

```
User                  RAG Page           RAGSystem          OpenAI
 │                       │                   │                │
 │  Upload PDF           │                   │                │
 ├──────────────────────>│                   │                │
 │                       │  create_retriever()│                │
 │                       ├──────────────────>│                │
 │                       │                   │  Embed chunks  │
 │                       │                   ├───────────────>│
 │                       │                   │<───────────────┤
 │                       │<──────────────────┤                │
 │  Ask Question         │                   │                │
 ├──────────────────────>│                   │                │
 │                       │  query(question)  │                │
 │                       ├──────────────────>│                │
 │                       │                   │  Retrieve docs │
 │                       │                   │  + Generate    │
 │                       │                   ├───────────────>│
 │                       │                   │<───────────────┤
 │                       │<──────────────────┤                │
 │<──────────────────────┤                   │                │
 │  Display Answer       │                   │                │
```

---

## Technology Stack

### Frontend
- **Streamlit**: Web framework
- **st-pages**: Page navigation
- **streamlit-authenticator**: User authentication

### LLM & AI
- **LangChain**: LLM orchestration framework
- **LangChain Community**: Provider integrations
- **15+ LLM Providers**:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Google (Gemini, Vertex AI)
  - AWS Bedrock
  - Azure OpenAI
  - Cohere
  - Together AI
  - Groq
  - Mistral AI
  - HuggingFace
  - Ollama (Local)
  - DeepSeek
  - Perplexity
  - xAI (Grok)
  - NVIDIA AI

### Vector Storage & Embeddings
- **ChromaDB**: Vector database for RAG
- **Multiple Embedding Providers**:
  - OpenAI Embeddings
  - Cohere Embeddings
  - Google Embeddings
  - HuggingFace Embeddings
  - Sentence Transformers

### Document Processing
- **PyMuPDF**: PDF text extraction
- **BeautifulSoup4**: HTML parsing
- **tiktoken**: Token counting
- **LangChain Text Splitters**: Document chunking

### Search & APIs
- **arxiv**: ArXiv API client
- **semanticscholar**: Semantic Scholar API
- **duckduckgo-search**: DuckDuckGo search
- **Google Custom Search**: Google Scholar integration

### Database
- **MongoDB**: Provider registry, embeddings, prompts
- **PyMongo**: MongoDB Python driver

### Utilities
- **python-dotenv**: Environment variable management
- **pyyaml**: YAML configuration
- **pydantic**: Data validation

---

## Design Patterns Implemented

### 1. **Service Layer Pattern**
```python
# External API interactions isolated in services
class LLMManager:
    def initialize_model(provider, model):
        # Handle all LLM initialization logic
        pass

# Used by core modules
llm = llm_manager.initialize_model("openai", "gpt-4o")
```

### 2. **Repository Pattern**
```python
# Data access abstracted through managers
class ModelManager(MongoDBManager):
    def get_all_providers():
        return self.find()  # MongoDB query abstracted

# Used by services
providers = model_manager.get_all_providers()
```

### 3. **Facade Pattern**
```python
# Core modules provide simple interfaces
class ResearchSearcher:
    def search_all_sources(query):
        # Orchestrates multiple services
        arxiv_results = self.search_arxiv(query)
        semantic_results = self.search_semantic(query)
        return self.aggregate(arxiv_results, semantic_results)
```

### 4. **Singleton Pattern**
```python
# Settings and managers as class-level singletons
class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    # Shared configuration across app

class SessionStateManager:
    @staticmethod
    def initialize():
        # Single session state initialization
```

### 5. **Factory Pattern**
```python
# Dynamic service creation
class LLMManager:
    def initialize_model(provider, model, **kwargs):
        # Create appropriate LLM instance based on provider
        return init_chat_model(
            model=model,
            model_provider=provider,
            **kwargs
        )
```

### 6. **Strategy Pattern**
```python
# Different analysis strategies
ANALYSIS_TYPES = {
    "full": FullAnalysisStrategy(),
    "methodology": MethodologyStrategy(),
    "findings": FindingsStrategy()
}

# Selected at runtime
analysis = ANALYSIS_TYPES[user_choice].analyze(paper)
```

### 7. **Dependency Injection**
```python
# Services accept configuration
class RAGSystem:
    def __init__(self, llm, embeddings, chunk_size):
        self.llm = llm  # Injected
        self.embeddings = embeddings  # Injected
        self.chunk_size = chunk_size  # Injected
```

### 8. **Builder Pattern**
```python
# Complex prompt construction
class PaperAnalyzer:
    def _build_analysis_prompt(self, analysis_type, custom_prompt):
        # Build prompt step by step
        prompt = base_prompt
        if analysis_type:
            prompt += type_instructions
        if custom_prompt:
            prompt += custom_prompt
        return prompt
```

---

## Scalability Considerations

### Horizontal Scaling
- **Stateless Pages**: Each page can run independently
- **Session State**: Browser-side storage
- **MongoDB**: Distributed database support
- **Multi-User**: Separate credentials per session

### Vertical Scaling
- **Lazy Loading**: Providers loaded on demand
- **Caching**: Provider list cached in memory
- **Batch Processing**: Multiple papers analyzed in parallel
- **Token Management**: Automatic text truncation

### Database Scaling
- **MongoDB Sharding**: Horizontal database scaling
- **Indexed Queries**: Optimized lookups
- **Connection Pooling**: Efficient connections
- **Atlas Support**: Cloud-native scaling

### API Rate Limiting
- **Per-Provider Limits**: Respect individual API limits
- **Retry Logic**: Exponential backoff
- **Queue System**: Background job processing (future)
- **Usage Tracking**: Monitor and alert on limits

---

## Error Handling Strategy

### 1. Graceful Degradation
```python
# Fallback to basic providers if MongoDB fails
if not mongodb_connected:
    use_fallback_providers = {"openai": {...}}
```

### 2. User-Friendly Messages
```python
try:
    result = perform_action()
except APIError as e:
    st.error(f"❌ API Error: {user_friendly_message(e)}")
    st.info("💡 Try: Check API key, credits, or try again later")
```

### 3. Retry Mechanisms
```python
@retry(max_attempts=3, backoff=exponential)
def api_call():
    # Automatic retries on failure
    pass
```

### 4. Validation
```python
# Input validation before processing
if not query or len(query) < 3:
    st.warning("Please enter a valid search query (min 3 characters)")
    return
```

---

## Future Enhancements

### Planned Architecture Improvements

1. **Microservices**
   - Separate LLM service
   - Dedicated search service
   - Background job processor

2. **Caching Layer**
   - Redis for session data
   - Cache provider responses
   - Cached embeddings

3. **Message Queue**
   - RabbitMQ/Celery for async jobs
   - Background paper processing
   - Scheduled tasks

4. **API Gateway**
   - REST API endpoints
   - Rate limiting per user
   - API key management

5. **Analytics**
   - Usage tracking
   - Cost monitoring
   - Performance metrics

6. **Multi-Tenancy**
   - Organization support
   - Shared workspaces
   - Role-based access control

---

## Architectural Benefits

### ✅ Maintainability
- Clear module boundaries
- Single responsibility principle
- Easy to locate and fix bugs
- Consistent patterns throughout

### ✅ Testability
- Service layer can be mocked
- Core logic isolated from UI
- Database interactions abstracted
- Unit testable components

### ✅ Scalability
- Stateless design
- Database-backed configuration
- Horizontal scaling ready
- Multi-user support

### ✅ Security
- Session-based credentials
- No API keys in database
- Secure MongoDB connections
- Input validation throughout

### ✅ Flexibility
- Easy to add new LLM providers
- Pluggable embedding models
- Customizable analysis types
- Extensible prompt library

### ✅ User Experience
- Runtime configuration (no restart)
- Switch providers seamlessly
- Multi-provider comparison
- Intuitive UI components

---

**This architecture provides a solid foundation for a production-ready, multi-user, scalable research platform with enterprise-grade LLM integration capabilities.**
