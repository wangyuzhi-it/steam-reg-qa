"""Agent:ReAct 风格,自动拆问题 → 多轮检索 → 综合回答。

不引入 LangChain,自实现以保持依赖最小。

错误兜底策略:
- plan() 失败 / 返回空 → 用原问题,或返回 [] 表示「与游戏无关」
- synthesize() 失败 → 返回 fallback answer,绝不向上抛
- final 类型校验 → 任何不符合预期都退回安全默认值
- run() 永不抛 LLMError 之外的异常
"""
from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any

from .config import AGENT_MAX_SUBQS
from .llm import LLMClient, LLMError
from .prompt import (
    SYSTEM_PROMPT,
    USER_TEMPLATE,
    build_context,
)
from .retriever import Hit, TfIdfRetriever

log = logging.getLogger(__name__)


SAFE_FALLBACK = {
    "answer": "评论中未提及",
    "cited_reviews": [],
    "sentiment": "mixed",
    "confidence": "low",
}

OFF_TOPIC_ANSWER = {
    "answer": "这个问题与 Steam 游戏评论无关,我帮不到。",
    "cited_reviews": [],
    "sentiment": "mixed",
    "confidence": "high",
}


PLAN_PROMPT = """你是问题拆解助手。给定一个用户的 Steam 评论相关问题,把它拆成 1-{max_n} 个互相不重叠的子问题,
每个子问题对应一次独立的检索(关键词检索 TF-IDF 友好)。

要求:
- 子问题必须是关键词型短语,不要问句。
- 子问题之间尽量正交,合起来覆盖原问题所有维度。
- 如果问题与 Steam 游戏评论完全无关(打招呼、闲聊、辱骂、问候、哲学提问等),
  直接输出 {{"sub_questions": []}},不要勉强造关键词。
- 输出必须是合法 JSON,不要任何解释文字。JSON 格式:
{{"sub_questions": ["phrase1", "phrase2", ...]}}

原问题:{question}
"""


REFLECT_PROMPT = """你是答案审查员。游戏:{game}

原问题:{question}
已检索子问题:{sub_questions}
当前答案(节选):{answer_preview}

任务:评估当前答案是否充分。

判断维度:
1. 是否漏掉原问题中的关键维度?(例:原问题"值不值得买 + 剧情如何",答案只回了值不值得买)
2. 是否与召回片段自相矛盾?
3. 是否有显著的事实缺失值得追加检索?

输出:
- 充分 → {{"sufficient": true}}
- 不充分 → {{"sufficient": false, "new_sub_questions": ["phrase1", ...]}}
  - new_sub_questions 是 1-2 个补充检索短语,关键词型,TF-IDF 友好
  - 不要重复已有子问题
  - 输出必须是合法 JSON,不要任何解释文字
"""


SYNTHESIS_PROMPT = """你是综合客服。游戏:{game}

每轮召回(comment block)被一个子问题检索出来,可能包含矛盾或冗余信息。
请基于所有召回片段,综合给出最终答案。

硬性规则(同主 Prompt):
1. 必须从召回片段中归纳,无依据就说「评论中未提及」。
2. 输出必须是合法 JSON,不要 markdown 代码块。
3. cited_reviews 的 index 必须是 user 消息里实际出现的 [n] 编号。
4. sentiment 必须是 positive | mixed | negative 之一。
5. confidence 必须是 high | medium | low 之一。

{all_contexts}

用户原问题:{question}

JSON 格式:
{{
  "answer": "中文回答,引用 [n]",
  "cited_reviews": [{{"index": 1, "snippet": "...", "reason": "..."}}],
  "sentiment": "positive | mixed | negative",
  "confidence": "high | medium | low"
}}
"""


@dataclass
class AgentStep:
    sub_question: str
    hits: list[Hit]


@dataclass
class AgentResult:
    sub_questions: list[str]
    steps: list[AgentStep]
    final: dict

    def to_dict(self) -> dict:
        return {
            "sub_questions": self.sub_questions,
            "steps": [
                {
                    "sub_question": s.sub_question,
                    "hits": [h.to_dict() for h in s.hits],
                }
                for s in self.steps
            ],
            "final": self.final,
        }


