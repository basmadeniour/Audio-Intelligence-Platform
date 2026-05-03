from typing import List, Dict, Any

class ChaptersService:
    def detect(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not segments:
            return []
        
        chapters = []
        current_chapter = {
            "start": segments[0].get("start", 0),
            "end": segments[0].get("end", 0),
            "text": segments[0].get("text", ""),
            "topic": ""
        }
        
        for i in range(1, len(segments)):
            gap = segments[i].get("start", 0) - segments[i-1].get("end", 0)
            
            if gap > 2.0:
                current_chapter["end"] = segments[i-1].get("end", 0)
                chapters.append(current_chapter)
                
                current_chapter = {
                    "start": segments[i].get("start", 0),
                    "end": segments[i].get("end", 0),
                    "text": segments[i].get("text", ""),
                    "topic": ""
                }
            else:
                current_chapter["end"] = segments[i].get("end", 0)
                current_chapter["text"] += " " + segments[i].get("text", "")
        
        if current_chapter["text"]:
            chapters.append(current_chapter)
        
        for chapter in chapters:
            words = chapter["text"].split()[:10]
            chapter["topic"] = " ".join(words) + ("..." if len(chapter["text"].split()) > 10 else "")
            chapter["duration"] = round(chapter["end"] - chapter["start"], 2)
        
        return chapters