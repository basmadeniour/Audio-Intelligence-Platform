import os
from pathlib import Path
from groq import Groq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechToTextService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
            self.available = True
            logger.info("SpeechToTextService initialized successfully")
        else:
            self.client = None
            self.available = False
            logger.error("GROQ_API_KEY not found in environment variables")
    
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
        
        logger.info(f"Starting transcription for: {audio_path}")
        logger.info(f"File size: {audio_path.stat().st_size} bytes")
        
        try:
            with open(audio_path, "rb") as file:
                file_content = file.read()
                logger.info(f"File read successfully, size: {len(file_content)} bytes")
                
                logger.info("Calling Groq API for transcription")
                transcription = self.client.audio.transcriptions.create(
                    file=(audio_path.name, file_content),
                    model="whisper-large-v3-turbo",
                    response_format="verbose_json"
                )
            
            logger.info("Transcription completed successfully")
            
            segments = []
            if hasattr(transcription, 'segments') and transcription.segments:
                logger.info(f"Processing {len(transcription.segments)} segments")
                for seg in transcription.segments:
                    segments.append({
                        "start": getattr(seg, "start", 0),
                        "end": getattr(seg, "end", 0),
                        "text": getattr(seg, "text", "")
                    })
            else:
                logger.warning("No segments found in transcription response")
            
            logger.info(f"Transcription text length: {len(transcription.text)} characters")
            
            return {
                "text": transcription.text,
                "segments": segments
            }
        
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            
            if hasattr(e, 'response'):
                logger.error(f"Response status: {e.response.status if hasattr(e.response, 'status') else 'Unknown'}")
                if hasattr(e.response, 'text'):
                    logger.error(f"Response body: {e.response.text}")
            
            return {
                "text": f"Transcription error: {str(e)}",
                "segments": []
            }