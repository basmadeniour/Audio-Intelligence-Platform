from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.speech_to_text import SpeechToTextService
from app.services.summarizer import SummarizerService
from app.services.keywords import KeywordsService
from app.services.highlights import HighlightsService
from app.services.chapters import ChaptersService
from app.services.translation import TranslationService
from app.services.qa_service import QAService
from app.services.semantic_search import SemanticSearchService
from app.utils.file_handler import save_upload_file
from app.core.config import config
from app.models.schemas import AudioAnalysisResponse, AskRequest, AskResponse, SearchRequest, SearchResponse

router = APIRouter()

stt_service = SpeechToTextService()
summarizer_service = SummarizerService()
keywords_service = KeywordsService()
highlights_service = HighlightsService()
chapters_service = ChaptersService()
translation_service = TranslationService(target_lang=config.TRANSLATION_TARGET_LANG)
semantic_service = SemanticSearchService()
qa_service = QAService()
qa_service.set_semantic_service(semantic_service)


@router.post("/transcribe", response_model=AudioAnalysisResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.mp4')):
        raise HTTPException(400, "Unsupported file type")
    
    try:
        audio_path = save_upload_file(file, config.UPLOAD_DIR)
        
        transcript_result = stt_service.transcribe_with_segments(audio_path)
        transcript = transcript_result["text"]
        segments = transcript_result["segments"]
        
        semantic_service.index_segments(segments)
        
        summary = summarizer_service.summarize(transcript)
        keywords = keywords_service.extract_keywords(transcript)
        highlights = highlights_service.extract_highlights(transcript)
        chapters = chapters_service.detect(segments)
        translated_text = translation_service.translate(transcript)
        
        return AudioAnalysisResponse(
            transcript=transcript,
            summary=summary,
            keywords=keywords,
            highlights=highlights,
            chapters=chapters,
            highlights_with_time=[],
            translated_text=translated_text
        )
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@router.post("/search", response_model=list[SearchResponse])
async def search_transcript(request: SearchRequest):
    results = semantic_service.search(request.query, request.top_k)
    return [
        SearchResponse(
            text=r["text"],
            start_time=r["start"],
            end_time=r["end"]
        )
        for r in results
    ]


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    result = qa_service.ask_with_sources(request.question, request.top_k)
    return AskResponse(
        question=request.question,
        answer=result["answer"],
        confidence=result.get("confidence", 0.0),
        sources=result.get("sources", [])
    )