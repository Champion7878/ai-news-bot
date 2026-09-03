"""
Configuration management for AI News Bot
"""
import os
import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from .logger import setup_logger


logger = setup_logger(__name__)


# Supported language codes and their display names
LANGUAGE_NAMES = {
    "zh": "Chinese (中文)",
    "es": "Spanish (Español)",
    "fr": "French (Français)",
    "ja": "Japanese (日本語)",
    "de": "German (Deutsch)",
    "ko": "Korean (한국어)",
    "pt": "Portuguese (Português)",
    "ru": "Russian (Русский)",
    "ar": "Arabic (العربية)",
    "hi": "Hindi (हिन्दी)",
    "it": "Italian (Italiano)",
    "nl": "Dutch (Nederlands)",
}


class Config:
    """Application configuration manager"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config.yaml file. If None, searches for it in default locations
        """
        # Load environment variables from .env file
        load_dotenv()

        # Find and load YAML config
        self.config_path = self._find_config_file(config_path)
        self.config_data = self._load_yaml_config()

        logger.info(f"Configuration loaded from {self.config_path}")

    def _find_config_file(self, config_path: Optional[str] = None) -> Path:
        """
        Find the configuration file.

        Args:
            config_path: Explicit path to config file

        Returns:
            Path to configuration file

        Raises:
            FileNotFoundError: If config file cannot be found
        """
        if config_path:
            path = Path(config_path)
            if path.exists():
                return path
            raise FileNotFoundError(f"Config file not found: {config_path}")

        # Search in default locations
        search_paths = [
            Path("config.yaml"),
            Path("config.yml"),
            Path(__file__).parent.parent / "config.yaml",
            Path(__file__).parent.parent / "config.yml",
        ]

        for path in search_paths:
            if path.exists():
                return path

        raise FileNotFoundError(
            "Config file not found. Searched: " + ", ".join(str(p) for p in search_paths)
        )

    def _load_yaml_config(self) -> Dict[str, Any]:
        """
        Load YAML configuration file.

        Returns:
            Configuration dictionary
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config or {}
        except Exception as e:
            logger.error(f"Failed to load config file: {str(e)}")
            return {}

    @property
    def news_topics(self) -> List[str]:
        """Get list of news topics to cover"""
        return self.config_data.get("news", {}).get("topics", [
            "Latest AI developments and breakthroughs"
        ])

    @property
    def stage1_prompt_template(self) -> str:
        """Get the Stage 1 selection prompt template"""
        default_template = """{formatted_news}

## YOUR TASK - STAGE 1: NEWS SELECTION

You are a senior AI industry analyst. Analyze the {total_items} news items above and select exactly 15-20 of the highest-quality items.

### SELECTION CRITERIA:
- ✅ Groundbreaking research or technical breakthroughs
- ✅ Major product launches or significant updates
- ✅ Important policy changes or regulations
- ✅ Large funding rounds or M&A activities
- ✅ Balanced coverage across categories (LLM, Agents, Research, Products, etc.)
- ✅ Include both international and domestic news when available
- ✅ Prefer primary sources over secondary reporting

### OUTPUT FORMAT:
Return ONLY a JSON array of selected news IDs. No explanations, no markdown, just the JSON array.

Example format:
["INT-1", "INT-5", "DOM-2", "INT-12", ...]

CRITICAL: Select exactly 15-20 items. No more, no less."""

        return self.config_data.get("news", {}).get("stage1_prompt_template", default_template)

    @property
    def stage2_prompt_template(self) -> str:
        """Get the Stage 2 summarization prompt template"""
        default_template = """You are a senior AI industry analyst. Create a comprehensive, in-depth news digest for the {count} pre-selected news items below.

{selected_news}

## OUTPUT STRUCTURE:

Organize news items into relevant categories (use only categories that have news):
1. **Large Language Models & Foundation Models**
2. **AI Agents & Autonomous Systems**
3. **Research & Academic Breakthroughs**
4. **Product Launches & Updates**
5. **AI Infrastructure & Hardware**
6. **Funding & Market Dynamics**
7. **Policy & Regulation**

## CONTENT REQUIREMENTS:

For each news item:
- **Clear Headline**: Informative title
- **Analytical Summary (4-6 sentences)**: What happened, technical details, why it matters, implications
- **Source Attribution**: [Source Name](URL)

