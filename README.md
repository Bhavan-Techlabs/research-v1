# 🔬 Research Assistant Platform

A comprehensive, production-ready Streamlit application for AI-powered academic research with **dynamic multi-LLM support**, multi-source search, intelligent document analysis, and RAG-powered chat capabilities.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://research-v1.streamlit.app/)

## ✨ Key Features

- **🤖 Multi-LLM Support**: Configure and switch between 15+ LLM providers at runtime (OpenAI, Anthropic, Google, AWS, Cohere, Groq, Together, Mistral, HuggingFace, Ollama, and more)
- **� Runtime Configuration**: Set API keys and model parameters directly in the UI - no environment variables needed for LLMs
- **�🔍 Multi-Source Research**: Search across ArXiv, Semantic Scholar, Google Scholar, and DuckDuckGo simultaneously
- **📄 Intelligent Paper Analysis**: Analyze research papers with your choice of AI model and custom prompts
- **💬 RAG Chat System**: Interactive document Q&A using Retrieval Augmented Generation with multiple embedding models
- **📝 Prompt Library**: MongoDB-powered prompt management for organizing and reusing research templates
- **🔢 Flexible Embeddings**: Support for OpenAI, Cohere, Google, HuggingFace, and local embedding models
- **🎨 Clean Architecture**: Modular, maintainable codebase with clear separation of concerns

## 🏗️ Architecture

The application follows a clean, service-oriented architecture with runtime LLM configuration:

```
research-v1/
├── streamlit_app.py               # Main application entry point
├── pages/                          # Streamlit pages
│   ├── 00_home.py                 # Dashboard with metrics
│   ├── 01_research_assistant.py   # Multi-source paper search
│   ├── 02_paper_analyzer.py       # AI-powered paper analysis
│   ├── 03_rag_chat.py             # Document Q&A with RAG
│   ├── 04_prompt_manager.py       # Prompt library management
│   └── 05_settings.py             # LLM & API configuration
├── src/
│   ├── core/                       # Core business logic
│   │   ├── research_search.py     # Multi-source search orchestration
│   │   ├── paper_analyzer.py      # Paper analysis engine
│   │   └── rag_system.py          # RAG retrieval & generation
│   ├── services/                   # External API integrations
│   │   ├── llm_manager.py         # Dynamic multi-LLM manager
│   │   ├── arxiv_service.py       # ArXiv API integration
│   │   ├── semantic_scholar_service.py
│   │   └── search_service.py      # Google/DuckDuckGo search
│   └── utils/                      # Utility modules
│       ├── credentials_manager.py # Runtime API key management
│       ├── model_manager.py       # LLM provider database (MongoDB)
│       ├── embedding_model_manager.py # Embedding provider database
│       ├── document_utils.py      # PDF/document processing
│       ├── prompt_manager.py      # Prompt library (MongoDB)
│       ├── session_manager.py     # Session state management
│       ├── dynamic_selector.py    # Dynamic model selection UI
│       └── token_utils.py         # Token counting & management
├── config/                         # Configuration
│   ├── settings.py                # Environment settings (MongoDB)
│   └── constants.py               # Application constants
├── scripts/                        # Database seeding scripts
│   ├── seed_language_models.py    # Populate LLM providers
│   ├── seed_embedding_models.py   # Populate embedding providers
│   └── seed_prompts.py            # Populate default prompts
├── .streamlit/
│   ├── config.toml                # Streamlit configuration
│   ├── config.yaml                # Authentication configuration
│   └── pages_sections.toml        # Navigation structure
└── requirements.txt                # Dependencies (15+ LLM providers)
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd research-v1

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup (Required)

This application uses MongoDB for storing:
- LLM provider configurations
- Embedding model configurations  
- User-created prompts

**Option A: Local MongoDB**
```bash
# Install MongoDB locally
# macOS
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community
```

**Option B: MongoDB Atlas (Cloud)**
1. Create free account at https://www.mongodb.com/cloud/atlas
2. Create a cluster and get connection string
3. Add connection string to `.env` file

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and configure MongoDB
nano .env  # or use your preferred editor
```

