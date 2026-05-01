from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AudioAnalysisResponse(BaseModel):
    transcript: str
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    highlights: Optional[List[str]] = None
    emotion: Optional[Dict[str, Any]] = None
    audio_stats: Optional[Dict[str, Any]] = None
    chapters: Optional[List[Dict[str, Any]]] = None
    highlights_with_time: Optional[List[Dict[str, Any]]] = None
    
class HealthResponse(BaseModel):
    status: str
    message: str