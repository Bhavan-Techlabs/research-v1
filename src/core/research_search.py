"""
Research Search Module
Handles multi-source research paper search
"""

from typing import Dict, List
from src.services.arxiv_service import ArxivService
from src.services.semantic_scholar_service import SemanticScholarService
from src.services.search_service import SearchService
from config.constants import SEARCH_SOURCES


class ResearchSearcher:
    """Handles multi-source research paper search"""

    def __init__(self, provider: str, model_name: str):
        """
        Initialize Research Searcher

        Args:
            provider: LLM provider (e.g., 'openai', 'anthropic')
            model_name: Model to use for search agents
        """
        if not provider or not model_name:
            raise ValueError("Both provider and model_name are required")

        self.provider = provider
        self.model_name = model_name

        # Initialize services with provider and model
        self.arxiv_service = ArxivService(provider=provider, model_name=model_name)
        self.semantic_service = SemanticScholarService(
            provider=provider, model_name=model_name
        )
        self.search_service = SearchService(provider=provider, model_name=model_name)

    def search_all_sources(
        self,
        query: str,
        use_arxiv: bool = True,
        use_semantic: bool = True,
        use_google: bool = False,
        use_ddg: bool = False,
        progress_callback=None,
    ) -> Dict[str, str]:
        """
        Search across multiple sources

        Args:
            query: Search query
            use_arxiv: Search ArXiv
            use_semantic: Search Semantic Scholar
            use_google: Search Google Scholar
            use_ddg: Search DuckDuckGo
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with results from each source
        """
        results = {}
        sources = []

        if use_arxiv:
            sources.append("arxiv")
        if use_semantic:
            sources.append("semantic")
        if use_google:
            sources.append("google")
        if use_ddg:
            sources.append("ddg")

        total_sources = len(sources)
        current = 0

        # ArXiv search
        if use_arxiv:
            current += 1
            if progress_callback:
                progress_callback(current, total_sources, "Searching ArXiv...")
            try:
                results[SEARCH_SOURCES["ARXIV"]] = self.arxiv_service.search_with_agent(
                    query
                )
            except Exception as e:
                results[SEARCH_SOURCES["ARXIV"]] = f"Error: {str(e)}"

        # Semantic Scholar search
        if use_semantic:
            current += 1
            if progress_callback:
                progress_callback(
                    current, total_sources, "Searching Semantic Scholar..."
                )
            try:
                results[SEARCH_SOURCES["SEMANTIC_SCHOLAR"]] = (
                    self.semantic_service.search(query)
                )
            except Exception as e:
                results[SEARCH_SOURCES["SEMANTIC_SCHOLAR"]] = f"Error: {str(e)}"

        # Google Scholar search
        if use_google:
            current += 1
            if progress_callback:
                progress_callback(current, total_sources, "Searching Google Scholar...")
            try:
                results[SEARCH_SOURCES["GOOGLE_SCHOLAR"]] = (
                    self.search_service.google_search(
                        f"{query} site:scholar.google.com"
                    )
                )
            except Exception as e:
                results[SEARCH_SOURCES["GOOGLE_SCHOLAR"]] = f"Error: {str(e)}"

        # DuckDuckGo search
        if use_ddg:
            current += 1
            if progress_callback:
                progress_callback(current, total_sources, "Searching DuckDuckGo...")
            try:
                results[SEARCH_SOURCES["DUCKDUCKGO"]] = (
                    self.search_service.duckduckgo_search(f"{query} research papers")
                )
            except Exception as e:
                results[SEARCH_SOURCES["DUCKDUCKGO"]] = f"Error: {str(e)}"

        return results

    def search_arxiv(self, query: str, max_docs: int = 10) -> str:
        """Search ArXiv only"""
        return self.arxiv_service.load_documents_from_query(query, max_docs=max_docs)

    def search_semantic_scholar(self, query: str) -> str:
        """Search Semantic Scholar only"""
        return self.semantic_service.search(query)

    def search_google(self, query: str) -> str:
        """Search Google only"""
        return self.search_service.google_search(query)

    def search_duckduckgo(self, query: str) -> str:
        """Search DuckDuckGo only"""
        return self.search_service.duckduckgo_search(query)
