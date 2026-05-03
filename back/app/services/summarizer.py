import os
from groq import Groq

class SummarizerService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.available = True
        else:
            self.client = None
            self.available = False
    
    def summarize(self, text: str, max_length: int = 150) -> str:
        if not self.available:
            return "Error: GROQ_API_KEY not configured. Please add it to .env file"
        
        if len(text) < 100:
            return text
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"Summarize the following text in {max_length} words or less. Be concise and capture the main ideas."},
                    {"role": "user", "content": text[:4000]}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Summarization error: {str(e)}"