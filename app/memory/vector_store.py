import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Loads a sentence embedding model from HuggingFace
        self.model = SentenceTransformer(model_name)
        self.docs = []  # list to hold documents and their embeddings

    def add(self, doc_id, text, meta=None):
        # Converts text into vector (embedding)
        vec = self.model.encode(text, convert_to_numpy=True)
        # Stores document with vector and metadata
        self.docs.append({"id": doc_id, "text": text, "meta": meta or {}, "vector": vec})

    def search(self, query, top_k=5):
        # If no documents in store, return empty
        if not self.docs:
            return []
        # Encode the query into vector
        qv = self.model.encode(query, convert_to_numpy=True)
        # Computing cosine similarity between query and all docs
        sims = cosine_similarity([qv], [d["vector"] for d in self.docs])[0]
        # Rank documents by similarity score
        ranked = sorted(zip(sims, self.docs), key=lambda x: x[0], reverse=True)
        # Return top-k documents
        return [
            {"id": d["id"], "text": d["text"], "meta": d["meta"], "score": float(s)}
            for s, d in ranked[:top_k]
        ]
