from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class HighlightsService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
    
    def extract_highlights(self, text: str, top_k: int = 3) -> list:
        try:
            from app.services.text_cleaner import TextCleaner
            cleaned_text = TextCleaner.clean_text(text)
            
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 30]
            
            if len(sentences) < 2:
                return [text[:200]] if text else []
            
            tfidf_matrix = self.vectorizer.fit_transform(sentences)
            scores = tfidf_matrix.sum(axis=1).A1
            top_indices = scores.argsort()[-top_k:][::-1]
            
            highlights = [sentences[i] for i in top_indices if len(sentences[i]) > 30]
            return highlights[:top_k]
            
        except Exception as e:
            sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 30]
            sentences.sort(key=len, reverse=True)
            return sentences[:top_k]