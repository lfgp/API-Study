# storage/cache_manager.py
import redis
import json
import diskcache as dc
from typing import Any, Optional

class CacheManager:
    def __init__(self, config):
        self.type = config.get("CACHE_TIPO", "disk")
        self.ttl = config.get("CACHE_TTL", 3600)
        
        if self.type == "redis":
            self.cache = redis.Redis.from_url(config.get("REDIS_URL"))
        else:
            self.cache = dc.Cache(config.get("CACHE_DIR", "./cache"))
    
    def get(self, key: str) -> Optional[Any]:
        if self.type == "redis":
            data = self.cache.get(key)
            return json.loads(data) if data else None
        return self.cache.get(key)
    
    def set(self, key: str, value: Any):
        if self.type == "redis":
            self.cache.setex(key, self.ttl, json.dumps(value))
        else:
            self.cache.set(key, value, expire=self.ttl)
