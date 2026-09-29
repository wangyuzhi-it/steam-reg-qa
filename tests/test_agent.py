"""Agent 单元测试:用 mock LLM 验证 plan -> retrieve -> synthesize 流程。"""
import sys
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rag.agent import ReActAgent, single_shot  # noqa: E402
from rag.llm import LLMError  # noqa: E402


@dataclass
class _FakeHit:
    review: str = "stub review"
    hours_played: float = 1.0
    helpful: str = "0"
    recommendation: str = "Recommended"
    score: float = 0.5
    index: int = 0

    def to_dict(self):
        return {"index": self.index, "review": self.review, "score": self.score}


def _make_retriever(hits=None, fail=False):
    retr = MagicMock()
    if fail:
        retr.search.side_effect = RuntimeError("boom")
    else:
        retr.search.return_value = hits if hits is not None else [
            _FakeHit(index=0, review="Combat feels great, totally worth it."),
            _FakeHit(index=1, review="Optimization is meh on PC."),
        ]
    return retr


def test_agent_plan_and_synthesize():
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["combat quality", "performance optimization"]},
        {"answer": "值得买,但需注意优化 [1][2]",
         "cited_reviews": [
             {"index": 1, "snippet": "Combat feels great", "reason": "combat feedback"},
             {"index": 2, "snippet": "Optimization is meh", "reason": "perf feedback"},
         ],
         "sentiment": "mixed", "confidence": "high"},
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("worth buying?", top_k=2)
    assert result.sub_questions == ["combat quality", "performance optimization"]
    assert result.final["sentiment"] == "mixed"
    assert len(result.steps) == 2
    # original_index 映射:renumbered[1] -> all_hits[0].index = 0
    assert result.final["cited_reviews"][0]["original_index"] == 0
    assert llm.chat_json.call_count == 2


def test_agent_plan_returns_empty_for_offtopic():
    """与游戏无关 → plan 返回空 sub_questions → run 直接 off-topic 兜底,不调 synthesize。"""
    llm = MagicMock()
    llm.chat_json.return_value = {"sub_questions": []}
    retr = _make_retriever()
    agent = ReActAgent(llm=llm, retriever=retr, game="TestGame")
    result = agent.run("你是来拉屎的吧", top_k=3)
    assert result.sub_questions == []
    assert result.steps == []
    assert "无关" in result.final["answer"]
    assert result.final["confidence"] == "high"
    # 只调了一次 plan,没调 synthesize
    assert llm.chat_json.call_count == 1


def test_agent_plan_fallback_when_llm_breaks():
    llm = MagicMock()
    llm.chat_json.side_effect = LLMError("bad json")
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("worth buying?", top_k=2)
    # fallback: plan 返回 [原问题],仍会走 synthesize(被 mock 返回)
    assert result.sub_questions == ["worth buying?"]


def test_agent_synthesize_failure_returns_safe_fallback():
    """synthesize 阶段 LLM 抛错时,run 必须兜底返回而不抛。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        LLMError("deepseek 503"),
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    # 不应抛
    result = agent.run("worth buying?", top_k=2)
    assert "评论中未提及" in result.final["answer"]
    assert result.final["cited_reviews"] == []


def test_agent_final_not_dict_safe_fallback():
    """LLM 返回 final 不是 dict 时,run 必须兜底。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        "not a dict at all",  # 直接返回字符串(虽然 chat_json 会 json.loads,但 mock 直接绕过)
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("worth buying?", top_k=2)
    assert result.final["answer"] == "评论中未提及"
    assert result.final["cited_reviews"] == []


