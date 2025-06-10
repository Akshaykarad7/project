from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

# class VectorStore:
#     def __init__(self, model_name="all-MiniLM-L6-v2"):
#         self.model = SentenceTransformer(model_name)
#         self.index = None
#         self.text_chunks = []

#     def build_index(self, chunks):
#         self.text_chunks = chunks
#         embeddings = self.model.encode(chunks, show_progress_bar=True)
#         self.index = faiss.IndexFlatL2(embeddings.shape[1])
#         self.index.add(np.array(embeddings))

#     def search(self, query: str, top_k: int = 8):
#         query_embedding = self.model.encode([query])
#         distances, indices = self.index.search(np.array(query_embedding), top_k)
#         return [self.text_chunks[i] for i in indices[0]]


class VectorStore:
    def __init__(self, model_name="intfloat/e5-base-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.text_chunks = []

    def build_index(self, chunks):
        self.text_chunks = chunks
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))

    def search(self, query: str, top_k: int = 8):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), top_k)
        return [self.text_chunks[i] for i in indices[0]]

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({
                "text_chunks": self.text_chunks,
                "index": faiss.serialize_index(self.index),
                "model_name": self.model_name
            }, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.text_chunks = data["text_chunks"]
            self.index = faiss.deserialize_index(data["index"])
            self.model_name = data["model_name"]
            self.model = SentenceTransformer(self.model_name)

