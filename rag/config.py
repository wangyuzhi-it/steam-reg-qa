"""集中配置:路径、常量、默认参数。"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

DEFAULT_GAME = "Black Myth: Wukong"
SUPPORTED_GAMES: list[str] = [DEFAULT_GAME]
"""启动时由 registry 扫描 data/processed/ 自动扩展。"""

DEFAULT_TOP_K = 5
MAX_TOP_K = 10
AGENT_MAX_SUBQS = 3

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")
LLM_TEMPERATURE = 0.3
LLM_TIMEOUT = 60
LLM_MAX_RETRIES = 2