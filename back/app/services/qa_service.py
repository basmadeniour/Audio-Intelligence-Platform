import os
from typing import List, Dict, Any
from groq import Groq

class QAService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.available = True
        else:
            self.client = None
            self.available = False
        self.semantic_service = None
        self.segments_cache = []
    
    def set_semantic_service(self, semantic_service):
        self.semantic_service = semantic_service
    
    def index_segments(self, segments: List[Dict[str, Any]]):
        self.segments_cache = segments
    
    def _search_relevant(self, question: str, top_k: int = 3) -> List[Dict]:
        question_words = set(question.lower().split())
        scored = []
        
        for seg in self.segments_cache:
            text = seg.get("text", "").lower()
            score = sum(1 for word in question_words if word in text)
            if score > 0:
                scored.append((seg, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [seg for seg, _ in scored[:top_k]]
    
    def ask(self, question: str, top_k: int = 3) -> dict:
        if not self.available:
            return {
                "answer": "GROQ_API_KEY not configured. Please add it to .env file",
                "sources": [],
                "confidence": 0.0
            }
        
        if not self.segments_cache and self.semantic_service is None:
            return {
                "answer": "No transcript loaded. Please process an audio file first.",
                "sources": [],
                "confidence": 0.0
            }
        
        if self.semantic_service:
            results = self.semantic_service.search(question, top_k)
        else:
            results = self._search_relevant(question, top_k)
        
        if not results:
            return {
                "answer": "No relevant content found to answer your question.",
                "sources": [],
                "confidence": 0.0
            }
        
        context = " ".join([r.get("text", r.get("text", "")) for r in results])
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Answer the question based ONLY on the provided context. If the answer is not in the context, say 'I cannot find this in the transcript'."},
                    {"role": "user", "content": f"Context: {context[:3000]}\n\nQuestion: {question}"}
                ],
                temperature=0.1
            )
            answer = response.choices[0].message.content
            confidence = 0.9 if "cannot find" not in answer.lower() else 0.2
        except Exception as e:
            answer = f"Error: {str(e)}"
            confidence = 0.0
        
        sources = [
            {
                "text": r.get("text", ""),
                "start_time": r.get("start", 0),
                "end_time": r.get("end", 0)
            }
            for r in results
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }