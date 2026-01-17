from sentence_transformers import CrossEncoder

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

class Reranker:
    def __init__(self):
        self.model = CrossEncoder(RERANK_MODEL)

    def rerank(self, query: str, results: list, top_k=5):
        pairs = [(query, r["content"]) for r in results]
        scores = self.model.predict(pairs)

        for r, s in zip(results, scores):
            r["rerank_score"] = float(s)

        results = sorted(results, key=lambda x: x["rerank_score"], reverse=True)
        return results[:top_k]
