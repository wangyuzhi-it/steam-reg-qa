"""Flask 入口:Steam 评论 RAG 问答(多游戏 + ReAct Agent)。"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from rag import config, registry
from rag.agent import ReActAgent, single_shot
from rag.cache import ResponseCache
from rag.llm import LLMClient, LLMError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(config.LOG_DIR / "app.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("app")

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

llm = LLMClient(provider=os.getenv("LLM_PROVIDER", config.LLM_PROVIDER))
_agents: dict[str, ReActAgent] = {}
cache = ResponseCache(max_size=int(os.getenv("CACHE_MAX_SIZE", "1000")),
                      ttl_sec=int(os.getenv("CACHE_TTL_SEC", "3600")))


def get_agent(game: str) -> ReActAgent:
    if game not in _agents:
        retr = registry.get_retriever(game)
        _agents[game] = ReActAgent(llm=llm, retriever=retr, game=game)
    return _agents[game]


@app.errorhandler(Exception)
def _handle_unexpected(e):
    """任何未捕获异常都返回 JSON,绝不返回 HTML。"""
    if isinstance(e, LLMError):
        log.warning("llm error: %s", e)
        return jsonify({"error": f"llm error: {e}"}), 502
    log.exception("unexpected error")
    return jsonify({
        "error": f"server error: {type(e).__name__}: {str(e)[:200]}"
    }), 500


@app.get("/")
def index():
    games = registry.list_games()
    return render_template(
        "index.html",
        games=[g.name for g in games],
        default_game=config.DEFAULT_GAME,
        llm_ready=llm.ready,
        provider=llm.provider,
    )


@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "llm_ready": llm.ready,
        "provider": llm.provider,
        "model": llm.model,
        "games": [g.name for g in registry.list_games()],
    })


@app.get("/games")
def games():
    return jsonify({
        "games": [
            {"name": g.name, "n_rows": g.n_rows, "csv": g.csv_path.name}
            for g in registry.list_games()
        ]
    })


@app.get("/cache/stats")
def cache_stats():
    return jsonify(cache.stats())


@app.post("/cache/clear")
def cache_clear():
    cache.clear()
    return jsonify({"ok": True, **cache.stats()})


@app.post("/ask")
def ask():
    # 1) 解析 JSON  —— Werkzeug 3.1.8 + Py3.14 上 get_json 偶发失败,手动解析
    try:
        raw = request.get_data(cache=False)
        payload = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return jsonify({"error": "invalid json body"}), 400
    except Exception as e:
        log.exception("read body failed")
        return jsonify({"error": f"read body failed: {type(e).__name__}"}), 400
    if not isinstance(payload, dict):
        return jsonify({"error": "json body must be an object"}), 400

    # 2) 取参 + 校验
    question = (payload.get("question") or "").strip()
    game = (payload.get("game") or config.DEFAULT_GAME).strip()
    try:
        top_k = int(payload.get("top_k", config.DEFAULT_TOP_K))
    except (TypeError, ValueError):
        return jsonify({"error": "top_k must be an integer"}), 400
    top_k = max(1, min(top_k, config.MAX_TOP_K))
    use_agent = bool(payload.get("agent", True))
    use_reflect = bool(payload.get("reflect", False))

    if not question:
        return jsonify({"error": "question is required"}), 400
    if len(question) > 1000:
        return jsonify({"error": "question too long (max 1000 chars)"}), 400
    if not llm.ready:
        return jsonify({"error": "LLM api key missing, see README"}), 503

    # 3) 取 agent + 路由
    try:
        agent = get_agent(game)
    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        log.exception("get_agent failed")
        return jsonify({"error": f"failed to load retriever: {type(e).__name__}"}), 500

    # 4) 跑 Agent / single_shot,任何异常都被上面 errorhandler 兜住

    # cache key 必须包含影响输出的所有参数
    cache_key = ResponseCache.make_key({
        "game": game, "question": question, "top_k": top_k,
        "agent": use_agent, "reflect": use_reflect,
    })
    cached = cache.get(cache_key)
    if cached is not None:
        cached["cached"] = True
        cached["cache_stats"] = cache.stats()
        return jsonify(cached)

    if use_agent:
        try:
            result = agent.run(question, top_k=top_k, reflect=use_reflect)
            response = {
                "mode": "agent",
                "game": game,
                "question": question,
                "sub_questions": result.sub_questions,
                "steps": result.to_dict()["steps"],
                "answer": result.final,
                "reflect": use_reflect,
            }
        except Exception as e:
            log.exception("agent.run raised")
            return jsonify({
                "error": f"agent failed: {type(e).__name__}: {str(e)[:200]}"
            }), 500
    else:
        try:
            hits = agent.retriever.search(question, top_k=top_k)
        except Exception as e:
            log.exception("retriever.search failed")
            return jsonify({
                "error": f"retriever failed: {type(e).__name__}"
            }), 500
        if not hits:
            return jsonify({"error": "no review matched, try another question"}), 404
        parsed = single_shot(llm, agent.retriever, game, question, top_k)
        response = {
            "mode": "single_shot",
            "game": game,
            "question": question,
            "hits": [h.to_dict() for h in hits],
            "answer": parsed,
            "reflect": False,
        }

    response["cached"] = False
    response["cache_stats"] = cache.stats()
    cache.set(cache_key, dict(response))
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)