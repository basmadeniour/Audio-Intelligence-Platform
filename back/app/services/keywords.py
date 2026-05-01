from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('stopwords')

class KeywordsService:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update([
            'you', 'your', 'the', 'that', 'and', 'for', 'are', 'with', 'can',
            'will', 'have', 'this', 'but', 'not', 'all', 'from', 'get', 'just',
            'like', 'more', 'what', 'when', 'then', 'there', 'would', 'could',
            'them', 'they', 'their', 'was', 'were', 'been', 'being', 'into'
        ])
    
    def extract_keywords(self, text: str, top_k: int = 7) -> list:
        try:
            from app.services.text_cleaner import TextCleaner
            cleaned_text = TextCleaner.clean_text(text)
            
            vectorizer = TfidfVectorizer(
                max_features=20,
                stop_words=list(self.stop_words),
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.9
            )
            
            tfidf_matrix = vectorizer.fit_transform([cleaned_text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            
            top_indices = scores.argsort()[-top_k:][::-1]
            keywords = [feature_names[i] for i in top_indices if scores[i] > 0.1 and len(feature_names[i]) > 3]
            
            return keywords[:top_k]
            
        except Exception as e:
            return self._fallback_keywords(text, top_k)
    
    def _fallback_keywords(self, text: str, top_k: int) -> list:
        from app.services.text_cleaner import TextCleaner
        cleaned_text = TextCleaner.clean_text(text)
        words = cleaned_text.split()
        
        word_count = {}
        for w in words:
            if w not in self.stop_words and len(w) > 3:
                word_count[w] = word_count.get(w, 0) + 1
        
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [w for w, c in sorted_words[:top_k]]