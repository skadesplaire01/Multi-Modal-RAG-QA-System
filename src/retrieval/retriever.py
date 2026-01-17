import numpy as np
from src.retrieval.embedder import Embedder
from src.retrieval.vector_store import VectorStore

class Retriever:
    def __init__(self, store_dir="vector_store"):
        self.embedder = Embedder()
        self.vs = VectorStore(store_dir=store_dir)
        self.index, self.chunks = self.vs.load()

    def search(self, query: str, top_k=7):
        q_emb = self.embedder.embed(query).astype("float32")
        q_emb = np.expand_dims(q_emb, axis=0)

        scores, idxs = self.index.search(q_emb, top_k)

        results = []
        for score, idx in zip(scores[0], idxs[0]):
            c = self.chunks[int(idx)]
            results.append({
                "score": float(score),
                "content": c["content"],
                "page": c["page"],
                "type": c["type"],
                "source": c["source"],
                "chunk_id": c["chunk_id"]
            })

        return results
