"""
Document Processing Utilities
Handles PDF extraction, text processing, and document loading
"""

import os
from io import BytesIO
from typing import List
from pathlib import Path
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_core.documents import Document


class DocumentProcessor:
    """Handles document processing operations"""

    @staticmethod
    def extract_text_from_pdf(pdf_file: BytesIO) -> str:
        """
        Extract text from PDF file

        Args:
            pdf_file: BytesIO object containing PDF data

        Returns:
            Extracted text content
        """
        doc = fitz.open(stream=pdf_file, filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text

    @staticmethod
    def extract_text_from_html(url: str) -> str:
        """
        Extract text from HTML webpage

        Args:
            url: URL of the webpage

        Returns:
            Extracted text content
        """
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return " ".join([p.get_text() for p in soup.find_all("p")])

    @staticmethod
    def extract_text_from_url(url: str) -> str:
        """
        Extract text from URL (handles both PDF and HTML)

        Args:
            url: URL to extract text from

        Returns:
            Extracted text content
        """
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").lower()

        if "application/pdf" in content_type:
            pdf_file = BytesIO(response.content)
            return DocumentProcessor.extract_text_from_pdf(pdf_file)
        else:
            return DocumentProcessor.extract_text_from_html(url)

    @staticmethod
    def load_documents_from_path(file_path: str) -> List[Document]:
        """
        Load documents from file path

        Args:
            file_path: Path to the document

        Returns:
            List of Document objects
        """
        file_extension = os.path.splitext(file_path)[1]

        if file_extension == ".pdf":
            loader = PyMuPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)

        return loader.load()

    @staticmethod
    def get_papers_from_directory(directory: str) -> List[str]:
        """
        Get list of all paper files in a directory

        Args:
            directory: Directory path

        Returns:
            List of filenames
        """
        return os.listdir(directory)

    @staticmethod
    def save_uploaded_file(uploaded_file, save_path: Path) -> Path:
        """
        Save an uploaded Streamlit file

        Args:
            uploaded_file: Streamlit UploadedFile object
            save_path: Path to save the file

        Returns:
            Path to saved file
        """
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return save_path
