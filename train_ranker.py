import sqlite3
import pickle
import os
import random
from sklearn.linear_model import LogisticRegression
from feature_builder import build_features

# -----------------------------
# Load items
# -----------------------------
conn = sqlite3.connect("data/items.db")
items = {r[0]: r for r in conn.execute("SELECT * FROM items")}
conn.close()

item_ids = list(items.keys())

# -----------------------------
# Load clicks (positives)
# -----------------------------
conn = sqlite3.connect("data/clicks.db")
clicks = conn.execute(
    "SELECT query, item_id FROM clicks"
).fetchall()
conn.close()

X, y = [], []

# -----------------------------
# Build training data
# -----------------------------
for query, clicked_item_id in clicks:
    clicked_item = {
        "id": clicked_item_id,
        "title": items[clicked_item_id][1],
        "description": items[clicked_item_id][2],
        "category": items[clicked_item_id][3],
        "brand": items[clicked_item_id][4],
        "price": items[clicked_item_id][5],
    }

    # ✅ POSITIVE SAMPLE
    X.append(
        build_features(
            query=query,
            item=clicked_item,
            retrieval_score=1.0,
            clicks=1
        )
    )
    y.append(1)

    # ❌ NEGATIVE SAMPLE (random non-clicked item)
    neg_item_id = random.choice(item_ids)
    if neg_item_id == clicked_item_id:
        continue

    neg_item = {
        "id": neg_item_id,
        "title": items[neg_item_id][1],
        "description": items[neg_item_id][2],
        "category": items[neg_item_id][3],
        "brand": items[neg_item_id][4],
        "price": items[neg_item_id][5],
    }

    X.append(
        build_features(
            query=query,
            item=neg_item,
            retrieval_score=0.2,
            clicks=0
        )
    )
    y.append(0)

# -----------------------------
# Train model
# -----------------------------
model = LogisticRegression(max_iter=300)
model.fit(X, y)

# -----------------------------
# Save model
# -----------------------------
os.makedirs("models", exist_ok=True)
pickle.dump(model, open("models/ranker.pkl", "wb"))

print("✅ Ranker trained with positive + negative samples")
