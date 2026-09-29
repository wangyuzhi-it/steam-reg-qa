"""eval.py 的单元 + 集成测试。

纯函数测试(快)+ 真 LLM 端到端(慢,默认 skip if no key)。
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.eval import (  # noqa: E402
    QAResult,
    aggregate,
    evaluate_keywords,
    is_off_topic_correct,
    load_qa,
    render_markdown,
)


# ---------- 纯函数单元测试 ----------

def test_evaluate_keywords_all_match():
    rate, matched, missed = evaluate_keywords("Combat is great, boss fights are fun.", ["combat", "boss"])
    assert rate == 1.0
    assert matched == ["combat", "boss"]
    assert missed == []


def test_evaluate_keywords_partial():
    rate, matched, missed = evaluate_keywords("Combat is great.", ["combat", "boss"])
    assert rate == 0.5
    assert matched == ["combat"]
    assert missed == ["boss"]


def test_evaluate_keywords_empty():
    rate, _, _ = evaluate_keywords("anything", [])
    assert rate == 1.0


def test_evaluate_keywords_case_insensitive():
    rate, matched, _ = evaluate_keywords("Combat is GREAT", ["combat", "great"])
    assert rate == 1.0


def test_is_off_topic_correct():
    assert is_off_topic_correct("这个问题与游戏评论无关") is True
    assert is_off_topic_correct("值得购买,很多人推荐") is False
    assert is_off_topic_correct("无法回答这个问题") is True


def test_load_qa(tmp_path):
    p = tmp_path / "qa.jsonl"
    p.write_text(
        '{"id":1,"game":"X","question":"q1","expect_sentiment":"positive","expect_keywords":["a"]}\n'
        '\n'  # 空行
        '# comment line\n'
        '{"id":2,"game":"Y","question":"q2","expect_sentiment":"mixed","expect_keywords":[]}\n',
        encoding="utf-8",
    )
    qa = load_qa(p)
    assert len(qa) == 2
    assert qa[0]["game"] == "X"


def test_load_qa_limit():
    p = ROOT / "data" / "eval" / "qa.jsonl"
    if not p.exists():
        pytest.skip("qa.jsonl not generated")
    qa = load_qa(p, limit=10)
    assert len(qa) == 10


def test_aggregate_basic():
    rs = [
        QAResult(id=1, game="X", question="q", mode="m",
                 expect_sentiment="positive", expect_keywords=["a"],
                 sentiment="positive", answer="a", sentiment_correct=True,
                 keyword_hit_rate=1.0, keywords_matched=["a"], keywords_missed=[],
                 off_topic_hit=False, n_sub_questions=2, elapsed_sec=2.0,
                 cited_count=1, error=None),
        QAResult(id=2, game="X", question="q2", mode="m",
                 expect_sentiment="mixed", expect_keywords=["b", "c"],
                 sentiment="negative", answer="", sentiment_correct=False,
                 keyword_hit_rate=0.5, keywords_matched=["b"], keywords_missed=["c"],
                 off_topic_hit=False, n_sub_questions=0, elapsed_sec=5.0,
                 cited_count=0, error=None),
    ]
    summary = aggregate(rs, off_topic_ids=set())
    assert summary["total"] == 2
    assert summary["sentiment_accuracy"] == 0.5
    assert summary["keyword_hit_rate_avg"] == 0.75
    assert summary["off_topic_recall"] is None  # 没 off-topic 题
    assert summary["errors"] == 0


def test_aggregate_off_topic():
    rs = [
        QAResult(id=31, game="X", question="hello", mode="m",
                 expect_sentiment="mixed", expect_keywords=["无关"],
                 sentiment="mixed", answer="与游戏评论无关", sentiment_correct=True,
                 keyword_hit_rate=1.0, keywords_matched=["无关"], keywords_missed=[],
                 off_topic_hit=True, n_sub_questions=0, elapsed_sec=1.0,
                 cited_count=0, error=None),
        QAResult(id=32, game="X", question="hi", mode="m",
                 expect_sentiment="mixed", expect_keywords=["无关"],
                 sentiment="mixed", answer="值得购买", sentiment_correct=True,
                 keyword_hit_rate=0.0, keywords_matched=[], keywords_missed=["无关"],
                 off_topic_hit=False, n_sub_questions=2, elapsed_sec=2.0,
                 cited_count=0, error=None),
    ]
    summary = aggregate(rs, off_topic_ids={31, 32})
    assert summary["off_topic_recall"] == 0.5


def test_render_markdown_contains_table():
    rs = [
        QAResult(id=1, game="Black Myth: Wukong", question="q", mode="m",
                 expect_sentiment="positive", expect_keywords=["a"],
                 sentiment="positive", answer="a", sentiment_correct=True,
                 keyword_hit_rate=1.0, keywords_matched=["a"], keywords_missed=[],
                 off_topic_hit=False, n_sub_questions=2, elapsed_sec=2.0,
                 cited_count=1, error=None),
    ]
    md = render_markdown({"m": rs}, {"m": aggregate(rs, set())}, set())
    assert "# Evaluation Report" in md
    assert "| Mode |" in md
    assert "## 单题结果" in md
    assert "## 失败题" in md


# ---------- 集成测试:真 LLM 跑 3 题 ----------

@pytest.fixture(scope="module")
def has_key():
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    import os
    return bool(os.getenv("DEEPSEEK_API_KEY"))


def test_eval_runs_3_questions_single_shot(has_key):
    """跑前 3 题 single_shot,验证端到端评估可用。"""
    if not has_key:
        pytest.skip("no DEEPSEEK_API_KEY")
    qa_path = ROOT / "data" / "eval" / "qa.jsonl"
    if not qa_path.exists():
        pytest.skip("qa.jsonl not generated")
    from scripts.eval import run_qa
    from rag.llm import LLMClient
    llm = LLMClient(provider="deepseek")
    qa_list = load_qa(qa_path, limit=3)
    results = [run_qa(llm, q, "single_shot") for q in qa_list]
    summary = aggregate(results, off_topic_ids=set())
    # 仅断言结构存在,不强制数字(基线会变)
    assert summary["total"] == 3
    assert 0.0 <= summary["sentiment_accuracy"] <= 1.0
    assert summary["elapsed_sec_p95"] > 0


def test_eval_runs_offtopic_question(has_key):
    """off-topic 题必须被识别,answer 里出现「无关」之类的兜底词。"""
    if not has_key:
        pytest.skip("no DEEPSEEK_API_KEY")
    qa_path = ROOT / "data" / "eval" / "qa.jsonl"
    if not qa_path.exists():
        pytest.skip("qa.jsonl not generated")
    from scripts.eval import run_qa
    from rag.llm import LLMClient
    llm = LLMClient(provider="deepseek")
    qa_list = load_qa(qa_path, limit=40)  # 第 31-40 是 off-topic
    # 取一条 off-topic 题(任一 keywords=[无关] 的)
    off_topic_qa = [q for q in qa_list if q.get("expect_keywords") == ["无关"]]
    assert off_topic_qa, "no off-topic QA found"
    r = run_qa(llm, off_topic_qa[0], "agent")
    assert r.off_topic_hit, f"off-topic not detected: answer={r.answer[:120]}"