import re

class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def remove_repetitions(text: str) -> str:
        words = text.split()
        unique_words = []
        for w in words:
            if len(unique_words) == 0 or w != unique_words[-1]:
                unique_words.append(w)
        return ' '.join(unique_words)