class ReActAgent:
    def __init__(self, llm: LLMClient, retriever: TfIdfRetriever, game: str):
        self.llm = llm
        self.retriever = retriever
        self.game = game

    def plan(self, question: str) -> list[str]:
        """让 LLM 把问题拆成子问题。

        返回 [] 表示「与游戏无关」。
        失败 fallback 到 [原问题](退化为单子问题路径)。
        """
        msgs = [
            {"role": "system", "content": "你是问题拆解助手,只输出合法 JSON。"},
            {"role": "user", "content": PLAN_PROMPT.format(
                max_n=AGENT_MAX_SUBQS, question=question)},
        ]
        try:
            data = self.llm.chat_json(msgs, temperature=0.2)
            subs = data.get("sub_questions") or []
            subs = [str(s).strip() for s in subs if str(s).strip()]
            return subs[:AGENT_MAX_SUBQS]  # 空列表表示「与游戏无关」
        except (LLMError, ValueError, KeyError, AttributeError) as e:
            log.warning("plan failed (%s), fallback to original question", e)
            return [question]

    def _safe_final(self, raw: Any) -> dict:
        """把 LLM 返回的不确定结构强行规范化为合法 dict。"""
        if not isinstance(raw, dict):
            log.warning("final is not dict: %r, using SAFE_FALLBACK", type(raw))
            return dict(SAFE_FALLBACK)
        answer = raw.get("answer")
        if not isinstance(answer, str) or not answer.strip():
            raw["answer"] = SAFE_FALLBACK["answer"]
        if raw.get("sentiment") not in ("positive", "mixed", "negative"):
            raw["sentiment"] = "mixed"
        if raw.get("confidence") not in ("high", "medium", "low"):
            raw["confidence"] = "low"
        cited = raw.get("cited_reviews")
        if not isinstance(cited, list):
            raw["cited_reviews"] = []
        else:
            raw["cited_reviews"] = [c for c in cited if isinstance(c, dict)]
        return raw

    def _renumber_cited(self, all_hits: list[Hit], final: dict) -> None:
        """把 [1..N] 的 renumbered index 映射回原始 csv 行号 original_index。"""
        cite_map = {i + 1: all_hits[i].index for i in range(len(all_hits))}
        for c in final.get("cited_reviews", []):
            c["original_index"] = cite_map.get(c.get("index", -1), -1)

    def _reflect(self, question: str, sub_questions: list[str],
                 current_answer: str) -> tuple[bool, list[str]]:
        """让 LLM 评估当前答案是否充分。

        返回 (sufficient, new_sub_questions)。
        失败时按"充分"处理,不再追加检索(节省 token)。
        """
        answer_preview = (current_answer or "")[:400]
        msgs = [
            {"role": "system", "content": "你是答案审查员,只输出合法 JSON。"},
            {"role": "user", "content": REFLECT_PROMPT.format(
                game=self.game, question=question,
                sub_questions=sub_questions,
                answer_preview=answer_preview,
            )},
        ]
        try:
            data = self.llm.chat_json(msgs, temperature=0.1)
        except (LLMError, ValueError, KeyError, AttributeError) as e:
            log.warning("reflect failed (%s), treat as sufficient", e)
            return True, []
        if not isinstance(data, dict):
            return True, []
        if not data.get("sufficient", True):
            new_subs = data.get("new_sub_questions") or []
            new_subs = [str(s).strip() for s in new_subs if str(s).strip()][:2]
            if new_subs:
                return False, new_subs
        return True, []

    def run(self, question: str, top_k: int = 5,
            reflect: bool = False, max_reflections: int = 1) -> AgentResult:
        """跑 Agent。

        Args:
            question: 用户问题
            top_k: 每轮检索条数
            reflect: 是否启用 reflection loop(默认关,会多调 1-2 次 LLM)
            max_reflections: reflection 最多追加几轮
        """
        sub_qs = self.plan(question)
        log.info("agent plan: %s -> %s", question, sub_qs)

        if not sub_qs:
            # 与游戏无关,直接返回,不调 synthesize 省 token + 时延
            return AgentResult(
                sub_questions=[],
                steps=[],
                final=dict(OFF_TOPIC_ANSWER),
            )

        steps: list[AgentStep] = []
        seen_indexes: set[int] = set()
        all_hits: list[Hit] = []
        for sq in sub_qs:
            try:
                hits = self.retriever.search(sq, top_k=top_k)
            except Exception as e:
                log.warning("retriever.search(%r) failed: %s", sq, e)
                hits = []
            steps.append(AgentStep(sub_question=sq, hits=hits))
            for h in hits:
                if h.index not in seen_indexes:
                    seen_indexes.add(h.index)
                    all_hits.append(h)

        if not all_hits:
            return AgentResult(
                sub_questions=sub_qs,
                steps=steps,
                final=dict(SAFE_FALLBACK),
            )

        def _synthesize() -> dict:
            contexts = []
            for sq, step in zip(sub_qs, steps):
                ctx = build_context(step.hits)
                contexts.append(f"子问题:{sq}\n召回片段:\n{ctx}")
            all_contexts = "\n\n---\n\n".join(contexts)
            msgs = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": SYNTHESIS_PROMPT.format(
                    game=self.game,
                    all_contexts=all_contexts,
                    question=question,
                )},
            ]
            try:
                final = self.llm.chat_json(msgs)
                final = self._safe_final(final)
                self._renumber_cited(all_hits, final)
                return final
            except LLMError as e:
                log.warning("synthesize failed (%s), return fallback", e)
                return {
                    **SAFE_FALLBACK,
                    "answer": f"评论中未提及(综合阶段失败:{type(e).__name__})",
                }
            except Exception as e:
                log.exception("unexpected error in synthesize")
                return {
                    **SAFE_FALLBACK,
                    "answer": f"评论中未提及(内部错误:{type(e).__name__})",
                }

        final = _synthesize()

        # reflection loop
        if reflect:
            for _ in range(max_reflections):
                sufficient, new_subs = self._reflect(
                    question, sub_qs, final.get("answer", ""))
                if sufficient or not new_subs:
                    break
                log.info("reflection: adding sub_questions=%s", new_subs)
                for ns in new_subs:
                    try:
                        hits = self.retriever.search(ns, top_k=top_k)
                    except Exception as e:
                        log.warning("reflection retriever failed: %s", e)
                        hits = []
                    steps.append(AgentStep(sub_question=ns, hits=hits))
                    sub_qs = sub_qs + [ns]
                    for h in hits:
                        if h.index not in seen_indexes:
                            seen_indexes.add(h.index)
                            all_hits.append(h)
                final = _synthesize()

        return AgentResult(sub_questions=sub_qs, steps=steps, final=final)


