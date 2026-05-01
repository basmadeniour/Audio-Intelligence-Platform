from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.speech_to_text import SpeechToTextService
from app.services.summarizer import SummarizerService
from app.services.keywords import KeywordsService
from app.services.highlights import HighlightsService
from app.services.emotion import EmotionService
from app.services.audio_stats import AudioStatsService
from app.services.chapters import ChaptersService
from app.services.highlights import HighlightsWithTimeService
from app.utils.file_handler import save_upload_file
from app.core.config import config
from app.models.schemas import AudioAnalysisResponse

router = APIRouter()

stt_service = SpeechToTextService()
summarizer_service = SummarizerService()
keywords_service = KeywordsService()
highlights_service = HighlightsService()
emotion_service = EmotionService()
audio_stats_service = AudioStatsService()
chapters_service = ChaptersService()
highlights_time_service = HighlightsWithTimeService()

@router.post("/transcribe", response_model=AudioAnalysisResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.mp4')):
        raise HTTPException(400, "Unsupported file type")
    
    try:
        audio_path = save_upload_file(file, config.UPLOAD_DIR)
        
        transcript_result = stt_service.transcribe_with_segments(audio_path)
        transcript = transcript_result["text"]
        segments = transcript_result["segments"]
        
        summary = summarizer_service.summarize(transcript)
        keywords = keywords_service.extract_keywords(transcript)
        highlights = highlights_service.extract_highlights(transcript)
        emotion = emotion_service.analyze(transcript)
        audio_stats = audio_stats_service.get_stats(audio_path)
        chapters = chapters_service.detect(segments)
        highlights_with_time = highlights_time_service.extract(segments)
        
        return AudioAnalysisResponse(
            transcript=transcript,
            summary=summary,
            keywords=keywords,
            highlights=highlights,
            emotion=emotion,
            audio_stats=audio_stats,
            chapters=chapters,
            highlights_with_time=highlights_with_time
        )
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")