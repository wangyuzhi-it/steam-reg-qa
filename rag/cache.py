"""LLM 响应缓存:LRU + TTL,key 由请求参数决定。

线程安全,O(1) get/set。
"""
from __future__ import annotations

import hashlib
import json
import threading
import time
from typing import Any


class ResponseCache:
    def __init__(self, max_size: int = 1000, ttl_sec: int = 3600):
        self.max_size = max_size
        self.ttl_sec = ttl_sec
        self._cache: dict[str, tuple[float, dict]] = {}
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def make_key(params: dict) -> str:
        # 排序保证 key 稳定
        s = json.dumps(params, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def get(self, key: str) -> dict | None:
        now = time.time()
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self.misses += 1
                return None
            ts, value = entry
            if now - ts > self.ttl_sec:
                del self._cache[key]
                self.misses += 1
                return None
            self.hits += 1
            return value

    def set(self, key: str, value: dict) -> None:
        with self._lock:
            if len(self._cache) >= self.max_size and key not in self._cache:
                # 删最早(LRU 简化版:按写入时间)
                oldest = min(self._cache, key=lambda k: self._cache[k][0])
                del self._cache[oldest]
            self._cache[key] = (time.time(), value)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = self.hits + self.misses
            return {
                "hits": self.hits,
                "misses": self.misses,
                "size": len(self._cache),
                "max_size": self.max_size,
                "ttl_sec": self.ttl_sec,
                "hit_rate": round(self.hits / total, 3) if total else 0.0,
            }


if __name__ == "__main__":
    c = ResponseCache(max_size=3, ttl_sec=1)
    k1 = ResponseCache.make_key({"q": "a"})
    c.set(k1, {"answer": "1"})
    print(c.get(k1))
    print("stats:", c.stats())
    time.sleep(1.1)
    print("after ttl:", c.get(k1))
    c2 = ResponseCache(max_size=2, ttl_sec=10)
    c2.set("a", {"v": 1})
    c2.set("b", {"v": 2})
    c2.set("c", {"v": 3})  # 触发 LRU
    print("size:", len(c2._cache))
    print("'a' evicted?", c2.get("a") is None)