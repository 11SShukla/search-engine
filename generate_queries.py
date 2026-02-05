import random, json

terms = ["iphone", "shoes", "laptop", "tv", "jacket", "running"]
queries = []

for _ in range(100000):
    q = random.choice(terms)
    queries.append(q)

json.dump(queries, open("data/queries.json", "w"))
print("✅ 100k queries generated")
