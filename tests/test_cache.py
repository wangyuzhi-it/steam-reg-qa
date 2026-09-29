"""ResponseCache 单元测试。"""
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rag.cache import ResponseCache  # noqa: E402


def test_make_key_is_stable():
    k1 = ResponseCache.make_key({"a": 1, "b": 2})
    k2 = ResponseCache.make_key({"b": 2, "a": 1})
    assert k1 == k2, "key must be order-independent"


def test_make_key_different_inputs_different_keys():
    k1 = ResponseCache.make_key({"q": "x"})
    k2 = ResponseCache.make_key({"q": "y"})
    assert k1 != k2


def test_get_miss_then_hit():
    c = ResponseCache()
    k = "k1"
    assert c.get(k) is None
    assert c.misses == 1
    c.set(k, {"v": 1})
    assert c.get(k) == {"v": 1}
    assert c.hits == 1


def test_ttl_expiry():
    c = ResponseCache(ttl_sec=0.1)
    c.set("k", {"v": 1})
    assert c.get("k") == {"v": 1}
    time.sleep(0.15)
    assert c.get("k") is None
    # 第一次 get:hit;第二次 get (ttl 过期):miss
    assert c.hits == 1
    assert c.misses == 1


def test_lru_eviction():
    c = ResponseCache(max_size=2)
    c.set("a", {"v": 1})
    c.set("b", {"v": 2})
    c.set("c", {"v": 3})  # 触发 LRU,删 a
    assert c.get("a") is None
    assert c.get("b") == {"v": 2}
    assert c.get("c") == {"v": 3}
    stats = c.stats()
    assert stats["size"] == 2


def test_stats_fields():
    c = ResponseCache()
    s = c.stats()
    for k in ("hits", "misses", "size", "max_size", "ttl_sec", "hit_rate"):
        assert k in s


def test_hit_rate_zero_when_no_calls():
    c = ResponseCache()
    assert c.stats()["hit_rate"] == 0.0


def test_clear_resets():
    c = ResponseCache()
    c.set("k", {"v": 1})
    c.get("k")  # hit
    c.get("x")  # miss
    c.clear()
    s = c.stats()
    assert s["hits"] == 0 and s["misses"] == 0 and s["size"] == 0


def test_thread_safety_smoke():
    """烟雾测试:并发 set/get 不抛异常、最终 size 不超限。"""
    import threading
    c = ResponseCache(max_size=100)
    def worker(i):
        for j in range(50):
            c.set(f"k-{i}-{j}", {"v": j})
            c.get(f"k-{i}-{j}")
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads: t.start()
    for t in threads: t.join()
    s = c.stats()
    assert s["size"] <= 100