import sqlite3, pickle
from bm25_index import BM25Index
from feature_builder import build_features

conn = sqlite3.connect("data/items.db")
rows = conn.execute("SELECT * FROM items").fetchall()
conn.close()

items, corpus = [], []
for r in rows:
    item = {
        "id": r[0],
        "title": r[1],
        "description": r[2],
        "category": r[3],
        "brand": r[4],
        "price": r[5],
    }
    items.append(item)
    corpus.append(item["title"] + " " + item["description"])

bm25 = BM25Index(corpus)

try:
    ranker = pickle.load(open("models/ranker.pkl", "rb"))
except:
    ranker = None

def search(query):
    candidates = bm25.search(query)
    results = []

    for pos, (idx, score) in enumerate(candidates):
        item = items[idx]
        if ranker:
            feats = build_features(query, item, score, 1)
            score = ranker.predict_proba([feats])[0][1]
        results.append((item, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:20]