def test_agent_final_cited_not_list_sanitized():
    """LLM 返回 cited_reviews 不是 list 时,run 应清洗掉。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        {"answer": "ok", "cited_reviews": "not a list", "sentiment": "good", "confidence": "high"},
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("worth buying?", top_k=2)
    assert result.final["cited_reviews"] == []
    assert result.final["sentiment"] == "mixed"  # "good" 不在白名单


def test_agent_final_bad_sentiment_confidence():
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        {"answer": "ok", "cited_reviews": [],
         "sentiment": "amazing", "confidence": "yes"},
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("worth buying?", top_k=2)
    assert result.final["sentiment"] == "mixed"
    assert result.final["confidence"] == "low"


def test_agent_no_hits_returns_default():
    llm = MagicMock()
    llm.chat_json.return_value = {"sub_questions": ["nothing"]}
    agent = ReActAgent(llm=llm, retriever=_make_retriever(hits=[]), game="TestGame")
    result = agent.run("nothing", top_k=2)
    assert result.final["answer"] == "评论中未提及"
    assert result.final["confidence"] == "low"
    # plan 后没 hits,不调 synthesize
    assert llm.chat_json.call_count == 1


def test_agent_retriever_crash_doesnt_kill_run():
    """retriever.search 抛错时 run 必须继续(空 hits 兜底)。"""
    llm = MagicMock()
    llm.chat_json.return_value = {"sub_questions": ["worth buying"]}
    agent = ReActAgent(llm=llm, retriever=_make_retriever(fail=True), game="TestGame")
    result = agent.run("worth buying?", top_k=2)
    assert result.final["answer"] == "评论中未提及"


def test_single_shot_success():
    llm = MagicMock()
    llm.chat_json.return_value = {
        "answer": "yes", "cited_reviews": [], "sentiment": "positive", "confidence": "high"
    }
    parsed = single_shot(llm, _make_retriever(), "TestGame", "worth?", top_k=2)
    assert parsed["answer"] == "yes"


def test_single_shot_no_hits_returns_fallback():
    llm = MagicMock()
    parsed = single_shot(llm, _make_retriever(hits=[]), "TestGame", "?", top_k=2)
    assert parsed["answer"] == "评论中未提及"
    assert llm.chat_json.call_count == 0


def test_single_shot_llm_error_doesnt_raise():
    llm = MagicMock()
    llm.chat_json.side_effect = LLMError("502")
    parsed = single_shot(llm, _make_retriever(), "TestGame", "?", top_k=2)
    assert "评论中未提及" in parsed["answer"]


def test_single_shot_bad_response_sanitized():
    llm = MagicMock()
    llm.chat_json.return_value = {"answer": 123, "sentiment": "bad"}
    parsed = single_shot(llm, _make_retriever(), "TestGame", "?", top_k=2)
    assert parsed["sentiment"] == "mixed"
    assert parsed["answer"] == "评论中未提及"


def test_agent_to_dict_handles_no_steps():
    """空 steps 时 to_dict 不应崩。"""
    llm = MagicMock()
    llm.chat_json.return_value = {"sub_questions": []}
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("off-topic", top_k=3)
    d = result.to_dict()
    assert d["sub_questions"] == []
    assert d["steps"] == []
    assert "无关" in d["final"]["answer"]


def test_reflect_disabled_short_circuits():
    """reflect=False 时,LLM 不应被调用 reflection 逻辑。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        {"answer": "ok", "cited_reviews": [], "sentiment": "mixed", "confidence": "low"},
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    agent.run("?", top_k=3, reflect=False)
    # plan + synthesize = 2 次
    assert llm.chat_json.call_count == 2


def test_reflect_sufficient_returns_immediately():
    """reflect=True 但 reflection 说充分 → 不追加检索。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        {"answer": "ok", "cited_reviews": [], "sentiment": "mixed", "confidence": "low"},
        {"sufficient": True},
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    agent.run("?", top_k=3, reflect=True)
    # plan + synthesize + reflect = 3 次,但没有第二次 synthesize
    assert llm.chat_json.call_count == 3


def test_reflect_insufficient_triggers_extra_retrieve_and_synthesize():
    """reflect=True 且 insufficient → 追加检索 + 再 synthesize。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        {"answer": "ok", "cited_reviews": [], "sentiment": "mixed", "confidence": "low"},
        {"sufficient": False, "new_sub_questions": ["story plot quality"]},
        {"answer": "更全的答案", "cited_reviews": [], "sentiment": "positive", "confidence": "high"},
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("?", top_k=3, reflect=True)
    # plan + synthesize + reflect + synthesize = 4 次
    assert llm.chat_json.call_count == 4
    assert "worth buying" in result.sub_questions
    assert "story plot quality" in result.sub_questions


def test_reflect_failure_treated_as_sufficient():
    """reflection 抛错时不追加。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        {"answer": "ok", "cited_reviews": [], "sentiment": "mixed", "confidence": "low"},
        LLMError("boom"),
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("?", top_k=3, reflect=True)
    # reflect 抛错被吞,不追加
    assert len(result.sub_questions) == 1
    assert llm.chat_json.call_count == 3


def test_reflect_empty_new_questions_stops():
    """reflection 返回 new_sub_questions=[] 应停止循环,不调第二次 synthesize。"""
    llm = MagicMock()
    llm.chat_json.side_effect = [
        {"sub_questions": ["worth buying"]},
        {"answer": "ok", "cited_reviews": [], "sentiment": "mixed", "confidence": "low"},
        {"sufficient": False, "new_sub_questions": []},
    ]
    agent = ReActAgent(llm=llm, retriever=_make_retriever(), game="TestGame")
    result = agent.run("?", top_k=3, reflect=True)
    assert len(result.sub_questions) == 1
    assert llm.chat_json.call_count == 3