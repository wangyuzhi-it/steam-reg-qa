# Steam 评论 RAG 问答系统
基于 Flask + LLM API 实现的多游戏评论 RAG 问答系统项目,使用Python Flask + DeepSeek API,支持 ReAct Agent 自动拆解问题、Reflection 自检追加检索、LRU 缓存降本;基于 50 条人工 QA 评测,sentiment 准确率 74%,off-topic 召回 100%。


---

## TLDR:

这是一个网页demo:
- 用户选游戏、输入问题(或问"值得买吗"、"在线模式怎么样")
- 系统从该游戏的 Steam 评论里检索相关内容
- LLM 综合生成回答,标注 `[1][2]` 引用编号、情感倾向(positive / mixed / negative)、置信度
- 让用户能用自然语言问 Steam 游戏评论,系统从评论里找答案,给出带引用和情感标签的回答。




[//]: # (![demo]&#40;docs/demo.gif&#41;)

---

## 核心数字(50 题 ground truth)

| 模式 | Sentiment Acc | Keyword Hit | Off-topic Rec | p95 |
|---|---|---|---|---|
| 单轮 RAG | 58% | 45% | 20% | 2.6s |
| ReAct Agent | 68% | 75% | **100%** | 4.6s |
| + Reflection | **74%** | **76%** | 100% | 8.7s |

详见 [`logs/eval_v5_final.md`](logs/eval_v5_final.md)。

---

## 技术栈

- **后端**:Python 3.14 · Flask 3 · scikit-learn · pandas
- **LLM**:DeepSeek API(OpenAI 兼容协议)
- **检索**:TF-IDF(1-2gram,50000 词,余弦相似度)
- **测试**:pytest(65 用例,含真 LLM 集成)
- **前端**:原生 HTML/CSS/JS

---

## 30 秒上手

```bash
pip install -r requirements.txt
cp .env.example .env            # 填 DEEPSEEK_API_KEY
python scripts/sample_reviews.py    # 抽样数据到 data/processed/
python app.py                      # 起服务
# 浏览器打开 http://localhost:5000
```

无 key 也能起,前端会显示 `key missing`,接口 503 兜底。

跑测试:`python -m pytest tests/ -v`  
跑评估:`python scripts/eval.py --modes agent`

---

## 功能

**1. 多轮 ReAct Agent**  
用户问"这游戏值得买吗?剧情如何?",LLM 自动拆成"value for money"和"story plot quality"两个子问题,各自检索评论再综合。比单轮检索关键词覆盖率高 30%。

**2. Reflection 自检追加检索**  
LLM 答完后自检"是否漏了维度",不够就追加检索再综合。sentiment 准确率从 68% 提到 74%,代价 4 秒。

**3. 鲁棒性兜底**  
用户问候 / 辱骂 / 问无关问题,都能识别并友好回应;LLM 调用失败、JSON 解析失败、类型异常等 7 层兜底,前端永远不会看到崩溃。

**4. 缓存降本**  
LRU + TTL 查询缓存,sha256(key) 直接命中,响应 < 100ms。

**5. 量化评估**  
50 条人工 QA 作为 ground truth,跑三种模式出对比报告,改 prompt 时直接跑回归,数字说话不是凭感觉。

**6. 工程化**  
65 个 pytest 用例(单元 + Flask 端到端);4 个游戏;所有错误路径都有兜底。

---

## 工程决策

**TF-IDF 而非 embedding**:短文本场景 TF-IDF 不输 BGE 等 embedding 模型,且无需下载 ~400MB 模型、启动 <1s。如果未来要换,只需新写一个 `BgeRetriever` 实现同接口。

**ReAct 自实现而非 LangChain**:LangChain 抽象层 debug 难度高,自实现 ReAct(plan → 多检索 → synthesize)约 100 行,够 demo。

---

## 真实踩过的坑

1. **`threading.Lock` 死锁** — `get_retriever` 持锁后调 `ensure_loaded`,后者又抢同一锁,死锁。改 `RLock`(可重入锁)即可。
2. **Werkzeug 3.1.8 + Python 3.14 上 `request.get_json()` 偶发失败** — 手动 `json.loads` 兜底。
3. **PowerShell 5.1 把 `{...}` 当 hashtable 解析** — curl 调试时 JSON 引号被吃掉,改用文件传 body。
4. **Flask 500 默认返回 HTML** — 前端 `resp.json()` 解析失败报 `SyntaxError: Unexpected token '<'`,7 层兜底 + 前端明确报错修复。

---

## 目录

```
app.py                    Flask 入口(/ /games /ask /health /cache/stats)
rag/
  agent.py                ReAct Agent + Reflection + 全链路兜底
  retriever.py            TF-IDF 检索
  llm.py                  DeepSeek / OpenAI 双 provider
  cache.py                LRU + TTL 查询缓存
  registry.py             游戏注册表
  config.py               集中配置
  prompt.py               Prompt 模板
templates/index.html      单页前端
scripts/
  eval.py                 量化评估(读 qa.jsonl + 三模式对比 + Markdown 报告)
  sample_reviews.py       数据抽样
  start_flask.py          pytest 启服务用
tests/                    65 个 pytest 用例
data/eval/qa.jsonl        50 条人工 QA
docs/                     架构与 Prompt 设计
```

---

## 详细文档

- [架构](docs/ARCHITECTURE.md) — 数据流图 + 设计权衡
- [Prompt 设计](docs/PROMPT.md) — 5 条硬规则 + 多轮 plan/synthesis/reflect

---

## 数据来源

基于 Kaggle 公开 Steam Reviews 数据集(约 99 万条评论),本项目抽样 3 个游戏的英文评论共 ~9000 条用于检索。