"""RAG 检索:TF-IDF + cosine,返回 top-k 评论。"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

log = logging.getLogger(__name__)


@dataclass
class Hit:
    index: int
    review: str
    hours_played: float
    helpful: str
    recommendation: str
    score: float

    def to_dict(self) -> dict:
        return asdict(self)


class TfIdfRetriever:
    def __init__(self, csv_path: Path):
        csv_path = Path(csv_path)
        df = pd.read_csv(csv_path).fillna(
            {"review": "", "helpful": "0", "recommendation": "Unknown"}
        )
        df["review"] = df["review"].astype(str)
        self.df = df.reset_index(drop=True)
        self.source = csv_path
        log.info("building tfidf index for %s (%d docs)", csv_path.name, len(df))
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=50_000,
            sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform(self.df["review"].tolist())
        log.info("tfidf ready: vocab=%d, matrix=%s", len(self.vectorizer.vocabulary_), self.matrix.shape)

    def search(self, query: str, top_k: int = 5) -> list[Hit]:
        if not query.strip():
            return []
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix).ravel()
        order = sims.argsort()[::-1][:top_k]
        hits: list[Hit] = []
        for idx in order:
            row = self.df.iloc[idx]
            hits.append(
                Hit(
                    index=int(idx),
                    review=str(row["review"])[:400],
                    hours_played=float(row.get("hours_played", 0) or 0),
                    helpful=str(row.get("helpful", "0")),
                    recommendation=str(row.get("recommendation", "Unknown")),
                    score=float(sims[idx]),
                )
            )
        return hits

    @property
    def size(self) -> int:
        return len(self.df)


if __name__ == "__main__":
    import sys

    csv = Path(__file__).resolve().parent.parent / "data" / "processed" / "reviews_sample.csv"
    retr = TfIdfRetriever(csv)
    q = " ".join(sys.argv[1:]) or "is the game worth buying?"
    for h in retr.search(q, top_k=3):
        print(f"[{h.score:.3f}] ({h.recommendation}) {h.review[:120]}...")