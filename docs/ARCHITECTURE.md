# 🏗️ Architecture Diagram - Research Assistant v2.0

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                         │
│                            (Streamlit)                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  app.py (Entry Point)                                                │
│  ├── Authentication                                                  │
│  └── Navigation                                                      │
│                                                                       │
│  pages/                                                              │
│  ├── 00_home.py            - Dashboard & Quick Access               │
│  ├── 01_research_assistant.py - Multi-source Paper Search           │
│  ├── 02_paper_analyzer.py     - PDF Analysis                        │
│  ├── 03_rag_chat.py           - Document Q&A                        │
│  ├── 04_prompt_manager.py     - Prompt CRUD                         │
│  └── 05_settings.py           - Configuration                       │
│                                                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ uses
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CORE BUSINESS LOGIC LAYER                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  src/core/                                                           │
│  ├── research_search.py                                             │
│  │   └── ResearchSearcher                                           │
│  │       ├── search_all_sources()                                   │
│  │       ├── search_arxiv()                                         │
│  │       ├── search_semantic_scholar()                              │
│  │       └── search_google/duckduckgo()                             │
│  │                                                                   │
│  ├── paper_analyzer.py                                              │
│  │   └── PaperAnalyzer                                              │
│  │       ├── analyze_pdf()                                          │
│  │       ├── analyze_multiple_pdfs()                                │
│  │       └── _build_analysis_prompt()                               │
│  │                                                                   │
│  └── rag_system.py                                                  │
│      └── RAGSystem                                                  │
│          ├── create_retriever()                                     │
│          └── query()                                                │
│                                                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ depends on
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SERVICES LAYER (API Integrations)                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  src/services/                                                       │
│  ├── openai_service.py                                              │
│  │   └── OpenAIService                                              │
│  │       ├── chat_completion()                                      │
│  │       ├── simple_query()                                         │
│  │       ├── structured_query()                                     │
│  │       └── analyze_paper()                                        │
│  │                                                                   │
│  ├── arxiv_service.py                                               │
│  │   └── ArxivService                                               │
│  │       ├── search_with_agent()                                    │
│  │       ├── load_documents_from_query()                            │
│  │       └── load_document_by_id()                                  │
│  │                                                                   │
│  ├── semantic_scholar_service.py                                    │
│  │   └── SemanticScholarService                                     │
│  │       └── search()                                               │
│  │                                                                   │
│  └── search_service.py                                              │
│      └── SearchService                                              │
│          ├── google_search()                                        │
│          └── duckduckgo_search()                                    │
│                                                                       │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ uses
                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        UTILITIES LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  src/utils/                                                          │
│  ├── document_utils.py                                              │
│  │   └── DocumentProcessor                                          │
│  │       ├── extract_text_from_pdf()                                │
│  │       ├── extract_text_from_html()                               │
│  │       ├── extract_text_from_url()                                │
│  │       ├── load_documents_from_path()                             │
│  │       └── save_uploaded_file()                                   │
│  │                                                                   │
│  ├── token_utils.py                                                 │
│  │   └── TokenManager                                               │
│  │       ├── count_tokens()                                         │
│  │       ├── truncate_text()                                        │
│  │       └── optimize_prompt()                                      │
│  │                                                                   │
│  ├── session_manager.py                                             │
│  │   └── SessionStateManager                                        │
│  │       ├── initialize()                                           │
│  │       ├── get() / set() / clear()                                │
│  │       ├── add_search_to_history()                                │
│  │       └── add_message_to_chat()                                  │
│  │                                                                   │
│  ├── mongo_utils.py                                                 │
│  │   └── PromptManager                                              │
│  │       ├── add_prompt()                                           │
│  │       ├── get_prompt_by_title()                                  │
│  │       ├── update_prompt()                                        │
│  │       └── delete_prompt()                                        │
│  │                                                                   │
│  └── mongo_manager.py                                               │
│      └── MongoDBManager (base class)                                │
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
│  │       ├── API Keys (OPENAI_API_KEY, etc.)                        │
│  │       ├── Model Configuration (DEFAULT_MODEL, etc.)              │
│  │       ├── Document Processing (CHUNK_SIZE, etc.)                 │
│  │       ├── Search Configuration (MAX_RESULTS, etc.)               │
│  │       ├── is_openai_configured()                                 │
│  │       ├── is_google_configured()                                 │
│  │       └── ensure_directories()                                   │
│  │                                                                   │
│  └── constants.py                                                   │
│      ├── ANALYSIS_TYPES                                             │
│      ├── OUTPUT_FORMATS                                             │
│      ├── SEARCH_SOURCES                                             │
│      ├── UI_MESSAGES                                                │
│      └── EXAMPLE_QUERIES                                            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘


                              ▲
                              │
                              │ reads from
                              │
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTERNAL CONFIGURATION                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  .env (Environment Variables)                                        │
│  ├── OPENAI_API_KEY                                                 │
│  ├── GOOGLE_API_KEY                                                 │
│  ├── MONGODB_URI                                                    │
│  └── DEFAULT_MODEL, CHUNK_SIZE, etc.                                │
│                                                                       │
│  .streamlit/                                                         │
│  ├── config.yaml (Authentication)                                   │
│  └── pages_sections.toml (Navigation)                               │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Example: Research Paper Search

