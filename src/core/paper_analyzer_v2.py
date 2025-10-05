"""
Paper Analyzer Module - Multi-LLM Support
Analyzes research papers using multiple LLM providers
"""

from pathlib import Path
from typing import List, Optional
from src.services.llm_manager import get_llm_manager
from src.utils.document_utils import DocumentProcessor
from config.constants import ANALYSIS_TYPES


class PaperAnalyzer:
    """
    Analyzes research papers using AI with multi-LLM support
    """

    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 2000,
        **kwargs,
    ):
        """
        Initialize Paper Analyzer with multi-LLM support

        Args:
            provider: LLM provider (openai, anthropic, google-genai, etc.)
            model: Model name
            api_key: API key for the provider
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
        """
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Initialize LLM manager
        self.llm_manager = get_llm_manager()

        # Set credentials if provided
        if api_key:
            self.llm_manager.set_credentials(provider, api_key, **kwargs)

    def analyze_pdf(
        self,
        pdf_path: str,
        analysis_type: str = "summary",
        custom_prompt: Optional[str] = None,
    ) -> str:
        """
        Analyze a single PDF

        Args:
            pdf_path: Path to PDF file
            analysis_type: Type of analysis
            custom_prompt: Custom analysis prompt

        Returns:
            Analysis result
        """
        # Extract text from PDF
        text = DocumentProcessor.extract_text_from_pdf(pdf_path)

        if not text:
            raise ValueError("Could not extract text from PDF")

        # Initialize LLM
        llm = self.llm_manager.initialize_model(
            provider=self.provider,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        # Analyze with LLM
        prompt = self._get_analysis_prompt(analysis_type, custom_prompt)
        full_prompt = f"{prompt}\n\nDocument:\n{text}"

        from langchain_core.messages import HumanMessage

        response = llm.invoke([HumanMessage(content=full_prompt)])
        result = response.content

        return result

    def analyze_multiple_pdfs(
        self, pdf_paths: List[str], analysis_type: str = "summary"
    ) -> List[dict]:
        """
        Analyze multiple PDFs

        Args:
            pdf_paths: List of PDF file paths
            analysis_type: Type of analysis

        Returns:
            List of analysis results
        """
        results = []

        for pdf_path in pdf_paths:
            try:
                result = self.analyze_pdf(pdf_path, analysis_type)
                results.append(
                    {"file": Path(pdf_path).name, "success": True, "result": result}
                )
            except Exception as e:
                results.append(
                    {"file": Path(pdf_path).name, "success": False, "error": str(e)}
                )

        return results

    def _get_analysis_prompt(
        self, analysis_type: str, custom_prompt: Optional[str] = None
    ) -> str:
        """Get the analysis prompt"""
        if custom_prompt:
            return custom_prompt

        return ANALYSIS_TYPES.get(analysis_type, ANALYSIS_TYPES["summary"])
