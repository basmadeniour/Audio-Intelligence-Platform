from transformers import pipeline
import torch

class SummarizerService:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1
        )
    
    def summarize(self, text: str, max_length: int = 150) -> str:
        try:
            if len(text) > 1024:
                text = text[:1024]
            
            result = self.summarizer(text, max_length=max_length, min_length=30)
            return result[0]['summary_text']
        except Exception as e:
            return f"Summarization failed: {str(e)}"