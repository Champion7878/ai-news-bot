"""
Gemini Provider - Google Gemini API implementation
"""
import os
import re
import time
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

        # Configure Gemini API before any model lookup, since resolving the
        # default model needs a live, authenticated call.
        genai.configure(api_key=api_key)

        self._model_candidates: List[str] = []  # ranked fallback list, filled by discovery
        self._tried_models: set = set()

        super().__init__(api_key=api_key, model=model or self._resolve_default_model())

        self.client = genai.GenerativeModel(self.model)
        logger.info(f"Gemini provider initialized with model: {self.model}")

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def default_model(self) -> str:
        """Last-resort fallback if live model discovery fails (e.g. network/permission issue).

        Google frequently renames/retires Gemini model versions (this hardcoded value has
        gone stale three times already — gemini-3-pro-preview, gemini-2.0-flash-exp, then
        gemini-2.5-flash got cut off from new API keys), so _resolve_default_model() below
        asks the API directly instead of relying on this guess whenever possible.
        """
        return "gemini-3.6-flash"

    def _resolve_default_model(self) -> str:
        """
        Ask the Gemini API which models are actually available for this key right now,
        and pick a sensible default — instead of hardcoding a version string that Google
        can rename or retire at any time.

        Returns:
            A model name confirmed to support generateContent for this API key.
        """
        try:
            available = [
                m for m in genai.list_models()
                if 'generateContent' in getattr(m, 'supported_generation_methods', [])
            ]
        except Exception as e:
            logger.warning(
                f"Could not list Gemini models ({e}); falling back to hardcoded guess "
                f"'{self.default_model}'. Set 'llm.model' in config.yaml to pin a specific model."
            )
            return self.default_model

        if not available:
            logger.warning(
                f"No Gemini models supporting generateContent were returned for this API key; "
                f"falling back to hardcoded guess '{self.default_model}'."
            )
            return self.default_model

        def stability_score(m) -> tuple:
            name = m.name.rsplit('/', 1)[-1]
            is_unstable = any(tag in name for tag in ('exp', 'preview', 'thinking'))
            is_lite = 'lite' in name
            is_flash = 'flash' in name
            version_match = re.search(r'(\d+)(?:\.(\d+))?', name)
            version = (
                (int(version_match.group(1)), int(version_match.group(2) or 0))
                if version_match else (0, 0)
            )
            # Prefer "lite" variants first: for a once-a-day summarization job, their much
            # higher free-tier daily quota (e.g. 500/day vs 20/day for plain Flash) matters
            # far more than raw model quality. Then flash over pro, stable over exp/preview/
            # thinking builds, and the newest version as a tie-break.
            return (
                0 if is_lite else 1,
                0 if is_flash else 1,
                1 if is_unstable else 0,
                tuple(-v for v in version),
                name,
            )

        ranked = sorted(available, key=stability_score)
        self._model_candidates = [m.name.rsplit('/', 1)[-1] for m in ranked]
        chosen_name = self._model_candidates[0]
        logger.info(
            f"Auto-selected Gemini model: {chosen_name} "
            f"(from {len(self._model_candidates)} available: {', '.join(self._model_candidates[:12])}"
            f"{', ...' if len(self._model_candidates) > 12 else ''})"
        )
        return chosen_name

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
            return self._generate_once(messages, max_tokens, temperature)
        except Exception as e:
            # Google sometimes retires a model even while list_models() still lists it
            # (e.g. "no longer available to new users") and names its replacement right
            # in the error text ("...use models/gemini-3.6-flash..."). Reuse that instead
            # of hardcoding yet another version string that will eventually go stale too.
            suggested = self._extract_suggested_model(str(e))
            if suggested and suggested != self.model:
                logger.warning(
                    f"Model '{self.model}' was rejected ({e}); API suggested '{suggested}', "
                    f"retrying once with it."
                )
                self.model = suggested
                self.client = genai.GenerativeModel(self.model)
                try:
                    return self._generate_once(messages, max_tokens, temperature)
                except Exception as retry_e:
                    logger.error(f"Gemini API error after retry: {str(retry_e)}", exc_info=True)
                    raise

            # A per-DAY quota (GenerateRequestsPerDayPerProjectPerModel) is exhausted until
            # tomorrow — no amount of waiting inside this run helps. Each model has its own
            # separate daily bucket, so switch to the next candidate instead of sleeping.
            if 'PerDay' in str(e):
                next_model = self._next_candidate_model()
                if next_model:
                    logger.warning(
                        f"Daily quota exhausted for '{self.model}' ({e}); switching to "
                        f"'{next_model}' instead of waiting (each model has its own daily quota)."
                    )
                    self.model = next_model
                    self.client = genai.GenerativeModel(self.model)
                    try:
                        return self._generate_once(messages, max_tokens, temperature)
                    except Exception as retry_e:
                        logger.error(f"Gemini API error after model switch: {str(retry_e)}", exc_info=True)
                        raise
                logger.error(f"Daily quota exhausted for '{self.model}' and no fallback model left: {e}")
                raise

            # Free-tier rate limits (requests/minute/model) are transient — Google tells us
            # exactly how long to back off, e.g. "Please retry in 44.02s." Worth one wait+retry
            # instead of failing the whole daily digest over a 60-second window.
            wait_seconds = self._extract_retry_delay(str(e))
            if wait_seconds is not None:
                wait_seconds = min(wait_seconds, 90) + 1
                logger.warning(
                    f"Gemini rate limit hit ({e}); waiting {wait_seconds:.0f}s before retrying once."
                )
                time.sleep(wait_seconds)
                try:
                    return self._generate_once(messages, max_tokens, temperature)
                except Exception as retry_e:
                    logger.error(f"Gemini API error after rate-limit retry: {str(retry_e)}", exc_info=True)
                    raise

            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            raise

    def _generate_once(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float) -> str:
        """Single attempt at a Gemini generateContent call, no retry logic."""
        logger.debug(f"Calling Gemini API with {len(messages)} messages")

        gemini_messages = self._convert_messages_to_gemini_format(messages)

        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )

        response = self.client.generate_content(
            gemini_messages,
            generation_config=generation_config,
        )

        if response.text:
            return response.text

        raise Exception("No response received from Gemini")

    @staticmethod
    def _extract_suggested_model(error_text: str) -> Optional[str]:
        """Pull a replacement model name out of a Gemini error message, if it names one
        (e.g. '...Please update your code to use models/gemini-3.6-flash...')."""
        match = re.search(r'use\s+models/([a-zA-Z0-9._-]+)', error_text, re.IGNORECASE)
        return match.group(1) if match else None

    @staticmethod
    def _extract_retry_delay(error_text: str) -> Optional[float]:
        """Pull the suggested backoff out of a Gemini 429 error, if it names one
        (e.g. '...Please retry in 44.02s.')."""
        match = re.search(r'retry in ([\d.]+)s', error_text, re.IGNORECASE)
        return float(match.group(1)) if match else None

    def _next_candidate_model(self) -> Optional[str]:
        """Next untried model from the ranked discovery list (see _resolve_default_model),
        or None if we're out of candidates or discovery never ran (e.g. explicit model pin)."""
        self._tried_models.add(self.model)
        for name in self._model_candidates:
            if name not in self._tried_models:
                return name
        return None

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