**Required Configuration:**
```bash
# MongoDB (Required)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=research_assistant
```

**Optional Configuration:**
```bash
# Search APIs (Optional - for Google Scholar)
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
```

### 4. Seed Database (First Time Setup)

```bash
# Populate LLM providers
python scripts/seed_language_models.py

# Populate embedding models
python scripts/seed_embedding_models.py

# (Optional) Add default prompts
python scripts/seed_prompts.py
```

### 5. Run the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at `http://localhost:8501`

### 6. Configure LLM Providers (In-App)

1. Navigate to **Settings** → **LLM Providers**
2. Add API keys for your preferred providers:
   - OpenAI (GPT-4, GPT-3.5)
   - Anthropic (Claude)
   - Google (Gemini)
   - And 12+ more providers
3. Test the connection
4. Start researching!

## 📚 Core Capabilities

### 🔍 Research Assistant
- **Multi-Database Search**: Query ArXiv, Semantic Scholar, Google Scholar, and DuckDuckGo simultaneously
- **AI-Enhanced Results**: Use any configured LLM to synthesize and summarize findings
- **Smart Filtering**: Filter by publication year, source, and relevance
- **Export Options**: Download results as CSV, JSON, or BibTeX
- **Search History**: Track and revisit previous searches

### 📄 Paper Analyzer
- **Flexible Analysis Types**: 
  - Full comprehensive analysis
  - Research questions & objectives
  - Methodology extraction
  - Key findings summary
  - Limitations & gaps identification
  - Citation analysis
- **Custom Prompts**: Write your own analysis instructions
- **Batch Processing**: Analyze multiple papers simultaneously
- **Multi-Model Support**: Compare results across different LLMs
- **Structured Output**: Get JSON or narrative text format

### 💬 RAG Chat System
- **Intelligent Q&A**: Ask questions about uploaded research documents
- **Context-Aware**: Uses semantic search to find relevant passages
- **Citation Support**: See which document sections informed each answer
- **Multi-Document**: Chat across multiple papers simultaneously
- **Configurable Embeddings**: Choose from OpenAI, Cohere, Google, or HuggingFace embeddings
- **Adjustable Parameters**: Fine-tune chunk size, overlap, and retrieval settings

### � Prompt Manager
- **Organized Library**: Store and categorize research prompts
- **Tags & Search**: Easily find prompts with tags and search
- **Variables Support**: Create reusable templates with placeholders
- **Categories**: Organize by research type, paper analysis, evaluation, etc.
- **Import/Export**: Share prompt collections with team members

### ⚙️ Settings & Configuration
- **Runtime LLM Setup**: Configure 15+ providers without touching environment variables:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude 3.5, Claude 3)
  - Google (Gemini 1.5 Pro/Flash)
  - AWS Bedrock (Multiple models)
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
- **API Key Management**: Secure, session-based credential storage
- **Model Testing**: Verify configuration before use
- **Preferences**: Set default models, temperature, tokens
- **Usage Stats**: Monitor API usage and costs

## 🔑 Configuration Details

### Required Environment Variables

Only MongoDB configuration is required via environment variables. All LLM configurations are done at runtime through the UI.

```bash
# MongoDB Configuration (Required)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=research_assistant

# MongoDB Collections (Optional - defaults shown)
MONGODB_COLLECTION_PROMPTS=prompts
MONGODB_COLLECTION_MODELS=models
MONGODB_COLLECTION_EMBEDDINGS=embedding_models
```

### Optional Environment Variables

```bash
# Search APIs (Optional - enhances Google Scholar search)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_custom_search_engine_id

# Document Processing (Optional - defaults shown)
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=200
MAX_TOKEN_LIMIT=100000
MAX_FILE_SIZE_MB=10

# Model Defaults (Optional)
DEFAULT_TEMPERATURE=0.0
DEFAULT_MAX_TOKENS=4000

# Search Configuration (Optional)
MAX_SEARCH_RESULTS=10
SEARCH_TIMEOUT=60
```

