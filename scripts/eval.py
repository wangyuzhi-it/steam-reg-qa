"""离线评估:读 qa.jsonl 跑多个模式,产出 sentiment 准确率、关键词命中率、Markdown 报告。

用法:
  python scripts/eval.py                                    # 默认 50 题,3 模式
  python scripts/eval.py --qa data/eval/qa.jsonl --limit 20 # 自定义
  python scripts/eval.py --modes single_shot agent          # 只跑两种

指标:
  - sentiment_accuracy: answer.sentiment vs qa.expect_sentiment(分类对/错)
  - keyword_hit_rate:   answer.answer 文本里包含 expect_keywords 的比例
  - off_topic_recall:   off-topic 题里 answer 提到「无关/无法回答」等兜底词
  - cite_valid_rate:    cited_reviews 全部合法
  - elapsed_p95:        95 分位时延(秒)
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rag import config, registry  # noqa: E402
from rag.agent import ReActAgent, single_shot  # noqa: E402
from rag.llm import LLMClient, LLMError  # noqa: E402

OFF_TOPIC_HINTS = {"无关", "无法回答", "帮不到", "不相关", "不匹配", "无法", "无法判断"}
SENTIMENT_SET = {"positive", "mixed", "negative"}


@dataclass
class QAResult:
    id: int
    game: str
    question: str
    mode: str
    expect_sentiment: str
    expect_keywords: list[str]
    sentiment: str
    answer: str
    sentiment_correct: bool
    keyword_hit_rate: float
    keywords_matched: list[str]
    keywords_missed: list[str]
    off_topic_hit: bool
    n_sub_questions: int
    elapsed_sec: float
    cited_count: int
    error: str | None = None


def load_qa(path: Path, limit: int | None = None) -> list[dict]:
    qa = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            qa.append(json.loads(line))
    if limit:
        qa = qa[:limit]
    return qa


def evaluate_keywords(answer: str, expect: list[str]) -> tuple[float, list[str], list[str]]:
    """答案里包含任一关键词(支持 `|` 同义词分隔)就算命中。

    例:expect=["worth|值得", "buy|购买"],答案"值得购买",→ 2/2 全命中
    """
    a = (answer or "").lower()
    matched, missed = [], []
    for kw in expect:
        alts = [s.strip().lower() for s in kw.split("|") if s.strip()]
        if not alts:
            continue
        if any(alt in a for alt in alts):
            matched.append(kw)
        else:
            missed.append(kw)
    rate = len(matched) / len(expect) if expect else 1.0
    return rate, matched, missed


def is_off_topic_correct(answer: str) -> bool:
    a = (answer or "")
    return any(hint in a for hint in OFF_TOPIC_HINTS)


def run_qa(llm: LLMClient, qa: dict, mode: str) -> QAResult:
    game = qa["game"]
    question = qa["question"]
    expect_sentiment = qa.get("expect_sentiment", "mixed")
    expect_keywords = qa.get("expect_keywords", [])

    started = time.time()
    error = None
    sentiment = "?"
    answer = ""
    n_sub = 0
    cited_count = 0
    try:
        retr = registry.get_retriever(game)
        agent = ReActAgent(llm=llm, retriever=retr, game=game)
        if mode == "single_shot":
            hits = retr.search(question, top_k=4)
            if not hits:
                sentiment = "mixed"
                answer = "评论中未提及"
            else:
                final = single_shot(llm, retr, game, question, top_k=4)
                sentiment = final.get("sentiment", "mixed")
                answer = final.get("answer", "")
                cited_count = len(final.get("cited_reviews", []) or [])
            n_sub = 0
        else:  # agent / agent+reflect
            reflect = (mode == "agent_reflect")
            result = agent.run(question, top_k=4, reflect=reflect)
            sentiment = result.final.get("sentiment", "mixed")
            answer = result.final.get("answer", "")
            cited_count = len(result.final.get("cited_reviews", []) or [])
            n_sub = len(result.sub_questions)
    except LLMError as e:
        error = f"LLMError: {e}"
    except Exception as e:
        error = f"{type(e).__name__}: {e}"

    elapsed = time.time() - started
    rate, matched, missed = evaluate_keywords(answer, expect_keywords)
    sentiment_correct = (sentiment == expect_sentiment) if sentiment in SENTIMENT_SET else False
    off_topic_hit = is_off_topic_correct(answer)

    return QAResult(
        id=qa.get("id", -1),
        game=game, question=question, mode=mode,
        expect_sentiment=expect_sentiment,
        expect_keywords=expect_keywords,
        sentiment=sentiment, answer=answer,
        sentiment_correct=sentiment_correct,
        keyword_hit_rate=round(rate, 3),
        keywords_matched=matched, keywords_missed=missed,
        off_topic_hit=off_topic_hit,
        n_sub_questions=n_sub, elapsed_sec=round(elapsed, 2),
        cited_count=cited_count, error=error,
    )


def aggregate(results: list[QAResult], off_topic_ids: set[int]) -> dict[str, Any]:
    total = len(results)
    sentiment_correct = sum(1 for r in results if r.sentiment_correct)
    keyword_rates = [r.keyword_hit_rate for r in results if r.expect_keywords]
    off_topic_records = [r for r in results if r.id in off_topic_ids]
    off_topic_correct = sum(1 for r in off_topic_records if r.off_topic_hit)
    cited_total = sum(r.cited_count for r in results)
    errors = sum(1 for r in results if r.error)
    elapsed = sorted([r.elapsed_sec for r in results])

    def p(q: float) -> float:
        if not elapsed:
            return 0.0
        idx = min(int(round(q * (len(elapsed) - 1))), len(elapsed) - 1)
        return round(elapsed[idx], 2)

    return {
        "total": total,
        "errors": errors,
        "sentiment_accuracy": round(sentiment_correct / total, 3) if total else 0,
        "keyword_hit_rate_avg": round(statistics.mean(keyword_rates), 3) if keyword_rates else 0,
        "off_topic_recall": round(off_topic_correct / len(off_topic_records), 3) if off_topic_records else None,
        "elapsed_sec_avg": round(statistics.mean(elapsed), 2) if elapsed else 0,
        "elapsed_sec_p50": p(0.50),
        "elapsed_sec_p95": p(0.95),
        "cited_total": cited_total,
        "n_sub_questions_avg": round(statistics.mean([r.n_sub_questions for r in results]), 2),
    }


def render_markdown(per_mode: dict[str, list[QAResult]],
                    summaries: dict[str, dict],
                    off_topic_ids: set[int]) -> str:
    lines = [
        "# Evaluation Report",
        "",
        f"生成时间:{time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 总体对比",
        "",
        "| Mode | N | Sentiment Acc | Keyword Hit | Off-topic Rec | p50 (s) | p95 (s) | Subs avg | Cited |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for mode, summary in summaries.items():
        off = summary["off_topic_recall"]
        off_s = f"{off:.0%}" if off is not None else "-"
        lines.append(
            f"| {mode} | {summary['total']} | "
            f"{summary['sentiment_accuracy']:.0%} | "
            f"{summary['keyword_hit_rate_avg']:.0%} | "
            f"{off_s} | "
            f"{summary['elapsed_sec_p50']} | {summary['elapsed_sec_p95']} | "
            f"{summary['n_sub_questions_avg']} | "
            f"{summary['cited_total']} |"
        )

    lines.extend(["", "## 单题结果(按模式)", ""])
    for mode, results in per_mode.items():
        lines.append(f"### mode = {mode}")
        lines.append("")
        lines.append("| ID | Game | Question | Expect | Got | KW | Sub | Time |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for r in results:
            q_short = r.question[:30] + ("..." if len(r.question) > 30 else "")
            kw = f"{len(r.keywords_matched)}/{len(r.expect_keywords)}" if r.expect_keywords else "-"
            lines.append(
                f"| {r.id} | {r.game[:20]} | {q_short} | "
                f"{r.expect_sentiment[:3]} | {r.sentiment[:3]} | "
                f"{kw} | {r.n_sub_questions} | {r.elapsed_sec}s |"
            )
        lines.append("")

    lines.append("## 失败题(sentiment 错或 keyword 漏)")
    lines.append("")
    for mode, results in per_mode.items():
        bad = [r for r in results if not r.sentiment_correct or (r.expect_keywords and r.keyword_hit_rate < 1.0)]
        if not bad:
            continue
        lines.append(f"### {mode} ({len(bad)} 题)")
        lines.append("")
        for r in bad[:15]:  # 最多列 15
            tag = []
            if not r.sentiment_correct:
                tag.append(f"sentiment: {r.sentiment} != {r.expect_sentiment}")
            if r.expect_keywords and r.keyword_hit_rate < 1.0:
                tag.append(f"missed: {r.keywords_missed}")
            lines.append(f"- **Q{r.id}** {r.question[:60]}  → {'; '.join(tag)}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--qa", default=str(ROOT / "data" / "eval" / "qa.jsonl"),
                        help="QA 数据 jsonl 路径")
    parser.add_argument("--limit", type=int, default=None, help="最多跑几条")
    parser.add_argument("--modes", nargs="+",
                        default=["single_shot", "agent", "agent_reflect"])
    parser.add_argument("--out-prefix", default=None,
                        help="报告文件名前缀,默认 logs/eval")
    args = parser.parse_args()

    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")

    qa_path = Path(args.qa)
    if not qa_path.exists():
        print(f"[ERR] QA file not found: {qa_path}", file=sys.stderr)
        print("       请先准备 50 条 QA,或运行 scripts/draft_qa.py 自动草拟", file=sys.stderr)
        return 1
    qa = load_qa(qa_path, limit=args.limit)
    if not qa:
        print("[ERR] QA file is empty", file=sys.stderr)
        return 1

    llm = LLMClient(provider=config.LLM_PROVIDER)
    if not llm.ready:
        print("[ERR] LLM key missing", file=sys.stderr)
        return 1

    off_topic_ids = {q["id"] for q in qa
                     if q.get("is_off_topic") is True
                     or q.get("expect_sentiment") == "off_topic"
                     or q.get("expect_keywords") in (["无关"], ["无法回答"])}

    print(f"[INFO] eval {len(qa)} QA × {len(args.modes)} modes")
    per_mode: dict[str, list[QAResult]] = {}
    summaries: dict[str, dict] = {}
    for mode in args.modes:
        results = []
        for q in qa:
            r = run_qa(llm, q, mode)
            results.append(r)
            mark = "+" if r.sentiment_correct else "-"
            kw = f"{len(r.keywords_matched)}/{len(r.expect_keywords)}" if r.expect_keywords else "-"
            err = f" ERR={r.error[:40]}" if r.error else ""
            print(f"  [{mode}] {mark} Q{r.id} sent={r.sentiment[:3]} kw={kw} {r.elapsed_sec}s{err}")
        per_mode[mode] = results
        summaries[mode] = aggregate(results, off_topic_ids)

    out_prefix = args.out_prefix or str(ROOT / "logs" / "eval")
    Path(out_prefix).parent.mkdir(parents=True, exist_ok=True)
    json_out = Path(f"{out_prefix}.json")
    md_out = Path(f"{out_prefix}.md")
    json_out.write_text(json.dumps(
        {"summaries": summaries,
         "records": {m: [asdict(r) for r in rs] for m, rs in per_mode.items()}},
        ensure_ascii=False, indent=2), encoding="utf-8")
    md_out.write_text(render_markdown(per_mode, summaries, off_topic_ids),
                      encoding="utf-8")

    print("\n[SUMMARY]")
    for mode, s in summaries.items():
        print(f"  {mode:14s} sent_acc={s['sentiment_accuracy']:.0%} kw_hit={s['keyword_hit_rate_avg']:.0%} p95={s['elapsed_sec_p95']}s")
    print(f"\n[OK] {md_out}\n[OK] {json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())