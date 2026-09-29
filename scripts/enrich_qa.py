"""给 qa.jsonl 的 expect_keywords 批量加中文同义词,用 | 分隔。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "eval" / "qa.jsonl"
OUT = SRC  # 原地改

# 关键词中文同义词词典(精简,够 demo 用)
SYNONYMS = {
    # 通用
    "worth": "值得", "buy": "购买", "money": "金钱",
    "boss": "boss", "fight": "战斗", "design": "设计",
    "combat": "战斗", "story": "故事", "chapter": "章节",
    "chinese": "中国",
    "optimization": "优化", "performance": "性能", "fps": "帧率",
    "difficult": "难", "hard": "难", "souls": "魂",
    "bugs": "bug", "crash": "崩溃", "glitches": "bug",
    "hours": "小时", "length": "时长",
    "graphics": "画面", "visuals": "画面", "beautiful": "美",
    "price": "价格", "value": "价值",
    "world": "世界", "exploration": "探索", "open": "开放",
    "casual": "休闲",
    "multiplayer": "联机", "coop": "合作", "online": "在线",
    "lore": "背景", "dark": "黑暗",
    "stutter": "卡顿",
    "finish": "通关",
    "magic": "魔法", "sorcery": "魔法", "build": "build",
    "newcomers": "新手", "friendly": "友好",
    "arthur": "亚瑟", "emotional": "感人",
    "horse": "马", "riding": "骑行", "control": "操控",
    "microtransactions": "氪金", "grind": "刷", "shark": "鲨鱼",
    "shooting": "射击", "gun": "枪", "dead": "死",
    "character": "角色", "gang": "帮派", "rockstar": "r星",
    "music": "音乐", "soundtrack": "配乐",
    "violence": "暴力", "content": "内容",
    "tip": "建议", "beginner": "新手", "advice": "建议",
    "compared": "对比", "previous": "前作",
    "server": "服务器", "active": "活跃",
    "dlc": "dlc",
    "pc": "pc", "deck": "deck",
}

def expand(kw: str) -> str:
    base = kw.strip()
    if "|" in base:
        return base
    zh = SYNONYMS.get(base.lower())
    if zh and zh.lower() != base.lower():
        return f"{base}|{zh}"
    return base

count = 0
lines = []
with SRC.open(encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            lines.append(line)
            continue
        q = json.loads(line)
        old = q["expect_keywords"]
        new = [expand(k) for k in old]
        if new != old:
            q["expect_keywords"] = new
            count += 1
        lines.append(json.dumps(q, ensure_ascii=False))

with OUT.open("w", encoding="utf-8") as f:
    for line in lines:
        if line:
            f.write(line + "\n")
print(f"updated {count} entries with zh synonyms")