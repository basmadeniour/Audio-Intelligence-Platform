import os
from typing import List, Dict, Any
from groq import Groq

class HighlightsService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    def extract_highlights(self, text: str, top_k: int = 5) -> list:
        if len(text) < 200:
            return [text]
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"Extract the {top_k} most important highlights from the text. Return each highlight on a new line."},
                {"role": "user", "content": text[:3000]}
            ],
            temperature=0.3
        )
        highlights_text = response.choices[0].message.content
        highlights = [h.strip() for h in highlights_text.split('\n') if h.strip()]
        return highlights[:top_k] if highlights else [text[:200]]

class HighlightsWithTimeService:
    def extract(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        highlights = []
        for seg in segments:
            text = seg.get("text", "").strip()
            if len(text) > 50:
                highlights.append({
                    "text": text,
                    "start": seg.get("start", 0),
                    "end": seg.get("end", 0)
                })
        return highlights[:10]