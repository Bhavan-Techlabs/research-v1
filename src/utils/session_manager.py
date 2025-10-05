"""
Session State Management
Centralized management of Streamlit session state
"""

import streamlit as st
from typing import Any, Dict


class SessionStateManager:
    """Manages Streamlit session state in a centralized way"""

    # Define all session state keys
    RESEARCH_RESULTS = "research_results"
    SEARCH_HISTORY = "search_history"
    ANALYSIS_RESULTS = "analysis_results"
    RAG_RETRIEVER = "rag_retriever"
    CHAT_HISTORY = "chat_history"
    DOCUMENTS_LOADED = "documents_loaded"
    EDIT_PROMPT = "edit_prompt"
    AUTHENTICATION_STATUS = "authentication_status"

    @staticmethod
    def initialize():
        """Initialize all session state variables with default values"""
        defaults = {
            SessionStateManager.RESEARCH_RESULTS: None,
            SessionStateManager.SEARCH_HISTORY: [],
            SessionStateManager.ANALYSIS_RESULTS: None,
            SessionStateManager.RAG_RETRIEVER: None,
            SessionStateManager.CHAT_HISTORY: [],
            SessionStateManager.DOCUMENTS_LOADED: [],
            SessionStateManager.EDIT_PROMPT: None,
        }

        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get a value from session state

        Args:
            key: Session state key
            default: Default value if key doesn't exist

        Returns:
            Value from session state or default
        """
        return st.session_state.get(key, default)

    @staticmethod
    def set(key: str, value: Any):
        """
        Set a value in session state

        Args:
            key: Session state key
            value: Value to set
        """
        st.session_state[key] = value

    @staticmethod
    def clear(key: str):
        """
        Clear a specific session state key

        Args:
            key: Session state key to clear
        """
        if key in st.session_state:
            if isinstance(st.session_state[key], list):
                st.session_state[key] = []
            else:
                st.session_state[key] = None

    @staticmethod
    def clear_all():
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]

    @staticmethod
    def append_to_list(key: str, item: Any):
        """
        Append an item to a list in session state

        Args:
            key: Session state key (must be a list)
            item: Item to append
        """
        if key not in st.session_state:
            st.session_state[key] = []
        st.session_state[key].append(item)

    @staticmethod
    def get_search_history() -> list:
        """Get search history"""
        return SessionStateManager.get(SessionStateManager.SEARCH_HISTORY, [])

    @staticmethod
    def add_search_to_history(query: str, sources: list):
        """Add a search to history"""
        from datetime import datetime

        history_item = {
            "query": query,
            "sources": sources,
            "timestamp": datetime.now().isoformat(),
        }
        SessionStateManager.append_to_list(
            SessionStateManager.SEARCH_HISTORY, history_item
        )

    @staticmethod
    def get_chat_history() -> list:
        """Get chat history"""
        return SessionStateManager.get(SessionStateManager.CHAT_HISTORY, [])

    @staticmethod
    def add_message_to_chat(role: str, content: str):
        """Add a message to chat history"""
        message = {"role": role, "content": content}
        SessionStateManager.append_to_list(SessionStateManager.CHAT_HISTORY, message)

    @staticmethod
    def clear_chat():
        """Clear chat history"""
        SessionStateManager.clear(SessionStateManager.CHAT_HISTORY)
