"""
Gemini Provider - Google Gemini API implementation
"""
import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from .base_provider import BaseLLMProvider
from ..logger import setup_logger


logger = setup_logger(__name__)


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Gemini provider.

        Args:
            api_key: Google API key. If None, reads from GOOGLE_API_KEY env var
            model: Model name to use. If None, uses default model

        Raises:
            ValueError: If API key is not provided and not in environment
        """
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "Google API key must be provided or set in GOOGLE_API_KEY environment variable"
            )

        super().__init__(api_key=api_key, model=model or self.default_model)

        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
        logger.info(f"Gemini provider initialized with model: {self.model}")

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def default_model(self) -> str:
        return "gemini-3.1-pro-preview"

    def generate(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 2000,
        temperature: float = 1.0,
        **kwargs
    ) -> str:
        """
        Generate a response using Gemini API.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            **kwargs: Additional Gemini-specific parameters

        Returns:
            Generated text response

        Raises:
            Exception: If API call fails
        """
        try:
            logger.debug(f"Calling Gemini API with {len(messages)} messages")

            # Convert messages to Gemini format
            gemini_messages = self._convert_messages_to_gemini_format(messages)

            # Configure generation settings
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )

            # Generate response
            response = self.client.generate_content(
                gemini_messages,
                generation_config=generation_config,
            )

            if response.text:
                return response.text

            raise Exception("No response received from Gemini")

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            raise

    def generate_with_tools(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        max_tokens: int = 2000,
        max_iterations: int = 8,
        tool_handler: Optional[callable] = None,
        **kwargs
    ) -> str:
        """
        Generate a response with tool calling support.

        Args:
            messages: List of message dicts
            tools: List of tool definitions
            max_tokens: Maximum tokens in response
            max_iterations: Maximum tool use iterations
            tool_handler: Function to handle tool calls
            **kwargs: Additional Gemini-specific parameters

        Returns:
            Generated text response after tool interactions

        Raises:
            Exception: If generation fails
        """
        try:
            logger.debug(f"Calling Gemini API with tools, max_iterations={max_iterations}")

            # Convert tools to Gemini format
            gemini_tools = self._convert_tools_to_gemini_format(tools)

            # For now, just generate without tools (simplified implementation)
            # Full tool support would require more complex conversation handling
            return self.generate(messages, max_tokens=max_tokens, **kwargs)

        except Exception as e:
            logger.error(f"Gemini API error with tools: {str(e)}", exc_info=True)
            raise

    def _convert_messages_to_gemini_format(self, messages: List[Dict[str, str]]) -> str:
        """
        Convert standard message format to Gemini format.

        Args:
            messages: List of message dicts

        Returns:
            Formatted prompt string for Gemini
        """
        # Gemini uses a simpler format - we'll combine all messages into a prompt
        prompt_parts = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        return "\n\n".join(prompt_parts)

    def _convert_tools_to_gemini_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert tool definitions to Gemini format.

        Args:
            tools: List of tool definitions

        Returns:
            List of tools in Gemini format
        """
        # Simplified - would need proper implementation for production use
        return tools
