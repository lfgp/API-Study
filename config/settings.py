from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv


def load_settings() -> Dict[str, Any]:
    """Loads runtime settings from environment variables and .env file."""
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "OPENAI_ORG_ID": os.getenv("OPENAI_ORG_ID", ""),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", ""),
        "STANDARD_MODEL": os.getenv("STANDARD_MODEL", "gpt-4o-mini"),
        "STANDARD_TEMPERATURE": os.getenv("STANDARD_TEMPERATURE", "0.7"),
        "STANDARD_MAX_TOKENS": os.getenv("STANDARD_MAX_TOKENS", "1200"),
        "CACHE_TYPE": os.getenv("CACHE_TYPE", "disk"),
        "CACHE_DIR": os.getenv("CACHE_DIR", "./cache"),
        "CACHE_TTL": os.getenv("CACHE_TTL", "3600"),
        "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        "DATA_DIR": os.getenv("DATA_DIR", "./data"),
    }
