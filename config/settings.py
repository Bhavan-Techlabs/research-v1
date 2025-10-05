"""
Centralized Settings Management
Handles environment variables and configuration for the Research Assistant Platform
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings with environment variable support"""

    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    TEMP_DIR = BASE_DIR / "temp"
    DOCUMENTS_DIR = BASE_DIR / "documents"
    CHROMADB_DIR = BASE_DIR / "chromadb"

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")

    # Model Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    DEFAULT_EMBEDDING_MODEL: str = os.getenv(
        "DEFAULT_EMBEDDING_MODEL", "text-embedding-3-large"
    )
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.0"))
    DEFAULT_MAX_TOKENS: int = int(os.getenv("DEFAULT_MAX_TOKENS", "4000"))

    # Document Processing
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    DEFAULT_CHUNK_SIZE: int = int(os.getenv("DEFAULT_CHUNK_SIZE", "1000"))
    DEFAULT_CHUNK_OVERLAP: int = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "200"))
    MAX_TOKEN_LIMIT: int = int(os.getenv("MAX_TOKEN_LIMIT", "100000"))

    # Search Configuration
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    SEARCH_TIMEOUT: int = int(os.getenv("SEARCH_TIMEOUT", "60"))
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", "20"))

    # Database
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "research_assistant")
    MONGODB_COLLECTION_PROMPTS: str = os.getenv("MONGODB_COLLECTION_PROMPTS", "prompts")

    # Authentication
    AUTH_COOKIE_NAME: str = os.getenv("AUTH_COOKIE_NAME", "st_research_v1")
    AUTH_COOKIE_KEY: str = os.getenv("AUTH_COOKIE_KEY", "da47w23s")
    AUTH_COOKIE_EXPIRY_DAYS: int = int(os.getenv("AUTH_COOKIE_EXPIRY_DAYS", "30"))

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.TEMP_DIR.mkdir(exist_ok=True, parents=True)
        cls.DOCUMENTS_DIR.mkdir(exist_ok=True, parents=True)
        cls.CHROMADB_DIR.mkdir(exist_ok=True, parents=True)

    @classmethod
    def is_openai_configured(cls) -> bool:
        """Check if OpenAI API key is configured"""
        return bool(cls.OPENAI_API_KEY)

    @classmethod
    def is_google_configured(cls) -> bool:
        """Check if Google API is configured"""
        return bool(cls.GOOGLE_API_KEY and cls.GOOGLE_CSE_ID)

    @classmethod
    def is_mongodb_configured(cls) -> bool:
        """Check if MongoDB is configured"""
        return bool(cls.MONGODB_URI)

    @classmethod
    def get_model_options(cls) -> list:
        """Get available model options"""
        return ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]

    @classmethod
    def get_embedding_options(cls) -> list:
        """Get available embedding model options"""
        return [
            "text-embedding-3-large",
            "text-embedding-3-small",
            "text-embedding-ada-002",
        ]


# Initialize directories on import
Settings.ensure_directories()
