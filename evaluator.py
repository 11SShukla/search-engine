import math

def ndcg_at_k(rels, k):
    dcg = sum((2**rel - 1) / math.log2(i+2) for i, rel in enumerate(rels[:k]))
    ideal = sorted(rels, reverse=True)
    idcg = sum((2**rel - 1) / math.log2(i+2) for i, rel in enumerate(ideal[:k]))
    return dcg / idcg if idcg else 0

def mrr(rels):
    for i, r in enumerate(rels):
        if r:
            return 1 / (i+1)
    return 0
