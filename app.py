from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3, time
from search_engine import search

app = FastAPI()

# ---------- SCHEMAS ----------

class BulkItem(BaseModel):
    id: int
    title: str
    description: str
    category: str
    brand: str
    price: float

class ClickEvent(BaseModel):
    user_id: str
    query: str
    item_id: int
    position: int
    ts: int | None = None

# ---------- INDEXING ----------

@app.post("/items/bulk")
def bulk_insert(items: list[BulkItem]):
    conn = sqlite3.connect("data/items.db")
    cur = conn.cursor()

    for item in items:
        cur.execute(
            "INSERT OR REPLACE INTO items VALUES (?,?,?,?,?,?)",
            (
                item.id,
                item.title,
                item.description,
                item.category,
                item.brand,
                item.price,
            ),
        )

    conn.commit()
    conn.close()
    return {"inserted": len(items)}

@app.post("/reindex")
def reindex():
    from importlib import reload
    import search_engine
    reload(search_engine)
    return {"status": "reindexed"}

# ---------- SEARCH ----------

@app.get("/search")
def search_api(q: str, k: int = 20, user_id: str | None = None):
    results = search(q)
    response = []

    for item, score in results[:k]:
        response.append({
            "id": item["id"],
            "score": score,
        })

    return {"items": response}

# ---------- FEEDBACK ----------

@app.post("/feedback/click")
def log_click(event: ClickEvent):
    conn = sqlite3.connect("data/clicks.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO clicks VALUES (NULL,?,?,?,?,?)",
        (
            event.user_id,
            event.query,
            event.item_id,
            event.position,
            event.ts or int(time.time()),
        ),
    )

    conn.commit()
    conn.close()
    return {"status": "logged"}

# ---------- METRICS ----------

@app.get("/top_queries")
def top_queries(window: int = 300):
    since = int(time.time()) - window
    conn = sqlite3.connect("data/clicks.db")
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT query, COUNT(*) as c
        FROM clicks
        WHERE ts >= ?
        GROUP BY query
        ORDER BY c DESC
        LIMIT 10
        """,
        (since,),
    ).fetchall()

    conn.close()
    return {"top_queries": rows}
