from pathlib import Path
import os

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR = BASE_DIR / "data" / "uploads"
    OUTPUT_DIR = BASE_DIR / "data" / "outputs"
    YOUTUBE_DOWNLOAD_DIR = BASE_DIR / "data" / "youtube_downloads"
    
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    YOUTUBE_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TRANSLATION_TARGET_LANG = os.getenv("TRANSLATION_TARGET_LANG", "ar")

config = Config()