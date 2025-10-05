"""
Application Constants
Centralized location for all constant values used across the application
"""

# Analysis Types
ANALYSIS_TYPES = [
    "Full Analysis",
    "Research Questions & Objectives",
    "Methodology Analysis",
    "Key Findings",
    "Limitations & Gaps",
    "Citation Analysis",
]

# Output Formats
OUTPUT_FORMATS = ["Structured JSON", "Narrative Text", "Both"]

# Search Sources
SEARCH_SOURCES = {
    "ARXIV": "ArXiv",
    "SEMANTIC_SCHOLAR": "Semantic Scholar",
    "GOOGLE_SCHOLAR": "Google Scholar",
    "DUCKDUCKGO": "DuckDuckGo",
}

# File Types
SUPPORTED_FILE_TYPES = ["pdf"]

# Text Splitter Separators
DEFAULT_SEPARATORS = ["\n---\n", "\n\n", "\n", " "]

# Prompt Categories
PROMPT_CATEGORIES = [
    "general",
    "research",
    "paper_analysis",
    "evaluation",
    "writing",
]

# UI Messages
UI_MESSAGES = {
    "NO_OPENAI_KEY": "⚠️ OpenAI API key not configured. Please configure it in Settings.",
    "DEPENDENCIES_NOT_INSTALLED": "⚠️ Research app dependencies not installed. Please run: pip install -r requirements.txt",
    "UPLOAD_DOCUMENTS_FIRST": "👆 Upload some documents first to start chatting!",
    "NO_PROMPTS_FOUND": "No prompts found.",
    "NO_SEARCH_HISTORY": "No search history yet. Perform a search to see results here.",
}

# Example Search Queries
EXAMPLE_QUERIES = {
    "AI_ML": "artificial intelligence machine learning",
    "HEALTHCARE": "healthcare medical research",
    "DATA_SCIENCE": "data science analytics",
}

# RAG Example Questions
RAG_EXAMPLE_QUESTIONS = [
    "What are the main findings?",
    "What methodology was used?",
    "What are the key contributions?",
    "What are the limitations?",
]

# Model Parameters
MODEL_PARAMS = {
    "temperature_range": (0.0, 1.0),
    "max_tokens_range": (1000, 16000),
    "chunk_size_range": (500, 5000),
    "chunk_overlap_range": (0, 1000),
}

# API Endpoints
API_URLS = {
    "OPENAI": "https://platform.openai.com/",
    "GOOGLE_CLOUD": "https://console.cloud.google.com/",
    "SCIHUB": "https://doi.org/",
}
