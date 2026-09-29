"""从 steam_game_reviews.csv 抽多个游戏的英文评论,产出 demo 数据集。

每个游戏一个文件:data/processed/reviews_<safe_name>.csv

用法:
  python scripts/sample_reviews.py                # 用默认游戏列表
  python scripts/sample_reviews.py "Game A" "Game B"
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "steam_game_reviews.csv"
OUT_DIR = ROOT / "data" / "processed"
CHUNKSIZE = 10_000
MAX_ROWS_PER_GAME = 6000
MIN_SEG_LEN = 30

DEFAULT_GAMES = ["Black Myth: Wukong", "ELDEN RING", "Red Dead Redemption 2"]

REGISTRY_JSON = OUT_DIR / "games.json"


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()


def split_segments(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return [p.strip() for p in re.split(r"-{5,}", text) if p.strip()]


def sample_one(game: str) -> Path:
    safe = safe_name(game)
    out = OUT_DIR / f"reviews_{safe}.csv"
    kept: list[dict] = []
    for chunk in pd.read_csv(
        SRC,
        usecols=["review", "hours_played", "helpful", "funny",
                 "recommendation", "date", "game_name", "username"],
        chunksize=CHUNKSIZE,
        dtype={"helpful": str, "funny": str},
    ):
        sub = chunk[chunk["game_name"] == game]
        for _, row in sub.iterrows():
            for seg in split_segments(row["review"]):
                if len(seg) < MIN_SEG_LEN:
                    continue
                kept.append(
                    {
                        "review": seg,
                        "hours_played": row["hours_played"],
                        "helpful": row["helpful"],
                        "funny": row["funny"],
                        "recommendation": row["recommendation"],
                        "date": row["date"],
                        "username": row["username"],
                    }
                )
                if len(kept) >= MAX_ROWS_PER_GAME:
                    break
            if len(kept) >= MAX_ROWS_PER_GAME:
                break
        if len(kept) >= MAX_ROWS_PER_GAME:
            break
    df = pd.DataFrame(kept)
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"[OK] {game}: {len(df)} rows -> {out.name}")
    return out


def main() -> int:
    if not SRC.exists():
        print(f"[ERR] missing source: {SRC}", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    games = sys.argv[1:] or DEFAULT_GAMES
    manifest: list[dict] = []
    for g in games:
        try:
            out = sample_one(g)
            manifest.append({"name": g, "csv": out.name, "safe_name": safe_name(g)})
        except Exception as e:
            print(f"[FAIL] {g}: {e}", file=sys.stderr)
    REGISTRY_JSON.write_text(
        __import__("json").dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] wrote manifest -> {REGISTRY_JSON.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())