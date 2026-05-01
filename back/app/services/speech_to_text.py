import whisper
from pathlib import Path
from app.core.config import config
import os

class SpeechToTextService:
    def __init__(self):
        ffmpeg_path = r"C:\Users\3B\AppData\Local\Temp\ffmpeg\bin"
        
        if os.path.exists(ffmpeg_path):
            os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")
            print(f"FFmpeg added from: {ffmpeg_path}")
        else:
            print(f"FFmpeg not found at: {ffmpeg_path}")
        
        self.model = whisper.load_model(config.WHISPER_MODEL_SIZE)
        print("Whisper model loaded successfully")
    
    def transcribe(self, audio_path: Path) -> str:
        try:
            print(f"Transcribing: {audio_path.name}")
            
            if not audio_path.exists():
                raise FileNotFoundError(f"File not found: {audio_path}")
            
            result = self.model.transcribe(str(audio_path), fp16=False)
            
            print(f"Transcription completed successfully")
            return result["text"]
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error: {error_msg}")
            raise Exception(f"Speech to text failed: {error_msg}")
    
    def transcribe_with_segments(self, audio_path: Path) -> dict:
        try:
            print(f"Transcribing with segments: {audio_path.name}")
            
            if not audio_path.exists():
                raise FileNotFoundError(f"File not found: {audio_path}")
            
            result = self.model.transcribe(str(audio_path), fp16=False)
            
            print(f"Transcription completed successfully")
            return {
                "text": result["text"],
                "segments": result.get("segments", [])
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error: {error_msg}")
            raise Exception(f"Speech to text failed: {error_msg}")