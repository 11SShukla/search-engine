from evaluator import ndcg_at_k, mrr

# Relevance labels: clicked=1, not=0
rels = [1, 0, 0, 1, 0]

print("NDCG@3:", ndcg_at_k(rels, 3))
print("MRR:", mrr(rels))
