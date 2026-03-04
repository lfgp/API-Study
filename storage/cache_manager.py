from __future__ import annotations

import json
from typing import Any, Optional

try:
    import diskcache as dc
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal test envs
    dc = None

try:
    import redis
except ModuleNotFoundError:  # pragma: no cover - fallback for minimal test envs
    redis = None


class CacheManager:
    def __init__(self, config: dict[str, Any]):
        self.cache_type = (config.get("CACHE_TYPE") or "disk").strip().lower()
        self.ttl = int(config.get("CACHE_TTL", 3600))

        self._fallback_cache: dict[str, Any] = {}

        if self.cache_type == "redis" and redis is not None:
            self.cache = redis.Redis.from_url(config.get("REDIS_URL", "redis://localhost:6379/0"))
            return

        if dc is not None:
            self.cache = dc.Cache(config.get("CACHE_DIR", "./cache"))
            return

        self.cache = None

    def get(self, key: str) -> Optional[Any]:
        if self.cache_type == "redis":
            if self.cache is None:
                return self._fallback_cache.get(key)
            raw = self.cache.get(key)
            return json.loads(raw) if raw else None
        if self.cache is None:
            return self._fallback_cache.get(key)
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        if self.cache_type == "redis":
            if self.cache is None:
                self._fallback_cache[key] = value
                return
            self.cache.setex(key, self.ttl, json.dumps(value, ensure_ascii=False))
            return
        if self.cache is None:
            self._fallback_cache[key] = value
            return
        self.cache.set(key, value, expire=self.ttl)

    @staticmethod
    def make_key(*parts: Any) -> str:
        return "::".join(str(part) for part in parts)
