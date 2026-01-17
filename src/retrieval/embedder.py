from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class Embedder:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        return self.model.encode(text, normalize_embeddings=True)
