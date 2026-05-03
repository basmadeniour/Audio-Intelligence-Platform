import os
from deep_translator import GoogleTranslator

class TranslationService:
    def __init__(self, target_lang: str = None):
        self.target_lang = target_lang or os.getenv("TRANSLATION_TARGET_LANG", "ar")
        self.translator = None
        self._initialize_translator()
    
    def _initialize_translator(self):
        try:
            self.translator = GoogleTranslator(source='en', target=self.target_lang)
        except Exception:
            self.translator = None
    
    def translate(self, text: str, target_lang: str = None) -> str:
        if self.translator is None:
            return text
        
        try:
            lang = target_lang or self.target_lang
            if len(text) > 5000:
                text = text[:5000] + "..."
            
            if lang != self.target_lang:
                temp_translator = GoogleTranslator(source='en', target=lang)
                return temp_translator.translate(text)
            
            return self.translator.translate(text)
        except Exception:
            return text