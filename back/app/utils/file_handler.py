import shutil
from pathlib import Path
from fastapi import UploadFile
from datetime import datetime
import re
import threading
import time

class FileHandler:
    def __init__(self):
        self.auto_delete_seconds = 300
    
    def save_upload_file(self, upload_file: UploadFile, upload_dir: Path) -> Path:
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
            
            self._schedule_deletion(file_path)
            
            return file_path
            
        except Exception as e:
            raise Exception(f"Failed to save file: {str(e)}")
    
    def _schedule_deletion(self, file_path: Path):
        def delete_file():
            time.sleep(self.auto_delete_seconds)
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"Auto-deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
        
        thread = threading.Thread(target=delete_file, daemon=True)
        thread.start()
    
    def delete_file_immediately(self, file_path: Path):
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Deleted: {file_path}")
                return True
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
                return False
        return False
    
    def set_auto_delete_delay(self, seconds: int):
        self.auto_delete_seconds = seconds


file_handler = FileHandler()
save_upload_file = file_handler.save_upload_file