### Runtime LLM Configuration (No Environment Variables Needed!)

All LLM provider API keys are configured through the Settings page:

1. Go to **Settings** → **LLM Providers**
2. Select a provider from the list
3. Enter your API key
4. (Optional) Configure additional parameters (endpoint, project ID, etc.)
5. Test the connection
6. Start using the provider throughout the app

Your API keys are:
- ✅ Stored securely in browser session
- ✅ Never sent to any third parties except the LLM provider
- ✅ Not persisted to disk or database
- ✅ Cleared when you close the browser

## 📖 Usage Guide

### Getting Started

1. **Initial Setup**
   - Ensure MongoDB is running
   - Run seeding scripts to populate providers
   - Launch the application

2. **Configure Your First LLM**
   - Navigate to **Settings** page
   - Go to **LLM Providers** tab
   - Select a provider (e.g., OpenAI)
   - Enter your API key
   - Click "Test Connection"

3. **Start Researching!**

### Research Assistant

**Search for Papers:**
1. Enter your research query
2. Select databases to search (ArXiv, Semantic Scholar, etc.)
3. Choose your preferred LLM and model
4. Configure advanced options (max results, year filter)
5. Click "Search Papers"
6. Review results with AI-generated summaries
7. Export results in your preferred format

**Pro Tips:**
- Use multiple sources for comprehensive coverage
- Enable "Include Abstracts" for better context
- Filter by publication year for recent research
- Save searches to history for later reference

### Paper Analyzer

**Analyze Research Papers:**
1. Upload one or more PDF files
2. Select provider and model
3. Choose analysis type or write custom prompt
4. Adjust temperature and max tokens
5. Click "Analyze"
6. Review structured insights
7. Download analysis results

**Analysis Types:**
- **Full Analysis**: Comprehensive overview of the paper
- **Research Questions**: Extract objectives and hypotheses
- **Methodology**: Detail the research methods used
- **Key Findings**: Summarize main results and conclusions
- **Limitations**: Identify gaps and areas for improvement
- **Citation Analysis**: Examine references and impact

**Batch Processing:**
- Upload multiple papers at once
- Same analysis applied to all papers
- Results organized by paper
- Export all analyses together

### RAG Chat System

**Chat with Your Documents:**
1. Upload research documents (PDFs)
2. Select LLM provider and model
3. Choose embedding model for retrieval
4. Configure RAG settings (chunk size, overlap)
5. Wait for document processing
6. Ask questions about your documents
7. Get AI-powered answers with source citations

**Effective Prompting:**
- Ask specific questions about methodology, findings, or conclusions
- Request comparisons between papers
- Ask for summaries of specific sections
- Query about limitations or future work

**Example Questions:**
- "What methodology was used in this study?"
- "What are the main findings across all papers?"
- "How do these papers compare in their approach?"
- "What are the limitations mentioned?"

### Prompt Manager

**Organize Your Research Templates:**

1. **Create Prompts**
   - Click "Create New Prompt"
   - Enter title and category
   - Write prompt with variables (use `{variable_name}`)
   - Add tags for organization
   - Save

2. **Use Prompts**
   - Browse by category or search
   - View prompt details
   - Copy to use in Paper Analyzer or RAG Chat
   - Edit or delete as needed

3. **Best Practices**
   - Use descriptive titles
   - Organize with categories and tags
   - Include clear variable placeholders
   - Add helpful descriptions

### Settings Management

**LLM Providers Tab:**
- Add/update API keys for multiple providers
- Test connections before use
- View configured providers
- Switch between providers anytime

**Preferences Tab:**
- Set default LLM and model
- Configure default temperature
- Set max tokens
- Adjust document processing parameters

**Usage Stats Tab:**
- Monitor API usage
- Track costs across providers
- View request history
- Identify optimization opportunities

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

