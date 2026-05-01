from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR = BASE_DIR / "data" / "uploads"
    OUTPUT_DIR = BASE_DIR / "data" / "outputs"
    
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    WHISPER_MODEL_SIZE = "base"
    
config = Config()