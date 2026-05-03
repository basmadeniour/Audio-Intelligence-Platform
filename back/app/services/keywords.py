import os
from groq import Groq

class KeywordsService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.available = True
        else:
            self.client = None
            self.available = False
    
    def extract_keywords(self, text: str, top_k: int = 7) -> list:
        if not self.available:
            return self._fallback_keywords(text, top_k)
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Extract the {top_k} most important keywords from the text. Return only the keywords as a comma-separated list, nothing else."},
                    {"role": "user", "content": text[:3000]}
                ],
                temperature=0.2
            )
            keywords_text = response.choices[0].message.content
            keywords = [k.strip().lower() for k in keywords_text.replace('\n', ',').split(',') if k.strip()]
            return keywords[:top_k]
        except Exception:
            return self._fallback_keywords(text, top_k)
    
    def _fallback_keywords(self, text: str, top_k: int) -> list:
        stop_words = {'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'that', 
                     'for', 'you', 'with', 'this', 'are', 'as', 'be', 'on', 'at'}
        words = text.lower().split()
        word_count = {}
        for w in words:
            if w not in stop_words and len(w) > 3:
                word_count[w] = word_count.get(w, 0) + 1
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [w for w, c in sorted_words[:top_k]]