Generate password hashes using:
```python
import streamlit_authenticator as stauth
hashed = stauth.Hasher(['your_password']).generate()
print(hashed)
```

## 🎯 Key Architecture Principles

### 1. **Runtime LLM Configuration**
- No hardcoded API keys
- All providers configurable through UI
- Session-based secure credential storage
- MongoDB-backed provider registry

### 2. **Service-Oriented Design**
- Clear separation between UI, business logic, and services
- Each external API has dedicated service class
- Core modules orchestrate complex workflows
- Utilities handle cross-cutting concerns

### 3. **Dynamic Provider System**
- LLM providers loaded from MongoDB
- New providers added via seeding scripts
- Supports 15+ providers out of the box
- Easy to extend with new providers

### 4. **Modular & Maintainable**
- Single responsibility principle
- DRY (Don't Repeat Yourself)
- Clear module boundaries
- Comprehensive error handling

## 🛠️ Advanced Configuration

### Adding New LLM Providers

1. **Add Provider to Seed Script** (`scripts/seed_language_models.py`):
```python
{
    "provider": "new_provider",
    "name": "New Provider",
    "api_key_env": "NEW_PROVIDER_API_KEY",
    "models": ["model-1", "model-2"],
    "requires_api_key": True,
}
```

2. **Run Seed Script**:
```bash
python scripts/seed_language_models.py
```

3. **Configure in UI**:
- Go to Settings → LLM Providers
- Find your new provider
- Add API key
- Test and use!

### Adding New Embedding Models

1. **Add to Seed Script** (`scripts/seed_embedding_models.py`):
```python
{
    "provider": "new_embed_provider",
    "name": "New Embeddings",
    "api_key_env": "NEW_EMBED_API_KEY",
    "models": [
        {
            "model_id": "embed-model-1",
            "name": "Embedding Model 1",
            "dimensions": 768,
            "max_input": 512,
            "description": "Description here"
        }
    ],
    "requires_api_key": True,
}
```

2. **Run Seed Script**:
```bash
python scripts/seed_embedding_models.py
```

### Custom Analysis Prompts

Create custom analysis types by adding to prompt manager or modifying `config/constants.py`:

```python
ANALYSIS_TYPES = [
    "Full Analysis",
    "Your Custom Analysis Type",
    # ... more types
]
```

## 🛠️ Development

### Project Structure

**Core Modules** (`src/core/`):
- `research_search.py`: Orchestrates multi-source paper search
- `paper_analyzer.py`: Handles PDF analysis with LLMs
- `rag_system.py`: Implements RAG retrieval and generation

**Services** (`src/services/`):
- `llm_manager.py`: Dynamic multi-provider LLM management
- `arxiv_service.py`: ArXiv API integration
- `semantic_scholar_service.py`: Semantic Scholar integration
- `search_service.py`: Google/DuckDuckGo search

**Utilities** (`src/utils/`):
- `credentials_manager.py`: Runtime API key management
- `model_manager.py`: LLM provider database interface
- `embedding_model_manager.py`: Embedding provider database
- `prompt_manager.py`: Prompt library database interface
- `document_utils.py`: PDF processing and text extraction
- `session_manager.py`: Streamlit session state management
- `dynamic_selector.py`: Dynamic model selection UI components
- `token_utils.py`: Token counting and management

### Adding a New Page

1. Create file in `pages/` (e.g., `06_new_feature.py`)
2. Add entry to `.streamlit/pages_sections.toml`:
```toml
[[pages]]
path = "pages/06_new_feature.py"
name = "New Feature"
icon = "✨"
```
3. Use existing utilities:
```python
from src.utils.session_manager import SessionStateManager
from src.utils.credentials_manager import CredentialsManager, LLMConfigWidget

SessionStateManager.initialize()
provider, model = LLMConfigWidget.render_model_selector()
```

### Adding a New Service

1. Create service class in `src/services/`:
```python
class NewService:
    def __init__(self):
        # Initialize service
        pass
    
    def perform_action(self, params):
        # Implement service logic
        pass
```

2. Import and use in core modules:
```python
from src.services.new_service import NewService

service = NewService()
result = service.perform_action(params)
```

### Testing

```bash
# Run tests (when implemented)
pytest tests/

# With coverage
pytest --cov=src tests/

# Test specific module
pytest tests/test_llm_manager.py
```

### Code Quality

```bash
# Format code
black src/ pages/

# Lint code
flake8 src/ pages/

# Type checking
mypy src/
```

## 📝 Migration & Deployment

### Deployment Checklist

1. **MongoDB Setup**
   - Ensure MongoDB is accessible from deployment environment
   - Update `MONGODB_URI` in production environment
   - Run seeding scripts in production

2. **Environment Variables**
   - Set `MONGODB_URI` in production
   - (Optional) Set `GOOGLE_API_KEY` and `GOOGLE_CSE_ID`
   - Configure other optional settings as needed

3. **Authentication**
   - Update `.streamlit/config.yaml` with production users
   - Use strong bcrypt hashed passwords
   - Set appropriate cookie expiry

4. **Streamlit Configuration**
   - Review `.streamlit/config.toml` settings
   - Configure appropriate server settings
   - Set memory limits if needed

### Deployment Options

**Streamlit Cloud:**
```bash
# Configure secrets in Streamlit Cloud dashboard
# Add MONGODB_URI and other environment variables
# Deploy from GitHub repository
```

**Docker:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
  
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/
    depends_on:
      - mongodb

volumes:
  mongo-data:
```

### Security Best Practices

1. **API Keys**
   - Never commit API keys to repository
   - Use session-based storage (already implemented)
   - API keys are cleared on logout

2. **Database**
   - Use MongoDB authentication in production
   - Enable TLS/SSL for MongoDB connections
   - Restrict database access by IP

3. **Application**
   - Enable authentication for production use
   - Use HTTPS in production
   - Set appropriate CORS policies

4. **Monitoring**
   - Monitor API usage and costs
   - Log errors and exceptions
   - Track user activity

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/research-v1.git
   cd research-v1
   ```
3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # if available
   ```

2. Set up MongoDB locally
3. Run seeding scripts
4. Make your changes

### Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to new functions/classes
- Include type hints where appropriate
- Write clear commit messages
- Add tests for new features

### Submitting Changes

1. Test your changes thoroughly
2. Update documentation if needed
3. Commit and push to your fork:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```
4. Open a Pull Request with description of changes

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New LLM provider integrations
- 📚 Documentation improvements
- 🧪 Test coverage
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🔧 New analysis types or features

## 🎓 Educational Use

This platform is ideal for:
- **Academic Researchers**: Streamline literature review and paper analysis
- **Graduate Students**: Manage research projects and references
- **Research Groups**: Collaborative prompt libraries and shared insights
- **Institutions**: Deploy as internal research tool

## 🚀 Roadmap

Planned features:
- [ ] Reference management integration (Zotero, Mendeley)
- [ ] Collaborative workspaces
- [ ] Advanced citation network analysis
- [ ] Export to LaTeX/Word formats
- [ ] Automated literature review generation
- [ ] Integration with institutional repositories
- [ ] API endpoints for programmatic access
- [ ] Enhanced visualization of research connections

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🙏 Acknowledgments

Built with these amazing technologies:
- [Streamlit](https://streamlit.io/) - Web framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [MongoDB](https://www.mongodb.com/) - Database
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing
- [ChromaDB](https://www.trychroma.com/) - Vector database

## 📧 Support

For questions, issues, or suggestions:

- 📫 **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/research-v1/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/research-v1/discussions)
- 📖 **Documentation**: Check this README and `/docs` folder
- 🐛 **Bug Reports**: Use issue templates

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/research-v1)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/research-v1)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/research-v1)
![License](https://img.shields.io/github/license/YOUR_USERNAME/research-v1)

---

**Built with ❤️ for researchers, by researchers**

*Powered by AI • Driven by Research • Built for Discovery*
