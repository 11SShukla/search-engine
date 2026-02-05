import sqlite3, json, random, time
from search_engine import search

queries = json.load(open("data/queries.json"))

conn = sqlite3.connect("data/clicks.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS clicks")
cur.execute("""
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    query TEXT,
    item_id INTEGER,
    position INTEGER,
    ts INTEGER
)
""")

def click_prob(pos):
    return 1 / (pos + 1)  # position bias

for q in queries[:20000]:  # simulate subset
    results = search(q)
    user = f"user_{random.randint(1,1000)}"

    for pos, (item, _) in enumerate(results):
        if random.random() < click_prob(pos) * random.uniform(0.7, 1.2):
            cur.execute(
                "INSERT INTO clicks VALUES (NULL,?,?,?,?,?)",
                (user, q, item["id"], pos, int(time.time()))
            )

conn.commit()
conn.close()
print(" Click simulation done")
