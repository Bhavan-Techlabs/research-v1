"""
Token Utilities
Handles token counting and text optimization for model context limits
"""

import tiktoken
from config.settings import Settings


class TokenManager:
    """Manages token counting and text optimization"""

    def __init__(self, model_name: str):
        """
        Initialize Token Manager

        Args:
            model_name: Model name for token encoding (required)
        """
        if not model_name:
            raise ValueError("model_name is a required parameter")

        self.model_name = model_name

    def count_tokens(self, text: str) -> int:
        """
        Calculate number of tokens in text

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        try:
            encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            # Fallback to cl100k_base encoding for unknown models
            encoding = tiktoken.get_encoding("cl100k_base")

        return len(encoding.encode(text))

    def truncate_text(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to fit within token limit

        Args:
            text: Text to truncate
            max_tokens: Maximum number of tokens

        Returns:
            Truncated text
        """
        try:
            encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")

        encoded_tokens = encoding.encode(text)[:max_tokens]
        return encoding.decode(encoded_tokens)

    def optimize_prompt(
        self, base_prompt: str, content: str, max_tokens: int = None
    ) -> str:
        """
        Optimize prompt by truncating content if needed

        Args:
            base_prompt: The base prompt template with {content} placeholder
            content: Content to insert
            max_tokens: Maximum tokens allowed

        Returns:
            Optimized prompt
        """
        max_tokens = max_tokens or Settings.MAX_TOKEN_LIMIT

        # Count tokens in content
        content_tokens = self.count_tokens(content)

        # Truncate if necessary
        if content_tokens > max_tokens:
            content = self.truncate_text(content, max_tokens)

        # Replace placeholder
        final_prompt = base_prompt.replace("{content}", content)
        final_prompt = final_prompt.replace("{full_paper}", content)

        return final_prompt
