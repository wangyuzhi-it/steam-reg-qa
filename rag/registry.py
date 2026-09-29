"""游戏注册表:从 data/processed/games.json 加载,缓存 retriever 实例。"""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from pathlib import Path

from .config import DATA_PROCESSED
from .retriever import TfIdfRetriever

MANIFEST = DATA_PROCESSED / "games.json"


@dataclass
class GameEntry:
    name: str
    csv_path: Path
    n_rows: int = 0


_lock = threading.RLock()  # 必须可重入:get_retriever 持锁后调 ensure_loaded
_entries: dict[str, GameEntry] = {}
_retrievers: dict[str, TfIdfRetriever] = {}
_loaded: bool = False


def _load_manifest() -> None:
    _entries.clear()
    if not MANIFEST.exists():
        return
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for item in manifest:
        csv = DATA_PROCESSED / item["csv"]
        if not csv.exists():
            continue
        try:
            import pandas as pd
            n = 0
            for chunk in pd.read_csv(csv, usecols=["review"], chunksize=5000):
                n += len(chunk)
        except Exception:
            n = 0
        _entries[item["name"]] = GameEntry(name=item["name"], csv_path=csv, n_rows=n)


def ensure_loaded() -> None:
    global _loaded
    with _lock:
        if _loaded:
            return
        _load_manifest()
        _loaded = True


def reload() -> None:
    """强制重载 manifest,用于 sample_reviews.py 跑完后刷新。"""
    global _loaded
    with _lock:
        _load_manifest()
        _loaded = True
    _retrievers.clear()


def get_entry(name: str) -> GameEntry:
    ensure_loaded()
    if name not in _entries:
        raise KeyError(f"game not found: {name}; available: {list(_entries)}")
    return _entries[name]


def get_retriever(name: str) -> TfIdfRetriever:
    ensure_loaded()
    with _lock:
        if name not in _retrievers:
            entry = get_entry(name)
            _retrievers[name] = TfIdfRetriever(entry.csv_path)
    return _retrievers[name]


def list_games() -> list[GameEntry]:
    ensure_loaded()
    return list(_entries.values())