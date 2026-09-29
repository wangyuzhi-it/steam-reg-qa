"""Prompt 模板单元测试。"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rag.prompt import (  # noqa: E402
    SYSTEM_PROMPT,
    USER_TEMPLATE,
    build_context,
    build_messages,
)
from rag.retriever import Hit  # noqa: E402


def _hits():
    return [
        Hit(index=10, review="Combat is great, worth the money.",
             hours_played=42.0, helpful="12", recommendation="Recommended", score=0.31),
        Hit(index=20, review="Needs more optimization atm.",
             hours_played=8.0, helpful="2", recommendation="Not Recommended", score=0.28),
    ]


def test_system_prompt_has_5_rules():
    for k in ("JSON", "评论中未提及", "sentiment", "confidence", "[n]"):
        assert k in SYSTEM_PROMPT


def test_build_context_indexed():
    ctx = build_context(_hits())
    assert "[1]" in ctx and "[2]" in ctx
    assert "hours=42" in ctx
    assert "rec=Recommended" in ctx
    assert "score=0.31" in ctx


def test_build_messages_two_roles():
    msgs = build_messages("Black Myth", _hits(), "is it worth it?")
    assert len(msgs) == 2
    assert msgs[0]["role"] == "system"
    assert msgs[1]["role"] == "user"
    user_content = msgs[1]["content"]
    assert "Black Myth" in user_content
    assert "is it worth it?" in user_content
    assert "[1]" in user_content


def test_user_template_has_json_schema():
    assert "answer" in USER_TEMPLATE
    assert "cited_reviews" in USER_TEMPLATE
    assert "sentiment" in USER_TEMPLATE
    assert "confidence" in USER_TEMPLATE