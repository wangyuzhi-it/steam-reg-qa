"""Prompt 模板:system + user,强制结构化 JSON 输出。"""

from __future__ import annotations

SYSTEM_PROMPT = """你是 Steam 游戏评论分析助手,只能基于用户提供的「召回评论片段」作答。

硬性规则:
1. 答案必须从召回片段中归纳得出,无依据就回答「评论中未提及」,不得编造。
2. 输出必须是合法 JSON,不要任何解释文字、不要 markdown 代码块。
3. cited_reviews 里只列你实际引用的片段,索引需对应 user 消息中的 [n]。
4. sentiment 必须是 positive | mixed | negative 之一。
5. confidence 必须是 high | medium | low 之一,根据引用片段数量与一致性判断。
"""

USER_TEMPLATE = """游戏:{game}

召回评论片段:
{context}

用户问题:{question}

请按下面 JSON 结构回答(注意是 JSON,不要包在代码块里):
{{
  "answer": "用中文回答,简洁,引用 [n] 标注依据",
  "cited_reviews": [
    {{"index": 1, "snippet": "原片段前 80 字", "reason": "为什么引用"}}
  ],
  "sentiment": "positive | mixed | negative",
  "confidence": "high | medium | low"
}}
"""


def build_context(hits: list, max_chars: int = 300) -> str:
    lines = []
    for i, h in enumerate(hits, start=1):
        snippet = h.review[:max_chars]
        meta = f"hours={h.hours_played:.0f} helpful={h.helpful} rec={h.recommendation} score={h.score:.2f}"
        lines.append(f"[{i}] ({meta})\n{snippet}")
    return "\n\n".join(lines)


def build_messages(game: str, hits: list, question: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_TEMPLATE.format(
            game=game,
            context=build_context(hits),
            question=question,
        )},
    ]