```
┌──────────┐
│   User   │ Enter query, select sources
└────┬─────┘
     │
     ▼
┌─────────────────────────────┐
│ 01_research_assistant.py    │ UI handles input
└────┬────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│ ResearchSearcher (core)     │ Orchestrates search
│ - search_all_sources()      │
└────┬────────────────────────┘
     │
     ├─────────────────────┬─────────────────────┬──────────────────┐
     │                     │                     │                  │
     ▼                     ▼                     ▼                  ▼
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
                   │ in Tabs          │
                   └──────────────────┘
```

---

## Module Dependency Graph

```
app.py
 └─> pages/*
      ├─> src/core/*
      │    ├─> src/services/*
      │    │    ├─> OpenAI API
      │    │    ├─> ArXiv API
      │    │    ├─> Semantic Scholar API
      │    │    └─> Google/DDG Search
      │    ├─> src/utils/*
      │    │    ├─> PDF Processing (PyMuPDF)
      │    │    ├─> Token Management (tiktoken)
      │    │    └─> Document Loading (LangChain)
      │    └─> config/*
      │         ├─> settings.py (Environment Vars)
      │         └─> constants.py
      └─> src/utils/session_manager.py
           └─> Streamlit Session State
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

## Component Interaction Matrix

| Component | Uses | Used By |
|-----------|------|---------|
| Pages | Core, Utils, Config | app.py |
| Core (ResearchSearcher) | Services, Utils | Pages |
| Core (PaperAnalyzer) | Services, Utils | Pages |
| Core (RAGSystem) | Services, Utils | Pages |
| Services (OpenAI) | OpenAI API, Config | Core, Pages |
| Services (ArXiv) | ArXiv API, LangChain | Core |
| Services (Search) | Google/DDG APIs | Core |
| Utils (DocumentProcessor) | PyMuPDF, BeautifulSoup | Core, Pages |
| Utils (TokenManager) | tiktoken, Config | Core, Services |
| Utils (SessionManager) | Streamlit State | Pages |
| Config (Settings) | Environment Vars | All Layers |
| Config (Constants) | - | All Layers |

---

## File Size Comparison

### Before (v1.0)
```
research_app.py     ████████████████████████████████████ 402 lines
paper_analyzer.py   ███████████████████████████ 251 lines
research_assist.py  █████████████████████████ 236 lines
rag_chat.py         ███████████████████ 207 lines
```

### After (v2.0) - Largest Files
```
research_assistant.py  ████████████████████████████ 250 lines (UI)
home.py               ████████████████████ 180 lines (UI)
paper_analyzer.py     ███████████████ 140 lines (Core Logic)
research_search.py    ████████████ 120 lines (Core Logic)
document_utils.py     ████████████ 115 lines (Utils)
rag_system.py         ██████████ 100 lines (Core Logic)
openai_service.py     █████████ 95 lines (Service)
arxiv_service.py      █████████ 90 lines (Service)
```

**Result**: Maximum file size reduced from 402 to 250 lines (38% reduction)

---

## Design Patterns Used

1. **Service Layer Pattern**: External API interactions isolated
2. **Repository Pattern**: MongoDB manager for data access
3. **Facade Pattern**: Core modules provide simple interfaces
4. **Singleton Pattern**: Settings and SessionManager (via class methods)
5. **Factory Pattern**: Service creation with configuration
6. **Strategy Pattern**: Different analysis types, search sources
7. **Dependency Injection**: Services accept configuration

---

**This architecture provides:**
- ✅ Separation of concerns
- ✅ Testability
- ✅ Maintainability
- ✅ Scalability
- ✅ Clear dependencies
- ✅ Easy to understand
- ✅ Production-ready
