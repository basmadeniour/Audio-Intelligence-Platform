import yt_dlp
from pathlib import Path
from typing import List, Dict

class YouTubeService:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_audio(self, url: str) -> List[Dict]:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True,
            'no_overwrites': True,
        }
        
        downloaded_files = []
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if 'entries' not in info:
                    title = info.get('title', 'audio')
                    for file in self.output_dir.iterdir():
                        if title in file.stem and file.suffix in ['.webm', '.m4a', '.mp3']:
                            downloaded_files.append({
                                'title': title,
                                'path': str(file),
                                'duration': info.get('duration', 0)
                            })
                            break
                else:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', 'audio')
                            for file in self.output_dir.iterdir():
                                if title in file.stem and file.suffix in ['.webm', '.m4a', '.mp3']:
                                    downloaded_files.append({
                                        'title': title,
                                        'path': str(file),
                                        'duration': entry.get('duration', 0)
                                    })
                                    break
            
            return downloaded_files
            
        except Exception as e:
            raise Exception(f"Failed to download from YouTube: {str(e)}")
    
    def cleanup(self):
        for file in self.output_dir.iterdir():
            if file.suffix in ['.webm', '.m4a', '.mp3']:
                try:
                    file.unlink()
                except:
                    pass