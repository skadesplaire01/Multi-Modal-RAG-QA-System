import os
import pickle
import numpy as np
import faiss

class VectorStore:
    def __init__(self, store_dir="vector_store"):
        self.store_dir = store_dir
        os.makedirs(self.store_dir, exist_ok=True)

        self.index_path = os.path.join(self.store_dir, "faiss.index")
        self.meta_path = os.path.join(self.store_dir, "chunks.pkl")

        self.index = None
        self.chunks = None

    def build(self, embeddings: np.ndarray, chunks: list):
        embeddings = embeddings.astype("float32")
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dim)  # cosine-like if embeddings are normalized
        self.index.add(embeddings)

        self.chunks = chunks

        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, "rb") as f:
            self.chunks = pickle.load(f)
        return self.index, self.chunks

    def exists(self):
        return os.path.exists(self.index_path) and os.path.exists(self.meta_path)