## WRITING STYLE:
- Professional, analytical tone
- Include specific metrics and data
- Technical accuracy
- Context and analysis

## QUALITY REQUIREMENTS:
- ✅ Summarize ALL {count} items (no skipping)
- ✅ Each summary exactly 4-6 sentences
- ✅ Include specific numbers and data
- ✅ Balanced coverage across categories
- ✅ All sources as clickable markdown links

## AVOID:
❌ Generic statements
❌ Wrong summary length
❌ Missing links
❌ Skipping items"""

        return self.config_data.get("news", {}).get("stage2_prompt_template", default_template)

    @property
    def log_level(self) -> str:
        """Get logging level"""
        return self.config_data.get("logging", {}).get("level", "INFO")

    @property
    def log_format(self) -> str:
        """Get logging format"""
        return self.config_data.get("logging", {}).get(
            "format",
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    @property
    def notification_methods(self) -> List[str]:
        """Get enabled notification methods from environment"""
        methods_str = os.getenv("NOTIFICATION_METHODS", "")
        if not methods_str:
            return []
        return [m.strip().lower() for m in methods_str.split(",")]

    @property
    def ai_response_language(self) -> str:
        """Get the language for AI-generated content (single language, deprecated)"""
        return os.getenv("AI_RESPONSE_LANGUAGE", "en").strip().lower()
    
    @property
    def ai_response_languages(self) -> List[str]:
        """Get the list of languages for AI-generated content (supports comma-separated values)"""
        languages_str = os.getenv("AI_RESPONSE_LANGUAGE", "en").strip().lower()
        # Split by comma and clean up whitespace
        languages = [lang.strip() for lang in languages_str.split(",") if lang.strip()]
        # Validate languages
        valid_languages = []
        for lang in languages:
            if lang == "en" or lang in LANGUAGE_NAMES:
                valid_languages.append(lang)
            else:
                logger.warning(f"Unsupported language code '{lang}', skipping")
        # Return at least 'en' if no valid languages
        return valid_languages if valid_languages else ["en"]

    @property
    def enable_web_search(self) -> bool:
        """Get whether to enable web search for fetching current news"""
        # Check config file first, then environment variable
        config_value = self.config_data.get("news", {}).get("enable_web_search")
        if config_value is not None:
            return bool(config_value)
        env_value = os.getenv("ENABLE_WEB_SEARCH", "false").strip().lower()
        return env_value in ("true", "1", "yes", "on")

    @property
    def max_items_per_source(self) -> int:
        """Maximum news items to fetch per source"""
        return self.config_data.get("news", {}).get("max_items_per_source", 5)

    @property
    def hackernews_max_items(self) -> int:
        """Maximum Hacker News front-page stories to fetch"""
        return self.config_data.get("news", {}).get("hackernews", {}).get("max_items", 15)

    @property
    def hackernews_min_points(self) -> int:
        """Minimum score a Hacker News story needs to be considered"""
        return self.config_data.get("news", {}).get("hackernews", {}).get("min_points", 40)

    @property
    def llm_provider(self) -> str:
        """Get the LLM provider to use (claude or deepseek)"""
        # Check environment variable first, then config file
        env_provider = os.getenv("LLM_PROVIDER", "").strip().lower()
        if env_provider:
            return env_provider
        return self.config_data.get("llm", {}).get("provider", "claude").lower()

    @property
    def llm_model(self) -> Optional[str]:
        """Get the specific model to use (if specified)"""
        # Check environment variable first, then config file
        env_model = os.getenv("LLM_MODEL", "").strip()
        if env_model:
            return env_model
        return self.config_data.get("llm", {}).get("model")

    @property
    def llm_api_key(self) -> Optional[str]:
        """Get the API key for the LLM provider"""
        # Check environment variables based on provider
        provider = self.llm_provider
        if provider == "deepseek":
            return os.getenv("DEEPSEEK_API_KEY")
        elif provider == "claude":
            return os.getenv("ANTHROPIC_API_KEY")
        elif provider == "gemini":
            return os.getenv("GOOGLE_API_KEY")
        elif provider == "grok":
            return os.getenv("XAI_API_KEY")
        elif provider == "openai":
            return os.getenv("OPENAI_API_KEY")
        return None

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Dot-separated key path (e.g., "news.topics")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config_data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value
