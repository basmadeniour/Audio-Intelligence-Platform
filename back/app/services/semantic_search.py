import os
import numpy as np
from groq import Groq
from typing import List, Dict, Any

class SemanticSearchService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.available = True
        else:
            self.client = None
            self.available = False
        self.text_chunks = []
        self.metadata = []
        self.embeddings = []
    
    def _get_embedding(self, text: str) -> List[float]:
        if not self.available:
            return []
        
        try:
            response = self.client.embeddings.create(
                model="nomic-embed-text-v1.5",
                input=[text]
            )
            return response.embeddings[0].embedding
        except Exception as e:
            print(f"Embedding error: {e}")
            return []
    
    def index_segments(self, segments: List[Dict[str, Any]]):
        self.text_chunks = [seg.get("text", "") for seg in segments]
        self.metadata = [
            {
                "start": seg.get("start", 0),
                "end": seg.get("end", 0),
                "text": seg.get("text", "")
            }
            for seg in segments
        ]
        
        if not self.text_chunks:
            return
        
        self.embeddings = []
        for chunk in self.text_chunks:
            embedding = self._get_embedding(chunk)
            if embedding:
                self.embeddings.append(embedding)
            else:
                self.embeddings.append([0] * 768)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.embeddings or not self.available:
            return []
        
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return self._fallback_search(query, top_k)
        
        similarities = []
        for idx, emb in enumerate(self.embeddings):
            if emb and not all(v == 0 for v in emb):
                sim = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb) + 1e-8)
                similarities.append((idx, sim))
            else:
                similarities.append((idx, 0))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in similarities[:top_k] if idx < len(self.metadata)]
        
        results = []
        for idx in top_indices:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        return results
    
    def _fallback_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_words = set(query.lower().split())
        scored = []
        
        for idx, meta in enumerate(self.metadata):
            text = meta.get("text", "").lower()
            score = sum(1 for word in query_words if word in text)
            if score > 0:
                scored.append((idx, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, _ in scored[:top_k]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        return results
    
    def clear_index(self):
        self.text_chunks = []
        self.metadata = []
        self.embeddings = []
    
    def is_indexed(self) -> bool:
        return len(self.text_chunks) > 0