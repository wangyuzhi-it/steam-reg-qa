# Prompt 设计说明

## 设计原则

1. **拒答护栏优于幻觉**:让模型在没依据时说"评论中未提及",而不是编造。
2. **强制结构化**:用 `response_format={"type":"json_object"}` + system 硬约束,前端可零成本解析。
3. **可观测引用**:要求模型引用召回片段的 `[n]` 编号,便于回溯到原始评论。
4. **元信息入 prompt**:把 `hours_played`、`recommendation`、`tfidf_score` 拼进去,模型能区分深度玩家评价和水军短评。

## System Prompt

```text
你是 Steam 游戏评论分析助手,只能基于用户提供的「召回评论片段」作答。

硬性规则:
1. 答案必须从召回片段中归纳得出,无依据就回答「评论中未提及」,不得编造。
2. 输出必须是合法 JSON,不要任何解释文字、不要 markdown 代码块。
3. cited_reviews 里只列你实际引用的片段,索引需对应 user 消息中的 [n]。
4. sentiment 必须是 positive | mixed | negative 之一。
5. confidence 必须是 high | medium | low 之一,根据引用片段数量与一致性判断。
```

要点:
- 规则 1 是"拒答护栏",防幻觉。
- 规则 2 + `response_format=json_object` 双保险,即便模型偶尔违反 system,API 也会兜住 JSON 形态。
- 规则 4、5 锁枚举,前端不用做容错。

## User Prompt 模板

```text
游戏:{game}

召回评论片段:
{context}

用户问题:{question}

请按下面 JSON 结构回答:
{{
  "answer": "用中文回答,简洁,引用 [n] 标注依据",
  "cited_reviews": [
    {{"index": 1, "snippet": "原片段前 80 字", "reason": "为什么引用"}}
  ],
  "sentiment": "positive | mixed | negative",
  "confidence": "high | medium | low"
}}
```

`{context}` 由 `rag/prompt.py:build_context` 拼装,格式:

```
[1] (hours=42 helpful=12 rec=Recommended score=0.31)
<前 300 字评论片段>
[2] (hours=8 helpful=2 rec=Not Recommended score=0.28)
<前 300 字评论片段>
```

## 输出 JSON

```json
{
  "answer": "玩家普遍认为值得买,但优化欠佳 [1][2]",
  "cited_reviews": [
    {"index": 1, "snippet": "Masterpiece, what a beautiful game...", "reason": "高分好评样本"},
    {"index": 2, "snippet": "needs some more optimization atm...", "reason": "指出优化短板"}
  ],
  "sentiment": "mixed",
  "confidence": "high"
}
```

## 迭代记录

| 版本 | 改动 | 解决什么问题 |
|---|---|---|
| v1 | 首版,5 条硬规则 + 双保险 JSON | 基础可跑通 |
| v2 | 新增 `PLAN_PROMPT`(拆问题)+ `SYNTHESIS_PROMPT`(综合) | Agent 多轮检索,复杂问题拆维度独立检索再合并 |

## v2 新增:问题拆解 (PLAN_PROMPT)

```
你是问题拆解助手。给定一个用户的 Steam 评论相关问题,把它拆成 1-3 个互相不重叠的子问题,
每个子问题对应一次独立的检索(关键词检索 TF-IDF 友好)。

要求:
- 子问题必须是关键词型短语,不要问句。
- 子问题之间尽量正交,合起来覆盖原问题所有维度。
- 输出必须是 JSON,不要任何解释文字。JSON 格式:
{"sub_questions": ["phrase1", "phrase2", ...]}
```

要点:**关键词短语**而不是完整问句,因为下游是 TF-IDF(关键词匹配),问句中的停用词反而干扰。例:
- `"值得买吗?剧情如何?"` → `["worth buying", "story plot quality"]`(2 个)

## v2 新增:综合 (SYNTHESIS_PROMPT)

把多轮召回拼一起,让 LLM 当综合客服。同一组 5 条硬规则,只是上下文从单轮换成多轮 `子问题:xx \n 召回:yy` 的拼接。

## 实现位置

- `rag/prompt.py`:单轮 `SYSTEM_PROMPT` / `USER_TEMPLATE` / `build_messages`
- `rag/agent.py`:`PLAN_PROMPT` / `SYNTHESIS_PROMPT`,Agent 编排