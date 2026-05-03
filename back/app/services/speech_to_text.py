import os
from pathlib import Path
from groq import Groq

class SpeechToTextService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.available = True
        else:
            self.client = None
            self.available = False
    
    def transcribe(self, audio_path: Path) -> str:
        if not self.available:
            return "Error: GROQ_API_KEY not configured. Please add it to .env file"
        
        result = self.transcribe_with_segments(audio_path)
        return result["text"]
    
    def transcribe_with_segments(self, audio_path: Path) -> dict:
        if not self.available:
            return {
                "text": "Error: GROQ_API_KEY not configured. Please add it to .env file",
                "segments": []
            }
        
        try:
            with open(audio_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(audio_path.name, file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json"
                )
            
            segments = []
            if hasattr(transcription, 'segments') and transcription.segments:
                for seg in transcription.segments:
                    segments.append({
                        "start": getattr(seg, "start", 0),
                        "end": getattr(seg, "end", 0),
                        "text": getattr(seg, "text", "")
                    })
            
            return {
                "text": transcription.text,
                "segments": segments
            }
        
        except Exception as e:
            return {
                "text": f"Transcription error: {str(e)}",
                "segments": []
            }