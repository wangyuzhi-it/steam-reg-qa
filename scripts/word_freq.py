import sys, re
from collections import Counter
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

STOP = set("""
the a an and or but if is are was were be been being have has had do does did
will would shall should can could may might must this that these those it its they
them their there here how what why when where who which not no so as to of in on
at for with from by about into through during before after above below between
out up down off over under again further then once very just also too only own
same than such don doesn didn hasn haven isn mustn need shouldn wasn weren weren
won wouldn game games play playing played really great good nice love like best
ever time times
""".split())

GAMES = ["Black Myth: Wukong", "ELDEN RING", "Red Dead Redemption 2"]
GAME_SLUG = {g: g.replace(":", "").replace(" ", "_").lower() for g in GAMES}

print(f"{'GAME':30s}  N   POS%  top 15 words (n>=20)")
for g in GAMES:
    csv = ROOT / "data" / "processed" / f"reviews_{GAME_SLUG[g]}.csv"
    df = pd.read_csv(csv, usecols=["review", "recommendation"])
    n = len(df)
    pos = (df["recommendation"] == "Recommended").sum()
    cnt = Counter()
    for r in df["review"].dropna().astype(str):
        for w in re.findall(r"[a-z]+", r.lower()):
            if len(w) >= 4 and w not in STOP:
                cnt[w] += 1
    print(f"\n=== {g} (n={n}, pos={pos*100//n}%) ===")
    for w, c in cnt.most_common(20):
        if c >= 20:
            print(f"   {c:>5}  {w}")