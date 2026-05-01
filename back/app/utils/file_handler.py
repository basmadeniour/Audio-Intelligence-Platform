import shutil
from pathlib import Path
from fastapi import UploadFile
from datetime import datetime
import re

def save_upload_file(upload_file: UploadFile, upload_dir: Path) -> Path:
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = upload_file.filename
    extension = Path(original_name).suffix
    
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', original_name[:-len(extension)] if extension else original_name)
    safe_filename = f"{timestamp}_{safe_name}{extension}"
    safe_filename = safe_filename.replace(' ', '_')
    
    file_path = upload_dir / safe_filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        upload_file.file.seek(0)
        
        print(f"File saved: {file_path}")
        print(f"File size: {file_path.stat().st_size} bytes")
        
        return file_path
        
    except Exception as e:
        raise Exception(f"Failed to save file: {str(e)}")