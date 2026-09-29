"""Retriever 单元测试:不调 LLM,纯本地。"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rag import registry  # noqa: E402
from rag.retriever import TfIdfRetriever  # noqa: E402


def test_registry_lists_games():
    games = registry.list_games()
    assert games, "no games registered; run scripts/sample_reviews.py first"
    names = [g.name for g in games]
    assert "Black Myth: Wukong" in names


def test_search_returns_relevant():
    g = next(x for x in registry.list_games() if x.name == "Black Myth: Wukong")
    retr = TfIdfRetriever(g.csv_path)
    hits = retr.search("worth buying", top_k=3)
    assert len(hits) == 3
    assert all(h.score > 0 for h in hits)
    # top-1 的 review 应包含 'worth' / 'buy' 之类的相关词(宽松匹配)
    top = hits[0].review.lower()
    assert any(k in top for k in ("worth", "buy", "recommend", "money"))


def test_search_empty_query():
    g = next(x for x in registry.list_games() if x.name == "Black Myth: Wukong")
    retr = TfIdfRetriever(g.csv_path)
    assert retr.search("", top_k=3) == []


def test_search_top_k_bounds():
    g = next(x for x in registry.list_games() if x.name == "Black Myth: Wukong")
    retr = TfIdfRetriever(g.csv_path)
    for k in (1, 5, 10):
        hits = retr.search("combat boss fight", top_k=k)
        assert 1 <= len(hits) <= k