import numpy as np
from rank_bm25 import BM25Okapi

class BM25Index:
    def __init__(self, documents):
        self.docs = [d.lower().split() for d in documents]
        self.bm25 = BM25Okapi(self.docs)

    def search(self, query, k=100):
        scores = self.bm25.get_scores(query.lower().split())
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return ranked[:k]
