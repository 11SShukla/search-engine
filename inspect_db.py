import sqlite3

conn = sqlite3.connect("data/items.db")
cur = conn.cursor()

print("Tables:")
print(cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())

print("\nSample rows:")
rows = cur.execute("SELECT * FROM items LIMIT 5").fetchall()
for r in rows:
    print(r)

print("\nTotal items:")
print(cur.execute("SELECT COUNT(*) FROM items").fetchone())

conn.close()
