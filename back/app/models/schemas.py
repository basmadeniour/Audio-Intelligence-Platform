from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AudioAnalysisResponse(BaseModel):
    transcript: str
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    highlights: Optional[List[str]] = None
    chapters: Optional[List[Dict[str, Any]]] = None
    highlights_with_time: Optional[List[Dict[str, Any]]] = None
    translated_text: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResponse(BaseModel):
    text: str
    start_time: float
    end_time: float

class AskRequest(BaseModel):
    question: str
    top_k: int = 3

class AskResponse(BaseModel):
    question: str
    answer: str
    confidence: float = 0.0
    sources: Optional[List[Dict[str, Any]]] = None

class YouTubeRequest(BaseModel):
    url: str
    index_for_semantic: bool = False