# 🔬 Research Assistant Platform v2.0

A comprehensive, modular Streamlit application for AI-powered research paper analysis, multi-source search, and document interaction.

## ✨ Features

- **🔍 Multi-Source Search**: Search across ArXiv, Semantic Scholar, Google Scholar, and DuckDuckGo
- **📄 AI-Powered Analysis**: Analyze research papers with GPT models
- **💬 RAG Chat System**: Interactive Q&A with your documents using Retrieval Augmented Generation
- **📝 Prompt Management**: Store and organize reusable research prompts
- **⚙️ Easy Configuration**: Simple setup with environment variables

## 🏗️ Architecture

The application follows a clean, modular architecture:

```
research-v1/
├── app.py                          # Main application entry point
├── pages/                          # Streamlit pages (refactored)
│   ├── 00_home.py
│   ├── 01_research_assistant.py
│   ├── 02_paper_analyzer.py
│   ├── 03_rag_chat.py
│   ├── 04_prompt_manager.py
│   └── 05_settings.py
├── src/
│   ├── core/                       # Core business logic
│   │   ├── __init__.py
│   │   ├── rag_system.py          # RAG operations
│   │   ├── paper_analyzer.py      # Paper analysis
│   │   └── research_search.py     # Multi-source search
│   ├── services/                   # External API integrations
│   │   ├── __init__.py
│   │   ├── openai_service.py      # OpenAI API
│   │   ├── arxiv_service.py       # ArXiv API
│   │   ├── semantic_scholar_service.py
│   │   └── search_service.py      # Google/DDG search
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       ├── document_utils.py      # PDF/document processing
│       ├── token_utils.py         # Token management
│       ├── session_manager.py     # Session state management
│       ├── mongo_utils.py         # MongoDB prompt management
│       └── mongo_manager.py       # Generic MongoDB operations
├── config/                         # Configuration management
│   ├── __init__.py
│   ├── settings.py                # Environment settings
│   └── constants.py               # Application constants
├── .streamlit/
│   ├── config.yaml                # Auth configuration
│   └── pages_sections.toml        # Navigation configuration
├── requirements-clean.txt          # Cleaned dependencies
├── .env.example                    # Environment template
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd research-v1

# Install dependencies
pip install -r requirements-clean.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your preferred editor
```

**Required:**
- `OPENAI_API_KEY`: Get from https://platform.openai.com/

**Optional:**
- `GOOGLE_API_KEY` & `GOOGLE_CSE_ID`: For Google Scholar search
- `MONGODB_URI`: For prompt management

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📚 Key Improvements in v2.0

### 🎯 Architecture
- **Separation of Concerns**: Business logic separated from UI (core/services/utils)
- **Service Layer**: Each external API has its own service class
- **Modular Core**: RAG, Analysis, and Search are independent modules
- **Centralized Config**: All settings in one place

### 🧹 Code Quality
- **No sys.path Hacks**: Proper Python package structure
- **Type Hints**: Better code documentation and IDE support
- **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
- **Session Management**: Centralized session state handling

### 📦 Dependencies
- **Cleaned Requirements**: Only used libraries included
- **Version Constraints**: Proper version pinning for stability
- **Organized by Category**: Easy to understand what each library does

### 🔧 Configuration
- **Environment Variables**: All config via .env file
- **Settings Class**: Type-safe access to configuration
- **Constants Module**: Centralized constants and UI messages

## 🔑 Environment Variables

### Core Settings
```bash
OPENAI_API_KEY=sk-...                              # Required
DEFAULT_MODEL=gpt-4o-mini                          # Optional
DEFAULT_TEMPERATURE=0.0                            # Optional
```

### Search APIs (Optional)
```bash
GOOGLE_API_KEY=...                                 # For Google Scholar
GOOGLE_CSE_ID=...                                  # Custom Search Engine ID
```

### Database (Optional)
```bash
MONGODB_URI=mongodb://localhost:27017/             # For prompt management
MONGODB_DATABASE=research_assistant
```

### Processing Settings
```bash
DEFAULT_CHUNK_SIZE=1000                            # RAG chunk size
DEFAULT_CHUNK_OVERLAP=200                          # Chunk overlap
MAX_TOKEN_LIMIT=100000                             # Max tokens per request
```

## 📖 Usage Guide

### Research Assistant
1. Enter your research query
2. Select databases to search (ArXiv, Semantic Scholar, etc.)
3. Configure advanced options if needed
4. Click "Search Papers"
5. Review and export results

### Paper Analyzer
1. Upload PDF files
2. Choose analysis type (Full, Methodology, Findings, etc.)
3. Configure model settings
4. Click "Analyze Papers"
5. Review structured analysis results

### RAG Chat System
1. Upload research documents (PDFs)
2. Wait for processing and indexing
3. Ask questions about your documents
4. Get AI-powered answers with context

### Prompt Manager
1. Create reusable research prompts
2. Organize by category and tags
3. Search existing prompts
4. Edit and update prompts

### Settings
1. Configure API keys
2. Adjust model parameters
3. Set document processing options
4. View system status

## 🔒 Authentication

The application uses `streamlit-authenticator` for user authentication. Configure users in `.streamlit/config.yaml`:

```yaml
credentials:
  usernames:
    your_username:
      email: your@email.com
      name: Your Name
      password: hashed_password  # Use bcrypt hash
```

## 🛠️ Development

### Adding a New Page
1. Create file in `pages/` directory (e.g., `06_new_feature.py`)
2. Add entry to `.streamlit/pages_sections.toml`
3. Use `SessionStateManager` for state management
4. Follow existing page structure

### Adding a New Service
1. Create service class in `src/services/`
2. Inherit from base patterns
3. Add to `src/services/__init__.py`
4. Use in core modules

### Testing
```bash
# Run tests (when implemented)
pytest tests/

# With coverage
pytest --cov=src tests/
```

## 📝 Migration from v1.0

If you're upgrading from the old version:

1. **Update imports**: Change from `from src.core.research_app import ResearchApp` to new modular imports
2. **Use new services**: Replace direct API calls with service classes
3. **Update config**: Move hardcoded values to `.env`
4. **Session state**: Use `SessionStateManager` instead of direct `st.session_state`

Example:
```python
# Old way
from src.core.research_app import ResearchApp
research_app = ResearchApp()
results = research_app.arxiv_search_agent(query)

# New way
from src.services.arxiv_service import ArxivService
arxiv = ArxivService()
results = arxiv.search_with_agent(query)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

See LICENSE file for details.

## 🐛 Troubleshooting

### Import Errors
- Ensure you're running from the project root
- Check that `PYTHONPATH` includes the project directory
- Verify all dependencies are installed: `pip install -r requirements-clean.txt`

### API Errors
- Verify API keys in `.env` file
- Check API key validity and credits
- Ensure internet connection is stable

### MongoDB Errors
- MongoDB is optional; the app works without it
- If using MongoDB, verify connection string
- Check MongoDB service is running

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review error messages in the Streamlit interface

---

**Built with ❤️ using Streamlit, LangChain, and OpenAI**
