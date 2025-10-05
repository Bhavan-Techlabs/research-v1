# � Research Assistant Platform

A comprehensive Streamlit application for research paper analysis, multi-source search, and AI-powered document interaction.

## Architecture

The application uses a clean page-based architecture with `st-pages` for navigation:

```
research-v1-main/
├── streamlit_app.py              # Main application entry point
├── about_st_pages.py             # About page (st-pages info)
├── research_assistant.py         # Multi-source paper search
├── paper_analyzer_page.py        # AI-powered document analysis  
├── rag_chat_page.py              # Interactive document Q&A
├── settings_page.py              # Configuration and API management
├── src/
│   ├── core/
│   │   └── research_app.py       # Core research functionality
│   └── utils/
│       └── mongo_utils.py        # MongoDB utilities (optional)
├── .streamlit/
│   ├── pages.toml                # Navigation without sections
│   └── pages_sections.toml       # Navigation with sections
└── requirements.txt              # Python dependencies
```

### Page Functions:
- **Research Assistant** (`research_assistant.py`): Multi-source paper search
- **Paper Analyzer** (`paper_analyzer_page.py`): AI-powered document analysis  
- **RAG Chat System** (`rag_chat_page.py`): Interactive document Q&A
- **Settings** (`settings_page.py`): Configuration and API management

## Installation & Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** (create `.env` file or use Settings page):
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here  # Optional
   MONGODB_URI=your_mongodb_uri_here       # Optional
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

## API Keys Required

- **OpenAI API Key** (Required): Get from https://platform.openai.com/
- **Google API Key** (Optional): For Google Scholar search
- **MongoDB URI** (Optional): For saving prompts and templates

## Usage

1. Visit the **Settings** page to configure your API keys
2. Use **Research Assistant** to search for papers across multiple sources
3. Use **Paper Analyzer** to upload and analyze PDF documents
4. Use **RAG Chat System** to ask questions about your uploaded documents
