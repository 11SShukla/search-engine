import math

def build_features(query, item, retrieval_score, clicks):
    """
    Feature vector:
    1. Retrieval score (BM25)
    2. Click count
    3. Price
    4. Query length
    5. Description length
    """

    return [
        retrieval_score,
        clicks,
        item["price"],
        len(query.split()),
        len(item["description"].split())
    ]