def single_shot(llm: LLMClient, retriever: TfIdfRetriever, game: str,
                question: str, top_k: int) -> dict:
    """退化路径:不调 plan,单次检索 + 单次问答。供 eval 对比。

    任何错误都返回 SAFE_FALLBACK,绝不抛异常。
    """
    try:
        hits = retriever.search(question, top_k=top_k)
    except Exception as e:
        log.warning("retriever.search failed in single_shot: %s", e)
        hits = []

    if not hits:
        return dict(SAFE_FALLBACK)

    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_TEMPLATE.format(
            game=game, context=build_context(hits), question=question,
        )},
    ]
    try:
        final = llm.chat_json(msgs)
        return _safe_single_shot(final)
    except LLMError as e:
        log.warning("single_shot llm failed: %s", e)
        return {
            **SAFE_FALLBACK,
            "answer": f"评论中未提及(生成失败:{type(e).__name__})",
        }
    except Exception as e:
        log.exception("unexpected error in single_shot")
        return {
            **SAFE_FALLBACK,
            "answer": f"评论中未提及(内部错误:{type(e).__name__})",
        }


def _safe_single_shot(raw: Any) -> dict:
    if not isinstance(raw, dict):
        return dict(SAFE_FALLBACK)
    if raw.get("sentiment") not in ("positive", "mixed", "negative"):
        raw["sentiment"] = "mixed"
    if raw.get("confidence") not in ("high", "medium", "low"):
        raw["confidence"] = "low"
    cited = raw.get("cited_reviews")
    if not isinstance(cited, list):
        raw["cited_reviews"] = []
    else:
        raw["cited_reviews"] = [c for c in cited if isinstance(c, dict)]
    if not isinstance(raw.get("answer"), str):
        raw["answer"] = SAFE_FALLBACK["answer"]
    return raw