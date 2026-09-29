# 架构说明

## 数据流

```
┌────────────────────────────────────────────────────────────────┐
│                        用户浏览器                                │
│  选游戏 + 输入问题 + (可选)勾选 Agent + top_k                   │
└────────────────────┬───────────────────────────────────────────┘
                     │  POST /ask {question, game, top_k, agent}
                     ▼
┌────────────────────────────────────────────────────────────────┐
│                       Flask (app.py)                            │
│  ① 解析 JSON  (绕过 Werkzeug get_json 在 Py3.14 的偶发 bug)    │
│  ② 检查 game 是否注册、key 是否就绪                            │
│  ③ get_agent(game) — 懒加载 + RLock 缓存                       │
└────────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────┐
│                  Game Registry (registry.py)                   │
│  读 data/processed/games.json → GameEntry{csv_path}              │
│  缓存 TfIdfRetriever(RLock 可重入,避免 get_retriever→           │
│  ensure_loaded 自调用死锁)                                      │
└────────────────────┬───────────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────┐
│                 TfIdfRetriever (retriever.py)                  │
│  TF-IDF (1-2gram, max 50k 词) + cosine 召回                    │
│  返回 top-k {index, review, hours_played, helpful, rec, score} │
└────────────────────┬───────────────────────────────────────────┘
                     │
        ┌────────────┴───────────────┐
        │ agent=True                 │ agent=False
        ▼                            ▼
┌──────────────────────┐    ┌────────────────────────┐
│  ReActAgent (agent.py)│    │   single_shot           │
│  ① plan(q) → sub_qs   │    │   (一次检索 + 一次问答) │
│     (LLM call #1)      │    └──────────┬─────────────┘
│  ② 每个 sub_q 检索     │               │
│  ③ synthesize → answer │               │
│     (LLM call #2)      │               │
└──────────┬─────────────┘               │
           └────────────┬────────────────┘
                        ▼
┌────────────────────────────────────────────────────────────────┐
│            Prompt (prompt.py + agent.py)                       │
│  system: 5 条硬规则 + JSON 输出                                │
│  user:   游戏 + 召回片段(含 hours/rec/score)+ 问题 + JSON 模板 │
│  agent:  PLAN_PROMPT / SYNTHESIS_PROMPT  (plan + 二次综合)     │
└────────────────────┬───────────────────────────────────────────┘
                     ▼
┌────────────────────────────────────────────────────────────────┐
│             LLMClient (llm.py) — DeepSeek / OpenAI             │
│  OpenAI 兼容协议,response_format=json_object                   │
│  5xx retry 2 次, 指数退避                                      │
│  ready 属性:无 key 直接 False,前端层优雅拦截                   │
└────────────────────┬───────────────────────────────────────────┘
                     ▼
┌────────────────────────────────────────────────────────────────┐
│                       返回 JSON                                 │
│  {answer, cited_reviews[{index,snippet,reason,original_index}],│
│   sentiment, confidence}                                       │
└────────────────────────────────────────────────────────────────┘
```

## 关键设计权衡

### 1. 为什么先 TF-IDF,不上 embedding

- 2194–4154 条评论 × TF-IDF 内存 50k vocab,启动 <1s,够 demo。
- embedding 要下载 bge 模型(~400MB) + 起 faiss,1-2 天内不值。
- `TfIdfRetriever` 是窄契约(`search(query, top_k) -> list[Hit]`),换 embedding 只需新写一个 `BgeRetriever`,Agent / API 都不用动。

### 2. 为什么 Agent 是 ReAct 而不是 LangChain

- LangChain 引入 ~30 个依赖 + 抽象层,debug 难度高。
- 自实现的 ReAct(plan → 多检索 → synthesize)就 100 行,够 demo。
- 真实生产再换 LangGraph / LangChain Agents。

### 3. 为什么手动 `json.loads`

- Werkzeug 3.1.8 + Python 3.14 上 `request.get_json()` 偶发返回 None/抛 400。
- 直接 `json.loads(request.get_data())` 完全可控,代码量一样。
- 见 `app.py:ask` 注释。

### 4. 为什么 RLock 而不是 Lock

- `get_retriever` 在锁内调 `ensure_loaded`,后者又要抢同一锁。
- `threading.Lock()` 会死锁,`RLock` 才允许同线程重入。
- 这是一个真实踩坑 + 修复记录(`backups/prototype_v1_20260923_171206/` 之前没这个)。

## 版本演进

| 版本 | 关键差异 |
|---|---|
| v1 | Flask + DeepSeek + 单轮 RAG,1 个游戏 |
| v2 | 多游戏 + ReAct Agent + 评估 + pytest + 集中配置 + RLock 修复 |
| v3 | 全链路错误兜底:PLAN 识别无关 / agent 永不抛 / Flask 双层 try + 手动 json.loads / 输入校验 |
| v4 (当前) | Agent reflection loop(自检追加检索) + LRU+TTL 查询缓存(降本) |

## v3 关键修复:非游戏问题 → HTML 兜底 → SyntaxError

**症状**:问"好好好"、"你是来拉屎的吧"等,前端报"网络错误: SyntaxError: Unexpected token '<'"。

**根因**:某些路径抛了非预期异常,Flask 返回 500 HTML,前端 `resp.json()` 解析失败。

**修复**(层层兜底):

1. `PLAN_PROMPT` 让 LLM 识别"与游戏无关",返回 `sub_questions=[]`
2. `agent.run` 收到空 → 直接 off-topic 兜底,不发第二次 LLM
3. `agent.run` / `single_shot` 所有 LLMError / 类型异常 / retriever 异常都被本地 try/except 吞掉,返回 SAFE_FALLBACK dict
4. `_safe_final` / `_safe_single_shot` 强制 final 是合法 dict,`sentiment`/`confidence` 在白名单
5. `app.py /ask` 全包 try/except,任何 view 内异常返回 JSON
6. `@app.errorhandler(Exception)` 兜底 Flask 默认 500 HTML
7. 前端 `JSON.parse` 失败时显示"服务器返回非 JSON(status=xxx)"而不是 SyntaxError