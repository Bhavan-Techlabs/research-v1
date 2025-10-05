"""
Paper Analysis Module
Handles research paper analysis operations
"""

import json
from typing import Dict
from io import BytesIO
from src.services.openai_service import OpenAIService
from src.utils.document_utils import DocumentProcessor
from src.utils.token_utils import TokenManager


class PaperAnalyzer:
    """Analyzes research papers using AI"""

    def __init__(self, model_name: str = None):
        """
        Initialize Paper Analyzer

        Args:
            model_name: Model to use for analysis
        """
        self.openai_service = OpenAIService(model_name=model_name)
        self.token_manager = TokenManager(model_name=model_name)

    def analyze_pdf(
        self,
        pdf_file: BytesIO,
        analysis_type: str = "Full Analysis",
        custom_prompt: str = None,
    ) -> Dict:
        """
        Analyze a PDF research paper

        Args:
            pdf_file: PDF file as BytesIO
            analysis_type: Type of analysis to perform
            custom_prompt: Optional custom analysis instructions

        Returns:
            Dictionary with analysis results
        """
        # Extract text
        text = DocumentProcessor.extract_text_from_pdf(pdf_file)

        if not text:
            return {"error": "Could not extract text from PDF", "success": False}

        # Build analysis prompt
        prompt = self._build_analysis_prompt(text, analysis_type, custom_prompt)

        # Get analysis
        try:
            result = self.openai_service.analyze_paper(prompt)
            return {"success": True, "result": result, "word_count": len(text.split())}
        except Exception as e:
            return {"error": str(e), "success": False}

    def _build_analysis_prompt(
        self, text: str, analysis_type: str, custom_prompt: str = None
    ) -> str:
        """
        Build analysis prompt based on type

        Args:
            text: Paper text
            analysis_type: Type of analysis
            custom_prompt: Custom instructions

        Returns:
            Formatted prompt
        """
        # Truncate text if needed (keep first 8000 characters for now)
        truncated_text = text[:8000]

        if analysis_type == "Full Analysis":
            prompt = f"""
            Analyze this research paper comprehensively and provide a structured JSON response with the following sections:
            - title: Paper title
            - research_questions: Main research questions
            - methodology: Research methodology used
            - key_findings: Main findings and results
            - limitations: Study limitations
            - contributions: Key contributions to the field
            - future_work: Suggested future research directions
            
            Paper content:
            {truncated_text}
            """
        else:
            prompt = f"""
            Analyze the following research paper focusing specifically on: {analysis_type}
            
            {'Additional instructions: ' + custom_prompt if custom_prompt else ''}
            
            Provide a detailed analysis in JSON format.
            
            Paper content:
            {truncated_text}
            """

        return prompt

    def analyze_multiple_pdfs(
        self,
        pdf_files: list,
        analysis_type: str = "Full Analysis",
        custom_prompt: str = None,
        progress_callback=None,
    ) -> list:
        """
        Analyze multiple PDF files

        Args:
            pdf_files: List of PDF files
            analysis_type: Type of analysis
            custom_prompt: Custom instructions
            progress_callback: Optional callback for progress updates

        Returns:
            List of analysis results
        """
        results = []

        for idx, pdf_file in enumerate(pdf_files):
            if progress_callback:
                progress_callback(idx, len(pdf_files), pdf_file.name)

            result = self.analyze_pdf(pdf_file, analysis_type, custom_prompt)
            result["filename"] = pdf_file.name
            result["analysis_type"] = analysis_type
            results.append(result)

        return results
