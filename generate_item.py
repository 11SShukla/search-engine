import sqlite3, random

categories = ["electronics", "fashion", "home", "sports"]
brands = ["sony", "nike", "apple", "samsung", "adidas"]

conn = sqlite3.connect("data/items.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS items")
cur.execute("""
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    category TEXT,
    brand TEXT,
    price REAL
)
""")

for i in range(50000):
    cat = random.choice(categories)
    brand = random.choice(brands)
    title = f"{brand} {cat} product {i}"
    desc = f"high quality {cat} item from {brand}"
    price = round(random.uniform(10, 2000), 2)

    cur.execute(
        "INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)",
        (i, title, desc, cat, brand, price)
    )

conn.commit()
conn.close()
print(" 50k items generated")
