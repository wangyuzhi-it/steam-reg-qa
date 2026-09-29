"""pytest:Flask 端到端测试。

跑一个真 Flask server(子进程),用 requests 调接口。
"""
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="module")
def server():
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")

    port = _free_port()
    env = {**os.environ, "PYTHONUNBUFFERED": "1"}
    proc = subprocess.Popen(
        [sys.executable, "scripts/start_flask.py", str(port)],
        env=env, cwd=str(ROOT),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    base = f"http://127.0.0.1:{port}"
    # 等服务起来
    for _ in range(40):
        try:
            requests.get(f"{base}/health", timeout=2)
            break
        except Exception:
            time.sleep(0.25)
    else:
        proc.terminate()
        raise RuntimeError("flask didn't start")

    yield {"base": base, "proc": proc, "has_key": bool(os.getenv("DEEPSEEK_API_KEY"))}

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def test_health(server):
    r = requests.get(f"{server['base']}/health", timeout=10)
    assert r.status_code == 200
    d = r.json()
    assert d["ok"] is True
    assert "Black Myth: Wukong" in d["games"]


def test_games(server):
    r = requests.get(f"{server['base']}/games", timeout=10)
    assert r.status_code == 200
    names = [g["name"] for g in r.json()["games"]]
    assert "ELDEN RING" in names


def test_index_html(server):
    r = requests.get(f"{server['base']}/", timeout=10)
    assert r.status_code == 200
    assert "Steam" in r.text and "RAG" in r.text


def test_ask_no_key(server):
    """无 key 时应该 503。"""
    if server["has_key"]:
        pytest.skip("DEEPSEEK_API_KEY 已配置,跳过无 key 分支")
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "worth?", "game": "Black Myth: Wukong", "top_k": 3},
        timeout=15,
    )
    assert r.status_code == 503
    assert "missing" in r.text


def test_ask_bad_json(server):
    r = requests.post(
        f"{server['base']}/ask",
        data=b"not json",
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    assert r.status_code == 400


def test_ask_unknown_game(server):
    if not server["has_key"]:
        pytest.skip("no key")
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "x", "game": "NoSuchGame", "top_k": 2},
        timeout=30,
    )
    assert r.status_code == 404


def test_ask_single_shot(server):
    if not server["has_key"]:
        pytest.skip("no key")
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "worth buying?", "game": "Black Myth: Wukong",
              "top_k": 3, "agent": False},
        timeout=90,
    )
    assert r.status_code == 200, r.text[:300]
    d = r.json()
    assert d["mode"] == "single_shot"
    assert "answer" in d
    assert d["answer"]["answer"]


def test_ask_agent(server):
    if not server["has_key"]:
        pytest.skip("no key")
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "worth buying and is it well optimized?",
              "game": "Black Myth: Wukong", "top_k": 3, "agent": True},
        timeout=120,
    )
    assert r.status_code == 200, r.text[:300]
    d = r.json()
    assert d["mode"] == "agent"
    assert 1 <= len(d["sub_questions"]) <= 3
    assert d["answer"]["answer"]


def test_ask_offtopic_returns_clean_json(server):
    """非游戏问题必须返回 200 + off-topic JSON,绝不返回 HTML。"""
    if not server["has_key"]:
        pytest.skip("no key")
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "你是来拉屎的吧", "game": "Black Myth: Wukong",
              "top_k": 3, "agent": True},
        timeout=90,
    )
    assert r.status_code == 200, r.text[:300]
    assert r.headers.get("Content-Type", "").startswith("application/json")
    d = r.json()
    # plan 应识别为无关 → sub_questions 空
    assert d["sub_questions"] == []
    assert "无关" in d["answer"]["answer"]


def test_ask_empty_question_400(server):
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "", "game": "Black Myth: Wukong"},
        timeout=10,
    )
    assert r.status_code == 400
    j = r.json()
    assert "required" in j["error"].lower()


def test_ask_long_question_400(server):
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "x" * 1500, "game": "Black Myth: Wukong"},
        timeout=10,
    )
    assert r.status_code == 400


def test_ask_top_k_invalid_400(server):
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "x", "game": "Black Myth: Wukong", "top_k": "abc"},
        timeout=10,
    )
    assert r.status_code == 400


def test_ask_garbage_question_agent(server):
    """乱问(问候、辱骂)走 Agent 也必须返回 JSON,绝不返回 HTML。"""
    if not server["has_key"]:
        pytest.skip("no key")
    for q in ["好好好", "是谁", "你好", "fuck you"]:
        r = requests.post(
            f"{server['base']}/ask",
            json={"question": q, "game": "Black Myth: Wukong",
                  "top_k": 3, "agent": True},
            timeout=90,
        )
        assert r.status_code == 200, f"q={q!r} got {r.status_code}: {r.text[:200]}"
        assert r.headers.get("Content-Type", "").startswith("application/json")
        d = r.json()
        # 要么 sub_questions 空(off-topic),要么正常问答;但 final 一定有
        assert "answer" in d
        assert isinstance(d.get("sub_questions"), list)


def test_cache_hit_on_second_call(server):
    """相同请求第二次必须命中缓存(返回 cached=True)。"""
    if not server["has_key"]:
        pytest.skip("no key")
    payload = {
        "question": "is worth buying?", "game": "Black Myth: Wukong",
        "top_k": 3, "agent": False,
    }
    r1 = requests.post(f"{server['base']}/ask", json=payload, timeout=90)
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["cached"] is False

    r2 = requests.post(f"{server['base']}/ask", json=payload, timeout=15)
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["cached"] is True
    # 同一 question 命中,内容应一致(子结构相同)
    assert d2["answer"]["answer"] == d1["answer"]["answer"]


def test_cache_different_params_different_key(server):
    """reflect 参数不同 → cache key 不同 → 第二次不命中。"""
    if not server["has_key"]:
        pytest.skip("no key")
    p1 = {"question": "is worth?", "game": "Black Myth: Wukong",
          "top_k": 3, "agent": False, "reflect": False}
    p2 = dict(p1, reflect=True)
    r1 = requests.post(f"{server['base']}/ask", json=p1, timeout=90)
    assert r1.json()["cached"] is False
    r2 = requests.post(f"{server['base']}/ask", json=p2, timeout=120)
    assert r2.json()["cached"] is False


def test_cache_stats_endpoint(server):
    r = requests.get(f"{server['base']}/cache/stats", timeout=10)
    assert r.status_code == 200
    d = r.json()
    for k in ("hits", "misses", "size", "max_size", "ttl_sec", "hit_rate"):
        assert k in d


def test_cache_clear(server):
    r = requests.post(f"{server['base']}/cache/clear", timeout=10)
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_ask_with_reflect(server):
    """reflect=True 端到端可调通。"""
    if not server["has_key"]:
        pytest.skip("no key")
    r = requests.post(
        f"{server['base']}/ask",
        json={"question": "worth buying and how is the story?",
              "game": "Black Myth: Wukong", "top_k": 3, "agent": True,
              "reflect": True},
        timeout=180,
    )
    assert r.status_code == 200, r.text[:300]
    d = r.json()
    assert d["reflect"] is True
    assert d["answer"]["answer"]