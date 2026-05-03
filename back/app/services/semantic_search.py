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
        
        response = self.client.embeddings.create(
            model="nomic-embed-text-v1.5",
            input=text
        )
        return response.embeddings[0].embedding
    
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
            self.embeddings.append(embedding)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.embeddings or not self.available:
            return []
        
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return []
        
        similarities = []
        for idx, emb in enumerate(self.embeddings):
            sim = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
            similarities.append((idx, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in similarities[:top_k]]
        
        results = []
        for idx in top_indices:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        return results
    
    def clear_index(self):
        self.text_chunks = []
        self.metadata = []
        self.embeddings = []
    
    def is_indexed(self) -> bool:
        return len(self.text_chunks) > 0